---
name: pdf
description: >
  Create, read, render, and visually QA PDF documents using Poppler (pdftoppm for page renders), Python libraries (reportlab for generation, pdfplumber/pypdf for extraction and inspection). 
  Use when the user needs to generate a new PDF with reliable formatting and layout, extract text or tables from an existing PDF, render PDF pages to images for visual review, validate layout/spacing/legibility before delivery, or review PDFs where visual fidelity and page rendering matter. 
  Strong trigger for "create pdf", "generate report as pdf", "render pdf pages", "check pdf layout", "extract text from pdf", "pdf visual qa", "review this pdf".
when-to-use: "Invoked for any PDF-related production or review task that benefits from deterministic rendering + Python tooling rather than pure LLM text. Especially when layout, typography, tables, or visual inspection of pages is required. Complements image_gen for any visual assets embedded in PDFs."
allowed-tools: ["read_file", "write", "search_replace", "run_terminal_cmd", "list_dir", "grep", "image_gen", "open_page"]
argument-hint: "<task description e.g. 'generate invoice PDF from this data' or 'render /path/to/file.pdf pages 1-3 and inspect'>"
---

# PDF Skill (Grok Port)

Handle PDF creation, inspection, rendering, and visual quality assurance in a Grok-native way. Prefer visual verification by rendering pages to PNGs (via Poppler pdftoppm) and reading the images with available tools. Use Python for structured generation and extraction.

**Grok Adaptation Note:** Grok has powerful native `image_gen` and `video_gen` tools. For PDFs that incorporate generated visuals, first produce assets with those tools, then embed via the PDF generation workflow. The core PDF handling remains deterministic via shell + Python. No Codex-specific `agents/` or image assets are included; this is a focused production skill.

## When to Use

- Generate polished, print-ready or digital PDFs (reports, invoices, docs, slides as PDF, catalogs).
- Visually QA an existing or generated PDF by rendering pages and inspecting for layout defects (clipped text, overlaps, alignment, contrast, typography).
- Extract structured content (text, tables) with layout awareness where `pdfplumber` excels over naive text.
- Validate final output before user delivery.
- Combine with Grok image generation for hybrid assets (e.g., generate chart images with `image_gen`, embed in reportlab PDF).

Do **not** use for:
- Pure text Markdown/HTML that will never be PDF.
- Cases where the user wants only SVG/vector that stays editable in-repo (prefer direct code edits).
- Trivial one-page text where a simple `write` + terminal pandoc/ wkhtmltopdf would suffice without the full QA loop.

## Prerequisites & Environment

Before any PDF work, verify or install dependencies (use `run_terminal_cmd`):

**Python packages (preferred with uv if available in env):**
```bash
uv pip install reportlab pdfplumber pypdf pillow
# or
python3 -m pip install reportlab pdfplumber pypdf pillow
```

**System rendering (Poppler for pdftoppm):**
- macOS: `brew install poppler`
- Debian/Ubuntu: `sudo apt-get install -y poppler-utils`
- Verify: `pdftoppm -v`

If installation is blocked, fall back to user-local review instructions and note the limitation explicitly.

Grok's `run_terminal_cmd` (or equivalent shell tool) is the primary mechanism for invoking these.

## Core Workflow

1. **Clarify intent and inputs**
   - Is this generation (new PDF) or inspection/QA (existing PDF)?
   - Collect exact data, template needs, page size, fonts, branding constraints.
   - For visuals in the PDF: use `image_gen` (or `image_edit`) first to produce assets, save to workspace/output/, then reference absolute paths in the PDF script.

2. **For Generation (reportlab path)**
   - Write or adapt a small Python generator script (or one-shot snippet) using reportlab for precise control over layout, fonts, tables, images, headers/footers, page numbers.
   - Use `write` to create the generator script under `output/pdf/` or a temp location if one-off.
   - Run via `run_terminal_cmd`: `python3 /path/to/generator.py --output /absolute/output.pdf [args]`
   - After generation, immediately proceed to render + visual QA (step 4).

3. **For Reading/Extraction**
   - Use `pdfplumber` (preferred for layout/tables) or `pypdf`.
   - Example invocation (via terminal or inline Python -c for quick checks):
     ```bash
     python3 -c '
     import pdfplumber
     with pdfplumber.open("/absolute/path/to/doc.pdf") as pdf:
         for i, page in enumerate(pdf.pages):
             print(f"--- Page {i+1} ---")
             print(page.extract_text() or "")
             tables = page.extract_tables()
             if tables: print("Tables:", tables)
     '
     ```
   - For full structured extraction, write a dedicated extractor script.

