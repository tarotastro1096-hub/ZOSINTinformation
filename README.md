# Z-OSINT 
## Cloé Sim

[![Go](https://img.shields.io/badge/go-%2300ADD8.svg?style=for-the-badge&logo=go&logoColor=white)](https://golang.org/) [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/) [![Apache](https://img.shields.io/badge/apache-%23D42029.svg?style=for-the-badge&logo=apache&logoColor=white)](https://www.apache.org/) [![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/) [![CodePen](https://img.shields.io/badge/Codepen-000000?style=for-the-badge&logo=codepen&logoColor=white)](https://codepen.io/) [![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://www.microsoft.com/fr-ca/windows) [![PowerShell](https://img.shields.io/badge/PowerShell-%235391FE.svg?style=for-the-badge&logo=powershell&logoColor=white)](https://learn.microsoft.com/fr-ca/powershell/) [![Debian](https://img.shields.io/badge/Debian-D70A53?style=for-the-badge&logo=debian&logoColor=white)](https://www.debian.org/) [![Kali](https://img.shields.io/badge/Kali-268BEE?style=for-the-badge&logo=kalilinux&logoColor=white)](https://www.kali.org/) [![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)](https://www.linux.org/) [![Red Hat](https://img.shields.io/badge/Red%20Hat-EE0000?style=for-the-badge&logo=redhat&logoColor=white)](https://www.redhat.com/fr) [![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com/) [![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=Raspberry%20Pi&logoColor=white)](https://www.raspberrypi.com/) [![Git](https://img.shields.io/badge/GIT-E44C30?style=for-the-badge&logo=git&logoColor=white)](https://git-scm.com/) [![PowerShell](https://img.shields.io/badge/powershell-5391FE?style=for-the-badge&logo=powershell&logoColor=white)](https://learn.microsoft.com/fr-ca/powershell/) [![Visual Studio](https://img.shields.io/badge/Visual_Studio-5C2D91?style=for-the-badge&logo=visual%20studio&logoColor=white)](https://visualstudio.microsoft.com/)

<p align="center">
  <a href="https://www.womentech.net/"><img src="https://github.com/user-attachments/assets/58836009-9b43-453c-8627-1c62ab517db6" alt="Women in Tech" height="40"/></a>
  <a href="https://developers.google.com/"><img src="https://github.com/user-attachments/assets/457e1ddc-353e-4f03-b967-5c5a13fa73eb" alt="Google Developer" height="40"/></a>
</p>
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
