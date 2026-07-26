"""
Distros/DevSage/DevSage.py
DevSage (Developer Sage) - AstraSage icin gelistirici odakli dagitim.

Cagrilisi: main.py icinde "dev" komutu bu moduldeki run_dev_command'a
yonlendirilir.

Komut yapisi:
  dev project create <Proje> -python/-html/-ast
  dev project open/delete/rename/list/tree
  dev code open/run/build/compile/test/debug/profile/format/lint
  dev file create/delete/copy .. at ../move .. at ../zip/unzip/search/replace
  dev folder create <Klasor>
  dev git init/clone/add/commit/push/pull/branch/merge/checkout
  dev github login/logout/repo create/repo delete/release create
  dev package install/remove/update/search/list
  dev docs readme/create/changelog/license/wiki
  dev config open/env/secrets/variables
  dev publish github/apk/exe/web/export
  dev ai explain/optimize/fix/docs/comment <Dosya>
  dev analyze stats/benchmark/dependencies/size
  dev astra package/upload/export
  dev tools json/yaml/xml/http/api/websocket
  dev android adb/logcat/apk install/apk sign

NOT: GitHub API, APK imzalama, gercek derleyici gibi komutlar sistemde
ilgili arac (git, pip paketleri, adb, buildozer, apksigner vb.) kuruluysa
calisir. Kurulu degilse program cokmez, acik bir hata mesaji verir.
"""

import os
import sys
import json
import shutil
import zipfile
import subprocess
import py_compile

DEVSAGE_KOK = os.getcwd()
PROJELER_KOK = os.path.join(DEVSAGE_KOK, "DevProjects")
CONFIG_DOSYASI = os.path.join(DEVSAGE_KOK, "devsage_config.json")
SECRETS_DOSYASI = os.path.join(DEVSAGE_KOK, "devsage_secrets.json")
VARIABLES_DOSYASI = os.path.join(DEVSAGE_KOK, "devsage_variables.json")
ENV_DOSYASI = os.path.join(DEVSAGE_KOK, ".env")

# ==================== TEMA (MOR) ====================
MOR = "\033[95m"
KOYU_MOR = "\033[35m"
BEYAZ = "\033[97m"
KIRMIZI = "\033[91m"
SARI = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"
PARLAK_MOR = "\033[95m"

LOGO = r"""
      ╔═╗╔═╗    ╔═╗      
     ╔██╝██╚╗   ██╚╗     
    ╔██╝  ██╚╗   ██╚╗    
    ██╚╗   ██╚╗  ╔██╝    
     ██╚╗   ██╚╗╔██╝     
      ██╝    ██╝██╝      
"""

def banner():
    print(PARLAK_MOR + LOGO + RESET)
    print(
        PARLAK_MOR
        + BOLD
        + "DevSage"
        + RESET
        + " • AstraSage Developer Distro"
    )
    print("")
    print("=" * 45)
    print(f"\n{MOR}Komut Kategorileri:{RESET}")
    print(f"  {BEYAZ}dev help{RESET}            → tüm komutlar")
    print(f"  {BEYAZ}dev project ...{RESET}     → proje araçları")
    print(f"  {BEYAZ}dev code ...{RESET}        → kod araçları")
    print(f"  {BEYAZ}dev build ...{RESET}       → derleme araçları")
    print(f"  {BEYAZ}dev package ...{RESET}     → paket yöneticisi")
    print(f"  {BEYAZ}dev return -AstraSage{RESET} → geri dön")
    print("=" * 45)


# ==================== ORTAK YARDIMCI FONKSIYONLAR ====================

