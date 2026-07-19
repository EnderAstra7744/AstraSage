
#DepSage • By:EnderAstra
#AstraSage Mini Distro - Arch Linux Esinli Sistem Yönetimi Terminali

import os
import sys
import time
import platform
import socket
import hashlib
import datetime
import shutil
import subprocess

#DepSage kök dizini
DEP_KOK = os.path.dirname(os.path.abspath(__file__))
ASTRASAGE_KOK = os.path.dirname(os.path.dirname(DEP_KOK))

dep_mevcut_dizin = [os.getcwd()]

class DepRenk:
    MAVI = "\033[94m"
    KOYU_MAVI = "\033[34m"
    CYAN = "\033[96m"
    KOYU_CYAN = "\033[36m"
    BEYAZ = "\033[97m"
    GRI = "\033[90m"
    YESIL = "\033[92m"
    KIRMIZI = "\033[91m"
    SARI = "\033[93m"
    RESET = "\033[0m"
    BOLD = "\033[1m"



LOGO = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢠⣾⣿⣏⠉⠉⠉⠉⠉⠉⢡⣶⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠻⢿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠈⣿⣿⣿⣿⣦⣽⣦⡀⠀⠀⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⢧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⡄
⠀⠘⢿⣿⣿⣿⣿⣿⣿⣦⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⠇
⠀⠀⠈⠻⣿⣿⣿⣿⡟⢿⠻⠛⠙⠉⠋⠛⠳⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⠀
⠀⠀⠀⠀⠈⠙⢿⡇⣠⣤⣶⣶⣾⡉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣰⡀⠀⠀⠀⠀⠀⠀⠀⠠⠾⢇⠀⣿⣿⣿⠃
⠀⠀⠀⠀⠀⠀⠀⠱⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⡇⠀⠀⠀⠀⠀⠐⠤⢤⣀⣀⣀⣤⣭⣿⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣶⣤⣄⣀⣀⣠⣴⣾⣿⣿⣿⣷⣤⣀⡀⠀⠀⠀⣀⣤⣾⣿⡿⠛⣿⣿⣇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣘⡛⠿⠟⠉⠀⠀⠻⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢿⣿⣿⣿⣶⣤⣀⡀⠀⠀⠻⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⠿⠛⠉⠁⠀⠈⠉⠙⠛⠻⠿⠿⠟⠛⠃⠀⠀⠉⠉⠛⠛⠿⠿⣶⣄⠀⠀⠁
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠿⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠀
"""

def depsage_banner():
    print(LOGO)
    print(DepRenk.BOLD + DepRenk.CYAN + "DepSage" + DepRenk.RESET + " • AstraSage System Distro")
    print(DepRenk.GRI + "By:EnderAstra" + DepRenk.RESET)
    print("")
    print("=" * 50)
    print(f"\n{DepRenk.CYAN}Komut Kategorileri:{DepRenk.RESET}")
    print(f"  {DepRenk.BEYAZ}dep help{DepRenk.RESET}           → tüm komutlar")
    print(f"  {DepRenk.BEYAZ}dep pkg ...{DepRenk.RESET}        → paket yönetimi")
    print(f"  {DepRenk.BEYAZ}dep sys ...{DepRenk.RESET}        → sistem bilgisi")
    print(f"  {DepRenk.BEYAZ}dep disk ...{DepRenk.RESET}       → disk araçları")
    print(f"  {DepRenk.BEYAZ}dep proc ...{DepRenk.RESET}       → süreç yönetimi")
    print(f"  {DepRenk.BEYAZ}dep net ...{DepRenk.RESET}        → ağ araçları")
    print(f"  {DepRenk.BEYAZ}dep file ...{DepRenk.RESET}       → dosya araçları")
    print(f"  {DepRenk.BEYAZ}dep dev ...{DepRenk.RESET}        → geliştirici araçları")
    print(f"  {DepRenk.BEYAZ}dep return -AstraSage{DepRenk.RESET} → geri dön")
    print("=" * 50)
    print("")


def dep_clear():
    os.system("clear")
    
# ==================== PAKET YÖNETİMİ (pacman esinli) ====================

def dep_pkg_list():
    """Kurulu pip paketlerini listeler (pacman -Q esinli)."""
    print(f"\n{DepRenk.CYAN}[DepSage/Pkg] Kurulu Paketler{DepRenk.RESET}")
    print("-" * 40)
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list"],
            capture_output=True, text=True
        )
        print(result.stdout)
    except Exception as hata:
        print(f"[HATA] {hata}")


def dep_pkg_search(paket):
    """Paket arar (pacman -Ss esinli)."""
    print(f"\n{DepRenk.CYAN}[DepSage/Pkg] Paket Arama: {paket}{DepRenk.RESET}")
    print("-" * 40)
    try:
        process = subprocess.Popen(
            [sys.executable, "-m", "pip", "search", paket],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, bufsize=1
        )
        for satir in process.stdout:
            print(satir, end="")
        process.wait()
    except Exception:
        # pip search artık çalışmıyor, PyPI'dan bilgi çek
        try:
            import urllib.request
            import json
            url = f"https://pypi.org/pypi/{paket}/json"
            with urllib.request.urlopen(url, timeout=5) as r:
                veri = json.loads(r.read())
                bilgi = veri["info"]
                print(f"İsim       : {bilgi['name']}")
                print(f"Sürüm      : {bilgi['version']}")
                print(f"Açıklama   : {bilgi['summary']}")
                print(f"Yazar      : {bilgi['author']}")
                print(f"Lisans     : {bilgi['license']}")
                print(f"PyPI       : {bilgi['package_url']}")
        except Exception as hata:
            print(f"[HATA] Paket bulunamadı: {hata}")


def dep_pkg_install(paket):
    """Paket kurar (pacman -S esinli)."""
    print(f"\n{DepRenk.CYAN}[DepSage/Pkg] Kuruluyor: {paket}{DepRenk.RESET}")
    print("-" * 40)
    try:
        process = subprocess.Popen(
            [sys.executable, "-m", "pip", "install", paket],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, bufsize=1
        )
        for satir in process.stdout:
            print(satir, end="")
        process.wait()
        if process.returncode == 0:
            print(f"\n{DepRenk.YESIL}'{paket}' başarıyla kuruldu.{DepRenk.RESET}")
        else:
            print(f"\n{DepRenk.KIRMIZI}'{paket}' kurulamadı.{DepRenk.RESET}")
    except Exception as hata:
        print(f"[HATA] {hata}")


def dep_pkg_remove(paket):
    """Paket kaldırır (pacman -R esinli)."""
    print(f"\n{DepRenk.CYAN}[DepSage/Pkg] Kaldırılıyor: {paket}{DepRenk.RESET}")
    onay = input(f"'{paket}' kaldırılsın mı? (e/h): ").strip().lower()
    if onay != "e":
        print("İptal edildi.")
        return
    try:
        process = subprocess.Popen(
            [sys.executable, "-m", "pip", "uninstall", paket, "-y"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, bufsize=1
        )
        for satir in process.stdout:
            print(satir, end="")
        process.wait()
        if process.returncode == 0:
            print(f"\n{DepRenk.YESIL}'{paket}' kaldırıldı.{DepRenk.RESET}")
        else:
            print(f"\n{DepRenk.KIRMIZI}'{paket}' kaldırılamadı.{DepRenk.RESET}")
    except Exception as hata:
        print(f"[HATA] {hata}")


def dep_pkg_upgrade():
    """pip'i günceller (pacman -Syu esinli)."""
    print(f"\n{DepRenk.CYAN}[DepSage/Pkg] Sistem Güncelleme{DepRenk.RESET}")
    print("-" * 40)
    try:
        process = subprocess.Popen(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, bufsize=1
        )
        for satir in process.stdout:
            print(satir, end="")
        process.wait()
        print(f"\n{DepRenk.YESIL}Güncelleme tamamlandı.{DepRenk.RESET}")
    except Exception as hata:
        print(f"[HATA] {hata}")


