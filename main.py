#AstraSage • By:EnderAstra
#Açık kaynaklı Terminal

#İmport değişkenleri
import random
import time
import os
import platform
import socket
import zipfile
import importlib.util
import json
import requests
import shutil
import webbrowser
import ASE
import getpass
import sys
import subprocess
from utils.code_editor import open_code_editor
from utils.updater import update_system, show_update_history
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
import importlib.util as _ilu


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

#Terminal renk kodları (ANSI)
def _tema_renkleri():
    TEMAS = {
        "yesil":   {"YESIL": "\033[92m", "KOYU_YESIL": "\033[32m", "KIRMIZI": "\033[91m", "SARI": "\033[93m"},
        "mavi":    {"YESIL": "\033[94m", "KOYU_YESIL": "\033[34m", "KIRMIZI": "\033[91m", "SARI": "\033[93m"},
        "kirmizi": {"YESIL": "\033[91m", "KOYU_YESIL": "\033[31m", "KIRMIZI": "\033[93m", "SARI": "\033[92m"},
        "sari":    {"YESIL": "\033[93m", "KOYU_YESIL": "\033[33m", "KIRMIZI": "\033[91m", "SARI": "\033[92m"},
        "mor":     {"YESIL": "\033[95m", "KOYU_YESIL": "\033[35m", "KIRMIZI": "\033[91m", "SARI": "\033[93m"},
        "turkuaz": {"YESIL": "\033[96m", "KOYU_YESIL": "\033[36m", "KIRMIZI": "\033[91m", "SARI": "\033[93m"},
    }
    tema = load_theme()
    return TEMAS.get(tema["renk"], TEMAS["yesil"])

class Renk:
    _r = _tema_renkleri()
    YESIL = _r["YESIL"]
    KOYU_YESIL = _r["KOYU_YESIL"]
    KIRMIZI = _r["KIRMIZI"]
    SARI = _r["SARI"]
    RESET = "\033[0m"
    BOLD = "\033[1m"

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

#Ana Fonksiyon
def main():
  loaded_libraries = load_data()
  installed_languages = load_installed_languages()
  komut_gecmisi = load_history()
  
  clear(os)
  banner()
  
  #Ana Döngü
  while True:
    try:
      # Kısa yol gösterimi için
      kisa_yol = mevcut_dizin[0].replace(os.path.expanduser("~"), "~")
      komut = input(f"\n {Renk.YESIL}{kisa_yol}/$>> {Renk.RESET}")
      parcalar = komut.split()
      
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
                else:
                    print("Yüklü kütüphaneler:")
                    for lib in loaded_libraries:
                        print(f"  - {lib}")
            else:
                print("Kullanım: as list -libraries")
        
        elif eylem.startswith("update"):
          if len(parcalar) < 3:
            print("Kullanım: as update -<versiyon>")
            continue
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
          time.sleep(0.6)
          clear(os)
        
        elif eylem == "encode":
          if len(parcalar) < 3:
            print("Kullanım: as encode <dosya.py>")
            continue
          dosya_yolu = parcalar[2]
          encode_to_ast(dosya_yolu)
        
        elif eylem == "help":
          time.sleep(0.3)
          help_menu()
        
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
      
      elif komut == "astra-sage-reto":
        open_advanced_panel()
      elif komut == "$arxsage":
        print("      -ArxSage Comminity-")
        show_progress_bar(20, 0.2)
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
    
    except KeyboardInterrupt:
      print("\nÇıkış yapılıyor...")
      break
    except Exception as hata:
      print(f"Bir hata oluştu: {hata}")

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
    print(f"  {cmd:<37} → {aciklama}")

