import os, sys, time, shutil, getpass
from datetime import datetime
import platform

RESET="\033[0m"; CYAN="\033[36m"; YELLOW="\033[33m"; RED="\033[41;37m"; SEL="\033[42;37m"

def clear(): print("\033[H\033[J", end="")

def header():
    print(CYAN+r"""
    ___         __            ____                 
   /   |  _____/ /________ _ / __/____ _____ ____ 
  / /| | / ___/ __/ ___/ _ `/\ \/ __ `/ __ `/ _ \
 / ___ |(__  ) /_/ /  / (_/ /___/ /_/ / /_/ /  __/
/_/  |_/____/\__/_/   \__,_//____\__,_/\__, /\___/
                                      /____/
"""+RESET)
    print(YELLOW+"="*60+RESET)
    print(f"Kullanıcı: {getpass.getuser()} | Python: {sys.version.split()[0]} | Saat: {datetime.now():%H:%M:%S}")
    print(YELLOW+"="*60+RESET)

def neofetch():
                print(r"""
    _         _
   / \   ___ | |_ _ __ __ _
  / _ \ / __|| __| '__/ _` |
 / ___ \\__ \| |_| | | (_| |
/_/   \_\___/ \__|_|  \__,_|

     ____                  
    / ___|  __ _  __ _  ___
    \___ \ / _` |/ _` |/ _ \
     ___) | (_| | (_| |  __/
    |____/ \__,_|\__, |\___|
                  |___/
""")

                print(f" OS           : AstraSage")
                print(f" Current Path : {os.getcwd()}")
                print(f" User         : {getpass.getuser()}")
                print(f" Hostname     : {platform.node()}")
                print(f" Kernel       : {platform.system()}")
                print(f" Release      : {platform.release()}")
                print(f" Machine      : {platform.machine()}")
                print(f" Processor    : {platform.processor()}")
                print(f" Python       : {platform.python_version()}")
                print(f" Architecture : {platform.architecture()[0]}")

                print("-" * 60)
                print("AstraSage • By EnderAstra")

def boot():
    os.system("python as_kernel.py")

def clock():
    n=datetime.now()
    print(n.strftime("%d.%m.%Y %H:%M:%S"))

def settings():
    print("Tema: Dark\nDil: TR\nLog: INFO")

opts=["System Boot", "System NoeFetch"]
cur=0
while True:
    clear(); header()
    for i,o in enumerate(opts):
        if i==cur: print(f"{SEL} ➤  [{i+1}] {o:<40} {RESET}")
        else: print(f"   [{i+1}] {o}")
    print("\n1-5 seç, Enter çalıştır, q çıkış")
    s=input(fr"~\$/>> ").strip().lower()
    if s.isdigit():
        n=int(s)-1
        if 0<=n<len(opts): cur=n
        else:
            input("Geçersiz numara.")
    elif s in ("","enter"):
        clear(); header()
        try:
            if cur==0: boot()
            elif cur==1: neofetch()
        except Exception as e:
            print(RED,f"Hata: {e}",RESET)
        input("\nDevam etmek için Enter...")
    elif s=="q":
        break
