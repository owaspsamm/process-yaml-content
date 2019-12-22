#!/bin/bash

test -z $1 && echo "usage: $0 <directory to markdown files>" && exit

markdown=$1

# a final script where all sorts of cleanups happen which didn't fit in elsewhere
for f in $markdown/*.md; do
    # replace & with 'and' in values of url like keys
    sed -i -re 's/^(.*)(url:)(.+)\&(.+)$/\1\2\3and\4/' $f

    # lowercase all *url values and replace spaces with hyphens
    sed -i -re 's/^(.*)(url:)(\s*)(.+)$/'"printf '%s%s%s' '\1' '\2' '\3'; printf '\4' | tr ' ' - | tr [A-Z] [a-z]"'/e' $f


    # replace No with "No" in lists
    sed -i -re 's/^(\s+- )No$/\1"No"/' $f

    # squeeze all instances of 2 or more consecutive blank lines into 1.
    awk 'BEGIN{blanks=0}/^$/{blanks++;if(blanks==1)print; else next}/^..*$/{blanks=0;print}' $f > $f.bak
    mv $f.bak $f

    # replace False with "No" in lists
    sed -i -re 's/^(\s+- )False$/\1"No"/' $f

done

