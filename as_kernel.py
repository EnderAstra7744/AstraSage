import time
import sys
import os
import glob
import platform
import socket
import hashlib
import main
import importlib.util
import importlib

ASTRASAGE_KOK = os.getcwd()  # AstraSage'in gerçek kök dizini, hiç değişmez

def clear():
    os.system("cls" if os.name == "nt" else "clear")
    
# Düzeltilmiş Frames (orijinal görünüme döndü)
frames = [
    r""" ._. 
 | | 
 | | 
 | | 
 | | 
 |_| """,
    r"""     /\ 
    / / 
   / /  
  / /   
 / /    
 \/     """,
    r"""         
         
  ______ 
 /_____/ 
         
         """,
    r"""/\    
\ \   
 \ \  
  \ \ 
   \ \
    \/"""
]

logo = r"""
  █████╗   ██████╗
 ██╔══██╗ ██╔════╝
 ███████║ ███████╗
 ██╔══██║ ╚════██║
 ██║  ██║ ███████║
 ╚═╝  ╚═╝ ╚══════╝
"""

def clear():
  os.system("clear")

def get_system_info():
    return {
        "cpu": platform.processor() or "AstraSage CPU",
        "ram": f"{os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') // (1024**3)} GB",
        "system": "AS v1.0"
    }


def show_progress_bar(toplam_adim=15, gecikme=0.05):
    for adim in range(toplam_adim + 1):
        yuzde = int((adim / toplam_adim) * 100)
        dolu = "#" * adim
        bos = "-" * (toplam_adim - adim)
        sys.stdout.write(f"\r%{yuzde:<3}[{dolu}{bos}]")
        sys.stdout.flush()
        time.sleep(gecikme)
    print()
    
    
def check_file_integrity():
    try:
        for f in ["main.py", "ASE.py"]:
            if os.path.exists(f):
                with open(f, "rb") as file:
                    hashlib.md5(file.read()).hexdigest()
        return True
    except:
        return False

def perform_real_checks():
    checks = {
        "Initializing Kernel...": lambda: time.sleep(0.3),
        "Loading Core Modules...": lambda: __import__("os"),
        "Loading Memory Manager...": lambda: sys.getsizeof("AstraSage"),
        "Loading File System...": lambda: os.listdir("."),
        "Checking File Integrity...": check_file_integrity,
        "Scanning Hardware...": lambda: platform.system(),
        "Detecting CPU...": lambda: platform.processor(),
        "Detecting RAM...": lambda: get_system_info()["ram"],
        "Initializing Display...": lambda: True,
        "Starting Display Server...": lambda: time.sleep(0.2),
        "Loading Shell...": lambda: True,
        "Checking Network Adapter...": lambda: socket.gethostbyname(socket.gethostname()),
        "Initializing Security...": lambda: True,
        "Loading Encryption Engine...": lambda: hashlib.md5(b"AstraSage").hexdigest(),
    }
    
    for msg, func in checks.items():
        try:
            func()
            print(f"\033[92m✓ {msg}\033[0m")
        except:
            print(f"\033[93m⚠ {msg} (simulated)\033[0m")
        time.sleep(0.15)

def check_critical_files():
    critical = ["main.py", ".signature", "ASE.py"]
    missing = [f for f in critical if not (os.path.exists(f) or glob.glob(f"**/{f}", recursive=True))]
    if missing:
        clear()
        print("\033[91m[CRITICAL ERROR] Missing files:\033[0m")
        for m in missing:
            print(f"   → {m}")
        print("\n\033[93mAstraSage yeniden başlatılıyor...\033[0m\n")
        time.sleep(2.5)
        return False
    return True

def boot_sequence():
    print("\033[?25l", end="")
    start = time.time()
    index = 0

    while not check_critical_files():
        pass

    try:
        while index < 100:
            for f in frames:
                clear()
                print("=" * 70)
                print(logo)
                print("=" * 70)
                print(" \033[92mStatus  : RUNNING\033[0m")
                print(" Kernel  : AS Kernel v1.0")
                print(" Version : 1.0.0")
                print(" Memory  : OK")
                print(" Drivers : Loaded")
                print(" Network : Connected\n")
                print(f)
                
                msg = "Loading AstraSage Core..."
                dots = "." * ((index % 4) + 1)
                print(f"\n> {msg}{dots}")
                print("-" * 70)
                print(f" Uptime : {time.time() - start:05.1f}s")
                print(f" Process: {min(index, 100)}%")
                print("-" * 70)
                time.sleep(0.09)
                index += 1
                if index >= 100:
                    break

        clear()
        print("\033[92m╔══════════════════════════════════════════════════════════════╗")
        print("║               AstraSage Boot Sequence Completed              ║")
        print("╚══════════════════════════════════════════════════════════════╝\033[0m\n")

        perform_real_checks()

        print("\n\033[96mFinalizing AS Environment...\033[0m")
        show_progress_bar(20, 0.2)

        
        print("\n\033[92mAstraSage System is ready.\033[0m")
        time.sleep(1)

        print("\n" + "="*70)
        print("\033[95mBoot tamamlandı. Komutları girebilirsiniz.\033[0m")
        while True:
            try:
                cmd = input("\nboot${Booting}@#:>> ").strip()
                if cmd == "join -kotlin":
                  print("Joinning Kotlin")
                  time.sleep(1)
                  show_progress_bar(20, 0.2)
                  os.system("python astra_kotlin.py")
                  break
                if cmd == "login -astrasage":
                    as_yolu = os.path.join(ASTRASAGE_KOK, "main.py")
                    if not os.path.exists(as_yolu):
                    	print("[HATA] ArxSage bulunamadı. main.py mevcut olmalı.")
                    else:
                    	os.execv(sys.executable, [sys.executable, as_yolu])

                elif cmd.startswith("distro -login "):
                    distro = cmd.replace("distro -login ", "").strip()
                    if distro.lower() == "arxsage":
                        print("\033[92mArxSage'e geçiş yapılıyor...\033[0m")
                        time.sleep(0.8)
                        os.system("python Distros/ArxSage/ArxSage.py")
                        break
                    elif distro.lower() == "depsage":
                        print("\033[92mDepSage'e geçiş yapılıyor...\033[0m")
                        time.sleep(0.8)
                        os.system("python Distros/DepSage/DepSage.py")
                        break
                    else:
                        print("\033[93mGeçersiz distro! Arxsage veya DepSage yazın.\033[0m")
                        
                elif cmd in ["shutdown /r /o /t /0", "shutdown", "poweroff"]:
                    print("\033[91mAstraSage kapatılıyor...\033[0m")
                    time.sleep(1)
                    sys.exit(0)
                    
                else:
                    if cmd:  # Boş değilse
                        print("\033[93mBilinmeyen komut. Kullanılabilir komutlar: login -astrasage | distro -login <Arxsage/DepSage> | shutdown /r /o /t /0  |  join -kotlin \033[0m")
                        
            except KeyboardInterrupt:
                print("\n\033[91mKapatılıyor...\033[0m")
                sys.exit(0)
            except Exception as e:
                print(f"\033[91mHata: {e}\033[0m")  
    except KeyboardInterrupt:
        print("\n\033[93mBoot interrupted.\033[0m")
    finally:
        print("\033[?25h", end="")

if __name__ == "__main__":
    clear()
    boot_sequence()