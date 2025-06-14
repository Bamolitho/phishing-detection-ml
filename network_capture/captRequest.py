from scapy.all import conf
import argparse
from http_url_sniffer import start_capture

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", help="Interface réseau à écouter (facultatif)")
    parser.add_argument("-o", "--output", default="output.txt", help="Fichier de sortie")
    args = parser.parse_args()

    # Détection automatique si aucune interface n'est précisée
    interface = args.interface if args.interface else conf.iface

    start_capture(interface, args.output)
