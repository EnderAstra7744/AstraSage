#AstraSage Kütüphanesi
#İsim: temiz_test
#Açıklama: AstraSecurity testi için temiz kütüphane

import random
import datetime

def run():
    print("Temiz Test Kütüphanesi Çalışıyor!")
    print(f"Rastgele sayı: {random.randint(1, 100)}")
    print(f"Tarih: {datetime.datetime.now().strftime('%d/%m/%Y')}")

KUTUPHANE_ADI = "temiz_test"
KUTUPHANE_SURUMU = "1.0"
KUTUPHANE_ACIKLAMA = "AstraSecurity testi için temiz kütüphane"
