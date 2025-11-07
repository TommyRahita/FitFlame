import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

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
                afficher_bienvenue(prenom)
            else:
                # Mot de passe incorrect
                afficher_mot_de_passe_incorrect()
            break
    
    if not utilisateur_trouve:
        # Si le prénom n'existe pas, ajouter à la base de données
        database.append((prenom, mot_de_passe))
        afficher_bienvenue(prenom)


# Fonction pour afficher la fenêtre de bienvenue
def afficher_bienvenue(prenom):
    root.withdraw()  # Cacher la fenêtre de login
    nouvelle_fenetre = tk.Toplevel()  # Créer une nouvelle fenêtre
    nouvelle_fenetre.title("Renseignez vos infos :")
    nouvelle_fenetre.geometry("720x370")

    # Label de bienvenue avec le prénom
    bienvenue_label = tk.Label(nouvelle_fenetre, text=f"Bienvenue {prenom} !", font=("Arial", 16))
    bienvenue_label.pack(padx=20, pady=20)

    NOM = tk.StringVar()
    PRENOM = tk.StringVar()
    SEXE = tk.StringVar()
    age = tk.IntVar()

    NATIONALITE = tk.StringVar()
    localisation_x = tk.IntVar()
    localisation_y = tk.IntVar()
    DISTANCE_RENCONTRE = tk.IntVar()
    SPORT1 = tk.StringVar()
    NIVEAU_SPORT1 = tk.StringVar()
    SPORT2 = tk.StringVar()
    NIVEAU_SPORT2 = tk.StringVar()
    SPORT3 = tk.StringVar()
    NIVEAU_SPORT3 = tk.StringVar()
    ATTENTE = tk.StringVar()
    GENRE_RECHERCHE = tk.StringVar()
    MIN_AGE_RECHERCHE = tk.StringVar()
    MAX_AGE_RECHERCHE = tk.StringVar()



    label_prenom = tk.Label(nouvelle_fenetre, text="Prénom:")
    label_prenom.place(x=50, y=50)
    entry_prenom = tk.Entry(nouvelle_fenetre, textvariable=PRENOM, font=("Arial", 8))
    entry_prenom.place(x=50, y=70)

    label_nom = tk.Label(nouvelle_fenetre, text="Nom:")
    label_nom.place(x=50, y=90)
    entry_nom = tk.Entry(nouvelle_fenetre, textvariable=NOM, font=("Arial", 8))
    entry_nom.place(x=50, y=110)

    label_sexe = tk.Label(nouvelle_fenetre, text="Sexe:")
    label_sexe.place(x=50, y=130)
    entry_sexe = tk.Entry(nouvelle_fenetre, textvariable=SEXE, font=("Arial", 8))
    entry_sexe.place(x=50, y=150)

    label_age = tk.Label(nouvelle_fenetre, text="Age:")
    label_age.place(x=50, y=170)
    entry_age = tk.Entry(nouvelle_fenetre, textvariable=age, font=("Arial", 8))
    entry_age.place(x=50, y=190)

    label_nat = tk.Label(nouvelle_fenetre, text="Nationalité:")
    label_nat.place(x=50, y=210)
    entry_nat = tk.Entry(nouvelle_fenetre, textvariable=NATIONALITE, font=("Arial", 8))
    entry_nat.place(x=50, y=230)

    # localisation
    label_localisation_X = tk.Label(nouvelle_fenetre, text="Localisation X:")
    label_localisation_X.place(x=50, y=250)
    entry_localisation_X = tk.Entry(nouvelle_fenetre, textvariable=localisation_x, font=("Arial", 8), width=10)
    entry_localisation_X.place(x=50, y=270)

    label_localisation_Y = tk.Label(nouvelle_fenetre, text="Localisation Y:")
    label_localisation_Y.place(x=150, y=250)
    entry_localisation_Y = tk.Entry(nouvelle_fenetre, textvariable=localisation_y, font=("Arial", 8), width=10)
    entry_localisation_Y.place(x=150, y=270)


    label_distance_rencontre = tk.Label(nouvelle_fenetre, text="distance_rencontre:")
    label_distance_rencontre.place(x=50, y=290)
    entry_distance_rencontre = tk.Entry(nouvelle_fenetre, textvariable=DISTANCE_RENCONTRE, font=("Arial", 8))
    entry_distance_rencontre.place(x=50, y=310)

    # Variable pour stocker le sport sélectionné
    ATTENTES = ["Amitié", "Amour", "Entraînements", "Ne sais pas"]
    SPORTS = ["Football", "Basketball", "Tennis", "Natation", "Rugby", "Cyclisme"]
    NIVEAU = ["Débutant", "Intermédiaire", "Avancé", "Pro"]
    SEXES = ["Femme", "Homme", "Tous"]


    label_attentes = tk.Label(nouvelle_fenetre, text="Tu cherches:")
    label_attentes.place(x=250, y=50)
    entry_attentes = ttk.Combobox(nouvelle_fenetre, textvariable=ATTENTE, values=ATTENTES, state="normal")
    entry_attentes.place(x=250, y=70)



    # Variable pour stocker le sport sélectionné

    label_sport1 = tk.Label(nouvelle_fenetre, text="Choisis ton sport préféré:")
    label_sport1.place(x=250, y=90)
    entry_sport1 = ttk.Combobox(nouvelle_fenetre, textvariable=SPORT1, values=SPORTS, state="normal")
    entry_sport1.place(x=250, y=110)

    label_niveau2 = tk.Label(nouvelle_fenetre, text="Choisis ton niveau:")
    label_niveau2.place(x=250, y=130)
    entry_niveau2 = ttk.Combobox(nouvelle_fenetre, textvariable=NIVEAU_SPORT1, values=NIVEAU, state="normal")
    entry_niveau2.place(x=250, y=150)


    label_sport2 = tk.Label(nouvelle_fenetre, text="Choisis ton sport préféré:")
    label_sport2.place(x=400, y=90)
    entry_sport2 = ttk.Combobox(nouvelle_fenetre, textvariable=SPORT2, values=SPORTS, state="normal")
    entry_sport2.place(x=400, y=110)

    label_niveau2 = tk.Label(nouvelle_fenetre, text="Choisis ton niveau:")
    label_niveau2.place(x=400, y=130)
    entry_niveau2 = ttk.Combobox(nouvelle_fenetre, textvariable=NIVEAU_SPORT2, values=NIVEAU, state="normal")
    entry_niveau2.place(x=400, y=150)


    label_sport3 = tk.Label(nouvelle_fenetre, text="Choisis ton sport préféré:")
    label_sport3.place(x=550, y=90)
    entry_sport3 = ttk.Combobox(nouvelle_fenetre, textvariable=SPORT3, values=SPORTS, state="normal")
    entry_sport3.place(x=550, y=110)

    label_niveau3 = tk.Label(nouvelle_fenetre, text="Choisis ton niveau:")
    label_niveau3.place(x=550, y=130)
    entry_niveau3 = ttk.Combobox(nouvelle_fenetre, textvariable=NIVEAU_SPORT3, values=NIVEAU, state="normal")
    entry_niveau3.place(x=550, y=150)

    label_attentes_sexe = tk.Label(nouvelle_fenetre, text="Tu cherches:")
    label_attentes_sexe.place(x=250, y=170)
    entry_attentes_sexe = ttk.Combobox(nouvelle_fenetre, textvariable=GENRE_RECHERCHE, values=SEXES, state="readonly")
    entry_attentes_sexe.place(x=250, y=190)

    label_age_minimum = tk.Label(nouvelle_fenetre, text="age minimum:")
    label_age_minimum.place(x=250, y=210)
    entry_age_minimum = tk.Entry(nouvelle_fenetre, textvariable=MIN_AGE_RECHERCHE, font=("Arial", 8))
    entry_age_minimum.place(x=250, y=230)


    label_age_maximum = tk.Label(nouvelle_fenetre, text="age maximum:")
    label_age_maximum.place(x=250, y=250)
    entry_age_maximum = tk.Entry(nouvelle_fenetre, textvariable=MAX_AGE_RECHERCHE, font=("Arial", 8))
    entry_age_maximum.place(x=250, y=270)


    # Bouton pour fermer la fenêtre
    button_quitter = tk.Button(nouvelle_fenetre, text="Quitter", command=nouvelle_fenetre.destroy)
    button_quitter.place(x=250, y=310)




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