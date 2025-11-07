# fichier : fitflame_match_swipe.py
import json
import os
import random
import time
from datetime import date, datetime, timedelta
from notifypy import Notify
from class_sportif import Sportif  # ta classe existante


# ----------------------------
# CONFIGURATION
# ----------------------------
SWIPE_LIMIT = 25
DATA_PATH = "data.json"


# ----------------------------
# CHARGEMENT DES SPORTIFS
# ----------------------------
def charger_sportifs(json_path: str = DATA_PATH) -> dict[int, Sportif]:
    """Charge les sportifs depuis le fichier JSON et retourne un dictionnaire {id: Sportif}."""
    if not os.path.isfile(json_path):
        raise FileNotFoundError(f"❌ Fichier JSON '{json_path}' introuvable.")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    sportifs = {}
    for i, entry in enumerate(data, start=1):
        sportifs[i] = Sportif(
            nom=entry.get("nom"),
            prenom=entry.get("prenom"),
            sexe=entry.get("sexe"),
            age=entry.get("age"),
            nationalite=entry.get("nationalite"),
            distance_rencontre=entry.get("distance_rencontre"),
            niveau_sports=entry.get("niveau_sports", {}),
            attentes=entry.get("attentes", []),
            genre_recherche=entry.get("genre_recherche"),
            min_age_recherchee=entry.get("min_age_recherchee"),
            max_age_recherchee=entry.get("max_age_recherchee"),
            photo_profil=entry.get("photo_profil"),
        )
        sportifs[i].swipes_effectues = 0
        sportifs[i].derniere_date_de_swipe = date.today() - timedelta(days=1)
    return sportifs


# ----------------------------
# NOTIFICATIONS
# ----------------------------
def envoyer_notification_match(nom_du_match: str, sportif_cible: Sportif):
    """Envoie une notification de bureau à un sportif."""
    notification = Notify()
    notification.title = "🔥 C'est un Match !"
    notification.message = f"Vous avez un Match avec {nom_du_match} !"
    notification.send()
    print(f"[Notification envoyée] à {sportif_cible.prenom} pour {nom_du_match}.")


# ----------------------------
# GESTION DES SWIPES
# ----------------------------
def verifier_et_reinitialiser_compteur(sportif: Sportif):
    """Réinitialise le compteur de swipe si un nouveau jour commence."""
    if date.today() > getattr(sportif, "derniere_date_de_swipe", date.today()):
        sportif.swipes_effectues = 0
        sportif.derniere_date_de_swipe = date.today()
        print(f"🔄 Compteur réinitialisé pour {sportif.prenom}.")


def tenter_swipe(sportif: Sportif, cible: Sportif) -> bool:
    """Vérifie si un sportif peut swiper et incrémente son compteur."""
    verifier_et_reinitialiser_compteur(sportif)

    if getattr(sportif, "swipes_effectues", 0) < SWIPE_LIMIT:
        sportif.swipes_effectues += 1
        print(f"✅ {sportif.prenom} swipe sur {cible.prenom} ({sportif.swipes_effectues}/{SWIPE_LIMIT})")
        return True
    else:
        print(f"❌ {sportif.prenom} a atteint la limite quotidienne de {SWIPE_LIMIT} swipes.")
        return False


# ----------------------------
# LOGIQUE DE MATCH
# ----------------------------
def verifier_et_declencher_match(sportif_a: Sportif, sportif_b: Sportif) -> bool:
    """Vérifie s’il y a match entre deux sportifs et envoie une notification."""
    print(f"\n--- Vérification de match entre {sportif_a.prenom} et {sportif_b.prenom} ---")

    # Simulation d’un match (tu remplaceras par ta logique réelle)
    match_trouve = random.choice([True, False])

    if match_trouve:
        print("🎯 Match trouvé ! Envoi des notifications...")
        envoyer_notification_match(sportif_b.prenom, sportif_a)
        envoyer_notification_match(sportif_a.prenom, sportif_b)
        return True
    else:
        print("😞 Pas de match pour l’instant.")
        return False


# ----------------------------
# EXÉCUTION DE DÉMONSTRATION
# ----------------------------
if __name__ == "__main__":
    sportifs = charger_sportifs()

    # Exemple : Julien (id=1) swipe sur Amélie (id=2)
    s1 = sportifs[1]
    s2 = sportifs[2]

    print(f"\nSimulation : {s1.prenom} ({s1.nom}) swipe sur {s2.prenom} ({s2.nom})")
    tenter_swipe(s1, s2)

    # Vérifie un match potentiel
    verifier_et_declencher_match(s1, s2)
