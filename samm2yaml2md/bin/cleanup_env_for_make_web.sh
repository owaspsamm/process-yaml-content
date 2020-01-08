#!/bin/bash

test -z "$1" && echo "usage: $0 <base dir to cleanup>" && exit 1

web="$1"

# these directories should be completely empty actually.
# we're just careful for now in case a precious artifact is left over.
# adjust when we have a stable working version
rm -f "$web/namespaces/*.ns"
rm -f "$web/templates/*.template"
rm -f "$web/ns2template.mapping/*.ns"
rm -f "$web/markdown/*.md"

mkdir -p "$web/{namespaces,templates,ns2template.mapping,markdown}"
