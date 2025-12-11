import os
import random


def random_mac():
    """Genererar en slumpmässig MAC-adress med ett giltigt prefix."""
    return "02:%02x:%02x:%02x:%02x:%02x" % tuple(random.randint(0, 255) for _ in range(5))


def change_mac(interface, mac):
    """Spoofar MAC-adress för ett specifikt interface."""
    os.system(f"sudo ip link set {interface} down")
    os.system(f"sudo ip link set {interface} address {mac}")
    os.system(f"sudo ip link set {interface} up")


def run():
    print("\n=== MAC Spoof ===")

    # 1. Generera slumpad MAC
    new_mac = random_mac()
    print(f"[INFO] Ny MAC-adress: {new_mac}")

    # 2. Stoppa NetworkManager
    print("[INFO] Stoppar NetworkManager...")
    os.system("sudo systemctl stop NetworkManager")

    # 3. Spoofa både eth0 och wlan0
    for iface in ["eth0", "wlan0"]:
        print(f"[INFO] Ändrar MAC på {iface}...")
        change_mac(iface, new_mac)

    # 4. Starta NetworkManager igen
    print("[INFO] Startar NetworkManager...")
    os.system("sudo systemctl start NetworkManager")

    print("\n[+] MAC-adress spoofad på eth0 och wlan0.")
    print(f"[+] Ny MAC: {new_mac}\n")