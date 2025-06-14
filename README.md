# 🛡️ Détéction de site web non légitime
> _Un système complet pour capturer des URLs HTTP, extraire des caractéristiques, et détecter des tentatives de phishing en temps réel grâce à l'apprentissage automatique._  

> Résumé : Quelqu'un va sur un site web utilisant http, on lui dit via notre interface web si ce site web est légitime ou non. 
---

## 🧭 Table des matières

- [📸 Démo](#-démo)
- [🚀 Fonctionnalités principales](#-fonctionnalités-principales)
- [📦 Technologies utilisées](#-technologies-utilisées)
- [🛠️ Installation](#️-installation)
- [▶️ Utilisation](#️-utilisation)
- [📁 Structure du projet](#-structure-du-projet)

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
http://localhost:5003
```



