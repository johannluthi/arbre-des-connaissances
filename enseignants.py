"""Liste des enseignant·e·s FGSE 2026-2027 (xlsx) -> data/enseignants.json
Usage : python3 enseignants.py [fichier.xlsx]"""
import json, re, sys, unicodedata, openpyxl
SRC = sys.argv[1] if len(sys.argv) > 1 else 'data/enseignants_source.xlsx'
def norm(s): return unicodedata.normalize('NFD', s).encode('ascii','ignore').decode().lower()
ws = openpyxl.load_workbook(SRC).active
rows = list(ws.iter_rows(values_only=True))
note = next((r[0] for r in rows if r[0] and r[0].startswith('Les enseignant')), '')
def clean(s): return re.sub(r'\s+', ' ', (s or '').replace('_x000D_', ' ')).strip()
people = {}
for r in rows[1:]:
    if not r[3]: continue
    nom, pre = [clean(x) for x in (r[3].split(',', 1) + [''])[:2]]
    key = norm(nom + ' ' + pre)
    p = people.setdefault(key, dict(nom=nom, prenom=pre, orient=[], dispo='', comm='', domaines=[]))
    for lab, v in zip(("Géographie, environnement et sociétés", "Sciences de l'environnement", "Géologie"), r[:3]):
        if v and lab not in p['orient']: p['orient'].append(lab)
    c = clean(r[4])
    if c:
        if c.startswith('Pas disponible'): p['dispo'] = 'Pas disponible en 2026-27'
        elif c not in p['comm']: p['comm'] = (p['comm'] + ' ; ' + c).strip(' ;')
    for d in re.split(r'[;,](?![^()]*\))', clean(r[5])):
        d = d.strip(' .')
        if d and norm(d) not in {norm(x) for x in p['domaines']}: p['domaines'].append(d[0].upper() + d[1:])
out = sorted(people.values(), key=lambda p: norm(p['nom'] + p['prenom']))
json.dump(dict(note=note, ens=out), open('data/enseignants.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(out), 'enseignant·e·s')
