## Enhanced Research Paper Requirements

**Mandatory Three-Format Output with Embedded Assets:**
1. **Markdown (RESEARCH_PAPER.md)** — Source with relative paths to `results/experiment_XX/` and `docs/findings/`
2. **HTML (RESEARCH_PAPER.html)** — Standalone via pandoc with Bootstrap CSS, all images embedded
3. **PDF (RESEARCH_PAPER.pdf)** — Via reportlab/weasyprint, all images embedded

**Commands:**
```bash
cd /home/hyperion/Projects/Base60Research/base12-base60-laboratory

# HTML with embedded images
pandoc RESEARCH_PAPER.md -o RESEARCH_PAPER.html --standalone --toc \
  --css=https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css \
  --metadata title="Base-12 / Base-60 Mathematical Research"

# PDF with embedded images (via Python/reportlab)
python3 -c "
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
import markdown
import os

with open('RESEARCH_PAPER.md', 'r') as f:
    md_content = f.read()
html = markdown.markdown(md_content, extensions=['tables', 'fenced_code', 'toc'])
# Full reportlab conversion handling img tags with local paths
"
```

**Research Paper Structure Requirements (Mandatory):**
- **Findings Assessment Section (Section 7)** — Each finding evaluated as Good/Bad/Neutral with:
  - Plain-language explanation
  - Why it matters (practical impact)
  - Applications (domain mapping: Quantum, Signal, Crypto, Financial, Scientific, Education, Historical, Cognitive, Computer Arithmetic, Music)
  - How to implement (concrete steps)
  - What graphs show (visualization descriptions in plain language)
  - Breakthrough ideas (theoretical applications not currently used that could lead to breakthroughs)
- **Application Domain Coverage** — At least 5 of 10 standard domains covered
- **Breakthrough Traceability** — Each breakthrough idea traces to a verified Good finding
- **Implementation Readiness** — Concrete steps with timeline (immediate/near-term/breakthrough)
- **Plain-Language Accessibility** — Non-mathematician can understand significance

**Visual QA Protocol:**
1. Verify all three formats exist with matching content
2. Check embedded images — HTML should have 100+ `<img>` tags with `results/experiment_XX/` and `docs/findings/` paths
3. Validate PDF — Should contain figure placeholders for all visualizations
4. Visual comparison — HTML and PDF should render identically for figures

**ulw-research Skill Requirements (when running for Base-60 topics):**
Phase 0 axes MUST include:
1. Exact Rational Arithmetic Implementation — Eliminate floats from compute path
2. Hybrid Architecture Design — Base-12 for humans, Base-60 for machines, exact conversion
3. 5-Smooth Algorithm Optimization — FFT, NTT, CORDIC, lattice reduction using 2^a·3^b·5^c
4. Hardware/Software Co-Design — RNS, carry-free arithmetic, memory access for base-60
5. Application-Specific Killer Apps — PQC, financial exactness, quantum simulation, neuromorphic
6. Adoption Barrier Analysis — Cognitive load, ecosystem lock-in, standardization path
7. Verification & Testing Strategy — Property-based testing, formal verification, cross-base round-trip

Enhanced delivery gates (in addition to standard):
- Findings Assessment Gate, Application Coverage Gate, Breakthrough Traceability Gate
- Implementation Readiness Gate, Plain-Language Gate

**Downloads Directory:** `/home/hyperion/Projects/Base60Research/downloads/` — for paper PDFs