#AstraSage 'at' Hedef Ayrıştırma Yardımcısı
#Konum: utils/at_helper.py
#Amaç: Komutlardaki "at <hedef>" kısmını ayıklamak ve gerçek dosya yoluna çevirmek

import os

def extract_at_target(parcalar):
    """
    parcalar listesinde 'at' kelimesi varsa, ondan sonraki kelimeyi hedef olarak alır.
    Döndürdüğü değerler:
      (komut_parcalari_at_olmadan, hedef_yol)
      'at' yoksa: (parcalar, None)
    """
    if "at" not in parcalar:
        return parcalar, None
    
    at_index = parcalar.index("at")
    
    if at_index == len(parcalar) - 1:
        # 'at' var ama sonrasında hedef yok
        print("[HATA] 'at' kullanıldı ama hedef belirtilmedi. Örnek: ... at AstraSage/test")
        return parcalar, "__INVALID__"
    
    hedef = parcalar[at_index + 1]
    temiz_parcalar = parcalar[:at_index]
    
    return temiz_parcalar, hedef


def resolve_target_path(hedef):
    """
    Kullanıcının verdiği hedefi gerçek bir klasör yoluna çevirir.
    Klasör yoksa otomatik oluşturur.
    """
    # Sonunda / veya \ varsa temizle, os.path.join ile karışıklık olmasın
    hedef = hedef.rstrip("/\\")
    
    try:
        os.makedirs(hedef, exist_ok=True)
        return hedef
    except Exception as error:
        print(f"[HATA] Hedef klasör oluşturulamadı: {error}")
        return None
