#!/usr/bin/env python3
# IP Tracker Pro by Dan Jersey
# Version: 2.0
# Fonctionnalités : Tracking IP, numéro de téléphone, username et détection VPN

import json
import requests
import os
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from sys import stderr
import argparse
from datetime import datetime

# Couleurs pour l'affichage
class Couleurs:
    ROUGE = '\033[91m'
    VERT = '\033[92m'
    JAUNE = '\033[93m'
    BLEU = '\033[94m'
    VIOLET = '\033[95m'
    CYAN = '\033[96m'
    BLANC = '\033[97m'
    RESET = '\033[0m'
    GRAS = '\033[1m'

# Configuration de l'API
API_IP = "http://ipwho.is/"
API_TELEPHONE = "http://apilayer.net/api/validate"

def afficher_banniere():
    """Affiche la bannière du programme"""
    stderr.writelines(f"""
{Couleurs.CYAN}
  _____ _____   ____   _____ ____  _____ ______ _____  
 |_   _|  __ \ / __ \ / ____/ __ \|  __ \  ____|  __ \ 
   | | | |__) | |  | | |   | |  | | |__) | |__  | |__) |
   | | |  ___/| |  | | |   | |  | |  _  /|  __| |  ___/ 
  _| |_| |    | |__| | |___| |__| | | \ \| |____| |     
 |_____|_|     \____/ \_____\____/|_|  \_\______|_|     

{Couleurs.VIOLET}          [ + ] OUTIL PROFESSIONNEL DE TRACKING [ + ]
{Couleurs.BLEU}          [ + ] Code par Dan Jersey - 2023 [ + ]
{Couleurs.RESET}
""")

def tracker_ip(ip=None):
    """Track une adresse IP et affiche les informations"""
    try:
        if not ip:
            ip = requests.get('https://api.ipify.org').text
            
        print(f"\n{Couleurs.BLEU}>>> Recherche d'information pour l'IP: {ip}{Couleurs.RESET}")
        
        reponse = requests.get(f"{API_IP}{ip}")
        donnees = reponse.json()
        
        if donnees.get("success", True) == False:
            print(f"{Couleurs.ROUGE}Erreur: {donnees.get('message', 'Inconnue')}{Couleurs.RESET}")
            return
            
        print(f"\n{Couleurs.CYAN}=== INFORMATIONS IP ==={Couleurs.RESET}")
        print(f"{Couleurs.BLANC}IP: {Couleurs.VERT}{donnees.get('ip', 'N/A')}{Couleurs.RESET}")
        print(f"{Couleurs.BLANC}Localisation: {Couleurs.VERT}{donnees.get('city', 'N/A')}, {donnees.get('region', 'N/A')}, {donnees.get('country', 'N/A')}{Couleurs.RESET}")
        print(f"{Couleurs.BLANC}Coordonnées: {Couleurs.VERT}Latitude {donnees.get('latitude', 'N/A')}, Longitude {donnees.get('longitude', 'N/A')}{Couleurs.RESET}")
        print(f"{Couleurs.BLANC}Carte: {Couleurs.VERT}https://www.google.com/maps/@{donnees.get('latitude')},{donnees.get('longitude')},10z{Couleurs.RESET}")
        print(f"{Couleurs.BLANC}Fournisseur: {Couleurs.VERT}{donnees.get('connection', {}).get('isp', 'N/A')}{Couleurs.RESET}")
        print(f"{Couleurs.BLANC}Organisation: {Couleurs.VERT}{donnees.get('connection', {}).get('org', 'N/A')}{Couleurs.RESET}")
        
        if donnees.get('vpn', False) or donnees.get('proxy', False):
            print(f"{Couleurs.BLANC}Détection: {Couleurs.ROUGE}VPN/Proxy détecté!{Couleurs.RESET}")
            
        print(f"{Couleurs.CYAN}======================={Couleurs.RESET}")
        
    except Exception as e:
        print(f"{Couleurs.ROUGE}Erreur: {e}{Couleurs.RESET}")

