import pandas as pd
import os
from utils.find_path import get_data_path

def load_data(filename):
    full_path = get_data_path(filename)

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Le fichier à la route '{full_path}' n'a pas été trouvé.")
    
    try:
        df = pd.read_csv(full_path)

        if "type" not in df.columns:
            raise ValueError("La colonne 'type' est manquante dans le dataset.")
        
        X = df.drop(columns=["type"])
        y = df["type"]

        print(f"Dataset chargé avec succès depuis : {full_path}")
        print(f"{len(df)} échantillons.")
        print(f"Aperçu :\n{df.head()}")

        return X, y
    
    except Exception as e:
        print(f"Erreur lors du chargement du fichier : {e}")
        return None, None
