import random
import subprocess
import psutil


def random_mac():
    """Genererar en slumpmässig MAC-adress med ett giltigt prefix."""
    return "02:%02x:%02x:%02x:%02x:%02x" % tuple(random.randint(0, 255) for _ in range(5))


def change_mac(interface, mac):
    """Spoofar MAC-adress för ett specifikt interface."""
    subprocess.run(["sudo", "ip", "link", "set", interface, "down"], check=True)
    subprocess.run(["sudo", "ip", "link", "set", interface, "address", mac], check=True)
    subprocess.run(["sudo", "ip", "link", "set", interface, "up"], check=True)


def get_interfaces():
    """Hämtar aktiva nätverksinterface (exkl. loopback)."""
    return [iface for iface in psutil.net_if_addrs() if iface != "lo"]


def run():
    print("\n=== MAC Spoof ===")

    interfaces = get_interfaces()
    if not interfaces:
        print("[!] Inga interface hittades.")
        return

    print("Välj interface:")
    for i, iface in enumerate(interfaces, 1):
        print(f"[{i}] {iface}")

    try:
        sel = int(input("Val: "))
        iface = interfaces[sel - 1]
    except Exception:
        print("[!] Ogiltigt val.")
        return

    new_mac = random_mac()
    print(f"[INFO] Ny MAC-adress ({iface}): {new_mac}")

    print("[INFO] Stoppar NetworkManager...")
    subprocess.run(["sudo", "systemctl", "stop", "NetworkManager"], check=True)

    print(f"[INFO] Ändrar MAC på {iface}...")
    try:
        change_mac(iface, new_mac)
    except subprocess.CalledProcessError as e:
        print(f"[!] Fel vid MAC-byte: {e}")
        subprocess.run(["sudo", "systemctl", "start", "NetworkManager"])
        return

    print("[INFO] Startar NetworkManager...")
    subprocess.run(["sudo", "systemctl", "start", "NetworkManager"], check=True)

    print(f"\n[+] MAC-adress spoofad på {iface}.")
    print(f"[+] Ny MAC: {new_mac}\n")
