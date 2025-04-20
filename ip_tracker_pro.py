#!/usr/bin/env python3
# IP Tracker by Dan Jersey
# Version: 1.2
# Features: Géolocalisation, fournisseur d'accès, carte approximative, proxy/VPN detection

import requests
import json
import socket
import webbrowser
import sys
from datetime import datetime
import argparse

# Couleurs pour le terminal
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# Configuration de l'API
API_URL = "http://ip-api.com/json/"
FIELDS = "?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query"

def get_ip_info(ip_address=""):
    """Récupère les informations d'une IP via l'API"""
    try:
        response = requests.get(API_URL + ip_address + FIELDS)
        data = response.json()
        
        if data.get('status') == 'fail':
            print(f"{Colors.RED}Erreur: {data.get('message', 'Unknown error')}{Colors.RESET}")
            return None
            
        return data
    except Exception as e:
        print(f"{Colors.RED}Erreur de connexion à l'API: {e}{Colors.RESET}")
        return None

def print_ip_info(data):
    """Affiche joliment les informations de l'IP"""
    if not data:
        return
        
    print(f"\n{Colors.BOLD}{Colors.CYAN}=== INFORMATION SUR L'IP ==={Colors.RESET}")
    print(f"{Colors.BLUE}IP: {Colors.WHITE}{data.get('query', 'N/A')}{Colors.RESET}")
    print(f"{Colors.BLUE}Localisation: {Colors.WHITE}{data.get('city', 'N/A')}, {data.get('regionName', 'N/A')}, {data.get('country', 'N/A')} ({data.get('countryCode', 'N/A')}){Colors.RESET}")
    print(f"{Colors.BLUE}Coordonnées: {Colors.WHITE}Latitude {data.get('lat', 'N/A')}, Longitude {data.get('lon', 'N/A')}{Colors.RESET}")
    print(f"{Colors.BLUE}Fuseau horaire: {Colors.WHITE}{data.get('timezone', 'N/A')} (UTC {data.get('offset', 'N/A')}){Colors.RESET}")
    print(f"{Colors.BLUE}Fournisseur: {Colors.WHITE}{data.get('isp', 'N/A')}{Colors.RESET}")
    print(f"{Colors.BLUE}Organisation: {Colors.WHITE}{data.get('org', 'N/A')}{Colors.RESET}")
    
    # Détection spéciale
    special = []
    if data.get('proxy', False):
        special.append(f"{Colors.RED}Proxy/VPN détecté{Colors.RESET}")
    if data.get('hosting', False):
        special.append(f"{Colors.RED}Hébergement web{Colors.RESET}")
    if data.get('mobile', False):
        special.append(f"{Colors.GREEN}Connexion mobile{Colors.RESET}")
        
    if special:
        print(f"{Colors.BLUE}Détection: {Colors.WHITE}{', '.join(special)}{Colors.RESET}")

def show_on_map(lat, lon):
    """Ouvre la localisation dans OpenStreetMap"""
    map_url = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=12/{lat}/{lon}"
    print(f"\n{Colors.GREEN}Ouverture de la carte dans votre navigateur...{Colors.RESET}")
    webbrowser.open(map_url)

def get_local_ip():
    """Récupère l'IP locale"""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except:
        return None

def save_to_file(data, filename="ip_tracker_results.txt"):
    """Sauvegarde les résultats dans un fichier"""
    try:
        with open(filename, 'a') as f:
            f.write(f"\n=== Résultats du {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
            for key, value in data.items():
                f.write(f"{key}: {value}\n")
            f.write("="*50 + "\n")
        print(f"\n{Colors.GREEN}Résultats sauvegardés dans {filename}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}Erreur lors de la sauvegarde: {e}{Colors.RESET}")

def main():
    # Configuration des arguments
    parser = argparse.ArgumentParser(description="IP Tracker by Dan Jersey")
    parser.add_argument("ip", nargs="?", help="Adresse IP à tracker (vide pour votre IP publique)")
    parser.add_argument("-m", "--map", action="store_true", help="Ouvrir la carte de localisation")
    parser.add_argument("-s", "--save", action="store_true", help="Sauvegarder les résultats dans un fichier")
    parser.add_argument("-l", "--local", action="store_true", help="Afficher seulement l'IP locale")
    args = parser.parse_args()

    print(f"{Colors.BOLD}{Colors.PURPLE}\nIP Tracker by Dan Jersey{Colors.RESET}")
    
    if args.local:
        local_ip = get_local_ip()
        if local_ip:
            print(f"\n{Colors.GREEN}Votre IP locale: {local_ip}{Colors.RESET}")
        else:
            print(f"{Colors.RED}Impossible de déterminer l'IP locale{Colors.RESET}")
        return

    # Tracker l'IP
    target_ip = args.ip if args.ip else ""
    ip_data = get_ip_info(target_ip)
    
    if ip_data:
        print_ip_info(ip_data)
        
        # Options supplémentaires
        if args.map and 'lat' in ip_data and 'lon' in ip_data:
            show_on_map(ip_data['lat'], ip_data['lon'])
            
        if args.save:
            save_to_file(ip_data)
    else:
        print(f"{Colors.RED}Aucune donnée disponible pour cette IP{Colors.RESET}")

if __name__ == "__main__":
    main()