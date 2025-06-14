# send_url.py

import requests

def envoyer_url(url):
    payload = {"url": url}
    try:
        response = requests.post("http://127.0.0.1:5000/predict", json=payload, timeout=2)
        if response.status_code == 200:
            data = response.json()
            if "verdict" in data:
                return data["verdict"]
            else:
                print(f"[❌] Réponse JSON invalide : {data}")
                return "Unknown"
        else:
            print(f"[❌] Erreur HTTP : {response.status_code}")
            return "Unknown"

    except requests.exceptions.ConnectionError:
        print(f"[❌] Connexion échouée pour {url} (serveur ML indisponible)")
        return "Unknown"
    except requests.exceptions.Timeout:
        print(f"[⏱️] Timeout lors de l’envoi de {url}")
        return "Unknown"
    except requests.exceptions.RequestException as e:
        print(f"[!] Erreur réseau inconnue pour {url} : {e}")
        return "Unknown"
    except Exception as e:
        print(f"[!] Problème au niveau du modèle : {e}")
        return "Unknown"
