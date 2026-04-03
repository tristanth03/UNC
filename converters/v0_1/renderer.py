"""
renderer.py — converts notebook cells to HTML fragments
"""
import re, html as htmllib
from parser import extract_heading


def esc(s):
    return htmllib.escape(s, quote=False)


# ── Math ─────────────────────────────────────────────────────────────────────

# Dollar signs must be matched with re.escape(chr(36)) to get a genuine
# literal-dollar pattern.  Using \$ in a raw-string pattern produces the
# two-char sequence \$ which some regex builds treat as backslash + EOL-anchor.

_D  = re.escape(chr(36))                          # literal $  →  \$
_DD = _D + _D                                      # literal $$ →  \$\$
# Content: \$ (backslash+dollar) is treated as an escape unit so it does not
# act as a closing delimiter. This handles LaTeX \$1 (literal dollar sign).
_MATH_CONTENT = r'(?:\\' + _D + r'|[^' + _D + r'\n])+?'
_INLINE_MATH  = re.compile(_D + r'(' + _MATH_CONTENT + r')' + _D)
_DISPLAY_MATH = re.compile(_DD + r'\s*([\s\S]+?)\s*' + _DD)


def convert_math(src):
    """$$...$$ → \\[...\\]   $...$ → \\(...\\)"""
    src = _DISPLAY_MATH.sub(lambda m: r'\[' + m.group(1) + r'\]', src)
    src = _INLINE_MATH.sub( lambda m: r'\(' + m.group(1) + r'\)', src)
    return src


def strip_math(text):
    """Remove $...$ and $$...$$ spans from text — used only for slug generation."""
    text = _DISPLAY_MATH.sub('', text)
    text = _INLINE_MATH.sub('', text)
    return re.sub(r'\s+', ' ', text).strip()


# ── Markdown prose ────────────────────────────────────────────────────────────

def _is_table(lines):
    """True if lines form a GFM pipe table (header | separator | rows...)."""
    if len(lines) < 2:
        return False
    if not lines[0].strip().startswith('|'):
        return False
    return bool(re.match(r'^\|[\s|:-]+\|$', lines[1].strip()))


def _render_table(lines):
    """Convert GFM pipe-table lines to an HTML <table>."""
    def split_row(line):
        line = line.strip().strip('|')
        return [c.strip() for c in line.split('|')]

    def fmt_cell(c):
        c = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', c)
        c = re.sub(r'`([^`]+)`', r'<code>\1</code>', c)
        c = _INLINE_MATH.sub(lambda m: r'\(' + m.group(1) + r'\)', c)
        return c

    header = split_row(lines[0])
    body_rows = [split_row(l) for l in lines[2:]]
    th = ''.join(f'<th>{fmt_cell(c)}</th>' for c in header)
    rows = ''.join(
        '<tr>' + ''.join(f'<td>{fmt_cell(c)}</td>' for c in row) + '</tr>'
        for row in body_rows
    )
    return (
        '<div class="tbl-wrap">'
        f'<table><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table>'
        '</div>'
    )


def md_to_html(src):
    """
    Minimal markdown:
    - pipe tables → <table>
    - **bold**
    - `code`
    - math (via convert_math)
    - display math blocks are kept block-level (never inside <p>)
    - paragraphs split by blank lines
    """
    def fmt(s):
        s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
        s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
        return s

    # ── Pass 1: extract pipe-table blocks before any other processing ──
    table_placeholder = {}
    result_lines = []
    raw_lines = src.split('\n')
    i = 0
    while i < len(raw_lines):
        if raw_lines[i].strip().startswith('|'):
            block = []
            while i < len(raw_lines) and raw_lines[i].strip().startswith('|'):
                block.append(raw_lines[i])
                i += 1
            if _is_table(block):
                key = f'\x00TABLE{len(table_placeholder)}\x00'
                table_placeholder[key] = _render_table(block)
                result_lines.append(key)
            else:
                result_lines.extend(block)
        else:
            result_lines.append(raw_lines[i])
            i += 1
    src = '\n'.join(result_lines)

    # ── Pass 2: math conversion + paragraph splitting ──
    src = convert_math(src)
    DISP = re.compile(r'(\\\[[\s\S]+?\\\])')
    parts = DISP.split(src)
    out = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if part.startswith(r'\['):
            out.append(part)
        else:
            for p in re.split(r'\n{2,}', part):
                p = p.strip()
                if not p:
                    continue
                if p in table_placeholder:
                    out.append(table_placeholder[p])
                else:
                    out.append(f'<p>{fmt(p)}</p>')
    return '\n'.join(out)


