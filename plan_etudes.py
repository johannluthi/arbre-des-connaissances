# -*- coding: utf-8 -*-
"""Extrait le plan d'études 2026-2027 (PDF officiel de la FGSE) vers data/plan.json.

Structure : une ligne par enseignement ET par module où il figure. Le texte du PDF
donne les modules, les heures, l'évaluation et les ECTS ; la colonne Automne/Printemps
n'existe pas en texte, elle est lue sur la position des heures dans la page.
Usage :  python3 plan_etudes.py ba-pe-2627.pdf
"""
import csv, json, re, sys, unicodedata
import fitz

GES, SE, GEO = "Géographie, environnement et sociétés", "Sciences de l'environnement", "Géologie"
TOUS = [GES, SE, GEO]
CCI, ECR, ORA, PRA = "CCi", "Écrite", "Orale", "Pratique"

# (parcours, année, module, bloc, page, [ (titre PDF, enseignants, ECTS, évaluation, heures, type) ])
# type : O obligatoire · C à choisir dans la liste · pas de cours = ligne spéciale
M = []
def mod(parc, an, titre, page, rows, ects_exiges, note=""):
    M.append(dict(parc=parc, an=an, module=titre, page=page, rows=rows, exiges=ects_exiges, note=note))

# ---------- 1re année : partie propédeutique ----------
mod(TOUS, "1re", "Module 1 – Initiation aux orientations", 3, [
 ("Géographie, environnement et sociétés : approches et théories contemporaines", "M. Stock (coord.), C. Arnsperger, J. Steinberger", 6, [CCI, ECR+" (2h)"], "26C 26TP", "O"),
 ("Introduction aux sciences de l’environnement", "G. Mariéthoz (coord.), N. Chèvre, S. Lane, M. Keiluweit, M.-E. Perga, J. Steinberger", 6, [PRA, ECR+" (2h)"], "26C 26TP", "O"),
 ("Géologie : introduction aux Sciences de la Terre", "S. Pilet (coord.), G. Hetényi, S. Jaccard", 6, [PRA, ECR+" (2h)"], "39C 39TP", "O"),
], 18)
B2 = "Module 2 – Préparation à une orientation"
mod([GES], "1re", B2+" (bloc Géographie, environnement et sociétés)", 3, [
 ("Population et dé/croissance", "C. Mager", 6, [ECR+" (3h)"], "26C 13TP", "O"),
 ("La pensée géographique", "P. Rérat (coord.), M. Müller", 6, [PRA, ECR+" (2h)"], "26C 26TP", "O"),
 ("Excursions et cas d’études", "C. Arnsperger", 3, [CCI], "12C 14T", "O"),
], 18)
mod([SE], "1re", B2+" (bloc Sciences de l’environnement)", 3, [
 ("Systèmes énergétiques", "S. Yilmaz", 3, [ECR+" (2h)"], "13C 13S", "O"),
 ("Chimie générale", "S. Terrettaz / EPFL", 3, [ECR+" (2h)"], "26C 13TP", "O"),
 ("Physique générale I", "R. Trappitsch / EPFL", 3, [ECR+" (2h)"], "22C 22E", "O"),
 ("Excursions et cas d’études", "N. Chèvre (coord.), M.-E. Perga, S. Lane, P. Vittoz", 3, [PRA], "8T 16T", "O"),
 ("Introduction à la géologie alpine", "G. Jouvet (resp.), J.-D. Champagnac", 3, [PRA, ECR+" (1h)"], "8C 8TP 16T", "O"),
], 18)
mod([GEO], "1re", B2+" (bloc Géologie)", 4, [
 ("Chimie générale", "S. Terrettaz / EPFL", 3, [ECR+" (2h)"], "26C 13TP", "O"),
 ("Physique générale I", "R. Trappitsch / EPFL", 3, [ECR+" (2h)"], "22C 22E", "O"),
 ("Géologie régionale", "P. Lanari (coord.), S. Schmalholz", 3, [PRA, ORA], "16C 16T", "O"),
 ("Camp de terrain en géologie", "S. Schmalholz (coord.), A. Daley, A. Samsu", 3, [PRA], "75T", "O"),
 ("Histoire de la Vie et stratigraphie", "A. Daley (coord.), J. Marin Carbonne, P. Gueriau", 3, [ECR+" (2h)", CCI], "26C 7TP", "O"),
], 18)
mod(TOUS, "1re", B2+" (commun aux trois blocs)", 3, [
 ("Regards croisés sur le changement climatique", "S. Jaccard (coord.), D. Domeisen, J. Steinberger", 3, [ECR+" (2h)"], "26C", "O"),
], 0, "Fait partie du bloc de 18 ECTS de chacune des trois orientations.")
mod(TOUS, "1re", "Module 3 – Méthodes de base", 4, [
 ("Méthodes quantitatives I : introduction aux principes et statistiques descriptives", "G. Guex", 3, [CCI], "26C 13TP", "O"),
 ("Méthodes quantitatives II : statistiques inférentielles", "G. Guex", 3, [CCI], "26C 13TP", "O"),
 ("Géoinformatique I", "C. Kaiser", 6, [ORA], "52CTP", "O"),
], 15, "Communs aux trois orientations ; 15 ECTS en tout avec la ligne propre à l’orientation.")
mod([GES], "1re", "Module 3 – Méthodes de base (propre à Géographie, environnement et sociétés)", 4, [
 ("Introduction aux méthodes qualitatives", "R. Kunz (resp.), A. Fal-Dutra Santos, C. Danalet / SSP", 3, [CCI], "26C", "O"),
], 15)
mod([SE, GEO], "1re", "Module 3 – Méthodes de base (propre à Sciences de l’environnement et Géologie)", 4, [
 ("Mathématiques pour les géosciences", "K. Zuleta / EPFL", 3, [ECR+" (2h)"], "26C 26E", "O"),
], 15)
mod(TOUS, "1re", "Module 4 – Sciences de base (commun)", 4, [
 ("Éléments d’écologie", "A. Guisan", 3, [ECR+" (2h)"], "26C", "O"),
], 9)
mod([GES, SE], "1re", "Module 4 – Sciences de base (Géographie et Sciences de l’environnement)", 4, [
 ("Éléments de sciences économiques", "V. Boisvert (resp.), NN", 3, [ECR+" (2h)"], "26C", "O"),
 ("Éléments de sciences sociales", "J. Pollard / SSP", 3, [ECR+" (2h)"], "26C", "O"),
], 9)
mod([GEO], "1re", "Module 4 – Sciences de base (Géologie)", 4, [
 ("Minéralogie générale", "S. Pilet", 3, [ECR+" (2h)"], "26C 13TP", "O"),
 ("Minéralogie optique", "O. Müntener", 3, [CCI], "13C 26TP", "O"),
], 9)

