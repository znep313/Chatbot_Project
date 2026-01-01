 import streamlit as st
import os
import json
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Alerji Uzman Asistanı", 
    page_icon="🧬", 
    layout="wide",
    initial_sidebar_state="expanded"
)

load_dotenv()

# --- CUSTOM CSS ---
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Root Variables */
    :root {
        --primary: #0d9488;
        --primary-light: #14b8a6;
        --primary-dark: #0f766e;
        --accent: #f59e0b;
        --bg-dark: #0f172a;
        --bg-card: #1e293b;
        --bg-card-hover: #334155;
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --border: #334155;
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ef4444;
    }
    
    /* Main App Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Typography */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Main Title */
    .main-title {
        font-family: 'Outfit', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #14b8a6, #0d9488, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 0.5rem;
    }
    
    .sub-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1rem;
        color: #94a3b8;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Hero Section */
    .hero-container {
        background: linear-gradient(135deg, rgba(13, 148, 136, 0.1), rgba(245, 158, 11, 0.05));
        border: 1px solid rgba(13, 148, 136, 0.3);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-right: 1px solid #334155;
    }
    
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #f1f5f9 !important;
        font-family: 'Outfit', sans-serif;
    }
    
    /* Sidebar Section Cards */
    .sidebar-card {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .sidebar-card:hover {
        border-color: #0d9488;
        box-shadow: 0 0 20px rgba(13, 148, 136, 0.2);
    }
    
    .sidebar-card-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: #14b8a6;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* File List Items */
    .file-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 0.75rem;
        background: rgba(15, 23, 42, 0.5);
        border-radius: 8px;
        margin-bottom: 0.5rem;
        border-left: 3px solid #0d9488;
        font-size: 0.85rem;
        color: #e2e8f0;
        transition: all 0.2s ease;
    }
    
    .file-item:hover {
        background: rgba(13, 148, 136, 0.1);
        transform: translateX(4px);
    }
    
    .file-count {
        font-size: 0.75rem;
        color: #64748b;
        margin-top: 0.5rem;
        text-align: right;
    }
    
    /* Buttons */
    .stButton > button {
        font-family: 'Outfit', sans-serif;
        font-weight: 500;
        border-radius: 10px;
        padding: 0.5rem 1.5rem;
        transition: all 0.3s ease;
        border: none;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(13, 148, 136, 0.3);
    }
    
    /* Download Buttons */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #0d9488, #0f766e) !important;
        color: white !important;
        font-family: 'Outfit', sans-serif;
        font-weight: 500;
        border-radius: 10px;
        border: none !important;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #14b8a6, #0d9488) !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(13, 148, 136, 0.4);
    }
    
    /* Chat Messages */
    [data-testid="stChatMessage"] {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 1rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stChatMessage"][data-testid*="user"] {
        background: linear-gradient(135deg, rgba(13, 148, 136, 0.15), rgba(13, 148, 136, 0.05));
        border-color: rgba(13, 148, 136, 0.3);
    }
    
    [data-testid="stChatMessage"][data-testid*="assistant"] {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.6));
        border-color: #334155;
    }
    
    /* Chat Input */
    [data-testid="stChatInput"] {
        border-radius: 16px;
        border: 2px solid #334155;
        background: rgba(30, 41, 59, 0.8);
        transition: all 0.3s ease;
    }
    
    [data-testid="stChatInput"]:focus-within {
        border-color: #0d9488;
        box-shadow: 0 0 20px rgba(13, 148, 136, 0.2);
    }
    
    [data-testid="stChatInput"] textarea {
        font-family: 'Outfit', sans-serif;
        color: #f1f5f9;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(30, 41, 59, 0.6);
        border-radius: 10px;
        font-family: 'Outfit', sans-serif;
        font-weight: 500;
    }
    
    .streamlit-expanderContent {
        background: rgba(15, 23, 42, 0.4);
        border-radius: 0 0 10px 10px;
    }
    
    /* Metrics */
    [data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1rem;
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Outfit', sans-serif;
        color: #94a3b8;
    }
    
    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace;
        color: #14b8a6;
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #0d9488, #14b8a6, #f59e0b);
        border-radius: 10px;
    }
    
    /* Alerts */
    .stSuccess {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 10px;
    }
    
    .stInfo {
        background: rgba(13, 148, 136, 0.1);
        border: 1px solid rgba(13, 148, 136, 0.3);
        border-radius: 10px;
    }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 10px;
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: rgba(30, 41, 59, 0.4);
        border: 2px dashed #334155;
        border-radius: 12px;
        padding: 1rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #0d9488;
        background: rgba(13, 148, 136, 0.05);
    }
    
    /* Divider */
    hr {
        border-color: #334155;
        margin: 1.5rem 0;
    }
    
    /* Status Widget */
    [data-testid="stStatusWidget"] {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid #334155;
        border-radius: 12px;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1e293b;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #0d9488;
    }
    
    /* Feature Cards */
    .feature-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.6));
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        border-color: #0d9488;
        transform: translateY(-4px);
        box-shadow: 0 10px 30px rgba(13, 148, 136, 0.2);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #f1f5f9;
        margin-bottom: 0.25rem;
    }
    
    .feature-desc {
        font-size: 0.85rem;
        color: #94a3b8;
    }
    
    /* Pulse Animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* Gradient Text */
    .gradient-text {
        background: linear-gradient(135deg, #14b8a6, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
</style>
""", unsafe_allow_html=True)

# --- MODEL BAŞLATMA ---
@st.cache_resource
def get_models():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)
    tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    return embeddings, llm, tavily

embeddings, llm, tavily = get_models()

# --- YARDIMCI FONKSİYONLAR ---
def get_text_content(ai_message):
    content = ai_message.content
    return content[0].get('text', '') if isinstance(content, list) else str(content)

@st.cache_data
def load_keywords(file_path="keywords.txt"):
    keywords = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    keywords.append(line.lower())
    except FileNotFoundError:
        keywords = ["alerji", "alerjen", "astım", "kaşıntı", "besin", "polen", "ilaç", "test", "sağlık"]
    return keywords

def get_uploaded_files_list():
    try:
        db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
        all_docs = db.get()
        sources = set()
        if all_docs and 'metadatas' in all_docs:
            for meta in all_docs['metadatas']:
                if meta and 'source' in meta:
                    source = meta['source']
                    filename = os.path.basename(source) if source else "Bilinmeyen"
                    sources.add(filename)
        return sorted(list(sources))
    except Exception:
        return []

def export_chat_history():
    if not st.session_state.messages:
        return ""
    
    lines = []
    lines.append("=" * 50)
    lines.append("🧬 Alerji Asistanı - Sohbet Geçmişi")
    lines.append(f"📅 Tarih: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    lines.append("=" * 50)
    lines.append("")
    
    for msg in st.session_state.messages:
        role = "👤 Siz" if msg["role"] == "user" else "🤖 Asistan"
        lines.append(f"{role}:")
        lines.append(msg["content"])
        lines.append("-" * 30)
        lines.append("")
    
    return "\n".join(lines)

def calculate_source_ratio(local_context, web_context):
    local_len = len(local_context) if local_context else 0
    web_len = len(web_context) if web_context else 0
    total = local_len + web_len
    
    if total == 0:
        return 0, 0
    
    pdf_ratio = local_len / total
    web_ratio = web_len / total
    return pdf_ratio, web_ratio

# --- YAN PANEL (SIDEBAR) ---
with st.sidebar:
    # Logo/Brand
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0 1.5rem 0;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🧬</div>
            <div style="font-size: 1.2rem; font-weight: 600; color: #14b8a6;">Alerji Asistanı</div>
            <div style="font-size: 0.75rem; color: #64748b;">v2.0 Pro</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # --- 1. DOSYA YÜKLEME ---
    st.markdown("""
        <div class="sidebar-card-title">📤 Dosya Yükle</div>
    """, unsafe_allow_html=True)
    st.caption("PDF, CSV veya Excel dosyası yükleyerek botu eğitin")
    
    uploaded_file = st.file_uploader("Dosya seç", type=["pdf", "csv", "xlsx"], label_visibility="collapsed")
    
    if uploaded_file is not None:
        with st.spinner("✨ Dosya işleniyor..."):
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            if uploaded_file.name.endswith(".pdf"):
                loader = PyPDFLoader(uploaded_file.name)
                docs = loader.load()
            else:
                df = pd.read_csv(uploaded_file.name) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file.name)
                docs = [Document(page_content=df.to_string(), metadata={"source": uploaded_file.name})]
            
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            splits = text_splitter.split_documents(docs)
            
            Chroma.from_documents(
                documents=splits, 
                embedding=embeddings, 
                persist_directory="./chroma_db"
            )
            st.success(f"✅ {uploaded_file.name} başarıyla eklendi!")
            os.remove(uploaded_file.name)
            st.rerun()
    
    st.divider()
    
    # --- 2. YÜKLENEN DOSYALAR LİSTESİ ---
    st.markdown("""
        <div class="sidebar-card-title">📚 Bilgi Tabanı</div>
    """, unsafe_allow_html=True)
    
    uploaded_files_list = get_uploaded_files_list()
    
    if uploaded_files_list:
        for filename in uploaded_files_list:
            if filename.endswith('.pdf'):
                icon = "📄"
                color = "#ef4444"
            elif filename.endswith(('.csv', '.xlsx', '.xls')):
                icon = "📊"
                color = "#22c55e"
            else:
                icon = "📁"
                color = "#64748b"
            
            st.markdown(f"""
                <div class="file-item">
                    <span>{icon}</span>
                    <span style="flex: 1; overflow: hidden; text-overflow: ellipsis;">{filename}</span>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="file-count">📁 {len(uploaded_files_list)} dosya yüklendi</div>
        """, unsafe_allow_html=True)
    else:
        st.info("💡 Henüz dosya yüklenmemiş")
    
    st.divider()
    
    # --- 3. SOHBETİ KAYDET ---
    st.markdown("""
        <div class="sidebar-card-title">💾 Sohbet Yönetimi</div>
    """, unsafe_allow_html=True)
    
    if st.session_state.get("messages"):
        chat_export = export_chat_history()
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 TXT",
                data=chat_export,
                file_name=f"sohbet_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col2:
            json_export = json.dumps(st.session_state.messages, ensure_ascii=False, indent=2)
            st.download_button(
                label="📥 JSON",
                data=json_export,
                file_name=f"sohbet_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)
        
        if st.button("🗑️ Sohbeti Temizle", use_container_width=True, type="secondary"):
            st.session_state.messages = []
            st.rerun()
    else:
        st.info("💬 Henüz sohbet başlamadı")
    
    # Footer
    st.markdown("""
        <div style="position: absolute; bottom: 1rem; left: 1rem; right: 1rem; text-align: center;">
            <div style="font-size: 0.7rem; color: #475569;">
                Powered by Gemini AI 🚀
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- ANA EKRAN ---
# Header
st.markdown("""
    <div class="main-title">🧬 Akıllı Alerji & Sağlık Asistanı</div>
    <div class="sub-title">Yapay Zeka Destekli • PDF Analizi • Canlı Web Araması • Akademik Kaynaklar</div>
""", unsafe_allow_html=True)

# Feature Cards (Sohbet yoksa göster)
if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">📄</div>
                <div class="feature-title">PDF Analizi</div>
                <div class="feature-desc">Akademik makaleleri ve raporları anlık analiz edin</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🌐</div>
                <div class="feature-title">Canlı Arama</div>
                <div class="feature-desc">Güncel tıbbi bilgilere anında erişin</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🔬</div>
                <div class="feature-title">Çapraz Reaksiyon</div>
                <div class="feature-desc">Alerjen etkileşimlerini keşfedin</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 2rem'></div>", unsafe_allow_html=True)

# Veritabanı bağlantısı
db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

# Sohbet Geçmişi
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🧑‍💻" if message["role"] == "user" else "🧬"):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "source_info" in message:
            info = message["source_info"]
            with st.expander("📊 Kaynak Analizi", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("📄 PDF Kaynaklar", f"{info['pdf_ratio']:.0%}")
                    st.progress(info['pdf_ratio'])
                with col2:
                    st.metric("🌐 Web Kaynaklar", f"{info['web_ratio']:.0%}")
                    st.progress(info['web_ratio'])

# --- SORU-CEVAP DÖNGÜSÜ ---
ALLOWED_KEYWORDS = load_keywords()

if prompt := st.chat_input("💬 Alerji hakkında bir soru sorun..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🧬"):
        if not any(word in prompt.lower() for word in ALLOWED_KEYWORDS):
            full_response = "Merhaba! 👋 Ben sadece **alerji ve sağlık** konularında uzmanım. Size bu alanda yardımcı olabilirim."
            source_info = None
        else:
            check_text = get_text_content(llm.invoke(f"Soru sağlıkla mı ilgili? EVET/HAYIR: {prompt}")).upper()
            
            if "EVET" not in check_text:
                full_response = "Bu konu uzmanlık alanımın dışında kalıyor. Alerji veya sağlık ile ilgili sorularınızı yanıtlayabilirim. 🩺"
                source_info = None
            else:
                local_context = ""
                web_context = ""
                sources = []
                
                with st.status("🔍 Veriler analiz ediliyor...", expanded=True) as status:
                    st.write("📄 Yerel dosyalar taranıyor...")
                    local_docs = db.similarity_search(prompt, k=3)
                    local_context = "\n".join([d.page_content for d in local_docs])
                    sources = list(set([d.metadata.get("source", "Hafıza") for d in local_docs]))
                    
                    st.write("🌐 Canlı web araması yapılıyor...")
                    try:
                        web_res = tavily.search(query=f"{prompt} medical allergy analysis", search_depth="advanced")
                        web_context = "\n".join([r['content'] for r in web_res['results']])
                    except Exception:
                        web_context = ""
                    
                    st.write("🧠 Cevap oluşturuluyor...")
                    status.update(label="✅ Analiz tamamlandı!", state="complete")

                pdf_ratio, web_ratio = calculate_source_ratio(local_context, web_context)
                source_info = {"pdf_ratio": pdf_ratio, "web_ratio": web_ratio}

                final_prompt = f"Uzman bir Alerji Asistanı ol. İngilizce kaynakları Türkçe özetle.\nHAFIZA: {local_context}\nWEB: {web_context}\nSORU: {prompt}"
                full_response = get_text_content(llm.invoke(final_prompt))
                
                if sources:
                    source_names = [os.path.basename(s) for s in sources]
                    full_response += f"\n\n---\n**📍 Yararlanılan Dosyalar:** {', '.join(source_names)}"

        st.markdown(full_response)
        
        if source_info:
            with st.expander("📊 Kaynak Analizi", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("📄 PDF Kaynaklar", f"{source_info['pdf_ratio']:.0%}")
                    st.progress(source_info['pdf_ratio'])
                with col2:
                    st.metric("🌐 Web Kaynaklar", f"{source_info['web_ratio']:.0%}")
                    st.progress(source_info['web_ratio'])
                
                if source_info['pdf_ratio'] > 0.7:
                    st.success("✅ **Yüksek güvenilirlik:** Cevap ağırlıklı olarak yüklediğiniz belgelerden oluşturuldu.")
                elif source_info['pdf_ratio'] > 0.3:
                    st.info("ℹ️ **Karma kaynak:** Cevap hem belgelerden hem web'den derlendi.")
                else:
                    st.warning("⚠️ **Web ağırlıklı:** Cevap çoğunlukla web kaynaklarından alındı. Doğrulamayı unutmayın.")
        
        msg_data = {"role": "assistant", "content": full_response}
        if source_info:
            msg_data["source_info"] = source_info
        st.session_state.messages.append(msg_data)
