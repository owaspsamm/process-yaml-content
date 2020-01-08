#!/bin/bash

test -z "$2" && echo "Usage: $0 [web|pdf] <output directory>" && exit 1

#
# dump all static directories to the output directory.
# this is useful when're running in a container and need to use the default
# static files that are bundled with the release rather than specify our own
# 

src="$1"
output="$2"

test -e "$src" || (echo "No such type of output $1. Try web or pdf" && exit 1)

cp -r "$src/static.*" "$output"/