# ---------- 2e et 3e années : orientation Géographie, environnement et sociétés ----------
G = [GES]
mod(G, "2e", "Module 1 – Géographie humaine", 5, [
 ("Géographie sociale et culturelle", "R. Véron (coord.), L. Chanteloup", 6, [CCI, ECR+" (2h)"], "39C 13TP", "O"),
 ("Géographie urbaine", "C. Rozenblat (resp.), M. Rogov", 6, [CCI, ECR+" (2h)"], "26C 8T", "O"),
 ("Géographie économique", "C. Mager", 3, [ORA], "26C", "O"),
 ("Aménagement du territoire", "G. Debrunner", 6, [PRA, ECR+" (2h)"], "26C 13TP", "O"),
], 21)
mod(G, "2e", "Module 2 – Durabilité et transition écologique", 5, [
 ("Introduction à la pensée écologique", "S. A. Schroer", 3, ["À définir"], "26C", "O"),
 ("Gestion sociale des flux de matière", "J. Steinberger (coord.), C. Arnsperger", 6, [CCI, ECR+" (2h)"], "26C 26ST", "O"),
 ("Politiques environnementales", "J. Pollard / SSP", 6, [CCI], "52CS", "O"),
], 15)
mod(G, "2e", "Module 3 – Environnement naturel", 5, [
 ("Gestion de l’eau", "E. Reynard", 3, [ORA], "26C", "O"),
 ("Géomorphologie I", "E. Reynard", 3, [ECR+" (2h)"], "26C", "O"),
 ("Télédétection", "G. Mariéthoz", 3, [CCI], "26C 26TP", "O"),
], 9)
mod(G, "2e", "Module 4 – Outils et méthodes", 5, [
 ("Production de savoirs en géographie et environnement", "C. Kull (resp.), S. Lane", 3, [CCI], "26CTP", "O"),
 ("Méthodes quantitatives III : statistiques multivariées", "G. Guex", 3, [CCI], "26C 13TP", "O"),
 ("Méthodes d’enquête et d’analyse", "C. Rozenblat (resp.), M. Rogov", 3, [PRA], "13C 13TP", "O"),
 ("Méthodes qualitatives avancées : méthodes et terrains", "L. Chanteloup (coord.), G. Walters", 6, [CCI], "26C 26TP", "O"),
], 15)
mod(G, "3e", "Module 5 – Spécialisation en géographie humaine", 6, [
 ("Géoinformatique II", "T. Beucler", 3, [CCI], "26CTP", "O"),
 ("Political Ecology", "C. Kull", 3, [PRA, ECR+" (1h)"], "14C 9S", "C"),
 ("Tourisme : environnement, société, économie", "Mo. Müller (coord.), C. Clivaz, L. Kébir, M. Stock", 3, [ECR+" (2h)"], "26CS", "C"),
 ("Géographie des mobilités", "P. Rérat", 3, [PRA, ECR+" (2h)"], "22C 4TP", "C"),
 ("Géographie du développement", "R. Véron", 3, [ECR+" (2h)"], "26C", "C"),
 ("Systèmes complexes et organisation de l’espace géographique", "C. Rozenblat (resp.), M. Rogov", 3, [CCI], "26C", "C"),
 ("Dynamiques urbaines", "J. Salomon Cavin (coord.), C. Trivin, M. Müller", 6, [CCI], "14C 34T", "C"),
], 18, "Géoinformatique II est obligatoire ; 15 ECTS à choisir parmi les autres enseignements (24 ECTS offerts). Dynamiques urbaines : cours de terrain début juillet.")
mod(G, "3e", "Module 6 – Spécialisation en transition écologique", 6, [
 ("Systèmes énergétiques", "S. Yilmaz", 3, [ECR+" (2h)"], "13C 13S", "C"),
 ("Évaluation critique des méthodes en économie environnementale", "C. Mager", 3, [PRA], "10C 16TP", "C"),
 ("Droit de l’environnement", "C. Blattner", 6, [CCI], "39CS", "C"),
 ("Durabilité et modes de vie", "C. Arnsperger", 3, [CCI], "26C", "C"),
 ("Éléments d’économie écologique", "V. Boisvert", 3, [ECR+" (2h)"], "26C", "C"),
], 15, "15 ECTS à choisir parmi les enseignements offerts (18 ECTS offerts). Éléments d’économie écologique n’est pas donné au printemps 2027.")
mod(G, "3e", "Module 7 – Travail de Bachelor", 6, [
 ("Préparation au travail de Bachelor", "J. Salomon Cavin (coord.)", 2, [PRA], "17CE", "O"),
 ("Travail de Bachelor", "", 10, [], "", "O"),
], 12, "Une seule note pour 12 ECTS, donnée par la personne qui supervise le travail.")
mod(G, "2e/3e", "Module 8 – Module à choix libre", 7, [
 ("Enseignements à choix libre", "", 15, [], "", "L"),
], 15, "Enseignements à choisir dans les autres orientations, d’autres facultés ou universités.")

