# Detta blir basen i mitt projekt, själva menyn där man väljer vilket verktyg man vill använda.

#!/usr/bin/env python3

import os
import sys
import time
import platform
import subprocess
from tools import portscanner
from tools import pingsweep
from tools import macspoof

# --- Funktion för att skriva ett tecken i taget ---

def typer(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# --- CLEAR SCREEN FUNCTION ---

def clrscr():
    #WIN ELLER LINUX
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

# --- Få ut IP-ADDRESSER ----

def get_local_ips():
    if platform.system().lower() == "windows":
        return []

    try:
        # Hitta interface som används för default route
        route = subprocess.check_output(["ip", "route", "get", "1.1.1.1"], text=True).strip()
        # Ex: "... dev wlan0 src 192.168.1.123 ..."
        parts = route.split()
        dev = parts[parts.index("dev") + 1]

        ip_out = subprocess.check_output(["ip", "-4", "-o", "addr", "show", "dev", dev], text=True).strip()
        # Ex: "3: wlan0    inet 192.168.1.123/24 ..."
        ip_cidr = ip_out.split()[3]
        ip = ip_cidr.split("/")[0]

        print(f"              Aktiv NIC: {dev} | IP: {ip}")
        return [ip]
    except Exception:
        return []


# --- PAUSE ---

def pause():
    input("Pr3ss [3nter] t0 c0nt1nu3...")

# --- MENY-SYSTEMET ---

def menu() -> None:
    print(r"""
          
    ▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌
    ▐                                                      ▌
    ▐   _______ ______ ______ ____   __  __ ____ _______   ▌
    ▐  |_     _|      |      |_   | |  |/  |_   |_     _|  ▌
    ▐    |   | |  --  |  --  |_|  |_|     < _|  |_|   |    ▌
    ▐    |___| |______|______|______|__|\__|______|___|    ▌
    ▐                                                      ▌
    ▐▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌
          
              CYBER SECURITY TOOLKIT FOR LINUX
                         MAIN MENU""")
    print("")
    get_local_ips()
    print("")
    typer("[1]. PING SWEEP")
    typer("[2]. PORT SCAN" )
    typer("[3]. SPOOF YOUR MAC ADDRESS" )
    typer("[4]. PLACEHOLDER" )
    typer("[0]. Exit")    

def main():
    while True:
        clrscr()  # --- RENSA SKÄRMEN --- 
        menu()
        val = input("\nCh00s3 yu0r t001: ")

        if val == "1":
            time.sleep(1)
            
            pingsweep.run()
            pause()
        elif val == "2":
            time.sleep(1)
            portscanner.run()
            pause()

            
        elif val == "3":
            time.sleep(1)
            macspoof.run()
            pause()
        elif val == "0":
            typer("\n --- SO LONG SUCKER! ---")
            
            time.sleep(1)
            sys.exit()
        else:
            typer("Wr0ng 1nput, Try Ag61n: ")
            time.sleep(1)



if __name__ == "__main__":
    main()
