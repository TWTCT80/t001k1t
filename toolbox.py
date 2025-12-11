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
    if platform.system().lower() != "windows":
        try:
            result = subprocess.check_output(["hostname", "-I"]).decode("utf-8")
            ips = result.strip().split(" ")
            ipv4_only = [ip for ip in ips if "." in ip]
            print(f"     Dina IP nummer: {ipv4_only}")
        except:
            return []
    else:
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
    typer("[3]. Change your mac-address" )
    typer("[4]. Placeholder" )
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
