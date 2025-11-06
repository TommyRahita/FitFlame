# Dictionnaires simulant une base de données
utilisateurs = {
    1: {"nom": "Alice", "photo": None},
    2: {"nom": "Bob", "photo": None},
}

images = {}  # stockage en mémoire des fichiers binaires


def est_image(fichier_bytes: bytes) -> bool:
    """Vérifie si le contenu correspond à une image PNG ou JPEG."""
    return (
        fichier_bytes.startswith(b"\x89PNG") or  # PNG
        fichier_bytes.startswith(b"\xFF\xD8")    # JPEG
    )


def ajouter_photo_profil(id_utilisateur: int, fichier_bytes: bytes) -> bool:
    """Ajoute une photo de profil si l'utilisateur existe et que le fichier est une image."""
    if id_utilisateur not in utilisateurs:
        print("❌ Utilisateur inexistant.")
        return False

    if not est_image(fichier_bytes):
        print("❌ Le fichier n'est pas une image PNG ou JPEG valide.")
        return False

    images[id_utilisateur] = fichier_bytes
    utilisateurs[id_utilisateur]["photo"] = f"image_{id_utilisateur}"
    print("✅ Photo ajoutée avec succès pour l'utilisateur", utilisateurs[id_utilisateur]["nom"])
    return True


# ---------------------------
# Tests avec fichiers réels
# ---------------------------
def test_fichier_existant():
    """Test avec un fichier image existant."""
    chemin = "uploads/test_profil.png"  # mets ici le nom de ton fichier image réel (dans le même dossier)
    try:
        with open(chemin, "rb") as f:
            contenu = f.read()
    except FileNotFoundError:
        print(f"❌ Fichier '{chemin}' introuvable pour le test.")
        return

    ok = ajouter_photo_profil(1, contenu)
    if ok and utilisateurs[1]["photo"] == "image_1":
        print("🎯 TEST RÉUSSI : image existante bien ajoutée.\n")
    else:
        print("❌ TEST ÉCHOUÉ avec image existante.\n")


def test_fichier_non_existant():
    """Test avec un fichier qui n'existe pas."""
    chemin = "fichier_inexistant.png"  # ce fichier ne doit pas exister
    try:
        with open(chemin, "rb") as f:
            contenu = f.read()
    except FileNotFoundError:
        print(f"✅ TEST RÉUSSI : le fichier '{chemin}' est bien détecté comme manquant.\n")
        return

    # Si le fichier existe par erreur :
    print(f"⚠️ Le fichier '{chemin}' existe, le test est invalide.\n")


if __name__ == "__main__":
    test_fichier_existant()
    test_fichier_non_existant()
