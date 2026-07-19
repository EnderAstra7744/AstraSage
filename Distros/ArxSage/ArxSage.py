#ArxSage • By:EnderAstra
#AstraSage Mini Distro - Siber Güvenlik ve Etik Hackerlık Terminali

import os
import sys
import time
import platform
import socket
import hashlib
import datetime
import ssl
import urllib.request
import urllib.error
import importlib.util
import importlib

#ArxSage kök dizini
ASTRASAGE_KOK = os.getcwd()  # AstraSage'in gerçek kök dizini, hiç değişmez
ARX_KOK = os.path.dirname(os.path.abspath(__file__))
ASTRASAGE_KOK = os.path.dirname(os.path.dirname(ARX_KOK))

arx_mevcut_dizin = [os.getcwd()]

class ArxRenk:
    KIRMIZI = "\033[91m"
    KOYU_KIRMIZI = "\033[31m"
    BEYAZ = "\033[97m"
    GRI = "\033[90m"
    YESIL = "\033[92m"
    SARI = "\033[93m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

LOGO = """
  ⣆⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
  ⠙⠻⢷⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀
  ⠀⠀⠀⠉⠛⢷⣦⠀⠀⠀⠀⠀⠀
  ⠀⠀⣠⣤⡾⠟⠋⠀⠀⠀⠀⠀⠀
  ⣶⡿⠟⠉⠀⠀⠀⣤⣤⣤⣤⣤⣤⣤⣤⣤
  ⠁⠀⠀⠀⠀⠀⠀⠛⠛⠛⠛⠛⠛⠛⠛⠛
"""

def arxsage_banner():
    print(ArxRenk.KIRMIZI + LOGO + ArxRenk.RESET)
    print(ArxRenk.BOLD + ArxRenk.KIRMIZI + "ArxSage" + ArxRenk.RESET + " • AstraSage Security Distro")
    print("")
    print("=" * 45)
    print(f"\n{ArxRenk.KIRMIZI}Komut Kategorileri:{ArxRenk.RESET}")
    print(f"  {ArxRenk.BEYAZ}arx help{ArxRenk.RESET}          → tüm komutlar")
    print(f"  {ArxRenk.BEYAZ}arx net ...{ArxRenk.RESET}       → ağ araçları")
    print(f"  {ArxRenk.BEYAZ}arx file ...{ArxRenk.RESET}      → dosya analizi")
    print(f"  {ArxRenk.BEYAZ}arx crypto ...{ArxRenk.RESET}    → şifreleme araçları")
    print(f"  {ArxRenk.BEYAZ}arx info ...{ArxRenk.RESET}      → bilgi toplama")
    print(f"  {ArxRenk.BEYAZ}arx return -AstraSage{ArxRenk.RESET} → geri dön")
    print("=" * 45)
    print("")


def arx_clear():
    os.system("clear")


# ==================== AĞ ARAÇLARI ====================

def arx_ping(hedef):
    """Hedefe ping atar."""
    print(f"\n{ArxRenk.SARI}[ArxSage/Net] Ping: {hedef}{ArxRenk.RESET}")
    try:
        ip = socket.gethostbyname(hedef)
        print(f"IP Adresi  : {ip}")
        sonuc = os.system(f"ping -c 4 {ip} 2>/dev/null || ping -n 4 {ip} 2>/dev/null")
        if sonuc != 0:
            print(f"[BİLGİ] Ping komutu bu ortamda desteklenmiyor olabilir.")
    except socket.gaierror:
        print(f"[HATA] '{hedef}' çözümlenemedi.")


