#!/bin/bash

test -z $1 && echo "usage: $0 <prefix directory>" && exit

webDir=$1
mapDir=$webDir/ns2template.mapping

#
# this script creates 1 file per namespace file (with the same name as the namespace file). It contains the name of the template file, ready for use (no new lines)
# for simplicity, the rules are baked into the script for now. 
#
mkdir -p $mapDir
for f in $webDir/namespaces/function-*.ns; do 
    newName=$(basename ${f/function-/})
    echo -n "function.template" >  $mapDir/$newName
    mv $f $webDir/namespaces/$newName
done

for f in $webDir/namespaces/practice-*.ns; do 
    newName=$(basename ${f/practice-/})
    echo -n "practice.template" > $mapDir/$newName
    mv $f $webDir/namespaces/$newName
done

for f in $webDir/namespaces/activity-*.ns; do 
    newName=$(basename ${f/activity-/})
    echo -n "activity.template" > $mapDir/$newName
    mv $f $webDir/namespaces/$newName
done