# ---------- Sciences de l'environnement ----------
S = [SE]
mod(S, "2e", "Module 1 – Éléments de chimie et biologie", 7, [
 ("Géochimie environnementale", "J. Marin-Carbonne", 3, [PRA], "26C", "O"),
 ("Chimie organique environnementale", "M. Keiluweit", 3, [ECR+" (2h)"], "26C", "O"),
 ("Biologie", "P. Vittoz (resp.), M. Blanc", 3, [ECR+" (2h)"], "26C", "O"),
 ("Écologie végétale", "P. Vittoz", 3, [ECR+" (2h)"], "26C", "O"),
], 12)
mod(S, "2e", "Module 2 – Outils quantitatifs", 7, [
 ("Méthodes quantitatives III : statistiques multivariées", "G. Guex", 3, [CCI], "26C 13TP", "O"),
 ("Levés géomatiques", "B. Quintal", 3, [PRA], "20C 20TP", "O"),
 ("Télédétection", "G. Mariéthoz", 3, [CCI], "26C 26TP", "O"),
 ("Analyse vectorielle", "P. De Anna", 3, [PRA, ORA], "18C 18E", "O"),
 ("Modélisation numérique", "G. Jouvet", 3, [CCI], "13C 26E", "O"),
], 15)
mod(S, "2e", "Module 3 – Éléments de géosciences", 8, [
 ("Physique générale II", "F. Carbone / EPFL", 3, [ECR+" (2h)"], "26C 28E", "O"),
 ("Physique du globe", "J. Irving (resp.), NN", 3, [PRA, ECR+" (3h)"], "24C 20E", "O"),
 ("Géomorphologie I", "E. Reynard", 3, [ECR+" (2h)"], "26C", "O"),
 ("Géomorphologie II", "C. Lambiel", 3, [ORA], "26CTP", "O"),
 ("Risques environnementaux", "M. Jaboyedoff", 3, [ECR+" (2h)"], "27C 9E", "O"),
], 15)
mod(S, "2e", "Module 4 – Processus environnementaux", 8, [
 ("Production de savoirs en géographie et environnement", "C. Kull (resp.), S. Lane", 3, [CCI], "26CTP", "O"),
 ("Principes de la science atmosphérique", "D. Domeisen", 6, [ECR+" (2h)", PRA], "39CTP", "O"),
 ("Hydrologie", "P. Benettin", 6, [ECR+" (2h)"], "26C 26TP", "O"),
], 15)
mod(S, "3e", "Module 5 – Approches et gestion de l’environnement", 8, [
 ("Hydrologie", "P. Benettin", 6, [ECR+" (2h)"], "26C 26TP", "O"),
 ("Droit de l’environnement", "C. Blattner", 6, [CCI], "39CS", "O"),
 ("Hydrauliques, formes et processus fluviaux", "S. Lane (coord.), G. Antoniazza", 3, [PRA, ORA], "14C 10TP 8T", "O"),
 ("Gestion de l’eau", "E. Reynard", 3, [ORA], "26C", "O"),
 ("Pédologie", "S. Grand", 3, [PRA, ECR+" (2h)"], "26C", "O"),
 ("Camp de terrain en environnement", "S. Lane (resp.), G. Antoniazza", 3, [PRA], "40T", "O"),
], 18, "Hydrologie : uniquement au printemps 2027. Droit de l’environnement : dès le printemps 2028. Module 4 pour les étudiant·e·s entré·e·s en seconde partie en septembre 2025.")
mod(S, "3e", "Module 6 – Sciences et outils quantitatifs en environnement", 8, [
 ("Géoinformatique II", "T. Beucler", 3, [CCI], "26CTP", "O"),
 ("Géophysique de l’environnement", "N. Linde", 6, [ECR+" (3h)"], "39C 39TP", "O"),
 ("Géophysique de l’environnement : camp", "J. Irving (coord.), N. Linde", 3, [PRA], "42T", "O"),
 ("Analyses des données environnementales", "M. Perga", 3, [CCI], "13C 13TP", "O"),
], 15, "Module 5 pour les étudiant·e·s entré·e·s en seconde partie en septembre 2025.")
mod(S, "3e", "Module 7a – Processus de la surface terrestre (module thématique, 1 à choix)", 8, [
 ("Excursions et cartographie géomorphologique", "C. Lambiel", 3, [PRA], "40T", "C"),
 ("Études des mouvements gravitaires", "M.-H. Derron (coord.), M. Jaboyedoff", 3, [PRA, ECR+" (2h)"], "13C 32T", "C"),
 ("Changement environnemental du quaternaire", "G. King", 3, [CCI], "11C 11TP", "C"),
 ("Cartographie géologique", "S. Schmalholz (coord.), A. Daley", 3, [PRA], "40T", "C"),
], 12, "Un module thématique à choisir : 7a ou 7b.")
mod(S, "3e", "Module 7b – Sciences aquatiques (module thématique, 1 à choix)", 9, [
 ("Écotoxicologie", "N. Chèvre", 3, [CCI, ECR+" (2h)"], "26C 13TP", "C"),
 ("Hydrochimie et pollution des eaux", "J. Berg", 3, [ECR+" (1h30)"], "21C 9TP", "C"),
 ("Limnologie", "M.-E. Perga", 3, [ECR+" (2h)"], "26C", "C"),
 ("Introduction à la géochimie isotopique", "T. Vennemann (resp.), B. Bomou", 3, [ECR+" (2h)"], "26C 26E", "C"),
], 12, "Un module thématique à choisir : 7a ou 7b.")
mod(S, "3e", "Module 8 – Travail de Bachelor", 9, [
 ("Préparation au travail de Bachelor", "J. Salomon Cavin (coord.)", 2, [PRA], "17CE", "O"),
 ("Travail de Bachelor", "", 10, [], "", "O"),
], 12, "Une seule note pour 12 ECTS.")
mod(S, "2e/3e", "Module 9 – Module à choix libre", 9, [
 ("Enseignements à choix libre", "", 6, [], "", "L"),
], 6, "Enseignements à choisir dans les autres orientations, d’autres facultés ou universités.")