#Yardım Menüsü
def help_menu():

    print(f"\n{Renk.YESIL}[ KÜTÜPHANELER ]{Renk.RESET}")
    komut("as list -libraries", "Yüklü kütüphaneleri listeler.")
    komut("as export <Kütüphane>", "Kütüphane indirir.")
    komut("as unexport <Kütüphane>", "Kütüphaneyi kaldırır.")
    komut("as export -gt <URL>", "GitHub'dan kütüphane indirir.")
    komut("asinstall <Script>", "Kodlama dilinin API'sini indirir.")

    print(f"\n{Renk.YESIL}[ GELİŞTİRME ]{Renk.RESET}")
    komut("as codeeditor", "Kod editörünü açar.")
    komut("ai <Mesaj> -run", "Yapay zekâya mesaj gönderir.")
    komut("as encode <Dosyaİsmi>", "Dosyayı .ast formatına dönüştürür.")
    komut("as update -Version", "Terminali günceller.")

    print(f"\n{Renk.YESIL}[ DOSYA SİSTEMİ ]{Renk.RESET}")
    komut("as ls <Klasör>", "Klasör içeriğini listeler.")
    komut("as cd <Klasör>", "Belirtilen klasöre geçer.")
    komut("as pwd", "Geçerli çalışma dizinini gösterir.")
    komut("as cdir <Dosyaİsmi> at <HedefYol>", "Dosyayı belirtilen konuma taşır.")
    komut("as can <Create/Delete> -Null/İsim.txt", "Dosya oluşturur veya siler.")
    komut("as <info/read> -<DosyaYolu>", "Dosya bilgilerini veya içeriğini gösterir.")

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

    print(f"\n{Renk.YESIL}[ SİSTEM ]{Renk.RESET}")
    komut("as server add", "Yeni sunucu ekler.")
    komut("as platform -get <Bilgi>", "Platform bilgilerini gösterir.")
    komut("as history", "Komut geçmişini listeler.")

#Ana Menü
def banner():
  tema = load_theme()
  
  BANNER_STILLERI = {
    "klasik":  "Astra Sage'e Hoşgeldin!!!",
    "minimal": "[ AstraSage ]",
    "bold":    "★ ASTRASAGE ★",
    "ascii":   "\n    _         _            ____\n   / \\   ___ | |_ _ __ __ / ___|  __ _  __ _  ___\n  / _ \\ / __|| __| '__/ _` \\___ \\ / _` |/ _` |/ _ \\\n / ___ \\\\__ \\| |_| | | (_| |___) | (_| | (_| |  __/\n/_/   \\_\\___/ \\__|_|  \\__,_|____/ \\__,_|\\__, |\\___|  |___/",
  }
  
  banner_metni = BANNER_STILLERI.get(tema["banner"], BANNER_STILLERI["klasik"])
  
  print(banner_metni)
  print("")
  print("=" * 50)
  print("Sistem içi Gelişmiş Seçenekler komudu:")
  print(f"  {Renk.YESIL}astra-sage-reto{Renk.RESET}")
  print(f"\n{Renk.YESIL}Sistem içi Komutlar:{Renk.RESET}")
  print("\n Ekran silmek:"f"{Renk.YESIL} as clear{Renk.RESET}")
  print(" Kütüphane listelemek:"f"{Renk.YESIL} as list{Renk.RESET}")
  print(" Yardım Komutu:"f"{Renk.YESIL} as help{Renk.RESET}")
  print(" Sistem Güncelleme:"f"{Renk.YESIL} as update -Version{Renk.RESET}")
  print("\n Github Sayfam:"f"{Renk.YESIL} https://github.com/EnderAstra7744{Renk.RESET}")
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


def arxbanner():
  print(" ArxSage'e Hoşgeldiniz")
  print("=" * 50)
  print(f''' ⣆⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠙⠻⢷⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠉⠛⢷⣦⠀⠀⠀⠀⠀⠀
 ⠀⠀⣠⣤⡾⠟⠋⠀⠀⠀⠀⠀⠀
 ⣶⡿⠟⠉⠀⠀⠀⣤⣤⣤⣤⣤⣤
 ⠁⠀⠀⠀⠀⠀⠀⠛⠛⠛⠛⠛⠛''')
  print(f"\n {Renk.YESIL} Komutlar:{Renk.RESET}")
  print("\n    Açıklamayı Okumak için: "f"{Renk.YESIL}arx information{Renk.RESET}")
  print("=" * 50)

def arxsage_distro():
  clear(os)
  arxbanner()
  
  while True:
    cmd = input(f"\n{Renk.YESIL} ~/AstraSage/ArxSage/$>>: {Renk.RESET}")
    
    pr = cmd.split()
    if pr[0] == "arx" and pr[1] == "information":
      print("Açıklama: ")
      print(f"{Renk.YESIL}Bu AstraSage'in içindeki basit bir Distro dur bu Distro siber güvenlik ve etik Hackerlık için geliştirilmiştir {Renk.RESET}")
      print(f"{Renk.KIRMIZI}NOT: Etik Hackerlık dışında kullanılması Yasal değildir{Renk.RESET}")




if __name__ == '__main__':
  main()