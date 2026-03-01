# Z-OSINT 🚀

**Ethical Bug Bounty Recon + Cookies/Session Extractor**

Advanced OSINT crawler that extracts **cookies**, **session tokens**, **emails**, **phones**, **subdomains** from websites. 100% Termux compatible.

## ✨ **Features**
- 🔍 **Cookie/Session ID Extraction** (PHPSESSID, JWT, auth tokens)
- 📧 **Email & Phone Regex** 
- 🌐 **Passive Subdomain Enum**
- 🕵️ **Stealth Mode** (silent scanning)
- 🎨 **Matrix Rain + Glitch Effects**
- 📊 **JSON Reports + Per-Page Cookies**
- ⚡ **Termux/Kali Ready**

## 🛠️ **Installation (Termux)**
```bash
pkg update && pkg install python requests beautifulsoup4 colorama
pip install requests beautifulsoup4 colorama
curl -O https://raw.githubusercontent.com/yourusername/z-osint/main/zosint.py
chmod +x zosint.py