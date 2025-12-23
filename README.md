# 🧬 Akıllı Alerji & Sağlık Asistanı

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Google AI](https://img.shields.io/badge/Gemini_AI-4285F4?style=for-the-badge&logo=google&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-121212?style=for-the-badge)
![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6F00?style=for-the-badge)

**Yapay Zeka Destekli Alerji Uzman Chatbot**

*PDF Analizi • Canlı Web Araması • Çapraz Reaksiyon Veritabanı • RAG Sistemi*

[Kurulum](#kurulum) • [Kullanım](#kullanım) • [Proje Yapısı](#proje-yapısı) • [Özellikler](#özellikler)

</div>

---

## Özellikler

### 🤖 Akıllı Sohbet
- **Gemini 2.5 Flash** modeli ile doğal dil işleme
- Türkçe ve İngilizce kaynak desteği
- Bağlam farkındalığı ile tutarlı yanıtlar
- Sohbet geçmişi hafızası



### 📄 RAG (Retrieval-Augmented Generation)
- ChromaDB vektör veritabanı
- Akademik makaleleri ve raporları otomatik işleme
- Similarity search ile ilgili belgeleri bulma
- Kaynak güvenilirlik skoru

### 🌐 Canlı Web Araması
- **Tavily API** ile güncel tıbbi bilgilere erişim
- Gerçek zamanlı kaynak doğrulama

### 📊 Çapraz Reaksiyon Veritabanı
- CSV/Excel dosyalarından alerjen verisi yükleme
- Besin-alerjen ilişki haritası
- Risk seviyesi analizi

### 💾 Sohbet Yönetimi
- TXT ve JSON formatında dışa aktarma
- Sohbet geçmişi saklama
- Modern ve şık UI tasarımı

---

## Teknolojiler

| Kategori | Teknoloji |
|----------|-----------|
| **Backend** | Python 3.10+ |
| **Frontend** | Streamlit |
| **LLM** | Google Gemini 2.5 Flash |
| **Embeddings** | Google Text Embedding 004 |
| **Vektör DB** | ChromaDB |
| **Framework** | LangChain |
| **Web Arama** | Tavily API |
| **PDF İşleme** | PyPDF |

---

## 🚀 Hızlı Başlangıç

```bash
# 1. Projeyi klonlayın
git clone https://github.com/znep313/Chatbot_Project.git
cd Chatbot_Project

# 2. Sanal ortam oluşturun ve aktif edin
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# 3. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 4. .env dosyası oluşturun
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux
# .env dosyasını düzenleyip API anahtarlarınızı girin

# 5. Veritabanını oluşturun
python ingestion.py

# 6. Uygulamayı başlatın
streamlit run app.py
```

---

## Kurulum

### Gereksinimler

- Python 3.10 veya üzeri
- Google AI API Key
- Tavily API Key (opsiyonel, web araması için)

### Adım 1: Projeyi İndirin

```bash
git clone https://github.com/znep313/Chatbot_Project.git
cd Chatbot_Project
```

### Adım 2: Sanal Ortam Oluşturun

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Adım 3: Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### Adım 4: API Anahtarlarını Ayarlayın

Proje dizininde `.env` dosyası oluşturun:

**Yöntem 1:** `.env.example` dosyasını kopyalayın:
```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

**Yöntem 2:** Manuel olarak `.env` dosyası oluşturun:
```env
GOOGLE_API_KEY=your_google_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

> **API Anahtarı Alma:**
> - **Google AI** (Zorunlu): [Google AI Studio](https://aistudio.google.com/apikey) - Ücretsiz
> - **Tavily** (Opsiyonel): [Tavily Dashboard](https://tavily.com/) - Web araması için

### Adım 5: Veritabanını Oluşturun

**Önemli:** `data/` klasörüne PDF, CSV veya Excel dosyalarınızı ekleyin (opsiyonel).

```bash
python ingestion.py
```

Bu script:
- `data/` klasöründeki PDF dosyalarını yükler
- CSV/Excel dosyalarını işler
- Web sitelerini tarar (ingestion.py içindeki URL_LIST'ten)
- Tüm verileri ChromaDB'ye yazar

**Not:** Eğer `data/` klasörü boşsa, sadece web siteleri taranır.

### Adım 6: Uygulamayı Başlatın

```bash
streamlit run app.py
```

Tarayıcınızda `http://localhost:8501` adresine gidin.

---

## Proje Yapısı

```
📁 Chatbot Project/
│
├── 📁 data/                     # Veri dosyaları
│   ├── alerji.csv               # Çapraz reaksiyon veritabanı
│   └── *.pdf                    # Akademik makaleler (PDF dosyaları)
│
├── 📁 chroma_db/                # Vektör veritabanı (otomatik oluşur)
│
├── 📄 app.py                    # Ana Streamlit web arayüzü
├── 📄 main.py                   # Terminal tabanlı chatbot
├── 📄 ingestion.py              # Veri yükleme ve işleme scripti
├── 📄 keywords.txt              # Anahtar kelime listesi (filtreleme için)
├── 📄 requirements.txt          # Python bağımlılıkları
├── 📄 .gitignore                # Git ignore kuralları
├── 📄 .env.example              # .env dosyası örneği (kopyalayıp .env yapın)
├── 📄 .env                      # API anahtarları (gizli - oluşturmanız gerekir)
└── 📄 README.md                 # Bu dosya
```

### Dosya Açıklamaları

| Dosya | Açıklama |
|-------|----------|
| `app.py` | Streamlit web arayüzü - Modern UI, dosya yükleme, sohbet, kaynak analizi |
| `main.py` | Terminal tabanlı chatbot - Komut satırından kullanım |
| `ingestion.py` | Veri yükleme scripti - PDF, CSV, Excel ve web sitelerini ChromaDB'ye yükler |
| `keywords.txt` | Anahtar kelime listesi - Chatbot'un hangi konularda yanıt vereceğini belirler |
| `requirements.txt` | Python paket bağımlılıkları |
| `.env` | API anahtarları (GOOGLE_API_KEY, TAVILY_API_KEY) |

---

## Kullanım

### Web Arayüzü (Streamlit)
<img width="1912" height="853" alt="Ekran görüntüsü 2025-12-22 145002" src="https://github.com/user-attachments/assets/f272fb1c-13d4-42cd-a05d-72af48c26ac2" />
<img width="1910" height="845" alt="Ekran görüntüsü 2025-12-23 195655" src="https://github.com/user-attachments/assets/d588474e-efc1-46b5-ab52-82fe48967aec" />
<img width="1382" height="470" alt="Ekran görüntüsü 2025-12-23 195720" src="https://github.com/user-attachments/assets/57d7eba5-cfed-4c5d-936a-4b7cabeae550" />
<img width="308" height="855" alt="Ekran görüntüsü 2025-12-23 195745" src="https://github.com/user-attachments/assets/bfbcd5b5-799f-4fea-a992-2805a1e4176f" />


```bash
streamlit run app.py
```

**Özellikler:**
- 💬 Sohbet arayüzü ile soru sorma
- 📤 Sidebar'dan dosya yükleme (PDF, CSV, Excel)
- 📚 Yüklenen dosyaları görüntüleme
- 💾 Sohbeti TXT/JSON olarak indirme
- 📊 Kaynak analizi ve güven skoru

### Terminal Arayüzü

```bash
python main.py
```

### Veri Yükleme

```bash
python ingestion.py
```

**Çıktı Örneği:**
```
============================================================
🧬 ALERJİ CHATBOT - VERİ YÜKLEME SİSTEMİ
============================================================

📂 PDF Dosyaları Yükleniyor...
  ✅ Allergy - 2002 - Aalberse.pdf (12 sayfa)
  ✅ Structural biology of allergens.pdf (8 sayfa)
  ⏭️  janeways-immunobiology.pdf (85.2 MB) - Çok büyük, atlanıyor...

📊 CSV/Excel Dosyaları Yükleniyor...
  ✅ alerji.csv (9 satır)

🌐 Web Siteleri Taranıyor...
  ✅ www.aid.org.tr/hastaliklar/alerji...

============================================================
📊 YÜKLEME RAPORU
  📄 PDF: 5 dosya (45 sayfa)
  📊 CSV: 1 dosya
  🌐 Web: 4 site
  📦 Toplam: 156 metin parçası
============================================================
✅ İŞLEM TAMAMLANDI!
```

---

## Yapılandırma

### Anahtar Kelimeler (keywords.txt)

Chatbot'un hangi konularda yanıt vereceğini belirler. Yeni kelimeler eklemek için dosyayı düzenleyin:

```txt
# Yorum satırları # ile başlar
alerji
alerjen
astım
anafilaksi
kaşıntı
besin
polen
# Yeni kelime eklemek için satır ekleyin
```

### Web Kaynakları (ingestion.py)

Web sitelerini taramak için `ingestion.py` dosyasındaki `URL_LIST` değişkenini düzenleyin:

```python
URL_LIST = [
    "https://www.aid.org.tr/hastaliklar/alerji-ve-bagisiklik-sistemi-hastaliklari/gida-alerjisi/",
    "https://istanbulalerjimerkezi.com.tr/alerji-nedir-belirtileri-nelerdir/",
    "https://www.aid.org.tr/",
    "https://alerjiastim.org.tr/"
]
```

### Model Ayarları

Model ayarları kod içinde tanımlıdır:
- **LLM Model**: `gemini-2.5-flash`
- **Temperature**: `0.1`
- **Embedding Model**: `models/text-embedding-004`
- **Chunk Size**: `1000` karakter
- **Chunk Overlap**: `100` karakter
- **Max File Size**: `50 MB`

---

## Bağımlılıklar

`requirements.txt` dosyasındaki ana kütüphaneler:

```
streamlit>=1.28.0
langchain>=0.1.0
langchain-google-genai>=1.0.0
langchain-chroma>=0.1.0
chromadb>=0.4.0
pypdf>=3.0.0
tavily-python>=0.3.0
python-dotenv==1.0.0
pandas>=2.0.0
```

Kurulum:
```bash
pip install -r requirements.txt
```

---

## Güvenlik

- ⚠️ `.env` dosyasını **asla** Git'e eklemeyin
- `.gitignore` dosyası aşağıdakileri hariç tutar:
  - `.env` - API anahtarları
  - `.venv/` - Sanal ortam
  - `chroma_db/` - Vektör veritabanı
  - `__pycache__/` - Python cache
  - `*.log` - Log dosyaları

---

## Sorun Giderme

### "API Key bulunamadı" hatası
`.env` dosyasının proje dizininde olduğundan emin olun.

### PDF okuma hataları
Bazı PDF'ler bozuk olabilir. `ingestion.py` hatalı dosyaları atlayıp devam eder.

### Çok büyük PDF'ler
50 MB üzeri dosyalar otomatik atlanır. Limiti değiştirmek için `ingestion.py` dosyasındaki `MAX_FILE_SIZE_MB = 50` değerini güncelleyin.

### Web araması çalışmıyor
Tavily API anahtarınızı kontrol edin veya internet bağlantınızı test edin.

### Import hataları
```bash
pip install -r requirements.txt --upgrade
```

---

## Katkıda Bulunma

1. Bu repoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/yeni-ozellik`)
5. Pull Request açın


---

## İletişim

Sorularınız için issue açabilir veya pull request gönderebilirsiniz.

---

<div align="center">

**⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın! ⭐**

Made with ❤️ using Python, Streamlit & LangChain

*Powered by Google Gemini AI 🚀*

</div>
