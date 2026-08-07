# aspi - AstraSage Package Installer

AstraSage için paket yöneticisi.

## Kullanım

aspi <paket> -export <link>   → indirir ve kurar
aspi <paket> -install         → assets/pc/ içinden kurar  
aspi <paket> -remove          → paketi kaldırır (.pc kalır)
aspi <paket> -unexport        → paketi ve .pc dosyasını siler
aspi list                     → kurulu paketleri listeler

## Paket Formatı (.pc)

Her .pc dosyası bir ZIP arşividir. İçinde:
- main.py (paketin ana kodu)
- README.md (açıklama)
- setup.py (isteğe bağlı, kurulum scripti)
