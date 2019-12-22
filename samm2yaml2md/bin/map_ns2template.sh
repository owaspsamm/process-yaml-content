#!/bin/bash

test -z $1 && echo "usage: $0 <prefix directory>" && exit

pdfDir=$1
mapDir=$pdfDir/ns2template.mapping

mkdir -p $mapDir
#
# this script creates 1 file per namespace file (with the same name as the namespace file). It contains the name of the template file, ready for use (no new lines)
# for simplicity, the rules are baked into the script for now. 
#
for f in $pdfDir/namespaces/*-{1,2,3}.ns; do echo -n "action.template" > $mapDir/$(basename $f) ; done
for f in $pdfDir/namespaces/businessFunction-*.ns; do _f=$(basename $f); echo -n "function-details.template" > $mapDir/$_f ; done
echo -n "functions-overview.template" > $mapDir/businessFunctionsOverview.ns

# the separator pages..
for f in $pdfDir/namespaces/businessFunctionSeparator-*.ns; do _f=$(basename $f); echo -n "function-separator.template" > $mapDir/$_f ; done

