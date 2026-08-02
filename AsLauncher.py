# AsLauncher • By: EnderAstra
# AstraSage'in çalıştırma Çekirdeği

import os
import platform
import time
import sys
import subprocess
import importlib.util


# ============================================================
# AsLauncher BAŞLANGIÇ / BAĞIMLILIK KONTROLÜ
# ============================================================

# Minimum Python sürümü
MIN_PYTHON = (3, 9)

# AsLauncher / AstraSage için gerekli pip paketleri
#
# Sol taraf:
# Python içerisindeki import adı
#
# Sağ taraf:
# pip ile kurulacak paket adı
GEREKLI_PAKETLER = {
    "requests": "requests",
    "prompt_toolkit": "prompt-toolkit",
}


def python_kontrol():
    """
    Çalışan Python sürümünü kontrol eder.
    """

    mevcut_surumu = sys.version_info[:2]

    if mevcut_surumu < MIN_PYTHON:

        print()
        print("=" * 60)
        print("          AsLauncher BAŞLATILAMADI")
        print("=" * 60)
        print()

        print(
            f"[X] Python sürümü yetersiz."
        )

        print(
            f"[!] Gerekli Python : "
            f"{MIN_PYTHON[0]}.{MIN_PYTHON[1]}+"
        )

        print(
            f"[!] Mevcut Python  : "
            f"{mevcut_surumu[0]}.{mevcut_surumu[1]}"
        )

        print()
        print("Lütfen Python'u güncelleyin.")
        print()
        print("=" * 60)

        return False

    return True


def pip_kontrol():
    """
    pip'in kullanılabilir olup olmadığını kontrol eder.
    """

    try:

        sonuc = subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "--version"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if sonuc.returncode != 0:

            print()
            print("=" * 60)
            print("          AsLauncher BAŞLATILAMADI")
            print("=" * 60)
            print()

            print("[X] pip bulunamadı.")
            print()
            print(
                "Python ortamınızda pip kurulu değil."
            )

            print()
            print("=" * 60)

            return False

        return True

    except Exception as e:

        print()
        print("=" * 60)
        print("          AsLauncher BAŞLATILAMADI")
        print("=" * 60)
        print()

        print(f"[X] pip kontrol edilemedi: {e}")

        print()
        print("=" * 60)

        return False


def paket_kontrol():
    """
    Gerekli Python modüllerini kontrol eder.
    """

    eksik_paketler = []

    for modul, pip_adi in GEREKLI_PAKETLER.items():

        try:
            mevcut = importlib.util.find_spec(modul)

        except Exception:
            mevcut = None

        if mevcut is None:
            eksik_paketler.append(pip_adi)

    if not eksik_paketler:
        return True

    print()
    print("=" * 60)
    print("          AsLauncher BAŞLATILAMADI")
    print("=" * 60)
    print()

    print("[X] Eksik Python paketleri bulundu:")
    print()

    for paket in eksik_paketler:
        print(f"    [X] {paket}")

    print()
    print("Eksik paketleri kurmak için:")
    print()

    print(
        "python -m pip install "
        + " ".join(eksik_paketler)
    )

    print()
    print("Alternatif olarak:")
    print()

    print(
        "pip install "
        + " ".join(eksik_paketler)
    )

    print()
    print("=" * 60)

    return False


def baslangic_kontrolu():
    """
    AsLauncher başlamadan önce bütün kontrolleri çalıştırır.
    """

    print()
    print("[*] Python kontrol ediliyor...")

    if not python_kontrol():
        return False

    print(
        f"[✓] Python "
        f"{sys.version_info.major}."
        f"{sys.version_info.minor} uygun."
    )

    print("[*] pip kontrol ediliyor...")

    if not pip_kontrol():
        return False

    print("[✓] pip kullanılabilir.")

    print("[*] Gerekli paketler kontrol ediliyor...")

    if not paket_kontrol():
        return False

    print("[✓] Gerekli paketler mevcut.")

    print()

    return True


# ============================================================
# AsLauncher Değişkenleri
# ============================================================

situation = False
error_while = False

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


RESET = "\033[0m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
RED = "\033[41;37m"
SEL = "\033[42;37m"


# ============================================================
# LOADING
# ============================================================

def loading():

    frames = ["/", "-", "\\", "|"]

    for i in range(25):

        print(
            f"\r[ {frames[i % len(frames)]} ] "
            f"AsLauncher Başlatılıyor...",
            end="",
            flush=True
        )

        time.sleep(0.1)

    print(
        "\r[✓] AsLauncher Başlatıldı!          "
    )


# ============================================================
# HATA SİSTEMİ
# ============================================================

def is_error(error):

    global error_while

    if error == "situation":

        time.sleep(0.2)

        print(
            "Hata Sebebi: Sistem Başlatılmadı"
        )

        print(
            "Situation Is Not True!!"
        )

        error_while = True

    elif error == "command":

        time.sleep(0.2)

        print(
            "Hata Sebebi: Komut Bulunamadı"
        )

        print(
            "Command Is Not Found"
        )

        error_while = False


# ============================================================
# PYTHON DOSYASI ÇALIŞTIRMA
# ============================================================

def run_py(folder):

    folder = os.path.abspath(folder)

    if not os.path.isfile(folder):

        print(
            f"[!] '{folder}' bulunamadı, atlanıyor..."
        )

        return

    workdir = os.path.dirname(folder)

    subprocess.run(
        [sys.executable, folder],
        cwd=workdir
    )


