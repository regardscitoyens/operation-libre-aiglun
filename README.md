# Opération Libre Aiglun

Ce dépôt contient le travail réalisé lors de l'Opération Libre 2016 à Aiglun.

## Contenu principal du dépôt

* `sources` fichiers fournis par la municipalité
* `data` données produites au format CSV
* `images` graphiques produits à partir des donnée
* `restitution/index.html` page web de présentation des données produites

## Reproduction des résultats

### Conversion des comptes-rendu en HTML

Exécuter `bin/convert-to-html.sh`.

### Présence des conseillers municipaux

1. Exécuter le script `bin/extract-presences.py`, qui produit le fichier `data/presences-cm.csv`.
2. Nettoyer manuellement le fichier (quelques cas ne sont pas gérés correctement par le script).
3. Exécuter le script `bin/uniform-names.py` qui uniformise les noms
4. Exécuter le script `bin/aggregate-presences.py` pour générer les données agrégées
