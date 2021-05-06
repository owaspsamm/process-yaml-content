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

# USAGE STATEMENT
function usage() {
cat << EOF
usage: $0 -d Datafiles_dir -o output_dir

EOF
}


while getopts "d:o:" OPTION; do
  case $OPTION in
    d)
      DATAFILES=$OPTARG
      ;;
    o)
      OUTPUT=$OPTARG
      ;;
    ?)
      echo "ERROR: Invalid Option $OPTION Provided!"
      echo
      usage
      exit 1
      ;;
  esac
done

BASEDIR=$(dirname $0)

src=$BASEDIR/web

#
# TODO:
# we should capture the steps in functions and allow calling arbitrary ones via cmdline params (something like ./make_pdf.sh --steps=[start]:[stop], e.g. --steps=:writeNamespaces to stop after writing the templates and namespaces)
#

echo tidying up any leftover files
$BASEDIR/bin/cleanup_env_for_make_web.sh $OUTPUT

test -e $src/static.templates && echo "writing ns files to namespaces" && cp $src/static.templates/*.template $OUTPUT/templates/

$BASEDIR/bin/make_namespaces.py --target web --output $OUTPUT --model $DATAFILES

echo "mapping namespaces to templates"
$BASEDIR/bin/map_web_ns2template.sh $OUTPUT

echo creating ./run_make_markdown_script.sh
# generate the script that automates the calls to "make_markdown.py namespaces/foo.ns templates/generic.template"

$BASEDIR/create_make_web_markdown_script.sh $OUTPUT $BASEDIR/run_make_web_markdown_script.sh
test $? -ne 0 && echo "create_make_web_markdown_script.sh failed" && exit

echo runing ./run_make_web_markdown_script.sh
# this script is created by ./create_make_markdown_script.sh
$BASEDIR/run_make_web_markdown_script.sh

echo "fixing up markdown files.."
$BASEDIR/bin/fixup_web_markdown.sh $OUTPUT/markdown/

echo "done"
