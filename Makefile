.PHONY: pdf clean package
pdf:
	cd paper && pdflatex -interaction=nonstopmode main.tex && bibtex main && pdflatex -interaction=nonstopmode main.tex && pdflatex -interaction=nonstopmode main.tex
clean:
	cd paper && rm -f *.aux *.bbl *.blg *.log *.out *.toc *.lof *.lot
package:
	zip -r mmals-symplectic-dynamics.zip README.md Makefile LICENSE CITATION.cff CHANGELOG.md paper diderot magazine scripts docs
