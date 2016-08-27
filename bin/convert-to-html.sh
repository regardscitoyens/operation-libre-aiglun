#!/bin/bash

# Liste des répertoires contentant des docx
DIRS=comptes-rendus

BASE=$(dirname $(dirname $0))
SOURCES=$BASE/sources
HTML=$BASE/html

for dir in $DIRS; do
	mkdir -p $HTML/$dir
	soffice --headless --convert-to html --outdir $HTML/$dir $SOURCES/$dir/*.doc $SOURCES/$dir/*.docx
done
