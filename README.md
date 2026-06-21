# MMALS Symplectic Dynamics

**Symplectic Transport, Dissipative Learning, and Fisher--Rao Control for MMALS**

This repository contains an arXiv-style theory paper that connects the quantum--symplectic realification discussed by Igor Volovich with the current MMALS research program. It reframes symplectic computation as a geometric and control-theoretic layer rather than claiming an unconditional advantage over quantum computing.

## Contents

- `paper/main.tex` - complete article source
- `paper/references.bib` - bibliography
- `paper/main.pdf` - compiled paper
- `diderot/entry.json` - importable Diderot concept entry
- `diderot/entry.md` - human-readable Diderot article
- `scripts/update_diderot.py` - safe insert/update script
- `magazine/chapter.md` - magazine chapter
- `magazine/chapter.tex` - LaTeX chapter fragment
- `docs/GITHUB_INFO.md` - repository description, topics, commit and release text
- `docs/REVIEW_CHECKLIST.md` - scientific and publication checks

## Build

```bash
cd paper
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Or:

```bash
make pdf
```

## Positioning

The paper makes three distinctions explicit:

1. Unitary dynamics is an orthogonal-symplectic subcase.
2. A larger transformation group does not itself prove greater computational power.
3. MMALS needs symplectic transport **plus** dissipation, information geometry, measurement, control, and resource accounting.

## Scientific status

This is a theoretical foundation paper. Existing MMALS values are included as an internal evidence snapshot and are not presented as newly re-run results. The proposed symplectic--dissipative model still requires dedicated experiments.

## License

MIT for code and repository integration material. The article text is provided for research circulation; choose a publication license before arXiv submission.
