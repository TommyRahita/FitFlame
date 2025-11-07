# Tests/test_galerie.py
import os
import sys
import json

# Permet d'importer la classe Sportif depuis le dossier parent
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from class_sportif import Sportif

JSON_PATH = os.path.join(BASE_DIR, "data.json")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
PHOTO_REL = "uploads/test_galerie.png"  # ce qui sera écrit dans le JSON
PHOTO_ABS = os.path.join(BASE_DIR, PHOTO_REL.replace("/", os.sep))


def _ensure_uploads_dir():
    if not os.path.isdir(UPLOADS_DIR):
        os.makedirs(UPLOADS_DIR, exist_ok=True)


def _ensure_json_with_user(json_path: str, prenom: str, nom: str):
    """
    Crée un JSON minimal si absent.
    Si présent mais sans l'utilisateur, l'ajoute.
    """
    data = []
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                data = []
        except Exception:
            data = []

    # utilisateur présent ?
    exists = any(e.get("prenom") == prenom and e.get("nom") == nom for e in data)
    if not exists:
        data.append({
            "nom": nom,
            "prenom": prenom,
            "sexe": None,
            "age": None,
            "nationalite": None,
            "localisalisation": None,  # on garde la compat avec ton JSON existant
            "distance_rencontre": None,
            "niveau_sports": {},
            "attentes": [],
            "genre_recherche": None,
            "min_age_recherchee": None,
            "max_age_recherchee": None,
            "photo_profil": None
            # 'galerie_photos' sera créée par la méthode si absente
        })

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _read_json(json_path: str) -> list:
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_ajout_galerie():
    print("— Test : ajout à la galerie —")
    _ensure_uploads_dir()
    if not os.path.exists(PHOTO_ABS):
        print(f"⚠️ Image de test absente : {PHOTO_ABS}")
        print("   Ajoute un vrai fichier 'uploads/test_galerie.png' puis relance le test.")
        return

    # Préparer JSON et sportif
    _ensure_json_with_user(JSON_PATH, "Julien", "Durand")
    s = Sportif(prenom="Julien", nom="Durand")

    # 1) ajout
    ok = s.ajouter_photo_galerie_dans_json(PHOTO_REL, JSON_PATH)
    data = _read_json(JSON_PATH)
    in_json = any(
        e.get("prenom") == "Julien"
        and e.get("nom") == "Durand"
        and PHOTO_REL in (e.get("galerie_photos") or [])
        for e in data
    )
    if ok and in_json and PHOTO_REL in s.galerie_photos:
        print("✅ Ajout OK (écrit dans JSON et dans l'objet).")
    else:
        print("❌ Ajout KO.")
        return

    # 2) doublon (unique=True par défaut)
    ok2 = s.ajouter_photo_galerie_dans_json(PHOTO_REL, JSON_PATH, unique=True)
    data2 = _read_json(JSON_PATH)
    # doit rester une seule occurrence
    gal = next(
        (e.get("galerie_photos", []) for e in data2
         if e.get("prenom") == "Julien" and e.get("nom") == "Durand"),
        []
    )
    count = gal.count(PHOTO_REL)
    if count == 1:
        print("✅ Protection contre les doublons OK.")
    else:
        print("❌ Doublon non filtré.")
    print()


def test_suppression_galerie():
    print("— Test : suppression de la galerie —")
    _ensure_uploads_dir()
    _ensure_json_with_user(JSON_PATH, "Julien", "Durand")
    s = Sportif(prenom="Julien", nom="Durand")

    # S'assurer qu'une image est présente
    s.ajouter_photo_galerie_dans_json(PHOTO_REL, JSON_PATH)

    # 1) suppression par chemin exact
    ok_del = s.supprimer_photo_galerie_dans_json(PHOTO_REL, JSON_PATH)
    data = _read_json(JSON_PATH)
    still_in = any(
        e.get("prenom") == "Julien"
        and e.get("nom") == "Durand"
        and PHOTO_REL in (e.get("galerie_photos") or [])
        for e in data
    )
    if ok_del and not still_in and PHOTO_REL not in s.galerie_photos:
        print("✅ Suppression par chemin exact OK.")
    else:
        print("❌ Suppression par chemin exact KO.")
        return

    # 2) re-ajout puis suppression par basename
    s.ajouter_photo_galerie_dans_json(PHOTO_REL, JSON_PATH)
    basename = os.path.basename(PHOTO_REL)
    ok_del2 = s.supprimer_photo_galerie_dans_json(basename, JSON_PATH)
    data2 = _read_json(JSON_PATH)
    still_in2 = any(
        e.get("prenom") == "Julien"
        and e.get("nom") == "Durand"
        and PHOTO_REL in (e.get("galerie_photos") or [])
        for e in data2
    )
    if ok_del2 and not still_in2 and all(os.path.basename(p) != basename for p in s.galerie_photos):
        print("✅ Suppression par nom de fichier OK.")
    else:
        print("❌ Suppression par nom de fichier KO.")
    print()


if __name__ == "__main__":
    test_ajout_galerie()
    test_suppression_galerie()
