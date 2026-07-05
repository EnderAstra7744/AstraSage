#AstraSage Code Editor Modülü
#Konum: utils/code_editor.py
#Amaç: Yüklü dil API'lerine bağlı olarak basit kod yazma ve çalıştırma

import os
import subprocess
import sys
import json

PROJECTS_FOLDER = os.path.join("assets", "created_projects")
DESTEKLENEN_DILLER = ["python", "json"]

#Editöre dosya ismi, dil ve installed_languages listesi gelir
def open_code_editor(installed_languages):
    if len(installed_languages) == 0:
        print("[HATA] Henüz hiçbir dil kurulu değil.")
        print("Önce 'asinstall <dil>' komutuyla bir dil kurun (örn: asinstall python)")
        return
    
    print("Kurulu diller: " + ", ".join(installed_languages))
    dil = input("Hangi dilde kod yazmak istersiniz: ").strip().lower()
    
    if dil not in installed_languages:
        print(f"[HATA] '{dil}' kurulu değil. Önce 'asinstall {dil}' ile kurun.")
        return
    
    if dil not in DESTEKLENEN_DILLER:
        print(f"[HATA] '{dil}' için editör desteği henüz hazır değil.")
        return
    
    uzanti = ".py" if dil == "python" else ".json"
    
    dosya_ismi = input(f"Dosya ismini girin (örn: deneme{uzanti}): ").strip()
    if not dosya_ismi:
        print("İşlem iptal edildi.")
        return
    
    if not dosya_ismi.endswith(uzanti):
        dosya_ismi += uzanti
    
    os.makedirs(PROJECTS_FOLDER, exist_ok=True)
    dosya_yolu = os.path.join(PROJECTS_FOLDER, dosya_ismi)
    
    print(f"\n'{dosya_ismi}' için kod yazmaya başlayın.")
    print("Her satırı yazıp Enter'a basın.")
    print("Son satırı silmek için  : geri")
    print("Bitirmek için           : bitir\n")
    
    satirlar = []
    while True:
        satir = input(">>> ")
        
        if satir.strip().lower() == "bitir":
            break
        
        if satir.strip().lower() == "geri":
            if len(satirlar) == 0:
                print("[BİLGİ] Silinecek satır yok.")
            else:
                silinen = satirlar.pop()
                print(f"[BİLGİ] Silindi: {silinen}")
            continue
        
        satirlar.append(satir)
    
    icerik = "\n".join(satirlar)
    
    # JSON için: kaydetmeden önce geçerlilik kontrolü
    if dil == "json":
        if not validate_json(icerik):
            return
    
    try:
        with open(dosya_yolu, "w", encoding="utf-8") as dosya:
            dosya.write(icerik)
        print(f"\n'{dosya_ismi}' başarıyla kaydedildi. (Konum: {dosya_yolu})")
    except Exception as error:
        print(f"[HATA] Dosya kaydedilirken hata oluştu: {error}")
        return
    
    if dil == "python":
        calistir = input("\nBu kodu şimdi çalıştırmak ister misiniz? (run/hayır): ").strip().lower()
        if calistir == "run":
            run_python_file(dosya_yolu)
    elif dil == "json":
        print("(JSON dosyaları 'çalıştırılmaz', sadece geçerliliği kontrol edilir.)")


#JSON içeriğinin geçerli olup olmadığını kontrol eder
def validate_json(icerik):
    if icerik.strip() == "":
        print("[HATA] Boş içerik geçerli bir JSON değil.")
        cevap = input("Yine de kaydetmek ister misiniz? (evet/hayır): ").strip().lower()
        return cevap == "evet"
    
    try:
        json.loads(icerik)
        print("\n[BİLGİ] Geçerli bir JSON yapısı.")
        return True
    except json.JSONDecodeError as error:
        print(f"\n[HATA] Geçersiz JSON: {error}")
        cevap = input("Hataya rağmen kaydetmek ister misiniz? (evet/hayır): ").strip().lower()
        return cevap == "evet"


#Yazılan Python dosyasını çalıştırır
def run_python_file(dosya_yolu):
    if not os.path.exists(dosya_yolu):
        print(f"[HATA] '{dosya_yolu}' bulunamadı.")
        return
    
    print(f"\n--- '{dosya_yolu}' çalıştırılıyor ---\n")
    try:
        sonuc = subprocess.run(
            [sys.executable, dosya_yolu],
            capture_output=True, text=True, timeout=15
        )
        
        if sonuc.stdout:
            print(sonuc.stdout)
        
        if sonuc.returncode != 0:
            print("[HATA] Kodda bir hata var, çalıştırma başarısız oldu:\n")
            print(sonuc.stderr)
        else:
            print(f"--- Çalıştırma başarıyla bitti (çıkış kodu: {sonuc.returncode}) ---")
    
    except subprocess.TimeoutExpired:
        print("[HATA] Çalıştırma zaman aşımına uğradı (15 saniye sınırı).")
    except Exception as error:
        print(f"[HATA] Çalıştırma sırasında hata oluştu: {error}")
