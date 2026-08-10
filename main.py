#CREDITS:
#AstraSage • By:EnderAstra
#Açık kaynaklı Terminal

#INFORMATION:
#AstraSage'in Ana Dosyası main.py
#NOT:
#  Herhangi Bir Bilgi Dosyasını Okumadan Sistem Dosyalarını Değiştirmeyiniz!!
#Örn: README.md, LICENSE gibi

#PYTHON CODE:

#İmport değişkenleri
import random
import time
import os
import platform
import socket
import zipfile
import importlib.util
import json
import re
import requests
import shutil
import webbrowser
import ASE
import getpass
import sys
import subprocess
import readline
import traceback
from utils.code_editor import open_code_editor
from utils.at_helper import extract_at_target, resolve_target_path
from utils.cdir import cdir_file
from utils.ast_format import encode_to_ast, decode_ast
from utils.astra_ai import run_ai_command, learn_new_example
from utils.server_manager import add_server, delete_server, list_servers
from utils.can_command import run_can_command
from utils.astra_ocunt import run_ao_command
from utils.api_manager import run_api_command
from utils.read_info import read_file, info_file
from utils.astra_security import tara
from Distros.ArxSage.ArxSage import run
from Distros.DepSage.DepSage import dep_run
import importlib.util as _ilu
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit import prompt
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from utils.alias_manager import load_aliases, save_aliases, add_alias, remove_alias, list_aliases, resolve_alias
from utils.android_helper import run_android_command
from utils.system_reset import run_system_command
from utils.distro_manager import distro_manager
from utils.neofetch import show_neofetch
from utils.doctor import doctor_target, doctor_system
from utils.repair import repair_target, repair_system
from python.python.python import run_python_command
from python.pip.pip import run_pip_command
from utils.as_tree import run_tree

DISTRO = "AstraSage"
distro_manager.load(sys.modules[__name__])
distro = distro_manager.distro
ALL_COMMANDS = []
START_TIME = time.time()

# ============================================================
# AstraSage Completion Menü Stili
# ============================================================
ASTRASAGE_STYLE = Style.from_dict({
    # Completion menüsü
    "completion-menu":
        "bg:#000000 #00FF00",

    # Normal komutlar
    "completion-menu.completion":
        "bg:#000000 #00FF00",

    # Seçili komut
    "completion-menu.completion.current":
        "bg:#00FF00 #000000 bold",

    # Meta alanı
    "completion-menu.meta":
        "bg:#000000 #00FF00",

    # Seçili meta alanı
    "completion-menu.meta.current":
        "bg:#00FF00 #000000 bold",

    # Scrollbar
    "scrollbar.background":
        "bg:#000000",

    "scrollbar.button":
        "bg:#00FF00",
})

COMMAND_TREE = {
    "as": {
        "!system": {
            "-reset": {
                "/s": {}
            },
            # ==================================================
            # ASTRA SAGE DOCTOR
            # ==================================================
            "doctor": {
                "--K-AstraSage": "__DIRS__",
                "--F-AstraSage": "__FILES__"
            },
            # ==================================================
            # ASTRA SAGE REPAIR
            # ==================================================
            "repair": {
                "--system": {},
                "--file": "__FILES__",
                "--folder": "__DIRS__"
            }
        },
        # ======================================================
        # ALIAS
        # ======================================================
        "alias": {
            "list": {},
            "remove": {}
        },
        # ======================================================
        # ANDROID
        # ======================================================
        "android": {
            "-notify": {},
            "-copy": {},
            "-paste": {},
            "-share": "__FILES__",
            "-vibrate": {}
        },
        "help": {},
        "clear": {},
        # ======================================================
        # LIBRARIES
        # ======================================================
        "list": {
            "-libraries": {}
        },
        # ======================================================
        # HISTORY
        # ======================================================
        "history": {
            "-clear": {}
        },
        # ======================================================
        # SYSTEM
        # ======================================================
        "sys": {
            "--distro": {},
            "--version": {},
            # ==================================================
            # NEOFETCH
            # ==================================================
            "-neofetch": {
                "--ascii_logo=": {},
                "--text_color=": {},
                "--logo_color=": {},
                "--separator=": {},
                "--show_cpu=": {
                    "true": {},
                    "false": {}
                },
                "--show_memory=": {
                    "true": {},
                    "false": {}
                },
                "--show_pip=": {
                    "true": {},
                    "false": {}
                },
                "--config": {}
            }
        },
        # ======================================================
        # DOSYA / KLASÖR
        # ======================================================
        "cd": "__DIRS__",
        "ls": "__DIRS__",
        "pwd": {},
        # ======================================================
        # LIBRARY EXPORT
        # ======================================================
        "export": "__LIBRARIES__",
        "unexport": "__LIBRARIES__",
        # ======================================================
        # PYTHON
        # ======================================================
        "python": {
           "run": "__FILES__",
           "exec": {},
           "--version": {},
           "shell": {},
           "info": {},
           "doctor": {},
           "module": {},
        },
        "pip": {
           "install": {},
           "uninstall": {},
           "upgrade": {},
           "list": {},
           "show": {},
           "freeze": {},
           "--version": {},
           "doctor": {},
        },
        
        # ======================================================
        # UPDATE
        # ======================================================
        "update": {},
        # ======================================================
        # CODE EDITOR
        # ======================================================
        "codeeditor": {},
        # ======================================================
        # FILE TOOLS
        # ======================================================
        "encode": "__FILES__",
        "read": "__FILES__",
        "info": "__FILES__",
        # ==========================================================
        # TREE
        # ==========================================================
        "tree": {
           "--file-system": {},
           "--as-commands": {},
           "--help": {},
        },
        # ======================================================
        # ASINSTALL
        # ======================================================
        "asinstall": {
            "python": {},
            "json": {},
        },
        # ======================================================
        # PLATFORM
        # ======================================================
        "platform": {
            "-get": {
                "name": {},
                "version": {},
                "machine": {},
                "processor": {},
                "node": {},
                "bit": {},
                "all": {}
            }
        },
        # ======================================================
        # SERVER
        # ======================================================
        "server": {
            "add": {},
            "delete": {},
            "list": {}
        }
    },
    # ==========================================================
    # ASTRA AI
    # ==========================================================
    "ai": {},
    # ==========================================================
    # ASTRA OCUNT
    # ==========================================================
    "ao": {
        "services": {
            "-stop": {},
            "-start": {},
        },
    },
    # ==========================================================
    # ASTRA API
    # ==========================================================
    "as-api": {},
    # ==========================================================
    # DISTROS
    # ==========================================================
    "$arxsage": {},
    "$depsage": {},
    "$devsage": {},
    "$linuxsage": {},
    # ==========================================================
    # LAUNCHER
    # ==========================================================
    "\\launcher": {},
    # ==========================================================
    # RETO
    # ==========================================================
    "astra-sage-reto": {}, 
}


def _gorunur_uzunluk(s):
       return len(re.sub(r'\x1b\[[0-9;]*m', '', s))
class AstraSageCompleter(Completer):

    def __init__(self, command_tree):
        self.command_tree = command_tree

    def _flatten_tree(self, tree, prefix=""):
        commands = []

        if not isinstance(tree, dict):
            return commands

        for command, children in tree.items():

            command = str(command).strip()

            if not command:
                continue

            current = command

            if prefix:
                current = f"{prefix} {command}"

            commands.append(current)

            if isinstance(children, dict) and children:
                commands.extend(
                    self._flatten_tree(
                        children,
                        current
                    )
                )

        return commands

    def get_completions(self, document, complete_event):

        text = document.text_before_cursor
        current = text.strip()

        commands = self._flatten_tree(
            self.command_tree
        )

        commands = sorted(set(commands))

        for command in commands:

            if command.lower().startswith(
                current.lower()
            ):

                yield Completion(
                command,
                start_position=-len(current),
                display=command,
                )
