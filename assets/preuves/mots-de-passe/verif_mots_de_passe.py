import sqlite3
import json
import itertools
import string

# === Chargement des dictionnaires JSON ===
def charger_dictionnaire(fichier):
    with open(fichier, "r", encoding="utf-8") as f:
        return json.load(f)

mots = charger_dictionnaire("dictionnaire.json")
couleurs = charger_dictionnaire("complement.json")
speciaux = charger_dictionnaire("speciaux.json")

# === Connexion à la base de données ===
conn = sqlite3.connect("Test_Mots_De_Passe.db")
cursor = conn.cursor()
cursor.execute("SELECT login, password FROM utilisateur")
utilisateurs = cursor.fetchall()

# === Étape 7 : Mot exact ===
def test_mot_exact():
    print("\n🔍 Étape 7 : Mot exact")
    for login, password in utilisateurs:
        if password in mots:
            print(f"✅ {login} : {password}")

# === Étape 8 : Mot + nombre ===
def test_mot_nombre():
    print("\n🔍 Étape 8 : Mot + nombre")
    for login, password in utilisateurs:
        for mot in mots:
            for i in range(10000):
                test = f"{mot}{i}"
                if test == password:
                    print(f"✅ {login} : {test}")
                    break

# === Étape 9 : Mot + couleur ===
def test_mot_couleur():
    print("\n🔍 Étape 9 : Mot + couleur")
    for login, password in utilisateurs:
        for mot in mots:
            for couleur in couleurs:
                if password == mot + couleur:
                    print(f"✅ {login} : {password} (mot : {mot}, couleur : {couleur})")
                    break

# === Étape 10 : Mot + caractère spécial + couleur ===
def test_mot_speciaux_couleur():
    print("\n🔍 Étape 10 : Mot + caractère spécial + couleur")
    for login, password in utilisateurs:
        for mot in mots:
            for s in speciaux:
                for couleur in couleurs:
                    test = mot + s + couleur
                    if password == test:
                        print(f"✅ {login} : {password} (mot : {mot}, spécial : {s}, couleur : {couleur})")
                        break

# === Étape 11 : Mot + caractère spécial + chiffre ===
def test_mot_speciaux_chiffre():
    print("\n🔍 Étape 11 : Mot + caractère spécial + chiffre")
    for login, password in utilisateurs:
        for mot in mots:
            for s in speciaux:
                for i in range(100):
                    test = f"{mot}{s}{i}"
                    if password == test:
                        print(f"✅ {login} : {password} (mot : {mot}, spécial : {s}, chiffre : {i})")
                        break

# === Étape 12 : Force brute sur 3 à 5 caractères ===
def force_brute():
    print("\n🔍 Étape 12 : Force brute sur 3 à 5 caractères")
    charset = string.ascii_letters + string.digits + ''.join(speciaux)
    for login, password in utilisateurs:
        for l in range(3, 6):
            for comb in itertools.product(charset, repeat=l):
                test = ''.join(comb)
                if password == test:
                    print(f"🔓 {login} : {test}")
                    break

# === Menu principal ===
def menu():
    print("\n📌 Menu de vérification des mots de passe")
    print("1 - Test mot exact")
    print("2 - Test mot + nombre")
    print("3 - Test mot + couleur")
    print("4 - Test mot + caractère + couleur")
    print("5 - Test mot + caractère + chiffre")
    print("6 - Force brute sur 3 à 5 caractères")
    print("7 - Quitter")
    return input("Choisis une option : ")

# === Boucle principale ===
while True:
    choix = menu()
    if choix == "1":
        test_mot_exact()
    elif choix == "2":
        test_mot_nombre()
    elif choix == "3":
        test_mot_couleur()
    elif choix == "4":
        test_mot_speciaux_couleur()
    elif choix == "5":
        test_mot_speciaux_chiffre()
    elif choix == "6":
        force_brute()
    elif choix == "7":
        print("👋 Fin du programme.")
        break
    else:
        print("❌ Option invalide. Réessaie.")

conn.close()
