#!/usr/bin/env python3
import os, re, time, socket, argparse, random, sys, json
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

init(autoreset=True)

# ================= CONFIG =================
DEFAULT_MAX_PAGES = 15
DEFAULT_DELAY = 1.2
TIMEOUT = 10
STEALTH_PASSWORD = "whitedevil"
USER_AGENT = "Z-OSINT (Ethical Bug Bounty Recon)"
STEALTH_MODE = False

COMMON_SUBS = [
    "www","api","dev","test","staging","beta","mail","blog","cdn",
    "shop","admin","static","img","assets","m"
]

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
PHONE_REGEX = r"(?:\+?\d{1,3}[\s\-]?)?(?:\(?\d{2,4}\)?[\s\-]?)?\d{3,4}[\s\-]?\d{3,4}"

# Cookie/Session ID patterns
SESSION_PATTERNS = [
    r'(?:session|SID|PHPSESSID|JSESSIONID|ASP.NET_SessionId|auth[_-]?token)[^=]*=[^;\s]+',
    r'[\w\-]{32,}|[A-F0-9]{32}|[a-zA-Z0-9\-_]{24,}',
    r'eyJ[A-Za-z0-9-_]+'
]
# =========================================


# ============== VISUAL EFFECTS ==============

def stealth_print(msg, color=Fore.GREEN):
    print((Style.DIM if STEALTH_MODE else "") + color + msg)

def stealth_dot():
    if STEALTH_MODE:
        sys.stdout.write(Fore.GREEN + ".")
        sys.stdout.flush()
        time.sleep(0.15)

def matrix_rain(duration=2):
    if STEALTH_MODE:
        return
    chars = "01▓▒░<>/\\@#$%"
    width = 80
    drops = [0]*width
    start = time.time()
    while time.time() - start < duration:
        line = ""
        for i in range(width):
            if random.random() > 0.97:
                drops[i] = 0
            line += random.choice(chars) if drops[i] < 15 else " "
            drops[i] += 1
        print(Fore.GREEN + line)
        time.sleep(0.04)

def glitch_text(text, cycles=3):
    if STEALTH_MODE:
        print(Fore.GREEN + text)
        return
    glitch = "!@#$%^&*<>?"
    for _ in range(cycles):
        out = "".join(c if random.random() > 0.25 else random.choice(glitch) for c in text)
        print(Fore.RED + out, end="\r")
        time.sleep(0.05)
    print(Fore.CYAN + text)

def neon_loading_bar(label="LOADING", duration=1.5, width=25):
    if STEALTH_MODE:
        stealth_print(f"[{label}]")
        return
    start = time.time()
    while time.time() - start < duration:
        filled = int(((time.time() - start) / duration) * width)
        bar = "▰"*filled + "▱"*(width-filled)
        sys.stdout.write(Fore.GREEN + Style.BRIGHT + f"\r[{label}] [{bar}]")
        sys.stdout.flush()
        time.sleep(0.05)
    print()

def red_glitch_warning(msg):
    if STEALTH_MODE:
        print(Fore.RED + Style.DIM + f"[!] {msg}")
        return
    glitch = "@#$%&01▓▒"
    for _ in range(4):
        corrupted = "".join(c if random.random() > 0.3 else random.choice(glitch) for c in msg)
        print(Fore.RED + Style.BRIGHT + corrupted)
        time.sleep(0.08)
    print(Fore.RED + Style.BRIGHT + f"[!] {msg}\n")

# ================= FIXED COOKIE EXTRACTOR =================

def extract_cookies(response):
    """Extract cookies - 100% COMPATIBLE WITH ALL REQUESTS VERSIONS"""
    cookies = {}

    # SAFEST WAY: Direct header access
    try:
        set_cookie = response.headers.get('Set-Cookie', '')
        if set_cookie:
            parts = set_cookie.split(';')[0].split('=', 1)
            if len(parts) == 2:
                name, value = parts
                cookies[name.strip()] = value.strip()
    except:
        pass

    # Response cookies jar (ALWAYS SAFE)
    try:
        if hasattr(response, 'cookies') and response.cookies:
            for name, cookie in response.cookies.items():
                if cookie.value:
                    cookies[name] = cookie.value
    except:
        pass

    return cookies

def extract_session_tokens(text):
    """Extract session tokens from page content"""
    tokens = set()
    try:
        for pattern in SESSION_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            tokens.update(matches)

        filtered = []
        for token in tokens:
            token = token.strip('";\'= ')
            if len(token) >= 20 and len(token) <= 500 and not token.isdigit():
                filtered.append(token)
        return filtered
    except:
        return []

