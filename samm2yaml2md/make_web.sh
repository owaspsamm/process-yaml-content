#!/bin/bash

# requires the following files:
#  ./templates/generic.template
#  ./Datafiles/*.yml
#  ./css/pdfbook.css
#  ./bin/make_markdown.py
#  ./bin/make_namespaces.py
#  ./bin/collate_pdf_pages.sh
#  ./bin/map_ns2template.sh
#  ./bin/cleanup_env_for_make_pdf.sh
#
# ./static.templates/*.template

test -z $1 && echo "usage: $0 <output directory>" && exit 1

src=./web
out=$1

#
# TODO:
# we should capture the steps in functions and allow calling arbitrary ones via cmdline params (something like ./make_pdf.sh --steps=[start]:[stop], e.g. --steps=:writeNamespaces to stop after writing the templates and namespaces)
#

echo tidying up any leftover files
./bin/cleanup_env_for_make_web.sh $out

test -e $src/static.templates && echo "writing ns files to namespaces" && cp $src/static.templates/*.template $out/templates/

./bin/make_namespaces.py --target web --output $out --yaml FIXME Datafiles/*.yml 

echo "mapping namespaces to templates"
./bin/map_web_ns2template.sh $out

echo creating ./run_make_markdown_script.sh
# generate the script that automates the calls to "make_markdown.py namespaces/foo.ns templates/generic.template"

./create_make_web_markdown_script.sh $out ./run_make_web_markdown_script.sh
test $? -ne 0 && echo "create_make_web_markdown_script.sh failed" && exit

echo runing ./run_make_web_markdown_script.sh
# this script is created by ./create_make_markdown_script.sh
./run_make_web_markdown_script.sh

echo "fixing up markdown files.."
./bin/fixup_web_markdown.sh $out/markdown/

