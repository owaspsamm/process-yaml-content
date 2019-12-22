#!/bin/bash

BASEDIR=$(dirname $0)

makemarkdown=$BASEDIR/bin/make_markdown.py
outputsh=$BASEDIR/run_make_web_markdown_script.sh

test -z $1 && echo "usage: $0 <web directory> <output_script>" && exit 1

pfx=$1
outputsh=$2

test -e $pfx || (echo "Invalid directory $pfx" && exit)
rm -f $outputsh

#
# each file in the namespaces directory has an identically named file in the ns2template.mapping directory which contains the name of the template to use when generating that file's markdown.
# write a 1 line call of the form:
# $makemarkdown [namespace file] [template file] > [markdown output file]
#
for f in $pfx/namespaces/*.ns; do 
    _f=$(basename $f)
    echo "$makemarkdown $f $pfx/templates/$(cat $pfx/ns2template.mapping/$_f) > $pfx/markdown/$(basename $f .ns).md" >> $outputsh
done

chmod 755 $outputsh
echo wrote $outputsh
exit 0
