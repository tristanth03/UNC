"""
template.py — static CSS (layout, typography, components) and JS.
Colors are NOT here — they come from theme.py → font_mapping.json.
"""
from theme import build_theme_css

# ── Static CSS (no color values) ─────────────────────────────────────────────

STATIC_CSS = """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html{font-size:16px;}
body{background:var(--bg);color:var(--text);font-family:var(--font-body),'EB Garamond',Georgia,serif;line-height:1.78;-webkit-font-smoothing:antialiased;transition:background .25s,color .25s;overflow-x:auto;}
.shell{display:flex;min-height:100vh;max-width:1600px;margin:0 auto;min-width:700px;}
.toc{width:230px;flex-shrink:0;background:var(--sidebar-bg);border-right:1px solid var(--sidebar-border);padding:2rem 0 4rem;position:sticky;top:0;height:100vh;overflow-y:auto;transition:background .25s,border-color .25s;}
.toc-head{font-family:'JetBrains Mono',monospace;font-size:.58rem;letter-spacing:.18em;text-transform:uppercase;color:var(--acc);padding:0 1.3rem .9rem;border-bottom:1px solid var(--sidebar-border);margin-bottom:.7rem;}
.toc a{display:block;font-family:'JetBrains Mono',monospace;font-size:.63rem;color:var(--sub);text-decoration:none;padding:.25rem 1.3rem;border-left:2px solid transparent;transition:color .12s,background .12s;line-height:1.45;}
.toc a:hover{color:var(--acc);background:var(--tag-bg);}
.toc a.active{color:var(--acc);border-left-color:var(--acc);background:var(--tag-bg);}
.toc a.h2{color:var(--text);font-size:.65rem;margin-top:.3rem;}
.toc a.h3{padding-left:2rem;}
.toc a.h4{padding-left:2.8rem;}
.toc a.h5{padding-left:3.6rem;font-size:.58rem;}
.tswrap{display:flex;align-items:center;gap:.5rem;padding:1rem 1.3rem 0;font-family:'JetBrains Mono',monospace;font-size:.57rem;letter-spacing:.07em;text-transform:uppercase;color:var(--silver);}
.tsw{position:relative;width:32px;height:17px;background:var(--border);border-radius:9px;cursor:pointer;border:1px solid var(--acc);flex-shrink:0;transition:background .2s;}
.tsw::after{content:'';position:absolute;top:2px;left:2px;width:11px;height:11px;background:var(--acc);border-radius:50%;transition:transform .2s;}
.tsw.on::after{transform:translateX(15px);}
.main{flex:1;padding:3.5rem clamp(1.5rem,5vw,5rem) 6rem;min-width:0;}
.rh{margin-bottom:3rem;padding-bottom:2rem;border-bottom:1px solid var(--border);}
.rl{font-family:'JetBrains Mono',monospace;font-size:.6rem;letter-spacing:.16em;text-transform:uppercase;color:var(--acc);margin-bottom:.8rem;}
.rt{font-size:2.3rem;font-weight:500;color:var(--text);margin-bottom:.4rem;line-height:1.15;}
h2.stitle{font-size:1.25rem;font-weight:500;color:var(--text);margin-bottom:1rem;padding-bottom:.4rem;border-bottom:1px solid var(--border);margin-top:2.5rem;}
h3.sstitle{font-size:1.05rem;font-weight:500;color:var(--text);margin:1.6rem 0 .6rem;}
h4.ssstitle{font-size:.95rem;font-weight:400;color:var(--sub);margin:1.3rem 0 .5rem;font-style:italic;}
h5.sssstitle{font-size:.88rem;font-weight:400;color:var(--silver);margin:1.1rem 0 .4rem;font-style:italic;letter-spacing:.01em;}
p{margin-bottom:.85rem;}
strong{font-weight:600;}
code{font-family:'JetBrains Mono',monospace;font-size:.78em;background:var(--tag-bg);padding:1px 4px;border-radius:3px;}
.tag{display:inline-block;font-family:'JetBrains Mono',monospace;font-size:.58rem;letter-spacing:.1em;text-transform:uppercase;background:var(--tag-bg);color:var(--tag-color);border:1px solid var(--tag-border);border-radius:3px;padding:1px 7px;margin-bottom:.55rem;}
.katex-display{margin:1.1rem 0!important;padding:.9rem 1.4rem;background:var(--mblock-bg);border-left:3px solid var(--acc);border-radius:0 4px 4px 0;overflow-x:auto;transition:background .25s;}
.ctog{display:flex;align-items:center;gap:.4rem;font-family:'JetBrains Mono',monospace;font-size:.6rem;letter-spacing:.08em;text-transform:uppercase;color:var(--silver);cursor:pointer;padding:.35rem 0;margin-top:.3rem;border:none;background:none;}
.ctog:hover{color:var(--acc);}
.ar{display:inline-block;transition:transform .18s;}
.ctog.open .ar{transform:rotate(90deg);}
.cdraw{display:none;background:var(--code-bg);border:1px solid var(--code-border);border-radius:4px;padding:.8rem 1rem;margin-top:.3rem;overflow-x:auto;transition:background .25s;}
.cdraw.open{display:block;}
pre{font-family:'JetBrains Mono',monospace;font-size:.7rem;line-height:1.6;color:#a8c0d0;white-space:pre;}
.rf{border-top:1px solid var(--border);padding-top:1.2rem;margin-top:3rem;display:flex;justify-content:space-between;font-family:'JetBrains Mono',monospace;font-size:.6rem;color:var(--silver);}
.toc::-webkit-scrollbar{width:4px;}
.toc::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px;}
"""

