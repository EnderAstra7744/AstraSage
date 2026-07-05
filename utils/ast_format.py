#AstraSage .ast Format Modülü
#Konum: utils/ast_format.py
#Amaç: .py dosyalarını AES ile şifreleyip .ast formatında saklamak, gerektiğinde çözüp çalıştırmak

import os
import pyaes
import hashlib

#Sabit anahtar - sadece AstraSage'in bu dosyaları çözebilmesi için
#Not: Bu anahtar kodun içinde sabit olduğu için, AstraSage'in kaynak koduna
#erişebilen biri teorik olarak şifreyi çözebilir. Gerçek bir "kırılamaz" güvenlik
#değil, ama dosyanın doğrudan metin editörüyle okunmasını engeller.
_GIZLI_ANAHTAR_METNI = "AstraSage-EnderAstra-Encoding-Key-2026"
_AES_KEY = hashlib.sha256(_GIZLI_ANAHTAR_METNI.encode()).digest()  # 32 byte, AES-256 için


def _get_aes():
    return pyaes.AESModeOfOperationCTR(_AES_KEY)


def encode_to_ast(py_dosya_yolu):
    """
    Bir .py dosyasını okuyup AES ile şifreler, .ast uzantısıyla kaydeder.
    """
    if not os.path.exists(py_dosya_yolu):
        print(f"[HATA] '{py_dosya_yolu}' bulunamadı.")
        return None
    
    try:
        with open(py_dosya_yolu, "r", encoding="utf-8") as f:
            icerik = f.read()
    except Exception as error:
        print(f"[HATA] Dosya okunamadı: {error}")
        return None
    
    try:
        aes = _get_aes()
        sifreli_veri = aes.encrypt(icerik.encode("utf-8"))
    except Exception as error:
        print(f"[HATA] Şifreleme başarısız: {error}")
        return None
    
    ast_yolu = os.path.splitext(py_dosya_yolu)[0] + ".ast"
    
    try:
        with open(ast_yolu, "wb") as f:
            f.write(sifreli_veri)
        print(f"'{ast_yolu}' başarıyla oluşturuldu (şifrelenmiş).")
        return ast_yolu
    except Exception as error:
        print(f"[HATA] .ast dosyası kaydedilemedi: {error}")
        return None


def decode_ast(ast_dosya_yolu):
    """
    Bir .ast dosyasını okuyup şifresini çözer, düz Python kodu (string) olarak döner.
    """
    if not os.path.exists(ast_dosya_yolu):
        print(f"[HATA] '{ast_dosya_yolu}' bulunamadı.")
        return None
    
    try:
        with open(ast_dosya_yolu, "rb") as f:
            sifreli_veri = f.read()
    except Exception as error:
        print(f"[HATA] .ast dosyası okunamadı: {error}")
        return None
    
    try:
        aes = _get_aes()
        cozulmus_veri = aes.decrypt(sifreli_veri)
        return cozulmus_veri.decode("utf-8")
    except Exception as error:
        print(f"[HATA] Şifre çözme başarısız: {error}")
        return None
