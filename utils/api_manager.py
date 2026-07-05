#AstraSage as-api Modülü
#Konum: utils/api_manager.py
#Amaç: 'as-api -<isim.cf> -<link/install>' komutu ile yeni komutları indirip kurmak

import os
import json
import zipfile
import requests

COMMANDS_FOLDER = "commands"
CF_FOLDER = os.path.join("assets", "cf")


def load_installed_commands():
    """Kurulu komutların listesini döner."""
    kayit = os.path.join(COMMANDS_FOLDER, "installed.json")
    if not os.path.exists(kayit):
        return {}
    try:
        with open(kayit, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_installed_commands(komutlar):
    """Kurulu komutlar listesini kaydeder."""
    os.makedirs(COMMANDS_FOLDER, exist_ok=True)
    kayit = os.path.join(COMMANDS_FOLDER, "installed.json")
    try:
        with open(kayit, "w", encoding="utf-8") as f:
            json.dump(komutlar, f, indent=2, ensure_ascii=False)
    except Exception as error:
        print(f"[HATA] Komut listesi kaydedilemedi: {error}")


def install_cf(cf_yolu, komut_ismi):
    """
    Verilen .cf dosyasını açıp commands/<komut_ismi>/ klasörüne kurar.
    """
    if not os.path.exists(cf_yolu):
        print(f"[HATA] '{cf_yolu}' bulunamadı.")
        return False

    hedef_klasor = os.path.join(COMMANDS_FOLDER, komut_ismi)

    if os.path.exists(hedef_klasor):
        print(f"[HATA] '{komut_ismi}' komutu zaten kurulu.")
        return False

    try:
        with zipfile.ZipFile(cf_yolu, "r") as zf:
            icerik = zf.namelist()

            if "main.py" not in icerik:
                print(f"[HATA] '{cf_yolu}' geçerli bir .cf dosyası değil (main.py eksik).")
                return False

            os.makedirs(hedef_klasor, exist_ok=True)
            zf.extractall(hedef_klasor)

        print(f"'{komut_ismi}' komutu kuruldu: {hedef_klasor}")

        komutlar = load_installed_commands()
        komutlar[komut_ismi] = {"cf_dosyasi": cf_yolu}
        save_installed_commands(komutlar)
        return True

    except zipfile.BadZipFile:
        print(f"[HATA] '{cf_yolu}' geçerli bir ZIP/CF arşivi değil.")
        return False
    except Exception as error:
        print(f"[HATA] Kurulum sırasında hata oluştu: {error}")
        return False


def download_and_install_cf(komut_ismi, link):
    """
    Verilen linkten .cf dosyasını indirir ve kurar.
    """
    os.makedirs(CF_FOLDER, exist_ok=True)
    cf_yolu = os.path.join(CF_FOLDER, f"{komut_ismi}.cf")

    print(f"'{komut_ismi}.cf' indiriliyor...")
    try:
        response = requests.get(link, timeout=10)
        if response.status_code != 200:
            print(f"[HATA] İndirme başarısız. Sunucu yanıtı: {response.status_code}")
            return
        with open(cf_yolu, "wb") as f:
            f.write(response.content)
        print(f"'{komut_ismi}.cf' indirildi.")
    except Exception as error:
        print(f"[HATA] İndirme sırasında hata oluştu: {error}")
        return

    install_cf(cf_yolu, komut_ismi)


def remove_command(komut_ismi):
    """
    Kurulu bir komutu kaldırır (commands/ klasöründen siler).
    .cf dosyasına dokunmaz.
    """
    import shutil
    komutlar = load_installed_commands()

    if komut_ismi not in komutlar:
        print(f"[HATA] '{komut_ismi}' kurulu değil.")
        return

    hedef_klasor = os.path.join(COMMANDS_FOLDER, komut_ismi)
    try:
        if os.path.exists(hedef_klasor):
            shutil.rmtree(hedef_klasor)
        del komutlar[komut_ismi]
        save_installed_commands(komutlar)
        print(f"'{komut_ismi}' komutu kaldırıldı.")
    except Exception as error:
        print(f"[HATA] Kaldırma sırasında hata oluştu: {error}")


def list_commands():
    """Kurulu komutları listeler."""
    komutlar = load_installed_commands()
    if not komutlar:
        print("Henüz kurulu bir komut yok.")
        return
    print("Kurulu komutlar:")
    for isim in komutlar:
        print(f"  - {isim}")


def run_api_command(parcalar):
    """
    Ana döngüden çağrılacak giriş noktası.
    Sözdizimi: as-api -<isim.cf> -<link/install>
    """
    if len(parcalar) < 3:
        print("Kullanım:")
        print("  as-api -<isim.cf> -<indirme linki>   → indirir ve kurar")
        print("  as-api -<isim.cf> -install            → assets/cf/ içinden kurar")
        print("  as-api list                           → kurulu komutları listeler")
        print("  as-api remove -<komut ismi>           → komutu kaldırır")
        return

    if parcalar[1] == "list":
        list_commands()
        return

    if parcalar[1] == "remove":
        if len(parcalar) < 3:
            print("Kullanım: as-api remove -<komut ismi>")
            return
        komut_ismi = parcalar[2].lstrip("-")
        remove_command(komut_ismi)
        return

    cf_arg = parcalar[1].lstrip("-")          # örn: "aspi.cf"
    islem_arg = parcalar[2].lstrip("-")        # örn: link veya "install"

    if not cf_arg.endswith(".cf"):
        print(f"[HATA] '{cf_arg}' geçerli bir .cf dosya ismi değil.")
        return

    komut_ismi = cf_arg.replace(".cf", "")     # "aspi.cf" → "aspi"

    if islem_arg == "install":
        # assets/cf/ içindeki hazır .cf dosyasını kur
        cf_yolu = os.path.join(CF_FOLDER, cf_arg)
        install_cf(cf_yolu, komut_ismi)
    else:
        # Dışarıdan indirip kur
        download_and_install_cf(komut_ismi, islem_arg)