# ===========================================

def banner():
    os.system("clear || cls")
    matrix_rain(1.5)
    glitch_text("""
███████╗ ██████╗       ██████╗  ███████╗██╗███╗   ██╗████████╗
╚══███╔╝██╔═══██╗     ██╔═══██╗ ██╔════╝██║████╗  ██║╚══██╔══╝
  ███╔╝ ██║   ██║     ██║   ██║ ███████╗██║██╔██╗ ██║   ██║
 ███╔╝  ██║   ██║     ██║   ██║ ╚════██║██║██║╚██╗██║   ██║
███████╗╚██████╔╝██╗  ╚██████╔╝ ███████║██║██║ ╚████║   ██║
╚══════╝ ╚═════╝ ╚═╝   ╚═════╝  ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝
""")
    stealth_print("Z-OSINT | Ethical Bug Bounty Recon w/ Cookies Extractor")
    stealth_print("Author: White_Devil\n", Fore.MAGENTA)

def login_gate():
    try:
        pwd = input(Fore.RED + "[STEALTH LOGIN] Password: ").strip()
    except KeyboardInterrupt:
        print("")
        exit(0)
    if pwd != STEALTH_PASSWORD:
        red_glitch_warning("UNAUTHORIZED ACCESS")
        matrix_rain(3)
        exit(1)
    stealth_print("[ACCESS GRANTED]\n")

def resolve_ip(host):
    try:
        return socket.gethostbyname(host)
    except:
        return "Unknown"

def safe_mkdir(p):
    try:
        if not os.path.exists(p):
            os.makedirs(p, exist_ok=True)
    except:
        pass

def fetch(url, delay):
    time.sleep(delay)
    try:
        r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT, allow_redirects=True)
        if r.status_code in (403, 429):
            red_glitch_warning(f"BLOCKED {r.status_code}")
            return None
        if r.status_code >= 400:
            return None
        return r
    except:
        return None

def parse_robots(base):
    disallowed = set()
    try:
        r = requests.get(urljoin(base, "/robots.txt"), timeout=TIMEOUT)
        if r and r.status_code == 200:
            for line in r.text.splitlines():
                if line.lower().startswith("disallow:"):
                    d = line.split(":",1)[1].strip()
                    if d:
                        disallowed.add(d)
    except:
        pass
    return disallowed

def allowed_by_robots(path, disallowed):
    for d in disallowed:
        if d == "/" or path.startswith(d.rstrip("*")):
            return False
    return True

def passive_subdomains(domain):
    found = {}
    for sub in COMMON_SUBS:
        try:
            h = f"{sub}.{domain}"
            ip = resolve_ip(h)
            if ip and ip != "Unknown":
                found[h] = ip
        except:
            pass
    return found

