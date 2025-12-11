import psutil
import ipaddress
import subprocess


def get_networks():
    nets = []
    for iface, addrs in psutil.net_if_addrs().items():
        for a in addrs:
            if a.family == 2:
                ip = a.address
                mask = a.netmask
                if ip.startswith("127."):
                    continue
                try:
                    net = ipaddress.ip_network(f"{ip}/{mask}", strict=False)
                    nets.append((str(net), iface))
                except ValueError:
                    pass
    return nets


def run():
    print("\n=== Nmap Sweep ===")

    nets = get_networks()
    if not nets:
        print("[!] Inga nät hittades.")
        return

    if len(nets) == 1:
        cidr, iface = nets[0]
        print(f"Använder {cidr} ({iface})")
    else:
        print("Tillgängliga nätverk:")
        for i, (net, iface) in enumerate(nets, start=1):
            print(f"[{i}] {net} ({iface})")
        try:
            val = int(input("Välj nät: "))
            cidr, iface = nets[val - 1]
        except Exception:
            print("[!] Ogiltigt val.")
            return

    print(f"\nSkannar {cidr} med nmap -sn...\n")

    proc = subprocess.run(
        ["nmap", "-sn", cidr],
        capture_output=True,
        text=True
    )

    up_hosts = []
    for line in proc.stdout.splitlines():
        if line.startswith("Nmap scan report for "):
            host = line.replace("Nmap scan report for ", "").strip()
            up_hosts.append(host)

    for h in up_hosts:
        print(f"[+] {h} är aktiv")

    print(f"\nKlar. Hittade {len(up_hosts)} aktiva adresser.")
