#AstraSage read/info Modülü
#Konum: utils/read_info.py
#Amaç: 'as read' ve 'as info' komutları için dosya okuma ve bilgi gösterme

import os
import zipfile
import tarfile
import datetime
from utils.ast_format import decode_ast

ARSIV_UZANTILARI = {".zip", ".cf", ".pc", ".tar", ".gz", ".tar.gz"}


def is_arsiv(dosya_yolu):
    """Dosyanın arşiv olup olmadığını kontrol eder."""
    isim = dosya_yolu.lower()
    if isim.endswith(".tar.gz"):
        return True
    _, uzanti = os.path.splitext(isim)
    return uzanti in ARSIV_UZANTILARI


def read_file(dosya_yolu):
    """
    'as read -<yol>' komutunun mantığı.
    Normal dosyaların içeriğini, arşivlerin içindeki dosya listesini gösterir.
    """
    if not os.path.exists(dosya_yolu):
        print(f"[HATA] '{dosya_yolu}' bulunamadı.")
        return

    # Arşiv dosyası mı?
    if is_arsiv(dosya_yolu):
        _read_arsiv(dosya_yolu)
        return

    # .ast dosyası mı?
    if dosya_yolu.endswith(".ast"):
        _read_ast(dosya_yolu)
        return

    # Normal metin dosyası
    _read_normal(dosya_yolu)


def _read_arsiv(dosya_yolu):
    """Arşiv dosyasının içindeki dosya/klasörleri listeler."""
    print(f"\n[Arşiv İçeriği: {os.path.basename(dosya_yolu)}]")
    print("-" * 40)

    try:
        if dosya_yolu.endswith(".tar.gz") or dosya_yolu.endswith(".tar"):
            with tarfile.open(dosya_yolu, "r:*") as tar:
                icerik = tar.getnames()
                for item in sorted(icerik):
                    print(f"  {item}")
        else:
            with zipfile.ZipFile(dosya_yolu, "r") as zf:
                icerik = zf.namelist()
                for item in sorted(icerik):
                    bilgi = zf.getinfo(item)
                    boyut = bilgi.file_size
                    print(f"  {item:<40} {boyut:>8} byte")

        print("-" * 40)
        print(f"Toplam: {len(icerik)} öğe")

    except Exception as error:
        print(f"[HATA] Arşiv okunamadı: {error}")


def _read_ast(dosya_yolu):
    """.ast dosyasının şifresini çözüp içeriğini gösterir."""
    print(f"\n[.ast Dosyası: {os.path.basename(dosya_yolu)}]")
    print("-" * 40)
    kod = decode_ast(dosya_yolu)
    if kod:
        print(kod)
    else:
        print("[HATA] .ast dosyası çözülemedi.")
    print("-" * 40)


def _read_normal(dosya_yolu):
    """Normal metin dosyasının içeriğini ekrana yazar."""
    print(f"\n[{os.path.basename(dosya_yolu)}]")
    print("-" * 40)
    try:
        with open(dosya_yolu, "r", encoding="utf-8") as f:
            icerik = f.read()
        print(icerik)
        print("-" * 40)
        satir_sayisi = len(icerik.splitlines())
        print(f"Toplam: {satir_sayisi} satır")
    except UnicodeDecodeError:
        print("[BİLGİ] Bu dosya metin formatında değil (binary dosya).")
    except Exception as error:
        print(f"[HATA] Dosya okunamadı: {error}")


def info_file(dosya_yolu):
    """
    'as info -<yol>' komutunun mantığı.
    Dosya veya klasör hakkında detaylı bilgi gösterir.
    """
    if not os.path.exists(dosya_yolu):
        print(f"[HATA] '{dosya_yolu}' bulunamadı.")
        return

    stat = os.stat(dosya_yolu)

    olusturma = datetime.datetime.fromtimestamp(stat.st_ctime).strftime("%d/%m/%Y %H:%M:%S")
    degisiklik = datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%d/%m/%Y %H:%M:%S")

    boyut = stat.st_size
    if boyut < 1024:
        boyut_str = f"{boyut} byte"
    elif boyut < 1024 * 1024:
        boyut_str = f"{boyut / 1024:.2f} KB"
    else:
        boyut_str = f"{boyut / (1024 * 1024):.2f} MB"

    _, uzanti = os.path.splitext(dosya_yolu)

    if os.path.isdir(dosya_yolu):
        tur = "Klasör"
        icerik_sayisi = len(os.listdir(dosya_yolu))
    elif is_arsiv(dosya_yolu):
        tur = f"Arşiv ({uzanti})"
        icerik_sayisi = None
    elif uzanti == ".py":
        tur = "Python Dosyası"
        icerik_sayisi = None
    elif uzanti == ".ast":
        tur = "AstraSage Şifreli Dosya (.ast)"
        icerik_sayisi = None
    elif uzanti == ".json":
        tur = "JSON Dosyası"
        icerik_sayisi = None
    elif uzanti == ".md":
        tur = "Markdown Dosyası"
        icerik_sayisi = None
    else:
        tur = f"Dosya ({uzanti if uzanti else 'uzantısız'})"
        icerik_sayisi = None

    print(f"\n[Dosya Bilgisi: {os.path.basename(dosya_yolu)}]")
    print("-" * 40)
    print(f"Tür          : {tur}")
    print(f"Tam Yol      : {os.path.abspath(dosya_yolu)}")
    print(f"Boyut        : {boyut_str}")
    print(f"Oluşturulma  : {olusturma}")
    print(f"Son Değişiklik: {degisiklik}")

    if icerik_sayisi is not None:
        print(f"İçerik Sayısı: {icerik_sayisi} öğe")

    if os.path.isfile(dosya_yolu) and not is_arsiv(dosya_yolu) and uzanti not in {".ast"}:
        try:
            with open(dosya_yolu, "r", encoding="utf-8") as f:
                satirlar = f.readlines()
            print(f"Satır Sayısı : {len(satirlar)}")
        except Exception:
            pass

    print("-" * 40)