def arx_port_tara(hedef, baslangic=1, bitis=1024):
    """Belirtilen aralıktaki portları tarar."""
    print(f"\n{ArxRenk.SARI}[ArxSage/Net] Port Tarama: {hedef} ({baslangic}-{bitis}){ArxRenk.RESET}")
    print(ArxRenk.GRI + "Bu işlem biraz sürebilir..." + ArxRenk.RESET)

    try:
        ip = socket.gethostbyname(hedef)
        print(f"Hedef IP   : {ip}")
        print("-" * 35)

        acik_portlar = []
        for port in range(baslangic, bitis + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3)
            sonuc = sock.connect_ex((ip, port))
            if sonuc == 0:
                acik_portlar.append(port)
                print(f"{ArxRenk.YESIL}[AÇIK] Port {port}{ArxRenk.RESET}")
            sock.close()

        print("-" * 35)
        if acik_portlar:
            print(f"Toplam {len(acik_portlar)} açık port bulundu.")
        else:
            print("Açık port bulunamadı.")

    except socket.gaierror:
        print(f"[HATA] '{hedef}' çözümlenemedi.")
    except Exception as hata:
        print(f"[HATA] {hata}")


def arx_dns(hedef):
    """DNS sorgusu yapar."""
    print(f"\n{ArxRenk.SARI}[ArxSage/Net] DNS Sorgusu: {hedef}{ArxRenk.RESET}")
    try:
        ip = socket.gethostbyname(hedef)
        print(f"IP Adresi  : {ip}")
        try:
            ters = socket.gethostbyaddr(ip)
            print(f"Ters DNS   : {ters[0]}")
        except Exception:
            print(f"Ters DNS   : Bulunamadı")
    except socket.gaierror:
        print(f"[HATA] '{hedef}' çözümlenemedi.")


def arx_myip():
    """Cihazın yerel IP adresini gösterir."""
    print(f"\n{ArxRenk.SARI}[ArxSage/Net] Ağ Bilgisi{ArxRenk.RESET}")
    try:
        hostname = socket.gethostname()
        print(f"Cihaz Adı  : {hostname}")
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)
        s.connect(("8.8.8.8", 80))
        yerel_ip = s.getsockname()[0]
        s.close()
        print(f"Yerel IP   : {yerel_ip}")
        print(f"Bağlantı   : İnternet bağlantısı var")
    except Exception:
        print(f"Yerel IP   : Alınamadı")
        print(f"Bağlantı   : İnternet yok veya erişilemiyor")


# ==================== DOSYA ANALİZİ ====================

def arx_hash(dosya_yolu, algoritma="sha256"):
    """Dosyanın hash değerini hesaplar."""
    print(f"\n{ArxRenk.SARI}[ArxSage/File] Hash: {dosya_yolu} ({algoritma}){ArxRenk.RESET}")

    if not os.path.exists(dosya_yolu):
        print(f"[HATA] '{dosya_yolu}' bulunamadı.")
        return

    try:
        h = hashlib.new(algoritma)
        with open(dosya_yolu, "rb") as f:
            while True:
                blok = f.read(8192)
                if not blok:
                    break
                h.update(blok)

        print(f"{algoritma.upper()}: {h.hexdigest()}")
    except ValueError:
        print(f"[HATA] '{algoritma}' desteklenmiyor. (md5, sha1, sha256, sha512)")
    except Exception as hata:
        print(f"[HATA] {hata}")


def arx_meta(dosya_yolu):
    """Dosyanın meta verilerini gösterir."""
    print(f"\n{ArxRenk.SARI}[ArxSage/File] Meta Veri: {dosya_yolu}{ArxRenk.RESET}")

    if not os.path.exists(dosya_yolu):
        print(f"[HATA] '{dosya_yolu}' bulunamadı.")
        return

    try:
        stat = os.stat(dosya_yolu)
        boyut = stat.st_size
        boyut_str = f"{boyut} byte" if boyut < 1024 else f"{boyut/1024:.2f} KB" if boyut < 1024*1024 else f"{boyut/(1024*1024):.2f} MB"

        print(f"Boyut      : {boyut_str}")
        print(f"Oluşturma  : {datetime.datetime.fromtimestamp(stat.st_ctime).strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Değişiklik : {datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Tam Yol    : {os.path.abspath(dosya_yolu)}")

        _, uzanti = os.path.splitext(dosya_yolu)
        print(f"Uzantı     : {uzanti if uzanti else 'yok'}")

        if os.path.isfile(dosya_yolu):
            try:
                with open(dosya_yolu, "r", encoding="utf-8") as f:
                    satirlar = f.readlines()
                print(f"Satır      : {len(satirlar)}")
            except Exception:
                print(f"Satır      : (binary dosya)")

    except Exception as hata:
        print(f"[HATA] {hata}")


