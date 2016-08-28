#!/bin/bash

echo "mot;nombre;type;annee" > data/mots_annees.csv
for annee in 2012 2013 2014 2015 2016 ; do 
	date=$(echo $annee"-01-01")
	cat "txt/comptes-rendus/"$annee"-"*txt | 
        sed 's/[:;\t\.\,«»"]/ /g' |
        sed 's/[)(]/ /g' | sed "s/[’']/ /g" | sed 's/É/é/g' | sed 's/[  ]/ /g' |
	sed 's/ /\n/g' | 
        tr '[:upper:]' '[:lower:]' | grep '....' | 
        sort | uniq -c  | 
        sed 's/^ *//' | sed 's/ /;/' | 
        awk -F ';' '{ if ( $1 > 10 ) print $0 }' | 
	sort -t ';' -k 2,2 > "/tmp/mots_"$file".csv" ; 
	join -a 1 -t ';' -1 2 -2 1 "/tmp/mots_"$file".csv" data/mots-themes.csv | grep -v IGNORE | sed "s/\$/;$date/" >> data/mots_annees.csv
done

cat /tmp/mots_*csv | sed 's/^[0-9]*;//' | sort -u > /tmp/mots.txt

cat "data/mots_annees.csv" | grep THEME | sort -t ';' -k 1,1 > /tmp/mots_annees_themes.csv

cat data/mots_tout.csv | grep THEME | sort -t ';' -k 1,1 > /tmp/mots_themes.csv
echo "mot;nombre;theme;type" > data/mots_themes.csv
join -j 1 -t ';' /tmp/mots_themes.csv data/mots-themes-themes.csv >> data/mots_themes.csv

echo "mot;nombre;theme;annee;type" > data/mots_annees_themes.csv
join -j 1 -t ';' /tmp/mots_annees_themes.csv data/mots-themes-themes.csv >> data/mots_annees_themes.csv

echo 'mot;nombre;type;' > data/mots_tout.csv
cat data/mots_annees.csv | grep -v 'mot;' | awk -F ';' 'BEGIN{old=""}{if ( $1 == old ) { value = value + $2 } else { value = value + $2 ; print $1";"value";"$3";"$5 ; value = 0 } old = $1; }' >> data/mots_tout.csv
