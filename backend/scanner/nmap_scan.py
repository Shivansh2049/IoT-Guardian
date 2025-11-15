# backend/scanner/nmap_scan.py
import nmap

def nmap_scan_host(ip, profile="fast"):
    if profile=="fast":
        ports="1-200"; args="-sS -Pn -T2 --open"
    elif profile=="normal":
        ports="1-1024"; args="-sS -Pn -T3 --open"
    else:
        ports="1-65535"; args="-sS -Pn -T3 --open"
    nm = nmap.PortScanner()
    nm.scan(ip, ports, arguments=args)
    results=[]
    if ip in nm.all_hosts():
        for proto in nm[ip].all_protocols():
            for p in nm[ip][proto]:
                info = nm[ip][proto][p]
                results.append({"port": p, "state": info.get("state"), "service": info.get("name"), "version": info.get("version","")})
    return results