# ---------- Géologie ----------
Y = [GEO]
mod(Y, "2e", "Module 1 – Géologie structurale et pétrologie", 10, [
 ("Pétrographie magmatique et métamorphique", "O. Müntener (coord.), P. Lanari", 3, [ECR+" (2h)", CCI], "26C 26TP", "O"),
 ("Géologie structurale", "A. Samsu", 6, [PRA, ORA], "26C 48TP 4T", "O"),
 ("Camp de géologie structurale", "A. Samsu", 3, [PRA], "48T", "O"),
 ("Camp de pétrologie magmatique", "O. Müntener (coord.), S. Pilet", 3, [PRA], "72T", "O"),
], 15)
mod(Y, "2e", "Module 2 – Sédimentologie, géomorphologie et paléontologie", 10, [
 ("Sédimentologie physique", "S. Jaccard (resp.), B. Bomou", 3, [ECR+" (3h)"], "26C 26TP", "O"),
 ("Géomorphologie I", "E. Reynard", 3, [ECR+" (2h)"], "26C", "O"),
 ("Géomorphologie II", "C. Lambiel", 3, [ORA], "26CTP", "O"),
 ("Paléontologie", "A. Daley (resp.), A. Pictet", 3, [ECR+" (2h)", PRA], "26C 26TP", "O"),
 ("Camp de stratigraphie et sédimentologie", "S. Jaccard (resp.), B. Bomou", 3, [PRA], "72T", "O"),
], 15)
mod(Y, "2e", "Module 3 – Géophysique et risques", 10, [
 ("Physique du globe", "J. Irving", 3, [PRA, ECR+" (3h)"], "24C 20E", "O"),
 ("Télédétection", "G. Mariéthoz", 3, [CCI], "26C 26TP", "O"),
 ("Tectonique et géodynamique", "S. Schmalholz", 3, [PRA], "26C 26TP", "O"),
 ("Risques environnementaux", "M. Jaboyedoff", 3, [ECR+" (2h)"], "27C 9E", "O"),
], 12)
mod(Y, "2e", "Module 4 – Sciences et méthodes de base", 10, [
 ("Géochimie environnementale", "J. Marin-Carbonne", 3, [PRA], "26C", "O"),
 ("Introduction à la géochimie isotopique", "T. Vennemann (resp.), M. Galvez", 3, [ECR+" (2h)"], "26C 26E", "O"),
 ("Analyse vectorielle", "P. De Anna", 3, [PRA, ORA], "18C 18E", "O"),
 ("Physique générale II", "S. Bréchet / EPFL", 3, [ECR+" (2h)"], "26C 28E", "O"),
 ("Modélisation numérique", "G. Jouvet", 3, [CCI], "13C 26E", "O"),
], 15)
mod(Y, "3e", "Module 5 – Géologie avancée", 10, [
 ("Pétrologie magmatique et métamorphique", "P. Lanari (coord.), O. Müntener", 3, [ORA, CCI], "26C 26TP", "O"),
 ("Thermodynamique et cinétique", "O. Müntener (coord.), J. Marin-Carbonne, P. Lanari", 3, [CCI], "26C 13E", "O"),
 ("Pétrologie métamorphique, camp", "P. Lanari", 5, [PRA], "80T", "O"),
 ("Géologie de la chaîne alpine", "O. Müntener (coord.), S. Schmalholz, P. Lanari", 3, [PRA], "12C 24T", "O"),
], 14)
mod(Y, "3e", "Module 6 – Géologie de la surface terrestre", 11, [
 ("Géoinformatique II", "T. Beucler", 3, [CCI], "26CTP", "O"),
 ("Érosion, tectonique et climat", "G. Jouvet (resp.), J.-D. Champagnac, G. King", 3, [PRA], "18C 13TP", "O"),
 ("Hydrogéologie générale", "P. Renard, C. Roques / UNINE", 3, [CCI], "24CE 8T", "O"),
 ("Sédimentologie biochimique", "S. Jaccard", 3, [ECR+" (3h)"], "26C 26TP", "O"),
 ("Camp de cartographie et paléontologie", "A. Daley (coord.), S. Jaccard, B. Bomou", 3, [PRA], "40T", "O"),
], 15)
mod(Y, "3e", "Module 7 – Géologie de l’exploration", 11, [
 ("Géophysique d’exploration", "K. Holliger", 6, [CCI], "44C 44TP", "O"),
 ("Géophysique d’exploration – camp", "J. Irving (coord.), N. Linde, B. Quintal", 6, [PRA], "120T", "O"),
 ("Géologie de l’ingénieur", "M. Violay (EPFL) (coord.), O. Müntener, P. Lanari", 3, [ECR+" (2h)"], "22C 14E 8T", "O"),
 ("Géologie de l’ingénieur, excursion", "B. Quintal (coord.), L. Baron", 1, [PRA], "12T", "O"),
], 16)
mod(Y, "3e", "Module 8 – Travail de Bachelor", 11, [
 ("Préparation au travail de Bachelor", "J. Salomon Cavin (coord.)", 9, [PRA], "17CE", "O"),
 ("Travail de Bachelor", "", 0, [], "", "O"),
], 9, "Une seule note pour 9 ECTS, donnée par la personne qui supervise le travail.")
mod(Y, "2e/3e", "Module 9 – Module à choix libre", 12, [
 ("Enseignements à choix libre", "", 9, [], "", "L"),
 ("Principes de la science atmosphérique", "D. Domeisen", 3, [], "", "L"),
], 9, "Enseignements à choisir dans les autres orientations, d’autres facultés ou universités. Liste proposée à l’automne : Micropaléontologie (UNIGE), Principes de la science atmosphérique, Ressources minérales (UNIGE), Gestion de l’eau, Méthodes quantitatives III, Pédologie, Hydrauliques, formes et processus fluviaux, Hydrologie, Droit de l’environnement, Écotoxicologie, Hydrochimie et pollution des eaux, Écologie végétale.")

