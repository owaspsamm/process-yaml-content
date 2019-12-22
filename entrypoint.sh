#!/bin/sh -l

echo "--- Building SAMM Web markdown"
echo "*** Datafiles dir: /github/workspace/Datafiles"
echo "*** Destination dir: /github/workspace/output"

ls -l /github/*

touch /github/home/TEST1 /github/workflow/TEST1 /github/workspace/TEST1
touch /github/home/TEST1 
touch /github/workflow/TEST1
touch /github/workspace/TEST1

/build/make_web.sh -d /github/workspace/Datafiles -o /github/workspace/output
