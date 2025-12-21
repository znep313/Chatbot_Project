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

## Kurulum

### Gereksinimler

- Python 3.10 veya üzeri
- Google AI API Key
- Tavily API Key (opsiyonel, web araması için)

### Adım 1: Projeyi İndirin

```bash
git clone https://github.com/kullanici/alerji-chatbot.git
cd alerji-chatbot
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

```env
GOOGLE_API_KEY=your_google_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

> **API Anahtarı Alma:**
> - Google AI: [Google AI Studio](https://aistudio.google.com/apikey)
> - Tavily: [Tavily Dashboard](https://tavily.com/)

### Adım 5: Veritabanını Oluşturun

```bash
python ingestion.py
```

### Adım 6: Uygulamayı Başlatın

```bash
streamlit run app.py
```

Tarayıcınızda `http://localhost:8501` adresine gidin.

---

## Proje Yapısı

```
📁 alerji-chatbot/
│
├── 📁 app/                      # Uygulama modülleri
│   ├── __init__.py              # Paket tanımı (v2.0.0)
│   ├── config.py                # Merkezi konfigürasyon ayarları
│   └── utils.py                 # Yardımcı fonksiyonlar
│
├── 📁 data/                     # Veri dosyaları
│   ├── alerji.csv               # Çapraz reaksiyon veritabanı
│   └── *.pdf                    # Akademik makaleler
│
├── 📁 models/                   # Model yönetimi
│   ├── __init__.py              # Model exports
│   └── llm.py                   # LLM ve embedding konfigürasyonu
│
├── 📁 scripts/                  # Yardımcı scriptler
│   └── __init__.py
│
├── 📁 chroma_db/                # Vektör veritabanı (otomatik oluşur)
│
├── 📄 app.py                    # Ana Streamlit uygulaması
├── 📄 main.py                   # Terminal tabanlı chatbot
├── 📄 ingestion.py              # Veri yükleme ve işleme scripti
├── 📄 keywords.txt              # Anahtar kelime listesi
├── 📄 requirements.txt          # Python bağımlılıkları
├── 📄 .gitignore                # Git ignore kuralları
├── 📄 .env                      # API anahtarları (gizli)
└── 📄 README.md                 # Bu dosya
```

### Modül Açıklamaları

| Modül | Dosya | Açıklama |
|-------|-------|----------|
| **app** | `config.py` | API anahtarları, model ayarları, RAG parametreleri |
| **app** | `utils.py` | `get_text_content()`, `load_keywords()`, `calculate_source_ratio()` |
| **models** | `llm.py` | `get_models()`, `get_embeddings()`, `get_llm()`, `get_tavily()` |
| **root** | `app.py` | Streamlit web arayüzü |
| **root** | `main.py` | Terminal chatbot |
| **root** | `ingestion.py` | PDF, CSV ve web verilerini ChromaDB'ye yazar |

---

## Kullanım

### Web Arayüzü (Streamlit)

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

### Merkezi Konfigürasyon (app/config.py)

```python
# Model Ayarları
LLM_MODEL = "gemini-2.5-flash"
LLM_TEMPERATURE = 0.1
EMBEDDING_MODEL = "models/text-embedding-004"

# RAG Ayarları
SIMILARITY_SEARCH_K = 3
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

# Dosya Ayarları
MAX_FILE_SIZE_MB = 50
```

### Anahtar Kelimeler (keywords.txt)

```txt
# Yorum satırları # ile başlar
alerji
alerjen
astım
anafilaksi
# Yeni kelime eklemek için satır ekleyin
```

### Web Kaynakları (app/config.py)

```python
URL_LIST = [
    "https://www.aid.org.tr/",
    "https://alerjiastim.org.tr/",
    # Daha fazla ekleyin...
]
```

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

---

## Sorun Giderme

### "API Key bulunamadı" hatası
`.env` dosyasının proje dizininde olduğundan emin olun.

### PDF okuma hataları
Bazı PDF'ler bozuk olabilir. `ingestion.py` hatalı dosyaları atlayıp devam eder.

### Çok büyük PDF'ler
50 MB üzeri dosyalar otomatik atlanır. Limiti değiştirmek için `app/config.py` içindeki `MAX_FILE_SIZE_MB` değerini güncelleyin.

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

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

---

## İletişim

Sorularınız için issue açabilir veya pull request gönderebilirsiniz.

---

<div align="center">

**⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın! ⭐**

Made with ❤️ using Python, Streamlit & LangChain

*Powered by Google Gemini AI 🚀*

</div>
