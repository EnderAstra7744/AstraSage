#AstraSage Kütüphanesi
#İsim: tehlikeli_test
#Açıklama: AstraSecurity testi için tehlikeli kütüphane (TEST AMAÇLI)

import os
import subprocess

def run():
    print("Bu kütüphane çalışmamalı!")
    os.system("echo tehlikeli komut")
    subprocess.run(["ls"])

KUTUPHANE_ADI = "tehlikeli_test"
KUTUPHANE_SURUMU = "1.0"
KUTUPHANE_ACIKLAMA = "AstraSecurity testi - tehlikeli kod içerir"
