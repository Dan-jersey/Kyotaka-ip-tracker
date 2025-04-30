#!/usr/bin/python
# github.com/danjersey-dev

import json
import requests
import time
import os
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from sys import stderr

BLK = '\033[30m'
RED = '\033[1;31m'
GRN = '\033[1;32m'
YEL = '\033[1;33m'
BLU = '\033[1;34m'
MAG = '\033[1;35m'
CYN = '\033[1;36m'
WHT = '\033[1;37m'

def banner():
    print(f"""
{GRN}██████╗  █████╗ ███╗   ██╗     ██╗███████╗{WHT} ██████╗  █████╗ ███╗   ██╗
{GRN}██╔══██╗██╔══██╗████╗  ██║    ██╔╝██╔════╝{WHT}██╔════╝ ██╔══██╗████╗  ██║
{GRN}██║  ██║███████║██╔██╗ ██║   ██╔╝ █████╗  {WHT}██║  ███╗███████║██╔██╗ ██║
{GRN}██║  ██║██╔══██║██║╚██╗██║  ██╔╝  ██╔══╝  {WHT}██║   ██║██╔══██║██║╚██╗██║
{GRN}██████╔╝██║  ██║██║ ╚████║ ██╔╝   ███████╗{WHT}╚██████╔╝██║  ██║██║ ╚████║
{GRN}╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═╝    ╚══════╝{WHT} ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝
                                        
{WHT}╔═══════════════════════════════════════════════════════════╗
{WHT}║ {GRN}[DJS] {BLU}Author  : {CYN}Dan Jersey                             {WHT}║
{WHT}║ {GRN}[DJS] {BLU}GitHub  : {CYN}github.com/danjersey-dev               {WHT}║
{WHT}║ {GRN}[DJS] {BLU}Tool    : {CYN}JCODE Tracker                         {WHT}║
{WHT}╚═══════════════════════════════════════════════════════════╝
    """)

def get_info(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        print(f"{WHT}Number: {CYN}{phone_number}")
        print(f"{WHT}Valid: {CYN}{phonenumbers.is_valid_number(parsed_number)}")
        print(f"{WHT}Region: {CYN}{geocoder.description_for_number(parsed_number, 'en')}")
        print(f"{WHT}Carrier: {CYN}{carrier.name_for_number(parsed_number, 'en')}")
        print(f"{WHT}Timezone: {CYN}{timezone.time_zones_for_number(parsed_number)}")
    except Exception as e:
        print(f"{RED}Erreur: {e}", file=stderr)

def main():
    os.system('clear')
    banner()
    number = input(f"{YEL}Entrez le numéro avec l'indicatif (ex: +243...): {WHT}")
    get_info(number)

if __name__ == "__main__":
    main()