kb = KeyBindings()
# ============================================================
# AstraSage OC (Old Command) sistemi
# ============================================================

old_commands = []
oc_index = -1


def add_old_command(command):
    """Çalıştırılan gerçek komutu eski komut listesine ekler."""
    command = command.strip()

    if not command:
        return

    # OC komutlarının kendisini geçmişe ekleme
    if command.lower() == "oc":
        return

    old_commands.append(command)


def get_old_command():
    """
    En son eski komutu getirir.
    Sonraki çağrılarda geriye doğru gider.
    """
    global oc_index

    if not old_commands:
        return None

    if oc_index == -1:
        oc_index = len(old_commands) - 1
    elif oc_index > 0:
        oc_index -= 1

    return old_commands[oc_index]


def reset_oc():
    """OC gezinme konumunu sıfırlar."""
    global oc_index
    oc_index = -1
session = PromptSession(
    key_bindings=kb,
    completer=AstraSageCompleter(COMMAND_TREE),
    complete_while_typing=True,
    style=ASTRASAGE_STYLE,
    complete_in_thread=True
)

did_you_mean = False
mevcut_dizin = [os.getcwd()]
ASTRASAGE_KOK = os.getcwd()  # AstraSage'in gerçek kök dizini, hiç değişmez

TEMA_DOSYASI = os.path.join(ASTRASAGE_KOK, "assets", "astrasage_theme.json")

def load_theme():
    if not os.path.exists(TEMA_DOSYASI):
        return {"renk": "yesil", "banner": "klasik"}
    try:
        with open(TEMA_DOSYASI, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"renk": "yesil", "banner": "klasik"}

HISTORY_FILE = os.path.join(ASTRASAGE_KOK, "assets", "history.json")

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("history", [])
    except Exception:
        return []

def save_history(history):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump({"history": history}, f, indent=2, ensure_ascii=False)
    except Exception:
        pass
# ============================================================
# ASTRA SAGE ANSI RENK SİSTEMİ
# ============================================================

def _tema_renkleri():

    TEMAS = {

        "yesil": {
            "YESIL": "\033[92m",
            "KOYU_YESIL": "\033[32m",
            "KIRMIZI": "\033[91m",
            "SARI": "\033[93m",

            "BG_TEMA": "\033[102m",
            "BG_KOYU_TEMA": "\033[42m",
        },

        "mavi": {
            "YESIL": "\033[94m",
            "KOYU_YESIL": "\033[34m",
            "KIRMIZI": "\033[91m",
            "SARI": "\033[93m",

            "BG_TEMA": "\033[104m",
            "BG_KOYU_TEMA": "\033[44m",
        },

        "kirmizi": {
            "YESIL": "\033[91m",
            "KOYU_YESIL": "\033[31m",
            "KIRMIZI": "\033[93m",
            "SARI": "\033[92m",

            "BG_TEMA": "\033[101m",
            "BG_KOYU_TEMA": "\033[41m",
        },

        "sari": {
            "YESIL": "\033[93m",
            "KOYU_YESIL": "\033[33m",
            "KIRMIZI": "\033[91m",
            "SARI": "\033[92m",

            "BG_TEMA": "\033[103m",
            "BG_KOYU_TEMA": "\033[43m",
        },

        "mor": {
            "YESIL": "\033[95m",
            "KOYU_YESIL": "\033[35m",
            "KIRMIZI": "\033[91m",
            "SARI": "\033[93m",

            "BG_TEMA": "\033[105m",
            "BG_KOYU_TEMA": "\033[45m",
        },

        "turkuaz": {
            "YESIL": "\033[96m",
            "KOYU_YESIL": "\033[36m",
            "KIRMIZI": "\033[91m",
            "SARI": "\033[93m",

            "BG_TEMA": "\033[106m",
            "BG_KOYU_TEMA": "\033[46m",
        },
    }

    tema = load_theme()

    return TEMAS.get(
        tema.get("renk", "yesil"),
        TEMAS["yesil"]
    )


class Renk:

    # ========================================================
    # TEMA
    # ========================================================

    _TEMA = _tema_renkleri()

    YESIL = _TEMA["YESIL"]
    KOYU_YESIL = _TEMA["KOYU_YESIL"]
    KIRMIZI = _TEMA["KIRMIZI"]
    SARI = _TEMA["SARI"]

    BG_TEMA = _TEMA["BG_TEMA"]
    BG_KOYU_TEMA = _TEMA["BG_KOYU_TEMA"]

    # ========================================================
    # TEMEL RENKLER
    # ========================================================

    SIYAH = "\033[30m"
    MAVI = "\033[34m"
    MOR = "\033[35m"
    TURKUAZ = "\033[36m"
    BEYAZ = "\033[37m"

    # ========================================================
    # PARLAK RENKLER
    # ========================================================

    ACIK_SIYAH = "\033[90m"
    ACIK_KIRMIZI = "\033[91m"
    ACIK_YESIL = "\033[92m"
    ACIK_SARI = "\033[93m"
    ACIK_MAVI = "\033[94m"
    ACIK_MOR = "\033[95m"
    ACIK_TURKUAZ = "\033[96m"
    ACIK_BEYAZ = "\033[97m"

    # ========================================================
    # BİÇİMLENDİRME
    # ========================================================

    RESET = "\033[0m"
    KALIN = "\033[1m"
    SOLUK = "\033[2m"
    ITALIK = "\033[3m"
    ALT_CIZGI = "\033[4m"
    TERS = "\033[7m"

    # ========================================================
    # NORMAL ARKA PLANLAR
    # ========================================================

    BG_SIYAH = "\033[38;5;236m"
    BG_KIRMIZI = "\033[41m"
    BG_YESIL = "\033[42m"
    BG_SARI = "\033[43m"
    BG_MAVI = "\033[44m"
    BG_MOR = "\033[45m"
    BG_TURKUAZ = "\033[46m"
    BG_BEYAZ = "\033[47m"

    # ========================================================
    # PARLAK ARKA PLANLAR
    # ========================================================

    BG_ACIK_SIYAH = "\033[100m"
    BG_ACIK_KIRMIZI = "\033[101m"
    BG_ACIK_YESIL = "\033[102m"
    BG_ACIK_SARI = "\033[103m"
    BG_ACIK_MAVI = "\033[104m"
    BG_ACIK_MOR = "\033[105m"
    BG_ACIK_TURKUAZ = "\033[106m"
    BG_ACIK_BEYAZ = "\033[107m"
    
def load_dynamic_commands():
    """commands/ ve packages/ içindeki tüm komutları yükler."""
    dinamik_komutlar = {}
    
    for klasor in ["commands", "packages"]:
        tam_yol = os.path.join(ASTRASAGE_KOK, klasor)
        if not os.path.exists(tam_yol):
            continue
        for isim in os.listdir(tam_yol):
            alt_yol = os.path.join(tam_yol, isim, "main.py")
            if os.path.exists(alt_yol):
                dinamik_komutlar[isim] = alt_yol
    return dinamik_komutlar
    
