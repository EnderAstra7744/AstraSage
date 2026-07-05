#AstraSage AstraOcunt Modülü
#Konum: utils/astra_ocunt.py
#Amaç: 'ao <paket> -<komut>' ile servis yönetimi ve pip paket yönetimi

import subprocess
import sys
import json
import os
import threading
import importlib.util

OCUNT_FILE = "ocunt_packages.json"

# Aktif servisler: {servis_ismi: (thread, stop_event)}
_aktif_servisler = {}


def load_packages():
    if not os.path.exists(OCUNT_FILE):
        return []
    try:
        with open(OCUNT_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("packages", [])
    except Exception:
        return []


def save_packages(packages):
    try:
        with open(OCUNT_FILE, "w", encoding="utf-8") as f:
            json.dump({"packages": packages}, f, indent=2, ensure_ascii=False)
    except Exception as error:
        print(f"[HATA] Paket listesi kaydedilemedi: {error}")


def install_package(paket):
    packages = load_packages()
    if paket in packages:
        print(f"'{paket}' zaten kurulu.")
        return
    print(f"'{paket}' kuruluyor...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", paket],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            packages.append(paket)
            save_packages(packages)
            print(f"'{paket}' başarıyla kuruldu.")
        else:
            print(f"[HATA] '{paket}' kurulamadı:")
            print(result.stderr)
    except Exception as error:
        print(f"[HATA] Kurulum sırasında hata oluştu: {error}")


def remove_package(paket):
    packages = load_packages()
    if paket not in packages:
        print(f"'{paket}' AstraOcunt ile kurulmamış.")
        return
    print(f"'{paket}' kaldırılıyor...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "uninstall", paket, "-y"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            packages.remove(paket)
            save_packages(packages)
            print(f"'{paket}' başarıyla kaldırıldı.")
        else:
            print(f"[HATA] '{paket}' kaldırılamadı:")
            print(result.stderr)
    except Exception as error:
        print(f"[HATA] Kaldırma sırasında hata oluştu: {error}")


def start_service(kutuphane_ismi):
    if kutuphane_ismi in _aktif_servisler:
        print(f"'{kutuphane_ismi}' zaten çalışıyor.")
        return

    aradicaklar = [
        os.path.join("libraries", kutuphane_ismi),
        os.path.join("libraries", "gt", kutuphane_ismi),
    ]

    kutuphane_yolu = None
    for yol in aradicaklar:
        if os.path.exists(yol):
            kutuphane_yolu = yol
            break

    if kutuphane_yolu is None:
        print(f"[HATA] '{kutuphane_ismi}' kütüphanesi bulunamadı.")
        return

    try:
        spec = importlib.util.spec_from_file_location(kutuphane_ismi, kutuphane_yolu)
        modul = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modul)

        if not hasattr(modul, "service"):
            print(f"[HATA] '{kutuphane_ismi}' içinde 'service()' fonksiyonu yok.")
            print("Servis modu için kütüphanenin içine 'def service(stop_event):' fonksiyonu eklenmelidir.")
            return

        stop_event = threading.Event()

        def servis_calistir():
            try:
                modul.service(stop_event)
            except Exception as error:
                print(f"\n[SERVİS HATASI] '{kutuphane_ismi}': {error}")
            finally:
                if kutuphane_ismi in _aktif_servisler:
                    del _aktif_servisler[kutuphane_ismi]

        thread = threading.Thread(target=servis_calistir, daemon=True)
        thread.start()
        _aktif_servisler[kutuphane_ismi] = (thread, stop_event)

        print(f"'{kutuphane_ismi}' servisi başlatıldı.")
        print("Durdurmak için Enter'a basın...")
        input()
        stop_service(kutuphane_ismi)

    except Exception as error:
        print(f"[HATA] Servis başlatılırken hata oluştu: {error}")

def stop_service(kutuphane_ismi):
    if kutuphane_ismi not in _aktif_servisler:
        print(f"'{kutuphane_ismi}' şu an çalışmıyor.")
        return

    thread, stop_event = _aktif_servisler[kutuphane_ismi]
    stop_event.set()
    thread.join(timeout=3)
    
    # Zaten silinmiş olabilir (finally bloğu tarafından), kontrol et
    if kutuphane_ismi in _aktif_servisler:
        del _aktif_servisler[kutuphane_ismi]
    
    print(f"'{kutuphane_ismi}' servisi durduruldu.")


def list_services():
    if len(_aktif_servisler) == 0:
        print("Şu an çalışan bir servis yok.")
        return

    print("Aktif servisler:")
    for isim, (thread, stop_event) in _aktif_servisler.items():
        durum = "çalışıyor" if thread.is_alive() else "durdu"
        print(f"  - {isim} [{durum}]")


def list_packages():
    packages = load_packages()
    if len(packages) == 0:
        print("Henüz AstraOcunt ile kurulmuş bir paket yok.")
        return
    print("AstraOcunt ile kurulu paketler:")
    for paket in packages:
        print(f"  - {paket}")


def run_ao_command(parcalar):
    if len(parcalar) < 2:
        print("Kullanım:")
        print("  ao <kütüphane> -start    → servisi arka planda başlatır")
        print("  ao <kütüphane> -stop     → servisi durdurur")
        print("  ao services              → aktif servisleri listeler")
        print("  ao <paket> -install      → pip paketi kurar")
        print("  ao <paket> -remove       → pip paketini kaldırır")
        print("  ao list                  → kurulu paketleri listeler")
        return

    if parcalar[1] == "list":
        list_packages()
        return

    if parcalar[1] == "services":
        list_services()
        return

    if len(parcalar) < 3:
        print("Kullanım: ao <paket/kütüphane> -<komut>")
        return

    hedef = parcalar[1]
    komut = parcalar[2].lstrip("-").lower()

    if komut == "start":
        start_service(hedef)
    elif komut == "stop":
        stop_service(hedef)
    elif komut == "install":
        install_package(hedef)
    elif komut == "remove":
        remove_package(hedef)
    else:
        print(f"[HATA] '{komut}' geçersiz bir AstraOcunt komutu.")
        print("Geçerli komutlar: -start, -stop, -install, -remove")