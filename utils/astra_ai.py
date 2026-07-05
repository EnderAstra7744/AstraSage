#AstraSage AstraAI Modülü (Gerçek Makine Öğrenmesi - Naive Bayes)
#Konum: utils/astra_ai.py
#Amaç: Basit bir metin sınıflandırıcı - mesajın "duygu" tonunu (olumlu/olumsuz/nötr) tahmin eder
#Not: Bu ChatGPT/Claude gibi bir dil modeli DEĞİLDİR. Gerçek ama çok basit bir
#Naive Bayes sınıflandırma algoritmasıdır - sadece eğitildiği örneklere göre tahmin yapar.

import math
import os
import json
from collections import defaultdict

MODEL_FILE = os.path.join("assets", "astra_ai_model.json")

#Başlangıç eğitim verisi - örnek mesajlar ve etiketleri
_VARSAYILAN_EGITIM_VERISI = [
    ("bugün çok güzel bir gün", "olumlu"),
    ("seni seviyorum", "olumlu"),
    ("harika bir başarı oldu", "olumlu"),
    ("çok mutluyum", "olumlu"),
    ("teşekkür ederim çok yardımcı oldun", "olumlu"),
    ("bu projeyi tamamlamak güzel hissettiriyor", "olumlu"),
    
    ("çok kötü bir gün geçirdim", "olumsuz"),
    ("bu hiç işe yaramadı", "olumsuz"),
    ("çok sinirliyim şu anda", "olumsuz"),
    ("hata aldım ve çok üzüldüm", "olumsuz"),
    ("bu hiç güzel değil", "olumsuz"),
    ("yapamadım çok kötü oldu", "olumsuz"),
    
    ("saat kaç şu anda", "nötr"),
    ("dosyayı kaydettim", "nötr"),
    ("kütüphane yüklendi", "nötr"),
    ("bu bir test mesajıdır", "nötr"),
    ("sistem çalışıyor", "nötr"),
]


class NaiveBayesClassifier:
    def __init__(self):
        self.kategori_sayilari = defaultdict(int)          # her kategoriden kaç örnek var
        self.kelime_sayilari = defaultdict(lambda: defaultdict(int))  # kategori -> kelime -> sayı
        self.toplam_kelime = defaultdict(int)               # kategori -> toplam kelime sayısı
        self.kelime_dagarcigi = set()                       # görülen tüm kelimeler
    
    def _tokenize(self, metin):
        return metin.lower().split()
    
    def train(self, egitim_verisi):
        for metin, kategori in egitim_verisi:
            self.kategori_sayilari[kategori] += 1
            for kelime in self._tokenize(metin):
                self.kelime_sayilari[kategori][kelime] += 1
                self.toplam_kelime[kategori] += 1
                self.kelime_dagarcigi.add(kelime)
    
    def predict(self, metin):
        kelimeler = self._tokenize(metin)
        toplam_ornek = sum(self.kategori_sayilari.values())
        
        if toplam_ornek == 0:
            return "bilinmiyor", 0.0
        
        en_iyi_kategori = None
        en_iyi_skor = float("-inf")
        
        for kategori in self.kategori_sayilari:
            # Önsel olasılık (prior): bu kategori genel olarak ne kadar yaygın
            log_olasilik = math.log(self.kategori_sayilari[kategori] / toplam_ornek)
            
            kelime_dagarcigi_buyuklugu = len(self.kelime_dagarcigi)
            
            for kelime in kelimeler:
                # Laplace smoothing (hiç görülmemiş kelimeler için sıfır olasılık sorununu önler)
                kelime_sayisi = self.kelime_sayilari[kategori].get(kelime, 0)
                olasilik = (kelime_sayisi + 1) / (self.toplam_kelime[kategori] + kelime_dagarcigi_buyuklugu)
                log_olasilik += math.log(olasilik)
            
            if log_olasilik > en_iyi_skor:
                en_iyi_skor = log_olasilik
                en_iyi_kategori = kategori
        
        return en_iyi_kategori, en_iyi_skor
    
    def to_dict(self):
        return {
            "kategori_sayilari": dict(self.kategori_sayilari),
            "kelime_sayilari": {k: dict(v) for k, v in self.kelime_sayilari.items()},
            "toplam_kelime": dict(self.toplam_kelime),
            "kelime_dagarcigi": list(self.kelime_dagarcigi),
        }
    
    @classmethod
    def from_dict(cls, veri):
        model = cls()
        model.kategori_sayilari = defaultdict(int, veri["kategori_sayilari"])
        model.kelime_sayilari = defaultdict(lambda: defaultdict(int))
        for kategori, kelimeler in veri["kelime_sayilari"].items():
            model.kelime_sayilari[kategori] = defaultdict(int, kelimeler)
        model.toplam_kelime = defaultdict(int, veri["toplam_kelime"])
        model.kelime_dagarcigi = set(veri["kelime_dagarcigi"])
        return model


_model = None  # bellekte tek bir model tutulur (lazy-loaded)


def _get_model():
    global _model
    if _model is not None:
        return _model
    
    if os.path.exists(MODEL_FILE):
        try:
            with open(MODEL_FILE, "r", encoding="utf-8") as f:
                veri = json.load(f)
            _model = NaiveBayesClassifier.from_dict(veri)
            return _model
        except Exception:
            pass
    
    # Model dosyası yoksa veya bozuksa, varsayılan veriyle yeniden eğit
    _model = NaiveBayesClassifier()
    _model.train(_VARSAYILAN_EGITIM_VERISI)
    _save_model(_model)
    return _model


def _save_model(model):
    os.makedirs(os.path.dirname(MODEL_FILE), exist_ok=True)
    try:
        with open(MODEL_FILE, "w", encoding="utf-8") as f:
            json.dump(model.to_dict(), f, indent=2, ensure_ascii=False)
    except Exception as error:
        print(f"[UYARI] Model kaydedilemedi: {error}")


def learn_new_example(metin, kategori):
    """Kullanıcının kendi örneğini modele ekler (gerçek zamanlı öğrenme)."""
    model = _get_model()
    model.train([(metin, kategori)])
    _save_model(model)


def run_ai_command(parcalar):
    """
    Ana döngüden çağrılacak giriş noktası.
    parcalar: ['ai', 'mesaj', 'kelimeleri', '-run'] şeklinde gelir.
    """
    if len(parcalar) < 3 or parcalar[-1] != "-run":
        print("Kullanım: ai <mesaj> -run")
        return
    
    mesaj = " ".join(parcalar[1:-1])
    
    if not mesaj:
        print("Kullanım: ai <mesaj> -run")
        return
    
    model = _get_model()
    kategori, skor = model.predict(mesaj)
    
    print(f"[AstraAI] Tahmin: '{mesaj}' --> {kategori}")
    print(f"(Bu bir Naive Bayes makine öğrenmesi tahminidir, kesin doğruluk garantisi yoktur.)")
