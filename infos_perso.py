import sys
import os

chemin_actuel = os.getcwd()
sys.path.append(chemin_actuel)

from class_sportif import *


def func_infos_personelles(
    nom: str, 
    prenom:str,
    sexe: str,
    age: int, 
    nationalite: str,
    localisalisation: list[float],
    distance_rencontre: int,
    niveau_sports: dict,
    attentes: list[str],
    genre_recherche: str,
    min_age_recherchee: int, 
    max_age_recherchee: int
):
    
    sportif = Sportif(
        nom = nom,
        prenom = prenom,
        sexe = sexe,
        age = age,
        nationalite = nationalite,
        localisalisation = localisalisation,
        distance_rencontre = distance_rencontre,
        niveau_sports = niveau_sports, 
        attentes = attentes,
        genre_recherche = genre_recherche,
        min_age_recherchee = min_age_recherchee,
        max_age_recherchee = max_age_recherchee,
    )

    return sportif 
