from dataclasses import dataclass, field
from typing import Optional, Tuple

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
    attentes: list[str] = field(default_factory=list)
    genre_recherche: Optional[str] = None
    min_age_recherchee: Optional[int] = None
    max_age_recherchee: Optional[int] = None

    photo_profil: Optional[str] = None                  # ex: "uploads/julien.png"

    nb_swipes_restants: Optional[int] = 25

