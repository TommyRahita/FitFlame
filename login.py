import tkinter as tk
from tkinter import messagebox

# Liste pour stocker les couples (prénom, mot de passe)
database = []



# Fonction pour gérer la connexion
def se_connecter():
    prenom = entry_prenom.get()  # Récupérer le prénom
    mot_de_passe = entry_mdp.get()  # Récupérer le mot de passe

    # Vérification si le prénom existe dans la base de données
    utilisateur_trouve = False
    for couple in database:
        if couple[0] == prenom:
            utilisateur_trouve = True
            if couple[1] == mot_de_passe:
                # Mot de passe correct
                print(f"Bonjour {prenom}")
            else:
                # Mot de passe incorrect
                print(f"mdp incorrect")
            break
    
    if not utilisateur_trouve:
        # Si le prénom n'existe pas, ajouter à la base de données
        database.append((prenom, mot_de_passe))
        print(f"Bonjour {prenom}")





# Fonction pour afficher un message d'erreur pour mot de passe incorrect
def afficher_mot_de_passe_incorrect():
    messagebox.showerror("Erreur", "Mot de passe incorrect.")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Page de Login")

# Paramétrage de la taille de la fenêtre
root.geometry("400x300")

# Ajouter un label "Login" en haut de la fenêtre
label_login = tk.Label(root, text="Login", font=("Arial", 20))
label_login.pack(pady=20)

# Zone de texte pour le prénom
label_prenom = tk.Label(root, text="Prénom:")
label_prenom.pack()
entry_prenom = tk.Entry(root, font=("Arial", 14))
entry_prenom.pack(pady=5)

# Zone de texte pour le mot de passe
label_mdp = tk.Label(root, text="Mot de passe:")
label_mdp.pack()
entry_mdp = tk.Entry(root, show="*", font=("Arial", 14))
entry_mdp.pack(pady=5)

# Bouton "Se connecter"
button_connexion = tk.Button(root, text="Se connecter", font=("Arial", 14), command=se_connecter)
button_connexion.pack(pady=20)

# Lancer la boucle principale de l'interface
root.mainloop()