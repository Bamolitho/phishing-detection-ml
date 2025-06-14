import os

def get_data_path(filename):
    """
    Retourne le chemin absolu vers un fichier dans le dossier 'data/'.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))  # chemin de find_path.py
    return os.path.normpath(os.path.join(base_dir, "..", "data", filename)) # Dossier parent

def get_model_path():
    """
    Retourne le chemin absolu vers le fichier du modèle entraîné.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(base_dir, "..", "model", "modele_phishing.h5"))