def dep_pkg_info(paket):
    """Paket bilgisi gösterir (pacman -Qi esinli)."""
    print(f"\n{DepRenk.CYAN}[DepSage/Pkg] Paket Bilgisi: {paket}{DepRenk.RESET}")
    print("-" * 40)
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", paket],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f"'{paket}' kurulu değil.")
    except Exception as hata:
        print(f"[HATA] {hata}")


# ==================== SİSTEM BİLGİSİ (neofetch/uname esinli) ====================

def dep_sys_neofetch():
    """Sistem bilgisini neofetch stili gösterir."""
    print(f"\n{DepRenk.CYAN}{'='*45}{DepRenk.RESET}")

    logo_satirlar = [
        f"{DepRenk.CYAN}    /\\{DepRenk.RESET}",
        f"{DepRenk.CYAN}   /  \\{DepRenk.RESET}",
        f"{DepRenk.CYAN}  / /\\ \\{DepRenk.RESET}",
        f"{DepRenk.CYAN} / ____ \\{DepRenk.RESET}",
        f"{DepRenk.CYAN}/_/    \\_\\{DepRenk.RESET}",
        "",
    ]

    bilgiler = [
        f"{DepRenk.CYAN}OS{DepRenk.RESET}       : DepSage (AstraSage üzerinde)",
        f"{DepRenk.CYAN}Kernel{DepRenk.RESET}   : {platform.system()} {platform.release()}",
        f"{DepRenk.CYAN}Arch{DepRenk.RESET}     : {platform.machine()}",
        f"{DepRenk.CYAN}Python{DepRenk.RESET}   : {sys.version.split()[0]}",
        f"{DepRenk.CYAN}Shell{DepRenk.RESET}    : DepSage/dep",
        f"{DepRenk.CYAN}Node{DepRenk.RESET}     : {platform.node()}",
    ]

    for i in range(max(len(logo_satirlar), len(bilgiler))):
        sol = logo_satirlar[i] if i < len(logo_satirlar) else " " * 10
        sag = bilgiler[i] if i < len(bilgiler) else ""
        print(f"{sol:<25} {sag}")

    print(f"\n{DepRenk.CYAN}{'='*45}{DepRenk.RESET}")