# ============================================================
# EKRAN TEMİZLEME
# ============================================================

def clear():

    if platform.system() == "Windows":
        os.system("cls")

    else:
        os.system("clear")


# ============================================================
# LOGO
# ============================================================

def show_logo():

    logo = '''██╗      █████╗ ██╗   ██╗███╗   ██╗ ██████╗██╗  ██╗███████╗██████╗ 
██║     ██╔══██╗██║   ██║████╗  ██║██╔════╝██║  ██║██╔════╝██╔══██╗
██║     ███████║██║   ██║██╔██╗ ██║██║     ███████║█████╗  ██████╔╝
██║     ██╔══██║██║   ██║██║╚██╗██║██║     ██╔══██║██╔══╝  ██╔══██╗
███████╗██║  ██║╚██████╔╝██║ ╚████║╚██████╗██║  ██║███████╗██║  ██║
╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
'''

    print(logo)


# ============================================================
# MENÜ
# ============================================================

def menu():

    show_logo()

    print("Dağıtım seçiniz.\n")

    print("  AstraSage[1]")
    print("  ArxSage[2]")
    print("  DepSage[3]")
    print("  DevSage[4]")


# ============================================================
# ANA FONKSİYON
# ============================================================

def main():

    global situation, error_while

    # --------------------------------------------------------
    # BAŞLANGIÇ KONTROLLERİ
    # --------------------------------------------------------

    if not baslangic_kontrolu():

        print()
        print(
            "[!] AsLauncher başlatılamıyor."
        )

        input(
            "Çıkmak için Enter'a basın..."
        )

        return

    # --------------------------------------------------------
    # Boot Ekranını Çalıştır
    # --------------------------------------------------------

    run_py(
        os.path.join(
            BASE_DIR,
            "as_kernel.py"
        )
    )

    # --------------------------------------------------------
    # Sistemin Durumunu Etkinleştir
    # --------------------------------------------------------

    situation = True

    if situation != True:

        print(
            "Launcher Başlatılamadı"
        )

        is_error("situation")

        return

    # --------------------------------------------------------
    # Launcher Başlat
    # --------------------------------------------------------

    print("Sistem Başlatılıyor..")

    time.sleep(0.2)

    print(
        "Bu Biraz Uzun Sürebilir"
    )

    print(
        "Launcher'ı Kapatmayınız!!"
    )

    loading()

    clear()

    menu()

    # --------------------------------------------------------
    # Dağıtım seçenekleri
    # --------------------------------------------------------

    opts = [
        "AstraSage",
        "ArxSage",
        "DepSage",
        "DevSage"
    ]

    cur = 0

    # --------------------------------------------------------
    # Menü döngüsü
    # --------------------------------------------------------

    while True:

        if error_while:
            break

        clear()

        show_logo()

        print(
            "Dağıtım seçiniz.\n"
        )

        for i, o in enumerate(opts):

            if i == cur:

                print(
                    f"  ➤  "
                    f"{SEL}  [{i+1}] "
                    f"{o}{RESET}"
                )

            else:

                print(
                    f"     [{i+1}] {o}"
                )

        print(
            "\n1-4 seç, Enter çalıştır, q çıkış"
        )

        s = input(
            r"\~\$/>> "
        ).strip().lower()

        # ----------------------------------------------------
        # Çıkış
        # ----------------------------------------------------

        if s in (
            "q",
            "quit",
            "exit"
        ):

            print(
                "\nAsLauncher kapatılıyor..."
            )

            break

        # ----------------------------------------------------
        # Numara seçimi
        # ----------------------------------------------------

        if s.isdigit():

            n = int(s) - 1

            if 0 <= n < len(opts):

                cur = n

            else:

                input(
                    "Geçersiz Numara. "
                    "Devam için Enter..."
                )

        # ----------------------------------------------------
        # Enter
        # ----------------------------------------------------

        elif s in (
            "",
            "enter"
        ):

            clear()

            show_logo()

            try:

                selected = opts[cur]

                print(
                    f"\n[✓] Seçilen: {selected}"
                )

                time.sleep(0.5)

                if selected == "AstraSage":

                    run_py(
                        os.path.join(
                            BASE_DIR,
                            "main.py"
                        )
                    )

                if selected == "ArxSage":

                    run_py(
                        os.path.join(
                            BASE_DIR,
                            "Distros",
                            "ArxSage",
                            "ArxSage.py"
                        )
                    )

                if selected == "DepSage":

                    run_py(
                        os.path.join(
                            BASE_DIR,
                            "Distros",
                            "DepSage",
                            "DepSage.py"
                        )
                    )

                if selected == "DevSage":

                    run_py(
                        os.path.join(
                            BASE_DIR,
                            "Distros",
                            "DevSage",
                            "DevSage.py"
                        )
                    )

            except Exception as e:

                print(
                    f"Hata: {e}"
                )

                input(
                    "Devam için Enter..."
                )

        # ----------------------------------------------------
        # Geçersiz giriş
        # ----------------------------------------------------

        else:

            input(
                "Geçersiz giriş. "
                "Devam için Enter..."
            )


# ============================================================
# PROGRAM BAŞLANGICI
# ============================================================

if __name__ == "__main__":

    main()