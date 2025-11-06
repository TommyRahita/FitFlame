from typing import Optional, Tuple, Dict
import os
from class_sportif import Sportif

# =========================
# "Base de données" en mémoire
# =========================

sportifs: Dict[int, Sportif] = {
    1: Sportif(prenom="Alice", nom="Martin", age=24),
    2: Sportif(prenom="Bob", nom="Durand", age=28),
}

# =========================
# Fonctions utilitaires
# =========================

def est_image(contenu: bytes) -> bool:
    """Reconnaissance ultra-simple: PNG ou JPEG via signatures magiques."""
    return (
        contenu.startswith(b"\x89PNG") or   # PNG
        contenu.startswith(b"\xFF\xD8")     # JPEG
    )

def ajouter_photo_profil(sportif_id: int, chemin_fichier: str) -> bool:
    """
    Lit une image locale et la stocke dans Sportif.photo_profil.
    Retourne True si succès, False sinon.
    """
    sportif = sportifs.get(sportif_id)
    if not sportif:
        print("Sportif introuvable.")
        return False

    if not os.path.exists(chemin_fichier):
        print(f"Fichier '{chemin_fichier}' introuvable.")
        return False

    with open(chemin_fichier, "rb") as f:
        contenu = f.read()

    if not est_image(contenu):
        print("Le fichier n'est pas reconnu comme image PNG/JPEG.")
        return False

    sportif.photo_profil = contenu
    print(f"Photo de profil ajoutée pour {sportif.prenom} {sportif.nom}.")
    return True

# =========================
# Tests
# =========================

def test_photo_existe():
    """Test avec une vraie image locale existante."""
    print("— Test : fichier existant —")
    chemin = "uploads/test_profil.png"

    sportifs[1].photo_profil = None

    ok = ajouter_photo_profil(1, chemin)
    if ok and sportifs[1].photo_profil:
        print("TEST RÉUSSI : la photo de profil a bien été ajoutée.\n")
    else:
        print("TEST ÉCHOUÉ : la photo n’a pas été enregistrée.\n")

def test_photo_absente():
    """Test avec un fichier inexistant (doit échouer sans modifier l'état)."""
    print("— Test : fichier non existant —")
    chemin = "fichier_inexistant.png"

    sportifs[1].photo_profil = None

    ok = ajouter_photo_profil(1, chemin)
    if not ok and sportifs[1].photo_profil is None:
        print("TEST RÉUSSI : fichier manquant bien détecté, aucune photo enregistrée.\n")
    else:
        print("TEST ÉCHOUÉ : état incorrect après tentative avec fichier absent.\n")

if __name__ == "__main__":
    test_photo_existe()
    test_photo_absente()