def _dosya_json_yukle(yol, varsayilan):
    if not os.path.exists(yol):
        return varsayilan
    try:
        with open(yol, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return varsayilan


def _dosya_json_kaydet(yol, veri):
    try:
        with open(yol, "w", encoding="utf-8") as f:
            json.dump(veri, f, indent=2, ensure_ascii=False)
        return True
    except Exception as hata:
        print(f"{KIRMIZI}[HATA] '{yol}' kaydedilemedi: {hata}{RESET}")
        return False


def _at_ayir(parcalar):
    """'<kaynak> at <hedef>' seklindeki argumanlari ayirir."""
    if "at" not in parcalar:
        return None, None
    idx = parcalar.index("at")
    kaynak = " ".join(parcalar[:idx])
    hedef = " ".join(parcalar[idx + 1:])
    return kaynak or None, hedef or None


def _proje_yolu(isim):
    return os.path.join(PROJELER_KOK, isim)


# ==================== PROJE YONETIMI ====================

_PYTHON_SABLON = '''def main():
    print("Merhaba, {isim}!")


if __name__ == "__main__":
    main()
'''

_HTML_SABLON = '''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>{isim}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>{isim}</h1>
    <script src="script.js"></script>
</body>
</html>
'''

_AST_SABLON = '''def run():
    print("{isim} kutuphanesi calisti.")
'''


def proje_olustur(tur, isim):
    if not isim:
        print(f"{KIRMIZI}Kullanim: dev project create <isim> -python/-html/-ast{RESET}")
        return

    hedef = _proje_yolu(isim)
    if os.path.exists(hedef):
        print(f"{KIRMIZI}[HATA] '{isim}' zaten var.{RESET}")
        return

    os.makedirs(hedef, exist_ok=True)

    if tur == "python":
        with open(os.path.join(hedef, "main.py"), "w", encoding="utf-8") as f:
            f.write(_PYTHON_SABLON.format(isim=isim))
        with open(os.path.join(hedef, "requirements.txt"), "w", encoding="utf-8"):
            pass
        print(f"{MOR}Python projesi olusturuldu: {hedef}{RESET}")

    elif tur == "html":
        with open(os.path.join(hedef, "index.html"), "w", encoding="utf-8") as f:
            f.write(_HTML_SABLON.format(isim=isim))
        with open(os.path.join(hedef, "style.css"), "w", encoding="utf-8") as f:
            f.write("body {\n  font-family: sans-serif;\n}\n")
        with open(os.path.join(hedef, "script.js"), "w", encoding="utf-8") as f:
            f.write("// buraya kod yaz\n")
        print(f"{MOR}HTML projesi olusturuldu: {hedef}{RESET}")

    elif tur == "ast":
        with open(os.path.join(hedef, "main.py"), "w", encoding="utf-8") as f:
            f.write(_AST_SABLON.format(isim=isim))
        with open(os.path.join(hedef, "README.md"), "w", encoding="utf-8") as f:
            f.write(f"# {isim}\n\nAstraSage kutuphanesi.\n")
        print(f"{MOR}AstraSage kutuphane iskeleti olusturuldu: {hedef}{RESET}")

    else:
        shutil.rmtree(hedef, ignore_errors=True)
        print(f"{KIRMIZI}[HATA] Gecersiz proje turu: '{tur}' (-python / -html / -ast kullan){RESET}")


def proje_ac(isim):
    hedef = _proje_yolu(isim)
    if not os.path.isdir(hedef):
        print(f"{KIRMIZI}[HATA] '{isim}' bulunamadi.{RESET}")
        return
    print(f"{MOR}'{isim}' acildi: {hedef}{RESET}")
    for item in sorted(os.listdir(hedef)):
        print(f"  - {item}")


def proje_sil(isim):
    hedef = _proje_yolu(isim)
    if not os.path.isdir(hedef):
        print(f"{KIRMIZI}[HATA] '{isim}' bulunamadi.{RESET}")
        return
    onay = input(f"'{isim}' kalici olarak silinecek. Emin misin? (evet/hayir): ").strip().lower()
    if onay != "evet":
        print("Islem iptal edildi.")
        return
    shutil.rmtree(hedef)
    print(f"{MOR}'{isim}' silindi.{RESET}")


def proje_yeniden_adlandir(eski, yeni):
    eski_yol = _proje_yolu(eski)
    yeni_yol = _proje_yolu(yeni)
    if not os.path.isdir(eski_yol):
        print(f"{KIRMIZI}[HATA] '{eski}' bulunamadi.{RESET}")
        return
    if os.path.exists(yeni_yol):
        print(f"{KIRMIZI}[HATA] '{yeni}' zaten var.{RESET}")
        return
    os.rename(eski_yol, yeni_yol)
    print(f"{MOR}'{eski}' -> '{yeni}' olarak yeniden adlandirildi.{RESET}")


def proje_listele():
    if not os.path.isdir(PROJELER_KOK):
        print("Henuz hicbir proje yok. 'dev project create <isim> -python' ile olusturabilirsin.")
        return
    projeler = sorted(os.listdir(PROJELER_KOK))
    if not projeler:
        print("Henuz hicbir proje yok.")
        return
    print(f"{MOR}Projeler:{RESET}")
    for p in projeler:
        print(f"  - {p}")


def _agac_yazdir(yol, girinti=""):
    try:
        icerik = sorted(os.listdir(yol))
    except Exception:
        return
    for i, item in enumerate(icerik):
        son_mu = (i == len(icerik) - 1)
        dal = "+-- " if son_mu else "|-- "
        print(girinti + dal + item)
        tam = os.path.join(yol, item)
        if os.path.isdir(tam):
            yeni_girinti = girinti + ("    " if son_mu else "|   ")
            _agac_yazdir(tam, yeni_girinti)


def proje_agac(isim=None):
    hedef = _proje_yolu(isim) if isim else PROJELER_KOK
    if not os.path.isdir(hedef):
        print(f"{KIRMIZI}[HATA] '{hedef}' bulunamadi.{RESET}")
        return
    print(os.path.basename(hedef) or hedef)
    _agac_yazdir(hedef)


def dev_project(alt):
    if not alt:
        print(f"{KIRMIZI}Kullanim: dev project <create/open/delete/rename/list/tree>{RESET}")
        return
    eylem, geri = alt[0], alt[1:]

    if eylem == "create":
        if len(geri) < 2:
            print(f"{KIRMIZI}Kullanim: dev project create <Proje> -python/-html/-ast{RESET}")
            return
        proje_olustur(geri[1].lstrip("-"), geri[0])
    elif eylem == "open":
        proje_ac(geri[0] if geri else "")
    elif eylem == "delete":
        proje_sil(geri[0] if geri else "")
    elif eylem == "rename":
        if len(geri) < 2:
            print(f"{KIRMIZI}Kullanim: dev project rename <Eski> <Yeni>{RESET}")
            return
        proje_yeniden_adlandir(geri[0], geri[1])
    elif eylem == "list":
        proje_listele()
    elif eylem == "tree":
        proje_agac(geri[0] if geri else None)
    else:
        print(f"{KIRMIZI}[HATA] 'dev project {eylem}' gecersiz.{RESET}")


# ==================== KODLAMA ====================

def kod_editoru_ac():
    print(f"{MOR}Mevcut calisma dizini: {os.getcwd()}{RESET}")
    print("AstraSage'in 'as codeeditor' komutunu da kullanabilirsin.")


def dosya_calistir(dosya):
    if not dosya or not os.path.isfile(dosya):
        print(f"{KIRMIZI}[HATA] '{dosya}' bulunamadi.{RESET}")
        return
    subprocess.run([sys.executable, dosya])


def dosya_derle(dosya):
    if not dosya or not os.path.isfile(dosya):
        print(f"{KIRMIZI}[HATA] '{dosya}' bulunamadi.{RESET}")
        return
    try:
        cikti = dosya + "c"
        py_compile.compile(dosya, cfile=cikti, doraise=True)
        print(f"{MOR}Derleme basarili: {cikti}{RESET}")
    except py_compile.PyCompileError as hata:
        print(f"{KIRMIZI}[HATA] Derleme basarisiz:\n{hata}{RESET}")


def test_calistir(dosya):
    hedef = [dosya] if dosya else []
    try:
        subprocess.run([sys.executable, "-m", "pytest"] + hedef)
    except FileNotFoundError:
        try:
            subprocess.run([sys.executable, "-m", "unittest"] + (["discover"] if not dosya else [dosya]))
        except Exception as hata:
            print(f"{KIRMIZI}[HATA] Test calistirilamadi: {hata}{RESET}")


def hata_ayikla(dosya):
    if not dosya or not os.path.isfile(dosya):
        print(f"{KIRMIZI}[HATA] '{dosya}' bulunamadi.{RESET}")
        return
    subprocess.run([sys.executable, "-m", "pdb", dosya])


def performans_olc(dosya):
    if not dosya or not os.path.isfile(dosya):
        print(f"{KIRMIZI}[HATA] '{dosya}' bulunamadi.{RESET}")
        return
    subprocess.run([sys.executable, "-m", "cProfile", dosya])


def kod_formatla(dosya):
    if not dosya or not os.path.isfile(dosya):
        print(f"{KIRMIZI}[HATA] '{dosya}' bulunamadi.{RESET}")
        return
    try:
        subprocess.run([sys.executable, "-m", "black", dosya], check=True)
    except FileNotFoundError:
        print(f"{KIRMIZI}[HATA] 'black' kurulu degil. Once: dev package install black{RESET}")
    except subprocess.CalledProcessError as hata:
        print(f"{KIRMIZI}[HATA] Formatlama basarisiz: {hata}{RESET}")


def kod_kontrol(dosya):
    if not dosya or not os.path.isfile(dosya):
        print(f"{KIRMIZI}[HATA] '{dosya}' bulunamadi.{RESET}")
        return
    try:
        subprocess.run([sys.executable, "-m", "pyflakes", dosya], check=False)
    except FileNotFoundError:
        print(f"{KIRMIZI}[HATA] 'pyflakes' kurulu degil. Once: dev package install pyflakes{RESET}")


def proje_derle(bayrak):
    if bayrak == "web":
        build_klasoru = os.path.join(os.getcwd(), "build_web")
        os.makedirs(build_klasoru, exist_ok=True)
        kopyalanan = 0
        for dosya in os.listdir("."):
            if dosya.endswith((".html", ".css", ".js")):
                shutil.copy(dosya, build_klasoru)
                kopyalanan += 1
        print(f"{MOR}Web build tamamlandi: {build_klasoru} ({kopyalanan} dosya){RESET}")

    elif bayrak == "exe":
        try:
            subprocess.run([sys.executable, "-m", "PyInstaller", "--onefile", "main.py"], check=True)
            print(f"{MOR}EXE build tamamlandi, 'dist/' klasorune bak.{RESET}")
        except FileNotFoundError:
            print(f"{KIRMIZI}[HATA] PyInstaller kurulu degil. Once: dev package install pyinstaller{RESET}")
        except subprocess.CalledProcessError as hata:
            print(f"{KIRMIZI}[HATA] EXE build basarisiz: {hata}{RESET}")

    elif bayrak == "apk":
        try:
            subprocess.run(["buildozer", "android", "debug"], check=True)
            print(f"{MOR}APK build tamamlandi, 'bin/' klasorune bak.{RESET}")
        except FileNotFoundError:
            print(f"{KIRMIZI}[HATA] 'buildozer' bulunamadi. APK build icin Android SDK ve "
                  f"buildozer kurulu bir ortam gerekiyor; bu genelde Pydroid3 icinde dogrudan calismaz.{RESET}")
        except subprocess.CalledProcessError as hata:
            print(f"{KIRMIZI}[HATA] APK build basarisiz: {hata}{RESET}")

    else:
        print(f"{KIRMIZI}Kullanim: dev code build -apk/-exe/-web{RESET}")


def dev_code(alt):
    if not alt:
        print(f"{KIRMIZI}Kullanim: dev code <open/run/build/compile/test/debug/profile/format/lint>{RESET}")
        return
    eylem, geri = alt[0], alt[1:]

    if eylem == "open":
        kod_editoru_ac()
    elif eylem == "run":
        dosya_calistir(geri[0] if geri else None)
    elif eylem == "build":
        proje_derle(geri[0].lstrip("-") if geri else "")
    elif eylem == "compile":
        dosya_derle(geri[0] if geri else None)
    elif eylem == "test":
        test_calistir(geri[0] if geri else None)
    elif eylem == "debug":
        hata_ayikla(geri[0] if geri else None)
    elif eylem == "profile":
        performans_olc(geri[0] if geri else None)
    elif eylem == "format":
        kod_formatla(geri[0] if geri else None)
    elif eylem == "lint":
        kod_kontrol(geri[0] if geri else None)
    else:
        print(f"{KIRMIZI}[HATA] 'dev code {eylem}' gecersiz.{RESET}")


# ==================== DOSYA / KLASOR ISLEMLERI ====================

def dosya_olustur(dosya):
    try:
        with open(dosya, "a", encoding="utf-8"):
            pass
        print(f"{MOR}'{dosya}' olusturuldu.{RESET}")
    except Exception as hata:
        print(f"{KIRMIZI}[HATA] {hata}{RESET}")


def dosya_sil(dosya):
    if not os.path.exists(dosya):
        print(f"{KIRMIZI}[HATA] '{dosya}' bulunamadi.{RESET}")
        return
    try:
        os.remove(dosya) if os.path.isfile(dosya) else shutil.rmtree(dosya)
        print(f"{MOR}'{dosya}' silindi.{RESET}")
    except Exception as hata:
        print(f"{KIRMIZI}[HATA] {hata}{RESET}")


def dosya_kopyala(kaynak, hedef):
    if not kaynak or not hedef:
        print(f"{KIRMIZI}Kullanim: dev file copy <Dosya> at <Hedef>{RESET}")
        return
    try:
        shutil.copytree(kaynak, hedef) if os.path.isdir(kaynak) else shutil.copy(kaynak, hedef)
        print(f"{MOR}'{kaynak}' -> '{hedef}' kopyalandi.{RESET}")
    except Exception as hata:
        print(f"{KIRMIZI}[HATA] {hata}{RESET}")


def dosya_tasi(kaynak, hedef):
    if not kaynak or not hedef:
        print(f"{KIRMIZI}Kullanim: dev file move <Dosya> at <Hedef>{RESET}")
        return
    try:
        shutil.move(kaynak, hedef)
        print(f"{MOR}'{kaynak}' -> '{hedef}' tasindi.{RESET}")
    except Exception as hata:
        print(f"{KIRMIZI}[HATA] {hata}{RESET}")


def dosya_ziple(dosya):
    if not dosya or not os.path.exists(dosya):
        print(f"{KIRMIZI}[HATA] '{dosya}' bulunamadi.{RESET}")
        return
    hedef = dosya.rstrip("/\\") + ".zip"
    try:
        if os.path.isdir(dosya):
            with zipfile.ZipFile(hedef, "w", zipfile.ZIP_DEFLATED) as z:
                for kok, _, dosyalar in os.walk(dosya):
                    for d in dosyalar:
                        tam = os.path.join(kok, d)
                        z.write(tam, os.path.relpath(tam, os.path.dirname(dosya)))
        else:
            with zipfile.ZipFile(hedef, "w", zipfile.ZIP_DEFLATED) as z:
                z.write(dosya, os.path.basename(dosya))
        print(f"{MOR}'{dosya}' -> '{hedef}' sikistirildi.{RESET}")
    except Exception as hata:
        print(f"{KIRMIZI}[HATA] {hata}{RESET}")


def dosya_zip_ac(dosya):
    if not dosya or not os.path.isfile(dosya):
        print(f"{KIRMIZI}[HATA] '{dosya}' bulunamadi.{RESET}")
        return
    hedef = dosya[:-4] if dosya.endswith(".zip") else dosya + "_acik"
    try:
        with zipfile.ZipFile(dosya, "r") as z:
            z.extractall(hedef)
        print(f"{MOR}'{dosya}' -> '{hedef}' konumuna acildi.{RESET}")
    except Exception as hata:
        print(f"{KIRMIZI}[HATA] {hata}{RESET}")


def dosya_ara(isim, klasor="."):
    bulunanlar = []
    for kok, dizinler, dosyalar in os.walk(klasor):
        for d in dosyalar + dizinler:
            if isim.lower() in d.lower():
                bulunanlar.append(os.path.join(kok, d))
    if not bulunanlar:
        print(f"'{isim}' hicbir yerde bulunamadi.")
        return
    print(f"{MOR}Bulunanlar:{RESET}")
    for b in bulunanlar:
        print(f"  - {b}")


def metin_degistir(eski, yeni, klasor="."):
    toplam = 0
    for kok, _, dosyalar in os.walk(klasor):
        for d in dosyalar:
            tam = os.path.join(kok, d)
            try:
                with open(tam, "r", encoding="utf-8", errors="ignore") as f:
                    icerik = f.read()
                if eski in icerik:
                    with open(tam, "w", encoding="utf-8") as f:
                        f.write(icerik.replace(eski, yeni))
                    adet = icerik.count(eski)
                    toplam += adet
                    print(f"  {tam}: {adet} degisiklik")
            except Exception:
                continue
    print(f"{MOR}Toplam {toplam} degisiklik yapildi.{RESET}")


def dev_file(alt):
    if not alt:
        print(f"{KIRMIZI}Kullanim: dev file <create/delete/copy/move/zip/unzip/search/replace>{RESET}")
        return
    eylem, geri = alt[0], alt[1:]

    if eylem == "create":
        dosya_olustur(geri[0]) if geri else print(f"{KIRMIZI}Kullanim: dev file create <Dosya>{RESET}")
    elif eylem == "delete":
        dosya_sil(geri[0]) if geri else print(f"{KIRMIZI}Kullanim: dev file delete <Dosya>{RESET}")
    elif eylem == "copy":
        kaynak, hedef = _at_ayir(geri)
        dosya_kopyala(kaynak, hedef)
    elif eylem == "move":
        kaynak, hedef = _at_ayir(geri)
        dosya_tasi(kaynak, hedef)
    elif eylem == "zip":
        dosya_ziple(geri[0]) if geri else print(f"{KIRMIZI}Kullanim: dev file zip <Dosya>{RESET}")
    elif eylem == "unzip":
        dosya_zip_ac(geri[0]) if geri else print(f"{KIRMIZI}Kullanim: dev file unzip <Dosya.zip>{RESET}")
    elif eylem == "search":
        dosya_ara(geri[0]) if geri else print(f"{KIRMIZI}Kullanim: dev file search <Isim>{RESET}")
    elif eylem == "replace":
        if len(geri) < 2:
            print(f"{KIRMIZI}Kullanim: dev file replace <Eski> <Yeni>{RESET}")
        else:
            metin_degistir(geri[0], geri[1])
    else:
        print(f"{KIRMIZI}[HATA] 'dev file {eylem}' gecersiz.{RESET}")


def dev_folder(alt):
    if not alt or alt[0] != "create" or len(alt) < 2:
        print(f"{KIRMIZI}Kullanim: dev folder create <Klasor>{RESET}")
        return
    try:
        os.makedirs(alt[1], exist_ok=True)
        print(f"{MOR}'{alt[1]}' klasoru olusturuldu.{RESET}")
    except Exception as hata:
        print(f"{KIRMIZI}[HATA] {hata}{RESET}")


# ==================== GIT ====================

def git_calistir(args):
    try:
        sonuc = subprocess.run(["git"] + args, capture_output=True, text=True)
        if sonuc.stdout:
            print(sonuc.stdout.strip())
        if sonuc.stderr:
            print(f"{SARI}{sonuc.stderr.strip()}{RESET}")
    except FileNotFoundError:
        print(f"{KIRMIZI}[HATA] 'git' bulunamadi. Once git'i kurman gerekiyor.{RESET}")
    except Exception as hata:
        print(f"{KIRMIZI}[HATA] {hata}{RESET}")


def dev_git(alt):
    if not alt:
        print(f"{KIRMIZI}Kullanim: dev git <init/clone/add/commit/push/pull/branch/merge/checkout>{RESET}")
        return
    eylem, geri = alt[0], alt[1:]

    if eylem == "commit":
        mesaj = " ".join(geri)
        if len(mesaj) >= 2 and mesaj[0] == mesaj[-1] and mesaj[0] in ('"', "'"):
            mesaj = mesaj[1:-1]
        if not mesaj:
            print(f"{KIRMIZI}Kullanim: dev git commit \"<Mesaj>\"{RESET}")
            return
        git_calistir(["commit", "-m", mesaj])
    else:
        git_calistir([eylem] + geri)


# ==================== GITHUB (gercek API) ====================

def _secrets_yukle():
    return _dosya_json_yukle(SECRETS_DOSYASI, {})


def _secrets_kaydet(veri):
    return _dosya_json_kaydet(SECRETS_DOSYASI, veri)


def _github_token_al():
    return _secrets_yukle().get("github_token")


def _github_kullanici_al(token):
    try:
        import requests
        yanit = requests.get("https://api.github.com/user", headers={"Authorization": f"token {token}"})
        if yanit.status_code == 200:
            return yanit.json().get("login")
        print(f"{KIRMIZI}[HATA] Kullanici bilgisi alinamadi ({yanit.status_code}). Token gecersiz olabilir.{RESET}")
        return None
    except Exception as hata:
        print(f"{KIRMIZI}[HATA] {hata}{RESET}")
        return None


def github_login():
    token = input("GitHub Personal Access Token (repo yetkili): ").strip()
    if not token:
        print(f"{KIRMIZI}Islem iptal edildi.{RESET}")
        return
    veri = _secrets_yukle()
    veri["github_token"] = token
    if _secrets_kaydet(veri):
        print(f"{MOR}GitHub token'i kaydedildi (yerel olarak, sifrelenmemis).{RESET}")


def github_logout():
    veri = _secrets_yukle()
    if veri.pop("github_token", None) is not None:
        _secrets_kaydet(veri)
        print(f"{MOR}GitHub oturumu kapatildi (token silindi).{RESET}")
    else:
        print("Zaten giris yapilmamis.")


def github_repo_create(isim):
    token = _github_token_al()
    if not token:
        print(f"{KIRMIZI}[HATA] Once 'dev github login' ile giris yap.{RESET}")
        return
    if not isim:
        print(f"{KIRMIZI}Kullanim: dev github repo create <Isim>{RESET}")
        return
    try:
        import requests
        yanit = requests.post(
            "https://api.github.com/user/repos",
            headers={"Authorization": f"token {token}"},
            json={"name": isim},
        )
        if yanit.status_code == 201:
            print(f"{MOR}'{isim}' deposu olusturuldu: {yanit.json().get('html_url')}{RESET}")
        else:
            print(f"{KIRMIZI}[HATA] Depo olusturulamadi ({yanit.status_code}): {yanit.text[:200]}{RESET}")
    except Exception as hata:
        print(f"{KIRMIZI}[HATA] {hata}{RESET}")


def github_repo_delete(isim):
    token = _github_token_al()
    if not token:
        print(f"{KIRMIZI}[HATA] Once 'dev github login' ile giris yap.{RESET}")
        return
    if not isim:
        print(f"{KIRMIZI}Kullanim: dev github repo delete <Isim>{RESET}")
        return
    kullanici = _github_kullanici_al(token)
    if not kullanici:
        return
    onay = input(f"'{kullanici}/{isim}' deposu KALICI olarak silinecek. Emin misin? (evet/hayir): ").strip().lower()
    if onay != "evet":
        print("Islem iptal edildi.")
        return
    try:
        import requests
        yanit = requests.delete(
            f"https://api.github.com/repos/{kullanici}/{isim}",
            headers={"Authorization": f"token {token}"},
        )
        if yanit.status_code == 204:
            print(f"{MOR}'{isim}' deposu silindi.{RESET}")
        else:
            print(f"{KIRMIZI}[HATA] Depo silinemedi ({yanit.status_code}): {yanit.text[:200]}{RESET}")
    except Exception as hata:
        print(f"{KIRMIZI}[HATA] {hata}{RESET}")


def github_release_create():
    token = _github_token_al()
    if not token:
        print(f"{KIRMIZI}[HATA] Once 'dev github login' ile giris yap.{RESET}")
        return
    kullanici = _github_kullanici_al(token)
    if not kullanici:
        return
    repo = input("Repo ismi: ").strip()
    tag = input("Tag (ornek: v1.0.0): ").strip()
    baslik = input("Surum basligi: ").strip()
    try:
        import requests
        yanit = requests.post(
            f"https://api.github.com/repos/{kullanici}/{repo}/releases",
            headers={"Authorization": f"token {token}"},
            json={"tag_name": tag, "name": baslik},
        )
        if yanit.status_code == 201:
            print(f"{MOR}Surum yayimlandi: {yanit.json().get('html_url')}{RESET}")
        else:
            print(f"{KIRMIZI}[HATA] Surum olusturulamadi ({yanit.status_code}): {yanit.text[:200]}{RESET}")
    except Exception as hata:
        print(f"{KIRMIZI}[HATA] {hata}{RESET}")


def dev_github(alt):
    if not alt:
        print(f"{KIRMIZI}Kullanim: dev github <login/logout/repo/release>{RESET}")
        return
    eylem, geri = alt[0], alt[1:]

    if eylem == "login":
        github_login()
    elif eylem == "logout":
        github_logout()
    elif eylem == "repo":
        if len(geri) < 2:
            print(f"{KIRMIZI}Kullanim: dev github repo create/delete <Isim>{RESET}")
            return
        if geri[0] == "create":
            github_repo_create(geri[1])
        elif geri[0] == "delete":
            github_repo_delete(geri[1])
        else:
            print(f"{KIRMIZI}[HATA] 'dev github repo {geri[0]}' gecersiz.{RESET}")
    elif eylem == "release":
        if geri and geri[0] == "create":
            github_release_create()
        else:
            print(f"{KIRMIZI}Kullanim: dev github release create{RESET}")
    else:
        print(f"{KIRMIZI}[HATA] 'dev github {eylem}' gecersiz.{RESET}")


# ==================== PAKET YONETIMI (pip) ====================

def dev_package(alt):
    if not alt:
        print(f"{KIRMIZI}Kullanim: dev package <install/remove/update/search/list> [paket]{RESET}")
        return
    eylem, geri = alt[0], alt[1:]

    try:
        if eylem == "install":
            if not geri:
                print(f"{KIRMIZI}Kullanim: dev package install <Paket>{RESET}")
                return
            subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages"] + geri)
        elif eylem == "remove":
            if not geri:
                print(f"{KIRMIZI}Kullanim: dev package remove <Paket>{RESET}")
                return
            subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y"] + geri)
        elif eylem == "update":
            if not geri:
                print(f"{KIRMIZI}Kullanim: dev package update <Paket>{RESET}")
                return
            subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages", "--upgrade"] + geri)
        elif eylem == "search":
            print(f"{SARI}[i] pip'in yerlesik arama API'si kaldirildi. "
                  f"https://pypi.org/search/?q={'+'.join(geri)} adresine bakabilirsin.{RESET}")
        elif eylem == "list":
            subprocess.run([sys.executable, "-m", "pip", "list"])
        else:
            print(f"{KIRMIZI}[HATA] 'dev package {eylem}' gecersiz.{RESET}")
    except Exception as hata:
        print(f"{KIRMIZI}[HATA] {hata}{RESET}")


# ==================== DOKUMANTASYON ====================

def dev_docs(alt):
    eylem = alt[0] if alt else ""

    if eylem == "readme":
        with open("README.md", "w", encoding="utf-8") as f:
            f.write("# Proje Adi\n\nKisa aciklama.\n\n## Kurulum\n\n## Kullanim\n\n## Lisans\n")
        print(f"{MOR}README.md olusturuldu.{RESET}")

    elif eylem == "create":
        os.makedirs("docs", exist_ok=True)
        with open(os.path.join("docs", "index.md"), "w", encoding="utf-8") as f:
            f.write("# Dokumantasyon\n\nBuraya proje dokumantasyonunu yaz.\n")
        print(f"{MOR}'docs/index.md' olusturuldu.{RESET}")

    elif eylem == "changelog":
        with open("CHANGELOG.md", "w", encoding="utf-8") as f:
            f.write("# Changelog\n\n## [Yayinlanmadi]\n### Eklenen\n- Ilk surum.\n")
        print(f"{MOR}CHANGELOG.md olusturuldu.{RESET}")

    elif eylem == "license":
        with open("LICENSE", "w", encoding="utf-8") as f:
            f.write(
                "MIT License\n\nCopyright (c) 2026\n\n"
                "Bu yazilimin bir kopyasini edinen herkese, kisitlama olmaksizin "
                "kullanma, kopyalama, degistirme, birlestirme, yayinlama, dagitma, "
                "alt lisanslama ve/veya satma izni verilir.\n"
            )
        print(f"{MOR}LICENSE (MIT) olusturuldu.{RESET}")

    elif eylem == "wiki":
        os.makedirs("wiki", exist_ok=True)
        with open(os.path.join("wiki", "Home.md"), "w", encoding="utf-8") as f:
            f.write("# Wiki Ana Sayfa\n\nProje hakkinda genel bilgiler buraya.\n")
        print(f"{MOR}'wiki/Home.md' olusturuldu.{RESET}")

    else:
        print(f"{KIRMIZI}Kullanim: dev docs <readme/create/changelog/license/wiki>{RESET}")


# ==================== PROJE AYARLARI ====================

def dev_config(alt):
    eylem = alt[0] if alt else ""

    if eylem == "open":
        veri = _dosya_json_yukle(CONFIG_DOSYASI, {})
        print(f"{MOR}Config dosyasi: {CONFIG_DOSYASI}{RESET}")
        if not veri:
            print("(bos)")
        for k, v in veri.items():
            print(f"  {k} = {v}")

    elif eylem == "env":
        geri = alt[1:]
        satirlar = {}
        if os.path.exists(ENV_DOSYASI):
            with open(ENV_DOSYASI, "r", encoding="utf-8") as f:
                for satir in f:
                    if "=" in satir:
                        k, v = satir.strip().split("=", 1)
                        satirlar[k] = v
        if not geri:
            if not satirlar:
                print("'.env' dosyasi bos veya yok.")
            for k, v in satirlar.items():
                print(f"  {k}={v}")
        elif geri[0] == "set" and len(geri) >= 3:
            satirlar[geri[1]] = geri[2]
            with open(ENV_DOSYASI, "w", encoding="utf-8") as f:
                for k, v in satirlar.items():
                    f.write(f"{k}={v}\n")
            print(f"{MOR}'{geri[1]}' .env dosyasina yazildi.{RESET}")
        elif geri[0] == "unset" and len(geri) >= 2:
            satirlar.pop(geri[1], None)
            with open(ENV_DOSYASI, "w", encoding="utf-8") as f:
                for k, v in satirlar.items():
                    f.write(f"{k}={v}\n")
            print(f"{MOR}'{geri[1]}' .env dosyasindan silindi.{RESET}")
        else:
            print(f"{KIRMIZI}Kullanim: dev config env  |  dev config env set <K> <V>  |  dev config env unset <K>{RESET}")

    elif eylem == "secrets":
        dev_secrets_yonet(alt[1:])

    elif eylem == "variables":
        geri = alt[1:]
        degiskenler = _dosya_json_yukle(VARIABLES_DOSYASI, {})
        if not geri:
            if not degiskenler:
                print("Henuz hicbir degisken tanimli degil.")
            for k, v in degiskenler.items():
                print(f"  {k} = {v}")
        elif len(geri) == 1:
            print(f"{geri[0]} = {degiskenler.get(geri[0], '(tanimli degil)')}")
        else:
            degiskenler[geri[0]] = geri[1]
            _dosya_json_kaydet(VARIABLES_DOSYASI, degiskenler)
            print(f"{MOR}'{geri[0]}' = '{geri[1]}' kaydedildi.{RESET}")

    else:
        print(f"{KIRMIZI}Kullanim: dev config <open/env/secrets/variables>{RESET}")


def dev_secrets_yonet(alt):
    print(f"{SARI}[!] Uyari: secrets dosyasi duz metin olarak saklanir, gercek "
          f"sifre/token'lari dikkatli kullan.{RESET}")
    veri = _secrets_yukle()
    if not alt:
        print("Kullanim: dev config secrets set <K> <V> | list | remove <K>")
        return
    eylem = alt[0]
    if eylem == "set" and len(alt) >= 3:
        veri[alt[1]] = alt[2]
        _secrets_kaydet(veri)
        print(f"{MOR}'{alt[1]}' kaydedildi.{RESET}")
    elif eylem == "list":
        for k in veri:
            print(f"  {k} = ****")
    elif eylem == "remove" and len(alt) >= 2:
        veri.pop(alt[1], None)
        _secrets_kaydet(veri)
        print(f"{MOR}'{alt[1]}' silindi.{RESET}")
    else:
        print("Kullanim: dev config secrets set <K> <V> | list | remove <K>")


# ==================== YAYINLAMA ====================

def dev_publish(alt):
    eylem = alt[0] if alt else ""

    if eylem == "github":
        github_release_create()
    elif eylem in ("apk", "exe", "web"):
        proje_derle(eylem)
    elif eylem == "export":
        hedef = "dist_export.zip"
        with zipfile.ZipFile(hedef, "w", zipfile.ZIP_DEFLATED) as z:
            for kok, dizinler, dosyalar in os.walk("."):
                dizinler[:] = [d for d in dizinler if d not in (".git", "__pycache__", "dist_export.zip")]
                for d in dosyalar:
                    tam = os.path.join(kok, d)
                    z.write(tam, os.path.relpath(tam, "."))
        print(f"{MOR}Dagitim paketi olusturuldu: {hedef}{RESET}")
    else:
        print(f"{KIRMIZI}Kullanim: dev publish <github/apk/exe/web/export>{RESET}")


# ==================== YAPAY ZEKA ====================

def dev_ai(alt):
    if len(alt) < 2:
        print(f"{KIRMIZI}Kullanim: dev ai <explain/optimize/fix/docs/comment> <Dosya>{RESET}")
        return
    eylem, dosya = alt[0], alt[1]

    if not os.path.isfile(dosya):
        print(f"{KIRMIZI}[HATA] '{dosya}' bulunamadi.{RESET}")
        return

    with open(dosya, "r", encoding="utf-8", errors="ignore") as f:
        icerik = f.read()

    istekler = {
        "explain": f"Bu kodu acikla:\n\n{icerik}",
        "optimize": f"Bu kodu optimize et:\n\n{icerik}",
        "fix": f"Bu koddaki hatalari bul ve duzelt:\n\n{icerik}",
        "docs": f"Bu kod icin dokumantasyon yaz:\n\n{icerik}",
        "comment": f"Bu koda aciklayici yorum satirlari ekle:\n\n{icerik}",
    }

    if eylem not in istekler:
        print(f"{KIRMIZI}[HATA] 'dev ai {eylem}' gecersiz.{RESET}")
        return

    try:
        # NOT: utils/astra_ai.py'nin gercek fonksiyon imzasini gormedigimiz
        # icin bu entegrasyon varsayimsaldir; calismazsa run_ai_command'in
        # gercek imzasina gore duzeltmen gerekebilir.
        from utils.astra_ai import run_ai_command
        run_ai_command(["ai", istekler[eylem], "-run"])
    except Exception as hata:
        print(f"{KIRMIZI}[HATA] AI modulune erisilemedi: {hata}{RESET}")
        print("AstraSage'in mevcut 'ai <mesaj> -run' komutunu manuel olarak kullanabilirsin.")


# ==================== ANALIZ ====================

def dev_analyze(alt):
    eylem = alt[0] if alt else ""

    if eylem == "stats":
        dosya_sayisi = 0
        satir_sayisi = 0
        for kok, dizinler, dosyalar in os.walk("."):
            dizinler[:] = [d for d in dizinler if d not in (".git", "__pycache__")]
            for d in dosyalar:
                if d.endswith((".py", ".html", ".css", ".js")):
                    dosya_sayisi += 1
                    try:
                        with open(os.path.join(kok, d), "r", encoding="utf-8", errors="ignore") as f:
                            satir_sayisi += sum(1 for _ in f)
                    except Exception:
                        continue
        print(f"{MOR}Dosya sayisi: {dosya_sayisi}{RESET}")
        print(f"{MOR}Toplam satir: {satir_sayisi}{RESET}")

    elif eylem == "benchmark":
        hedef = "main.py" if os.path.isfile("main.py") else None
        if not hedef:
            print(f"{KIRMIZI}[HATA] 'main.py' bulunamadi.{RESET}")
            return
        import time
        baslangic = time.time()
        subprocess.run([sys.executable, hedef])
        print(f"{MOR}Calisma suresi: {time.time() - baslangic:.3f} saniye{RESET}")

    elif eylem == "dependencies":
        if os.path.isfile("requirements.txt"):
            with open("requirements.txt", "r", encoding="utf-8") as f:
                print(f.read())
        else:
            bulunanlar = set()
            for kok, _, dosyalar in os.walk("."):
                for d in dosyalar:
                    if d.endswith(".py"):
                        try:
                            with open(os.path.join(kok, d), "r", encoding="utf-8", errors="ignore") as f:
                                for satir in f:
                                    satir = satir.strip()
                                    if satir.startswith("import ") or satir.startswith("from "):
                                        bulunanlar.add(satir)
                        except Exception:
                            continue
            print(f"{MOR}Bulunan import'lar:{RESET}")
            for b in sorted(bulunanlar):
                print(f"  {b}")

    elif eylem == "size":
        hedef = alt[1] if len(alt) > 1 else "."
        toplam = 0
        for kok, _, dosyalar in os.walk(hedef):
            for d in dosyalar:
                try:
                    toplam += os.path.getsize(os.path.join(kok, d))
                except Exception:
                    continue
        birim = "B"
        for b in ["B", "KB", "MB", "GB"]:
            birim = b
            if toplam < 1024:
                break
            toplam /= 1024
        print(f"{MOR}'{hedef}' boyutu: {toplam:.2f} {birim}{RESET}")

    else:
        print(f"{KIRMIZI}Kullanim: dev analyze <stats/benchmark/dependencies/size>{RESET}")


# ==================== ASTRASAGE ENTEGRASYONU ====================

def dev_astra(alt):
    eylem = alt[0] if alt else ""

    if eylem == "package":
        if len(alt) < 2:
            print(f"{KIRMIZI}Kullanim: dev astra package <isim>{RESET}")
            return
        isim = alt[1]
        if not os.path.isfile("main.py"):
            print(f"{KIRMIZI}[HATA] Bu klasorde 'main.py' yok, once onu olustur.{RESET}")
            return
        pc_yolu = f"{isim}.pc"
        with zipfile.ZipFile(pc_yolu, "w", zipfile.ZIP_DEFLATED) as z:
            z.write("main.py")
            if os.path.isfile("README.md"):
                z.write("README.md")
        print(f"{MOR}Paket olusturuldu: {pc_yolu}{RESET}")

    elif eylem == "upload":
        # NOT: Gercek bir uzak sunucu/hosting altyapisi olmadigi icin bu,
        # paketi AstraSage'in yerel kutuphane klasorune kopyalayan bir
        # "yerel yukleme" simulasyonudur.
        if len(alt) < 2:
            print(f"{KIRMIZI}Kullanim: dev astra upload <isim.pc>{RESET}")
            return
        kaynak = alt[1]
        if not os.path.isfile(kaynak):
            print(f"{KIRMIZI}[HATA] '{kaynak}' bulunamadi.{RESET}")
            return
        hedef_klasor = os.path.join(DEVSAGE_KOK, "libraries", "gt")
        os.makedirs(hedef_klasor, exist_ok=True)
        shutil.copy(kaynak, hedef_klasor)
        print(f"{MOR}'{kaynak}' yerel kutuphane klasorune kopyalandi (gercek uzak sunucu yok): {hedef_klasor}{RESET}")

    elif eylem == "export":
        hedef_klasor = alt[1] if len(alt) > 1 else os.path.join(DEVSAGE_KOK, "Assets", "pc")
        os.makedirs(hedef_klasor, exist_ok=True)
        if not os.path.isfile("main.py"):
            print(f"{KIRMIZI}[HATA] Bu klasorde 'main.py' yok.{RESET}")
            return
        isim = os.path.basename(os.getcwd())
        pc_yolu = os.path.join(hedef_klasor, f"{isim}.pc")
        with zipfile.ZipFile(pc_yolu, "w", zipfile.ZIP_DEFLATED) as z:
            z.write("main.py")
            if os.path.isfile("README.md"):
                z.write("README.md")
        print(f"{MOR}AstraSage icin disa aktarildi: {pc_yolu}{RESET}")

    else:
        print(f"{KIRMIZI}Kullanim: dev astra <package/upload/export>{RESET}")


# ==================== GELISTIRICI ARACLARI ====================

def dev_tools(alt):
    eylem = alt[0] if alt else ""
    geri = alt[1:]

    if eylem == "json":
        if not geri or not os.path.isfile(geri[0]):
            print(f"{KIRMIZI}Kullanim: dev tools json <dosya.json>{RESET}")
            return
        dosya = geri[0]
        try:
            with open(dosya, "r", encoding="utf-8") as f:
                veri = json.load(f)
        except Exception as hata:
            print(f"{KIRMIZI}[HATA] Gecersiz JSON: {hata}{RESET}")
            return
        print(json.dumps(veri, indent=2, ensure_ascii=False))
        while True:
            komut = input(f"{MOR}json> {RESET}(anahtar=deger / cikis): ").strip()
            if komut.lower() in ("cikis", "exit"):
                break
            if "=" in komut:
                k, v = komut.split("=", 1)
                veri[k.strip()] = v.strip()
                with open(dosya, "w", encoding="utf-8") as f:
                    json.dump(veri, f, indent=2, ensure_ascii=False)
                print(f"{MOR}'{k.strip()}' guncellendi.{RESET}")

    elif eylem == "yaml":
        if not geri or not os.path.isfile(geri[0]):
            print(f"{KIRMIZI}Kullanim: dev tools yaml <dosya.yaml>{RESET}")
            return
        try:
            import yaml
            with open(geri[0], "r", encoding="utf-8") as f:
                veri = yaml.safe_load(f)
            print(yaml.dump(veri, allow_unicode=True, sort_keys=False))
        except ImportError:
            print(f"{KIRMIZI}[HATA] PyYAML kurulu degil. Once: dev package install pyyaml{RESET}")
        except Exception as hata:
            print(f"{KIRMIZI}[HATA] {hata}{RESET}")

    elif eylem == "xml":
        if not geri or not os.path.isfile(geri[0]):
            print(f"{KIRMIZI}Kullanim: dev tools xml <dosya.xml>{RESET}")
            return
        try:
            from xml.dom import minidom
            with open(geri[0], "r", encoding="utf-8") as f:
                icerik = f.read()
            print(minidom.parseString(icerik).toprettyxml(indent="  "))
        except Exception as hata:
            print(f"{KIRMIZI}[HATA] {hata}{RESET}")

    elif eylem == "http":
        if not geri:
            print(f"{KIRMIZI}Kullanim: dev tools http <url>{RESET}")
            return
        try:
            import requests
            yanit = requests.get(geri[0], timeout=10)
            print(f"{MOR}Durum kodu: {yanit.status_code}{RESET}")
            print(yanit.text[:1000])
        except Exception as hata:
            print(f"{KIRMIZI}[HATA] {hata}{RESET}")

    elif eylem == "api":
        yontem = input("HTTP yontemi (GET/POST/PUT/DELETE): ").strip().upper() or "GET"
        url = input("URL: ").strip()
        try:
            import requests
            yanit = requests.request(yontem, url, timeout=10)
            print(f"{MOR}Durum kodu: {yanit.status_code}{RESET}")
            print(yanit.text[:1000])
        except Exception as hata:
            print(f"{KIRMIZI}[HATA] {hata}{RESET}")

    elif eylem == "websocket":
        if not geri:
            print(f"{KIRMIZI}Kullanim: dev tools websocket <ws_url>{RESET}")
            return
        try:
            import asyncio
            import websockets

            async def _baglan():
                async with websockets.connect(geri[0]) as ws:
                    print(f"{MOR}Baglanti kuruldu: {geri[0]}{RESET}")
                    while True:
                        mesaj = input("gonder> ")
                        if mesaj.lower() in ("cikis", "exit"):
                            break
                        await ws.send(mesaj)
                        yanit = await ws.recv()
                        print(f"< {yanit}")

            asyncio.run(_baglan())
        except ImportError:
            print(f"{KIRMIZI}[HATA] 'websockets' kurulu degil. Once: dev package install websockets{RESET}")
        except Exception as hata:
            print(f"{KIRMIZI}[HATA] {hata}{RESET}")

    else:
        print(f"{KIRMIZI}Kullanim: dev tools <json/yaml/xml/http/api/websocket>{RESET}")


# ==================== ANDROID ====================

def dev_android(alt):
    if not alt:
        print(f"{KIRMIZI}Kullanim: dev android <adb/logcat/apk>{RESET}")
        return
    eylem, geri = alt[0], alt[1:]

    if eylem == "adb":
        try:
            subprocess.run(["adb"] + geri)
        except FileNotFoundError:
            print(f"{KIRMIZI}[HATA] 'adb' bulunamadi. Android SDK Platform-Tools gerekiyor.{RESET}")

    elif eylem == "logcat":
        try:
            subprocess.run(["adb", "logcat"])
        except FileNotFoundError:
            print(f"{KIRMIZI}[HATA] 'adb' bulunamadi.{RESET}")

    elif eylem == "apk":
        if not geri:
            print(f"{KIRMIZI}Kullanim: dev android apk install/sign <APK>{RESET}")
            return
        alt_eylem = geri[0]
        if alt_eylem == "install" and len(geri) >= 2:
            try:
                subprocess.run(["adb", "install", geri[1]])
            except FileNotFoundError:
                print(f"{KIRMIZI}[HATA] 'adb' bulunamadi.{RESET}")
        elif alt_eylem == "sign" and len(geri) >= 2:
            try:
                subprocess.run(["apksigner", "sign", geri[1]], check=True)
                print(f"{MOR}'{geri[1]}' imzalandi.{RESET}")
            except FileNotFoundError:
                print(f"{KIRMIZI}[HATA] 'apksigner' bulunamadi. Android SDK build-tools gerekiyor.{RESET}")
            except subprocess.CalledProcessError as hata:
                print(f"{KIRMIZI}[HATA] Imzalama basarisiz: {hata}{RESET}")
        else:
            print(f"{KIRMIZI}Kullanim: dev android apk install <APK>  |  dev android apk sign <APK>{RESET}")
    else:
        print(f"{KIRMIZI}[HATA] 'dev android {eylem}' gecersiz.{RESET}")


# ==================== YARDIM ====================
def _dev_help():
    print(f"\n{MOR}[ PROJE YÖNETİMİ ]{RESET}")
    print("  dev project create <isim> -python")
    print("  dev project create <isim> -html")
    print("  dev project create <isim> -ast")
    print("  dev project open <isim>")
    print("  dev project delete <isim>")
    print("  dev project rename <eski> <yeni>")
    print("  dev project list")
    print("  dev project tree")

    print(f"\n{MOR}[ KODLAMA ]{RESET}")
    print("  dev code")
    print("  dev run <dosya>")
    print("  dev build -exe")
    print("  dev build -apk")
    print("  dev build -web")
    print("  dev compile <dosya>")
    print("  dev test <dosya>")
    print("  dev debug <dosya>")
    print("  dev profile <dosya>")
    print("  dev format <dosya>")
    print("  dev lint <dosya>")

    print(f"\n{MOR}[ DOSYA İŞLEMLERİ ]{RESET}")
    print("  dev file create <dosya>")
    print("  dev file delete <dosya>")
    print("  dev file copy <kaynak> at <hedef>")
    print("  dev file move <kaynak> at <hedef>")
    print("  dev file zip <dosya>")
    print("  dev file unzip <dosya.zip>")
    print("  dev file search <isim>")
    print("  dev file replace <eski> <yeni>")

    print(f"\n{MOR}[ KLASÖR ]{RESET}")
    print("  dev folder create <isim>")

    print(f"\n{MOR}[ GIT ]{RESET}")
    print("  dev git init")
    print("  dev git clone <url>")
    print("  dev git add .")
    print("  dev git commit \"Mesaj\"")
    print("  dev git push")
    print("  dev git pull")
    print("  dev git branch")
    print("  dev git checkout <branch>")
    print("  dev git merge <branch>")

    print(f"\n{MOR}[ GITHUB ]{RESET}")
    print("  dev github login")
    print("  dev github logout")
    print("  dev github repo create <isim>")
    print("  dev github repo delete <isim>")
    print("  dev github release create")

    print(f"\n{MOR}[ PAKET ]{RESET}")
    print("  dev package install <paket>")
    print("  dev package remove <paket>")
    print("  dev package update <paket>")
    print("  dev package search <paket>")
    print("  dev package list")

    print(f"\n{MOR}[ DOKÜMAN ]{RESET}")
    print("  dev docs readme")
    print("  dev docs create")
    print("  dev docs changelog")
    print("  dev docs license")
    print("  dev docs wiki")

    print(f"\n{MOR}[ AYARLAR ]{RESET}")
    print("  dev config open")
    print("  dev config env")
    print("  dev config secrets")
    print("  dev config variables")

    print(f"\n{MOR}[ YAYINLAMA ]{RESET}")
    print("  dev publish github")
    print("  dev publish exe")
    print("  dev publish apk")
    print("  dev publish web")
    print("  dev publish export")

    print(f"\n{MOR}[ YAPAY ZEKA ]{RESET}")
    print("  dev ai explain <dosya>")
    print("  dev ai optimize <dosya>")
    print("  dev ai fix <dosya>")
    print("  dev ai docs <dosya>")
    print("  dev ai comment <dosya>")

    print(f"\n{MOR}[ ANALİZ ]{RESET}")
    print("  dev analyze stats")
    print("  dev analyze benchmark")
    print("  dev analyze dependencies")
    print("  dev analyze size")

    print(f"\n{MOR}[ ASTRASAGE ]{RESET}")
    print("  dev astra package")
    print("  dev astra upload")
    print("  dev astra export")

    print(f"\n{MOR}[ GELİŞTİRİCİ ARAÇLARI ]{RESET}")
    print("  dev tools json")
    print("  dev tools yaml")
    print("  dev tools xml")
    print("  dev tools http")
    print("  dev tools api")
    print("  dev tools websocket")

    print(f"\n{MOR}[ ANDROID ]{RESET}")
    print("  dev android adb")
    print("  dev android logcat")
    print("  dev android apk install <apk>")
    print("  dev android apk sign <apk>")

    print(f"\n{MOR}[ DİĞER ]{RESET}")
    print("  dev help")
    print("  clear")
    print("  exit")
    print("  dev return -AstraSage")
    print()

def run():
    os.system("clear")
    banner()
    while True:
        try:

            komut = input(
                f"\n{MOR}dev@DevSage:{RESET}"
                f"~/Distros/{os.path.basename(os.getcwd())}# "
            ).strip()
            parcalar = komut.split()

        except (KeyboardInterrupt, EOFError):
            print()
            break

        if not komut:
            continue
        if parcalar[0] != "dev":
                print("[HATA] DevSage komutları 'dev' ile başlamalı.")
                continue

        if len(parcalar) < 2:
            _dev_help()
            continue
        
        kategori = parcalar[1]
        alt = parcalar[2:]
        
        if parcalar[0] == "dev":
            if kategori in ("exit", "quit", "return"):
                break
            elif kategori in ("clear", "cls"):
               os.system("clear")
               banner()
            elif kategori in ("help", "?"):
               _dev_help()
            elif kategori == "project":
              dev_project(alt)
            elif kategori == "code":
              dev_code(alt)
            elif kategori == "file":
              dev_file(alt)
            elif kategori == "folder":
              dev_folder(alt)
            elif kategori == "git":
              dev_git(alt)
            elif kategori == "github":
              dev_github(alt)
            elif kategori == "package":
              dev_package(alt)
            elif kategori == "docs":
              dev_docs(alt)
            elif kategori == "config":
              dev_config(alt)
            elif kategori == "publish":
              dev_publish(alt)
            elif kategori == "ai":
              dev_ai(alt)
            elif kategori == "analyze":
              dev_analyze(alt)
            elif kategori == "astra":
              dev_astra(alt)
            elif kategori == "tools":
              dev_tools(alt)
            elif kategori == "android":
              dev_android(alt)
            elif kategori == ("return", "back"):
            	if alt == "-AstraSage":
            		print("AstraSage'e dönülüyor")
            		time.sleep(0.1)
            		os.system("clear")
            		break
            	else:
            		print(f"[HATA] {alt} adında böyle bir alt komut bulunamadı!")
            else:
              print(f"{KIRMIZI}[HATA] 'dev {kategori}' adinda bir kategori bulunamadi. "
              f"Tum komutlar icin: dev help{RESET}")
                      
if __name__ == '__main__':
	run()