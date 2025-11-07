import sys
import os
import json


chemin_actuel = os.getcwd()
sys.path.append(chemin_actuel)

from class_sportif import *


def func_get_sportifs_from_json():
    with open("data.json", 'r', encoding='utf-8') as fichier:
        
        liste_sportifs = json.load(fichier)

    liste_sportifs_match = [Sportif(
            nom = dict_sportif['nom'],
            prenom = dict_sportif['prenom'],
            sexe = dict_sportif['sexe'],
            age = dict_sportif['age'],
            nationalite = dict_sportif['nationalite'],
            localisation = dict_sportif['localisation'],
            distance_rencontre = dict_sportif['distance_rencontre'],
            niveau_sports = dict_sportif['niveau_sports'],
            attentes = dict_sportif['attentes'],
            genre_recherche = dict_sportif['genre_recherche'],
            min_age_recherchee = dict_sportif['min_age_recherchee'],
            max_age_recherchee = dict_sportif['max_age_recherchee'],
            photo_profil = dict_sportif['photo_profil'],
            nb_swipes_restants = dict_sportif['nb_swipes_restants']
        )
            for dict_sportif in liste_sportifs 
    ]
    return liste_sportifs_match