def arx_scan(dosya_yolu):
    """AstraSecurity ile dosya tarar."""
    print(f"\n{ArxRenk.SARI}[ArxSage/File] Güvenlik Taraması: {dosya_yolu}{ArxRenk.RESET}")
    try:
        if ASTRASAGE_KOK not in sys.path:
            sys.path.insert(0, ASTRASAGE_KOK)
        from utils.astra_security import tara
        sonuc = tara(dosya_yolu)
        if sonuc:
            print(f"{ArxRenk.YESIL}Dosya temiz.{ArxRenk.RESET}")
        else:
            print(f"{ArxRenk.KIRMIZI}Tehlikeli kod tespit edildi!{ArxRenk.RESET}")
    except Exception as hata:
        print(f"[HATA] Tarama başarısız: {hata}")


# ==================== ŞİFRELEME ARAÇLARI ====================

def arx_hash_metin(metin, algoritma="sha256"):
    """Bir metni hashler."""
    print(f"\n{ArxRenk.SARI}[ArxSage/Crypto] Metin Hash ({algoritma}){ArxRenk.RESET}")
    try:
        h = hashlib.new(algoritma)
        h.update(metin.encode("utf-8"))
        print(f"Girdi      : {metin}")
        print(f"{algoritma.upper()}: {h.hexdigest()}")
    except ValueError:
        print(f"[HATA] '{algoritma}' desteklenmiyor. (md5, sha1, sha256, sha512)")


def arx_encode(metin):
    """Metni Base64 ile kodlar."""
    import base64
    print(f"\n{ArxRenk.SARI}[ArxSage/Crypto] Base64 Kodlama{ArxRenk.RESET}")
    kodlu = base64.b64encode(metin.encode("utf-8")).decode("utf-8")
    print(f"Girdi      : {metin}")
    print(f"Base64     : {kodlu}")


def arx_decode(kodlu_metin):
    """Base64 kodlu metni çözer."""
    import base64
    print(f"\n{ArxRenk.SARI}[ArxSage/Crypto] Base64 Çözme{ArxRenk.RESET}")
    try:
        cozulmus = base64.b64decode(kodlu_metin.encode("utf-8")).decode("utf-8")
        print(f"Girdi      : {kodlu_metin}")
        print(f"Çözüldü    : {cozulmus}")
    except Exception:
        print(f"[HATA] Geçersiz Base64 verisi.")


# ==================== BİLGİ TOPLAMA ====================

def arx_sysinfo():
    """Sistem bilgisi gösterir."""
    print(f"\n{ArxRenk.SARI}[ArxSage/Info] Sistem Bilgisi{ArxRenk.RESET}")
    print("-" * 35)
    print(f"Sistem     : {platform.system()}")
    print(f"Sürüm      : {platform.release()}")
    print(f"Makine     : {platform.machine()}")
    print(f"İşlemci    : {platform.processor()}")
    print(f"Python     : {sys.version.split()[0]}")
    print(f"Düğüm      : {platform.node()}")
    print(f"Bit        : {platform.architecture()[0]}")
    print(f"Distro     : ArxSage (AstraSage üzerinde)")
    print("-" * 35)


