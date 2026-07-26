"""
utils/alias_manager.py
AstraSage için Alias (kısayol) sistemi.

Kullanım örnekleri:
  as alias ll="as ls -all"
  as alias list
  as alias remove ll
  as alias run ll        (veya doğrudan "ll" yazınca otomatik çözülür)
"""

import os
import json

ALIAS_DOSYASI = "aliases.json"


def load_aliases():
    if not os.path.exists(ALIAS_DOSYASI):
        return {}
    try:
        with open(ALIAS_DOSYASI, "r", encoding="utf-8") as f:
            return json.load(f).get("aliases", {})
    except Exception:
        return {}


def save_aliases(aliases):
    try:
        with open(ALIAS_DOSYASI, "w", encoding="utf-8") as f:
            json.dump({"aliases": aliases}, f, indent=2, ensure_ascii=False)
    except Exception as hata:
        print(f"[HATA] aliases.json kaydedilirken hata oluştu: {hata}")


def parse_alias_tanimi(ham_metin):
    """
    'll="as ls -all"' şeklindeki tanımı (isim, komut) olarak ayırır.
    Girdi hatalıysa (None, None) döner.
    """
    if "=" not in ham_metin:
        return None, None

    isim, komut = ham_metin.split("=", 1)
    isim = isim.strip()
    komut = komut.strip()

    # Tırnak işaretlerini temizle ("..." veya '...')
    if len(komut) >= 2 and komut[0] == komut[-1] and komut[0] in ("'", '"'):
        komut = komut[1:-1]

    if not isim or not komut:
        return None, None

    return isim, komut


def add_alias(ham_metin, aliases):
    isim, komut = parse_alias_tanimi(ham_metin)
    if isim is None:
        print("Kullanım: as alias <isim>=\"<komut>\"")
        return
    aliases[isim] = komut
    save_aliases(aliases)
    print(f"'{isim}' kısayolu tanımlandı → {komut}")


def remove_alias(isim, aliases):
    if isim not in aliases:
        print(f"'{isim}' adında bir kısayol bulunamadı.")
        return
    del aliases[isim]
    save_aliases(aliases)
    print(f"'{isim}' kısayolu silindi.")


def list_aliases(aliases):
    if not aliases:
        print("Henüz hiçbir kısayol tanımlanmadı.")
        return
    print("Tanımlı kısayollar:")
    for isim, komut in aliases.items():
        print(f"  {isim:<12} → {komut}")


def resolve_alias(komut_metni, aliases, derinlik=0):
    """
    Girilen komutun ilk kelimesi bir alias'sa, onu gerçek komuta çevirir.
    Alias'lar zincirleme tanımlanabildiği için (ör. x -> y -> as ls) derinlik
    sınırı konularak sonsuz döngü engellenir.
    """
    if derinlik > 10:
        print("[HATA] Alias zinciri çok derin veya döngüsel, iptal edildi.")
        return komut_metni

    parcalar = komut_metni.split(" ", 1)
    ilk_kelime = parcalar[0]

    if ilk_kelime in aliases:
        yeni_komut = aliases[ilk_kelime]
        if len(parcalar) > 1:
            yeni_komut = f"{yeni_komut} {parcalar[1]}"
        return resolve_alias(yeni_komut, aliases, derinlik + 1)

    return komut_metni