# ── TOC ───────────────────────────────────────────────────────────────────────

class TOC:
    def __init__(self):
        self.entries = []
        self._counts = {}

    def add(self, level, text):
        plain = strip_math(text)           # plain text used only for the slug
        sid = re.sub(r'[^a-z0-9]+', '-', plain.lower()).strip('-')
        n = self._counts.get(sid, 0)
        self._counts[sid] = n + 1
        if n:
            sid = f'{sid}-{n}'
        label = convert_math(text)         # math converted for display in TOC
        self.entries.append((level, label, sid))
        return sid

    def render(self):
        lines = []
        for level, label, sid in self.entries:
            cls = {2: 'h2', 3: 'h3', 4: 'h4', 5: 'h5'}.get(level, 'h5')
            lines.append(f'<a href="#{sid}" class="{cls}">{label}</a>')
        return '\n  '.join(lines)


# ── Cell renderers ────────────────────────────────────────────────────────────

_code_counter = [0]

# Match plt.plot( lines that have an inline # comment
_PLOT_COMMENT = re.compile(r'^\s*plt\.plot\s*\(.*#\s*(.+)$')


def _extract_plot_captions(src):
    """
    Split source on plt.show() calls; for each segment return the text of
    the first inline comment on a plt.plot(...) line, or None if absent.
    One caption per plt.show() call = one caption per output image.
    """
    segments = re.split(r'\bplt\.show\s*\(\s*\)', src)
    captions = []
    for seg in segments[:-1]:          # drop trailing fragment after last show()
        cap = None
        for line in seg.splitlines():
            m = _PLOT_COMMENT.match(line)
            if m:
                cap = m.group(1).strip()
                break
        captions.append(cap)
    return captions


def render_code_cell(src, outputs):
    _code_counter[0] += 1
    cid = f'code-{_code_counter[0]}'
    parts = [
        f'<button class="ctog" onclick="tog(\'{cid}\',this)">'
        f'<span class="ar">&#9658;</span> Source code</button>',
        f'<div class="cdraw" id="{cid}"><pre>{esc(src)}</pre></div>',
    ]

    png_outputs = [
        o['data']['image/png']
        for o in outputs
        if o.get('data', {}).get('image/png')
    ]

    if png_outputs:
        captions = _extract_plot_captions(src)
        for i, b64 in enumerate(png_outputs):
            cap = captions[i] if i < len(captions) else None
            cap_html = (
                f'<div class="plot-cap">{esc(cap)}</div>' if cap else ''
            )
            parts.append(
                f'<figure class="plot-fig">'
                f'{cap_html}'
                f'<img class="plot-img" src="data:image/png;base64,{b64}"'
                f' alt="{esc(cap or "plot")}">'
                f'</figure>'
            )

    return '\n'.join(parts)


def render_tags(tags):
    if not tags:
        return ''
    return ''.join(f'<span class="tag">{esc(t)}</span> ' for t in tags) + '<br>\n'


def render_markdown_cell(src, tags, toc):
    h = extract_heading(src)
    if h:
        level, text = h
        if level == 1:
            return ''   # title — handled in header
        sid = toc.add(level, text)
        cls = {2: 'stitle', 3: 'sstitle', 4: 'ssstitle', 5: 'sssstitle'}.get(level, 'sssstitle')
        body = convert_math(text)          # math converted on raw text, no esc() first
        return f'<h{level} class="{cls}" id="{sid}">{body}</h{level}>\n'
    return render_tags(tags) + md_to_html(src) + '\n'


def render_cells(cells, toc):
    """Render all remaining cells to a list of HTML strings."""
    parts = []
    for cell in cells:
        src = ''.join(cell['source']).strip()
        if not src:
            continue
        tags = cell.get('metadata', {}).get('tags', [])
        if cell['cell_type'] == 'markdown':
            parts.append(render_markdown_cell(src, tags, toc))
        elif cell['cell_type'] == 'code':
            outputs = cell.get('outputs', [])
            parts.append(render_code_cell(src, outputs))
    return parts