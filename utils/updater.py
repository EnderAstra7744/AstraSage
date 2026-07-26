# AstraSage Update Modülü (v2 - GitHub Canlı Güncelleme)
# Konum: utils/updater.py
# Amaç: GitHub reposundaki değişiklikleri tespit edip sadece değişen dosyaları güncellemek

import os
import json
import shutil
import tarfile
import requests
from datetime import datetime
from pathlib import Path

REPO_OWNER = "EnderAstra7744"
REPO_NAME = "AstraSage"
GITHUB_API = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"
UPDATE_FOLDER = os.path.join("utils", "update")
LOCAL_COMMIT_FILE = os.path.join(UPDATE_FOLDER, "local_commit.json")
HISTORY_PATH = os.path.join(UPDATE_FOLDER, "update_history.json")

# İsteğe bağlı GitHub Token (rate limit için)
GITHUB_TOKEN = None  # İstersen buraya token koyabilirsin


def _headers():
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    return headers


def _load_local_commit():
    if not os.path.exists(LOCAL_COMMIT_FILE):
        return None
    try:
        with open(LOCAL_COMMIT_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("sha")
    except Exception:
        return None


def _save_local_commit(sha):
    os.makedirs(UPDATE_FOLDER, exist_ok=True)
    with open(LOCAL_COMMIT_FILE, "w", encoding="utf-8") as f:
        json.dump({"sha": sha, "updated_at": datetime.now().isoformat()}, f, indent=2)


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
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump({"updates": history}, f, indent=2, ensure_ascii=False)


def _get_latest_commit():
    """GitHub'dan main branch'in son commit SHA'sını alır"""
    url = f"{GITHUB_API}/commits/main"
    try:
        r = requests.get(url, headers=_headers(), timeout=15)
        r.raise_for_status()
        return r.json()["sha"]
    except Exception as e:
        print(f"[HATA] Commit bilgisi alınamadı: {e}")
        return None


def _get_repo_tree(sha=None):
    """Repo'nun tüm dosya listesini recursive olarak alır"""
    if sha is None:
        sha = "main"
    url = f"{GITHUB_API}/git/trees/{sha}?recursive=1"
    try:
        r = requests.get(url, headers=_headers(), timeout=20)
        r.raise_for_status()
        data = r.json()
        # Sadece dosyaları al (blob), klasörleri atla
        files = {}
        for item in data.get("tree", []):
            if item["type"] == "blob":
                files[item["path"]] = item["sha"]
        return files
    except Exception as e:
        print(f"[HATA] Repo tree alınamadı: {e}")
        return None


def _download_file(path, sha):
    """Tek bir dosyayı GitHub'dan indirir"""
    url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/{path}"
    try:
        r = requests.get(url, headers=_headers(), timeout=20)
        r.raise_for_status()
        return r.content
    except Exception as e:
        print(f"[HATA] {path} indirilemedi: {e}")
        return None


def check_updates():
    """as update -cheak updates"""
    print("\n--- AstraSage Güncelleme Kontrolü ---")
    
    remote_sha = _get_latest_commit()
    if not remote_sha:
        return
    
    local_sha = _load_local_commit()
    
    if local_sha is None:
        print("İlk kez kontrol ediliyor... Yerel commit kaydı oluşturuluyor.")
        _save_local_commit(remote_sha)
        print("Şu an en güncel sürümdesiniz.")
        return
    
    if local_sha == remote_sha:
        print("AstraSage zaten en güncel sürümde.")
        return
    
    print("AstraSage'in güncel bir versiyonu tespit edildi.")
    print("as update -nowversion ile yenileyebilirsiniz.")
    print(f"\nYerel  : {local_sha[:7]}")
    print(f"Uzak   : {remote_sha[:7]}")


def _create_dated_backup(changed_and_deleted):
    """Değişecek ve silinecek dosyaları tarihli tar.gz olarak yedekler"""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_name = f"backup_{timestamp}.tar.gz"
    backup_path = os.path.join(UPDATE_FOLDER, backup_name)
    
    os.makedirs(UPDATE_FOLDER, exist_ok=True)
    
    with tarfile.open(backup_path, "w:gz") as tar:
        for path in changed_and_deleted:
            if os.path.exists(path):
                tar.add(path, arcname=path)
    
    print(f"Yedek alındı: {backup_path}")
    return backup_path


def update_nowversion():
    """as update -nowversion"""
    print("\n--- AstraSage Canlı Güncelleme (nowversion) ---")
    
    remote_sha = _get_latest_commit()
    if not remote_sha:
        return
    
    local_sha = _load_local_commit()
    
    if local_sha == remote_sha:
        print("Zaten en güncel sürümdesiniz. Güncelleme gerekmiyor.")
        return
    
    print("Uzak repo tree'si alınıyor...")
    remote_files = _get_repo_tree(remote_sha)
    if remote_files is None:
        return
    
    # Yerel dosyaları tara (sadece repo kökünden itibaren)
    local_files = {}
    for root, dirs, files in os.walk("."):
        # Gereksiz klasörleri atla
        dirs[:] = [d for d in dirs if d not in [".git", "__pycache__", "utils/update"]]
        for f in files:
            full = os.path.join(root, f).lstrip("./").replace("\\", "/")
            if full.startswith("utils/update/"):
                continue
            local_files[full] = True
    
    # Değişen / yeni dosyalar
    to_download = []
    for path, sha in remote_files.items():
        local_path = path
        if not os.path.exists(local_path):
            to_download.append(path)  # yeni dosya
        else:
            # Basit kontrol: her zaman indir (daha doğru hash karşılaştırması yapılabilir)
            to_download.append(path)
    
    # Silinmiş dosyalar (GitHub'da yok ama yerelde var)
    to_delete = []
    for path in local_files:
        if path not in remote_files and not path.startswith("utils/update/"):
            # Kullanıcı verilerini koru (assets içindeki bazı dosyalar)
            if path.startswith("assets/") and path.endswith((".json", ".txt", ".log")):
                continue
            to_delete.append(path)
    
    if not to_download and not to_delete:
        print("Değişiklik bulunamadı.")
        _save_local_commit(remote_sha)
        return
    
    print(f"\nİndirilecek / güncellenecek dosya sayısı : {len(to_download)}")
    print(f"Silinecek dosya sayısı                 : {len(to_delete)}")
    
    # Onay
    cevap = input("\nGüncellemeyi uygulamak istiyor musunuz? (evet/hayır): ").strip().lower()
    if cevap != "evet":
        print("Güncelleme iptal edildi.")
        return
    
    # 1. Yedek al
    print("\nYedek alınıyor...")
    backup_list = list(set(to_download + to_delete))
    _create_dated_backup(backup_list)
    
    # 2. Silinen dosyaları temizle
    for path in to_delete:
        try:
            if os.path.isfile(path):
                os.remove(path)
                print(f"Silindi: {path}")
            elif os.path.isdir(path):
                shutil.rmtree(path)
                print(f"Klasör silindi: {path}")
        except Exception as e:
            print(f"[UYARI] {path} silinemedi: {e}")
    
    # 3. Yeni / değişen dosyaları indir ve yaz
    print("\nDosyalar indiriliyor...")
    success = 0
    for path in to_download:
        content = _download_file(path, remote_files[path])
        if content is None:
            continue
        
        # Klasör yoksa oluştur
        dir_name = os.path.dirname(path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        
        try:
            with open(path, "wb") as f:
                f.write(content)
            print(f"Güncellendi: {path}")
            success += 1
        except Exception as e:
            print(f"[HATA] {path} yazılamadı: {e}")
    
    # 4. Commit kaydını güncelle
    _save_local_commit(remote_sha)
    
    # 5. Geçmişe kaydet
    history = _load_history()
    history.append({
        "type": "nowversion",
        "from_sha": local_sha[:7] if local_sha else "ilk",
        "to_sha": remote_sha[:7],
        "files_updated": success,
        "files_deleted": len(to_delete),
        "tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    _save_history(history)
    
    # 6. ASE imzasını yenile
    try:
        import ASE
        ASE.generate_signature()
        print("ASE imzası yenilendi.")
    except Exception as e:
        print(f"[UYARI] ASE imzası güncellenemedi: {e}")
    
    print(f"\nGüncelleme tamamlandı!")
    print(f"{success} dosya güncellendi, {len(to_delete)} dosya silindi.")
    print("Değişikliklerin etkili olması için AstraSage'i yeniden başlatın.")


def show_update_history():
    history = _load_history()
    if not history:
        print("Henüz hiçbir güncelleme yapılmadı.")
        return
    
    print("Güncelleme Geçmişi:")
    for kayit in history:
        if kayit.get("type") == "nowversion":
            print(f"  - nowversion  {kayit.get('from_sha')} → {kayit.get('to_sha')}  ({kayit.get('tarih')})")
        else:
            print(f"  - {kayit.get('versiyon')}  ({kayit.get('tarih')})")