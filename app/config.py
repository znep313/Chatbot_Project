"""
🧬 Alerji Chatbot - Konfigürasyon Ayarları
==========================================
Tüm uygulama ayarları bu dosyada merkezi olarak yönetilir.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# --- API ANAHTARLARI ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# --- MODEL AYARLARI ---
LLM_MODEL = "gemini-2.5-flash"
LLM_TEMPERATURE = 0.1
EMBEDDING_MODEL = "models/text-embedding-004"

# --- VERİTABANI AYARLARI ---
CHROMA_DB_PATH = "./chroma_db"
DATA_FOLDER = "./data"

# --- RAG AYARLARI ---
SIMILARITY_SEARCH_K = 3  # Kaç benzer belge getirilsin
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

# --- DOSYA AYARLARI ---
MAX_FILE_SIZE_MB = 50  # Maksimum PDF boyutu
KEYWORDS_FILE = "./keywords.txt"

# --- WEB KAYNAKLARI ---
URL_LIST = [
    "https://www.aid.org.tr/hastaliklar/alerji-ve-bagisiklik-sistemi-hastaliklari/gida-alerjisi/",
    "https://istanbulalerjimerkezi.com.tr/alerji-nedir-belirtileri-nelerdir/",
    "https://www.aid.org.tr/",
    "https://alerjiastim.org.tr/"
]

# --- UI AYARLARI ---
PAGE_TITLE = "Alerji Uzman Asistanı"
PAGE_ICON = "🧬"
LAYOUT = "wide"

