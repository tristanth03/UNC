# nb2report — Converter Instructions

## Usage
```
python3 cli.py <notebook.ipynb> <name>
```
Output is always saved to `reports/<name>.html`.
The `reports/` directory is created automatically if it does not exist.

---

## Project Structure
```
converters/v0_0/
    cli.py          entry point, argv only
    converter.py    orchestrator
    parser.py       notebook reading, cell parsing
    renderer.py     markdown, math, code, TOC
    template.py     HTML assembly, static CSS, JS
    theme.py        loads font_mapping.json → CSS variables

theme/
    font_mapping.json   single source of truth for all colors and fonts

reports/            generated HTML files (git-ignored)
samples/            example notebooks
instructions/       this file
```

---

## Cell 0 — Header
Must be a markdown cell. Exactly two things are read:
- `# Title` → report title
- `**Category: X**` → category label

Missing title → `Title missing`
Missing category → `Category missing`
Nothing else in Cell 0 is rendered.

---

## Heading Hierarchy
All headings go into the sidebar TOC with correct indentation and are anchor-linked.

| Notebook | HTML | TOC class | Role |
|---|---|---|---|
| `#` | `<h1>` | — | Title (Cell 0 only, not in TOC) |
| `##` | `<h2>` | `h2` | Section |
| `###` | `<h3>` | `h3` | Subsection |
| `####` | `<h4>` | `h4` | Sub-subsection |
| `#####` | `<h5>` | `h5` | Sub-sub-subsection |

TOC active link highlights on scroll.

---

## Content Rules
- **Prose verbatim** — no spelling or grammar correction, ever
- **Tags** (cell metadata `tags: [...]`) → monospace badge rendered above cell content
- **No tags** → no badge, nothing rendered
- **Inline math** `$...$` → `\(...\)` (KaTeX)
- **Display math** `$$...$$` → `\[...\]` block-level, never inside `<p>`
- **Code cells** → collapsed source drawer only
- **Empty cells** → skipped

---

## Math Rendering
- Engine: KaTeX via CDN (`auto-render`)
- Inline delimiter: `\(...\)`
- Display delimiter: `\[...\]`
- Display blocks have left accent border (theme accent color)
- No raw `$` or `$$` in the output HTML

---

## Color Map (`theme/font_mapping.json`)
Single source of truth. **Never hardcode colors anywhere else.**

Two themes — `navy_vault` and `gunmetal` — each with these tokens:

| Token | Role |
|---|---|
| `canvas` | page and sidebar background |
| `obs` | primary data color |
| `mid` | secondary / forecast color |
| `cyan` | accent highlight |
| `silver` | muted text, secondary elements |
| `ci` | borders, confidence interval fills |
| `text` | headings, primary prose |
| `subtext` | tick labels, axis titles, sub-labels |
| `accent` | buttons, toggle, active UI elements |
| `grid` | plot gridlines |

`theme.py` reads this file and maps tokens to CSS variables.
`template.py` consumes CSS variables only — no hex values.

---

## Themes
- Default on load: **Navy Vault** (`<html class="navy">`)
- Toggle in sidebar switches to **Gunmetal** (`class="gunmetal"`)
- All colors update via CSS variables — no JS re-render needed
- Theme label shown in footer

---

## Layout
- Sidebar TOC: `230px`, sticky, scrollable
- Main content: fluid, `clamp()` horizontal padding
- Shell: `max-width: 1600px`, centered, `min-width: 700px`
- Below `700px`: horizontal scroll (layout never collapses)
- Header label: `{category} Report`
- Footer: `{title} — {category} Report` on left, theme name on right

---

## Figures (future)
- Code cells with plot outputs → re-render in Plotly using `font_mapping.json`
- Inline comments (`# comment`) → shown in figure header
- If output cannot be re-rendered → nothing shown
- CSV download button per figure

---

## What the Converter Does NOT Do
- Correct typos or grammar
- Add explanations, summaries, or any content not in the notebook
- Infer or execute code
- Re-render matplotlib/R outputs (yet)
