# oneko

AstraSage icin GUI'siz, terminal tabanli kedi animasyonu. Klasik "oneko"
(fare imlecini kovalayan masaustu kedisi) fikrinden esinlenilmistir, ama
terminalde gercek bir fare imleci olmadigi icin kedi bunun yerine kendi
basina dolasir.

## Kurulum

Bu paket `packages/oneko/main.py` olarak AstraSage'e yerlestirilir.
Ekstra bir kurulum adimi gerekmez -- `load_dynamic_commands()` zaten
`packages/` klasorunu tarar, dosya orada durdugu surece komut olarak
taninir.

## Kullanim

```
oneko
```

yazinca kedi ekranda belirir ve kendi kendine dolasmaya baslar.

Ekranin altinda sabit bir satir bulunur:

```
Cikmak icin bos birakip Enter'a bas | Mama vermek icin 'mama' yaz + Enter:
```

- **Bos birakip Enter'a basmak** -> oneko'dan cikar, AstraSage'e doner.
- **"mama" yazip Enter'a basmak** -> kediye mama animasyonu oynatilir
  (birkac kare boyunca yer, sonra tekrar dolasmaya devam eder).

## Davranislar

Kedi asagidaki durumlar arasinda kendi kendine gecis yapar:

| Durum   | Aciklama                                              |
|---------|--------------------------------------------------------|
| Yurume  | Rastgele bir yonde (sag/sol/yukari/asagi) birkac adim yurur, duvara carpinca yon degistirir. |
| Oturma  | Durur, kuyrugunu sallar (iki kareli animasyon).         |
| Uyku    | Oturduktan sonra bazen (yaklasik %35 ihtimalle) uyur, "zZ" animasyonu oynatilir. |
| Mama    | "mama" komutuyla tetiklenir, birkac kare boyunca yer.   |

Her durumun kendine ait, yone gore degisen ASCII sprite'lari vardir.

## Teknik notlar

- **Arka plan input:** `input()` normalde programi durdurur. Animasyonun
  akmaya devam etmesi icin kullanici girdisi ayri bir thread'de okunur;
  ana dongu her karede bu thread'in kuyrugunu bloklamadan kontrol eder.
- **Ekran cizimi:** Kedi, ANSI imlec adresleme (`\033[satir;sutunH`) ile
  belirli bir bolgeye cizilir; her karede sadece o bolge temizlenip
  yeniden cizilir, tum ekran silinmez -- boylece alttaki input satiri
  korunur.
- **Terminal uyumlulugu:** Bu teknik gercek bir tty saglayan terminallerde
  guvenilir calisir. Pydroid3 gibi bazi ortamlarda konsol gercek bir tty
  gibi davranmayabilir; boyle durumlarda input satirinin yeri kaymasi
  veya ekran ciziminde kucuk kaymalar gorulebilir.

## Cikis

Ctrl+C ile de kapatilabilir (bekleme mekanizmasi olarak `finally` bloğu
ekrani temizler ve "oneko durduruldu." mesaji basar).
