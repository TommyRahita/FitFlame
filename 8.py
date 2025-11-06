# fichier : galerie_photos.py
from __future__ import annotations
from typing import Dict, Iterable
from class_sportif import Sportif
import os

# -------------------------------------------------------------------
# Core (API galerie)
# -------------------------------------------------------------------

def _get_sportif(sportifs: Dict[int, Sportif], sportif_id: int) -> Sportif | None:
    """Récupère le sportif sans créer d'état global."""
    return sportifs.get(sportif_id)

def _est_image(contenu: bytes) -> bool:
    """Détection minimaliste PNG/JPEG via signatures magiques."""
    return contenu.startswith(b"\x89PNG") or contenu.startswith(b"\xFF\xD8")

def ajouter_photo_galerie(
    sportifs: Dict[int, Sportif],
    sportif_id: int,
    chemin_fichier: str,
    nom_cle: str | None = None,
) -> bool:
    """
    Ajoute une image dans la galerie du sportif.
    - sportifs: dict[int, Sportif] fourni par l'appelant (pas d'état global ici)
    - sportif_id: identifiant du sportif
    - chemin_fichier: chemin local de l'image
    - nom_cle: clé sous laquelle stocker l'image (par défaut, nom du fichier)
    Retourne True si succès.
    """
    sp = _get_sportif(sportifs, sportif_id)
    if not sp:
        print("❌ Sportif introuvable.")
        return False

    if not os.path.exists(chemin_fichier):
        print(f"❌ Fichier '{chemin_fichier}' introuvable.")
        return False

    with open(chemin_fichier, "rb") as f:
        contenu = f.read()

    if not _est_image(contenu):
        print("❌ Le fichier n'est pas reconnu comme image PNG/JPEG.")
        return False

    key = nom_cle or os.path.basename(chemin_fichier)
    sp.galerie_photos[key] = contenu
    print(f"✅ Image ajoutée dans la galerie sous la clé '{key}'.")
    return True

def supprimer_photo_galerie(
    sportifs: Dict[int, Sportif],
    sportif_id: int,
    nom_cle: str,
) -> bool:
    """
    Supprime une image de la galerie du sportif par sa clé.
    Retourne True si une image a été supprimée.
    """
    sp = _get_sportif(sportifs, sportif_id)
    if not sp:
        print("❌ Sportif introuvable.")
        return False

    existed = sp.galerie_photos.pop(nom_cle, None) is not None
    if existed:
        print(f"🗑️  Image '{nom_cle}' supprimée de la galerie.")
    else:
        print(f"ℹ️  Aucune image sous la clé '{nom_cle}'.")
    return existed

def lister_clefs_galerie(sportifs: Dict[int, Sportif], sportif_id: int) -> list[str]:
    """Renvoie la liste des clés (noms) des images de la galerie."""
    sp = _get_sportif(sportifs, sportif_id)
    if not sp:
        print("❌ Sportif introuvable.")
        return []
    return list(sp.galerie_photos.keys())

def compter_galerie(sportifs: Dict[int, Sportif], sportif_id: int) -> int:
    """Renvoie le nombre d'images dans la galerie du sportif."""
    sp = _get_sportif(sportifs, sportif_id)
    if not sp:
        print("❌ Sportif introuvable.")
        return 0
    return len(sp.galerie_photos)

def vider_galerie(sportifs: Dict[int, Sportif], sportif_id: int) -> int:
    """Supprime toutes les images de la galerie et renvoie combien ont été retirées."""
    sp = _get_sportif(sportifs, sportif_id)
    if not sp:
        print("❌ Sportif introuvable.")
        return 0
    n = len(sp.galerie_photos)
    sp.galerie_photos.clear()
    print(f"🧹 Galerie vidée ({n} image(s) supprimée(s)).")
    return n

def ajouter_plusieurs(
    sportifs: Dict[int, Sportif],
    sportif_id: int,
    chemins: Iterable[str],
) -> int:
    """
    Ajoute plusieurs fichiers à la galerie (ignore ceux qui échouent).
    Renvoie le nombre d'images ajoutées.
    """
    added = 0
    for p in chemins:
        if ajouter_photo_galerie(sportifs, sportif_id, p):
            added += 1
    return added

# -------------------------------------------------------------------
# Tests (format test / main)
# -------------------------------------------------------------------

# ⚠️ Dictionnaire local pour les tests (évite NameError)
sportifs: Dict[int, Sportif] = {
    1: Sportif(prenom="Alice", nom="Martin", age=24),
}

def test_galerie_existe():
    """Test avec une vraie image locale existante."""
    print("— Test : ajout d'image existante dans la galerie —")
    chemin = "uploads/test_galerie.png"  # mets une vraie image PNG/JPG ici

    # Petit rappel utile
    if not os.path.isdir("uploads"):
        print("ℹ️  Dossier 'uploads' introuvable (pense à le créer et y mettre l'image).")

    # Réinitialisation de la galerie pour un test propre
    vider_galerie(sportifs, 1)

    ok = ajouter_photo_galerie(sportifs, 1, chemin, "ma_photo")

    if ok and "ma_photo" in lister_clefs_galerie(sportifs, 1):
        print("🎯 TEST RÉUSSI : l'image a bien été ajoutée à la galerie.\n")
    else:
        print("❌ TEST ÉCHOUÉ : l'image n'a pas été ajoutée correctement.\n")

def test_galerie_absente():
    """Test avec un fichier inexistant (doit échouer sans modifier la galerie)."""
    print("— Test : ajout d'un fichier inexistant —")
    chemin = "fichier_inexistant.png"

    # Réinitialisation de la galerie
    vider_galerie(sportifs, 1)

    ok = ajouter_photo_galerie(sportifs, 1, chemin, "photo_absente")

    if not ok and len(lister_clefs_galerie(sportifs, 1)) == 0:
        print("🎯 TEST RÉUSSI : fichier manquant détecté, galerie inchangée.\n")
    else:
        print("❌ TEST ÉCHOUÉ : la galerie a été modifiée alors que le fichier est manquant.\n")

if __name__ == "__main__":
    test_galerie_existe()
    test_galerie_absente()
