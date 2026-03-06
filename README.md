Reisim o telaşın arasında haklısın kaynadı gitti yukarıda! Hemen o efsane bot için hazırladığım README şablonunu tekrar bırakıyorum buraya.

Bunu kopyalayıp proje klasörünün içine README.md adında bir dosya oluşturarak yapıştırman yeterli:

Markdown
# 🗺️ KMT Dijital - Maps Scraper Pro (v4.0 Final)

Bu proje, dijital ajanslar ve B2B satış yapan işletmeler için Google Haritalar (Google Maps) üzerinden otomatik olarak potansiyel müşteri (Lead) verilerini toplayan, masaüstü arayüzüne (GUI) sahip gelişmiş bir Python veri kazıma (web scraping) botudur.

## 🚀 Projenin Amacı
İşletmelerin hedefledikleri sektör ve lokasyondaki firmaların iletişim bilgilerine saniyeler içinde ulaşmasını sağlamak. Manuel arama zahmetini ortadan kaldırarak, toplanan verileri doğrudan Excel formatında dışa aktarır ve pazarlama/satış hunisine (pipeline) aktarılmaya hazır hale getirir.

## 💎 Temel Özellikler

* **Kullanıcı Dostu Arayüz (GUI):** Tkinter ile tasarlanmış, kodlama bilmeden kullanılabilen basit ve modern kontrol paneli.
* **Akıllı Filtreleme:** Sadece belirli numara formatlarını (Örn: `05` ile başlayan cep telefonları) filtreleyebilme özelliği.
* **Dahili Tarayıcı Kurulumu:** İlk kullanımda gereken Playwright Chromium tarayıcılarını menü üzerinden tek tıkla otomatik indirme ve kurma altyapısı.
* **Canlı Log Ekranı:** Arka planda çalışan scraping işlemlerini, aranan firmaları ve hataları anlık olarak takip edebilme.
* **Tek Tıkla Excel'e Aktarım:** Toplanan verileri (İşletme Adı, Telefon, Puan, Bölge) doğrudan `.xlsx` formatında raporlama (`pandas` entegrasyonu).
* **Anti-Blokaj Yapısı:** Gerçek kullanıcı deneyimini simüle eden bekleme süreleri (sleep) ve DOM kaydırma algoritmaları.

## 🛠️ Kullanılan Teknolojiler

* **Dil:** Python 3
* **Arayüz (GUI):** Tkinter
* **Veri Kazıma (Scraping):** Playwright (Senkron API)
* **Veri İşleme:** Pandas, Openpyxl
* **Eşzamanlılık:** Threading (Arayüzün donmasını engellemek için)

## ⚙️ Kurulum ve Kullanım

### Geliştirici Ortamı İçin Kurulum
1. Projeyi bilgisayarınıza klonlayın:
   ```bash
   git clone [https://github.com/Tiftik37/i-letme-bilgisi-ekme-uygulamas-.git](https://github.com/Tiftik37/i-letme-bilgisi-ekme-uygulamas-.git)
Gerekli kütüphaneleri yükleyin:

Bash
pip install playwright pandas openpyxl
Scripti çalıştırın:

Bash
python main.py
Uygulama açıldığında üst menüden "⚙️ Kurulum & Ayarlar" -> "Gerekli Tarayıcıları Yükle" seçeneğine tıklayarak Playwright tarayıcılarını sisteme entegre edin.

Sektör, Şehir, Hedef Sayı ve Filtre bilgilerini girip "BAŞLAT" butonuna basın.

⚠️ Yasal Uyarı
Bu yazılım yalnızca eğitim ve araştırma amacıyla geliştirilmiştir. Veri kazıma (scraping) işlemleri platformların hizmet şartlarına (TOS) tabi olabilir. Yazılımın kullanımından doğabilecek her türlü sorumluluk son kullanıcıya aittir.

Geliştirici: Kaan Tiftik
