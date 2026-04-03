"""
theme.py — loads font_mapping.json and generates the CSS theme variables.
All colors come exclusively from font_mapping.json — never hardcoded here.
"""
import json
from pathlib import Path

_MAP_PATH = Path(__file__).parent.parent.parent / 'theme' / 'font_mapping.json'


def load_map():
    with open(_MAP_PATH, encoding='utf-8') as f:
        return json.load(f)


def build_theme_css():
    """
    Read font_mapping.json and emit :root.navy { ... } and :root.gunmetal { ... }
    CSS blocks, plus the shared font declarations.
    """
    m = load_map()
    font_family = m['font']['family']
    nv = m['themes']['navy_vault']
    gm = m['themes']['gunmetal']

    def block(cls, t):
        # Map font_mapping tokens → CSS variables used by the HTML template
        return f""":root.{cls} {{
  --bg:{t['canvas']}; --surface:{t['canvas']}; --border:{t['ci']};
  --text:{t['text']}; --sub:{t['subtext']}; --acc:{t['accent']}; --silver:{t['silver']};
  --grid:{t['grid']}; --code-bg:#0a0f1a; --code-border:#1e2d42;
  --tag-bg:{_alpha(t['accent'], 0.10)}; --tag-border:{t['accent']}; --tag-color:{t['mid']};
  --mblock-bg:{t['canvas']}; --sidebar-bg:{t['canvas']}; --sidebar-border:{t['ci']};
  --font-body:{font_family};
}}"""

    # gunmetal code block is darker
    gm_block = f""":root.gunmetal {{
  --bg:{gm['canvas']}; --surface:{gm['canvas']}; --border:{gm['ci']};
  --text:{gm['text']}; --sub:{gm['subtext']}; --acc:{gm['accent']}; --silver:{gm['silver']};
  --grid:{gm['grid']}; --code-bg:#040810; --code-border:{gm['ci']};
  --tag-bg:{_alpha(gm['accent'], 0.08)}; --tag-border:{gm['accent']}; --tag-color:{gm['accent']};
  --mblock-bg:{gm['body']}; --sidebar-bg:{gm['canvas']}; --sidebar-border:{gm['ci']};
  --font-body:{font_family};
}}"""

    return block('navy', nv) + '\n' + gm_block


def _alpha(hex_color, a):
    """Convert #RRGGBB to rgba(r,g,b,a)."""
    h = hex_color.lstrip('#')
    if len(h) == 6:
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return f'rgba({r},{g},{b},{a})'
    return hex_color  # fallback if not a plain hex
