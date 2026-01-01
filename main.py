import os
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

load_dotenv()

# --- AYARLAR ---
def load_keywords(file_path="keywords.txt"):
    """Anahtar kelimeleri txt dosyasından yükler."""
    keywords = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                
                if line and not line.startswith("#"):
                    keywords.append(line.lower())
        print(f"✅ {len(keywords)} anahtar kelime yüklendi.")
    except FileNotFoundError:
        print(f"⚠️ {file_path} bulunamadı! Varsayılan kelimeler kullanılıyor.")
        keywords = ["alerji", "alerjen", "astım", "kaşıntı", "besin", "polen", "ilaç", "test", "sağlık"]
    return keywords

ALLOWED_KEYWORDS = load_keywords()
chat_history = []
# Modeller

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

def get_text_content(ai_message):
    """Modelden gelen cevabın liste veya string olma durumunu güvenle çözer."""
    content = ai_message.content
    if isinstance(content, list):
        # Liste gelirse ilk elemanın içindeki 'text' anahtarını al
        return content[0].get('text', '')
    return str(content)

print("✅ SÜPER ASİSTAN ÇEVRİMİÇİ! (Hafıza + Canlı Arama + Filtre) (Çıkmak için 'q' veya 'exit' yazın)")

while True:
    user_input = input("\nSiz: ")
    if user_input.lower() in ['q', 'exit']: break
    if not user_input.strip(): continue

    # --- 1. KATMAN: ANAHTAR KELİME KONTROLÜ ---
    if not any(word in user_input.lower() for word in ALLOWED_KEYWORDS):
        print("Bot: Üzgünüm, sadece uzmanlık alanım (Alerji/Sağlık) ile ilgili soruları yanıtlayabilirim. 😊")
        continue

    # --- 2. KATMAN: KONU ANALİZİ (Gatekeeper) ---
    check_prompt = f"Bu soru sağlık/alerji ile mi ilgili? EVET veya HAYIR olarak cevap ver. Soru: {user_input}"
    raw_check = llm.invoke(check_prompt)
    check_text = get_text_content(raw_check).upper()

    if "EVET" not in check_text:
        print("Bot: Bu konu uzmanlık alanımın dışında kalıyor. Başka bir sağlık sorunuz var mı?")
        continue

    print("🔎 Bilgi harmanlanıyor...")

    # --- 3. KATMAN: HAFIZA VE ARAŞTIRMA ---
    local_docs = db.similarity_search(user_input, k=3)
    sources = list(set([d.metadata.get("source", "Dosya") for d in local_docs]))
    local_context = "\n".join([d.page_content for d in local_docs])

    try:
        # Web aramasını daha spesifik hale getirmek için 'medical' ekliyoruz
        web_res = tavily.search(query=f"{user_input} medical allergy", search_depth="advanced")
        web_context = "\n".join([r['content'] for r in web_res['results']])
    except Exception as e:
        web_context = "Web araması yapılamadı."

    # --- 4. KATMAN: CEVAP OLUŞTURMA ---
    # Geçmişteki son 2 mesajı hafıza olarak veriyoruz
    final_prompt = f"""
    Sen uzman bir alerji asistanısın.
    
    SOHBET GEÇMİŞİ: {chat_history[-4:]}
    YEREL KAYNAKLAR: {local_context}
    WEB BİLGİSİ: {web_context}
    
    SORU: {user_input}
    
    Talimat: Bilgileri birleştir, tıbbi terimleri açıkla ve dürüst ol. Kaynaklarda yoksa uydurma.
    """

    final_res = llm.invoke(final_prompt)
    response_text = get_text_content(final_res)
    
    print(f"\nBot: {response_text}")
    print(f"\n📍 Yararlanılan Kaynaklar: {', '.join(sources)}")
    
    # Hafızayı güncelle
    chat_history.append(f"Kullanıcı: {user_input}")
    chat_history.append(f"Bot: {response_text}")
