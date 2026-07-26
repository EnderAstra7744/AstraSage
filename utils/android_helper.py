"""
utils/android_helper.py
AstraSage için Android'e özgü entegrasyon (SL4A / androidhelper üzerinden).

NOT: androidhelper modülü sadece Termux:API veya SL4A (Scripting Layer for
Android) kurulu cihazlarda çalışır. Pydroid3'te varsayılan olarak GELMEZ,
ayrıca kurulman gerekebilir. Bu yüzden modül import'u try/except içine
alınmıştır — cihazda yoksa AstraSage çökmez, sadece "desteklenmiyor" der.

Kullanım örnekleri:
  as android -notify "Görev tamamlandı"
  as android -copy "Panoya kopyalanacak metin"
  as android -paste
  as android -share dosya.txt
  as android -vibrate 500
"""

import os
import shutil

try:
    import android
    droid = android.Android()
    ANDROID_DESTEKLI = True
except Exception:
    droid = None
    ANDROID_DESTEKLI = False


def _destek_kontrolu():
    if not ANDROID_DESTEKLI:
        print("[HATA] Android entegrasyonu bu cihazda kullanılamıyor.")
        print("       SL4A / androidhelper modülü bulunamadı.")
        print("       (Bu özellik Termux:API veya SL4A gerektirir.)")
        return False
    return True


def send_notification(baslik, mesaj):
    if not _destek_kontrolu():
        return
    try:
        droid.notify(baslik, mesaj)
        print(f"Bildirim gönderildi: {baslik} - {mesaj}")
    except Exception as hata:
        print(f"[HATA] Bildirim gönderilemedi: {hata}")


def copy_to_clipboard(metin):
    if not _destek_kontrolu():
        return
    try:
        droid.setClipboard(metin)
        print("Metin panoya kopyalandı.")
    except Exception as hata:
        print(f"[HATA] Panoya kopyalama başarısız: {hata}")


def paste_from_clipboard():
    if not _destek_kontrolu():
        return None
    try:
        sonuc = droid.getClipboard()
        metin = sonuc.result
        print(f"Pano içeriği: {metin}")
        return metin
    except Exception as hata:
        print(f"[HATA] Pano okunamadı: {hata}")
        return None


def share_file(dosya_yolu):
    if not _destek_kontrolu():
        return
    if not os.path.exists(dosya_yolu):
        print(f"[HATA] '{dosya_yolu}' bulunamadı.")
        return
    try:
        tam_yol = os.path.abspath(dosya_yolu)
        droid.shareFile(tam_yol, "*/*")
        print(f"'{dosya_yolu}' paylaşım menüsü açıldı.")
    except Exception as hata:
        print(f"[HATA] Dosya paylaşılamadı: {hata}")


def vibrate(milisaniye=500):
    if not _destek_kontrolu():
        return
    try:
        droid.vibrate(milisaniye)
        print(f"Titreşim tetiklendi ({milisaniye}ms).")
    except Exception as hata:
        print(f"[HATA] Titreşim başarısız: {hata}")


def run_android_command(parcalar):
    """
    'as android -<eylem> [argüman]' komutlarını yönetir.
    main.py içinden çağrılır.
    """
    if len(parcalar) < 3:
        print("Kullanım: as android -notify/-copy/-paste/-share/-vibrate <argüman>")
        return

    eylem = parcalar[2].lstrip("-")
    argumanlar = parcalar[3:]

    if eylem == "notify":
        if not argumanlar:
            print("Kullanım: as android -notify <mesaj>")
            return
        send_notification("AstraSage", " ".join(argumanlar))

    elif eylem == "copy":
        if not argumanlar:
            print("Kullanım: as android -copy <metin>")
            return
        copy_to_clipboard(" ".join(argumanlar))

    elif eylem == "paste":
        paste_from_clipboard()

    elif eylem == "share":
        if not argumanlar:
            print("Kullanım: as android -share <dosya>")
            return
        share_file(argumanlar[0])

    elif eylem == "vibrate":
        sure = int(argumanlar[0]) if argumanlar and argumanlar[0].isdigit() else 500
        vibrate(sure)

    else:
        print(f"'{eylem}' adında bir android eylemi bulunamadı.")
