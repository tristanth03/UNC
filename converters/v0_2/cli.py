"""
cli.py — entry point for nb2report
Usage: python3 cli.py <notebook.ipynb> <name>

Output is always saved to:  reports/<name>.html
The reports/ directory is created if it does not exist.
"""
import sys
from pathlib import Path
from converter import convert

REPORTS_DIR = Path(__file__).parent / 'reports'

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 cli.py <notebook.ipynb> <name>")
        print("Output:  reports/<name>.html")
        sys.exit(1)

    nb_path  = Path(sys.argv[1])
    name     = sys.argv[2]
    out_path = REPORTS_DIR / f'{name}.html'

    REPORTS_DIR.mkdir(exist_ok=True)
    convert(nb_path, out_path)

if __name__ == '__main__':
    main()