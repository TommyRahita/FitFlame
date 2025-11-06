import sys
import os
import json
from dataclasses import asdict

chemin_actuel = os.getcwd()
chemin_parent = os.path.dirname(chemin_actuel)
sys.path.append(chemin_parent)

from class_sportif import *
import json
import os

# La classe Sportif est une dataclass importée

def func_stocker_sportif(nouveau_sportif):
    nom_fichier = 'data.json' 
    
    # 1. Conversion de l'objet Sportif en dictionnaire.
    sportif_dict = asdict(nouveau_sportif)
    
    # 2. Gestion de l'attribut 'photo_profil' (bytes) non sérialisable en JSON
    if 'photo_profil' in sportif_dict and isinstance(sportif_dict['photo_profil'], bytes):
        # Conversion en chaîne de caractères simple pour l'exemple
        sportif_dict['photo_profil'] = 'bytes_dummy_replaced'

    try:
        # Tenter d'ouvrir et lire le fichier existant
        with open(nom_fichier, 'r', encoding='utf-8') as fichier:
            donnees = json.load(fichier)
            
        # Ajouter le nouveau dictionnaire à la liste
        if isinstance(donnees, list):
            donnees.append(sportif_dict)
        else:
            donnees = [sportif_dict]
            
        print(f"✅ Le sportif {sportif_dict['prenom']} a été ajouté à la liste Python.")

        # Ouvrir le fichier en mode écriture ('w') pour le réécrire complètement
        with open(nom_fichier, 'w', encoding='utf-8') as fichier:
            json.dump(donnees, fichier, indent=2, ensure_ascii=False) 
            
        print(f"💾 Le fichier {nom_fichier} a été mis à jour avec le nouveau sportif.")

    except FileNotFoundError:
        print(f"⚠️ Le fichier {nom_fichier} n'a pas été trouvé. Création d'un nouveau fichier avec uniquement ce sportif.")
        # Création du fichier
        with open(nom_fichier, 'w', encoding='utf-8') as fichier:
            json.dump([sportif_dict], fichier, indent=2, ensure_ascii=False)
            
        print(f"💾 Le fichier {nom_fichier} a été créé et le sportif {sportif_dict['prenom']} ajouté.")

    except Exception as e:
        print(f"❌ Une erreur inattendue s'est produite : {e}")


sportif_1 = Sportif(
    nom="Dupond", 
    prenom="Pierre", 
    sexe="Homme", 
    age=30, 
    nationalite="Française", 
    localisalisation=[48.8, 2.3], 
    distance_rencontre=20, 
    niveau_sports={"Judo": "Expert"}, 
    attentes=["Entraînement intensif"], 
    genre_recherche="Femme", 
    min_age_recherchee=25, 
    max_age_recherchee=35, 
    photo_profil=b'dummy1_bytes'
)

func_stocker_sportif(sportif_1)