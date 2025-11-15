import subprocess, shlex, re

def run_netdiscover(network_cidr):
    """
    Try to run netdiscover (if installed). Returns list of dicts {ip, mac, vendor}
    """
    cmd = f"netdiscover -r {network_cidr} -P -N"
    try:
        out = subprocess.check_output(shlex.split(cmd), stderr=subprocess.DEVNULL, text=True, timeout=8)
    except Exception:
        return []
    devices = []
    for line in out.splitlines():
        line = line.strip()
        # heuristic parse: looks for ip and mac
        m = re.search(r'(?P<ip>\d+\.\d+\.\d+\.\d+)\s+(?P<mac>([0-9a-f]{2}:){5}[0-9a-f]{2})\s+.*?(?P<vendor>[A-Za-z0-9\-\_ ]+)$', line, re.I)
        if m:
            devices.append({"ip": m.group("ip"), "mac": m.group("mac"), "vendor": m.group("vendor").strip()})
    return devices

def arp_scan_fallback(network_cidr="192.168.1.0/24", timeout=2):
    """
    Fallback to scapy ARP ping if netdiscover is missing.
    """
    try:
        from scapy.all import ARP, Ether, srp
    except Exception:
        return []
    pkt = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=network_cidr)
    ans, _ = srp(pkt, timeout=timeout, verbose=False)
    devices = []
    for _, r in ans:
        devices.append({"ip": r.psrc, "mac": r.hwsrc, "vendor": ""})
    return devices
