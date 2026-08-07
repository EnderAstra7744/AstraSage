"""
utils/aspa_manager.py
ASPA (Astra Sage Package App) - AstraSage'in uygulama sistemi.

Iki komut:
  aspi -install                      -> ASPA motorunu AstraSage'e kurar (tek seferlik)
  aspa install <isim> <dosya_yolu>   -> bir .aspa uygulamasini kurar
  aspa run <isim>                    -> kurulu uygulamayi calistirir
  aspa remove <isim>                 -> kurulu uygulamayi kaldirir
  aspa list                          -> kurulu uygulamalari listeler
  aspa info <isim>                   -> uygulamanin manifest bilgisini gosterir

.aspa DOSYA FORMATI (zip arsivi):
  <giris_dosyasi>.py   -> zorunlu, manifest'teki "entry" alaninda belirtilir
  manifest.json        -> zorunlu: name, version, entry (opsiyonel: author, description)
  README.md            -> opsiyonel

NOT: Bu modul utils.astra_security.tara() fonksiyonunu kullanarak her
kurulumdan once guvenlik taramasi yapar; tarama gecmezse uygulama
kurulmaz.
"""

import os
import json
import shutil
import zipfile

ASTRASAGE_KOK = os.getcwd()
APPS_KLASORU = os.path.join(ASTRASAGE_KOK, "Apps")
KAYIT_DOSYASI = os.path.join(ASTRASAGE_KOK, "aspa_registry.json")
DURUM_DOSYASI = os.path.join(ASTRASAGE_KOK, "aspa_state.json")

YESIL = "\033[92m"
KIRMIZI = "\033[91m"
SARI = "\033[93m"
RESET = "\033[0m"

ZORUNLU_MANIFEST_ALANLARI = ("name", "version", "entry")


# ==================== ORTAK YARDIMCI FONKSIYONLAR ====================

