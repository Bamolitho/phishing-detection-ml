# 🛡️ Détéction de site web non légitime
> _Un système complet pour capturer des URLs HTTP, extraire des caractéristiques, et détecter des tentatives de phishing en temps réel grâce à l'apprentissage automatique._  

> Résumé : Quelqu'un va sur un site web utilisant http, on lui dit via notre interface web si ce site web est légitime ou non. 
---

## 🧭 Table des matières

- [📸 Démo](#-démo)
- [🚀 Fonctionnalités principales](#-fonctionnalités-principales)
- [📦 Technologies utilisées](#-technologies-utilisées)
- [📁 Structure du projet](#-structure-du-projet)
- [🛠️ Installation](#️-installation)
- [▶️ Utilisation](#️-utilisation)
- [ Perspectives](#-perspectives)
---

## 📸 Démo

![Demo](./demo/demo.gif)  
>_ À venir

---

## 🚀 Fonctionnalités principales
Ce projet propose un **système complet de détection de phishing en temps réel** basé sur :
- 📡 Capture des paquets HTTP en temps réel avec Scapy
- 🧠 Extraction automatique de 13+ caractéristiques d'URL (IP, longueur, entropie, etc.)
- 🤖 Classification intelligente (phishing vs légitime) avec un modèle ML
- 🌐 **API Flask** pour intégrer la prédiction dans n’importe quel outil (pour interagir avec le modèle)
- 📊 Interface web **web de monitoring** avec logs et statistiques
- 🧾 **Base de données SQLite** pour conserver les détections (date, IP, protocole, verdict)

---

## 📦 Technologies utilisées

| Type        | Technologie                      |
|-------------|----------------------------------|
| Langage     | Python 3.11                      |
| Capture     | Scapy                            |
| Machine Learning | TensorFlow, scikit-learn    |
| Données     | pandas, re, urllib               |
| API         | Flask                            |
| Base de données | SQLite                       |
| Web         | HTML / CSS / JS                  |

---

## Structure du projet
```bash
phishing-detection-ml/
│
├── 📁 data/                     # Contient les jeux de données bruts et prétraités
│   ├── url_dataset.xlsx                 # Jeu de données original avec URLs (phishing et légitimes)
│   ├── http_url_dataset.csv            # Version filtrée ne contenant que les URLs en HTTP
│   └── features_phishing_dataset.csv   # Jeu de données avec les caractéristiques extraites (features)
│
├── 📁 model/                    # Scripts pour entraîner, charger, et utiliser le modèle ML
│   ├── __init__.py                       # Fichier d’initialisation du module
│   ├── model_handler.py                 # Fonctions pour gérer le modèle (chargement, prédiction, etc.)
│   └── phishing_model.h5                # Modèle de détection de phishing préentraîné (Keras/TensorFlow)
│
├── 📁 network_capture/          # Scripts pour la capture réseau en temps réel (via Scapy)
│   ├── __init__.py                       # Fichier d’initialisation du module
│   ├── http_url_sniffer.py             # Capture les URLs HTTP transitant sur le réseau local
│   └── captRequest.py                  # Récupère, traite et prépare les requêtes sniffées pour analyse
│
├── 📁 api/                      # API Flask servant d’interface entre Scapy/Web et le modèle ML
│   ├── __init__.py                       # Fichier d’initialisation
│   └── receptFlask.py                  # API REST qui reçoit les URLs et renvoie la prédiction
│
├── 📁 web/                      # Interface web pour interagir avec l’utilisateur
│   ├── __init__.py                       # Initialisation du module web
│   ├── app.py                           # Lance l’application web (probablement Flask ou Django intégré)
│   └── templates/                       # Fichiers HTML pour les pages web
│       ├── changer_mot_de_passe.html       # Page de changement de mot de passe
│       ├── index.html                      # Page d'accueil
│       ├── login.html                      # Page de connexion
│       ├── profile_admin.html              # Interface de l’administrateur
│       ├── profile_user.html               # Interface de l’utilisateur standard
│       ├── register.html                   # Formulaire d'inscription
│       └── stats.html                      # Page de statistiques (prédictions, trafic, etc.)
│   └── static/                          # Fichiers statiques (CSS, images, JS...)
│       ├── style.css                      # Style global
│       ├── profile_user.css               # Style de la page utilisateur
│       └── profile_admin.css              # Style de la page administrateur
│
├── 📁 utils/                    # Fonctions utilitaires pour automatiser le traitement
│   ├── __init__.py                       # Initialisation du module
│   ├── convert_https_to_http.py         # Convertit les URLs HTTPS vers HTTP (utile pour sniffing)
│   ├── extract_features_from_http_dataset_csv.py  # Extrait les caractéristiques des URLs d’un CSV HTTP
│   ├── extract_features_from_one_url.py           # Extrait les caractéristiques d’une seule URL
│   ├── find_path.py                      # Trouve dynamiquement les chemins relatifs vers les fichiers
│   ├── load_data.py                      # Charge les datasets dans des formats utilisables (Pandas, etc.)
│   └──  send_url.py                       # Envoie une URL à l’API Flask pour analyse
│ 
├── 📁 database/                 # 🗄Scripts et base de données pour la gestion des utilisateurs
│   ├── __init__.py                       # Initialisation
│   ├── database.py                      # Gère la base SQLite (création, accès, requêtes)
│   └── users.db                         # Base de données SQLite générée automatiquement si absente
│
├── .gitignore                  # Fichiers et dossiers à ignorer par Git (comme .db, __pycache__, etc.)
├── launch_all.sh              # Script shell pour tout lancer automatiquement (API, sniffing, web)
├── README.md                  # Documentation complète du projet : objectif, installation, démo
└── requirements.txt           # Dépendances Python à installer avec `pip install -r requirements.txt`
```

## 🛠️ Installation

```bash
# 1. Cloner le repo
git clone https://github.com/Bamolitho/phishing-detection-ml.git
cd phishing-detection-ml

# 2. Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # ou .\venv\Scripts\activate sur Windows

# 3. Installer les dépendances
pip install -r requirements.txt
```

## ▶️ Utilisation
```bash
# 1. Se placer dans le dossier du projet, phishing-detection-ml.
cd chemin_vers_phishing-detection-ml

# 2. Ajouter des privilèges d'exécution pour l'utilisateur
sudo chmod +x launch_all.sh

# 3. Pour lancer les 3 composantes (Modèle ML, la sonde, l'app flask contenant les fonctionnalités essentielles pour l'interface web)
./launch_all.sh ou bash launch_all.sh

# 4. Ouvrir un navigateur pour accéder à l'interface web via l'adresse suivante
http://localhost:5003/login
```
## Perspectives



