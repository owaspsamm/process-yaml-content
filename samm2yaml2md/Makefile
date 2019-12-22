include make.env

MD2HTML=pandoc
TEMPLATE2MD=./bin/make_markdown.py
TEMPLATE2MDFLAGS=2>/dev/null

#HTML2PDF=wkhtmltopdf
#HTML2PDF=/home/user/lab/wkhtmltopdf/usr/local/bin/wkhtmltopdf
#CSS=./css/pdfbook.css

MAKE_NS=./bin/make_template.py
MD2HTMLFLAGS=-s --to=html -V css=$(CSS)
HTML2PDFFLAGS=-B 25mm -T 25mm -L 25mm -R 25mm -q -s Letter
RELEASE=samm2yaml2pdf
CLEANUP=run_make_markdown_script.sh  run_make_web_markdown_script.sh $(RELEASE) $(RELEASE).tgz
PACKAGE=./bin/package.sh
MAKE_PDF=./make_pdf.sh
DOCKER_CMD=docker build --build-arg userid=1000 --build-arg groupid=1000 -t nessimk/samm2yaml2pdf:latest ../docker

.DEFAULT_GOAL:=book

book:
	$(MAKE_PDF)
	@echo "\nIf things went according to plan, you should have a shiny new samm2.pdf file waiting in the pdf/ directory. If not...meh."

%.md: %.template
	$(TEMPLATE2MD) $(basename $@).ns $(basename $@).template $(TEMPLATE2MDFLAGS) > $@

%.pdf: %.html
	$(HTML2PDF) $(HTML2PDFFLAGS) $< $@

%.html: %.md
	$(MD2HTML) -o $(basename $@).html $< $(MD2HTMLFLAGS) --metadata pagetitle=$(basename $@)

.PRECIOUS: %.md %.html
.PHONY: clean realclean

default:
	@echo "try make <filename.{md,html,pdf}>. You probably want to run make_pdf.sh instead though"

clean:
	rm -f namespaces/*.ns markdown/*.md html/*.html pdf/*.pdf  ns.order

veryclean: clean
	rm -rf $(CLEANUP)

release:
	$(PACKAGE)
	cp $(RELEASE).tgz ../docker

image: 
	$(DOCKER_CMD)

    
