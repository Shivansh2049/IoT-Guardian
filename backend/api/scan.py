# backend/api/scan.py
from flask import Blueprint, request, jsonify
import subprocess, threading, random, uuid, re

scan_bp = Blueprint("scan_bp", __name__)
scans = {}

# helper: parse nmap output (using python-nmap if available)
try:
    import nmap
    _HAVE_PYNMAP = True
except Exception:
    _HAVE_PYNMAP = False

def scan_ports_with_nmap(ip, profile="fast"):
    """
    Return list of dicts: [{"port": 22, "service": "ssh"}, ...]
    """
    results = []
    if _HAVE_PYNMAP:
        try:
            nm = nmap.PortScanner()
            if profile == "fast":
                ports = "1-200"
                args = "-sS -Pn -T2 --open"
            elif profile == "normal":
                ports = "1-1024"
                args = "-sS -Pn -T3 --open"
            else:
                ports = "1-65535"
                args = "-sS -Pn -T3 --open"

            nm.scan(ip, ports, arguments=args)
            if ip in nm.all_hosts():
                for proto in nm[ip].all_protocols():
                    for p in nm[ip][proto]:
                        info = nm[ip][proto][p]
                        results.append({
                            "port": int(p),
                            "service": info.get("name", "") or "",
                        })
            return results
        except Exception:
            # fall through to subprocess fallback
            pass

    # subprocess fallback parsing (grepable output)
    try:
        if profile == "fast":
            ports = "1-200"
            args = "-sS -Pn -T2 --open"
        elif profile == "normal":
            ports = "1-1024"
            args = "-sS -Pn -T3 --open"
        else:
            ports = "1-65535"
            args = "-sS -Pn -T3 --open"

        cmd = f"nmap {args} -p {ports} {ip} -oG -"
        out = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL, timeout=60)
        for line in out.splitlines():
            # Host: 192.168.1.10 ()  Ports: 22/open/tcp//ssh//,80/open/tcp//http// ...
            if line.startswith("Host:"):
                m = re.search(r"Ports:\s*(.*)$", line)
                if not m:
                    continue
                ports_str = m.group(1)
                for seg in ports_str.split(","):
                    seg = seg.strip()
                    pm = re.match(r'(\d+)\/(\w+)\/\w+\/\/([^\/]*)\/\/', seg)
                    if pm:
                        port = int(pm.group(1))
                        service = pm.group(3) or ""
                        results.append({"port": port, "service": service})
        return results
    except Exception:
        return []


def run_scan(network, profile="fast"):
    """
    Discovery (nmap -sn) then for each host, run port scan to fill open_ports.
    Returns a list of devices with open_ports.
    """
    # 1) discovery with nmap ping-scan (-sn)
    print(f"[SCAN] Starting discovery for {network}")
    devices = []
    try:
        out = subprocess.check_output(["nmap", "-sn", network], text=True, stderr=subprocess.DEVNULL, timeout=60)
        print("[SCAN] Discovery output received")
    except Exception as e:
        # If discovery fails, return empty list
        print("Discovery failed:", e)
        return devices

    current_ip = None
    for line in out.splitlines():
        if "Nmap scan report for" in line:
            parts = line.split()
            current_ip = parts[-1]
        elif "MAC Address" in line and current_ip:
            # "MAC Address: 00:11:22:33:44:55 (Vendor Name)"
            parts = line.split()
            mac = parts[2]
            # vendor parse (if present in parentheses)
            vendor = ""
            m = re.search(r'\((.*?)\)', line)
            if m:
                vendor = m.group(1)
            # do a ports scan per-host
            open_ports = scan_ports_with_nmap(current_ip, profile=profile)
            devices.append({
                "ip": current_ip,
                "mac": mac,
                "vendor": vendor,
                "open_ports": open_ports,   # GUARANTEED field
                "risk": round(random.uniform(1.0, 10.0), 2),
                "recommendation": random.choice([
                    "Update firmware",
                    "Change default password",
                    "Disable unused services",
                    "Monitor network traffic"
                ])
            })
            current_ip = None

    return devices


def start_scan(scan_id, network, profile="fast"):
    scans[scan_id] = {"status": "started", "devices": []}

    def worker():
        print(f"[THREAD] Worker started for scan {scan_id}")
        try:
            data = run_scan(network, profile=profile)
            print(f"[THREAD] Found {len(data)} devices — marking finished")
            scans[scan_id] = {"status": "finished", "devices": data}
        except Exception as e:
            scans[scan_id] = {"status": f"failed: {e}"}
            print("[ERROR] Worker failed:", e)

    threading.Thread(target=worker, daemon=True).start()


@scan_bp.route("/scan/start", methods=["POST"])
def api_start_scan():
    data = request.get_json(force=True)
    network = data.get("network", "127.0.0.1/32")
    profile = data.get("profile", "fast")
    scan_id = f"scan-{uuid.uuid4().hex[:8]}"
    start_scan(scan_id, network, profile)
    return jsonify({"scan_id": scan_id, "status": "started"}), 202


@scan_bp.route("/scan/status/<scan_id>")
def api_scan_status(scan_id):
    return jsonify(scans.get(scan_id, {"status": "unknown"}))


@scan_bp.route("/scan/result/<scan_id>")
def api_scan_result(scan_id):
    s = scans.get(scan_id)
    if not s or s["status"] != "finished":
        return jsonify({"error": "result not ready"})
    # normalize to frontend expected format: { results: [...] }
    return jsonify({"status": s["status"], "results": s["devices"]})

