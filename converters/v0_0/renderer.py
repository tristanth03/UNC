"""
renderer.py — converts notebook cells to HTML fragments
"""
import re, html as htmllib
from parser import extract_heading


def esc(s):
    return htmllib.escape(s, quote=False)


# ── Math ─────────────────────────────────────────────────────────────────────

def convert_math(src):
    """$$...$$ → \\[...\\]   $...$ → \\(...\\)"""
    src = re.sub(r'\$\$\s*([\s\S]+?)\s*\$\$', lambda m: r'\[' + m.group(1) + r'\]', src)
    src = re.sub(r'\$([^\$\n]+?)\$',           lambda m: r'\(' + m.group(1) + r'\)', src)
    return src


# ── Markdown prose ────────────────────────────────────────────────────────────

def md_to_html(src):
    """
    Minimal markdown:
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
                p = fmt(p.strip())
                if p:
                    out.append(f'<p>{p}</p>')
    return '\n'.join(out)


# ── TOC ───────────────────────────────────────────────────────────────────────

class TOC:
    def __init__(self):
        self.entries = []
        self._counts = {}

    def add(self, level, text):
        sid = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
        n = self._counts.get(sid, 0)
        self._counts[sid] = n + 1
        if n:
            sid = f'{sid}-{n}'
        self.entries.append((level, text, sid))
        return sid

    def render(self):
        lines = []
        for level, text, sid in self.entries:
            cls = {2: 'h2', 3: 'h3', 4: 'h4', 5: 'h5'}.get(level, 'h5')
            lines.append(f'<a href="#{sid}" class="{cls}">{esc(text)}</a>')
        return '\n  '.join(lines)


# ── Cell renderers ────────────────────────────────────────────────────────────

_code_counter = [0]


def render_code_cell(src):
    _code_counter[0] += 1
    cid = f'code-{_code_counter[0]}'
    return (
        f'<button class="ctog" onclick="tog(\'{cid}\',this)">'
        f'<span class="ar">&#9658;</span> Source code</button>\n'
        f'<div class="cdraw" id="{cid}"><pre>{esc(src)}</pre></div>'
    )


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
        return f'<h{level} class="{cls}" id="{sid}">{esc(text)}</h{level}>\n'
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
            parts.append(render_code_cell(src))
    return parts