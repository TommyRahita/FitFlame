# fichier : galerie_photos.py
from __future__ import annotations
from typing import Dict, Iterable
from class_sportif import Sportif
import os

# -------------------------------------------------------------------
# Core (API galerie)
# -------------------------------------------------------------------

def _get_sportif(sportifs: Dict[int, Sportif], sportif_id: int) -> Sportif | None:
    return sportifs.get(sportif_id)

def _ensure_galerie(sp: Sportif) -> None:
    """Assure l'existence de sp.galerie_photos (et du mapping des chemins)."""
    if not hasattr(sp, "galerie_photos") or sp.galerie_photos is None:
        sp.galerie_photos = {}
    if not hasattr(sp, "galerie_paths") or getattr(sp, "galerie_paths") is None:
        # clé -> chemin d'origine (optionnel)
        setattr(sp, "galerie_paths", {})

def _est_image(contenu: bytes) -> bool:
    """Détection via signatures magiques: PNG/JPEG/GIF/WebP."""
    if len(contenu) < 12:
        return False
    if contenu.startswith(b"\x89PNG\r\n\x1a\n"):  # PNG
        return True
    if contenu[:2] == b"\xFF\xD8":               # JPEG
        return True
    if contenu.startswith(b"GIF87a") or contenu.startswith(b"GIF89a"):  # GIF
        return True
    if contenu[:4] == b"RIFF" and contenu[8:12] == b"WEBP":  # WebP
        return True
    return False

def ajouter_photo_galerie(
    sportifs: Dict[int, Sportif],
    sportif_id: int,
    chemin_fichier: str,
    nom_cle: str | None = None,
) -> bool:
    sp = _get_sportif(sportifs, sportif_id)
    if not sp:
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

    if not _est_image(contenu):
        print("Le fichier n'est pas reconnu comme image PNG/JPEG/GIF/WebP.")
        return False

    _ensure_galerie(sp)
    key = nom_cle or os.path.basename(chemin_fichier)
    sp.galerie_photos[key] = contenu
    sp.galerie_paths[key] = chemin_fichier  # on mémorise le chemin d'origine
    print(f"Image ajoutée dans la galerie sous la clé '{key}'.")
    return True

def ecrire_image_galerie_sur_disque(
    sportifs: Dict[int, Sportif],
    sportif_id: int,
    nom_cle: str,
    chemin_sortie: str,
) -> bool:
    """Réécrit une image de la galerie sur disque (preuve de son exploitabilité)."""
    sp = _get_sportif(sportifs, sportif_id)
    if not sp:
        print("Sportif introuvable.")
        return False
    _ensure_galerie(sp)

    contenu = sp.galerie_photos.get(nom_cle)
    if not contenu:
        print(f"Aucune image sous la clé '{nom_cle}'.")
        return False

    dossier = os.path.dirname(chemin_sortie)
    if dossier and not os.path.isdir(dossier):
        os.makedirs(dossier, exist_ok=True)

    try:
        with open(chemin_sortie, "wb") as f:
            f.write(contenu)
        print(f"Image '{nom_cle}' écrite dans: {chemin_sortie}")
        return True
    except Exception as e:
        print(f"Erreur d'écriture: {e}")
        return False

def supprimer_photo_galerie(
    sportifs: Dict[int, Sportif],
    sportif_id: int,
    nom_cle: str,
) -> bool:
    sp = _get_sportif(sportifs, sportif_id)
    if not sp:
        print("Sportif introuvable.")
        return False
    _ensure_galerie(sp)

    existed = sp.galerie_photos.pop(nom_cle, None) is not None
    # on nettoie aussi le chemin mémorisé
    if hasattr(sp, "galerie_paths"):
        sp.galerie_paths.pop(nom_cle, None)

    if existed:
        print(f"Image '{nom_cle}' supprimée de la galerie.")
    else:
        print(f"ℹ Aucune image sous la clé '{nom_cle}'.")
    return existed

def lister_clefs_galerie(sportifs: Dict[int, Sportif], sportif_id: int) -> list[str]:
    sp = _get_sportif(sportifs, sportif_id)
    if not sp:
        print("Sportif introuvable.")
        return []
    _ensure_galerie(sp)
    return list(sp.galerie_photos.keys())

def compter_galerie(sportifs: Dict[int, Sportif], sportif_id: int) -> int:
    sp = _get_sportif(sportifs, sportif_id)
    if not sp:
        print("Sportif introuvable.")
        return 0
    _ensure_galerie(sp)
    return len(sp.galerie_photos)

def vider_galerie(sportifs: Dict[int, Sportif], sportif_id: int) -> int:
    sp = _get_sportif(sportifs, sportif_id)
    if not sp:
        print("Sportif introuvable.")
        return 0
    _ensure_galerie(sp)
    n = len(sp.galerie_photos)
    sp.galerie_photos.clear()
    if hasattr(sp, "galerie_paths"):
        sp.galerie_paths.clear()
    print(f"Galerie vidée ({n} image(s) supprimée(s)).")
    return n

def ajouter_plusieurs(
    sportifs: Dict[int, Sportif],
    sportif_id: int,
    chemins: Iterable[str],
) -> int:
    added = 0
    for p in chemins:
        if ajouter_photo_galerie(sportifs, sportif_id, p):
            added += 1
    return added

# -------------------------------------------------------------------
# Tests (format test / main)
# -------------------------------------------------------------------

sportifs: Dict[int, Sportif] = {
    1: Sportif(prenom="Alice", nom="Martin", age=24),
}

def test_galerie_existe():
    """Test avec une vraie image locale existante + réécriture sur disque."""
    print("— Test : ajout d'image existante dans la galerie —")
    chemin = "uploads/test_galerie.png"       # mets une vraie image
    cle    = "ma_photo"
    sortie = "uploads/_out_galerie.png"       # preuve d'exploitabilité

    if not os.path.isdir("uploads"):
        print("Dossier 'uploads' introuvable (pense à le créer et y mettre l'image).")

    vider_galerie(sportifs, 1)

    ok_add = ajouter_photo_galerie(sportifs, 1, chemin, cle)
    ok_out = ecrire_image_galerie_sur_disque(sportifs, 1, cle, sortie) if ok_add else False

    if ok_add and cle in lister_clefs_galerie(sportifs, 1) and ok_out and os.path.exists(sortie):
        print("TEST RÉUSSI : image ajoutée et réécrite correctement (utilisable).\n")
    else:
        print("TEST ÉCHOUÉ : ajout ou écriture défaillant.\n")

def test_galerie_absente():
    """Test avec un fichier inexistant (doit échouer sans modifier la galerie)."""
    print("— Test : ajout d'un fichier inexistant —")
    chemin = "fichier_inexistant.png"
    cle = "photo_absente"

    vider_galerie(sportifs, 1)

    ok = ajouter_photo_galerie(sportifs, 1, chemin, cle)

    if not ok and len(lister_clefs_galerie(sportifs, 1)) == 0:
        print("TEST RÉUSSI : fichier manquant détecté, galerie inchangée.\n")
    else:
        print("TEST ÉCHOUÉ : la galerie a été modifiée alors que le fichier est manquant.\n")

if __name__ == "__main__":
    test_galerie_existe()
    test_galerie_absente()
