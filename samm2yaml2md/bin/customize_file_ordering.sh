#!/bin/bash

#
# the make_namespaces.py creates an ns.order file listing the order in which files generated from the core content will be added to the pdf.
# here we insert any additional pages such as intro and credits.
# 
test -z "$1" && echo "usage: $0 <path to ns.order>" && exit 1

nsFile="$1"
tmpFile=$(mktemp "$(dirname "$nsFile")"/ns.XXXXXXXX)

{
  echo startPage.ns;
  echo toc.ns;

  sed -n '1,6p' "$nsFile";

  echo businessFunctionSeparator-Governance.ns;
  sed -n '7,15p' "$nsFile";

  echo businessFunctionSeparator-Design.ns;
  sed -n '16,24p' "$nsFile";

  echo businessFunctionSeparator-Implementation.ns;
  sed -n '25,33p' "$nsFile";

  echo businessFunctionSeparator-Verification.ns; 
  sed -n '34,42p' "$nsFile";

  echo businessFunctionSeparator-Operations.ns; 
  sed -n '43,51p' "$nsFile";

  echo endPage.ns; } >> "$tmpFile"

cat "$tmpFile"

rm -f "$tmpFile"
#cp -f $nsFile ${nsFile}.bak
#mv -f $tmpFile $nsFile
