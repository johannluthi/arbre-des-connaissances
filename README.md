# Arbre des connaissances — Bachelor FGSE

Cartographie des compétences développées par les étudiantes et étudiants dans les
enseignements du **Baccalauréat universitaire ès Sciences en géosciences et environnement**
de l'Université de Lausanne, plan d'études 2026-2027.

**→ [Consulter le site](https://johannluthi.github.io/arbre-des-connaissances/)** — tri, filtres et recherche.

## Ce que contient ce dépôt

| Fichier | Contenu |
|---|---|
| `index.html` | Le site : deux tableaux triables, filtrables et cherchables |
| `data/competences.csv` | Une ligne par compétence |
| `data/enseignements.csv` | Une ligne par enseignement |
| `data/arbre.json` | Les deux jeux de données réunis |

## Ce qui est publié, et ce qui ne l'est pas

**Chaque compétence de ce dépôt a été rédigée ou approuvée par l'enseignant·e responsable du
cours.** Le champ `valide_par` nomme la personne. Rien d'autre n'est publié.

Le recensement est en cours : les enseignements marqués « À documenter » n'ont pas encore fait
l'objet d'une réponse. Le travail préparatoire — propositions rédigées pour amorcer la
consultation — reste interne au groupe thématique et n'a pas vocation à être publié : il
n'engagerait pas les personnes citées.

## Colonnes

### `competences.csv`

| Colonne | Description |
|---|---|
| `id` | Identifiant stable, dérivé de l'intitulé du cours (`GEOMORI-2`) |
| `categorie` | Connaissances disciplinaires · Terrain / Méthodo · Techniques et informatique · Soft Skills |
| `competence` | La compétence, formulée du point de vue de l'étudiant·e |
| `enseignement`, `orientation`, `annee` | Rattachement au cursus |
| `statut`, `valide_par` | Toujours `Validé`, et le nom de l'enseignant·e |
| `sappuie_sur` | Identifiants des compétences prérequises, quand l'enseignant·e les a signalées |

### `enseignements.csv`

Intitulé, module, orientation, année, ECTS, responsable, rattachement, nombre de compétences
recensées et validées, état de la consultation.

## Méthode

1. Dépouillement du plan d'études 2026-2027 : 100 enseignements, 50 responsables FGSE.
2. Rédaction de 2 à 3 propositions de compétences par cours, à partir de l'intitulé, du volume
   horaire, de la modalité d'évaluation et de la fiche Moodle quand elle était renseignée.
3. Consultation de chaque enseignant·e responsable, avec ces propositions comme point de départ
   plutôt qu'une page blanche.
4. **Seules les compétences issues de l'étape 3 sont publiées ici.**

Les propositions de l'étape 2 avaient un biais assumé : lorsque la spécialité de recherche de
l'enseignant·e était identifiable, elles tendaient à réduire le cours à cette spécialité.
Plusieurs enseignant·e·s l'ont relevé et corrigé. C'est précisément pourquoi elles ne sont pas
publiées et pourquoi seul le retour des intéressé·e·s fait foi.

## Données personnelles

Le site ne publie **aucune adresse électronique**. Les noms des enseignant·e·s responsables
figurent au plan d'études, document public de la Faculté.

## Corrections

Toute personne citée peut demander la modification ou le retrait d'une ligne la concernant,
par *issue* sur ce dépôt ou par courriel.

## Régénérer le site

Les fichiers sont produits par une chaîne de dépouillement et de consolidation des réponses
qui vit hors de ce dépôt. `index.html` embarque ses données : il s'ouvre tel quel, sans serveur
et sans dépendance externe.
