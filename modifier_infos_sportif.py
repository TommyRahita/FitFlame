import sys

import sys
import os

chemin_actuel = os.getcwd()
sys.path.append(chemin_actuel)

from class_sportif import *

def func_modif_infos_sportifs(
    sportif: Sportif,
    dict_modifs: dict  # Dicitonnaire sous la forme {"nom_champ_a_modifier": nouvelle valeur, "nom_champ_a_modifier": nouvelle valeur ...}
) -> Sportif:
    
    for champ_a_modifier, nouvelle_valeur in dict_modifs.items():
        # Vérifie que le champ existe avant de modifier
        if hasattr(sportif, champ_a_modifier):
            setattr(sportif, champ_a_modifier, nouvelle_valeur)
        else:
            print(f"Champ '{champ_a_modifier}' introuvable dans Sportif — ignoré.")
        
    return sportif