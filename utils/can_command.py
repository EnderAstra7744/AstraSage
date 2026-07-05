#AstraSage 'can' Modülü
#Konum: utils/can_command.py
#Amaç: 'as can create/delete -<anahtar>' komutunun mantığı - basit oluşturma/silme işlemleri

import os
import sys
import time

VARSAYILAN_NULL_ISMI = "null_dosya"


def show_progress_bar(toplam_adim=15, gecikme=0.05):
    """Basit bir ilerleme çubuğu: %0 [##----------]"""
    for adim in range(toplam_adim + 1):
        yuzde = int((adim / toplam_adim) * 100)
        dolu = "#" * adim
        bos = "-" * (toplam_adim - adim)
        
        sys.stdout.write(f"\r%{yuzde:<3} [{dolu}{bos}]")
        sys.stdout.flush()
        time.sleep(gecikme)
    
    print()


def can_create(anahtar):
    """
    'as can create -<anahtar>' komutunun mantığı.
    """
    if anahtar.lower() == "null":
        isim = VARSAYILAN_NULL_ISMI
    else:
        isim = anahtar
    
    if os.path.exists(isim):
        print(f"[HATA] '{isim}' zaten var.")
        return
    
    print(f"\n'{isim}' oluşturuluyor...")
    show_progress_bar()
    
    try:
        with open(isim, "w", encoding="utf-8") as f:
            pass
        print(f"'{isim}' başarıyla oluşturuldu.")
    except Exception as error:
        print(f"[HATA] Oluşturma başarısız: {error}")


def can_delete(anahtar):
    """
    'as can delete -<anahtar>' komutunun mantığı.
    """
    if anahtar.lower() == "null":
        isim = VARSAYILAN_NULL_ISMI
    else:
        isim = anahtar
    
    if not os.path.exists(isim):
        print(f"[HATA] '{isim}' bulunamadı.")
        return
    
    print(f"\n'{isim}' siliniyor...")
    show_progress_bar()
    
    try:
        if os.path.isdir(isim):
            os.rmdir(isim)
        else:
            os.remove(isim)
        print(f"'{isim}' başarıyla silindi.")
    except Exception as error:
        print(f"[HATA] Silme başarısız: {error}")


def run_can_command(parcalar):
    """
    Ana döngüden çağrılacak giriş noktası.
    parcalar: ['as', 'can', 'create', '-isim'] şeklinde gelir.
    """
    if len(parcalar) < 4:
        print("Kullanım: as can create -<isim>  veya  as can delete -<isim>")
        return
    
    eylem = parcalar[2]
    anahtar_ham = parcalar[3]
    
    if not anahtar_ham.startswith("-"):
        print("[HATA] Anahtar '-' ile başlamalı. Örnek: as can create -dosya.txt")
        return
    
    anahtar = anahtar_ham.lstrip("-")
    
    if not anahtar:
        print("[HATA] Anahtar boş olamaz.")
        return
    
    if eylem == "create":
        can_create(anahtar)
    elif eylem == "delete":
        can_delete(anahtar)
    else:
        print(f"[HATA] '{eylem}' geçersiz bir 'can' eylemi. (create veya delete bekleniyor)")
