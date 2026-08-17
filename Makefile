.PHONY: pdf clean package volovich validate-volovich
pdf:
	cd paper && pdflatex -interaction=nonstopmode main.tex && bibtex main && pdflatex -interaction=nonstopmode main.tex && pdflatex -interaction=nonstopmode main.tex
volovich:
	python scripts/generate_volovich_notebook.py --output 01_volovich_realification_falsification.ipynb
validate-volovich: volovich
	python scripts/validate_volovich_notebook.py 01_volovich_realification_falsification.ipynb
clean:
	cd paper && rm -f *.aux *.bbl *.blg *.log *.out *.toc *.lof *.lot
package:
	zip -r mmals-symplectic-dynamics.zip README.md Makefile LICENSE CITATION.cff CHANGELOG.md requirements-experiments.txt 01_volovich_realification_falsification.ipynb paper diderot magazine scripts docs