def arx_whoami():
    """Mevcut kullanıcı bilgisini gösterir."""
    print(f"\n{ArxRenk.SARI}[ArxSage/Info] Kullanıcı Bilgisi{ArxRenk.RESET}")
    try:
        import getpass
        print(f"Kullanıcı  : {getpass.getuser()}")
        print(f"Ev Dizini  : {os.path.expanduser('~')}")
    except Exception:
        print(f"Kullanıcı  : Alınamadı")
    print(f"Cihaz      : {platform.node()}")


# ==================== DOSYA SİSTEMİ ====================

def arx_ls(hedef=None):
    hedef = hedef or arx_mevcut_dizin[0]
    try:
        icerik = os.listdir(hedef)
        if not icerik:
            print("(boş klasör)")
            return
        for item in sorted(icerik):
            tam_yol = os.path.join(hedef, item)
            if os.path.isdir(tam_yol):
                print(f"{ArxRenk.KIRMIZI}[K] {item}/{ArxRenk.RESET}")
            else:
                print(f"    {item}")
    except Exception as hata:
        print(f"[HATA] {hata}")


def arx_cd(hedef):
    if hedef == "..":
        yeni = os.path.dirname(arx_mevcut_dizin[0])
    else:
        yeni = os.path.join(arx_mevcut_dizin[0], hedef)
    if not os.path.isdir(yeni):
        print(f"[HATA] '{hedef}' bulunamadı.")
        return
    arx_mevcut_dizin[0] = yeni
    print(f"→ {arx_mevcut_dizin[0]}")

# ==================== ETİK HACKER ARAÇLARI ====================

def arx_whois(domain):
    """Whois sorgusu yapar."""
    print(f"\n{ArxRenk.SARI}[ArxSage/Recon] Whois: {domain}{ArxRenk.RESET}")
    try:
        # Whois sunucusuna bağlan
        whois_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        whois_socket.settimeout(10)
        whois_socket.connect(("whois.iana.org", 43))
        whois_socket.send(f"{domain}\r\n".encode())
        
        cevap = b""
        while True:
            veri = whois_socket.recv(4096)
            if not veri:
                break
            cevap += veri
        whois_socket.close()
        
        # İlgili satırları filtrele
        satirlar = cevap.decode("utf-8", errors="ignore").splitlines()
        for satir in satirlar:
            if any(k in satir.lower() for k in ["domain", "registrar", "creation", "expir", "name server", "status", "whois"]):
                print(f"  {satir.strip()}")
    
    except Exception as hata:
        print(f"[HATA] Whois sorgusu başarısız: {hata}")


def arx_subdomain(domain):
    """Yaygın subdomain'leri kontrol eder."""
    print(f"\n{ArxRenk.SARI}[ArxSage/Recon] Subdomain Tarama: {domain}{ArxRenk.RESET}")
    print(ArxRenk.GRI + "Yaygın subdomain'ler kontrol ediliyor..." + ArxRenk.RESET)
    print("-" * 35)

    YAYGIN_SUBDOMAINLER = [
        "www", "mail", "ftp", "smtp", "pop", "imap",
        "api", "dev", "test", "staging", "admin",
        "blog", "shop", "store", "app", "mobile",
        "cdn", "static", "media", "img", "images",
        "vpn", "remote", "portal", "secure", "login",
        "m", "ns1", "ns2", "dns", "mx", "webmail",
    ]

    bulunanlar = []
    for sub in YAYGIN_SUBDOMAINLER:
        hedef = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(hedef)
            bulunanlar.append((hedef, ip))
            print(f"{ArxRenk.YESIL}[BULUNDU] {hedef:<35} → {ip}{ArxRenk.RESET}")
        except socket.gaierror:
            pass  # Bulunamadı, sessizce geç

    print("-" * 35)
    if bulunanlar:
        print(f"Toplam {len(bulunanlar)} subdomain bulundu.")
    else:
        print("Hiçbir subdomain bulunamadı.")


