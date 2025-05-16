# 🛡️ Phishing Detection using Machine Learning
> _Un système complet pour capturer des URLs HTTP, extraire des caractéristiques, et détecter des tentatives de phishing en temps réel grâce au Machine Learning._  
> **"Sniffe les paquets, analyse les URLs, classifier les sites web (légitime ou phishing)."**
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
- [👤 Auteurs](#-auteurs)
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
python3 api/receptFlask.py

# 2. Lancer la capture des paquets HTTP
sudo python3 network_capture/captRequest.py -i [interface] # ifconfig (linux) pour trouver l'interface active

# 3. Lancer le terminal sur une autre fenetre ou ouvrir un navigateur web
# Terminal : wget http://example.com
# Navigateur web : http://example.com

# Nota : Se placer dans le dossier parent des dossiers model, api, network_capture... est important
```

## 👤 Auteurs
<img src="https://media.licdn.com/dms/image/v2/D4E03AQE0RS8O9YuIBQ/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1731164064570?e=1752710400&v=beta&t=SL7J1e3sF2duZ7tIablBmQb0CzHfy6kArP7a2lzcw40" alt="Amolitho Baldé" width="120" style="border-radius: 50%; margin-right: 15px;" align="left">

**Amolitho Baldé**  
💼 *Étudiant en Télécommunications & Réseaux*  
🔗 [LinkedIn](https://www.linkedin.com/in/amolithobalde/) | [Portfolio](https://bamolitho.github.io/portfolio/)
<p>Université Sorbonne Paris Nord</p>

<br clear="left"/>

<img src="https://media.licdn.com/dms/image/v2/D4E03AQE6W960oHvj7g/profile-displayphoto-shrink_200_200/B4EZZAPunCHEAg-/0/1744834599732?e=1752710400&v=beta&t=3v_xSXek9HFZZTx0vzI22pzobe7jCrBwBK7u9_5jR3c" alt="Amolitho Baldé" width="120" style="border-radius: 50%; margin-right: 15px;" align="left">

**Edmond Kameni Junior**  
💼 *Étudiant en Télécommunications & Réseaux*  
🔗 [LinkedIn](https://www.linkedin.com/in/edmond-junior-kameni-6715a9278/)
<p>Université Sorbonne Paris Nord</p>>

<br clear="left"/>