def complete_command(text):
    parts = text.split()

    if text.endswith(" "):
        parts.append("")

    tree = COMMAND_TREE

    for part in parts[:-1]:

        # Dosya / klasör düğümüne geldiysek dur
        if tree in ("__DIRS__", "__FILES__", "__LIBRARIES__"):
            break

        if isinstance(tree, dict) and part in tree:
            tree = tree[part]
        else:
            return text

    current = parts[-1]

    # ----------------------------
    # Klasör Tamamlama
    # ----------------------------
    if tree == "__DIRS__":

        try:
            klasorler = [
                d for d in os.listdir(mevcut_dizin[0])
                if os.path.isdir(os.path.join(mevcut_dizin[0], d))
            ]
        except:
            return text

        matches = [
            d for d in klasorler
            if d.startswith(current)
        ]

    # ----------------------------
    # Dosya Tamamlama
    # ----------------------------
    elif tree == "__FILES__":

        try:
            dosyalar = [
                f for f in os.listdir(mevcut_dizin[0])
                if os.path.isfile(os.path.join(mevcut_dizin[0], f))
            ]
        except:
            return text

        matches = [
            f for f in dosyalar
            if f.startswith(current)
        ]

    # ----------------------------
    # Libraries Tamamlama
    # ----------------------------
    elif tree == "__LIBRARIES__":

        kutuphane_klasoru = os.path.join(ASTRASAGE_KOK, "libraries")

        if os.path.exists(kutuphane_klasoru):
            kutuphaneler = os.listdir(kutuphane_klasoru)
        else:
            kutuphaneler = []

        matches = [
            k for k in kutuphaneler
            if k.startswith(current)
        ]

    # ----------------------------
    # Normal Komut Tamamlama
    # ----------------------------
    else:

        matches = [
            key
            for key in tree.keys()
            if key.startswith(current)
        ]

    if len(matches) == 1:
        parts[-1] = matches[0]
        return " ".join(parts) + " "

    return text
    
from prompt_toolkit.document import Document

@kb.add(" ")
def _(event):
    buffer = event.app.current_buffer
    text = buffer.text
    before = text
    after = ""
    if text.lower() == "oc":
    	old_command = get_old_command()
    	if old_command is None:
    	   buffer.text = "oc "
    	   buffer.cursor_position = len(buffer.text)
    	   return
    	buffer.text = old_command
    	buffer.cursor_position = len(old_command)
    	return
    
    if text.startswith("as cd "):
        yeni = complete_directory(text)
    elif text.startswith("as ls "):
        yeni = complete_directory(text)
    elif text.startswith("as read "):
        yeni = complete_file(text)
    elif text.startswith("as info "):
        yeni = complete_file(text)
    elif text.startswith("as encode "):
        yeni = complete_file(text)
    elif text.startswith("as export "):
        yeni = complete_library(text)
    else:
        yeni = complete_command(text)
    if yeni != text:
        from prompt_toolkit.document import Document
        buffer.document = Document(
            text=yeni,
            cursor_position=len(yeni)
        )
    else:
        buffer.insert_text(" ")

def build_command_tree():
    tree = {}
    for command in ALL_COMMANDS:
        words = command.split()
        current = tree
        for word in words:
            if word not in current:
                current[word] = {}
            current = current[word]
    return tree

def complete_directory(text):
    import os
    parts = text.split()
    if len(parts) < 3:
        return text
    current = parts[-1]
    try:
        klasorler = [
            x for x in os.listdir(mevcut_dizin[0])
            if os.path.isdir(os.path.join(mevcut_dizin[0], x))
        ]
    except:
        return text
    matches = [k for k in klasorler if k.startswith(current)]
    if len(matches) == 1:
        parts[-1] = matches[0]
        return " ".join(parts) + " "
    return text
    
def complete_file(text):
    import os
    parts = text.split()
    if len(parts) < 3:
        return text
    current = parts[-1]
    try:
        dosyalar = os.listdir(mevcut_dizin[0])
    except:
        return text
    matches = [d for d in dosyalar if d.startswith(current)]
    if len(matches) == 1:
        parts[-1] = matches[0]
        return " ".join(parts) + " "
    return text

def complete_library(text):
    import os
    parts = text.split()
    if len(parts) < 3:
        return text
    current = parts[-1]
    klasor = os.path.join(ASTRASAGE_KOK, "libraries")
    try:
        libs = os.listdir(klasor)
    except:
        return text
    matches = [l for l in libs if l.startswith(current)]
    if len(matches) == 1:
        parts[-1] = matches[0]
        return " ".join(parts) + " "
    return text

def get_prompt():
    yol = mevcut_dizin[0]

    # Android yolunu kısalt
    yol = yol.replace("/storage/emulated/0", "~")

    return ANSI(f"{Renk.YESIL}{yol}/$>> {Renk.RESET}")

