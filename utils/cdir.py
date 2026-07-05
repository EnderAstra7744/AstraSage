#AstraSage cdir Modülü
#Konum: utils/cdir.py
#Amaç: AstraSage klasörü içinde dosya arayıp, bulunan dosyayı başka bir konuma taşımak

import os
import shutil


def find_file(dosya_ismi, baslangic_dizini="."):
    """
    AstraSage klasörü (ve alt klasörleri) içinde dosya ismiyle arama yapar.
    Bulunan tüm eşleşmelerin tam yollarını liste olarak döner.
    """
    bulunanlar = []
    
    for kok, klasorler, dosyalar in os.walk(baslangic_dizini):
        if dosya_ismi in dosyalar:
            bulunanlar.append(os.path.join(kok, dosya_ismi))
    
    return bulunanlar


def cdir_file(dosya_ismi, hedef):
    """
    'as cdir <dosya> at <hedef>' komutunun ana mantığı.
    """
    if not dosya_ismi or not hedef:
        print("Kullanım: as cdir <dosya ismi> at <yeni yol>")
        return
    
    bulunanlar = find_file(dosya_ismi)
    
    if len(bulunanlar) == 0:
        print(f"[HATA] '{dosya_ismi}' AstraSage içinde bulunamadı.")
        return
    
    if len(bulunanlar) > 1:
        print(f"[UYARI] '{dosya_ismi}' birden fazla yerde bulundu:")
        for index, yol in enumerate(bulunanlar, start=1):
            print(f"  [{index}] {yol}")
        
        secim = input("Hangisini taşımak istersiniz (numara girin): ").strip()
        
        try:
            secim_index = int(secim) - 1
            if secim_index < 0 or secim_index >= len(bulunanlar):
                print("[HATA] Geçersiz seçim.")
                return
            kaynak = bulunanlar[secim_index]
        except ValueError:
            print("[HATA] Geçersiz giriş, sayı bekleniyordu.")
            return
    else:
        kaynak = bulunanlar[0]
    
    try:
        os.makedirs(hedef, exist_ok=True)
        hedef_dosya_yolu = os.path.join(hedef, dosya_ismi)
        
        shutil.move(kaynak, hedef_dosya_yolu)
        print(f"'{dosya_ismi}' başarıyla taşındı: {kaynak}  -->  {hedef_dosya_yolu}")
    except Exception as error:
        print(f"[HATA] Taşıma sırasında hata oluştu: {error}")
