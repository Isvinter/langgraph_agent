from langchain_community.tools.tavily_search import TavilySearchResults
import subprocess
from typing_extensions import TypedDict
from models import *


class State(TypedDict):
    graph_state: str

def tevily_websearch(query):
    tavily_search = TavilySearchResults(max_results=3)
    search_docs = tavily_search.invoke(query)
    return search_docs

def llm_node(state: State):
    result_ai = llm.invoke(state["graph_state"])
    return {"graph_state": state["graph_state"] + " AI_assistant respsnse: " + result_ai.content}  
    
def graph_visualization(graph):
    png_data = graph.get_graph().draw_mermaid_png()
    with open('graph.png', 'wb') as f:
        f.write(png_data)
    subprocess.run(['open', '-a', 'Preview', 'graph.png'])
       