# ── JS ────────────────────────────────────────────────────────────────────────

JS = """<script>
function tog(id,btn){document.getElementById(id).classList.toggle('open');btn.classList.toggle('open');}
function toggleTheme(){
  const dark=document.documentElement.classList.toggle('gunmetal');
  document.documentElement.classList.toggle('navy',!dark);
  document.getElementById('tsw').classList.toggle('on',dark);
  document.getElementById('theme-lbl').textContent=dark?'Gunmetal':'Navy Vault';
}
(function(){
  const links=[...document.querySelectorAll('.toc a[href^="#"]')];
  const obs=new IntersectionObserver(entries=>{
    entries.forEach(e=>{
      if(e.isIntersecting){
        links.forEach(l=>l.classList.remove('active'));
        const a=links.find(l=>l.getAttribute('href')==='#'+e.target.id);
        if(a)a.classList.add('active');
      }
    });
  },{rootMargin:'-15% 0px -70% 0px'});
  links.map(l=>document.querySelector(l.getAttribute('href'))).filter(Boolean).forEach(t=>obs.observe(t));
})();
</script>"""


def build_style():
    return f'<style>\n{build_theme_css()}\n{STATIC_CSS}\n</style>'


# ── HTML assembly ─────────────────────────────────────────────────────────────

KATEX_HEAD = [
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">',
    '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>',
    '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"',
    "  onload=\"renderMathInElement(document.body,{delimiters:[",
    "    {left:'\\\\[',right:'\\\\]',display:true},",
    "    {left:'\\\\(',right:'\\\\)',display:false}",
    '  ],throwOnError:false});\"></script>',
]

GOOGLE_FONTS = (
    '<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:'
    'ital,wght@0,400;0,500;1,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">'
)


def assemble(title_e, cat_e, toc_html, body):
    lines = [
        '<!DOCTYPE html>',
        '<html lang="en" class="navy">',
        '<head>',
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        f'<title>{title_e}</title>',
        *KATEX_HEAD,
        GOOGLE_FONTS,
        build_style(),
        '</head>',
        '<body>',
        '<div class="shell">',
        '<nav class="toc" id="toc">',
        '  <div class="toc-head">Contents</div>',
        f'  {toc_html}',
        '  <div class="tswrap">',
        '    <span>Navy</span>',
        '    <div class="tsw" id="tsw" onclick="toggleTheme()"></div>',
        '    <span>Gunmetal</span>',
        '  </div>',
        '</nav>',
        '<main class="main">',
        '  <header class="rh">',
        f'    <div class="rl">{cat_e} Report</div>',
        f'    <h1 class="rt">{title_e}</h1>',
        '  </header>',
        body,
        '  <footer class="rf">',
        f'    <div>{title_e} &mdash; {cat_e} Report</div>',
        '    <div id="theme-lbl">Navy Vault</div>',
        '  </footer>',
        '</main>',
        '</div>',
        JS,
        '</body>',
        '</html>',
    ]
    return '\n'.join(lines)