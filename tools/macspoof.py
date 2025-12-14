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

    choices = ["eth0", "wlan0"]
    print("Välj interface:")
    for i, c in enumerate(choices, 1):
        print(f"[{i}] {c}")

    try:
        sel = int(input("Val: "))
        iface = choices[sel - 1]
    except Exception:
        print("[!] Ogiltigt val.")
        return

    new_mac = random_mac()
    print(f"[INFO] Ny MAC-adress ({iface}): {new_mac}")

    print("[INFO] Stoppar NetworkManager...")
    os.system("sudo systemctl stop NetworkManager")

    print(f"[INFO] Ändrar MAC på {iface}...")
    change_mac(iface, new_mac)

    print("[INFO] Startar NetworkManager...")
    os.system("sudo systemctl start NetworkManager")

    print(f"\n[+] MAC-adress spoofad på {iface}.")
    print(f"[+] Ny MAC: {new_mac}\n")
