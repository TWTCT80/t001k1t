import subprocess
import platform
from datetime import datetime

"""
def get_local_ips():
    if platform.system().lower() != "windows":
        try:
            result = subprocess.check_output(["hostname", "-I"]).decode("utf-8")
            ips = result.strip().split(" ")
            return ips
        except:
            return []
    else:
        return []
"""
#Hämta alla ip-adresser

def get_networks_from_route():
    networks = []
    
    # Detta funkar bara på Linux/Mac (Kali)
    if platform.system().lower() == "windows":
        return []

    try:
        # Kör kommandot 'ip route'
        output = subprocess.check_output(["ip", "route"]).decode("utf-8")
        
        # Gå igenom varje rad i resultatet
        for line in output.splitlines():
            parts = line.split(" ")
            
            # Vi vill inte ha "default" (internet-gateway)
            # Vi letar efter rader som ser ut som "192.168.56.0/24 dev eth1 ..."
            if "default" not in parts[0] and "/" in parts[0]:
                network_cidr = parts[0]   # T.ex. "192.168.56.0/24"
                interface = "okänd"
                
                # Hitta vilket interface det gäller (t.ex. eth0 eller eth1)
                if "dev" in parts:
                    dev_index = parts.index("dev") + 1
                    interface = parts[dev_index]
                
                networks.append((network_cidr, interface))
        print(networks)
        return networks

    except Exception as e:
        print(f"Kunde inte läsa ip route: {e}")
        return []





"""
def run():
    print("\n       --- P1NG SWEEP v1.0 ---")
    my_ips = get_local_ips()
    chosen_ip = ""

    #Alternativ för användaren
    if len(my_ips) > 0:
        print("\nDessa IP-adresser finns på din maskin:")
        for i, ip in enumerate(my_ips):
            print(f"[{i+1}] {ip}")
        
        print(f"[0] Skriv in manuellt")

        val = input("\nVilket nät vill du utgå ifrån? Ange siffra: ")

        try:
            val_int = int(val)
            if val_int > 0 and val_int <= len(my_ips):
                chosen_ip = my_ips[val_int -1]
        except ValueError:
            pass
"""    