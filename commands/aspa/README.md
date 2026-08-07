# ASPA (Astra Sage Package App)

ASPA (Astra Sage Package App), AstraSage için geliştirilmiş resmi uygulama paket formatıdır.

ASPA sayesinde AstraSage içerisine yeni uygulamalar güvenli bir şekilde kurulabilir, çalıştırılabilir ve yönetilebilir.

---

## Özellikler

- 📦 Tek dosyada uygulama dağıtımı (.aspa)
- 🔒 AstraSecurity ile güvenlik taraması
- ⚡ Hızlı kurulum
- ▶️ run() tabanlı AstraSage çalışma sistemi
- 📄 Manifest desteği
- 📚 README desteği
- 🗑️ Güvenli kaldırma sistemi

---

## Dosya Yapısı

Bir ASPA dosyası aslında ZIP tabanlı bir arşivdir.

Örnek:

```
MyApp.aspa
│
├── manifest.json
├── main.py
└── README.md
```

---

## manifest.json

Her ASPA uygulamasında bulunmalıdır.

Örnek:

```json
{
    "name": "MyApp",
    "version": "1.0.0",
    "author": "EnderAstra",
    "description": "İlk ASPA uygulamam",
    "entry": "main.py"
}
```

---

## main.py

Giriş dosyasıdır.

ASPA uygulamaları **main()** yerine **run()** fonksiyonunu kullanır.

Örnek:

```python
def run():
    print("Merhaba AstraSage!")
```

---

## Kurulum

Önce ASPA sistemini kurun.

```
aspi install aspa
```

Ardından uygulamayı kurun.

```
aspa install MyApp MyApp.aspa
```

---

## Çalıştırma

```
aspa run MyApp
```

---

## Uygulama Bilgisi

```
aspa info MyApp
```

---

## Kurulu Uygulamaları Listeleme

```
aspa list
```

---

## Uygulama Kaldırma

```
aspa remove MyApp
```

---

## Güvenlik

Kurulumdan önce tüm ASPA paketleri AstraSecurity tarafından taranır.

Güvenlik kontrolünü geçemeyen uygulamalar kurulmaz.

---

## Gereksinimler

- AstraSage
- ASPA Motoru
- Python 3

---

## Lisans

Bu proje AstraSage ekosisteminin resmi uygulama paket formatıdır.

Developed with ❤️ by EnderAstra.