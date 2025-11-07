import json
import os
import sys

# Permet d'importer class_sportif.py situé dans le dossier parent
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from class_sportif import Sportif


# =========================
# Préparation du contexte
# =========================

def creer_json_test(path: str):
    """Crée un fichier JSON de test avec deux sportifs."""
    data = [
        {
            "nom": "Durand",
            "prenom": "Julien",
            "sexe": "Homme",
            "age": 29,
            "photo_profil": None
        },
        {
            "nom": "Leroy",
            "prenom": "Amélie",
            "sexe": "Femme",
            "age": 23,
            "photo_profil": None
        }
    ]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"🧩 Fichier JSON de test créé → {path}\n")


# =========================
# Test principal
# =========================

def test_ajouter_photo():
    print("=== TEST : ajout d'une vraie photo locale ===")

    # 1️⃣ Crée un JSON de base dans le dossier parent
    json_path = os.path.join(os.path.dirname(__file__), "..", "data.json")
    creer_json_test(json_path)

    # 2️⃣ Crée l'objet sportif
    s = Sportif(prenom="Julien", nom="Durand")

    # 3️⃣ Chemin de ton vrai fichier image local
    chemin_photo = os.path.join(os.path.dirname(__file__), "..", "uploads", "test_profil.png")

    # Vérifie que le fichier existe avant de continuer
    if not os.path.exists(chemin_photo):
        print(f"❌ Le fichier {chemin_photo} n'existe pas — vérifie ton dossier 'uploads'.")
        return

    # 4️⃣ Appelle la méthode de ta classe
    ok = s.ajouter_photo_dans_json(chemin_photo, json_path)

    # 5️⃣ Vérifie que la mise à jour a été faite
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    maj_ok = any(
        e.get("prenom") == "Julien"
        and e.get("nom") == "Durand"
        and e.get("photo_profil") == chemin_photo.replace("\\", "/")
        for e in data
    )

    # 6️⃣ Résultat du test
    if ok and maj_ok:
        print("✅ TEST RÉUSSI : la vraie photo a bien été enregistrée dans data.json.\n")
    else:
        print("❌ TEST ÉCHOUÉ : la photo n'a pas été correctement enregistrée.\n")


# =========================
# Lancement direct
# =========================

if __name__ == "__main__":
    test_ajouter_photo()
