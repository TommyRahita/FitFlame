import sys
import os
import json
import math


chemin_actuel = os.getcwd()
sys.path.append(chemin_actuel)

from class_sportif import *


def func_calculer_distance(lat1, lon1, lat2, lon2):
        """
        Calcule la distance entre deux points GPS.
        Les coordonnées doivent être en degrés décimaux.
        Retourne la distance en kilomètres (km).
        """
        R = 6371  # Rayon de la Terre en kilomètres
        
        # 1. Conversion des degrés en radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        # 2. Différences de coordonnées
        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad

        # 3. Application de la formule de Haversine
        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance = R * c
        return distance


def func_algo_matching(
    sportif_a_matcher: Sportif
):

    if sportif_a_matcher.nb_swipes_restants == 0:
         print("0 swipes restants")
         return []

    with open("data.json", 'r', encoding='utf-8') as fichier:
        liste_sportifs = json.load(fichier)

    liste_sportifs_match = []

    for dict_sportif in liste_sportifs:
        current_sportif = Sportif(
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
            # photo_profil = dict_sportif['photo_profil'],
            # galerie_photos = dict_sportif['galerie_photos'],
            nb_swipes_restants = dict_sportif['nb_swipes_restants']
        )

        if current_sportif.prenom != "Amélie":
            continue

        if current_sportif.nb_swipes_restants == 0:
            print("0 swipes restants")
            continue

        if sportif_a_matcher.attentes == current_sportif.attentes:
            print("attentes diffétentes")
            continue
        
        if not(sportif_a_matcher.min_age_recherchee <= current_sportif.age <= sportif_a_matcher.max_age_recherchee) or not(current_sportif.min_age_recherchee <= sportif_a_matcher.age <= current_sportif.max_age_recherchee):
            print("age different")
            continue

        if (sportif_a_matcher.genre_recherche != current_sportif.sexe) or (sportif_a_matcher.sexe != current_sportif.genre_recherche):
            print("genre recherché incompatible")
            continue
        
        distance_entre_les_deux = func_calculer_distance(
             lat1 = sportif_a_matcher.localisation[0],
             lon1 = sportif_a_matcher.localisation[1],
             lat2 = current_sportif.localisation[0],
             lon2 = current_sportif.localisation[1]
        )
        
        if (sportif_a_matcher.distance_rencontre < distance_entre_les_deux) or (current_sportif.distance_rencontre < distance_entre_les_deux):
            print("trop loin")
            continue    

        liste_sportifs_match.append(current_sportif)

    return liste_sportifs_match
