#!/bin/bash

echo "📡 Lancement du système de détection de phishing..."

# Dossier racine du projet (à adapter si besoin)
PROJECT_DIR="$(pwd)"

# Lancement du modèle (receptFlask.py)
gnome-terminal --title="🧠 Modèle" -- bash -c "
cd \"$PROJECT_DIR/api\"
echo '🚀 Initialisation du modèle...'
python3 receptFlask.py
exec bash"

# Lancement de la sonde réseau (captRequest.py)
gnome-terminal --title="🔍 Sonde Réseau" -- bash -c "
cd \"$PROJECT_DIR/network_capture\"
echo '📡 Lancement de la sonde réseau...'
sudo python3 captRequest.py
exec bash"

# Lancement de l'application Flask (app.py)
gnome-terminal --title="🌐 App Flask" -- bash -c "
cd \"$PROJECT_DIR/web\"
echo '🌐 Lancement de l''application Flask...'
python3 app.py
exec bash"

echo "✅ Tous les composants sont lancés dans des terminaux séparés !"
