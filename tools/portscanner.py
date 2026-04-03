import socket
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


def scan_port(target_ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1)
        result = s.connect_ex((target_ip, port))
        s.close()
        return port if result == 0 else None
    except socket.error:
        return None


def run():
    print("\n       --- P0RTSC4NN3R v1.0 ---")
    target = input("\nEnter the IP or URL you want to scan: ")
    print("\nAnge ett intervall som du vill scanna (ex 1-100). ")
    while True:
        try:
            from_port = int(input("Ange start: "))
            break
        except ValueError:
            print("[!] Ogiltigt värde. Ange ett heltal.")

    while True:
        try:
            to_port = int(input("Ange slut: "))
            break
        except ValueError:
            print("[!] Ogiltigt värde. Ange ett heltal.")

    if not (0 <= from_port <= 65535 and 0 <= to_port <= 65535):
        print("[!] Portintervallet måste vara inom 0–65535.")
        return

    if from_port > to_port:
        print("[!] Startport får inte vara högre än slutport.")
        return

    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print("\n[!] Couldn't find the address, did you enter it correctly?")
        input("Press Enter to exit...")
        return

    print(f"[+]...scanning {target_ip} ...")
    print(f"[+] Tid: {datetime.now()}")
    print("-" * 50)

    open_ports = []

    try:
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = {executor.submit(scan_port, target_ip, port): port for port in range(from_port, to_port + 1)}
            for future in as_completed(futures):
                result = future.result()
                if result is not None:
                    open_ports.append(result)

    except KeyboardInterrupt:
        print("\n\n[!] Du avbröt skanningen!")
        sys.exit()

    for port in sorted(open_ports):
        print(f"Port {port}: \t[ÖPPEN]")

    print("-" * 50)
    print("Skanning slutförd")