4. **Visual Rendering + QA (Mandatory for production)**
   - Always render pages for any deliverable or review:
     ```bash
     mkdir -p /tmp/pdf-render-$(date +%s)
     pdftoppm -png -r 150 /absolute/input.pdf /tmp/pdf-render-$(date +%s)/page
     ls /tmp/pdf-render-*/page*.png
     ```
   - Use `read_file` on the rendered PNG paths (Grok can visually describe images when read this way, or attach via other means).
   - Inspect every page for:
     - No clipped text, no overlaps, consistent margins/gaps.
     - Sharp typography, good contrast, aligned columns/tables.
     - Correct page breaks, headers/footers, numbering.
     - Embedded images sharp and correctly placed (no low-res artifacts).
   - If defects found, fix source (reportlab code or data), re-generate, re-render, re-inspect. Iterate until zero visual defects.

5. **Output & Cleanup**
   - Final PDFs land in `output/pdf/<descriptive-name>.pdf` (or user-specified absolute path).
   - Keep intermediate renders in `/tmp/...` or `output/pdf/renders/` and clean after approval.
   - Report the final absolute path(s), page count, and confirmation of visual QA pass.
   - For multi-page, provide a contact-sheet style summary or per-page highlights.

## Temp / Output Conventions (Grok Workspace)

- Intermediate: `/tmp/grok-pdf-<id>/` (auto-clean recommended after success).
- Project artifacts: `output/pdf/` (create with `mkdir -p` via terminal if needed).
- Generated visuals for embedding: `output/assets/` or alongside the PDF generator.
- Never leave final deliverables only in /tmp.

## Quality Expectations & Success Criteria

- **Generation:** PDF is well-formed, opens in standard readers (Preview, Acrobat, browsers), fonts embedded or standard, images at appropriate DPI.
- **Visual QA:** Every delivered page, when rendered at 150+ DPI, passes human (or Grok image description) review with zero defects listed in the original rubric (clipped text, overlaps, broken tables, low contrast, uneven spacing, etc.).
- **Extraction:** Text/tables faithfully recovered with structure; layout notes preserved where relevant.
- **No Unicode dash pitfalls:** Use ASCII hyphen-minus in reportlab flows unless explicitly testing advanced typography.
- User receives: the PDF path + render confirmation + any extraction artifacts + clear statement "Visual QA passed on all N pages."

## Integration with Other Grok Tools

- `image_gen` / `image_edit`: Produce charts, diagrams, photos, illustrations, then embed paths into reportlab `Image` flowables.
- `video_gen`: If the PDF is a companion to video (e.g., storyboard PDF), coordinate timelines.
- `write` / `search_replace`: Author the reportlab generator code or extraction scripts.
- `run_terminal_cmd`: The workhorse for pdftoppm, python invocations, mkdir, etc.
- For very simple one-off PDFs, a minimal reportlab one-liner in terminal may suffice; escalate to full script + QA for anything multi-page or branded.

## Limitations & Fallbacks

- If Poppler/pdftoppm unavailable: Instruct user to install locally and/or use browser "Print to PDF" preview for quick checks; do not claim visual fidelity without renders.
- Complex fonts or advanced PDF features (forms, annotations, 3D): Note limitations; prefer external tools for those.
- Encrypted or protected PDFs: Report access failure plainly.

## References & Further Reading (if porting more)

Original Codex references focused on CLI + Python. In Grok context, lean on native image tools for visuals and deterministic shell/Python for the PDF container itself. Always prefer render-inspect-fix over "trust the generator."

This port preserves the visual-first discipline while adapting to Grok's tool surface (image_gen first-class, strong terminal/Python access).

## Success Criteria for Skill Use

- User gets a production-quality PDF (or verified extraction) with explicit visual QA evidence.
- No "it looks good in my mind" deliveries — every page was rendered and checked.
- Clear, actionable error messages on missing deps with exact install commands.
- Integration with Grok's creative tools (image_gen) is seamless for mixed-media PDFs.

The user should feel: "The PDF is done, every page was visually verified, and I have the exact file path plus confidence it will render correctly everywhere."
