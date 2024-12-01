#!/bin/bash

# Merci LeChat

# Vérifie si un argument a été passé
if [ $# -ne 1 ]; then
  echo "Usage: $0 <jour>"
  exit 1
fi

# Récupère le jour passé en argument
jour=$1

# Vérifie si le jour est un nombre entre 01 et 31
if ! [[ $jour =~ ^(0[1-9]|[12][0-9]|3[01])$ ]]; then
  echo "Erreur: Le jour doit être un nombre entre 01 et 31."
  exit 1
fi

# Vérifie si le fichier 01.py existe
if [ ! -f "01.py" ]; then
  echo "Erreur: Le fichier 01.py n'existe pas."
  exit 1
fi

# Crée le fichier <jour>.py en dupliquant 01.py
cp 01.py "${jour}.py"

# Vérifie si le dossier data existe, sinon le crée
if [ ! -d "data" ]; then
  mkdir data
fi

# Crée les fichiers vides <jour>.in et <jour>.ex dans le dossier data
touch "data/${jour}.in"
touch "data/${jour}.ex"

echo "Fichiers créés avec succès: ${jour}.py, data/${jour}.in, data/${jour}.ex"
