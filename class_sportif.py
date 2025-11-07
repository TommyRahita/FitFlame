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
