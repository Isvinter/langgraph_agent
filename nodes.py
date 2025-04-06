from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage

from pydantic import BaseModel, Field

import subprocess

from typing_extensions import List

from models import *


#klasasendefinition state
class State(BaseModel):
    graph_state: List[AnyMessage] = Field(default_factory=list)
    
    @classmethod
    def with_sys_msg(cls):
        sys_msg = SystemMessage(content="""You are a helpful assistand twich expert knowledge in Coding, and natural sciences.
                                When asked about topics touching natural sciences or informatics, tailer your answers to someone 
                                who has already broad foundational knowledge in thos fields""")
        return cls(graph_state=[sys_msg])
    
    def update_with(self, new_message: AnyMessage) -> "State":
        new_state = self.model_copy()
        new_state.graph_state.append(new_message)
        return new_state
    
#initialisierung des states mit system-message asl erste message 
def initialize_state(state: State) -> State:
    if not state.graph_state:
        state.graph_state.append(sys_msg)
    return state

#graph-visualisierung
def graph_visualization(graph):
    png_data = graph.get_graph().draw_mermaid_png()
    with open('graph.png', 'wb') as f:
        f.write(png_data)
    subprocess.run(['open', '-a', 'Preview', 'graph.png'])

#tool für websearch
def tevily_websearch(query):
    tavily_search = TavilySearchResults(max_results=3)
    search_docs = tavily_search.invoke(query)
    return search_docs

def graph_state_reducer(state: State, new_message: AnyMessage) -> State:
    new_state = state.model_copy()
    new_state.graph_state.append(new_message)
    return new_state

#llm-knoten
def llm_node(state: State):
    messages = [{"role": msg.type, "content": msg.content} for msg in state.graph_state]
    result_ai = llm_open_ai.invoke(messages)
    return state.update_with(result_ai)
    

       