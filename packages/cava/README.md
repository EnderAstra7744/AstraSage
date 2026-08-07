# 🎤 Ses ile Hareket Eden Yeşil Çubuklar

Mikrofonunuzdan gelen sese gerçek zamanlı tepki veren, yeşil renkli dikey çubuklardan oluşan bir ses görselleştirici (audio visualizer).

## 📁 Dosyalar

| Dosya | Açıklama |
|---|---|
| `ses_gorsellestirici.py` | Masaüstü (Linux/Windows/Mac) için Python + Pygame versiyonu |
| `ses_gorsellestirici.html` | Tarayıcı/mobil için HTML + JavaScript versiyonu |
| `baslat.py` | HTML dosyasını yerel sunucu üzerinden otomatik tarayıcıda açan Python scripti |

## 🖥️ Masaüstünde Çalıştırma (Python)

Gerekli kütüphaneleri kurun:

```bash
pip install pygame sounddevice numpy
```

Linux'ta ses erişimi için PortAudio gerekebilir:

```bash
sudo apt-get install portaudio19-dev python3-pyaudio
```

Ardından çalıştırın:

```bash
python3 ses_gorsellestirici.py
```

Çıkmak için pencereyi kapatın veya **ESC** tuşuna basın.

## 📱 Mobilde / Tarayıcıda Çalıştırma (HTML)

Masaüstünde `.html` dosyasını doğrudan çift tıklayarak da açabilirsiniz, ancak mikrofon izinlerinin sorunsuz çalışması için yerel bir sunucu üzerinden açmanız önerilir:

```bash
python3 baslat.py
```

Bu script:
1. `ses_gorsellestirici.html` dosyasını yerel bir sunucuda (`http://localhost`) yayınlar
2. Varsayılan tarayıcınızı otomatik olarak açar

Telefonda kullanmak isterseniz, `ses_gorsellestirici.html` dosyasını telefonunuza aktarıp tarayıcıda (Chrome/Safari) açmanız yeterli — "Başlat" butonuna basınca mikrofon izni istenir.

> ⚠️ **Not:** `baslat.py` ve `ses_gorsellestirici.html` dosyalarının **aynı klasörde** olması gerekir.

## ⚙️ Ayarlar

Her iki versiyonda da dosyanın başında değiştirebileceğiniz ayarlar bulunur:

- **Çubuk sayısı** (`NUM_BARS`): Ekrandaki dikey çubuk adedi
- **Yumuşatma** (`SMOOTHING`): Çubukların ne kadar akıcı/yavaş hareket edeceği (0-1 arası)
- **Renkler**: Çubukların soluk ve parlak yeşil tonları

## 🔊 Nasıl Çalışır?

1. Mikrofondan ham ses verisi alınır
2. **FFT (Fourier Dönüşümü)** ile ses, frekans bantlarına ayrılır
3. Frekans bantları logaritmik ölçekte gruplanarak çubuklara dağıtılır (bas sesler solda, tiz sesler sağda)
4. Her bandın ses şiddeti, ilgili çubuğun yüksekliğine ve rengin parlaklığına yansıtılır
5. Ani sıçramaları azaltmak için yükseklikler kare kare yumuşatılır (smoothing)

## 🐧 Gereksinimler

- **Python versiyonu:** `ses_gorsellestirici.py` ve `baslat.py` için Python 3.7+
- **Tarayıcı versiyonu:** Mikrofon (getUserMedia) destekleyen güncel bir tarayıcı (Chrome, Safari, Firefox, Edge)
