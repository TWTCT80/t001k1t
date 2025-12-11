import time
import socket
import sys
from datetime import datetime


def pause():
    input("Pr3ss [3nter] t0 c0nt1nu3...")

def run():
    print("\n       --- P0RTSC4NN3R v1.0 ---")
    target = input("\nEnter the IP or URL you want to scan: ")
    print("\nAnge ett intervall som du vill scanna (ex 1-100). ")
    from_port = int(input("Ange start: "))
    to_port = int(input("Ange slut: "))
    
    

# Ändra URL till ip-nummer
    try: 
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print("\n[!] Couldn't find the address, did you enter it correctly?")
        input("Press Enter to exit...")
        return
    
    print(f"[+]...scanning {target_ip} ...")
    print(f"[+] Tid: {datetime.now()}")
    print("-" * 50)

    try:
        for port in range(from_port,to_port):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPV4, TCP
            s.settimeout(0.1)
            result = s.connect_ex((target_ip, port))

            if result == 0:
                print(f"Port {port}: \t[ÖPPEN]")
            
            s.close()
            

    except KeyboardInterrupt:
        # Om du vill ctrl + c för att avsluta
        print("\n\n[!] Du avbröt skanningen!")
        sys.exit()
    
    except socket.error:
        print("\n[!] Kunde inte ansluta ")

    print("-" * 50)
    print ("Skanning slutförd")
    
