import os
import sys
import warnings
import pandas as pd
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_core.documents import Document

# Uyarıları bastır
warnings.filterwarnings("ignore")

load_dotenv()

# --- AYARLAR ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DATA_FOLDER = "./data"
MAX_FILE_SIZE_MB = 50  # 50 MB'dan büyük dosyaları atla

# Öğretmek istediğin web sitelerinin linklerini buraya ekle:
URL_LIST = [
    "https://www.aid.org.tr/hastaliklar/alerji-ve-bagisiklik-sistemi-hastaliklari/gida-alerjisi/",
    "https://istanbulalerjimerkezi.com.tr/alerji-nedir-belirtileri-nelerdir/",
    "https://www.aid.org.tr/",
    "https://alerjiastim.org.tr/"
]

if not GOOGLE_API_KEY:
    print("❌ HATA: .env dosyasında API Key bulunamadı!")
    sys.exit(1)

# --- İSTATİSTİKLER ---
stats = {
    "pdf_success": 0,
    "pdf_failed": 0,
    "pdf_skipped": 0,
    "csv_success": 0,
    "web_success": 0,
    "total_pages": 0
}
failed_files = []
skipped_files = []

# --- YARDIMCI FONKSİYONLAR ---
def get_file_size_mb(file_path):
    """Dosya boyutunu MB olarak döndürür."""
    return os.path.getsize(file_path) / (1024 * 1024)

def load_single_pdf(file_path):
    """Tek bir PDF dosyasını güvenli şekilde yükler."""
    filename = os.path.basename(file_path)
    
    # Dosya boyutu kontrolü
    size_mb = get_file_size_mb(file_path)
    if size_mb > MAX_FILE_SIZE_MB:
        print(f"  ⏭️  {filename} ({size_mb:.1f} MB) - Çok büyük, atlanıyor...")
        skipped_files.append(f"{filename} ({size_mb:.1f} MB)")
        stats["pdf_skipped"] += 1
        return []
    
    try:
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        page_count = len(docs)
        stats["pdf_success"] += 1
        stats["total_pages"] += page_count
        print(f"  ✅ {filename} ({page_count} sayfa)")
        return docs
    except Exception as e:
        error_msg = str(e)[:50]  # Hatayı kısalt
        print(f"  ❌ {filename} - Hata: {error_msg}")
        failed_files.append(filename)
        stats["pdf_failed"] += 1
        return []

def load_structured_data(file_path):
    """CSV veya Excel dosyasını yükleyip Document listesine dönüştürür."""
    filename = os.path.basename(file_path)
    try:
        if file_path.endswith('.csv'):
            # Farklı encoding'leri dene
            for encoding in ['utf-8', 'latin-1', 'cp1254', 'iso-8859-9']:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                df = pd.read_csv(file_path, encoding='utf-8', errors='ignore')
        else:
            df = pd.read_excel(file_path)
        
        documents = []
        for _, row in df.iterrows():
            content = " | ".join([f"{col}: {val}" for col, val in row.items()])
            documents.append(Document(page_content=content, metadata={"source": file_path}))
        
        stats["csv_success"] += 1
        print(f"  ✅ {filename} ({len(df)} satır)")
        return documents
    except Exception as e:
        print(f"  ❌ {filename} - Hata: {e}")
        failed_files.append(filename)
        return []

# --- BANNER ---
print("\n" + "=" * 60)
print("🧬 ALERJİ CHATBOT - VERİ YÜKLEME SİSTEMİ")
print("=" * 60 + "\n")

all_documents = []

# --- 1. PDF DOSYALARINI YÜKLE ---
print("📂 PDF Dosyaları Yükleniyor...")
print("-" * 40)

if os.path.exists(DATA_FOLDER):
    pdf_files = [f for f in os.listdir(DATA_FOLDER) if f.lower().endswith('.pdf')]
    
    if pdf_files:
        for pdf_file in sorted(pdf_files):
            file_path = os.path.join(DATA_FOLDER, pdf_file)
            docs = load_single_pdf(file_path)
            all_documents.extend(docs)
    else:
        print("  ℹ️ PDF dosyası bulunamadı.")
