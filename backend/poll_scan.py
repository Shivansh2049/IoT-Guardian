import time, requests, sys

if len(sys.argv) < 2:
    print("Usage: python poll_scan.py <scan_id>")
    sys.exit(1)

scan_id = sys.argv[1]
base = "http://127.0.0.1:5000"

for _ in range(120):  # try for ~10 minutes
    try:
        r = requests.get(f"{base}/api/scan/status/{scan_id}")
        if r.status_code != 200:
            print("Status error:", r.text)
            time.sleep(5)
            continue
        status = r.json().get("status")
        print(time.strftime("%X"), status)
        if status == "finished":
            out = requests.get(f"{base}/api/scan/result/{scan_id}")
            open("result.json", "wb").write(out.content)
            print("✅ Saved result.json")
            break
        if status and status.startswith("failed"):
            print("❌ Scan failed:", status)
            break
    except Exception as e:
        print("Error:", e)
    time.sleep(5)
else:
    print("⏰ Timed out waiting for scan.")
