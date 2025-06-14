import pandas as pd
import re
import math
import ipaddress
from collections import Counter
from urllib.parse import urlparse, parse_qs
from utils.find_path import get_data_path

# Fonction pour calculer l'entropie du domaine
def calculate_entropy(string):
    if not string:
        return 0
    prob = [n_x / len(string) for x, n_x in Counter(string).items()]
    entropy = -sum([p * math.log2(p) for p in prob])
    return entropy

# Fonction d'extraction des features
def extract_features_from_url(url: str):
    try:
        parsed = urlparse(url)
        features = []

        features.append(len(url))  # Longueur
        hostname = parsed.hostname or ""
        features.append(hostname.count("."))  # Sous-domaines
        features.append(1 if "@" in url else 0)  # Présence de @

        try:
            ipaddress.ip_address(hostname)
            features.append(1)  # IP
        except:
            features.append(0)

        features.append(len(re.findall(r"\d", url)))  # Nombres
        features.append(1 if re.search(r"\.(exe|zip|scr|php)$", parsed.path.lower()) else 0)  # Fichier suspect

        suspicious_keywords = ["login", "secure", "verify", "account", "update", "confirm"]
        features.append(1 if any(keyword in url.lower() for keyword in suspicious_keywords) else 0)  # Mots-clés suspects

        features.append(1 if "https" in parsed.path.lower() else 0)  # "https" dans le chemin
        features.append(parsed.path.count("/"))  # Slashs
        features.append(len(parse_qs(parsed.query)))  # Paramètres GET

        special_chars = ['%', '=', '&', '?', '-', '_', '.', ':']
        features.append(sum(url.count(c) for c in special_chars))  # Caractères spéciaux

        shorteners = ["bit.ly", "t.co", "tinyurl", "ow.ly", "goo.gl"]
        features.append(1 if any(short in url for short in shorteners) else 0)  # URL raccourcie

        features.append(calculate_entropy(hostname))  # Entropie

        return features

    except Exception as e:
        print(f"[!] URL ignorée (invalide) : {url} ➤ {e}")
        return None  # Ignorer cette URL

# === Configuration ===
input_path = get_data_path("http_url_dataset.csv")
output_path = get_data_path("features_phishing_dataset.csv")

# Lire le CSV
df = pd.read_csv(input_path)

# Liste des noms de colonnes pour les features
feature_names = [
    "url_length", "num_subdomains", "has_at", "has_ip", "num_digits",
    "suspicious_file", "suspicious_keywords", "https_in_path",
    "num_slashes", "num_get_params", "num_special_chars",
    "is_shortened", "domain_entropy"
]

# Appliquer la fonction d'extraction avec gestion des erreurs
features = df['url'].apply(extract_features_from_url)

# Filtrer les lignes valides
valid_mask = features.notnull()
df_valid = df[valid_mask].copy()
features_valid = pd.DataFrame(features[valid_mask].tolist(), columns=feature_names)

# Convertir type en label numérique
df_valid['type'] = df_valid['type'].apply(lambda x: 1 if str(x).lower() == 'phishing' else 0)
features_valid['type'] = df_valid['type']

# Sauvegarder
features_valid.to_csv(output_path, index=False)
print(f"Fichier généré avec succès : {output_path}")