else:
    print("  ⚠️ 'data' klasörü bulunamadı!")

print()

# --- 2. CSV / EXCEL DOSYALARINI YÜKLE ---
print("📊 CSV/Excel Dosyaları Yükleniyor...")
print("-" * 40)

if os.path.exists(DATA_FOLDER):
    data_files = [f for f in os.listdir(DATA_FOLDER) 
                  if f.lower().endswith(('.csv', '.xlsx', '.xls'))]
    
    if data_files:
        for data_file in sorted(data_files):
            file_path = os.path.join(DATA_FOLDER, data_file)
            docs = load_structured_data(file_path)
            all_documents.extend(docs)
    else:
        print("  ℹ️ CSV/Excel dosyası bulunamadı.")
else:
    print("  ⚠️ 'data' klasörü bulunamadı!")

print()

# --- 3. WEB SİTELERİNİ YÜKLE ---
print("🌐 Web Siteleri Taranıyor...")
print("-" * 40)

if URL_LIST:
    for url in URL_LIST:
        try:
            loader = WebBaseLoader([url])
            docs = loader.load()
            all_documents.extend(docs)
            stats["web_success"] += 1
            # URL'yi kısalt
            short_url = url.replace("https://", "").replace("http://", "")[:40]
            print(f"  ✅ {short_url}...")
        except Exception as e:
            print(f"  ❌ {url[:40]}... - Hata")
else:
    print("  ℹ️ URL listesi boş.")

print()

# --- SONUÇ KONTROLÜ ---
if not all_documents:
    print("=" * 60)
    print("❌ HİÇBİR VERİ KAYNAĞI YÜKLENEMEDİ!")
    print("=" * 60)
    sys.exit(1)

# --- 4. PARÇALAMA (CHUNKING) ---
print("✂️  Metinler Parçalanıyor...")
print("-" * 40)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=100,
    separators=["\n\n", "\n", ". ", " ", ""]
)
splits = text_splitter.split_documents(all_documents)
print(f"  📄 {len(all_documents)} döküman → {len(splits)} parça")
print()

# --- 5. VEKTÖR VERİTABANI (CHROMA) ---
print("💾 Veritabanına Yazılıyor...")
print("-" * 40)
print(f"  ⏳ {len(splits)} parça işleniyor... (Bu biraz sürebilir)")

embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

# Mevcut veritabanını temizle ve yeniden oluştur
import shutil
if os.path.exists("./chroma_db"):
    shutil.rmtree("./chroma_db")

db = Chroma.from_documents(
    documents=splits, 
    embedding=embeddings, 
    persist_directory="./chroma_db"
)

print("  ✅ Veritabanı başarıyla oluşturuldu!")
print()

# --- ÖZET RAPOR ---
print("=" * 60)
print("📊 YÜKLEME RAPORU")
print("=" * 60)
print(f"""
  📄 PDF Dosyaları:
     • Başarılı: {stats['pdf_success']} dosya ({stats['total_pages']} sayfa)
     • Başarısız: {stats['pdf_failed']} dosya
     • Atlanan (büyük): {stats['pdf_skipped']} dosya

  📊 CSV/Excel: {stats['csv_success']} dosya
  🌐 Web Siteleri: {stats['web_success']} site
  
  📦 Toplam: {len(splits)} metin parçası veritabanına yazıldı
""")

if failed_files:
    print("  ⚠️ Okunamayan Dosyalar:")
    for f in failed_files:
        print(f"     • {f}")
    print()

if skipped_files:
    print("  ⏭️ Atlanan Dosyalar (Çok Büyük):")
    for f in skipped_files:
        print(f"     • {f}")
    print()

print("=" * 60)
print("✅ İŞLEM TAMAMLANDI! Bot eğitildi ve hazır.")
print("=" * 60 + "\n")
