import re
import math
import urllib.parse
from collections import Counter
from urllib.parse import urlparse
import ipaddress

def calculate_entropy(string):
    """Calcule l'entropie d'un domaine"""
    prob = [n_x / len(string) for x, n_x in Counter(string).items()]
    entropy = -sum([p * math.log2(p) for p in prob])
    return entropy

def extract_features_from_url(url: str):
    parsed = urlparse(url)
    features = []

    # 1. Longueur de l'URL
    features.append(len(url))

    # 2. Nombre de sous-domaines
    hostname = parsed.hostname or ""
    features.append(hostname.count("."))

    # 3. Présence de @
    features.append(1 if "@" in url else 0)

    # 4. Présence d’une IP dans le domaine
    try:
        ipaddress.ip_address(hostname)
        features.append(1)
    except:
        features.append(0)

    # 5. Nombre de chiffres dans l’URL
    features.append(len(re.findall(r"\d", url)))

    # 6. Fichier suspect à la fin
    features.append(1 if re.search(r"\.(exe|zip|scr|php)$", parsed.path.lower()) else 0)

    # 7. Mots-clés suspects
    suspicious_keywords = ["login", "secure", "verify", "account", "update", "confirm"]
    features.append(1 if any(keyword in url.lower() for keyword in suspicious_keywords) else 0)

    # 8. Mot "https" dans le chemin
    features.append(1 if "https" in parsed.path.lower() else 0)

    # 9. Nombre de slashs "/"
    features.append(parsed.path.count("/"))

    # 10. Nombre de paramètres GET
    features.append(len(urllib.parse.parse_qs(parsed.query)))

    # 11. Caractères spéciaux
    special_chars = ['%', '=', '&', '?', '-', '_', '.', ':']
    features.append(sum(url.count(c) for c in special_chars))

    # 12. URL raccourcie ?
    shorteners = ["bit.ly", "t.co", "tinyurl", "ow.ly", "goo.gl"]
    features.append(1 if any(short in url for short in shorteners) else 0)

    # 13. Entropie du domaine
    features.append(calculate_entropy(hostname))

    return features
