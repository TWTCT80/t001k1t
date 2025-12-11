# Detta blir basen i mitt projekt, själva menyn där man väljer vilket verktyg man vill använda.

#!/usr/bin/env python3

import os
import sys
import time
#from tools import portscanner

# --- Funktion för att skriva ett tecken i taget ---

def typer(text, delay=0.03):
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
          
                  CYBER SECURITY TOOLKIT
                         MAIN MENU
           """)
    typer("[1]. Portscanner")
    typer("[2]. Placeholder" )
    typer("[3]. Placeholder" )
    typer("[4]. Placeholder" )
    typer("[0]. Exit")    

def main():
    while True:
        clrscr()  # --- RENSA SKÄRMEN --- 
        menu()
        val = input("Ch00s3 yu0r t001: ")

        if val == "1":
            #portscanner.run()
            typer(" --- Starting Portscanner --- ")
            pause()
        elif val == "2":
            #Placeholder
            pass
        elif val == "3":
            #Placeholder
            pass
        elif val == "0":
            typer("\n --- EXITING ---")
            time.sleep(1)
            sys.exit()
        else:
            typer("Wr0ng 1nput, Try Ag61n: ")




main()
