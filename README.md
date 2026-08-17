# MMALS Symplectic Dynamics

**Symplectic Transport, Dissipative Learning, and Fisher--Rao Control for MMALS**

This repository contains an arXiv-style theory paper that connects the quantum--symplectic realification discussed by Igor Volovich with the current MMALS research program. It reframes symplectic computation as a geometric and control-theoretic layer rather than claiming an unconditional advantage over quantum computing.

<p align="center">
  <a href="./MMALS_Symplectic_Dynamics_v0.1.0.pdf">
    <img src="https://img.shields.io/badge/Open-Article-0B5FFF?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="Open PDF">
  </a>
</p>

## Contents

- `paper/main.tex` - complete article source
- `paper/references.bib` - bibliography
- `paper/main.pdf` - compiled paper
- `01_volovich_realification_falsification.ipynb` - executable claim/falsification audit of arXiv:2407.12755v1
- `scripts/generate_volovich_notebook.py` - deterministic notebook generator
- `scripts/validate_volovich_notebook.py` - structural, deterministic, and execution validator
- `requirements-experiments.txt` - notebook validation dependencies
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

## Reproduce the Volovich audit

The notebook is generated rather than hand-maintained. To rebuild and execute all assertions:

```bash
python -m pip install -r requirements-experiments.txt
make volovich
make validate-volovich
```

The validation checks exactly 22 cells / 10 code cells, deterministic agreement with the generator, and executes the notebook with `nbclient`. The reference run reproduces a maximum complex-vs-real trajectory discrepancy of about `5.24e-14`, with orthogonal and symplectic residuals about `2.19e-15`.

The notebook distinguishes three classes of statements:

1. identities directly supported by the mathematics (Schrödinger realification; unitary-to-orthogonal-symplectic embedding),
2. explicit counterexamples or internal consistency issues (generic squeezing vs Euclidean normalization; tensor-product dimensions; the displayed NOT gate; the sign convention in eqs. 2.20/3.4),
3. open computational claims requiring a state/measurement model, physical implementation assumptions, noise and resource accounting, and complexity bounds.

## Positioning

The paper makes three distinctions explicit:

1. Unitary dynamics is an orthogonal-symplectic subcase.
2. A larger transformation group does not itself prove greater computational power.
3. MMALS needs symplectic transport **plus** dissipation, information geometry, measurement, control, and resource accounting.

## Scientific status

This is a theoretical foundation paper. Existing MMALS values are included as an internal evidence snapshot and are not presented as newly re-run results. The proposed symplectic--dissipative model still requires dedicated experiments.

The Volovich notebook is a falsification harness and proof-obligation register. It does not claim that symplectic computing is impossible or uninteresting; it identifies which claims are established, which are contradicted by simple executable examples, and which need a stronger computational and physical model.

## License

MIT for code and repository integration material. The article text is provided for research circulation; choose a publication license before arXiv submission.