def arx_http_headers(url):
    """Web sitesinin HTTP güvenlik başlıklarını analiz eder."""
    print(f"\n{ArxRenk.SARI}[ArxSage/Recon] HTTP Başlık Analizi: {url}{ArxRenk.RESET}")

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    GUVENLIK_BASLIKLARI = {
        "Strict-Transport-Security": "HSTS - HTTPS zorlaması",
        "Content-Security-Policy": "XSS ve injection koruması",
        "X-Frame-Options": "Clickjacking koruması",
        "X-Content-Type-Options": "MIME sniffing koruması",
        "X-XSS-Protection": "XSS filtresi",
        "Referrer-Policy": "Referrer bilgisi kontrolü",
        "Permissions-Policy": "Tarayıcı izin politikası",
        "Server": "Sunucu bilgisi (gizlenmiş olmalı)",
    }

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ArxSage/1.0"})
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        with urllib.request.urlopen(req, context=context, timeout=10) as response:
            basliklar = dict(response.headers)
            print(f"Durum Kodu : {response.status}")
            print("-" * 45)

            print(f"\n{ArxRenk.SARI}Güvenlik Başlıkları:{ArxRenk.RESET}")
            for baslik, aciklama in GUVENLIK_BASLIKLARI.items():
                deger = basliklar.get(baslik) or basliklar.get(baslik.lower())
                if deger:
                    print(f"{ArxRenk.YESIL}  [VAR]    {baslik}{ArxRenk.RESET}")
                    print(f"           {aciklama}")
                    print(f"           Değer: {deger[:80]}")
                else:
                    print(f"{ArxRenk.KIRMIZI}  [EKSİK]  {baslik}{ArxRenk.RESET}")
                    print(f"           {aciklama}")

    except urllib.error.URLError as hata:
        print(f"[HATA] Bağlantı kurulamadı: {hata}")
    except Exception as hata:
        print(f"[HATA] {hata}")


def arx_ssl(domain):
    """SSL/TLS sertifikasını analiz eder."""
    print(f"\n{ArxRenk.SARI}[ArxSage/Recon] SSL/TLS Sertifika: {domain}{ArxRenk.RESET}")

    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                sertifika = ssock.getpeercert()
                protokol = ssock.version()
                sifreler = ssock.cipher()

        print(f"Protokol   : {protokol}")
        print(f"Şifre      : {sifreler[0] if sifreler else 'Bilinmiyor'}")
        print("-" * 35)

        # Konu bilgisi
        konu = dict(x[0] for x in sertifika.get("subject", []))
        print(f"Domain     : {konu.get('commonName', 'Bilinmiyor')}")
        print(f"Kuruluş    : {konu.get('organizationName', 'Bilinmiyor')}")

        # Veren
        veren = dict(x[0] for x in sertifika.get("issuer", []))
        print(f"Veren      : {veren.get('organizationName', 'Bilinmiyor')}")

        # Geçerlilik
        bitis = sertifika.get("notAfter", "Bilinmiyor")
        print(f"Son Geçerlilik: {bitis}")

        # Alternatif isimler
        san = sertifika.get("subjectAltName", [])
        if san:
            print(f"\nAlt. İsimler ({len(san)}):")
            for tip, deger in san[:5]:
                print(f"  {tip}: {deger}")
            if len(san) > 5:
                print(f"  ... ve {len(san)-5} tane daha")

    except ssl.SSLError as hata:
        print(f"[HATA] SSL hatası: {hata}")
    except ConnectionRefusedError:
        print(f"[HATA] Port 443 kapalı veya bağlantı reddedildi.")
    except Exception as hata:
        print(f"[HATA] {hata}")
# ==================== YARDIM ====================

