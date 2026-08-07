#AstraSage aspi Komutu
#Açıklama: AstraSage Paket Yükleyici (Astra Sage Package Installer)

import os
import json
import zipfile
import shutil
import requests

PACKAGES_FOLDER = "packages"
PC_FOLDER = os.path.join("assets", "pc")


def load_installed_packages():
    kayit = os.path.join(PACKAGES_FOLDER, "installed.json")
    if not os.path.exists(kayit):
        return {}
    try:
        with open(kayit, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_installed_packages(paketler):
    os.makedirs(PACKAGES_FOLDER, exist_ok=True)
    kayit = os.path.join(PACKAGES_FOLDER, "installed.json")
    try:
        with open(kayit, "w", encoding="utf-8") as f:
            json.dump(paketler, f, indent=2, ensure_ascii=False)
    except Exception as error:
        print(f"[HATA] Paket listesi kaydedilemedi: {error}")


def export_package(paket_ismi, link):
    """Dışarıdan .pc dosyasını indirir ve kurar."""
    os.makedirs(PC_FOLDER, exist_ok=True)
    pc_yolu = os.path.join(PC_FOLDER, f"{paket_ismi}.pc")

    print(f"'{paket_ismi}.pc' indiriliyor...")
    try:
        response = requests.get(link, timeout=10)
        if response.status_code != 200:
            print(f"[HATA] İndirme başarısız. Sunucu yanıtı: {response.status_code}")
            return
        with open(pc_yolu, "wb") as f:
            f.write(response.content)
        print(f"'{paket_ismi}.pc' indirildi.")
    except Exception as error:
        print(f"[HATA] İndirme sırasında hata oluştu: {error}")
        return

    install_package(paket_ismi, pc_yolu)


def install_package(paket_ismi, pc_yolu=None):
    """assets/pc/ içindeki .pc dosyasını kurar."""
    if pc_yolu is None:
        pc_yolu = os.path.join(PC_FOLDER, f"{paket_ismi}.pc")

    if not os.path.exists(pc_yolu):
        print(f"[HATA] '{pc_yolu}' bulunamadı.")
        return

    paketler = load_installed_packages()
    if paket_ismi in paketler:
        print(f"'{paket_ismi}' zaten kurulu.")
        return

    hedef_klasor = os.path.join(PACKAGES_FOLDER, paket_ismi)

    try:
        with zipfile.ZipFile(pc_yolu, "r") as zf:
            os.makedirs(hedef_klasor, exist_ok=True)
            zf.extractall(hedef_klasor)

        paketler[paket_ismi] = {"pc_dosyasi": pc_yolu}
        save_installed_packages(paketler)
        print(f"'{paket_ismi}' paketi kuruldu: {hedef_klasor}")

        # Paketin kendi kurulum scriptini çalıştır (varsa)
        setup_script = os.path.join(hedef_klasor, "setup.py")
        if os.path.exists(setup_script):
            print(f"'{paket_ismi}' kurulum scripti çalıştırılıyor...")
            exec(open(setup_script).read())

    except zipfile.BadZipFile:
        print(f"[HATA] '{pc_yolu}' geçerli bir ZIP/PC arşivi değil.")
    except Exception as error:
        print(f"[HATA] Kurulum sırasında hata oluştu: {error}")


def remove_package(paket_ismi):
    """Paketi kaldırır ama .pc dosyasını silmez."""
    paketler = load_installed_packages()
    if paket_ismi not in paketler:
        print(f"'{paket_ismi}' kurulu değil.")
        return

    hedef_klasor = os.path.join(PACKAGES_FOLDER, paket_ismi)
    try:
        if os.path.exists(hedef_klasor):
            shutil.rmtree(hedef_klasor)
        del paketler[paket_ismi]
        save_installed_packages(paketler)
        print(f"'{paket_ismi}' kaldırıldı. (.pc dosyası korundu)")
    except Exception as error:
        print(f"[HATA] Kaldırma sırasında hata oluştu: {error}")


def unexport_package(paket_ismi):
    """Paketi kaldırır ve .pc dosyasını da siler."""
    paketler = load_installed_packages()
    if paket_ismi not in paketler:
        print(f"'{paket_ismi}' kurulu değil.")
        return

    pc_yolu = paketler[paket_ismi].get("pc_dosyasi", "")
    hedef_klasor = os.path.join(PACKAGES_FOLDER, paket_ismi)

    try:
        if os.path.exists(hedef_klasor):
            shutil.rmtree(hedef_klasor)
        if pc_yolu and os.path.exists(pc_yolu):
            os.remove(pc_yolu)
            print(f"'{paket_ismi}.pc' silindi.")
        del paketler[paket_ismi]
        save_installed_packages(paketler)
        print(f"'{paket_ismi}' tamamen kaldırıldı.")
    except Exception as error:
        print(f"[HATA] Kaldırma sırasında hata oluştu: {error}")


def list_packages():
    paketler = load_installed_packages()
    if not paketler:
        print("Henüz kurulu bir paket yok.")
        return
    print("Kurulu paketler:")
    for isim in paketler:
        print(f"  - {isim}")


def run(parcalar=None):
    """
    aspi komutunun giriş noktası.
    Sözdizimi: aspi <paket> -export/<link> | -remove | -unexport | -install
    """
    if parcalar is None or len(parcalar) < 2:
        print("Kullanım:")
        print("  aspi <paket> -export <link>   → indirir ve kurar")
        print("  aspi <paket> -install         → assets/pc/ içinden kurar")
        print("  aspi <paket> -remove          → paketi kaldırır (.pc kalır)")
        print("  aspi <paket> -unexport        → paketi ve .pc'yi siler")
        print("  aspi list                     → kurulu paketleri listeler")
        return

    if parcalar[1] == "list":
        list_packages()
        return

    if len(parcalar) < 3:
        print("Kullanım: aspi <paket> -<komut>")
        return

    paket_ismi = parcalar[1]
    bayrak = parcalar[2].lstrip("-").lower()

    if bayrak == "export":
        if len(parcalar) < 4:
            print("Kullanım: aspi <paket> -export <link>")
            return
        link = parcalar[3]
        export_package(paket_ismi, link)
    elif bayrak == "install":
        install_package(paket_ismi)
    elif bayrak == "remove":
        remove_package(paket_ismi)
    elif bayrak == "unexport":
        unexport_package(paket_ismi)
    else:
        print(f"[HATA] '{bayrak}' geçersiz bir aspi komutu.")
        print("Geçerli bayraklar: -export, -install, -remove, -unexport")
