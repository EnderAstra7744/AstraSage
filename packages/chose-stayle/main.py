#AstraSage Chose-Stayle Paketi
#Açıklama: AstraSage terminal teması ve banner özelleştirme paketi

import json
import os

TEMA_DOSYASI = "assets/astrasage_theme.json"

RENKLER = {
    "yesil":      {"YESIL": "\033[92m", "KOYU": "\033[32m", "KIRMIZI": "\033[91m", "SARI": "\033[93m", "RESET": "\033[0m", "BOLD": "\033[1m"},
    "mavi":       {"YESIL": "\033[94m", "KOYU": "\033[34m", "KIRMIZI": "\033[91m", "SARI": "\033[93m", "RESET": "\033[0m", "BOLD": "\033[1m"},
    "kirmizi":    {"YESIL": "\033[91m", "KOYU": "\033[31m", "KIRMIZI": "\033[93m", "SARI": "\033[92m", "RESET": "\033[0m", "BOLD": "\033[1m"},
    "sari":       {"YESIL": "\033[93m", "KOYU": "\033[33m", "KIRMIZI": "\033[91m", "SARI": "\033[92m", "RESET": "\033[0m", "BOLD": "\033[1m"},
    "mor":        {"YESIL": "\033[95m", "KOYU": "\033[35m", "KIRMIZI": "\033[91m", "SARI": "\033[93m", "RESET": "\033[0m", "BOLD": "\033[1m"},
    "turkuaz":    {"YESIL": "\033[96m", "KOYU": "\033[36m", "KIRMIZI": "\033[91m", "SARI": "\033[93m", "RESET": "\033[0m", "BOLD": "\033[1m"},
}

BANNER_STILLERI = {
    "klasik":  "Astra Sage'e Hoşgeldin!!!",
    "minimal": "[ AstraSage ]",
    "bold":    "★ ASTRASAGE ★",
    "ascii":   """
    _         _            ____
   / \\   ___ | |_ _ __ __ / ___|  __ _  __ _  ___
  / _ \\ / __|| __| '__/ _` \\___ \\ / _` |/ _` |/ _ \\
 / ___ \\\\__ \\| |_| | | (_| |___) | (_| | (_| |  __/
/_/   \\_\\___/ \\__|_|  \\__,_|____/ \\__,_|\\__, |\\___|
                                         |___/
""",
}


def load_theme():
    if not os.path.exists(TEMA_DOSYASI):
        return {"renk": "yesil", "banner": "klasik"}
    try:
        with open(TEMA_DOSYASI, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"renk": "yesil", "banner": "klasik"}


def save_theme(tema):
    os.makedirs(os.path.dirname(TEMA_DOSYASI), exist_ok=True)
    try:
        with open(TEMA_DOSYASI, "w", encoding="utf-8") as f:
            json.dump(tema, f, indent=2, ensure_ascii=False)
    except Exception as error:
        print(f"[HATA] Tema kaydedilemedi: {error}")


def show_menu():
    tema = load_theme()

    print("\n" + "=" * 45)
    print("       CHOSE-STAYLE - Tema Seçici")
    print("=" * 45)
    print(f"Aktif renk  : {tema['renk']}")
    print(f"Aktif banner: {tema['banner']}")
    print("=" * 45)

    print("\n[1] Renk Teması Seç")
    print("[2] Banner Stili Seç")
    print("[3] Önizleme Göster")
    print("[4] Çıkış")

    secim = input("\nSeçiminiz: ").strip()

    if secim == "1":
        renk_sec(tema)
    elif secim == "2":
        banner_sec(tema)
    elif secim == "3":
        onizleme(tema)
    elif secim == "4":
        return
    else:
        print("Geçersiz seçim.")


def renk_sec(tema):
    print("\nMevcut renkler:")
    for i, isim in enumerate(RENKLER.keys(), start=1):
        renk = RENKLER[isim]
        print(f"  [{i}] {renk['YESIL']}{isim}{renk['RESET']}")

    secim = input("\nRenk numarası seçin: ").strip()
    try:
        index = int(secim) - 1
        isim = list(RENKLER.keys())[index]
        tema["renk"] = isim
        save_theme(tema)
        print(f"Renk teması '{isim}' olarak ayarlandı.")
        print("Değişikliğin etkili olması için AstraSage'i yeniden başlatın.")
    except (ValueError, IndexError):
        print("[HATA] Geçersiz seçim.")


def banner_sec(tema):
    print("\nMevcut banner stilleri:")
    for i, isim in enumerate(BANNER_STILLERI.keys(), start=1):
        print(f"  [{i}] {isim}")

    secim = input("\nBanner numarası seçin: ").strip()
    try:
        index = int(secim) - 1
        isim = list(BANNER_STILLERI.keys())[index]
        tema["banner"] = isim
        save_theme(tema)
        print(f"Banner stili '{isim}' olarak ayarlandı.")
        print("Değişikliğin etkili olması için AstraSage'i yeniden başlatın.")
    except (ValueError, IndexError):
        print("[HATA] Geçersiz seçim.")


def onizleme(tema):
    renk = RENKLER.get(tema["renk"], RENKLER["yesil"])
    banner_metni = BANNER_STILLERI.get(tema["banner"], BANNER_STILLERI["klasik"])

    print("\n--- ÖNİZLEME ---")
    print(renk["YESIL"] + banner_metni + renk["RESET"])
    print(renk["YESIL"] + "=" * 45 + renk["RESET"])
    print(renk["KOYU"] + "  as list / as export / as help" + renk["RESET"])
    print(renk["YESIL"] + "=" * 45 + renk["RESET"])
    print(f"\n{renk['YESIL']}/~\\AstraSage/$>> {renk['RESET']}")
    print("--- ÖNİZLEME SONU ---")


def run(parcalar=None):
    show_menu()