def arx_help():
    print(f"\n{ArxRenk.KIRMIZI}{'='*45}")
    print(f"  ArxSage Komut Listesi")
    print(f"{'='*45}{ArxRenk.RESET}")

    print(f"\n{ArxRenk.SARI}[ Ağ Araçları ]{ArxRenk.RESET}")
    print("  arx net ping <hedef>              → ping at")
    print("  arx net portscan <hedef> <b> <s>  → port tara")
    print("  arx net dns <hedef>               → DNS sorgula")
    print("  arx net myip                      → IP bilgisi")

    print(f"\n{ArxRenk.SARI}[ Dosya Analizi ]{ArxRenk.RESET}")
    print("  arx file hash <dosya> <algoritma> → hash hesapla")
    print("  arx file meta <dosya>             → meta veri")
    print("  arx file scan <dosya>             → güvenlik tara")

    print(f"\n{ArxRenk.SARI}[ Şifreleme ]{ArxRenk.RESET}")
    print("  arx crypto hash <metin> <algo>    → metin hashle")
    print("  arx crypto encode <metin>         → Base64 kodla")
    print("  arx crypto decode <metin>         → Base64 çöz")

    print(f"\n{ArxRenk.SARI}[ Bilgi Toplama ]{ArxRenk.RESET}")
    print("  arx info sys                      → sistem bilgisi")
    print("  arx info whoami                   → kullanıcı bilgisi")

    print(f"\n{ArxRenk.SARI}[ Genel ]{ArxRenk.RESET}")
    print("  arx ls <klasör>                   → dizin listele")
    print("  arx cd <klasör>                   → dizin değiştir")
    print("  arx pwd                           → mevcut dizin")
    print("  arx clear                         → ekranı temizle")
    print("  arx return -<Distro/AstraSage>    → geri dön")
    
    print(f"\n{ArxRenk.SARI}[ Keşif / Recon ]{ArxRenk.RESET}")
    print("  arx recon whois <domain>          → domain bilgisi")
    print("  arx recon subdomain <domain>      → subdomain tara")
    print("  arx recon headers <url>           → HTTP başlık analizi")
    print("  arx recon ssl <domain>            → SSL sertifika analizi")
    print(f"\n{ArxRenk.KIRMIZI}{'='*45}{ArxRenk.RESET}")

# ==================== ANA DÖNGÜ ====================