def dep_sys_uname():
    """Sistem bilgisi (uname -a esinli)."""
    print(f"\n{DepRenk.CYAN}[DepSage/Sys] uname{DepRenk.RESET}")
    print(f"{platform.system()} {platform.node()} {platform.release()} {platform.version()} {platform.machine()}")


def dep_sys_uptime():
    """Sistem çalışma süresini gösterir."""
    print(f"\n{DepRenk.CYAN}[DepSage/Sys] Uptime{DepRenk.RESET}")
    try:
        with open("/proc/uptime", "r") as f:
            saniye = float(f.read().split()[0])
        gun = int(saniye // 86400)
        saat = int((saniye % 86400) // 3600)
        dakika = int((saniye % 3600) // 60)
        print(f"Çalışma Süresi: {gun} gün, {saat} saat, {dakika} dakika")
    except Exception:
        print(f"[BİLGİ] Uptime bu ortamda alınamıyor.")


def dep_sys_env():
    """Ortam değişkenlerini listeler (env esinli)."""
    print(f"\n{DepRenk.CYAN}[DepSage/Sys] Ortam Değişkenleri{DepRenk.RESET}")
    print("-" * 40)
    for key, value in sorted(os.environ.items()):
        print(f"  {DepRenk.MAVI}{key}{DepRenk.RESET}={value}")


def dep_sys_which(komut):
    """Komutun yolunu bulur (which esinli)."""
    print(f"\n{DepRenk.CYAN}[DepSage/Sys] which: {komut}{DepRenk.RESET}")
    yol = shutil.which(komut)
    if yol:
        print(f"{DepRenk.YESIL}{yol}{DepRenk.RESET}")
    else:
        print(f"'{komut}' bulunamadı.")


# ==================== DİSK ARAÇLARI (df/du esinli) ====================

def dep_disk_df():
    """Disk kullanımını gösterir (df -h esinli)."""
    print(f"\n{DepRenk.CYAN}[DepSage/Disk] Disk Kullanımı{DepRenk.RESET}")
    print("-" * 50)
    print(f"{'Yol':<20} {'Toplam':>10} {'Kullanılan':>12} {'Boş':>10} {'%':>5}")
    print("-" * 50)

    for yol in ["/", os.path.expanduser("~")]:
        try:
            toplam, kullanilan, bos = shutil.disk_usage(yol)
            t = f"{toplam/(1024**3):.1f}G"
            k = f"{kullanilan/(1024**3):.1f}G"
            b = f"{bos/(1024**3):.1f}G"
            yuzde = int(kullanilan / toplam * 100)
            renk = DepRenk.KIRMIZI if yuzde > 80 else DepRenk.YESIL
            print(f"{yol:<20} {t:>10} {k:>12} {b:>10} {renk}{yuzde}%{DepRenk.RESET}")
        except Exception:
            pass
    print("-" * 50)


def dep_disk_du(yol="."):
    """Klasör boyutunu gösterir (du -sh esinli)."""
    print(f"\n{DepRenk.CYAN}[DepSage/Disk] Klasör Boyutu: {yol}{DepRenk.RESET}")
    try:
        toplam = 0
        for dirpath, dirnames, filenames in os.walk(yol):
            for f in filenames:
                try:
                    toplam += os.path.getsize(os.path.join(dirpath, f))
                except Exception:
                    pass

        if toplam < 1024:
            boyut_str = f"{toplam} B"
        elif toplam < 1024**2:
            boyut_str = f"{toplam/1024:.1f} KB"
        elif toplam < 1024**3:
            boyut_str = f"{toplam/(1024**2):.1f} MB"
        else:
            boyut_str = f"{toplam/(1024**3):.1f} GB"

        print(f"Toplam Boyut: {DepRenk.CYAN}{boyut_str}{DepRenk.RESET}  ({yol})")
    except Exception as hata:
        print(f"[HATA] {hata}")


def dep_disk_ls(yol="."):
    """Detaylı dizin listesi (ls -la esinli)."""
    print(f"\n{DepRenk.CYAN}[DepSage/Disk] Dizin: {yol}{DepRenk.RESET}")
    print("-" * 60)
    print(f"{'Tür':<5} {'Boyut':>10} {'Tarih':<22} {'İsim'}")
    print("-" * 60)
    try:
        icerik = sorted(os.listdir(yol))
        for item in icerik:
            tam = os.path.join(yol, item)
            stat = os.stat(tam)
            boyut = stat.st_size
            tarih = datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%d/%m/%Y %H:%M")
            if os.path.isdir(tam):
                tur = "DIR"
                boyut_str = "-"
                print(f"{DepRenk.CYAN}{tur:<5}{DepRenk.RESET} {boyut_str:>10} {tarih:<22} {DepRenk.CYAN}{item}/{DepRenk.RESET}")
            else:
                tur = "FILE"
                boyut_str = f"{boyut}B" if boyut < 1024 else f"{boyut//1024}KB"
                print(f"{tur:<5} {boyut_str:>10} {tarih:<22} {item}")
    except Exception as hata:
        print(f"[HATA] {hata}")
    print("-" * 60)


def dep_disk_find(yol, pattern):
    """Dosya arar (find esinli)."""
    print(f"\n{DepRenk.CYAN}[DepSage/Disk] Arama: '{pattern}' → {yol}{DepRenk.RESET}")
    print("-" * 40)
    bulunanlar = []
    try:
        for root, dirs, files in os.walk(yol):
            for f in files:
                if pattern.lower() in f.lower():
                    tam = os.path.join(root, f)
                    bulunanlar.append(tam)
                    print(f"  {tam}")
        print("-" * 40)
        print(f"Toplam {len(bulunanlar)} sonuç.")
    except Exception as hata:
        print(f"[HATA] {hata}")


# ==================== SÜREÇ YÖNETİMİ (ps/kill esinli) ====================

def dep_proc_list():
    """Çalışan Python süreçlerini listeler (ps esinli)."""
    print(f"\n{DepRenk.CYAN}[DepSage/Proc] Süreçler{DepRenk.RESET}")
    print("-" * 40)
    try:
        result = subprocess.run(
            ["ps", "aux"],
            capture_output=True, text=True
        )
        satirlar = result.stdout.splitlines()
        print(satirlar[0])  # başlık
        for satir in satirlar[1:]:
            if "python" in satir.lower():
                print(f"{DepRenk.YESIL}{satir}{DepRenk.RESET}")
            else:
                print(satir)
    except Exception:
        print("[BİLGİ] ps komutu bu ortamda çalışmıyor.")
        print(f"Python PID: {os.getpid()}")


def dep_proc_kill(pid):
    """Süreci sonlandırır (kill esinli)."""
    print(f"\n{DepRenk.CYAN}[DepSage/Proc] Kill: PID {pid}{DepRenk.RESET}")
    onay = input(f"PID {pid} sonlandırılsın mı? (e/h): ").strip().lower()
    if onay != "e":
        print("İptal edildi.")
        return
    try:
        os.kill(int(pid), 15)
        print(f"{DepRenk.YESIL}PID {pid} sonlandırıldı.{DepRenk.RESET}")
    except ProcessLookupError:
        print(f"[HATA] PID {pid} bulunamadı.")
    except Exception as hata:
        print(f"[HATA] {hata}")


# ==================== AĞ ARAÇLARI ====================

def dep_net_ifconfig():
    """Ağ arayüzü bilgisi (ifconfig esinli)."""
    print(f"\n{DepRenk.CYAN}[DepSage/Net] Ağ Bilgisi{DepRenk.RESET}")
    print("-" * 40)
    try:
        hostname = socket.gethostname()
        print(f"Hostname   : {hostname}")
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        print(f"Yerel IP   : {ip}")
    except Exception:
        print(f"IP         : Alınamadı")


def dep_net_ping(hedef):
    """Ping atar."""
    print(f"\n{DepRenk.CYAN}[DepSage/Net] Ping: {hedef}{DepRenk.RESET}")
    try:
        ip = socket.gethostbyname(hedef)
        print(f"IP: {ip}")
        os.system(f"ping -c 4 {ip}")
    except Exception as hata:
        print(f"[HATA] {hata}")


def dep_net_dns(hedef):
    """DNS sorgusu."""
    print(f"\n{DepRenk.CYAN}[DepSage/Net] DNS: {hedef}{DepRenk.RESET}")
    try:
        ip = socket.gethostbyname(hedef)
        print(f"IP Adresi  : {ip}")
        try:
            ters = socket.gethostbyaddr(ip)
            print(f"Ters DNS   : {ters[0]}")
        except Exception:
            print(f"Ters DNS   : Bulunamadı")
    except Exception as hata:
        print(f"[HATA] {hata}")


def dep_net_curl(url):
    """URL'ye istek atar (curl esinli)."""
    import urllib.request
    print(f"\n{DepRenk.CYAN}[DepSage/Net] curl: {url}{DepRenk.RESET}")
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "DepSage/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            print(f"Durum      : {r.status}")
            print(f"İçerik Tipi: {r.headers.get('Content-Type', 'Bilinmiyor')}")
            print(f"Sunucu     : {r.headers.get('Server', 'Bilinmiyor')}")
            icerik = r.read(500).decode("utf-8", errors="ignore")
            print(f"\n--- İçerik (ilk 500 byte) ---")
            print(icerik)
    except Exception as hata:
        print(f"[HATA] {hata}")


# ==================== DOSYA ARAÇLARI ====================

def dep_file_cat(dosya):
    """Dosya içeriğini gösterir (cat esinli)."""
    print(f"\n{DepRenk.CYAN}[DepSage/File] cat: {dosya}{DepRenk.RESET}")
    print("-" * 40)
    if not os.path.exists(dosya):
        print(f"[HATA] '{dosya}' bulunamadı.")
        return
    try:
        with open(dosya, "r", encoding="utf-8") as f:
            for i, satir in enumerate(f, 1):
                print(f"{DepRenk.GRI}{i:4}{DepRenk.RESET}  {satir}", end="")
    except Exception as hata:
        print(f"[HATA] {hata}")


def dep_file_grep(pattern, dosya):
    """Dosyada metin arar (grep esinli)."""
    print(f"\n{DepRenk.CYAN}[DepSage/File] grep: '{pattern}' → {dosya}{DepRenk.RESET}")
    print("-" * 40)
    if not os.path.exists(dosya):
        print(f"[HATA] '{dosya}' bulunamadı.")
        return
    try:
        with open(dosya, "r", encoding="utf-8") as f:
            satirlar = f.readlines()
        bulunan = 0
        for i, satir in enumerate(satirlar, 1):
            if pattern.lower() in satir.lower():
                vurgulu = satir.replace(pattern, f"{DepRenk.SARI}{pattern}{DepRenk.RESET}")
                print(f"{DepRenk.GRI}{i:4}{DepRenk.RESET}  {vurgulu}", end="")
                bulunan += 1
        print("-" * 40)
        print(f"{bulunan} eşleşme bulundu.")
    except Exception as hata:
        print(f"[HATA] {hata}")


def dep_file_wc(dosya):
    """Dosya istatistikleri (wc esinli)."""
    print(f"\n{DepRenk.CYAN}[DepSage/File] wc: {dosya}{DepRenk.RESET}")
    if not os.path.exists(dosya):
        print(f"[HATA] '{dosya}' bulunamadı.")
        return
    try:
        with open(dosya, "r", encoding="utf-8") as f:
            icerik = f.read()
        satirlar = icerik.count("\n")
        kelimeler = len(icerik.split())
        karakterler = len(icerik)
        print(f"Satır      : {satirlar}")
        print(f"Kelime     : {kelimeler}")
        print(f"Karakter   : {karakterler}")
    except Exception as hata:
        print(f"[HATA] {hata}")


def dep_file_tail(dosya, n=10):
    """Dosyanın son satırlarını gösterir (tail esinli)."""
    print(f"\n{DepRenk.CYAN}[DepSage/File] tail -{n}: {dosya}{DepRenk.RESET}")
    print("-" * 40)
    if not os.path.exists(dosya):
        print(f"[HATA] '{dosya}' bulunamadı.")
        return
    try:
        with open(dosya, "r", encoding="utf-8") as f:
            satirlar = f.readlines()
        for satir in satirlar[-n:]:
            print(satir, end="")
    except Exception as hata:
        print(f"[HATA] {hata}")


def dep_file_head(dosya, n=10):
    """Dosyanın ilk satırlarını gösterir (head esinli)."""
    print(f"\n{DepRenk.CYAN}[DepSage/File] head -{n}: {dosya}{DepRenk.RESET}")
    print("-" * 40)
    if not os.path.exists(dosya):
        print(f"[HATA] '{dosya}' bulunamadı.")
        return
    try:
        with open(dosya, "r", encoding="utf-8") as f:
            for i, satir in enumerate(f):
                if i >= n:
                    break
                print(satir, end="")
    except Exception as hata:
        print(f"[HATA] {hata}")


def dep_file_cp(kaynak, hedef):
    """Dosya kopyalar (cp esinli)."""
    print(f"\n{DepRenk.CYAN}[DepSage/File] cp: {kaynak} → {hedef}{DepRenk.RESET}")
    try:
        shutil.copy2(kaynak, hedef)
        print(f"{DepRenk.YESIL}Kopyalandı.{DepRenk.RESET}")
    except Exception as hata:
        print(f"[HATA] {hata}")


def dep_file_mv(kaynak, hedef):
    """Dosya taşır (mv esinli)."""
    print(f"\n{DepRenk.CYAN}[DepSage/File] mv: {kaynak} → {hedef}{DepRenk.RESET}")
    try:
        shutil.move(kaynak, hedef)
        print(f"{DepRenk.YESIL}Taşındı.{DepRenk.RESET}")
    except Exception as hata:
        print(f"[HATA] {hata}")


def dep_file_rm(dosya):
    """Dosya siler (rm esinli)."""
    print(f"\n{DepRenk.CYAN}[DepSage/File] rm: {dosya}{DepRenk.RESET}")
    onay = input(f"'{dosya}' silinsin mi? (e/h): ").strip().lower()
    if onay != "e":
        print("İptal edildi.")
        return
    try:
        if os.path.isdir(dosya):
            shutil.rmtree(dosya)
        else:
            os.remove(dosya)
        print(f"{DepRenk.YESIL}Silindi.{DepRenk.RESET}")
    except Exception as hata:
        print(f"[HATA] {hata}")


def dep_file_mkdir(klasor):
    """Klasör oluşturur (mkdir esinli)."""
    try:
        os.makedirs(klasor, exist_ok=True)
        print(f"{DepRenk.YESIL}'{klasor}' oluşturuldu.{DepRenk.RESET}")
    except Exception as hata:
        print(f"[HATA] {hata}")


def dep_file_touch(dosya):
    """Boş dosya oluşturur (touch esinli)."""
    try:
        with open(dosya, "a"):
            os.utime(dosya, None)
        print(f"{DepRenk.YESIL}'{dosya}' oluşturuldu.{DepRenk.RESET}")
    except Exception as hata:
        print(f"[HATA] {hata}")


# ==================== GELİŞTİRİCİ ARAÇLARI ====================

def dep_dev_python_version():
    """Python sürümü gösterir."""
    print(f"\n{DepRenk.CYAN}[DepSage/Dev] Python{DepRenk.RESET}")
    print(f"Sürüm      : {sys.version}")
    print(f"Yol        : {sys.executable}")
    print(f"Platform   : {sys.platform}")


def dep_dev_hash(metin, algo="sha256"):
    """Metin hashler."""
    print(f"\n{DepRenk.CYAN}[DepSage/Dev] Hash ({algo}){DepRenk.RESET}")
    try:
        h = hashlib.new(algo)
        h.update(metin.encode("utf-8"))
        print(f"Girdi      : {metin}")
        print(f"{algo.upper()}: {h.hexdigest()}")
    except ValueError:
        print(f"[HATA] '{algo}' desteklenmiyor.")


def dep_dev_base64_encode(metin):
    """Base64 kodlar."""
    import base64
    print(f"\n{DepRenk.CYAN}[DepSage/Dev] Base64 Encode{DepRenk.RESET}")
    kodlu = base64.b64encode(metin.encode()).decode()
    print(f"Girdi      : {metin}")
    print(f"Kodlu      : {kodlu}")


def dep_dev_base64_decode(metin):
    """Base64 çözer."""
    import base64
    print(f"\n{DepRenk.CYAN}[DepSage/Dev] Base64 Decode{DepRenk.RESET}")
    try:
        cozulmus = base64.b64decode(metin.encode()).decode()
        print(f"Girdi      : {metin}")
        print(f"Çözüldü    : {cozulmus}")
    except Exception:
        print("[HATA] Geçersiz Base64.")


def dep_dev_timestamp():
    """Unix timestamp gösterir."""
    print(f"\n{DepRenk.CYAN}[DepSage/Dev] Timestamp{DepRenk.RESET}")
    simdi = datetime.datetime.now()
    print(f"Timestamp  : {int(simdi.timestamp())}")
    print(f"Tarih/Saat : {simdi.strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"UTC        : {datetime.datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S')}")


# ==================== YARDIM ====================

def dep_help():
    print(f"\n{DepRenk.CYAN}{'='*50}")
    print(f"  DepSage Komut Listesi")
    print(f"{'='*50}{DepRenk.RESET}")

    print(f"\n{DepRenk.SARI}[ Paket Yönetimi (pacman esinli) ]{DepRenk.RESET}")
    print("  dep pkg list              → kurulu paketler (-Q)")
    print("  dep pkg search <paket>    → paket ara (-Ss)")
    print("  dep pkg install <paket>   → paket kur (-S)")
    print("  dep pkg remove <paket>    → paket kaldır (-R)")
    print("  dep pkg upgrade           → güncelle (-Syu)")
    print("  dep pkg info <paket>      → paket bilgisi (-Qi)")

    print(f"\n{DepRenk.SARI}[ Sistem Bilgisi ]{DepRenk.RESET}")
    print("  dep sys neofetch          → sistem özeti")
    print("  dep sys uname             → kernel bilgisi")
    print("  dep sys uptime            → çalışma süresi")
    print("  dep sys env               → ortam değişkenleri")
    print("  dep sys which <komut>     → komut yolu")

    print(f"\n{DepRenk.SARI}[ Disk Araçları ]{DepRenk.RESET}")
    print("  dep disk df               → disk kullanımı")
    print("  dep disk du <yol>         → klasör boyutu")
    print("  dep disk ls <yol>         → detaylı liste")
    print("  dep disk find <yol> <pat> → dosya ara")

    print(f"\n{DepRenk.SARI}[ Süreç Yönetimi ]{DepRenk.RESET}")
    print("  dep proc list             → süreçler (ps)")
    print("  dep proc kill <pid>       → süreç sonlandır")

    print(f"\n{DepRenk.SARI}[ Ağ Araçları ]{DepRenk.RESET}")
    print("  dep net ifconfig          → ağ bilgisi")
    print("  dep net ping <hedef>      → ping")
    print("  dep net dns <hedef>       → DNS sorgu")
    print("  dep net curl <url>        → HTTP istek")

    print(f"\n{DepRenk.SARI}[ Dosya Araçları ]{DepRenk.RESET}")
    print("  dep file cat <dosya>      → dosya göster")
    print("  dep file grep <pat> <dos> → metin ara")
    print("  dep file wc <dosya>       → istatistik")
    print("  dep file head <dosya> <n> → ilk n satır")
    print("  dep file tail <dosya> <n> → son n satır")
    print("  dep file cp <k> <h>       → kopyala")
    print("  dep file mv <k> <h>       → taşı")
    print("  dep file rm <dosya>       → sil")
    print("  dep file mkdir <klasör>   → klasör oluştur")
    print("  dep file touch <dosya>    → dosya oluştur")

    print(f"\n{DepRenk.SARI}[ Geliştirici Araçları ]{DepRenk.RESET}")
    print("  dep dev python            → Python bilgisi")
    print("  dep dev hash <metin>      → hash üret")
    print("  dep dev encode <metin>    → Base64 kodla")
    print("  dep dev decode <metin>    → Base64 çöz")
    print("  dep dev timestamp         → zaman damgası")

    print(f"\n{DepRenk.SARI}[ Genel ]{DepRenk.RESET}")
    print("  dep ls <yol>              → dizin listele")
    print("  dep cd <klasör>           → dizin değiştir")
    print("  dep pwd                   → mevcut dizin")
    print("  dep clear                 → ekranı temizle")
    print("  dep return -AstraSage     → geri dön")
    print(f"\n{DepRenk.CYAN}{'='*50}{DepRenk.RESET}")


# ==================== DOSYA SİSTEMİ ====================

def dep_ls(hedef=None):
    hedef = hedef or dep_mevcut_dizin[0]
    try:
        icerik = os.listdir(hedef)
        if not icerik:
            print("(boş klasör)")
            return
        for item in sorted(icerik):
            tam_yol = os.path.join(hedef, item)
            if os.path.isdir(tam_yol):
                print(f"{DepRenk.CYAN}[K] {item}/{DepRenk.RESET}")
            else:
                print(f"    {item}")
    except Exception as hata:
        print(f"[HATA] {hata}")


def dep_cd(hedef):
    if hedef == "..":
        yeni = os.path.dirname(dep_mevcut_dizin[0])
    else:
        yeni = os.path.join(dep_mevcut_dizin[0], hedef)
    if not os.path.isdir(yeni):
        print(f"[HATA] '{hedef}' bulunamadı.")
        return
    dep_mevcut_dizin[0] = yeni
    print(f"→ {dep_mevcut_dizin[0]}")


# ==================== ANA DÖNGÜ ====================

def dep_run():
    dep_clear()
    depsage_banner()

    while True:
        try:
            kisa_yol = dep_mevcut_dizin[0].replace(os.path.expanduser("~"), "~")
            komut = input(f"{DepRenk.CYAN}dep@DepSage:{DepRenk.RESET}{kisa_yol}$ ")
            parcalar = komut.strip().split()

            if not parcalar:
                continue
                
            if parcalar[0] != "dep":
                print(f"[HATA] DepSage komutları 'dep' ile başlamalı.")
                continue

            if len(parcalar) < 2:
                dep_help()
                continue

            kategori = parcalar[1]

            # --- PKG ---
            if kategori == "pkg":
                if len(parcalar) < 3: print("Kullanım: dep pkg <list|search|install|remove|upgrade|info>"); continue
                alt = parcalar[2]
                if alt == "list": dep_pkg_list()
                elif alt == "search":
                    if len(parcalar) < 4: print("Kullanım: dep pkg search <paket>"); continue
                    dep_pkg_search(parcalar[3])
                elif alt == "install":
                    if len(parcalar) < 4: print("Kullanım: dep pkg install <paket>"); continue
                    dep_pkg_install(parcalar[3])
                elif alt == "remove":
                    if len(parcalar) < 4: print("Kullanım: dep pkg remove <paket>"); continue
                    dep_pkg_remove(parcalar[3])
                elif alt == "upgrade": dep_pkg_upgrade()
                elif alt == "info":
                    if len(parcalar) < 4: print("Kullanım: dep pkg info <paket>"); continue
                    dep_pkg_info(parcalar[3])
                else: print(f"[HATA] '{alt}' tanımlı değil.")

            # --- SYS ---
            elif kategori == "sys":
                if len(parcalar) < 3: print("Kullanım: dep sys <neofetch|uname|uptime|env|which>"); continue
                alt = parcalar[2]
                if alt == "neofetch": dep_sys_neofetch()
                elif alt == "uname": dep_sys_uname()
                elif alt == "uptime": dep_sys_uptime()
                elif alt == "env": dep_sys_env()
                elif alt == "which":
                    if len(parcalar) < 4: print("Kullanım: dep sys which <komut>"); continue
                    dep_sys_which(parcalar[3])
                else: print(f"[HATA] '{alt}' tanımlı değil.")

            # --- DISK ---
            elif kategori == "disk":
                if len(parcalar) < 3: print("Kullanım: dep disk <df|du|ls|find>"); continue
                alt = parcalar[2]
                if alt == "df": dep_disk_df()
                elif alt == "du":
                    yol = parcalar[3] if len(parcalar) >= 4 else "."
                    dep_disk_du(yol)
                elif alt == "ls":
                    yol = parcalar[3] if len(parcalar) >= 4 else "."
                    dep_disk_ls(yol)
                elif alt == "find":
                    if len(parcalar) < 5: print("Kullanım: dep disk find <yol> <pattern>"); continue
                    dep_disk_find(parcalar[3], parcalar[4])
                else: print(f"[HATA] '{alt}' tanımlı değil.")

            # --- PROC ---
            elif kategori == "proc":
                if len(parcalar) < 3: print("Kullanım: dep proc <list|kill>"); continue
                alt = parcalar[2]
                if alt == "list": dep_proc_list()
                elif alt == "kill":
                    if len(parcalar) < 4: print("Kullanım: dep proc kill <pid>"); continue
                    dep_proc_kill(parcalar[3])
                else: print(f"[HATA] '{alt}' tanımlı değil.")

            # --- NET ---
            elif kategori == "net":
                if len(parcalar) < 3: print("Kullanım: dep net <ifconfig|ping|dns|curl>"); continue
                alt = parcalar[2]
                if alt == "ifconfig": dep_net_ifconfig()
                elif alt == "ping":
                    if len(parcalar) < 4: print("Kullanım: dep net ping <hedef>"); continue
                    dep_net_ping(parcalar[3])
                elif alt == "dns":
                    if len(parcalar) < 4: print("Kullanım: dep net dns <hedef>"); continue
                    dep_net_dns(parcalar[3])
                elif alt == "curl":
                    if len(parcalar) < 4: print("Kullanım: dep net curl <url>"); continue
                    dep_net_curl(parcalar[3])
                else: print(f"[HATA] '{alt}' tanımlı değil.")

            # --- FILE ---
            elif kategori == "file":
                if len(parcalar) < 3: print("Kullanım: dep file <cat|grep|wc|head|tail|cp|mv|rm|mkdir|touch>"); continue
                alt = parcalar[2]
                if alt == "cat":
                    if len(parcalar) < 4: print("Kullanım: dep file cat <dosya>"); continue
                    dep_file_cat(parcalar[3])
                elif alt == "grep":
                    if len(parcalar) < 5: print("Kullanım: dep file grep <pattern> <dosya>"); continue
                    dep_file_grep(parcalar[3], parcalar[4])
                elif alt == "wc":
                    if len(parcalar) < 4: print("Kullanım: dep file wc <dosya>"); continue
                    dep_file_wc(parcalar[3])
                elif alt == "head":
                    if len(parcalar) < 4: print("Kullanım: dep file head <dosya> [n]"); continue
                    n = int(parcalar[4]) if len(parcalar) >= 5 else 10
                    dep_file_head(parcalar[3], n)
                elif alt == "tail":
                    if len(parcalar) < 4: print("Kullanım: dep file tail <dosya> [n]"); continue
                    n = int(parcalar[4]) if len(parcalar) >= 5 else 10
                    dep_file_tail(parcalar[3], n)
                elif alt == "cp":
                    if len(parcalar) < 5: print("Kullanım: dep file cp <kaynak> <hedef>"); continue
                    dep_file_cp(parcalar[3], parcalar[4])
                elif alt == "mv":
                    if len(parcalar) < 5: print("Kullanım: dep file mv <kaynak> <hedef>"); continue
                    dep_file_mv(parcalar[3], parcalar[4])
                elif alt == "rm":
                    if len(parcalar) < 4: print("Kullanım: dep file rm <dosya>"); continue
                    dep_file_rm(parcalar[3])
                elif alt == "mkdir":
                    if len(parcalar) < 4: print("Kullanım: dep file mkdir <klasör>"); continue
                    dep_file_mkdir(parcalar[3])
                elif alt == "touch":
                    if len(parcalar) < 4: print("Kullanım: dep file touch <dosya>"); continue
                    dep_file_touch(parcalar[3])
                else: print(f"[HATA] '{alt}' tanımlı değil.")

            # --- DEV ---
            elif kategori == "dev":
                if len(parcalar) < 3: print("Kullanım: dep dev <python|hash|encode|decode|timestamp>"); continue
                alt = parcalar[2]
                if alt == "python": dep_dev_python_version()
                elif alt == "hash":
                    if len(parcalar) < 4: print("Kullanım: dep dev hash <metin> [algo]"); continue
                    algo = parcalar[4] if len(parcalar) >= 5 else "sha256"
                    dep_dev_hash(parcalar[3], algo)
                elif alt == "encode":
                    if len(parcalar) < 4: print("Kullanım: dep dev encode <metin>"); continue
                    dep_dev_base64_encode(" ".join(parcalar[3:]))
                elif alt == "decode":
                    if len(parcalar) < 4: print("Kullanım: dep dev decode <metin>"); continue
                    dep_dev_base64_decode(parcalar[3])
                elif alt == "timestamp": dep_dev_timestamp()
                else: print(f"[HATA] '{alt}' tanımlı değil.")

            # --- GENEL ---
            elif kategori == "help": dep_help()
            elif kategori == "ls":
                hedef = parcalar[2] if len(parcalar) >= 3 else None
                dep_ls(hedef)
            elif kategori == "cd":
                if len(parcalar) < 3: print("Kullanım: dep cd <klasör>"); continue
                dep_cd(parcalar[2])
            elif kategori == "pwd": print(dep_mevcut_dizin[0])
            elif kategori == "clear":
                dep_clear()
                depsage_banner()
            elif kategori == "return":
                hedef = parcalar[2].lstrip("-") if len(parcalar) >= 3 else "AstraSage"
                print(f"\n{DepRenk.GRI}DepSage'den '{hedef}'e dönülüyor...{DepRenk.RESET}")
                time.sleep(0.8)
                dep_clear()
                return
            else:
                print(f"[HATA] '{kategori}' tanımlı değil. 'dep help' yaz.")

        except KeyboardInterrupt:
            print(f"\n{DepRenk.GRI}Çıkmak için 'dep return -AstraSage' yaz.{DepRenk.RESET}")


if __name__ == "__main__":
   dep_run()