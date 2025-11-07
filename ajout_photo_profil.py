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
    """Reconnaissance simple via signatures magiques: PNG/JPEG/GIF/WebP."""
    if len(contenu) < 12:
        return False
    # PNG
    if contenu.startswith(b"\x89PNG\r\n\x1a\n"):
        return True
    # JPEG (SOI)
    if contenu[:2] == b"\xFF\xD8":
        return True
    # GIF87a / GIF89a
    if contenu.startswith(b"GIF87a") or contenu.startswith(b"GIF89a"):
        return True
    # WebP: RIFF....WEBP
    if contenu[:4] == b"RIFF" and contenu[8:12] == b"WEBP":
        return True
    return False


def ajouter_photo_profil(sportif_id: int, chemin_fichier: str) -> bool:
    """
    Lit une image locale, vérifie la signature, stocke les octets dans Sportif.photo_profil
    ET mémorise le chemin source dans Sportif.photo_profil_path (attribut dynamique).
    Retourne True si succès, False sinon.
    """
    sportif = sportifs.get(sportif_id)
    if not sportif:
        print("Sportif introuvable.")
        return False

    if not os.path.exists(chemin_fichier):
        print(f"Fichier '{chemin_fichier}' introuvable.")
        return False

    try:
        with open(chemin_fichier, "rb") as f:
            contenu = f.read()
    except Exception as e:
        print(f"Erreur de lecture du fichier: {e}")
        return False

    if not est_image(contenu):
        print("Le fichier n'est pas reconnu comme image PNG/JPEG/GIF/WebP.")
        return False

    # Stockage mémoire + chemin (utile pour recharger plus tard)
    sportif.photo_profil = contenu
    setattr(sportif, "photo_profil_path", chemin_fichier)  # attribut dynamique
    print(f"Photo de profil ajoutée pour {sportif.prenom} {sportif.nom}.")
    return True


def ecrire_photo_profil_sur_disque(sportif_id: int, chemin_sortie: str) -> bool:
    """
    Écrit l'image stockée en mémoire vers un fichier (preuve que les octets sont exploitables).
    """
    sportif = sportifs.get(sportif_id)
    if not sportif or not getattr(sportif, "photo_profil", None):
        print("Aucune photo en mémoire à écrire.")
        return False

    dossier = os.path.dirname(chemin_sortie)
    if dossier and not os.path.isdir(dossier):
        os.makedirs(dossier, exist_ok=True)

    try:
        with open(chemin_sortie, "wb") as f:
            f.write(sportif.photo_profil)
        print(f"Image écrite dans: {chemin_sortie}")
        return True
    except Exception as e:
        print(f"Erreur d'écriture: {e}")
        return False


# =========================
# Tests
# =========================

def test_photo_existe():
    """Test avec une vraie image locale existante + réécriture pour valider l'utilisabilité."""
    print("— Test : fichier existant —")
    chemin = "uploads/test_profil.png"   # mets une vraie image (png/jpg/gif/webp)
    sortie = "uploads/_out_profil.png"   # fichier de sortie pour valider

    # Reset propre
    sportifs[1].photo_profil = None
    if hasattr(sportifs[1], "photo_profil_path"):
        delattr(sportifs[1], "photo_profil_path")

    ok = ajouter_photo_profil(1, chemin)
    ok_write = ecrire_photo_profil_sur_disque(1, sortie) if ok else False

    if ok and sportifs[1].photo_profil and ok_write and os.path.exists(sortie):
        print("TEST RÉUSSI : la photo a été chargée et réécrite correctement (utilisable).\n")
    else:
        print("TEST ÉCHOUÉ : chargement ou écriture de l'image défaillant.\n")


def test_photo_absente():
    """Test avec un fichier inexistant (doit échouer sans modifier l'état)."""
    print("— Test : fichier non existant —")
    chemin = "fichier_inexistant.png"

    # Reset propre
    sportifs[1].photo_profil = None
    if hasattr(sportifs[1], "photo_profil_path"):
        delattr(sportifs[1], "photo_profil_path")

    ok = ajouter_photo_profil(1, chemin)
    if not ok and sportifs[1].photo_profil is None and not hasattr(sportifs[1], "photo_profil_path"):
        print("TEST RÉUSSI : fichier manquant détecté, aucune photo enregistrée.\n")
    else:
        print("TEST ÉCHOUÉ : état incorrect après tentative avec fichier absent.\n")


if __name__ == "__main__":
    test_photo_existe()
    test_photo_absente()
