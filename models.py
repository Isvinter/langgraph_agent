import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

sys_msg = SystemMessage(content="""You are a helpful assistand twich expert knowledge in Coding, and natural sciences.
                        When asked about topics touching natural sciences or informatics, tailer your answers to someone 
                        who has already broad foundational knowledge in thos fields""")

llm = ChatOpenAI(
    model= "o3-mini",
    api_key= openai_api_key)