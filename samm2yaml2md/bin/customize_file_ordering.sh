#!/bin/bash

#
# the make_namespaces.py creates an ns.order file listing the order in which files generated from the core content will be added to the pdf.
# here we insert any additional pages such as intro and credits.
# 
test -z $1 && echo "usage: $0 <path to ns.order>" && exit 1

nsFile=$1
tmpFile=$(mktemp $(dirname $nsFile)/ns.XXXXXXXX)

echo startPage.ns > $tmpFile
echo toc.ns >> $tmpFile

sed -n '1,6p' $nsFile >> $tmpFile

echo businessFunctionSeparator-Governance.ns >> $tmpFile
sed -n '7,15p' $nsFile >> $tmpFile

echo businessFunctionSeparator-Design.ns >> $tmpFile
sed -n '16,24p' $nsFile >> $tmpFile

echo businessFunctionSeparator-Implementation.ns >> $tmpFile
sed -n '25,33p' $nsFile >> $tmpFile

echo businessFunctionSeparator-Verification.ns >> $tmpFile
sed -n '34,42p' $nsFile >> $tmpFile

echo businessFunctionSeparator-Operations.ns >> $tmpFile
sed -n '43,51p' $nsFile >> $tmpFile

echo endPage.ns >> $tmpFile

cat $tmpFile

rm -f $tmpFile
#cp -f $nsFile ${nsFile}.bak
#mv -f $tmpFile $nsFile