def tracker_telephone(numero):
    """Track un numéro de téléphone"""
    try:
        print(f"\n{Couleurs.BLEU}>>> Analyse du numéro: {numero}{Couleurs.RESET}")
        
        numero_parse = phonenumbers.parse(numero)
        valide = phonenumbers.is_valid_number(numero_parse)
        
        print(f"\n{Couleurs.CYAN}=== INFORMATIONS TELEPHONE ==={Couleurs.RESET}")
        print(f"{Couleurs.BLANC}Numéro: {Couleurs.VERT}{phonenumbers.format_number(numero_parse, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}{Couleurs.RESET}")
        print(f"{Couleurs.BLANC}Valide: {Couleurs.VERT}{'Oui' if valide else 'Non'}{Couleurs.RESET}")
        
        if valide:
            operateur = carrier.name_for_number(numero_parse, "fr")
            localisation = geocoder.description_for_number(numero_parse, "fr")
            fuseaux = timezone.time_zones_for_number(numero_parse)
            
            print(f"{Couleurs.BLANC}Opérateur: {Couleurs.VERT}{operateur or 'Inconnu'}{Couleurs.RESET}")
            print(f"{Couleurs.BLANC}Localisation: {Couleurs.VERT}{localisation or 'Inconnue'}{Couleurs.RESET}")
            print(f"{Couleurs.BLANC}Fuseau(x) horaire(s): {Couleurs.VERT}{', '.join(fuseaux) if fuseaux else 'Inconnu'}{Couleurs.RESET}")
        
        print(f"{Couleurs.CYAN}=============================={Couleurs.RESET}")
        
    except Exception as e:
        print(f"{Couleurs.ROUGE}Erreur: {e}{Couleurs.RESET}")

def tracker_utilisateur(username):
    """Recherche un username sur les réseaux sociaux"""
    try:
        print(f"\n{Couleurs.BLEU}>>> Recherche de l'utilisateur: @{username}{Couleurs.RESET}")
        
        reseaux = [
            {"nom": "Facebook", "url": f"https://facebook.com/{username}"},
            {"nom": "Instagram", "url": f"https://instagram.com/{username}"},
            {"nom": "Twitter", "url": f"https://twitter.com/{username}"},
            {"nom": "GitHub", "url": f"https://github.com/{username}"},
            {"nom": "LinkedIn", "url": f"https://linkedin.com/in/{username}"},
            {"nom": "TikTok", "url": f"https://tiktok.com/@{username}"},
            {"nom": "YouTube", "url": f"https://youtube.com/{username}"}
        ]
        
        print(f"\n{Couleurs.CYAN}=== RESULTATS RECHERCHE ==={Couleurs.RESET}")
        
        for reseau in reseaux:
            try:
                reponse = requests.get(reseau["url"], timeout=5)
                if reponse.status_code == 200:
                    print(f"{Couleurs.BLANC}[{Couleurs.VERT}+{Couleurs.BLANC}] {reseau['nom']}: {Couleurs.VERT}{reseau['url']}{Couleurs.RESET}")
                else:
                    print(f"{Couleurs.BLANC}[{Couleurs.ROUGE}-{Couleurs.BLANC}] {reseau['nom']}: {Couleurs.JAUNE}Non trouvé{Couleurs.RESET}")
            except:
                print(f"{Couleurs.BLANC}[{Couleurs.ROUGE}-{Couleurs.BLANC}] {reseau['nom']}: {Couleurs.ROUGE}Erreur de connexion{Couleurs.RESET}")
                
        print(f"{Couleurs.CYAN}=========================={Couleurs.RESET}")
        
    except Exception as e:
        print(f"{Couleurs.ROUGE}Erreur: {e}{Couleurs.RESET}")

def menu_principal():
    """Affiche le menu principal"""
    afficher_banniere()
    print(f"\n{Couleurs.VIOLET}1. Tracker une IP")
    print(f"2. Tracker un numéro de téléphone")
    print(f"3. Rechercher un utilisateur")
    print(f"4. Afficher mon IP publique")
    print(f"0. Quitter{Couleurs.RESET}")
    
    try:
        choix = input(f"\n{Couleurs.BLANC}Choisissez une option: {Couleurs.RESET}")
        
        if choix == "1":
            ip = input(f"{Couleurs.BLANC}Entrez l'IP à tracker (vide pour votre IP): {Couleurs.RESET}")
            tracker_ip(ip if ip else None)
        elif choix == "2":
            numero = input(f"{Couleurs.BLANC}Entrez le numéro (format international +33...): {Couleurs.RESET}")
            tracker_telephone(numero)
        elif choix == "3":
            username = input(f"{Couleurs.BLANC}Entrez le username: {Couleurs.RESET}")
            tracker_utilisateur(username)
        elif choix == "4":
            tracker_ip()
        elif choix == "0":
            print(f"\n{Couleurs.VERT}Au revoir!{Couleurs.RESET}")
            exit()
        else:
            print(f"{Couleurs.ROUGE}Option invalide!{Couleurs.RESET}")
            
        input(f"\n{Couleurs.BLANC}Appuyez sur Entrée pour continuer...{Couleurs.RESET}")
        menu_principal()
        
    except KeyboardInterrupt:
        print(f"\n{Couleurs.VERT}Au revoir!{Couleurs.RESET}")
        exit()

if __name__ == "__main__":
    try:
        menu_principal()
    except Exception as e:
        print(f"{Couleurs.ROUGE}Erreur critique: {e}{Couleurs.RESET}")