#Ana Fonksiyon
def main():
  COMMAND_TREE = build_command_tree()
  aliases = load_aliases()
  loaded_libraries = load_data()
  installed_languages = load_installed_languages()
  komut_gecmisi = load_history()
  
  clear(os)
  banner()
  
  #Ana Döngü
  while True:
    try:
      # Kısa yol gösterimi için
      komut = session.prompt(get_prompt())
      komut = resolve_alias(komut, aliases)
      parcalar = komut.split()
      add_old_command(komut)
      reset_oc()
      
      
      if len(parcalar) == 0:
        print("Lütfen bir komut girin.")
        continue
      
      # Geçmişe ekle (as history ve boş komutlar hariç)
      if komut.strip() and komut.strip() != "as history":
        komut_gecmisi.append(komut.strip())
        if len(komut_gecmisi) > 100:  # maksimum 100 komut tut
          komut_gecmisi = komut_gecmisi[-100:]
        save_history(komut_gecmisi)
      if parcalar[0] == "asinstall":
        if len(parcalar) < 2 or len(parcalar) > 2:
          print("Kullanım: asinstall <script>")
          continue
        kısım = parcalar[1]
        install_language(kısım, installed_languages)
      elif parcalar[0] == "as-api":
        run_api_command(parcalar)
      elif parcalar[0] == "ao":
        run_ao_command(parcalar)
      elif parcalar[0] == "ai":
        run_ai_command(parcalar)
      elif parcalar[0] == "as" and len(parcalar) >= 2 and parcalar[1] == "!system":
        if parcalar[2] == "-reset":
        	run_system_command(parcalar)
        # as !system doctor ...
        if len(parcalar) >= 3 and parcalar[2] == "doctor":

            if len(parcalar) < 4:
                print("[!] Usage: as !system doctor --target")
                continue

            target = parcalar[3]

           # --system
            if target == "--system":

                doctor_system(ASTRASAGE_KOK)

            # --K-folder
            elif target.startswith("--K-"):

                folder_name = target[4:]

                folder_path = os.path.join(
                    ASTRASAGE_KOK,
                    folder_name
                )

                doctor_target(folder_path)

            # --F-file
            elif target.startswith("--F-"):

                file_name = target[4:]

                file_path = os.path.join(
                    ASTRASAGE_KOK,
                    file_name
                )

                doctor_target(file_path)

            else:

                print(
                    "[!] Unknown doctor target."
                )

            continue
        
        if len(parcalar) >= 3 and parcalar[2] == "repair":

            if len(parcalar) < 4:
                print("[!] Usage: as !system repair --target")
                continue

            target = parcalar[3]

            # --system
            if target == "--system":

                repair_system(ASTRASAGE_KOK)

            # --K-folder
            elif target.startswith("--K-"):

                folder_name = target[4:]

                folder_path = os.path.join(
                    ASTRASAGE_KOK,
                    folder_name
                )

                repair_target(folder_path)

            # --F-file
            elif target.startswith("--F-"):

                file_name = target[4:]

                file_path = os.path.join(
                    ASTRASAGE_KOK,
                    file_name
                 )

                repair_target(file_path)

            else:

                print(
                    "[!] Unknown repair target."
                )

            continue
      elif parcalar[0] == "as":
        if len(parcalar) < 2:
          print("Bunu Demeyi mi Çalıştın?")
          help_menu()
          continue
          
        eylem = parcalar[1]
        
        
        if eylem == "list":
            if len(parcalar) >= 3 and parcalar[2] == "-libraries":
                if len(loaded_libraries) == 0:
                    print("Henüz hiçbir kütüphane yüklenmedi.")
                    continue
                else:
                    print("Yüklü kütüphaneler:")
                    for lib in loaded_libraries:
                        print(f"  - {lib}")
            else:
                print("Kullanım: as list -libraries")
        
        elif eylem == "update":
               if len(parcalar) < 3:
                   print("Kullanım:")
                   print("  as update -cheak updates     → Güncelleme var mı kontrol eder")
                   print("  as update -nowversion        → GitHub'dan güncellemeyi uygular")
                   print("  as update -<versiyon>        → Eski tar.gz yöntemi (uyumluluk için)")
                   continue
    
               alt = parcalar[2].lstrip("-").lower()
               if alt == "cheak" and len(parcalar) >= 4 and parcalar[3].lower() == "updates":
               	from utils.updater import check_updates
               	check_updates()
               elif alt == "nowversion":
                       from utils.updater import update_nowversion
                       update_nowversion()
               else:
                    # Eski sistem (tar.gz)
                    from utils.updater import update_system
                    versiyon = parcalar[2].lstrip("-")
                    update_system(versiyon)
        elif eylem == "server":
          if len(parcalar) < 3:
            print("Kullanım: as server add  |  as server delete <port>  |  as server add -<html/css/js> <dosya>")
            continue
          alt_komut = parcalar[2]
          if alt_komut == "add":
            if len(parcalar) >= 5 and parcalar[3].startswith("-"):
              dosya_turu = parcalar[3].lstrip("-")
              dosya_ismi = parcalar[4]
              add_server(dosya_turu, dosya_ismi)
            else:
              add_server()
          elif alt_komut == "delete":
            if len(parcalar) < 4:
              print("Kullanım: as server delete <port>")
              continue
            delete_server(parcalar[3])
          elif alt_komut == "list":
            list_servers()
          else:
            print(f"[HATA] '{alt_komut}' geçersiz bir server eylemi.")
        
        elif eylem == "cd":
          hedef = parcalar[2] if len(parcalar) >= 3 else ""
          if not hedef:
            print(f"Şu an: {mevcut_dizin[0]}")
            continue
          if hedef == "..":
            yeni_dizin = os.path.dirname(mevcut_dizin[0])
          else:
            yeni_dizin = os.path.join(mevcut_dizin[0], hedef)
          if not os.path.isdir(yeni_dizin):
            print(f"[HATA] '{hedef}' klasörü bulunamadı.")
            continue
          mevcut_dizin[0] = yeni_dizin
          print(f"→ {mevcut_dizin[0]}")
        
        elif eylem == "ls":
          hedef_klasor = parcalar[2] if len(parcalar) >= 3 else mevcut_dizin[0]
          try:
            icerik = os.listdir(hedef_klasor)
            if len(icerik) == 0:
              print("(boş klasör)")
            else:
              for item in sorted(icerik):
                tam_yol = os.path.join(hedef_klasor, item)
                if os.path.isdir(tam_yol):
                  print(f"{Renk.YESIL}[K] {item}/{Renk.RESET}")
                else:
                  print(f"    {item}")
          except Exception as hata:
            print(f"[HATA] {hata}")
        elif eylem == "tree":
        	run_tree(parcalar[2:])
        elif eylem == "python":
          subcommand = (
              parcalar[2]
              if len(parcalar) >= 3
              else "info"
          )

          args = (
              parcalar[3:]
              if len(parcalar) >= 4
              else []
          )

          run_python_command(
              subcommand,
              args
          )

          continue
        
        elif eylem == "pip":
          subcommand = (
              parcalar[2]
              if len(parcalar) >= 3
              else "info"
          )

          args = (
              parcalar[3:]
              if len(parcalar) >= 4
              else []
          )

          run_pip_command(
              subcommand,
              args
          )

          continue
        elif eylem == "sys":
            if len(parcalar) < 3:
                print("Kullanım: as sys -neofetch")
                continue
            if parcalar[2] == "--distro":
            	try:
            		print(f"{Renk.YESIL} AstraSage Dağıtımı: {distro.name}{Renk.RESET}")
            		continue
            	except NameError:
            		print(f"{Renk.KIRMIZI} DISTRO Değişkeni Bulunamadı!!{Renk.RESET}")
            		continue
            if parcalar[2] == "--version":
            	try:
            		print(f"{Renk.YESIL} AstraSage VERSIYONU: {VERSION}{Renk.RESET}")
            		continue
            	except NameError:
            		print(f"{Renk.KIRMIZI} VERSION Değişkeni Bulunamadı!!{Renk.RESET}")
            		continue
            uptime = int(time.time() - START_TIME)
            saat = uptime // 3600
            dakika = (uptime % 3600) // 60
            saniye = uptime % 60

            if parcalar[2] == "-neofetch":
                neofetch_args = parcalar[3:]

                try:

                    from utils.neofetch import (
                        run_neofetch_command
                    )

                    run_neofetch_command(
                        args=neofetch_args,
                        distro=DISTRO,
                    )

                except Exception as e:

                    print(
                        f"\033[91m"
                        f"[AstraSage Neofetch Error] "
                        f"{e}"
                        f"\033[0m"
                    )
            else:
                print(
                    f"'{parcalar[2]}' "
                    f"geçersiz bir sys komutudur."
                )

        elif eylem == "pwd":
            print(mevcut_dizin[0])
        elif eylem == "codeeditor":
          open_code_editor(installed_languages)
        elif eylem == "read":
          if len(parcalar) < 3:
            print("Kullanım: as read -<dosya yolu>")
            continue
          dosya_yolu = parcalar[2].lstrip("-")
          read_file(dosya_yolu)
        
        elif eylem == "info":
          if len(parcalar) < 3:
            print("Kullanım: as info -<dosya yolu>")
            continue
          dosya_yolu = parcalar[2].lstrip("-")
          info_file(dosya_yolu)
        elif eylem == "unexport":
          if len(parcalar) < 3:
            print("Kullanım: as unexport <kütüphane>")
            continue
          target = parcalar[2]
          unexport_library(target, loaded_libraries)
        
        elif eylem == "platform":
          if len(parcalar) < 4:
            print("Kullanım: as platform -get <Command>")
            print(f"\n{Renk.YESIL}Platform Komutları:{Renk.RESET}")
            print("  as platform -get name")
            print("  as platform -get version")
            print("  as platform -get machine")
            print("  as platform -get processor")
            print("  as platform -get node")
            print("  as platform -get bit")
            print("  as platform -get all")
            continue
          if parcalar[2] == "-get" and parcalar[3] == "all":
            print(f"\nPlaform-İsmi: {platform.system().upper()}")
            print(f"Platform Versiyonu: {platform.version().upper()}")
            print(f"Makine Bilgisi: {platform.machine()}")
            print(f"İşlemci Adı: {platform.processor()}")
            print(f"Cihaz Adı: {platform.node()}")
            print(f"Bit: {platform.architecture()[0]}")
          elif parcalar[2] == "-get" and parcalar[3] == "name":
            print(f"Plaform-İsmi: {platform.system().upper()}")
          elif parcalar[2] == "-get" and parcalar[3] == "version":
            print(f"Platform Versiyonu: {platform.version().upper()}")
          elif parcalar[2] == "-get" and parcalar[3] == "machine":
            print(f"Makine Bilgisi: {platform.machine()}")
          elif parcalar[2] == "-get" and parcalar[3] == "processor":
            print(f"İşlemci Adı: {platform.processor()}")
          elif parcalar[2] == "-get" and parcalar[3] == "node":
            print(f"Cihaz Adı: {platform.node()}")
          elif parcalar[2] == "-get" and parcalar[3] == "bit":
            print(f"Bit: {platform.architecture()[0]}")
          else:
            print(f"({parcalar[3]}) Adında Böyle bir bilgi bulunamadı")
        
        elif eylem == "clear":
          print("Ekran Siliniyor...")
          show_progress_bar()
          clear(os)
          banner()
          continue
        
        elif eylem == "encode":
          if len(parcalar) < 3:
            print("Kullanım: as encode <dosya.py>")
            continue
          dosya_yolu = parcalar[2]
          encode_to_ast(dosya_yolu)
        
        elif eylem == "help":
          time.sleep(0.3)
          help_menu()
          continue
        elif eylem == "cdir":
          if len(parcalar) < 3:
            print("Kullanım: as cdir <dosya ismi> at <yeni yol>")
            continue
          temiz_parcalar, at_hedef = extract_at_target(parcalar)
          if at_hedef in (None, "__INVALID__"):
            print("Kullanım: as cdir <dosya ismi> at <yeni yol>")
            continue
          dosya_ismi = temiz_parcalar[2]
          cdir_file(dosya_ismi, at_hedef)
        elif eylem == "android":
        	run_android_command(parcalar)
        elif eylem == "alias":
          if len(parcalar) < 3:
            print('Kullanım: as alias <isim>="<komut>"  |  as alias list  |  as alias remove <isim>')
            continue
          if parcalar[2] == "list":
            list_aliases(aliases)
          elif parcalar[2] == "remove":
            if len(parcalar) < 4:
              print("Kullanım: as alias remove <isim>")
              continue
            remove_alias(parcalar[3], aliases)
          else:
            ham_metin = komut.split(" ", 2)[2]
            add_alias(ham_metin, aliases)

        elif eylem == "can":
          run_can_command(parcalar)
        elif eylem == "history":
          if len(parcalar) >= 3 and parcalar[2] == "-clear":
            komut_gecmisi.clear()
            save_history(komut_gecmisi)
            print("Komut geçmişi temizlendi.")
          else:
            gosterilecek = int(parcalar[2]) if len(parcalar) >= 3 and parcalar[2].isdigit() else len(komut_gecmisi)
            son_komutlar = komut_gecmisi[-gosterilecek:]
            if not son_komutlar:
              print("Henüz komut geçmişi yok.")
            else:
              print(f"\n{Renk.YESIL}Komut Geçmişi:{Renk.RESET}")
              for i, k in enumerate(son_komutlar, start=len(komut_gecmisi) - len(son_komutlar) + 1):
                print(f"  {i:3}  {k}")
        elif eylem == "export":
          if len(parcalar) < 3:
            print("Kullanım: as export <hedef>  veya  as export -gt <link>")
            continue
          temiz_parcalar, at_hedef = extract_at_target(parcalar)
          if at_hedef == "__INVALID__":
            continue
          if temiz_parcalar[2] == "-gt":
            if len(temiz_parcalar) < 4:
              print("Kullanım: as export -gt <link>")
              continue
            link = temiz_parcalar[3]
            download_from_github(link, loaded_libraries, at_hedef)
          else:
            target = temiz_parcalar[2]
            # Kök dizinden libraries/ klasörünü kullan, mevcut_dizin'den değil
            target_path = os.path.join(ASTRASAGE_KOK, "libraries", target)
            load_library(target_path, loaded_libraries, target, at_hedef)
        else:
          print(f"'{eylem}' adında bir eylem bulunamadı.")
          continue
       
      elif komut == r"\\launcher":
        clear(os)
        return
      elif komut == "astra-sage-reto":
        open_advanced_panel()
      elif komut == "$depsage":  
        print("      -DepSage Comminity-")  
        show_progress_bar(20, 0.05)  
        dep_yolu = os.path.join(ASTRASAGE_KOK, "Distros", "DepSage", "DepSage.py")  
        if not os.path.exists(dep_yolu):  
          print("[HATA] ArxSage bulunamadı. Distros/DepSage/DepSage.py mevcut olmalı.")  
        else:  
          spec = importlib.util.spec_from_file_location("DepSage", dep_yolu)  
          dep_mod = importlib.util.module_from_spec(spec)  
          spec.loader.exec_module(dep_mod)  
          dep_mod.dep_run()  
          # ArxSage'den döndükten sonra AstraSage banner'ını tekrar göster  
          clear(os)  
          banner()  
      elif komut == "$linuxsage":
        print("      -LinuxSage Comminity-")
        show_progress_bar(20, 0.05)
        linux_yolu = os.path.join(ASTRASAGE_KOK, "Distros", "LinuxSage", "LinuxSage.py")

        if not os.path.exists(linux_yolu):
            print("[HATA] LinuxSage bulunamadı. Distros/LinuxSage/LinuxSage.py mevcut olmalı.")
        else:
            eski_dizin = os.getcwd()
            try:
                linux_dizin = os.path.dirname(linux_yolu)
                os.chdir(linux_dizin)
                spec = importlib.util.spec_from_file_location("LinuxSage", linux_yolu)
                linux_mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(linux_mod)
                linux_mod.run()
            except Exception as e:
            	print(f"[HATA] LinuxSage çalıştırılırken hata oluştu: {e}")
            finally:
            	# LinuxSage'den çıkınca AstraSage'in dizinine geri dön
                os.chdir(eski_dizin)
            # LinuxSage'den döndükten sonra AstraSage banner'ını tekrar göster
            clear(os)
            banner()
      elif komut == "$devsage":
        print("      -DevSage Comminity-")  
        show_progress_bar(20, 0.05)  
        dev_yolu = os.path.join(ASTRASAGE_KOK, "Distros", "DevSage", "DevSage.py")  
        if not os.path.exists(dev_yolu):  
          print("[HATA] DevSage bulunamadı. Distros/DevSage/DevSage.py mevcut olmalı.")  
        else:  
          spec = importlib.util.spec_from_file_location("DevSage", dev_yolu)  
          dev_mod = importlib.util.module_from_spec(spec)  
          spec.loader.exec_module(dev_mod)  
          dev_mod.run()  
          # DevSage'den döndükten sonra AstraSage banner'ını tekrar göster  
          clear(os)  
          banner()
      elif komut == "$arxsage":  
        print("      -ArxSage Comminity-")  
        show_progress_bar(20, 0.05)  
        arx_yolu = os.path.join(ASTRASAGE_KOK, "Distros", "ArxSage", "ArxSage.py")  
        if not os.path.exists(arx_yolu):  
          print("[HATA] ArxSage bulunamadı. Distros/ArxSage/ArxSage.py mevcut olmalı.")  
        else:  
          spec = importlib.util.spec_from_file_location("ArxSage", arx_yolu)  
          arx_mod = importlib.util.module_from_spec(spec)  
          spec.loader.exec_module(arx_mod)  
          arx_mod.run()  
          # ArxSage'den döndükten sonra AstraSage banner'ını tekrar göster  
          clear(os)  
          banner()
      
      else:
        # Dinamik komut mu?
        dinamik_komutlar = load_dynamic_commands()
        if parcalar[0] in dinamik_komutlar:
          try:
            spec = importlib.util.spec_from_file_location(
              parcalar[0], dinamik_komutlar[parcalar[0]]
            )
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, "run"):
              mod.run(parcalar)
            else:
              print(f"[HATA] '{parcalar[0]}' içinde run() fonksiyonu yok.")
          except Exception as hata:
            print(f"[HATA] '{parcalar[0]}' çalıştırılırken hata: {hata}")
        else:
          print(f"[HATA] '{parcalar[0]}' Adında bir komut Bulunamadı.")
          time.sleep(0.2)
          print("Tüm Komutları görmek için 'as help' Komutunu çalıştıra Bilirsiniz.")
    
    except Exception as hata:
      print(f"Bir hata oluştu: {hata}")
    except KeyboardInterrupt:
      print("\nÇıkış yapılıyor...")
      break
    