def run():
    arx_clear()
    arxsage_banner()

    while True:
        try:
            komut = input(f"\n{ArxRenk.KIRMIZI}arx@ArxSage:{ArxRenk.RESET}{arx_mevcut_dizin[0]}# ")
            parcalar = komut.strip().split()

            if not parcalar:
                continue
            if parcalar[0] != "arx":
                print(f"[HATA] ArxSage komutları 'arx' ile başlamalı.")
                continue

            if len(parcalar) < 2:
                arx_help()
                continue

            kategori = parcalar[1]

            # --- NET ---
            if kategori == "net":
                if len(parcalar) < 3:
                    print("Kullanım: arx net <ping|portscan|dns|myip> ...")
                    continue
                alt = parcalar[2]
                if alt == "ping":
                    if len(parcalar) < 4: print("Kullanım: arx net ping <hedef>"); continue
                    arx_ping(parcalar[3])
                elif alt == "portscan":
                    if len(parcalar) < 4: print("Kullanım: arx net portscan <hedef> [başlangıç] [bitiş]"); continue
                    b = int(parcalar[4]) if len(parcalar) >= 5 else 1
                    s = int(parcalar[5]) if len(parcalar) >= 6 else 1024
                    arx_port_tara(parcalar[3], b, s)
                elif alt == "dns":
                    if len(parcalar) < 4: print("Kullanım: arx net dns <hedef>"); continue
                    arx_dns(parcalar[3])
                elif alt == "myip":
                    arx_myip()
                else:
                    print(f"[HATA] '{alt}' tanımlı değil.")
                    
            # --- RECON ---
            elif kategori == "recon":
                if len(parcalar) < 3:
                    print("Kullanım: arx recon <whois|subdomain|headers|ssl> ...")
                    continue
                alt = parcalar[2]
                if alt == "whois":
                    if len(parcalar) < 4: print("Kullanım: arx recon whois <domain>"); continue
                    arx_whois(parcalar[3])
                elif alt == "subdomain":
                    if len(parcalar) < 4: print("Kullanım: arx recon subdomain <domain>"); continue
                    arx_subdomain(parcalar[3])
                elif alt == "headers":
                    if len(parcalar) < 4: print("Kullanım: arx recon headers <url>"); continue
                    arx_http_headers(parcalar[3])
                elif alt == "ssl":
                    if len(parcalar) < 4: print("Kullanım: arx recon ssl <domain>"); continue
                    arx_ssl(parcalar[3])
                else:
                    print(f"[HATA] '{alt}' tanımlı değil.")
            # --- FILE ---
            elif kategori == "file":
                if len(parcalar) < 3:
                    print("Kullanım: arx file <hash|meta|scan> ...")
                    continue
                alt = parcalar[2]
                if alt == "hash":
                    if len(parcalar) < 4: print("Kullanım: arx file hash <dosya> [algoritma]"); continue
                    algo = parcalar[4] if len(parcalar) >= 5 else "sha256"
                    arx_hash(parcalar[3], algo)
                elif alt == "meta":
                    if len(parcalar) < 4: print("Kullanım: arx file meta <dosya>"); continue
                    arx_meta(parcalar[3])
                elif alt == "scan":
                    if len(parcalar) < 4: print("Kullanım: arx file scan <dosya>"); continue
                    arx_scan(parcalar[3])
                else:
                    print(f"[HATA] '{alt}' tanımlı değil.")

            # --- CRYPTO ---
            elif kategori == "crypto":
                if len(parcalar) < 3:
                    print("Kullanım: arx crypto <hash|encode|decode> ...")
                    continue
                alt = parcalar[2]
                if alt == "hash":
                    if len(parcalar) < 4: print("Kullanım: arx crypto hash <metin> [algoritma]"); continue
                    metin = parcalar[3]
                    algo = parcalar[4] if len(parcalar) >= 5 else "sha256"
                    arx_hash_metin(metin, algo)
                elif alt == "encode":
                    if len(parcalar) < 4: print("Kullanım: arx crypto encode <metin>"); continue
                    arx_encode(" ".join(parcalar[3:]))
                elif alt == "decode":
                    if len(parcalar) < 4: print("Kullanım: arx crypto decode <metin>"); continue
                    arx_decode(parcalar[3])
                else:
                    print(f"[HATA] '{alt}' tanımlı değil.")

            # --- INFO ---
            elif kategori == "info":
                if len(parcalar) < 3:
                    print("Kullanım: arx info <sys|whoami>")
                    continue
                alt = parcalar[2]
                if alt == "sys":
                    arx_sysinfo()
                elif alt == "whoami":
                    arx_whoami()
                else:
                    print(f"[HATA] '{alt}' tanımlı değil.")

            # --- GENEL ---
            elif kategori == "help":
                arx_help()
            elif kategori == "ls":
                hedef = parcalar[2] if len(parcalar) >= 3 else None
                arx_ls(hedef)
            elif kategori == "cd":
                if len(parcalar) < 3: print("Kullanım: arx cd <klasör>"); continue
                arx_cd(parcalar[2])
            elif kategori == "pwd":
                print(arx_mevcut_dizin[0])
            elif kategori == "clear":
                arx_clear()
                arxsage_banner()
            elif kategori == "return":
              arx_clear()
              return
            else:
                print(f"[HATA] '{kategori}' tanımlı değil. 'arx help' yaz.")

        except KeyboardInterrupt:
            print(f"\n{ArxRenk.GRI}Çıkmak için 'arx return -AstraSage' yaz.{ArxRenk.RESET}")


if __name__ == "__main__":
    run()
