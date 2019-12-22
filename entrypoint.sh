#!/bin/sh -l

echo "--- Building SAMM Web markdown"
echo "*** Destination dir: $1"

/build/make_web.sh $1
