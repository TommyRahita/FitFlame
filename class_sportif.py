from dataclasses import dataclass, field
from typing import Optional, Tuple, List
import json, os

@dataclass
class Sportif:
    nom: Optional[str] = None
    prenom: Optional[str] = None
    sexe: Optional[str] = None
    age: Optional[int] = None
    nationalite: Optional[str] = None
    localisation: Optional[Tuple[float, float]] = None  # (lat, lon)
    distance_rencontre: Optional[int] = None
    niveau_sports: dict = field(default_factory=dict)
    attentes: List[str] = field(default_factory=list)
    genre_recherche: Optional[str] = None
    min_age_recherchee: Optional[int] = None
    max_age_recherchee: Optional[int] = None

    # Photos stockées en chemins (strings)
    photo_profil: Optional[str] = None                  # ex: "uploads/julien.png"
    galerie_photos: List[str] = field(default_factory=list)

    nb_swipes_restants: Optional[int] = 25

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

