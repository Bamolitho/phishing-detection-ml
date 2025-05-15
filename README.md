# 🛡️ Phishing Detection using Machine Learning
> _Un système complet pour capturer des URLs HTTP, extraire des caractéristiques, et détecter des tentatives de phishing en temps réel grâce au Machine Learning._  
> **"Sniffe les paquets, analyse les URLs, stoppe le phishing."**

Ce projet propose un **système complet de détection de phishing en temps réel** basé sur :
- 🔎 la capture du trafic réseau (HTTP) avec **Scapy**
- 🧠 l'extraction automatique de **caractéristiques d'URL**
- 🤖 la classification des URL par un **modèle de Machine Learning**
- 🌐 une **API Flask** pour intégrer la prédiction dans n’importe quel outil
- 📊 une interface **web de monitoring** avec logs et statistiques
- 🗄️ une **base de données SQL Server** pour conserver les détections
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
> _Ajoute ici un gif, une capture ou une vidéo de l'interface de capture + détection._

---

## 🚀 Fonctionnalités principales

- 📡 Capture des paquets HTTP en temps réel avec Scapy
- 🧠 Extraction de 13+ caractéristiques d'URL (IP, longueur, entropie, etc.)
- 🤖 Classification intelligente (phishing vs légitime) avec un modèle ML
- 🌐 API Flask pour interagir avec le modèle
- 📊 Interface web pour visualiser les verdicts
- 🧾 Stockage SQL Server (date, IP, protocole, verdict)

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
| Tests       | pytest *(à ajouter si besoin)*   |

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


