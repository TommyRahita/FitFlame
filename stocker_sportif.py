import sys
import os
import json

chemin_actuel = os.getcwd()
sys.path.append(chemin_actuel)

from class_sportif import *

def func_stocker_sportif(nouveau_sportif: Sportif):

    nom_fichier = 'data.json' 
    
    try:
        # Ouvrir et lire le fichier existant
        with open(nom_fichier, 'r', encoding='utf-8') as fichier:
            donnees = json.load(fichier)
            
        # Vérifier que donnees est bien une liste avant d'ajouter
        if isinstance(donnees, list):
            # Ajouter le nouvel objet à la liste
            donnees.append(nouveau_sportif)
        else:
            # Cas où le fichier était vide ou mal formaté, créer une nouvelle liste
            donnees = [nouveau_sportif]
            
        print(f"✅ Le sportif {nouveau_sportif['prenom']} a été ajouté à la liste Python.")

        # Ouvrir le fichier en mode écriture ('w') pour le réécrire complètement
        with open(nom_fichier, 'w', encoding='utf-8') as fichier:
            # Utiliser json.dump pour écrire la liste complète.
            # indent=2 pour un formatage lisible.
            json.dump(donnees, fichier, indent=2, ensure_ascii=False) 
            
        print(f"💾 Le fichier {nom_fichier} a été mis à jour avec le nouveau sportif.")

    except FileNotFoundError:
        print(f"⚠️ Le fichier {nom_fichier} n'a pas été trouvé. Création d'un nouveau fichier avec uniquement ce sportif.")
            

    except Exception as e:
        print(f"❌ Une erreur inattendue s'est produite : {e}")