ALIAS = {('Dynamiques urbaines', '3e'): 'DYNAURBACAM',
         ('Pétrologie magmatique et métamorphique', '3e'): 'PETRMAGMAVA'}
MULTI = {'Éléments d’écologie'}   # listé deux fois (blocs A et B) : les deux positions comptent
HRE = re.compile(r'^\d+(C|S|E|TP|T|CE|CS|CTP|ST|CT)$')

def norm(s):
    s = unicodedata.normalize('NFD', s.replace('’', "'")).lower()
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()

def semestres(pdf):
    """Pour chaque page : jetons d'heures avec leur semestre (A/P) lu sur la colonne."""
    doc = fitz.open(pdf); out = {}; reportees = []
    for pn in range(2, len(doc)):
        ws = doc[pn].get_text("words")
        heads = []
        for w in ws:
            if w[4] == 'Automne': heads.append([w[1], (w[0]+w[2])/2, None])
        for h in heads:
            for w in ws:
                if w[4] == 'Printemps' and abs(w[1]-h[0]) < 3: h[2] = (w[0]+w[2])/2
        heads = [h for h in heads if h[2]]
        heads = reportees + heads            # tableau qui continue : l'en-tête de la page précédente vaut
        if heads: reportees = [[-1, heads[-1][1], heads[-1][2]]]
        toks = []
        UN = ('CS', 'CTP', 'CE', 'ST', 'TP', 'C', 'S', 'E', 'T')
        fus, drop = [], set()
        for i, w in enumerate(ws[:-1]):      # « 26 » + « CS » : deux mots dans le PDF
            n = ws[i+1]
            if re.fullmatch(r'\d+', w[4]) and n[4] in UN and abs(n[1]-w[1]) < 2 and 0 <= n[0]-w[2] < 4:
                fus.append((w[0], w[1], n[2], n[3], w[4]+n[4])); drop.update({i, i+1})
        ws = [w for i, w in enumerate(ws) if i not in drop] + fus
        for i, w in enumerate(ws):
            t = w[4]
            if not HRE.match(t): continue
            hs = [h for h in heads if h[0] <= w[1]+1]
            if not hs: continue
            h = hs[-1]; mid = (h[1]+h[2])/2
            toks.append((w[1], 'A' if (w[0]+w[2])/2 < mid else 'P'))
        out[pn+1] = (doc[pn], toks)
    return out

