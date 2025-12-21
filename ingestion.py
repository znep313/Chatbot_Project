import os
import sys
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, WebBaseLoader

load_dotenv()

# --- AYARLAR ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DATA_FOLDER = "./data"
# Öğretmek istediğin web sitelerinin linklerini buraya ekle:
URL_LIST = [
    "https://www.aid.org.tr/hastaliklar/alerji-ve-bagisiklik-sistemi-hastaliklari/gida-alerjisi/",
    "https://istanbulalerjimerkezi.com.tr/alerji-nedir-belirtileri-nelerdir/"
    # Buraya istediğin kadar güvenilir link ekleyebilirsin
]

if not GOOGLE_API_KEY:
    print("❌ HATA: .env dosyasında API Key bulunamadı!")
    sys.exit(1)

all_documents = []

# --- 1. PDF DOSYALARINI YÜKLE ---
print("📂 PDF'ler yükleniyor...")
if os.path.exists(DATA_FOLDER):
    try:
        pdf_loader = DirectoryLoader(DATA_FOLDER, glob="*.pdf", loader_cls=PyPDFLoader)
        pdf_docs = pdf_loader.load()
        all_documents.extend(pdf_docs)
        print(f"✅ {len(pdf_docs)} sayfa PDF yüklendi.")
    except Exception as e:
        print(f"⚠️ PDF yükleme hatası: {e}")
else:
    print("ℹ️ 'data' klasörü bulunamadı, PDF yüklenmedi.")

# --- 2. WEB SİTELERİNİ YÜKLE ---
print("🌐 Web siteleri taranıyor...")
if URL_LIST:
    try:
        web_loader = WebBaseLoader(URL_LIST)
        web_docs = web_loader.load()
        all_documents.extend(web_docs)
        print(f"✅ {len(URL_LIST)} adet web sitesi içeriği yüklendi.")
    except Exception as e:
        print(f"⚠️ Web yükleme hatası: {e}")

if not all_documents:
    print("❌ Hiçbir veri kaynağı bulunamadı! İşlem durduruldu.")
    sys.exit(1)

# --- 3. PARÇALAMA (CHUNKING) ---
print("✂️  Metinler parçalara bölünüyor...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
splits = text_splitter.split_documents(all_documents)

# --- 4. VEKTÖR VERİTABANI (CHROMA) ---
print(f"💾 {len(splits)} parça veritabanına yazılıyor... (Lütfen bekleyin)")
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

# Veritabanını sıfırdan oluşturup kaydediyoruz
db = Chroma.from_documents(
    documents=splits, 
    embedding=embeddings, 
    persist_directory="./chroma_db"
)

print("BAŞARILI! Bot hem PDF'leri hem de web sitelerini öğrendi.")