"""
converter.py — orchestrates parser, renderer, and template into a final HTML file
"""
import html as htmllib
from pathlib import Path

from parser   import load_notebook, get_cells
from renderer import TOC, render_cells
from template import assemble


def esc(s):
    return htmllib.escape(s, quote=False)


def convert(nb_path: Path, out_path: Path):
    nb = load_notebook(nb_path)
    title, category, cells = get_cells(nb)

    toc = TOC()
    body_parts = render_cells(cells, toc)

    html = assemble(
        title_e  = esc(title),
        cat_e    = esc(category),
        toc_html = toc.render(),
        body     = '\n'.join(body_parts),
    )

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Written: {out_path}')
