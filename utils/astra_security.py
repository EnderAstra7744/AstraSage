#AstraSage AstraSecurity Modülü
#Konum: utils/astra_security.py
#Amaç: İndirilen/yüklenen dosyaları tehlikeli kod için taramak

import os
import zipfile
import re
from utils.ast_format import decode_ast

#Tehlikeli olarak işaretlenen kalıplar
TEHLIKELI_KALIPLAR = [
    #Sistem komutları
    (r"\bos\.system\s*\(", "os.system() - sistem komutu çalıştırma"),
    (r"\bsubprocess\.(run|call|Popen|check_output)\s*\(", "subprocess - dış process çalıştırma"),
    (r"\beval\s*\(", "eval() - dinamik kod çalıştırma"),
    (r"\bexec\s*\(", "exec() - dinamik kod çalıştırma"),
    (r"\b__import__\s*\(", "__import__() - dinamik modül yükleme"),
    
    #Dosya silme/değiştirme
    (r"\bos\.remove\s*\(", "os.remove() - dosya silme"),
    (r"\bos\.rmdir\s*\(", "os.rmdir() - klasör silme"),
    (r"\bshutil\.rmtree\s*\(", "shutil.rmtree() - klasör ağacı silme"),
    (r"\bshutil\.move\s*\(", "shutil.move() - dosya taşıma"),
    
    #Ağ/internet erişimi
    (r"\bsocket\.connect\s*\(", "socket.connect() - ağ bağlantısı"),
    (r"\brequests\.(get|post|put|delete)\s*\(", "requests - internet isteği"),
    
    #Hassas veri erişimi
    (r"open\s*\([^)]*['\"]w['\"]", "dosyaya yazma işlemi"),
    (r"\bpickle\.(load|loads)\s*\(", "pickle.load() - güvensiz veri yükleme"),
]

#Uyarı verilecek ama engellenmeyen kalıplar (şüpheli ama her zaman tehlikeli değil)
SUPHE_KALIPLARI = [
    (r"\bimport\s+os\b", "os modülü import ediliyor"),
    (r"\bimport\s+sys\b", "sys modülü import ediliyor"),
    (r"\bimport\s+subprocess\b", "subprocess modülü import ediliyor"),
    (r"\bimport\s+socket\b", "socket modülü import ediliyor"),
]


def _kod_tara(kod_metni, dosya_ismi=""):
    """
    Verilen kod metnini tehlikeli kalıplar için tarar.
    Döner: (guvenli: bool, tehlikeler: list, supheliler: list)
    """
    tehlikeler = []
    supheliler = []

    for pattern, aciklama in TEHLIKELI_KALIPLAR:
        if re.search(pattern, kod_metni):
            tehlikeler.append(aciklama)

    for pattern, aciklama in SUPHE_KALIPLARI:
        if re.search(pattern, kod_metni):
            supheliler.append(aciklama)

    guvenli = len(tehlikeler) == 0
    return guvenli, tehlikeler, supheliler


def _sonuc_yazdir(dosya_ismi, guvenli, tehlikeler, supheliler):
    """Tarama sonucunu ekrana yazar."""
    print(f"\n[AstraSecurity] '{dosya_ismi}' taranıyor...")

    if tehlikeler:
        print(f"[ENGELLENDI] Tehlikeli kod tespit edildi:")
        for t in tehlikeler:
            print(f"  ✗ {t}")

    if supheliler:
        print(f"[UYARI] Şüpheli kullanımlar:")
        for s in supheliler:
            print(f"  ! {s}")

    if guvenli:
        print(f"[GUVENLI] '{dosya_ismi}' temiz görünüyor.")

    return guvenli


def tara_py(dosya_yolu):
    """
    Bir .py dosyasını tarar.
    Döner: True (güvenli) / False (tehlikeli)
    """
    try:
        with open(dosya_yolu, "r", encoding="utf-8") as f:
            kod = f.read()
    except Exception as error:
        print(f"[AstraSecurity] Dosya okunamadı: {error}")
        return False

    dosya_ismi = os.path.basename(dosya_yolu)
    guvenli, tehlikeler, supheliler = _kod_tara(kod, dosya_ismi)
    return _sonuc_yazdir(dosya_ismi, guvenli, tehlikeler, supheliler)


def tara_ast(dosya_yolu):
    """
    Bir .ast dosyasını çözüp tarar.
    Döner: True (güvenli) / False (tehlikeli)
    """
    kod = decode_ast(dosya_yolu)
    if kod is None:
        print(f"[AstraSecurity] .ast dosyası çözülemedi, engellendi.")
        return False

    dosya_ismi = os.path.basename(dosya_yolu)
    guvenli, tehlikeler, supheliler = _kod_tara(kod, dosya_ismi)
    return _sonuc_yazdir(dosya_ismi, guvenli, tehlikeler, supheliler)


def tara_arsiv(dosya_yolu):
    """
    Bir .cf veya .pc arşivinin içindeki tüm .py dosyalarını tarar.
    Döner: True (tümü güvenli) / False (en az biri tehlikeli)
    """
    dosya_ismi = os.path.basename(dosya_yolu)
    print(f"\n[AstraSecurity] '{dosya_ismi}' arşivi taranıyor...")

    try:
        with zipfile.ZipFile(dosya_yolu, "r") as zf:
            py_dosyalari = [f for f in zf.namelist() if f.endswith(".py")]

            if not py_dosyalari:
                print(f"[AstraSecurity] Arşivde .py dosyası bulunamadı.")
                return True

            tum_guvenli = True
            for py_dosya in py_dosyalari:
                with zf.open(py_dosya) as f:
                    kod = f.read().decode("utf-8", errors="ignore")

                guvenli, tehlikeler, supheliler = _kod_tara(kod, py_dosya)
                _sonuc_yazdir(py_dosya, guvenli, tehlikeler, supheliler)

                if not guvenli:
                    tum_guvenli = False

            if not tum_guvenli:
                print(f"[ENGELLENDI] '{dosya_ismi}' arşivi tehlikeli kod içeriyor, kurulmadı.")

            return tum_guvenli

    except zipfile.BadZipFile:
        print(f"[AstraSecurity] '{dosya_ismi}' geçerli bir arşiv değil, engellendi.")
        return False
    except Exception as error:
        print(f"[AstraSecurity] Tarama hatası: {error}")
        return False


def tara(dosya_yolu):
    """
    Ana tarama fonksiyonu — dosya türüne göre doğru tarayıcıyı çağırır.
    load_library ve download_from_github'dan önce çağrılacak.
    Döner: True (güvenli, devam et) / False (tehlikeli, engelle)
    """
    if not os.path.exists(dosya_yolu):
        return True  # Dosya yoksa load_library zaten hata verecek

    if dosya_yolu.endswith(".ast"):
        return tara_ast(dosya_yolu)
    elif dosya_yolu.endswith((".cf", ".pc", ".zip")):
        return tara_arsiv(dosya_yolu)
    elif dosya_yolu.endswith(".py"):
        return tara_py(dosya_yolu)
    else:
        return True  # Bilinmeyen uzantı, geç
