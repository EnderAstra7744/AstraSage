#AstraSage Çekirdek Modülü: ASE (AstraSage Encoding)
#Bu modül normal export/unexport sisteminin DIŞINDADIR.
#Amacı: main.py dosyasının değiştirilip değiştirilmediğini kontrol etmek.

import hashlib
import os
import sys

SIGNATURE_FILE = ".signature"
PROTECTED_FILE = "main.py"


def _calculate_hash(path):
    """Verilen dosyanın SHA-256 hash'ini hesaplar."""
    try:
        with open(path, "rb") as f:
            content = f.read()
        return hashlib.sha256(content).hexdigest()
    except Exception:
        return None


def generate_signature():
    """
    İlk kurulumda ÇALIŞTIRILMASI gereken fonksiyon.
    main.py'nin şu anki hash'ini hesaplayıp .signature dosyasına kaydeder.
    Bu fonksiyon main.py'yi her değiştirdiğinde de tekrar çalıştırılmalı,
    yoksa bütünlük kontrolü her zaman 'değiştirilmiş' diyecektir.
    """
    file_hash = _calculate_hash(PROTECTED_FILE)
    
    if file_hash is None:
        print(f"HATA: '{PROTECTED_FILE}' bulunamadığı için imza oluşturulamadı.")
        return False
    
    try:
        with open(SIGNATURE_FILE, "w", encoding="utf-8") as f:
            f.write(file_hash)
        print(f"İmza oluşturuldu: {SIGNATURE_FILE}")
        return True
    except Exception as error:
        print(f"İmza yazılırken hata oluştu: {error}")
        return False


def verify_integrity():
    """
    Program her başladığında çağrılması gereken fonksiyon.
    main.py'nin hash'ini kayıtlı imza ile karşılaştırır.
    Eşleşmiyorsa veya imza dosyası yoksa False döner.
    """
    if not os.path.exists(SIGNATURE_FILE):
        print("=" * 50)
        print("UYARI: İmza dosyası (.signature) bulunamadı.")
        print("Bu kurulum doğrulanamıyor.")
        print("=" * 50)
        return False
    
    try:
        with open(SIGNATURE_FILE, "r", encoding="utf-8") as f:
            kayitli_hash = f.read().strip()
    except Exception:
        print("UYARI: İmza dosyası okunamadı.")
        return False
    
    guncel_hash = _calculate_hash(PROTECTED_FILE)
    
    if guncel_hash is None:
        print(f"UYARI: '{PROTECTED_FILE}' bulunamadı.")
        return False
    
    if guncel_hash != kayitli_hash:
        print("=" * 50)
        print("BÜTÜNLÜK HATASI TESPİT EDİLDİ!")
        print(f"'{PROTECTED_FILE}' dosyası, kayıtlı imzadan farklı.")
        print("Dosya değiştirilmiş olabilir.")
        print("=" * 50)
        return False
    
    return True


def enforce_integrity():
    """
    main.py'nin en başında çağrılacak fonksiyon.
    Bütünlük doğrulanamazsa programı tamamen durdurur.
    """
    if not verify_integrity():
        print("\nGüvenlik nedeniyle AstraSage başlatılamıyor.")
        sys.exit(1)


KUTUPHANE_ADI = "ASE"
KUTUPHANE_SURUMU = "1.0"
KUTUPHANE_ACIKLAMA = "AstraSage çekirdek bütünlük doğrulama modülü (export/unexport sisteminin dışında)"
