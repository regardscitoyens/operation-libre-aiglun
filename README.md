# Opération Libre Aiglun

Ce dépôt contient le travail réalisé lors de l'Opération Libre 2016 à Aiglun.

## Contenu du dépôt

* `bin` scripts de conversion
* `sources` fichiers fournis par la municipalité
* `html` fichiers convertis
* `tmp` fichiers temporaires utilisés par les scripts de conversion
* `data` données produites

## Reproduction des résultats

### Conversion des comptes-rendu en HTML

Exécuter `bin/convert-to-html.sh`.

## Présence des conseillers municipaux

Exécuter `bin/extract-presences.py`, qui produit le fichier `data/presences-cm.csv`.

Attention, les données produites ne sont pas parfaitement propres, il faut les nettoyer manuellement.