def _json_yukle(yol, varsayilan):
    if not os.path.exists(yol):
        return varsayilan
    try:
        with open(yol, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return varsayilan


def _json_kaydet(yol, veri):
    try:
        with open(yol, "w", encoding="utf-8") as f:
            json.dump(veri, f, indent=2, ensure_ascii=False)
        return True
    except Exception as hata:
        print(f"{KIRMIZI}[HATA] '{yol}' kaydedilemedi: {hata}{RESET}")
        return False


def _kayit_yukle():
    return _json_yukle(KAYIT_DOSYASI, {})


def _kayit_kaydet(veri):
    return _json_kaydet(KAYIT_DOSYASI, veri)


def _aspa_kurulu_mu():
    return _json_yukle(DURUM_DOSYASI, {}).get("installed", False)


# ==================== ASPI (motor kurulumu) ====================

def aspi_install():
    if _aspa_kurulu_mu():
        print(f"{SARI}[i] ASPA sistemi zaten kurulu.{RESET}")
        return
    os.makedirs(APPS_KLASORU, exist_ok=True)
    if not os.path.exists(KAYIT_DOSYASI):
        _kayit_kaydet({})
    _json_kaydet(DURUM_DOSYASI, {"installed": True})
    print(f"{YESIL}ASPA sistemi kuruldu. Artik 'aspa install <isim> <dosya_yolu>' kullanabilirsin.{RESET}")


def run_aspi_command(parcalar):
    """main.py icinden cagrilir: parcalar[0] == 'aspi'"""
    if len(parcalar) < 2 or parcalar[1].lstrip("-") != "install":
        print(f"{KIRMIZI}Kullanim: aspi -install{RESET}")
        return
    aspi_install()


# ==================== MANIFEST DOGRULAMA ====================

def _manifest_dogrula(pc_zip, isim):
    if "manifest.json" not in pc_zip.namelist():
        print(f"{KIRMIZI}[HATA] '{isim}' paketinde manifest.json yok.{RESET}")
        return None
    try:
        manifest = json.loads(pc_zip.read("manifest.json").decode("utf-8"))
    except Exception as hata:
        print(f"{KIRMIZI}[HATA] manifest.json okunamadi: {hata}{RESET}")
        return None

    eksikler = [alan for alan in ZORUNLU_MANIFEST_ALANLARI if alan not in manifest]
    if eksikler:
        print(f"{KIRMIZI}[HATA] manifest.json eksik alanlar iceriyor: {', '.join(eksikler)}{RESET}")
        return None

    if manifest["entry"] not in pc_zip.namelist():
        print(f"{KIRMIZI}[HATA] manifest'te belirtilen giris dosyasi ('{manifest['entry']}') arsivde yok.{RESET}")
        return None

    return manifest


# ==================== ASPA (uygulama yonetimi) ====================

def aspa_install(isim, dosya_yolu):
    if not isim or not dosya_yolu:
        print(f"{KIRMIZI}Kullanim: aspa install <isim> <dosya_yolu>{RESET}")
        return

    if not os.path.exists(dosya_yolu):
        print(f"{KIRMIZI}[HATA] '{dosya_yolu}' bulunamadi.{RESET}")
        return

    if not dosya_yolu.endswith(".aspa"):
        print(f"{KIRMIZI}[HATA] Sadece .aspa dosyalari kurulabilir.{RESET}")
        return

    # AstraSecurity taramasi
    try:
        from utils.astra_security import tara
        if not tara(dosya_yolu):
            print(f"{KIRMIZI}[AstraSecurity] '{isim}' guvenlik taramasindan gecemedi, kurulmadi.{RESET}")
            return
    except ImportError:
        print(f"{SARI}[!] AstraSecurity modulu bulunamadi, guvenlik taramasi atlandi.{RESET}")

    try:
        with zipfile.ZipFile(dosya_yolu, "r") as z:
            manifest = _manifest_dogrula(z, isim)
            if manifest is None:
                return
    except zipfile.BadZipFile:
        print(f"{KIRMIZI}[HATA] '{dosya_yolu}' gecerli bir .aspa (zip) dosyasi degil.{RESET}")
        return

    kayitlar = _kayit_yukle()
    if isim in kayitlar:
        print(f"{SARI}[i] '{isim}' zaten kurulu, uzerine yaziliyor.{RESET}")

    os.makedirs(APPS_KLASORU, exist_ok=True)
    hedef_yol = os.path.join(APPS_KLASORU, f"{isim}.aspa")
    shutil.copy(dosya_yolu, hedef_yol)

    kayitlar[isim] = {
        "yol": hedef_yol,
        "version": manifest.get("version"),
        "entry": manifest.get("entry"),
        "author": manifest.get("author", "bilinmiyor"),
        "description": manifest.get("description", ""),
    }
    _kayit_kaydet(kayitlar)

    print(f"{YESIL}'{isim}' (v{manifest.get('version')}) kuruldu. Calistirmak icin: aspa run {isim}{RESET}")


def aspa_run(isim):
    if not isim:
        print(f"{KIRMIZI}Kullanim: aspa run <isim>{RESET}")
        return

    kayitlar = _kayit_yukle()
    if isim not in kayitlar:
        print(f"{KIRMIZI}[HATA] '{isim}' kurulu degil. Once: aspa install {isim} <dosya_yolu>{RESET}")
        return

    kayit = kayitlar[isim]
    yol = kayit["yol"]
    entry = kayit["entry"]

    if not os.path.exists(yol):
        print(f"{KIRMIZI}[HATA] '{yol}' bulunamadi. Uygulama dosyasi silinmis olabilir.{RESET}")
        return

    try:
        with zipfile.ZipFile(yol, "r") as z:
            kod_metni = z.read(entry).decode("utf-8")
            namespace = {}
            exec(kod_metni, namespace)
            if "run" in namespace:
                namespace["run"]()
            else:
                print(f"{KIRMIZI}[HATA] '{isim}' icinde run() fonksiyonu yok.{RESET}")
    except Exception as hata:
        print(f"{KIRMIZI}[HATA] '{isim}' calistirilirken hata: {hata}{RESET}")


def aspa_remove(isim):
    if not isim:
        print(f"{KIRMIZI}Kullanim: aspa remove <isim>{RESET}")
        return

    kayitlar = _kayit_yukle()
    if isim not in kayitlar:
        print(f"{KIRMIZI}[HATA] '{isim}' kurulu degil.{RESET}")
        return

    onay = input(f"'{isim}' kaldirilacak. Emin misin? (evet/hayir): ").strip().lower()
    if onay != "evet":
        print("Islem iptal edildi.")
        return

    yol = kayitlar[isim].get("yol")
    if yol and os.path.exists(yol):
        os.remove(yol)

    del kayitlar[isim]
    _kayit_kaydet(kayitlar)
    print(f"{YESIL}'{isim}' kaldirildi.{RESET}")


def aspa_list():
    kayitlar = _kayit_yukle()
    if not kayitlar:
        print("Henuz hicbir ASPA uygulamasi kurulu degil.")
        return
    print(f"{YESIL}Kurulu uygulamalar:{RESET}")
    for isim, bilgi in kayitlar.items():
        print(f"  {isim:<20} v{bilgi.get('version', '?')}  -  {bilgi.get('author', 'bilinmiyor')}")


def aspa_info(isim):
    if not isim:
        print(f"{KIRMIZI}Kullanim: aspa info <isim>{RESET}")
        return
    kayitlar = _kayit_yukle()
    if isim not in kayitlar:
        print(f"{KIRMIZI}[HATA] '{isim}' kurulu degil.{RESET}")
        return
    bilgi = kayitlar[isim]
    print(f"{YESIL}[ {isim} ]{RESET}")
    print(f"  Versiyon    : {bilgi.get('version', '?')}")
    print(f"  Yazar       : {bilgi.get('author', 'bilinmiyor')}")
    print(f"  Giris dosyasi: {bilgi.get('entry', '?')}")
    print(f"  Aciklama    : {bilgi.get('description', '(yok)')}")
    print(f"  Dosya yolu  : {bilgi.get('yol', '?')}")


def run(parcalar):
    """main.py icinden cagrilir: parcalar[0] == 'aspa'"""
    if len(parcalar) < 2:
        print(f"{KIRMIZI}Kullanim: aspa <install/run/remove/list/info>{RESET}")
        return

    eylem = parcalar[1]
    geri = parcalar[2:]

    if eylem == "install":
        if len(geri) < 2:
            print(f"{KIRMIZI}Kullanim: aspa install <isim> <dosya_yolu>{RESET}")
            return
        aspa_install(geri[0], geri[1])
    elif eylem == "run":
        aspa_run(geri[0] if geri else None)
    elif eylem == "remove":
        aspa_remove(geri[0] if geri else None)
    elif eylem == "list":
        aspa_list()
    elif eylem == "info":
        aspa_info(geri[0] if geri else None)
    else:
        print(f"{KIRMIZI}[HATA] 'aspa {eylem}' gecersiz.{RESET}")