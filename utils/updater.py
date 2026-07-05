#AstraSage Update Modülü
#Konum: utils/updater.py
#Amaç: Hazırlanmış .tar.gz arşivlerini uygulayarak AstraSage'i güncellemek

import os
import json
import shutil
import tarfile
from datetime import datetime

UPDATE_FOLDER = os.path.join("utils", "update")
ARCHIVE_PATH = os.path.join(UPDATE_FOLDER, "new_versions.tar.gz")
HISTORY_PATH = os.path.join(UPDATE_FOLDER, "update_history.json")
BACKUP_PATH = "main_backup.py"
MAIN_FILE = "main.py"


def _load_history():
    if not os.path.exists(HISTORY_PATH):
        return []
    try:
        with open(HISTORY_PATH, "r", encoding="utf-8") as f:
            return json.load(f).get("updates", [])
    except Exception:
        return []


def _save_history(history):
    os.makedirs(UPDATE_FOLDER, exist_ok=True)
    try:
        with open(HISTORY_PATH, "w", encoding="utf-8") as f:
            json.dump({"updates": history}, f, indent=2, ensure_ascii=False)
    except Exception as error:
        print(f"[HATA] Güncelleme geçmişi kaydedilirken hata oluştu: {error}")


def update_system(versiyon):
    print(f"\n--- AstraSage Güncelleme Sistemi ---")
    print(f"Hedef versiyon: {versiyon}\n")
    
    # 1. Arşiv dosyası var mı kontrol et
    if not os.path.exists(ARCHIVE_PATH):
        print(f"[HATA] Güncelleme dosyası bulunamadı: {ARCHIVE_PATH}")
        print("Güncellemeden önce bu dosyayı oraya koymanız gerekiyor.")
        return
    
    gecmis = _load_history()
    
    if any(kayit.get("versiyon") == versiyon for kayit in gecmis):
        cevap = input(f"'{versiyon}' zaten kurulu görünüyor. Tekrar uygulamak istiyor musunuz? (evet/hayır): ").strip().lower()
        if cevap != "evet":
            print("Güncelleme iptal edildi.")
            return
    
    # 2. main.py'yi yedekle
    if os.path.exists(MAIN_FILE):
        try:
            shutil.copy(MAIN_FILE, BACKUP_PATH)
            print(f"Yedek alındı: {BACKUP_PATH}")
        except Exception as error:
            print(f"[HATA] Yedekleme başarısız, güncelleme durduruldu: {error}")
            return
    else:
        print("[UYARI] main.py bulunamadı, yedekleme atlandı.")
    
    # 3. Arşivi çıkar (mevcut dosyaların üzerine yazarak)
    try:
        with tarfile.open(ARCHIVE_PATH, "r:gz") as tar:
            tar.extractall(path=".")
        print("Yeni sürüm dosyaları başarıyla uygulandı.")
    except Exception as error:
        print(f"[HATA] Arşiv açılırken hata oluştu: {error}")
        print(f"Sorun yaşarsanız '{BACKUP_PATH}' dosyasını 'main.py' olarak geri adlandırabilirsiniz.")
        return
    
    # 4. ASE imzasını yeniden oluştur (main.py değiştiği için zorunlu)
    try:
        import ASE
        ASE.generate_signature()
    except Exception as error:
        print(f"[UYARI] ASE imzası güncellenemedi: {error}")
        print("Program bir sonraki açılışta bütünlük hatası verebilir.")
    
    # 5. Geçmişe kaydet
    gecmis.append({
        "versiyon": versiyon,
        "tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    _save_history(gecmis)
    
    print(f"\nGüncelleme tamamlandı: {versiyon}")
    print("Değişikliklerin etkili olması için AstraSage'i yeniden başlatın.")


def show_update_history():
    gecmis = _load_history()
    
    if len(gecmis) == 0:
        print("Henüz hiçbir güncelleme yapılmadı.")
        return
    
    print("Güncelleme Geçmişi:")
    for kayit in gecmis:
        print(f"  - {kayit.get('versiyon')}  ({kayit.get('tarih')})")
