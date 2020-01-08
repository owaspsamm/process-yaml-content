#!/bin/sh -l

export PATH=$PATH:/build:/build/bin

echo "--- Building SAMM Web markdown"

/build/make_web.sh "$*"
