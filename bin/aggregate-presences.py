#!/usr/bin/env python
# coding: utf-8

if __name__ == '__main__':
    bydate = []
    byname = {}

    with open('data/presences-cm-nettoye.csv', 'r') as infile:
        lastdate = ''
        curitem_bydate = None

        for item in [line.split(';') for line in infile.read().decode('utf-8').split('\n')[1:]]:
            if len(item) < 2:
                continue

            date = item[0]
            nom = item[1]
            present = item[2]

            if nom not in byname:
                byname[nom] = {'presences': 0, 'absences': 0}

            if date != lastdate:
                if curitem_bydate:
                    bydate.append(curitem_bydate)

                curitem_bydate = {'date': date, 'presents': 0, 'absents': 0}

            if present == '1':
                curitem_bydate['presents'] = curitem_bydate['presents'] + 1
                byname[nom]['presences'] = byname[nom]['presences'] + 1
            else:
                curitem_bydate['absents'] = curitem_bydate['absents'] + 1
                byname[nom]['absences'] = byname[nom]['absences'] + 1

            lastdate = date

        if curitem_bydate:
            bydate.append(curitem_bydate)

    with open('data/presences-cm-count-by-date.csv', 'w') as outfile:
        outfile.write('date;presents;absents\n')

        for item in bydate:
            outfile.write('%s;%s;%s\n' % (item['date'], item['presents'], item['absents']))

    with open('data/presences-cm-count-by-name.csv', 'w') as outfile:
        outfile.write('nom;presences;absences\n')

        for nom, valeurs in byname.iteritems():
            ligne = '%s;%s;%s\n' % (nom, valeurs['presences'], valeurs['absences'])
            outfile.write(ligne.encode('utf-8'))