def show_progress_bar(toplam_adim=15, gecikme=0.05):
    for adim in range(toplam_adim + 1):
        yuzde = int((adim / toplam_adim) * 100)
        dolu = "#" * adim
        bos = "-" * (toplam_adim - adim)
        sys.stdout.write(f"\r%{yuzde:<3}[{dolu}{bos}]")
        sys.stdout.flush()
        time.sleep(gecikme)
    print()

def komut(cmd, aciklama):
    ALL_COMMANDS.append((cmd, aciklama))
    print(f"  {cmd:<37} → {aciklama}")

#Yardım Menüsü
def help_menu():

    print(f"\n{Renk.YESIL}[ KÜTÜPHANELER ]{Renk.RESET}")
    komut("as list -libraries", "Yüklü kütüphaneleri listeler.")
    komut("as export <Kütüphane>", "Kütüphane indirir.")
    komut("as unexport <Kütüphane>", "Kütüphaneyi kaldırır.")
    komut("as export -gt <URL>", "GitHub'dan kütüphane indirir.")
    komut("asinstall <Script>", "Kodlama dilinin API'sini indirir.")
    
    print(f"\n{Renk.YESIL}[ GÜNCELLEME ]{Renk.RESET}")
    komut("as update -cheak updates","Güncelleme var mı kontrol eder")
    komut("as update -nowversion","GitHub'dan güncellemeyi uygular")
    komut("as update -<versiyon>","Eski tar.gz yöntemi (uyumluluk için)")

    print(f"\n{Renk.YESIL}[ GELİŞTİRME ]{Renk.RESET}")
    komut("as codeeditor", "Kod editörünü açar.")
    komut("ai <Mesaj> -run", "Yapay zekâya mesaj gönderir.")
    komut("as encode <Dosyaİsmi>", "Dosyayı .ast formatına dönüştürür.")
    komut("as update -Version", "Terminali günceller.")
    
    print(f"\n{Renk.YESIL}[ PYTHON ]{Renk.RESET}")
    komut("as python run <Dosya>", "Python dosyasını çalıştırır.")
    komut("as python exec <Kod>", "Python kodunu çalıştırır.")
    komut("as python --version", "Python sürümünü gösterir.")
    komut("as python shell", "Python çalıştırıcısının yolunu gösterir.")
    komut("as python info", "Python hakkında bilgi verir.")
    komut("as python doctor", "Python Da Sorun Varmı Kontrol Eder")
    komut("as python module", "Python Modülü hakkında bilgi verir.")

    print(f"\n{Renk.YESIL}[ PIP ]{Renk.RESET}")
    komut("as pip install <Paket>", "Python paketi yükler.")
    komut("as pip uninstall <Paket>", "Python paketini kaldırır.")
    komut("as pip upgrade <Paket>", "Python paketini günceller.")
    komut("as pip list", "Yüklü Python paketlerini listeler.")
    komut("as pip show <Paket>", "Python paketi hakkında bilgi gösterir.")
    komut("as pip freeze", "Kurulu Python paketlerini listeler.")
    komut("as pip --version", "Pip sürümünü gösterir.")
    komut("as pip doctor", "Pip Hatalarını Kontrol eder ve 'gösterir.")

    print(f"\n{Renk.YESIL}[ DOSYA SİSTEMİ ]{Renk.RESET}")
    komut("as ls <Klasör>", "Klasör içeriğini listeler.")
    komut("as cd <Klasör>", "Belirtilen klasöre geçer.")
    komut("as pwd", "Geçerli çalışma dizinini gösterir.")
    komut("as cdir <Dosyaİsmi> at <HedefYol>", "Dosyayı belirtilen konuma taşır.")
    komut("as can <Create/Delete> -Null/İsim.txt", "Dosya oluşturur veya siler.")
    komut("as read -<DosyaYolu>", "içeriğini gösterir.")
    komut("as info -<DosyaYolu>", "Dosya bilgilerini gösterir.")

    print(f"\n{Renk.YESIL}[ PAKET YÖNETİCİSİ ]{Renk.RESET}")
    komut("ao <Paket> -install", "Paketi yükler.")
    komut("ao <Paket> -remove", "Paketi kaldırır.")
    komut("ao <Paket> -search", "Paketi arar.")
    komut("ao list", "Yüklü paketleri listeler.")

    print(f"\n{Renk.YESIL}[ SERVİSLER ]{Renk.RESET}")
    komut("ao services/folder.py -start", "Servisi başlatır.")
    komut("ao services/folder.py -stop", "Servisi durdurur.")

    print(f"\n{Renk.YESIL}[ API ]{Renk.RESET}")
    komut("as-api -<isim.cf> -<link/install>", "Komut dosyasını yükler.")
    komut("as-api list", "Yüklü komut dosyalarını listeler.")
    komut("as-api remove", "Komut dosyasını kaldırır.")

    print(f"\n{Renk.YESIL}[ BİLGİ ]{Renk.RESET}")
    komut("as server add", "Yeni sunucu ekler.")
    komut("as platform -get <Bilgi>", "Platform bilgilerini gösterir.")
    komut("as history", "Komut geçmişini listeler.")
    
    print(f"\n{Renk.YESIL}[ SİSTEM ]{Renk.RESET}")
    komut("as sys -neofetch", "Sistem hakkında bilgi verir.")
    komut("as sys --version", "AstraSage sürümünü gösterir.")
    komut("as sys --distro", "Aktif AstraSage dağıtımını gösterir.")    
    
    print(f"\n{Renk.YESIL}[ ALIAS ]{Renk.RESET}")
    komut('as alias <isim>="<komut>"', "Yeni kısayol tanımlar.")
    komut("as alias list", "Tanımlı kısayolları listeler.")
    komut("as alias remove <isim>", "Kısayolu siler.")

    print(f"\n{Renk.YESIL}[ ANDROID ]{Renk.RESET}")
    komut("as android -notify <mesaj>", "Bildirim gönderir.")
    komut("as android -copy <metin>", "Panoya kopyalar.")
    komut("as android -paste", "Pano içeriğini gösterir.")
    komut("as android -share <dosya>", "Dosyayı paylaşım menüsüyle paylaşır.")
    komut("as android -vibrate <ms>", "Cihazı titreştirir.")
    

