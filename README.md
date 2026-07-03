# WiFiBruteForcer

Terminal üzerinden çalışan, Python ile geliştirilmiş bir Wi-Fi parola deneme aracıdır. Program, belirtilen bir SSID için bir parola listesindeki (wordlist) şifreleri sırayla deneyerek bağlantı kurulup kurulamadığını kontrol eder.

> **Not:** Bu proje eğitim, laboratuvar ortamı ve yalnızca sahibi olduğunuz veya test etme yetkinizin bulunduğu kablosuz ağlar üzerinde kullanılmak üzere geliştirilmiştir.

---

## Özellikler

* Modern terminal arayüzü
* Gerçek zamanlı ilerleme tablosu
* Denenen parola sayısı
* Kalan tahmini süre
* Deneme hızı (şifre/sn)
* Başarılı bağlantıda otomatik durma
* UTF-8 uyumlu wordlist desteği
* Basit ve anlaşılır kod yapısı

---

## Ekran Görüntüsü

```text
[>] SSID: MyWiFi
[>] WORDLIST: rockyou.txt

Toplam 14344392 şifre yüklendi.

Şu an denenen parola:
password123

İlerleme:
██████░░░░░░░░░░░░ 31.2%

Süre: 28.4s
Hız: 3.6/sn
Kalan: ~1523s
```

---

## Gereksinimler

* Python 3.10+
* Windows işletim sistemi (önerilir)
* Kablosuz ağ adaptörü
* Python paketleri:

```bash
pip install pywifi rich colorama
```

---

## Kurulum

Depoyu klonlayın:

```bash
git clone https://github.com/sychoticdox/WiFi-BruteForce.git
```

Klasöre girin:

```bash
cd WiFi-BruteForce
```

Bağımlılıkları yükleyin:

```bash
pip install -r requirements.txt
```

---

## Kullanım

Programı çalıştırın:

```bash
python wifibf.py
```

Ardından sizden aşağıdaki bilgiler istenir:

```text
[>] SSID ismini girin:
[>] Wordlist dosya yolu:
```

Örnek:

```text
SSID:
EvWiFi

Wordlist:
rockyou.txt
```

---

## Nasıl Çalışır?

Program aşağıdaki işlemleri gerçekleştirir:

1. Kablosuz ağ arayüzünü algılar.
2. Belirtilen SSID için bağlantı profili oluşturur.
3. Wordlist dosyasındaki parolaları sırayla okur.
4. Her parola ile bağlantı kurmayı dener.
5. Bağlantı başarılı olursa işlemi sonlandırır.
6. Başarısız olursa sıradaki parolaya geçer.

Program herhangi bir kablosuz ağ güvenlik açığından yararlanmaz; yalnızca verilen parolaları tek tek deneyerek bağlantı kurmayı test eder.

---

## Proje Yapısı

```text
WiFiBruteForcer/
│
├── wifibf.py
├── requirements.txt
├── README.md
└── wordlist.txt
```

---

## Kullanılan Kütüphaneler

* pywifi
* rich
* colorama
* time
* sys

---

## Sınırlamalar

* WPA/WPA2 kişisel ağlar için parola denemesi yapar.
* Deneme hızı kablosuz adaptöre ve işletim sistemine bağlıdır.
* Büyük wordlist dosyalarında işlem süresi uzun olabilir.
* Aynı anda yalnızca tek bir hedef ağ üzerinde çalışır.

---

## Sorumluluk Reddi

Bu yazılım yalnızca eğitim, araştırma ve yetkili güvenlik testleri amacıyla hazırlanmıştır.

Yazılımın izinsiz veya hukuka aykırı biçimde kullanılmasından doğabilecek hiçbir sorumluluk geliştiriciye ait değildir. Programı kullanmadan önce hedef ağ üzerinde gerekli izinlere sahip olduğunuzdan emin olun.

---

## Bana Ulaş

**H04x LLC**

Telegram: `t.me/sychoticdox`

---

## Lisans

Bu proje MIT Lisansı kapsamında dağıtılmaktadır.

İstediğiniz gibi değiştirebilir, geliştirebilir ve katkıda bulunabilirsiniz.
