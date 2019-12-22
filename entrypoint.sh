#!/bin/sh -l

echo "--- Building SAMM Web markdown"
echo "*** Destination dir: $1"

./make_web.sh $1
