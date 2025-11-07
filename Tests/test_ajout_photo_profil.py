# Tests/test_add_user_with_photo.py
import os, sys, json

# permettre l'import depuis le dossier parent (où se trouve class_sportif.py)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from class_sportif import Sportif

def charger_json(json_path: str) -> list:
    if not os.path.isfile(json_path):
        raise FileNotFoundError(f"JSON introuvable: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("Le JSON doit contenir une liste d'utilisateurs.")
    return data

def ecrire_json(json_path: str, data: list) -> None:
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def ajouter_ou_mettre_a_jour_sportif_avec_photo(
    data: list, sportif: Sportif, chemin_photo: str
) -> bool:
    """
    Ajoute le sportif s'il n'existe pas (clé = prenom+nom),
    sinon met à jour son 'photo_profil'.
    Retourne True si une écriture a été faite, False sinon.
    """
    if not (sportif.prenom and sportif.nom):
        print("❌ prénom/nom manquant.")
        return False

    # normaliser le chemin pour le JSON (slashes)
    chemin_photo = chemin_photo.replace("\\", "/")

    # 1) existe déjà ? -> update
    for entry in data:
        if entry.get("prenom") == sportif.prenom and entry.get("nom") == sportif.nom:
            entry["photo_profil"] = chemin_photo
            return True

    # 2) sinon -> on ajoute un nouvel objet au format de ton JSON
    nouvel_obj = {
        "nom": sportif.nom,
        "prenom": sportif.prenom,
        "sexe": sportif.sexe,
        "age": sportif.age,
        "nationalite": sportif.nationalite,
        # ta clé existante est 'localisalisation' (avec un s), on reste compatible
        "localisalisation": list(sportif.localisation) if getattr(sportif, "localisation", None) else None,
        "distance_rencontre": sportif.distance_rencontre,
        "niveau_sports": sportif.niveau_sports or {},
        "attentes": sportif.attentes or [],
        "genre_recherche": sportif.genre_recherche,
        "min_age_recherchee": sportif.min_age_recherchee,
        "max_age_recherchee": sportif.max_age_recherchee,
        "photo_profil": chemin_photo
        # 'galerie_photos' est optionnelle dans ton JSON ; on peut l'ajouter plus tard
    }
    data.append(nouvel_obj)
    return True

def test_add_or_update_user_with_real_photo():
    print("=== TEST : charger JSON + ajouter/met à jour un utilisateur avec sa vraie photo ===")

    json_path = os.path.join(BASE_DIR, "data.json")
    photo_path_abs = os.path.join(BASE_DIR, "uploads", "test_profil.png")
    photo_path_rel = "uploads/test_profil.png"  # ce qu'on veut écrire dans le JSON

    if not os.path.exists(photo_path_abs):
        print(f"❌ Fichier image manquant : {photo_path_abs}")
        return

    try:
        data = charger_json(json_path)
    except Exception as e:
        print(f"❌ Erreur chargement JSON : {e}")
        return

    # Ex : on cible Julien Durand
    s = Sportif(prenom="Julien", nom="Durand", sexe="Homme", age=29)

    changed = ajouter_ou_mettre_a_jour_sportif_avec_photo(data, s, photo_path_rel)
    if not changed:
        print("❌ Rien n'a été modifié (prénom/nom manquant ?).")
        return

    # Écrire le JSON mis à jour
    ecrire_json(json_path, data)

    # Recharger pour vérifier
    verif = charger_json(json_path)
    ok = any(
        e.get("prenom") == "Julien" and
        e.get("nom") == "Durand" and
        e.get("photo_profil") == photo_path_rel
        for e in verif
    )

    if ok:
        print("✅ TEST RÉUSSI : utilisateur présent et photo_profil correctement enregistrée dans data.json.\n")
    else:
        print("❌ TEST ÉCHOUÉ : la mise à jour n'a pas été retrouvée dans data.json.\n")

if __name__ == "__main__":
    test_add_or_update_user_with_real_photo()
