import os
import sys
from dotenv import load_dotenv

# Sadece temel parçaları çağırıyoruz, karmaşık zincirleri değil.
try:
    from langchain_chroma import Chroma
    from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
except ImportError as e:
    print(f"❌ Kütüphane eksik: {e}")
    sys.exit(1)

# 1. Ayarlar
load_dotenv()

if "GOOGLE_API_KEY" not in os.environ:
    print("❌ HATA: .env dosyasında GOOGLE_API_KEY bulunamadı.")
    sys.exit(1)

print("🤖 Alerji Asistanı (Manuel Mod) Başlatılıyor...")

# 2. Modelleri Hazırla
# Not: Ingestion.py ile aynı embedding modelini kullanmak zorundayız.
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

# Beyin (LLM)
llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=0.3
)

# 3. Veritabanına Bağlan
if not os.path.exists("./chroma_db"):
    print("❌ HATA: 'chroma_db' klasörü yok. Önce veriyi yüklemek için ingestion.py çalıştır.")
    sys.exit(1)

db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

print("\n✅ SİSTEM HAZIR! (Çıkmak için 'q')\n")

# --- SOHBET DÖNGÜSÜ ---
while True:
    user_input = input("Siz: ")
    
    if user_input.lower() in ['q', 'exit', 'cikis']:
        print("Görüşmek üzere!")
        break
    
    if not user_input.strip():
        continue

    print("🔎 Bilgi aranıyor ve cevaplanıyor...")

    try:
        # ADIM A: RETRIEVAL (Bilgi Getirme)
        # Zincir yerine veritabanına doğrudan "Bana buna benzer 3 parça getir" diyoruz.
        relevant_docs = db.similarity_search(user_input, k=3)
        
        # Bulunan metinleri tek bir paragraf haline getiriyoruz (Context oluşturma)
        context_text = "\n\n".join([doc.page_content for doc in relevant_docs])
        
        if not context_text:
            context_text = "Veritabanında ilgili bilgi bulunamadı."

        # ADIM B: AUGMENTATION (İstemi Hazırlama)
        # LLM'e göndereceğimiz mesajı f-string ile elle yazıyoruz.
        final_prompt = f"""
        Sen uzman bir alerji asistanısın. Aşağıdaki "BULUNAN BİLGİ" kısmını kullanarak soruyu cevapla.
        Eğer bilgi metinde yoksa, kendi kafandan uydurma, "Bu konuda bilgim yok" de.

        SORU: {user_input}

        BULUNAN BİLGİ (CONTEXT):
        {context_text}

        CEVAP:
        """

        # ADIM C: GENERATION (Cevap Üretme)
        # Hazırladığımız metni direkt modele veriyoruz.
        response = llm.invoke(final_prompt)
        
        print(f"Bot: {response.content}\n")
        
    except Exception as e:
        print(f"❌ Bir hata oldu: {e}")