"""
🧬 Alerji Chatbot - Yardımcı Fonksiyonlar
=========================================
Tekrar kullanılabilir yardımcı fonksiyonlar.
"""

import os


def get_text_content(ai_message):
    """
    Modelden gelen cevabın liste veya string olma durumunu güvenle çözer.
    
    Args:
        ai_message: LLM'den gelen yanıt objesi
        
    Returns:
        str: Yanıt metni
    """
    content = ai_message.content
    if isinstance(content, list):
        return content[0].get('text', '')
    return str(content)


def load_keywords(file_path="keywords.txt"):
    """
    Anahtar kelimeleri txt dosyasından yükler.
    
    Args:
        file_path: Anahtar kelime dosyasının yolu
        
    Returns:
        list: Anahtar kelimeler listesi
    """
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


def get_file_size_mb(file_path):
    """
    Dosya boyutunu MB olarak döndürür.
    
    Args:
        file_path: Dosya yolu
        
    Returns:
        float: Dosya boyutu (MB)
    """
    return os.path.getsize(file_path) / (1024 * 1024)


def calculate_source_ratio(local_context, web_context):
    """
    PDF ve Web kaynak oranlarını hesaplar.
    
    Args:
        local_context: Yerel kaynaklardan gelen metin
        web_context: Web kaynaklarından gelen metin
        
    Returns:
        tuple: (pdf_ratio, web_ratio)
    """
    local_len = len(local_context) if local_context else 0
    web_len = len(web_context) if web_context else 0
    total = local_len + web_len
    
    if total == 0:
        return 0, 0
    
    pdf_ratio = local_len / total
    web_ratio = web_len / total
    return pdf_ratio, web_ratio


def format_sources(sources):
    """
    Kaynak dosya isimlerini formatlar.
    
    Args:
        sources: Kaynak dosya yolları listesi
        
    Returns:
        list: Formatlanmış dosya isimleri
    """
    return [os.path.basename(s) for s in sources]

