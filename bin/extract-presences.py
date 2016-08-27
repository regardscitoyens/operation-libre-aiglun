#!/usr/bin/env python
# coding: utf-8

import sys
import re
import os


re_nl = re.compile('\n', re.I)
re_cleanup_head = re.compile(r'<!DOCTYPE.*</head>', re.I | re.S)
re_cleanup_tags = re.compile(r'<(/?(div|sup|sub|u|b|font|span|ol|i|li)|p)[^>]*>', re.I)
re_end_p = re.compile(r'</p>', re.I)
re_multspaces = re.compile(r'( |&nbsp;|\t)+', re.I)
re_startspaces = re.compile(r'^ ', re.M)


def cleanup(cr):
    cr = re_cleanup_head.sub('', cr)
    cr = re_cleanup_tags.sub('', cr)
    cr = ' '.join(cr.split('\n'))
    cr = re_end_p.sub('\n', cr)
    cr = re_multspaces.sub(' ', cr)
    cr = re_startspaces.sub('', cr)
    return cr


re_start_presences = re.compile(ur'pr[ée]sen(ts|ces)', re.I)
re_secretaire = re.compile(ur'secr[ée]taires? de s[ée]ance', re.I)


def presence_lines(date, cr):
    started = False
    out = []

    for line in cr.split('\n'):
        if len(line):
            if not started:
                if re_start_presences.search(line):
                    out.append(line)
                    started = True
            else:
                out.append(line)

                if re_secretaire.search(line):
                    return out

    if not started:
        print "Debut des presences introuvable dans CR %s" % date
    else:
        print "Fin des presences (secretaire de seance) introuvable dans CR %s" % date


extract_states = {
    'pre': re.compile(ur'([Éée]tai(en)?t )?pr[ée]sen(te?s|ces)\s*:\s*', re.I),
    'abs': re.compile(ur'([Éée]tai(en)?t )?(absente?s?|excusée?s?|absente?s? excusée?s?)( (et|ayant donn[eé]|sans) pouvoirs?)?\s*:\s*', re.I),
    'sec': re.compile(ur'secr[ée]taires? de s[ée]ance', re.I)
}

re_seance = re.compile(ur'ouv(re|erture de)( la)? s[ée]ance', re.I)
re_pouvoirs = [
    re.compile(ur'(.+) donne pour?voir [àa] (.+)', re.I),
    re.compile(ur'(.+) a donn[eé] pouvoir [àa] (.+)', re.I),
    re.compile(ur'(.+) a donn[eé] procuration [àa] (.+)', re.I),
    re.compile(ur'(.+) \(pouvoir (.+)\)', re.I),
    re.compile(ur'(.+) \(a donné (?:pourvoir|procuration) à (.*)(?: à partir .*)\)', re.I),
]

re_pouvoir_prec = [
    re.compile(ur'^donne pouvoir à (.+)', re.I),
    re.compile(ur'^pouvoir à (.+)', re.I),
]

re_cleanup_noms = re.compile(ur'^([Éée]lus|retard|pouvoirs?)\s*:\s*', re.I)
re_cleanup_sec = re.compile(ur' (est )?(déclaré|désigné)e?.*', re.I)
re_ignore = re.compile(ur'(^(mairie|public)\s*:\s*)|(^\s*/\s*)$', re.I)
re_split_noms = re.compile(r'(?:\s*,\s*|\s+et\s+)', re.I)

referentiel_noms = {}


def slugify(nom):
    return re.sub('elizabeth', 'elisabeth', re.sub(r'[^a-z]', '', nom.lower()))


def get_ref_nom(nom):
    if slugify(nom) in referentiel_noms:
        return referentiel_noms[slugify(nom)]
    else:
        referentiel_noms[slugify(nom)] = nom
        return nom


