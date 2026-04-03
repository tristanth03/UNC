"""
parser.py — reads a .ipynb file and extracts structured cells
"""
import json, re


def load_notebook(nb_path):
    with open(nb_path, encoding='utf-8') as f:
        return json.load(f)


def parse_header_cell(src):
    """
    Cell 0 must contain:
      # Title
      **Category: X**
    Missing either → 'Title missing' / 'Category missing'
    """
    title, category = None, None
    for line in src.splitlines():
        line = line.strip()
        if re.match(r'^#\s+', line) and not re.match(r'^##', line):
            title = re.sub(r'^#\s+', '', line).strip()
        m = re.match(r'\*\*Category:\s*(.+?)\*\*', line)
        if m:
            category = m.group(1).strip()
    return title or 'Title missing', category or 'Category missing'


def extract_heading(src):
    """Return (level, text) if first non-empty line is a heading, else None."""
    for line in src.splitlines():
        line = line.strip()
        if not line:
            continue
        m = re.match(r'^(#{1,5})\s+(.*)', line)
        if m:
            return len(m.group(1)), m.group(2).strip()
        return None
    return None


def get_cells(nb):
    """
    Return (title, category, remaining_cells).
    Cell 0 is consumed as the header; the rest are returned as-is.
    """
    cells = nb['cells']
    if cells and cells[0]['cell_type'] == 'markdown':
        title, category = parse_header_cell(''.join(cells[0]['source']))
        return title, category, cells[1:]
    return 'Title missing', 'Category missing', cells