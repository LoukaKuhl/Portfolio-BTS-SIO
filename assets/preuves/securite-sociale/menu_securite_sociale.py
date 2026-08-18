import random

def carte_vitale():
    # Demande du genre
    genre_valide = False
    while not genre_valide:
        genre = input("Entrer [1] pour Homme ou [2] pour Femme : ")
        if genre == "1" or genre == "2":
            genre_valide = True
        else:
            print(f">> Le genre '{genre}' n'est pas valide.")

    # Demande des deux derniers chiffres de l'année
    annee_valide = False
    while not annee_valide:
        annee_courte = input("Entrer les deux derniers chiffres de votre année de naissance (ex: 07) : ")
        if annee_courte.isdigit() and len(annee_courte) == 2:
            annee_valide = True
        else:
            print(">> Entrée non valide. Veuillez entrer exactement 2 chiffres.")

    # Demande du mois
    mois_valide = False
    while not mois_valide:
        mois_courte = input("Entrer le chiffre de votre mois de naissance (ex : 01 pour janvier) : ")
        if mois_courte.isdigit() and len(mois_courte) == 2 and 1 <= int(mois_courte) <= 12:
            mois_valide = True
        else:
            print(">> Entrée non valide. Veuillez entrer un mois entre 01 et 12.")

    # Demande du département
    departement_valide = False
    while not departement_valide:
        departement = input("Entrer le code département de naissance (2 chiffres, ex: 75) : ")
        if departement.isdigit() and len(departement) == 2 and 1 <= int(departement) <= 95:
            departement_valide = True
        else:
            print(">> Entrée non valide. Veuillez entrer un code département valide (01 à 95).")

    # Demande du code commune
    commune_valide = False
    while not commune_valide:
        commune = input("Entrer le code commune de naissance (3 chiffres) : ")
        if commune.isdigit() and len(commune) == 3:
            commune_valide = True
        else:
            print(">> Entrée non valide. Veuillez entrer 3 chiffres pour le code commune.")

    # Demande de l'ordre d'enregistrement ou génération si inconnu
    ordre_valide = False
    while not ordre_valide:
        ordre = input("Entrez votre ordre d'enregistrement à la naissance (3 chiffres, tapez 000 si inconnu) : ")
        if ordre.isdigit() and len(ordre) == 3:
            if ordre == "000":
                ordre = str(random.randint(1, 999)).zfill(3)
                print(f"Ordre d'enregistrement généré automatiquement : {ordre}")
            ordre_valide = True
        else:
            print(">> Entrée non valide. Veuillez entrer exactement 3 chiffres.")

    # Construction du NIR sans clé (13 chiffres)
    nir_sans_cle = genre + annee_courte + mois_courte + departement + commune + ordre

    # Calcul de la clé
    nir_num = int(nir_sans_cle)
    cle = 97 - (nir_num % 97)
    cle_str = str(cle).zfill(2)

    # Construction du NIR complet (15 chiffres)
    nir_complet = nir_sans_cle + cle_str

    # Formatage avec espaces : 1 2 2 2 3 3 2
    formatted_nir = (
        nir_complet[0] + " " +
        nir_complet[1:3] + " " +
        nir_complet[3:5] + " " +
        nir_complet[5:7] + " " +
        nir_complet[7:10] + " " +
        nir_complet[10:13] + " " +
        nir_complet[13:15]
    )

    print("\nNuméro de Sécurité Sociale complet (formaté) :")
    print(formatted_nir)

def test_combinaisons():
    # Scenario fixé
    genre = "1"            # Homme
    annee_courte = "85"    # 1985
    mois_courte = "10"     # Octobre
    departement = "99"     # Naissance hors France métropolitaine

    cle_donnee = 42

    # Liste pour stocker les résultats
    viables = []
    non_viables = []

    # Commune de 001 à 990
    commune_num = 1
    while commune_num <= 990:
        commune = str(commune_num).zfill(3)
        
        # Ordre de 001 à 999
        ordre_num = 1
        while ordre_num <= 999:
            ordre = str(ordre_num).zfill(3)
            
            nir_sans_cle = genre + annee_courte + mois_courte + departement + commune + ordre
            nir_num = int(nir_sans_cle)
            
            cle_calc = 97 - (nir_num % 97)
            
            if cle_calc == cle_donnee:
                viables.append(nir_sans_cle + str(cle_calc).zfill(2))
            else:
                non_viables.append(nir_sans_cle + str(cle_calc).zfill(2))
            
            ordre_num += 1
        commune_num += 1

    print(f"Nombre de combinaisons viables (clé = {cle_donnee}): {len(viables)}")
    print(f"Nombre de combinaisons non viables : {len(non_viables)}")

    print("\nExemples de combinaisons viables (max 10) :")
    for v in viables[:10]:
        # Affichage avec espaces comme sur carte vitale
        formatted = (
            v[0] + " " +
            v[1:3] + " " +
            v[3:5] + " " +
            v[5:7] + " " +
            v[7:10] + " " +
            v[10:13] + " " +
            v[13:15]
        )
        print(formatted)

    print("\nExemples de combinaisons non viables (max 10) :")
    for nv in non_viables[:10]:
        formatted = (
            nv[0] + " " +
            nv[1:3] + " " +
            nv[3:5] + " " +
            nv[5:7] + " " +
            nv[7:10] + " " +
            nv[10:13] + " " +
            nv[13:15]
        )
        print(formatted)

def menu():
    while True:
        print("\nMenu principal :")
        print("1 - Tester combinaisons (test_combinaisons)")
        print("2 - Générer numéro sécurité sociale (carte_vitale)")
        print("0 - Quitter")

        choix = input("Entrez votre choix : ")

        if choix == "1":
            test_combinaisons()
        elif choix == "2":
            carte_vitale()
        elif choix == "0":
            print("Au revoir !")
            break
        else:
            print("Choix invalide, réessayez.")

if __name__ == "__main__":
    menu()