#Ana Menü
def banner():
  tema = load_theme()
  
  BANNER_STILLERI = {
    "klasik":  " Astra Sage'e Hoşgeldin!!!",
    "minimal": " [ AstraSage ]",
    "bold":    " ★ ASTRASAGE ★",
    "ascii":   "\n    _         _            ____\n   / \\   ___ | |_ _ __ __ / ___|  __ _  __ _  ___\n  / _ \\ / __|| __| '__/ _` \\___ \\ / _` |/ _` |/ _ \\\n / ___ \\\\__ \\| |_| | | (_| |___) | (_| | (_| |  __/\n/_/   \\_\\___/ \\__|_|  \\__,_|____/ \\__,_|\\__, |\\___|  |___/",
  }
  
  banner_metni = BANNER_STILLERI.get(tema["banner"], BANNER_STILLERI["klasik"])
  
  print(banner_metni)
  print("")
  print("=" * 50)
  print("Sistem içi Gelişmiş Seçenekler komudu:")
  print(f"  {Renk.YESIL}- astra-sage-reto{Renk.RESET}")
  print(f"\n{Renk.YESIL}Sistem içi Komutlar:{Renk.RESET}")
  print("\n - Ekran silmek:"f"{Renk.YESIL} as clear{Renk.RESET}")
  print(" - Kütüphane listelemek:"f"{Renk.YESIL} as list -libraries{Renk.RESET}")
  print(" - Yardım Komutu:"f"{Renk.YESIL} as help{Renk.RESET}")
  print(" - Sistem Güncelleme:"f"{Renk.YESIL} as update -Version{Renk.RESET}")
  print("\n -- Github Sayfam:"f"{Renk.YESIL} https://github.com/EnderAstra7744{Renk.RESET}")
  print("=" * 50)
  
