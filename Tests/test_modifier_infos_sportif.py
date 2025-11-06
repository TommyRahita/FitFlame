import sys
import os

chemin_actuel = os.getcwd()
chemin_parent = os.path.dirname(chemin_actuel)
sys.path.append(chemin_parent)

from class_sportif import *
from modifier_infos_sportif import *

def func_test_modif_infos_sportifs():
    # Création d'un sportif de base
    sportif_initial = Sportif(
        nom="Lemoine",
        prenom="Julie",
        sexe="Femme",
        age=27,
        nationalite="Française",
        localisalisation=[48.85, 2.35],
        distance_rencontre=10,
        niveau_sports={"yoga": "débutant"},
        attentes=["bien-être"],
        genre_recherche="Homme",
        min_age_recherchee=25,
        max_age_recherchee=33
    )

    print("=== Avant modification ===")
    print(sportif_initial)

    # Modifications à appliquer
    modifications = {
        "age": 28,
        "nationalite": "Suisse",
        "niveau_sports": {"yoga": "avancé", "course": "intermédiaire"},
        "ville": "Paris"  # Ce champ n’existe pas
    }

    sportif_modifie = func_modif_infos_sportifs(sportif_initial, modifications)

    print("\n=== Après modification ===")
    print(sportif_modifie)

    # Vérifications avec des assertions
    assert sportif_modifie.age == 28, "❌ L'âge n'a pas été correctement modifié."
    assert sportif_modifie.nationalite == "Suisse", "❌ La nationalité n'a pas été modifiée."
    assert "course" in sportif_modifie.niveau_sports, "❌ Le champ niveau_sports n'a pas été mis à jour correctement."

    print("\n✅ Tous les tests sont passés avec succès !")

func_test_modif_infos_sportifs()