def cleanup_nom(nom):
    nom = re.sub(ur'^Mmes? ', '', nom)
    nom = re.sub(ur'^MM?\. ', '', nom)
    nom = re.sub(ur'\.$', '', nom)
    nom = re.sub(ur' jusqu[’\']à .*', '', nom)
    nom = re.sub(ur' \((qui est )?arrivée? à.*', '', nom)
    nom = re.sub(ur' \(qui quittera .*', '', nom)
    nom = re.sub(ur' \(qui donne pour?voir .*', '', nom)
    nom = re.sub(ur' \(a donné pour?voir .*', '', nom)
    nom = re.sub(ur' : absente? sans pouvoir', '', nom)

    if nom == '/':
        return ''

    return get_ref_nom(nom)


def extract_presences(date, plines):
    state = 'start'
    data = []

    print "****", date

    for line in plines:
        line = re_cleanup_noms.sub('', line)

        print '  # %s' % line

        if re_seance.search(line) or re_ignore.search(line):
            print '  !ign'
            continue

        for rstate, regexp in extract_states.iteritems():
            if regexp.search(line):
                state = rstate
                line = regexp.sub('', line)
                print '  !state %s =>' % state, line
                break

        if len(line):
            for person in re_split_noms.split(line):
                if not len(person):
                    continue

                if state == 'pre':
                    nom = cleanup_nom(person)
                    if not len(nom):
                        continue

                    print '  !present %s' % nom

                    data.append({
                        'date': date,
                        'nom': nom,
                        'present': 1,
                        'pouvoir': '',
                        'secretaire': 0
                    })

                if state == 'abs':
                    pouvoir = ''

                    for rpouvoir in re_pouvoirs:
                        mpouvoir = rpouvoir.search(person)
                        if mpouvoir:
                            person = mpouvoir.group(1)
                            pouvoir = cleanup_nom(mpouvoir.group(2))
                            continue

                    if not mpouvoir:
                        for rpouvoir in re_pouvoir_prec:
                            mpouvoir = rpouvoir.search(person)
                            if mpouvoir:
                                data[-1]['pouvoir'] = cleanup_nom(mpouvoir.group(1))
                                print '  !pouvoir prec = %s' % data[-1]['pouvoir']
                                continue

                        if mpouvoir:
                            continue

                    nom = cleanup_nom(person)
                    if not len(nom):
                        continue

                    print '  !absent %s (pouvoir %s)' % (person, pouvoir)

                    data.append({
                        'date': date,
                        'nom': nom,
                        'present': 0,
                        'pouvoir': pouvoir,
                        'secretaire': 0
                    })

                if state == 'sec':
                    person = cleanup_nom(re_cleanup_sec.sub('', person))
                    if not len(nom):
                        continue

                    print '  !sec = %s ' % person

                    find = [item for item in data if item['nom'] == person]
                    if len(find):
                        find[0]['secretaire'] = 1
                    else:
                        print "Secretaire %s introuvable dans le CR %s" % (person, date)

    if len(data) == 0:
        print "Rien dans %s (state=%s)" % (date, state)

    return data


def write_presence(outfile, data):
    csvline = '%s;%s;%s;%s;%s\n' % (
        data['date'],
        data['nom'],
        data['present'],
        data['pouvoir'],
        data['secretaire']
    )

    outfile.write(csvline.encode('utf-8'))


if __name__ == '__main__':
    crdir = 'html/comptes-rendus'
    tmpdir = 'tmp/comptes-rendus'
    output = 'data/presences-cm.csv'

    with open(output, 'w') as out:
        write_presence(out, {k: k for k in ['date', 'nom', 'present', 'pouvoir', 'secretaire']})

        files = os.listdir(crdir)
        files   .sort()
        for filename in files:
            date = re.sub('\.html', '', filename)

            with open(os.path.join(crdir, filename), 'r') as cr:
                cleaned = cleanup(cr.read().decode('utf-8'))

                with open(os.path.join(tmpdir, '%s.clean' % date), 'w') as crc:
                    crc.write(cleaned.encode('utf-8'))

                plines = presence_lines(date, cleaned)

                with open(os.path.join(tmpdir, '%s.presences' % date), 'w') as crp:
                    crp.write('\n'.join(plines).encode('utf-8'))

                for item in extract_presences(date, plines):
                    write_presence(out, item)
