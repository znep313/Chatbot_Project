"""
🧬 Alerji Chatbot - LLM Model Yönetimi
======================================
Google Gemini ve embedding modelleri bu dosyada yönetilir.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from tavily import TavilyClient

load_dotenv()


def get_embeddings(model_name="models/text-embedding-004"):
    """
    Google Text Embedding modelini döndürür.
    
    Args:
        model_name: Embedding model adı
        
    Returns:
        GoogleGenerativeAIEmbeddings: Embedding modeli
    """
    return GoogleGenerativeAIEmbeddings(model=model_name)


def get_llm(model_name="gemini-2.5-flash", temperature=0.1):
    """
    Google Gemini LLM modelini döndürür.
    
    Args:
        model_name: LLM model adı
        temperature: Yaratıcılık seviyesi (0-1)
        
    Returns:
        ChatGoogleGenerativeAI: LLM modeli
    """
    return ChatGoogleGenerativeAI(model=model_name, temperature=temperature)


def get_tavily():
    """
    Tavily web arama istemcisini döndürür.
    
    Returns:
        TavilyClient: Tavily istemcisi
    """
    return TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def get_models():
    """
    Tüm modelleri (embeddings, llm, tavily) döndürür.
    
    Returns:
        tuple: (embeddings, llm, tavily)
    """
    embeddings = get_embeddings()
    llm = get_llm()
    tavily = get_tavily()
    return embeddings, llm, tavily