def clear(os):
  if platform.system() == "Windows":
    os.system('cls')
  else:
    os.system('clear')
def has_run_function(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
        return "def run(" in content
    except Exception:
        return False

def load_library(path, loaded_libraries, display_name=None, at_hedef=None):
    if display_name is None:
        display_name = path
    if display_name in loaded_libraries:
        print(f"'{display_name}' kütüphanesi loaded_libraries.json da zaten bulunmakta.")
    
    if not os.path.exists(path):
        print(f"'{display_name}' kütüphanesi bulunamadı.")
        return
    
    # AstraSecurity taraması
    if not tara(path):
        print(f"[AstraSecurity] '{display_name}' güvenlik taramasından geçemedi, yüklenmedi.")
        return
    if path.endswith(".ast"):
        kod_metni = decode_ast(path)
        if kod_metni is None:
            return
        if "def run(" not in kod_metni:
            print(f"'{display_name}' AstraSage formatına uygun değil (run() fonksiyonu yok). Güvenlik için çalıştırılmadı.")
            return
        try:
            namespace = {}
            exec(kod_metni, namespace)
            if not display_name in loaded_libraries:
                print(f"'{display_name}' kütüphanesi yüklendi.")
            loaded_libraries.append(display_name)
            save_data(loaded_libraries)
            if "run" in namespace:
                namespace["run"]()
            else:
                print(f"'{display_name}' içinde çalıştırılabilir bir 'run()' fonksiyonu bulunamadı.")
            if at_hedef:
                resolved = resolve_target_path(at_hedef)
                if resolved:
                    try:
                        dosya_adi = os.path.basename(path)
                        hedef_dosya_yolu = os.path.join(resolved, dosya_adi)
                        shutil.copy(path, hedef_dosya_yolu)
                        print(f"Ayrıca '{display_name}' şuraya kopyalandı: {hedef_dosya_yolu}")
                    except Exception as error:
                        print(f"[HATA] 'at' hedefine kopyalama başarısız: {error}")
        except Exception as error:
            print(f"'{display_name}' çalıştırılırken hata oluştu: {error}")
        return
    
    if not has_run_function(path):
        print(f"'{display_name}' AstraSage formatına uygun değil (run() fonksiyonu yok). Güvenlik için çalıştırılmadı.")
        return
    
    try:
        spec = importlib.util.spec_from_file_location(display_name, path)
        module = importlib.util.module_from_spec(spec)
        if not display_name in loaded_libraries:
          print(f"'{display_name}' kütüphanesi yüklendi.")
        loaded_libraries.append(display_name)
        save_data(loaded_libraries)
        spec.loader.exec_module(module)
        if hasattr(module, "run"):
            module.run()
        else:
            print(f"'{display_name}' içinde çalıştırılabilir bir 'run()' fonksiyonu bulunamadı.")
        if at_hedef:
            resolved = resolve_target_path(at_hedef)
            if resolved:
                try:
                    dosya_adi = os.path.basename(path)
                    hedef_dosya_yolu = os.path.join(resolved, dosya_adi)
                    shutil.copy(path, hedef_dosya_yolu)
                    print(f"Ayrıca '{display_name}' şuraya kopyalandı: {hedef_dosya_yolu}")
                except Exception as error:
                  print(f"[HATA] 'at' hedefine kopyalama başarısız: {error}")
    except Exception as error:
        print(f"'{display_name}' yüklenirken hata oluştu: {error}")

def convert_to_raw_url(url):
    if "github.com" in url and "/blob/" in url:
        url = url.replace("github.com", "raw.githubusercontent.com")
        url = url.replace("/blob/", "/")
    return url

def download_from_github(url, loaded_libraries, at_hedef=None):
    url = convert_to_raw_url(url)
    file_name = url.split("/")[-1]
    if not file_name.endswith(".py"):
        print(f"Bu link bir .py dosyasına işaret etmiyor gibi görünüyor: '{file_name}'")
        print("Lütfen GitHub'daki dosyanın 'Raw' linkini kullan (örn: .../main/dosya.py)")
        return
    gt_folder = os.path.join(ASTRASAGE_KOK, "libraries", "gt")
    os.makedirs(gt_folder, exist_ok=True)
    library_path = os.path.join(gt_folder, file_name)
    try:
        print(f"'{file_name}' GitHub'dan indiriliyor...")
        response = requests.get(url)
        if response.status_code != 200:
            print(f"İndirme başarısız. Sunucu yanıtı: {response.status_code}")
            return
        with open(library_path, "w", encoding="utf-8") as file:
            file.write(response.text)
        print(f"'{file_name}' başarıyla indirildi.")
        
        # AstraSecurity taraması
        if not tara(library_path):
            print(f"[AstraSecurity] '{file_name}' güvenlik taramasından geçemedi, yüklenmedi.")
            return
        
        load_library(library_path, loaded_libraries, file_name, at_hedef)
    except Exception as error:
        print(f"GitHub'dan indirme sırasında hata oluştu: {error}")

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("loaded_libraries", [])
    except Exception as error:
        print(f"data.json okunurken hata oluştu: {error}")
        return []

def save_data(loaded_libraries):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump({"loaded_libraries": loaded_libraries}, file, indent=2, ensure_ascii=False)
    except Exception as error:
        print(f"data.json kaydedilirken hata oluştu: {error}")

#==================== GELİŞMİŞ SEÇENEKLER PANELİ ====================

def open_advanced_panel():
    print("Gelişmiş Seçenekler Paneli açılıyor...")
    show_progress_bar(20, 0.2)
    while True:
        clear(os)
        print(Renk.YESIL + Renk.BOLD)
        print("=" * 50)
        print("        GELİŞMİŞ SEÇENEKLER PANELİ")
        print("=" * 50)
        print(Renk.RESET)
        print(Renk.KOYU_YESIL + "  [1] Sistem" + Renk.RESET)
        print(Renk.KOYU_YESIL + "  [2] Giriş" + Renk.RESET)
        print(Renk.KOYU_YESIL + "  [3] Comunity" + Renk.RESET)
        print(Renk.KOYU_YESIL + "  [4] Folders" + Renk.RESET)
        print(Renk.KIRMIZI + "  [5] Çıkış" + Renk.RESET)
        print(Renk.YESIL + "=" * 50 + Renk.RESET)
        secim = input("\nSeçiminiz: ").strip()
        if secim == "1":
            show_system_info()
        elif secim == "2":
            show_login()
        elif secim == "3":
            open_community()
        elif secim == "4":
            open_folders()
        elif secim == "5":
            print("Gelişmiş Seçenekler Panelinden çıkılıyor...")
            show_progress_bar()
            time.sleep(0.8)
            clear(os)
            banner()
            break
        else:
            print(Renk.KIRMIZI + "Geçersiz seçim, lütfen 1-5 arası bir sayı girin." + Renk.RESET)
            time.sleep(1)

def show_system_info():
    clear(os)
    print(Renk.YESIL + "=" * 50)
    print("            SİSTEM BİLGİSİ")
    print("=" * 50 + Renk.RESET)
    print(f"Sistem   : {platform.system()}")
    print(f"Sürüm    : {platform.release()}")
    print(f"Makine   : {platform.machine()}")
    input("\nGeri dönmek için Enter'a basın...")

def show_login():
    clear(os)
    print(Renk.SARI + "Giriş sistemi henüz geliştirme aşamasında." + Renk.RESET)
    input("\nGeri dönmek için Enter'a basın...")

def open_community():
    print(Renk.YESIL + "Tarayıcıda Comunity sayfası açılıyor..." + Renk.RESET)
    webbrowser.open("https://github.com/EnderAstra7744/AstraSage")
    time.sleep(1)

def open_folders():
    clear(os)
    print(Renk.SARI + "[⚠]: Sistemin dosyalarına giriş yapıyorsunuz." + Renk.RESET)
    cevap = input("Emin misiniz? (evet/hayır): ").strip().lower()
    if cevap == "evet":
        folders_menu()
    else:
        print("İşlem iptal edildi.")
        time.sleep(1)

def folders_menu():
    while True:
        clear(os)
        print(Renk.YESIL + Renk.BOLD)
        print("=" * 50)
        print("           DOSYA İŞLEMLERİ")
        print("=" * 50)
        print(Renk.RESET)
        print(Renk.KOYU_YESIL + "  [1] Yeni Dosya Oluştur" + Renk.RESET)
        print(Renk.KOYU_YESIL + "  [2] Dosya Kopyala" + Renk.RESET)
        print(Renk.KOYU_YESIL + "  [3] Dosya Taşı" + Renk.RESET)
        print(Renk.KIRMIZI + "  [4] Geri Dön" + Renk.RESET)
        print(Renk.YESIL + "=" * 50 + Renk.RESET)
        secim = input("\nSeçiminiz: ").strip()
        if secim == "1":
            create_new_file()
        elif secim == "2":
            copy_file()
        elif secim == "3":
            move_file()
        elif secim == "4":
            break
        else:
            print(Renk.KIRMIZI + "Geçersiz seçim." + Renk.RESET)
            time.sleep(1)

def create_new_file():
    isim = input("Oluşturulacak dosya ismini girin: ").strip()
    if not isim:
        print("İşlem iptal edildi.")
        return
    try:
        with open(isim, "w") as f:
            pass
        print(Renk.YESIL + f"'{isim}' oluşturuldu." + Renk.RESET)
    except Exception as e:
        print(Renk.KIRMIZI + f"Hata: {e}" + Renk.RESET)
    time.sleep(1.2)

def copy_file():
    kaynak = input("Kopyalanacak dosyanın tam yolunu girin: ").strip()
    if not os.path.exists(kaynak):
        print(Renk.KIRMIZI + f"'{kaynak}' bulunamadı." + Renk.RESET)
        time.sleep(1.2)
        return
    hedef = input("Hedef konumu girin: ").strip()
    try:
        shutil.copy(kaynak, hedef)
        print(Renk.YESIL + f"'{kaynak}' başarıyla kopyalandı." + Renk.RESET)
    except Exception as e:
        print(Renk.KIRMIZI + f"Hata: {e}" + Renk.RESET)
    time.sleep(1.2)

def move_file():
    kaynak = input("Taşınacak dosyanın tam yolunu girin: ").strip()
    if not os.path.exists(kaynak):
        print(Renk.KIRMIZI + f"'{kaynak}' bulunamadı." + Renk.RESET)
        time.sleep(1.2)
        return
    hedef = input("Hedef konumu girin: ").strip()
    try:
        shutil.move(kaynak, hedef)
        print(Renk.YESIL + f"'{kaynak}' başarıyla taşındı." + Renk.RESET)
    except Exception as e:
        print(Renk.KIRMIZI + f"Hata: {e}" + Renk.RESET)
    time.sleep(1.2)

def unexport_library(target, loaded_libraries):
    if target not in loaded_libraries:
        print(f"'{target}' zaten yüklü değil.")
        return
    loaded_libraries.remove(target)
    save_data(loaded_libraries)
    print(f"'{target}' yüklü kütüphaneler listesinden çıkarıldı.")

INSTALLED_LANGUAGES_FILE = "installed_languages.json"

def load_installed_languages():
    if not os.path.exists(INSTALLED_LANGUAGES_FILE):
        return []
    try:
        with open(INSTALLED_LANGUAGES_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("languages", [])
    except Exception:
        return []

def save_installed_languages(languages):
    try:
        with open(INSTALLED_LANGUAGES_FILE, "w", encoding="utf-8") as f:
            json.dump({"languages": languages}, f, indent=2, ensure_ascii=False)
    except Exception as error:
        print(f"Kurulu diller kaydedilirken hata oluştu: {error}")

def check_python_installed():
    try:
        result = subprocess.run(
            [sys.executable, "--version"],
            capture_output=True, text=True, timeout=3
        )
        return result.returncode == 0
    except Exception:
        return False

def install_language(kisim, installed_languages):
    if kisim in installed_languages:
        print(f"'{kisim}' zaten kurulu.")
        return
    if kisim == "python":
        if check_python_installed():
            installed_languages.append(kisim)
            save_installed_languages(installed_languages)
            print("Python API doğrulandı ve aktif edildi.")
            print("Artık bu scripti yazabilirsiniz.")
        else:
            print("[HATA] Python kurulu bulunamadı.")
    elif kisim == "java":
        print("[HATA] Java kurulumu şu an desteklenmiyor.")
        print("(JDK indirme/kurma bu ortamda güvenli şekilde yapılamıyor.)")
    elif kisim == "json":
        installed_languages.append(kisim)
        save_installed_languages(installed_languages)
        print("JSON desteği aktif edildi.")
        print("Artık code editor'de JSON dosyası yazabilirsiniz.")
    else:
        print(f"[HATA] '{kisim}' API bulunamadı!")

if __name__ == '__main__':
  main()