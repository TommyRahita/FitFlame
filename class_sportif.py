import sys
import os
chemin_actuel = os.getcwd()
sys.path.append(chemin_actuel)

from dataclasses import dataclass, field
from typing import Optional, Tuple

@dataclass
class Sportif:
    nom: str = None
    prenom: str = None
    sexe: str = None
    age: int = None
    nationalite: str = None
    localisation: list[float, float] = None
    distance_rencontre: int = None
    niveau_sports: dict = None
    attentes: str = None
    genre_recherche: str = None
    min_age_recherchee: int = None
    max_age_recherchee: int = None
    nb_swipes_restants: int = None
    photo_profil: Optional[str] = None
    galerie_photos: list[str] = field(default_factory=list)