def trouver_y(page, titre, apres):
    base = titre.split(' : ')[0] if len(titre) > 55 else titre
    base = base[:38]
    var = [base, re.sub(r'\bÉ', 'E', base), ' '.join(base.split()[:3]), re.sub(r'\bÉ', 'E', ' '.join(base.split()[:3])),
           ' '.join(base.split()[:2])]
    for v in var:
        for q in (v, v.replace('’', "'")):
            cand = [r for r in page.search_for(q) if r.x0 < 260 and r.y0 > apres + 1]
            if cand: return min(cand, key=lambda r: r.y0).y0
    return None

def main(pdf):
    ens = list(csv.DictReader(open('data/enseignements.csv', encoding='utf-8')))
    nb = {}
    for e in ens:
        nb.setdefault(norm(re.sub(r'\s*\((GES|SE|Géologie)\)\s*$', '', e['enseignement'])), []).append(e)
    pg = semestres(pdf)
    rows, pid, manques = [], 0, []
    derniere = {}
    # 1) position de chaque titre dans la page
    pos = {}   # (index module, index ligne) -> (page, y)
    extra = []
    for mi, m in enumerate(M):
        pcur = m['page']
        for ri, r in enumerate(m['rows']):
            if r[5] == 'L' or r[0] == 'Travail de Bachelor': continue
            y = trouver_y(pg[pcur][0], r[0], derniere.get(pcur, 0))
            if y is None and pcur+1 in pg:           # le module déborde sur la page suivante
                y2 = trouver_y(pg[pcur+1][0], r[0], 0)
                if y2 is not None: pcur += 1; y = y2
            if y is None: manques.append(('TITRE INTROUVABLE', m['module'], r[0])); continue
            pos[(mi, ri)] = (pcur, y); derniere[pcur] = y
            if r[0] in MULTI:
                for q in pg[pcur][0].search_for(r[0].replace('É', 'E')[:20]):
                    if q.x0 < 260 and abs(q.y0-y) > 2: extra.append(((mi, ri), pcur, q.y0))
    # 2) chaque jeton d'heures va au titre le plus proche (même page)
    sems = {}
    for p, (page, toks) in pg.items():
        cands = [(y, k) for k, (pp, y) in pos.items() if pp == p] + [(y, k) for k, pp, y in extra if pp == p]
        cands.sort()
        for ty, sem in toks:      # un jeton appartient à la ligne dont le titre le précède de plus près
            avant = [c for c in cands if c[0] <= ty + 2]
            if avant: sems.setdefault(avant[-1][1], set()).add(sem)
    for mi, m in enumerate(M):
        for ri, (titre, prof, ects, ev, h, typ) in enumerate(m['rows']):
            s = sems.get((mi, ri), set())
            sem = {'A': 'Automne', 'P': 'Printemps'}.get(''.join(s), 'Automne et printemps' if s else '')
            if not sem and h: manques.append(('SEMESTRE ?', m['module'], titre))
            cands = nb.get(norm(titre), [])
            if len(cands) > 1:
                cands = [e for e in cands if any(p.split(',')[0][:6] in e['orientation'] or p == e['orientation'] for p in m['parc'])
                         or e['orientation'] == 'Propédeutique'] or cands
                if len(cands) > 1:
                    cands = [e for e in cands if e['annee'].startswith(m['an'][:2]) or m['an'] in e['annee']] or cands
            # variantes (GES)/(SE) pour Excursions et cas d'études
            if titre.startswith('Excursions et cas'):
                suf = 'GES' if m['parc'] == [GES] else 'SE'
                cands = [e for e in ens if e['enseignement'] == f"Excursions et cas d'études ({suf})"]
            eid = cands[0]['id'] if cands else ALIAS.get((titre, m['an']), '')
            if not eid and typ != 'L' and titre != 'Travail de Bachelor':
                manques.append((m['module'], titre))
            pid += 1
            acts = sorted(set(re.findall(r'\d+(CTP|CE|CS|ST|CT|TP|C|S|E|T)', h)))
            sym = []
            for a in re.findall(r'\d+(CTP|CE|CS|ST|CT|TP|C|S|E|T)', h):
                for p in ({'CTP': ['C', 'TP'], 'CE': ['C', 'E'], 'CS': ['C', 'S'], 'ST': ['S', 'T'], 'CT': ['C', 'T']}.get(a, [a])):
                    if p not in sym: sym.append(p)
            rows.append(dict(
                id=f"P{pid:03d}", cours=titre, eid=eid, module=m['module'], parcours=m['parc'], annee=m['an'],
                type={'O': 'Obligatoire', 'C': 'À choisir', 'L': 'Choix libre'}[typ],
                sem=sem, heures=h, acts=sym, eval=[re.sub(r' \(.*\)', '', x) for x in ev], eval_det=ev,
                ects=ects, ens=prof, exiges=m['exiges'], note=m['note']))
    json.dump(rows, open('data/plan.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(len(rows), 'lignes ; sans correspondance :')
    for x in manques: print('  ', x)

if __name__ == '__main__':
    main(sys.argv[1])
