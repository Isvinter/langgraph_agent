import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from langchain_google_genai import ChatGoogleGenerativeAI



load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
gemini_api_key = os.getenv("GOOGLE_API_KEY")

llm_open_ai = ChatOpenAI(
    model= "o3-mini",
    api_key= openai_api_key)

llm_google = ChatGoogleGenerativeAI(
    model= "gemini-2.5-pro-exp-03-25",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    google_api_key=gemini_api_key)

llm_summarizer = ChatOpenAI(
    model= "gpt-3.5-turbo",
    api_key= openai_api_key)