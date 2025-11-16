# 🛡️ IoT Guardian

IoT Guardian is a full-stack network security scanner designed to detect IoT devices, analyze open ports, assess risk, and provide mitigation recommendations.

This tool allows users to:
- Scan a local network (CIDR input)
- Detect active hosts and open ports
- Calculate a risk score per device
- Display results in a modern UI dashboard
- Choose between Fast / Normal / Deep scanning profiles

---

## 🚀 Features
### **Backend (Flask + Nmap)**
- Runs `nmap` scans and parses results
- Risk scoring model
- Vendor lookup from MAC prefix
- Asynchronous background scanning
- REST API:
  - `POST /api/scan/start`
  - `GET /api/scan/status/<scan_id>`
  - `GET /api/scan/result/<scan_id>`

### **Frontend (React)**
- Modern dashboard UI
- Scan form + live scan status
- Results table with:
  - IP
  - MAC
  - Vendor
  - Open Ports
  - Risk Score
  - Recommendations

---

## 📦 Installation & Setup

### **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
python app.py
