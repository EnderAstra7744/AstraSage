"""
utils/system_reset.py
AstraSage için özel sistem sıfırlama komutu.

Kullanım:
  as !system -reset          -> onay sorar, onaylanırsa sıfırlar
  as !system -reset /s       -> onay sormadan direkt sıfırlar (silent)

NOT: Bu komut SADECE aşağıdaki "geri getirilebilir / üretilen" verileri siler:
  - data.json               (yüklü kütüphaneler listesi)
  - installed_languages.json
  - history.json            (komut geçmişi)
  - aliases.json            (kısayollar)

astrasage_theme.json SİLİNMEZ — bu bir kullanıcı tercihi (tema), veri değil.
libraries/ klasöründeki gerçek dosyalar da SİLİNMEZ, sadece "yüklü" kaydı silinir.
"""

import os
import json

ASTRASAGE_KOK = os.getcwd()

SIFIRLANACAK_DOSYALAR = {
    "data.json": {"loaded_libraries": []},
    "installed_languages.json": {"languages": []},
    os.path.join(ASTRASAGE_KOK, "assets", "history.json"): {"history": []},
    "aliases.json": {"aliases": {}},
    os.path.join(ASTRASAGE_KOK, "assets", "astrasage_theme.json"): {"banner": "klasik", "renk": "yesil"},
}

KORUNAN_DOSYALAR = [
    os.path.join(ASTRASAGE_KOK, "assets", "astrasage_theme.json"),
]


def _dosyayi_sifirla(yol, bos_icerik):
    try:
        os.makedirs(os.path.dirname(yol) or ".", exist_ok=True)
        with open(yol, "w", encoding="utf-8") as f:
            json.dump(bos_icerik, f, indent=2, ensure_ascii=False)
        return True
    except Exception as hata:
        print(f"[HATA] '{yol}' sıfırlanırken hata oluştu: {hata}")
        return False


def reset_system(force=False):
    if not force:
        print("[⚠] Bu işlem şu verileri kalıcı olarak silecek:")
        for yol in SIFIRLANACAK_DOSYALAR:
            print(f"    - {yol}")
        print("[i] Tema ayarları (astrasage_theme.json) etkilenmeyecek.")
        onay = input("Devam etmek istiyor musunuz? (evet/hayır): ").strip().lower()
        if onay != "evet":
            print("İşlem iptal edildi.")
            return False

    basarili = 0
    for yol, bos_icerik in SIFIRLANACAK_DOSYALAR.items():
        if _dosyayi_sifirla(yol, bos_icerik):
            basarili += 1

    print(f"Sistem sıfırlandı. ({basarili}/{len(SIFIRLANACAK_DOSYALAR)} dosya)")
    print("[i] Terminali yeniden başlatman önerilir (as \\\\boot veya yeniden çalıştır).")
    return True


def run_system_command(parcalar):
    """
    'as !system -<eylem> [/s]' komutlarını yönetir.
    main.py içinden çağrılır.
    """
    if len(parcalar) < 3:
        print("Kullanım: as !system -reset [/s]")
        return

    eylem = parcalar[2].lstrip("-")

    if eylem == "reset":
        silent = len(parcalar) >= 4 and parcalar[3] == "/s"
        reset_system(force=silent)
    else:
        print(f"'{eylem}' adında bir !system eylemi bulunamadı.")
