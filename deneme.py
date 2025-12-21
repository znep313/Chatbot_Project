from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview") 
response = llm.invoke("Merhaba, nasılsın?")
print(response.content) 