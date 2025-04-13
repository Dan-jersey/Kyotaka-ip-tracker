#!/usr/bin/env python3
# IP Tracker Pro - Termux Edition
# Code by [Votre Nom] | v3.0

import os
import requests
import json
import socket
import folium
from colorama import Fore, Style, init

# Configuration des couleurs
init()
class c:
    G = Fore.GREEN
    R = Fore.RED
    Y = Fore.YELLOW
    B = Fore.BLUE
    C = Fore.CYAN
    W = Fore.WHITE
    BR = Style.BRIGHT
    RS = Style.RESET_ALL

# Configuration de base
class Config:
    SERVICES = {
        'ip-api': {
            'url': 'http://ip-api.com/json/{ip}',
            'fields': {
                'status': 'Statut',
                'country': 'Pays',
                'regionName': 'Région', 
                'city': 'Ville',
                'isp': 'Fournisseur',
                'lat': 'Latitude',
                'lon': 'Longitude'
            }
        },
        'ipinfo': {
            'url': 'https://ipinfo.io/{ip}/json',
            'fields': {
                'hostname': 'Hostname',
                'org': 'Organisation',
                'timezone': 'Fuseau horaire',
                'loc': 'Coordonnées'
            }
        }
    }

class IPTracker:
    def __init__(self):
        self.results = {}
        
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def show_banner(self):
        self.clear_screen()
        print(f"""{c.BR}{c.C}
   ▄▄▄▄▄▄▄ ▄▄   ▄▄ ▄▄▄▄▄▄▄ 
   █ ▄▄▄ █ ██ █ █ █ ▄▄▄ █ 
   █ ███ █  ▄▀▄  █ ███ █ 
   █▄▄▄▄▄█ █▄▀▄█ █▄▄▄▄▄█ 
   ▄▄▄▄▄  ▄ ▄▄▄██ ▄ ▄▄▄ 
   ▄ ▄ ▄▄▀██ ▀▄▄ ▄▄▀▀ ██ 
   █▄█▄▄▄██▄▄▄▄ ▀▄▀▄▀▄▀ 
   ▄▄▄▄▄▄▄ █▄▀▄ ▀█▄█ ██ 
   █ ▄▄▄ █  ▀▄██ ▄▄▀▄▄▀ 
   █ ███ █ █ ▄▀ ▀▄▄▄ ▄▀ 
   █▄▄▄▄▄█ █▀ █▀▄▀▀█▄█ 
        {c.RS}""")
        print(f"{c.BR}{c.Y} [>] {c.W}IP Tracker Pro {c.G}v3.0{c.RS}")
        print(f"{c.BR}{c.Y} [>] {c.W}Mode: {c.R}Grand Carrère Edition{c.RS}\n")

    def get_public_ip(self):
        try:
            return requests.get('https://api.ipify.org').text
        except:
            return None

    def validate_ip(self, ip):
        try:
            socket.inet_aton(ip)
            return True
        except:
            return False

    def fetch_data(self, ip):
        results = {}
        for name, service in Config.SERVICES.items():
            try:
                url = service['url'].format(ip=ip)
                r = requests.get(url, timeout=10)
                data = r.json()
                
                if 'error' not in data:
                    results[name] = data
                    print(f"{c.BR}{c.G} [+] {c.W}Service {name} réussi{c.RS}")
                else:
                    print(f"{c.BR}{c.R} [!] Erreur {name}: {data.get('message', 'Inconnue')}{c.RS}")
                    
            except Exception as e:
                print(f"{c.BR}{c.R} [!] Erreur {name}: {str(e)}{c.RS}")
        
        return results

    def display_results(self, ip, data):
        print(f"\n{c.BR}{c.Y} [*] {c.W}Résultats pour {c.G}{ip}{c.RS}")
        
        for service_name, result in data.items():
            service = Config.SERVICES[service_name]
            print(f"\n{c.BR}{c.C} ┌─[{service_name.upper()}]{c.RS}")
            
            for field, label in service['fields'].items():
                if field in result:
                    value = result[field]
                    if field == 'loc' and ',' in value:
                        lat, lon = value.split(',')
                        value = f"Lat: {lat}, Lon: {lon}"
                    print(f"{c.BR}{c.W} ├─ {label}: {c.G}{value}{c.RS}")

    def generate_map(self, ip, data):
        coords = None
        
        # Trouver les coordonnées
        if 'ip-api' in data and 'lat' in data['ip-api']:
            coords = (data['ip-api']['lat'], data['ip-api']['lon'])
        elif 'ipinfo' in data and 'loc' in data['ipinfo']:
            lat, lon = data['ipinfo']['loc'].split(',')
            coords = (float(lat), float(lon))
        
        if coords:
            try:
                m = folium.Map(location=coords, zoom_start=12)
                folium.Marker(
                    coords,
                    popup=f"IP: {ip}",
                    tooltip="Localisation approximative",
                    icon=folium.Icon(color='red', icon='info-sign')
                ).add_to(m)
                
                map_file = f"IP_{ip.replace('.','_')}_MAP.html"
                m.save(map_file)
                print(f"\n{c.BR}{c.G} [>] {c.W}Carte générée: {c.C}{map_file}{c.RS}")
            except Exception as e:
                print(f"{c.BR}{c.R} [!] Erreur carte: {str(e)}{c.RS}")

    def save_results(self, ip, data):
        filename = f"IP_{ip.replace('.','_')}_RESULTS.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"{c.BR}{c.G} [>] {c.W}Résultats sauvegardés: {c.C}{filename}{c.RS}")

    def run(self):
        self.show_banner()
        print(f"{c.BR}{c.W} [1] {c.G}Tracker une IP spécifique{c.RS}")
        print(f"{c.BR}{c.W} [2] {c.G}Votre IP publique{c.RS}")
        print(f"{c.BR}{c.W} [3] {c.R}Quitter{c.RS}")
        
        choice = input(f"\n{c.BR}{c.Y} [>] {c.W}Choix: {c.RS}")
        
        if choice == '1':
            ip = input(f"{c.BR}{c.Y} [>] {c.W}Entrez l'IP: {c.RS}")
            if self.validate_ip(ip):
                data = self.fetch_data(ip)
                self.display_results(ip, data)
                self.generate_map(ip, data)
                self.save_results(ip, data)
            else:
                print(f"{c.BR}{c.R} [!] IP invalide{c.RS}")
        elif choice == '2':
            ip = self.get_public_ip()
            if ip:
                print(f"\n{c.BR}{c.G} [>] {c.W}Votre IP: {c.C}{ip}{c.RS}")
                data = self.fetch_data(ip)
                self.display_results(ip, data)
                self.generate_map(ip, data)
                self.save_results(ip, data)
            else:
                print(f"{c.BR}{c.R} [!] Impossible de récupérer votre IP{c.RS}")
        elif choice == '3':
            exit()
        
        input(f"\n{c.BR}{c.Y} [>] {c.W}Appuyez sur Entrée...{c.RS}")
        self.run()

if __name__ == '__main__':
    try:
        # Vérification des dépendances
        import requests
        import folium
        
        tracker = IPTracker()
        tracker.run()
        
    except ImportError as e:
        print(f"\n{c.BR}{c.R} [!] Module manquant: {str(e)}{c.RS}")
        print(f"{c.BR}{c.Y} [>] Installez avec: {c.G}pip install {str(e).split()[-1]}{c.RS}")
    except KeyboardInterrupt:
        print(f"\n{c.BR}{c.R} [!] Interrompu par l'utilisateur{c.RS}"
