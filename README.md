# 🛡️ Phishing Detection using Machine Learning
> _Un système complet pour capturer des URLs HTTP, extraire des caractéristiques, et détecter des tentatives de phishing en temps réel grâce au Machine Learning._  
> **"Sniffe les paquets, analyse les URLs, stoppe le phishing."**
---

## 🧭 Table des matières

- [📸 Démo](#-démo)
- [🚀 Fonctionnalités principales](#-fonctionnalités-principales)
- [📦 Technologies utilisées](#-technologies-utilisées)
- [🛠️ Installation](#️-installation)
- [▶️ Utilisation](#️-utilisation)
- [🧪 Tests](#-tests)
- [📁 Structure du projet](#-structure-du-projet)
- [📄 Licence](#-licence)
- [👤 Auteur](#-auteur)
- [🙏 Remerciements](#-remerciements)

---

## 📸 Démo

![Demo](./screenshots/demo.gif)  
>_ À venir

---

## 🚀 Fonctionnalités principales
Ce projet propose un **système complet de détection de phishing en temps réel** basé sur :
- 📡 Capture des paquets HTTP en temps réel avec Scapy
- 🧠 Extraction automatique de 13+ caractéristiques d'URL (IP, longueur, entropie, etc.)
- 🤖 Classification intelligente (phishing vs légitime) avec un modèle ML
- 🌐 **API Flask** pour intégrer la prédiction dans n’importe quel outil (pour interagir avec le modèle)
- 📊 Interface web **web de monitoring** avec logs et statistiques
- 🧾 **Base de données SQL Server** pour conserver les détections (date, IP, protocole, verdict)

---

## 📦 Technologies utilisées

| Type        | Technologie                      |
|-------------|----------------------------------|
| Langage     | Python 3.11                      |
| Capture     | Scapy                            |
| Machine Learning | TensorFlow, scikit-learn   |
| Données     | pandas, re, urllib               |
| API         | Flask                            |
| Base de données | SQL Server (via pyodbc)     |
| Web         | HTML / Jinja / Bootstrap         |

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
# 1. Lancer le serveur Flask (prédiction)
cd api
python3 receptFlask.py

# 2. Lancer la capture des paquets HTTP
cd network_capture
sudo python3 captRequest.py -i [interface] #ifconfig (linux) pour trouver l'interface actif

# 3. Lancer le terminal sur une autre fenetre ou ouvrir un navigateur web
# Terminal : wget http://example.com
# Navigateur web : http://example.com
```