def crawl(start_url, max_pages, delay, do_subs):
    parsed = urlparse(start_url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    domain = parsed.netloc.replace('www.', '')

    out_dir = f"dump_{domain.replace(':', '_').replace('/', '_')}"
    safe_mkdir(out_dir)
    safe_mkdir(f"{out_dir}/html")
    safe_mkdir(f"{out_dir}/cookies")

    report = {
        "target": start_url,
        "base_domain": domain,
        "emails": [],
        "phones": [],
        "links": [],
        "pages": [],
        "subdomains": {},
        "cookies": {},
        "session_tokens": []
    }

    stealth_print(f"[+] Target: {start_url}")
    stealth_print(f"[+] Domain: {domain}")
    stealth_print(f"[+] IP: {resolve_ip(parsed.netloc)}")

    robots = parse_robots(base)
    if robots:
        stealth_print(f"[!] Robots.txt: {len(robots)} paths blocked", Fore.YELLOW)

    if do_subs:
        stealth_print("[*] Passive subdomain enum...")
        report["subdomains"] = passive_subdomains(domain)

    neon_loading_bar("SCAN START")

    visited = set()
    queue = [(start_url, 0)]
    total_cookies = 0
    total_tokens = 0

    while queue and len(visited) < max_pages:
        try:
            url, depth = queue.pop(0)
            if url in visited or depth > 3:
                continue
            if urlparse(url).netloc != parsed.netloc:
                continue

            path = urlparse(url).path or "/"
            if not allowed_by_robots(path, robots):
                continue

            r = fetch(url, delay)
            if not r:
                continue

            visited.add(url)
            report["pages"].append(url)
            page_num = len(visited)

            # SAVE HTML
            html_file = f"{out_dir}/html/page_{page_num}.html"
            try:
                with open(html_file, "w", encoding="utf-8", errors="ignore") as f:
                    f.write(r.text)
            except:
                pass

            # ========== COOKIES & TOKENS ==========
            page_cookies = extract_cookies(r)
            if page_cookies:
                report["cookies"][url] = page_cookies
                total_cookies += len(page_cookies)
                cookie_file = f"{out_dir}/cookies/page_{page_num}.json"
                try:
                    with open(cookie_file, "w") as cf:
                        json.dump(page_cookies, cf, indent=2)
                except:
                    pass

            tokens = extract_session_tokens(r.text)
            if tokens:
                for t in tokens:
                    if t not in report["session_tokens"]:
                        report["session_tokens"].append(t)
                total_tokens += len(tokens)
            # =====================================

            soup = BeautifulSoup(r.text, "html.parser")
            text = soup.get_text(" ", strip=True)

            emails = re.findall(EMAIL_REGEX, text)
            phones = re.findall(PHONE_REGEX, text)
            report["emails"].extend(emails)
            report["phones"].extend(phones)

            for a in soup.find_all("a", href=True):
                try:
                    clean = urljoin(base, urlparse(a["href"])._replace(query="", fragment="").geturl())
                    if clean not in report["links"]:
                        report["links"].append(clean)
                    if clean.startswith(base) and clean not in visited:
                        queue.append((clean, depth + 1))
                except:
                    pass

            if not STEALTH_MODE:
                stealth_print(f"[+] Page {page_num}/{max_pages}: {url}", Fore.GREEN)
            else:
                stealth_dot()

        except Exception as e:
            pass

    # SAVE REPORTS
    report_file = f"{out_dir}/report.json"
    try:
        clean_report = {
            "target": report["target"],
            "pages_crawled": len(report["pages"]),
            "total_cookies": total_cookies,
            "total_tokens": total_tokens,
            "emails": list(set(report["emails"])),
            "phones": list(set(report["phones"])),
            "links": report["links"][:100],  # Top 100
            "subdomains": report["subdomains"],
            "cookies_summary": {url: list(cookies.keys()) for url, cookies in list(report["cookies"].items())[:20]},
            "session_tokens": report["session_tokens"][:50]  # Top 50
        }
        with open(report_file, "w") as jf:
            json.dump(clean_report, jf, indent=2)
    except:
        pass

    # SUMMARY
    summary_file = f"{out_dir}/cookies_summary.txt"
    try:
        with open(summary_file, "w") as f:
            f.write(f"Z-OSINT SCAN RESULTS\n")
            f.write(f"Target: {start_url}\n")
            f.write(f"Pages: {len(visited)}\n")
            f.write(f"Cookies: {total_cookies}\n")
            f.write(f"Tokens: {total_tokens}\n\n")
            f.write("TOP COOKIES:\n")
            for url, cookies in list(report["cookies"].items())[:5]:
                f.write(f"{url}\n")
                for name, value in list(cookies.items())[:3]:
                    f.write(f"  {name}: {value[:30]}...\n")
                f.write("\n")
    except:
        pass

    stealth_print("\n" + "="*60, Fore.MAGENTA)
    stealth_print(f"[✓] COMPLETE - {out_dir}", Fore.MAGENTA)
    stealth_print(f"[✓] Pages: {len(visited)}", Fore.GREEN)
    stealth_print(f"[✓] Cookies: {total_cookies}", Fore.CYAN)
    stealth_print(f"[✓] Tokens: {total_tokens}", Fore.YELLOW)
    stealth_print(f"[✓] Report: {out_dir}/report.json", Fore.WHITE)

def main():
    global STEALTH_MODE
    banner()
    login_gate()

    parser = argparse.ArgumentParser(description="Z-OSINT - Ethical Recon + Cookies")
    parser.add_argument("--url", required=True)
    parser.add_argument("--max-pages", type=int, default=DEFAULT_MAX_PAGES)
    parser.add_argument("--delay", type=float, default=DEFAULT_DELAY)
    parser.add_argument("--subdomains", action="store_true")
    parser.add_argument("--stealth", action="store_true")
    args = parser.parse_args()

    STEALTH_MODE = args.stealth
    crawl(args.url, args.max_pages, args.delay, args.subdomains)

if __name__ == "__main__":
    main()