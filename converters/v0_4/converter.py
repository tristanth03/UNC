"""
converter.py — orchestrates parser, renderer, and template into a final HTML file
"""
import html as htmllib, re
from pathlib import Path

from parser   import load_notebook, get_cells
from renderer import TOC, render_cells
from template import assemble


def esc(s):
    return htmllib.escape(s, quote=False)


_VEGALITE_RE = re.compile(r'application/vnd\.vegalite')


def _extra_head(nb):
    """
    Scan notebook outputs and return CDN <script> tags for any special
    renderer that isn't already bundled in the base template (Plotly is
    always included; Vega-Lite and Bokeh are only added when needed).
    """
    needs_vega  = False
    needs_bokeh = False
    bokeh_ver   = '3.4.2'   # fallback; overridden if found in output

    for cell in nb.get('cells', []):
        for o in cell.get('outputs', []):
            for k in o.get('data', {}):
                if _VEGALITE_RE.search(k):
                    needs_vega = True
                if 'bokeh' in k:
                    needs_bokeh = True
                    bk = o['data'].get('application/vnd.bokeh.show+json', {})
                    if isinstance(bk, dict) and 'version' in bk:
                        bokeh_ver = bk['version']

    scripts = []
    if needs_vega:
        scripts += [
            '<script src="https://cdn.jsdelivr.net/npm/vega@5/build/vega.min.js"></script>',
            '<script src="https://cdn.jsdelivr.net/npm/vega-lite@5/build/vega-lite.min.js"></script>',
            '<script src="https://cdn.jsdelivr.net/npm/vega-embed@6/build/vega-embed.min.js"></script>',
        ]
    if needs_bokeh:
        base = f'https://cdn.bokeh.org/bokeh/release/bokeh-{bokeh_ver}.min.js'
        wdg  = f'https://cdn.bokeh.org/bokeh/release/bokeh-widgets-{bokeh_ver}.min.js'
        scripts += [
            f'<script src="{base}"></script>',
            f'<script src="{wdg}"></script>',
        ]
    return scripts


def convert(nb_path: Path, out_path: Path):
    nb = load_notebook(nb_path)
    title, category, cells = get_cells(nb)

    toc = TOC()
    body_parts = render_cells(cells, toc)

    html = assemble(
        title_e   = esc(title),
        cat_e     = esc(category),
        toc_html  = toc.render(),
        body      = '\n'.join(body_parts),
        extra_head = _extra_head(nb),
    )

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Written: {out_path}')
