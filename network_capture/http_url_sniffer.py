# htt_url_sniffer.py

from scapy.all import sniff
from scapy.layers.http import HTTPRequest
from datetime import datetime
import os, sys, argparse, socket, threading

# Ajout du chemin vers les modules nécessaires
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.send_url import envoyer_url

# Ajout du chemin vers la base de données
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../database')))
from database.database import insert_detection


class HTTPCapture:
    def __init__(self, output_file):
        self.output_file = output_file
        self.seen_url = ""
        self.user_id = None

    def set_user_id(self, user_id):
        self.user_id = user_id

    def process_packet(self, packet):
        if self.user_id is None:
            return  # Ne pas insérer si aucun utilisateur n'est lié

        if packet.haslayer(HTTPRequest):
            try:
                http_layer = packet[HTTPRequest]
                host = http_layer.Host.decode('utf-8') if http_layer.Host else ""
                path = http_layer.Path.decode('utf-8') if http_layer.Path else ""

                if not host:
                    return

                # 🔧 Normalisation : ajouter www. si absent
                if not host.startswith("www."):
                    host = "www." + host

                captured_url = f"http://{host}{path}"

                if captured_url != self.seen_url:
                    self.seen_url = captured_url
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"[{timestamp}] Nouvelle URL capturée : {captured_url}")

                    ip_src = packet[0][1].src
                    ip_dst = packet[0][1].dst
                    protocole = "HTTP"

                    verdict = envoyer_url(captured_url)

                    insert_detection(self.user_id, captured_url, ip_src, ip_dst, protocole, verdict, timestamp)

            except Exception as e:
                print(f"[⚠] Erreur lors du traitement du paquet : {e}")


def start_server(analyzer, host='localhost', port=5002):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"🛰️ En écoute sur {host}:{port}")

    while True:
        client_socket, _ = server_socket.accept()
        data = client_socket.recv(1024).decode()
        if data:
            try:
                user_id = int(data.strip())
                analyzer.set_user_id(user_id)
            except ValueError:
                print(f"[⚠] Valeur user_id invalide : {data}")
        client_socket.close()


def start_capture(interface, output_file):
    analyzer = HTTPCapture(output_file)

    # Démarrer le serveur en parallèle
    server_thread = threading.Thread(target=start_server, args=(analyzer,), daemon=True)
    server_thread.start()

    print(f"👉 Interface utilisée : {interface}")
    print(f"📡 Capture en cours sur {interface}... (Ctrl+C pour arrêter)\n")

    sniff(iface=interface, prn=analyzer.process_packet, filter="tcp port 80", store=0)
