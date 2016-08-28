#!/usr/bin/env python
# coding: utf-8


import re


referentiel_noms = {}


def slugify(nom):
    nom = re.sub(r'[^a-z]', '', nom.lower())
    nom = re.sub('elizabeth', 'elisabeth', nom)
    nom = re.sub('sylvianne', 'sylviane', nom)
    nom = re.sub('shodet', 'schodet', nom)
    return nom


def casify(nom):
    nom = nom.rstrip()
    if not len(nom):
        return nom
    nom = ' '.join(['%s%s' % (n[0].upper(), n[1:].lower()  ) for n in nom.split(' ')])
    return nom


def cleanup(nom):
    if slugify(nom) in referentiel_noms:
        return referentiel_noms[slugify(nom)]
    else:
        referentiel_noms[slugify(nom)] = casify(nom)
        return casify(nom)


if __name__ == '__main__':
    infile = 'data/presences-cm.csv'
    outfile = 'data/presences-cm-nettoye.csv'

    with open(infile, 'r') as sale:
        lines = sale.read().decode('utf-8').split('\n')

        with open(outfile, 'w') as propre:
            propre.write('%s\n' % lines[0])

            for line in lines[1:]:
                if not len(line):
                    continue

                item = line.split(';')
                item[1] = cleanup(item[1])
                if len(item[3]):
                    item[3] = cleanup(item[3])

                line = ';'.join(item)
                s = '%s\n' % line
                propre.write(s.encode('utf-8'))
