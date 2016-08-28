#!/usr/bin/env python
# coding: utf-8

breaks = {
    '2012-03-02': '2012',
    '2014-03-28': '2014'
}

feminins = [
    'fabienne',
    'myriam',
    'danielle',
    'karine',
    'sylviane',
    'elisabeth',
    'catherine',
    'marion'
]


if __name__ == '__main__':
    for k, v in breaks.iteritems():
        breaks[k] = {'nom': v, 'byname': {}, 'bydate': [], 'pouvoirs': {}}

    with open('data/presences-cm-nettoye.csv', 'r') as infile:
        lastdate = ''
        curbreak = None
        curitem_bydate = None

        for item in [line.split(';') for line in infile.read().decode('utf-8').split('\n')[1:]]:
            if len(item) < 2:
                continue

            date = item[0]
            nom = item[1]
            present = item[2]
            pouvoir = item[3]

            if date in breaks:
                curbreak = date

            if nom not in breaks[curbreak]['byname']:
                breaks[curbreak]['byname'][nom] = {'presences': 0, 'absences': 0}

            if len(pouvoir):
                if pouvoir not in breaks[curbreak]['pouvoirs']:
                    breaks[curbreak]['pouvoirs'][pouvoir] = {}

                if nom not in breaks[curbreak]['pouvoirs'][pouvoir]:
                    breaks[curbreak]['pouvoirs'][pouvoir][nom] = 1
                else:
                    breaks[curbreak]['pouvoirs'][pouvoir][nom] = breaks[curbreak]['pouvoirs'][pouvoir][nom] + 1

            if date != lastdate:
                if curitem_bydate:
                    breaks[curbreak]['bydate'].append(curitem_bydate)

                curitem_bydate = {'date': date, 'presents': 0, 'absents': 0}

            if present == '1':
                curitem_bydate['presents'] = curitem_bydate['presents'] + 1
                breaks[curbreak]['byname'][nom]['presences'] = breaks[curbreak]['byname'][nom]['presences'] + 1
            else:
                curitem_bydate['absents'] = curitem_bydate['absents'] + 1
                breaks[curbreak]['byname'][nom]['absences'] = breaks[curbreak]['byname'][nom]['absences'] + 1

            lastdate = date

        if curitem_bydate:
            breaks[curbreak]['bydate'].append(curitem_bydate)

    for k, v in breaks.iteritems():

        with open('data/presences-cm-%s-count-by-date.csv' % v['nom'], 'w') as outfile:
            outfile.write('date;presents;absents\n')

            for item in v['bydate']:
                outfile.write('%s;%s;%s\n' % (item['date'], item['presents'], item['absents']))

        with open('data/presences-cm-%s-count-by-name.csv' % v['nom'], 'w') as outfile:
            outfile.write('nom;sexe;presences;absences\n')

            for nom, valeurs in v['byname'].iteritems():
                sexe = 'F' if nom.split(' ')[0].lower() in feminins else 'M'
                ligne = '%s;%s;%s;%s\n' % (nom, sexe, valeurs['presences'], valeurs['absences'])
                outfile.write(ligne.encode('utf-8'))

        with open('data/pouvoirs-cm-%s.csv' % v['nom'], 'w') as outfile:
            outfile.write('receveur;donneur;nombre\n')

            for receveur, valeurs in v['pouvoirs'].iteritems():
                for donneur, nombre in valeurs.iteritems():
                    ligne = '%s;%s;%s\n' % (receveur, donneur, nombre)
                    outfile.write(ligne.encode('utf-8'))
