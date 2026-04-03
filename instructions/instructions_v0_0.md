# nb2report — Converter Instructions

## Purpose
Deterministic notebook-to-HTML report converter.
Input: `.ipynb`. Output: self-contained `.html`. No inference, no additions.

---

## Cell 0 — Header
- Must be a markdown cell with `# Title` and `**Category: X**`
- Missing title → render `Title missing`
- Missing category → render `Category missing`
- Nothing else is read from Cell 0

---

## Structure
- `#` → report title (Cell 0 only)
- `##` → section
- `###` → subsection
- `####` → sub-subsection
- All headings go into the sidebar TOC with correct indent
- TOC active link highlights on scroll

---

## Content Rules
- **Prose verbatim** — no spelling or grammar correction, ever
- **Tags** (cell metadata) → rendered as monospace badge above cell content; no tags = no badge
- **Inline math** `$...$` → `\(...\)`
- **Display math** `$$...$$` → `\[...\]` as block-level element, never inside `<p>`
- **Code cells** → collapsed source drawer only (no output rendering)
- **Empty cells** → skipped

---

## Figures (future)
- Code cells with plot outputs: re-render in Plotly using color map
- If output cannot be re-rendered: nothing shown (no placeholder, no raw PNG)
- Figure labels and inline comments (`# comment`) preserved in figure header

---

## Color Map (`color_map.json`)
Two themes, 8 tokens each:

| Token | Role |
|---|---|
| `canvas` | page background |
| `obs` | primary data (lines, bars, dots, stems) |
| `mid` | forecast / secondary data |
| `cyan` | accent (dark theme forecast) |
| `silver` | muted / secondary |
| `ci` | confidence interval fills |
| `text` | section headers, primary labels |
| `subtext` | tick labels, axis titles |
| `accent` | buttons, slider thumb, active UI |
| `grid` | plot gridlines |

**Navy Vault** — warm off-white background, dark navy text, cyan accent  
**Gunmetal** — deep navy background, silver text, cyan accent

---

## Themes
- Both themes always present, toggled via sidebar switch
- `<html class="navy">` on load (Navy Vault default)
- Toggle switches class to `gunmetal`
- All CSS variables update instantly, no re-render needed

---

## Layout
- Sidebar TOC: fixed width, sticky, scrollable
- Main content: fluid with `clamp()` padding, `max-width: 900px`
- Responsive: sidebar narrows at 900px, hides at 640px
- Works at full-screen, half-screen, third-screen

---

## Math Rendering
- KaTeX via CDN (`auto-render`)
- Delimiters: `\[...\]` display, `\(...\)` inline
- No `$` or `$$` in final HTML
- Display blocks styled with left accent border (theme color)

---

## What the Converter Does NOT Do
- Correct typos or grammar
- Add context, explanations, or summaries
- Infer plot types or re-render matplotlib outputs
- Add any content not present in the notebook
