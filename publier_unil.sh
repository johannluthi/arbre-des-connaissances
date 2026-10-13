#!/bin/bash
# Republie l'arbre des connaissances sur gse-sondage.unil.ch (SFTP, clé id_ed25519_unil).
# Ne publie que la page (arbre.html, déposée sous le nom index.html) et les 5 fichiers de données.
# Depuis le 13.10.2026, index.html du dépôt est la redirection GitHub, pas la page.
# Usage : ./publier_unil.sh
set -euo pipefail
cd "$(dirname "$0")"

BASE=quiz/arbre
URL=https://gse-sondage.unil.ch/quiz-rentree-fgse/arbre/
DATA="arbre.json competences.csv enseignements.csv parcours.csv plan.json"

[ -f arbre.html ] || { echo "arbre.html introuvable : lancer python3 build_html.py"; exit 1; }
for f in $DATA; do [ -f "data/$f" ] || { echo "data/$f introuvable"; exit 1; }; done

{
  echo "-mkdir $BASE"
  echo "-mkdir $BASE/data"
  echo "put arbre.html $BASE/index.html"
  for f in $DATA; do echo "put data/$f $BASE/data/$f"; done
} | sftp -q -i ~/.ssh/id_ed25519_unil -b - jluethi@gse-sondage.unil.ch 2>&1 \
  | grep -v -i 'quantum\|store now\|upgraded' || true

code=$(curl -s -o /tmp/arbre_unil.html -w '%{http_code}' "$URL")
if [ "$code" = 200 ] && cmp -s /tmp/arbre_unil.html arbre.html; then
  echo "OK : $URL (en ligne, identique au fichier local)"
else
  echo "ATTENTION : HTTP $code ou contenu différent de arbre.html"; exit 1
fi
