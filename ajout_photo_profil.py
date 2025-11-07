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

# --- MÉTHODE DEMANDÉE ---
def ajouter_photo_dans_json(self, chemin_fichier: str, json_path: str = "data.json") -> bool:
        """Ajoute/met à jour photo_profil dans data.json pour (prenom, nom)."""
        if not self.prenom or not self.nom:
            print("❌ Impossible d’ajouter la photo : prénom ou nom manquant.")
            return False
        if not os.path.isfile(json_path):
            print(f"❌ Fichier JSON '{json_path}' introuvable.")
            return False

        chemin_fichier = chemin_fichier.replace("\\", "/")

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print("❌ Erreur : le fichier JSON est vide ou invalide.")
            return False

        if not isinstance(data, list):
            print("❌ Format du JSON invalide (liste d'objets attendue).")
            return False

        trouve = False
        for entry in data:
            if entry.get("prenom") == self.prenom and entry.get("nom") == self.nom:
                entry["photo_profil"] = chemin_fichier
                trouve = True
                break

        if not trouve:
            print(f"⚠️ Sportif {self.prenom} {self.nom} introuvable dans le JSON.")
            return False

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        self.photo_profil = chemin_fichier
        print(f"✅ Photo ajoutée pour {self.prenom} {self.nom} dans '{json_path}'.")
        return True
    
def ajouter_photo_galerie_dans_json(
        self,
        chemin_fichier: str,
        json_path: str = "data.json",
        unique: bool = True,
    ) -> bool:
        """
        Ajoute un chemin d'image à la galerie du sportif dans le JSON
        (clé 'galerie_photos' = liste de str). Met aussi à jour self.galerie_photos.
        - unique=True empêche les doublons exacts.
        """
        if not self.prenom or not self.nom:
            print("❌ Impossible d’ajouter : prénom/nom manquant.")
            return False
        if not os.path.isfile(json_path):
            print(f"❌ Fichier JSON '{json_path}' introuvable.")
            return False

        chemin_norm = chemin_fichier.replace("\\", "/")

        # charger
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print("❌ JSON invalide.")
            return False
        if not isinstance(data, list):
            print("❌ Format JSON attendu: liste d'objets.")
            return False

        # trouver l'entrée
        entree = None
        for e in data:
            if e.get("prenom") == self.prenom and e.get("nom") == self.nom:
                entree = e
                break
        if entree is None:
            print(f"⚠️ Sportif {self.prenom} {self.nom} introuvable dans le JSON.")
            return False

        # s'assurer que la clé existe et est une liste
        gal = entree.get("galerie_photos")
        if gal is None or not isinstance(gal, list):
            gal = []
            entree["galerie_photos"] = gal

        # éviter les doublons si demandé
        if unique and chemin_norm in gal:
            print("ℹ️ Chemin déjà présent dans la galerie (aucune modification).")
        else:
            gal.append(chemin_norm)

        # écrire
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # maj de l'objet courant
        if unique and chemin_norm in self.galerie_photos:
            pass
        else:
            self.galerie_photos.append(chemin_norm)

        print(f"✅ Photo de galerie ajoutée pour {self.prenom} {self.nom}.")
        return True


def supprimer_photo_galerie_dans_json(
        self,
        chemin_ou_nom: str,
        json_path: str = "data.json",
    ) -> bool:
        """
        Supprime une entrée de la galerie du sportif dans le JSON ET dans l'objet.
        - Supprime par comparaison de chaîne exacte après normalisation.
        - Si 'chemin_ou_nom' ne contient pas de '/', on tente aussi une suppression
          par correspondance de nom de fichier (basename).
        """
        if not self.prenom or not self.nom:
            print("❌ Impossible de supprimer : prénom/nom manquant.")
            return False
        if not os.path.isfile(json_path):
            print(f"❌ Fichier JSON '{json_path}' introuvable.")
            return False

        cible = chemin_ou_nom.replace("\\", "/")
        cible_base = os.path.basename(cible)

        # charger
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print("❌ JSON invalide.")
            return False
        if not isinstance(data, list):
            print("❌ Format JSON attendu: liste d'objets.")
            return False

        # trouver l'entrée
        entree = None
        for e in data:
            if e.get("prenom") == self.prenom and e.get("nom") == self.nom:
                entree = e
                break
        if entree is None:
            print(f"⚠️ Sportif {self.prenom} {self.nom} introuvable dans le JSON.")
            return False

        gal = entree.get("galerie_photos")
        if not isinstance(gal, list):
            print("ℹ️ Pas de galerie à nettoyer.")
            gal = []
            entree["galerie_photos"] = gal

        # stratégie de suppression:
        # 1) essai exact
        removed = False
        if cible in gal:
            gal.remove(cible)
            removed = True
        else:
            # 2) essai par basename si l'utilisateur a donné juste un nom
            #    ou si des chemins relatifs/absolus ne matchent pas exactement
            for item in list(gal):
                if os.path.basename(str(item)) == cible_base:
                    gal.remove(item)
                    removed = True
                    break

        if not removed:
            print("ℹ️ Élément non trouvé dans la galerie (aucune suppression).")
            return False

        # écrire
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # maj objet courant (mêmes règles)
        if cible in self.galerie_photos:
            self.galerie_photos.remove(cible)
        else:
            for item in list(self.galerie_photos):
                if os.path.basename(item) == cible_base:
                    self.galerie_photos.remove(item)
                    break

        print(f"🗑️ Photo de galerie supprimée pour {self.prenom} {self.nom}.")
        return True

if __name__ == "__main__":
    test_photo_existe()
    test_photo_absente()
