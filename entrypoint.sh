#!/bin/sh -l

echo "--- Building SAMM Web markdown"
echo "*** Datafiles dir: /github/workspace/Datafiles"
echo "*** Destination dir: /github/workspace/output"

/build/make_web.sh -d /github/workspace/Datafiles -o /github/workspace/output
