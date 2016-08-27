# Opération Libre Aiglun

Ce dépôt contient le travail réalisé lors de l'Opération Libre 2016 à Aiglun.

## Contenu du dépôt

* `bin` scripts de conversion
* `sources` fichiers fournis par la municipalité
* `html` fichiers convertis
* `tmp` fichiers temporaires utilisés par les scripts de conversion
* `data` données produites
* `images` visualisation
* `restitution` page web de présentation

## Reproduction des résultats

### Conversion des comptes-rendu en HTML

Exécuter `bin/convert-to-html.sh`.

### Présence des conseillers municipaux

1. Exécuter le script `bin/extract-presences.py`, qui produit le fichier `data/presences-cm.csv`.
2. Nettoyer manuellement le fichier (quelques cas ne sont pas gérés correctement par le script).
3. Exécuter le script `bin/uniform-names.py` qui uniformise les noms
4. Exécuter le script `bin/aggregate-presences.py` pour générer les données agrégées
