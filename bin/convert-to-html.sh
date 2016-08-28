#!/bin/bash

# Liste des répertoires contentant des docx
DIRS=comptes-rendus

BASE=$(dirname $(dirname $0))
SOURCES=$BASE/sources
HTML=$BASE/html
TXT=$BASE/txt

for dir in $DIRS; do
	mkdir -p $HTML/$dir $TXT/$dir
	rm $HTML/$dir/*.html
	soffice --headless --convert-to html --outdir $HTML/$dir $SOURCES/$dir/*.doc $SOURCES/$dir/*.docx
        soffice --headless --convert-to txt --outdir $TXT/$dir $SOURCES/$dir/*.doc $SOURCES/$dir/*.docx
done
