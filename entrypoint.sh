#!/bin/sh -l

export PATH=$PATH:/build:/build/bin

echo "--- Building SAMM Web markdown"

echo "Using parameters: $*"

/build/make_web.sh "$*"
