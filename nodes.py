from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage

from pydantic import BaseModel, Field

import subprocess

from typing_extensions import List
from typing import Optional

from models import *


#klasasendefinition state
class State(BaseModel):
    graph_state: List[AnyMessage] = Field(default_factory=list)
    summary: Optional[AnyMessage] = None
    
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
    
    def delete_message(self, startindex, stopindex):
        """removes a message from a list or returns a slice of the message list (startindex, stopindex)
        
        args: startindex, stopindex"""
        new_state = self.model_copy()
        if stopindex is None:
            stopindex = len(new_state.graph_state)
        if startindex == stopindex:
            del new_state.graph_state[startindex]
        else:
            slice_list = new_state.graph_state[startindex: stopindex]
            new_state.graph_state = slice_list
        return new_state
    
    def update_summary(self, new_summary: AnyMessage) -> "State":
        new_state = self.model_copy()
        new_state.summary = new_summary
        return new_state
        
    
    def summarize_conversation(self):
        """Fasst alle Nachrichten außer den letzten 4 zusammen und speichert die Zusammenfassung im Parameter `summary`."""
        sys_msg_summarize = SystemMessage(content="""Summarize the content of this conversation for context for future conversations. 
                                            Include all information that might become relevant in the future, but be concise and keep 
                                            token usage low.""")
        msgs_to_summarize = []

        # Prüfen, ob mehr als 4 Nachrichten in der Konversationshistorie sind
        if len(self.graph_state) <= 4:
            return self
        
        # Falls eine Summary vorhanden ist, füge sie als erstes Element hinzu
        if self.summary is not None:
            msgs_to_summarize.append(self.summary)
        
        # Füge alle Nachrichten außer den letzten 4 hinzu
        msgs_to_summarize.extend(self.graph_state[1:-4])
        
        # Skip summarization if there's nothing to summarize
        if not msgs_to_summarize:
            return self
        
        # Zusammenfassung erstellen
        query_list = [sys_msg_summarize] + msgs_to_summarize
        try:
            summary = llm_summarizer.invoke(query_list)
        except Exception as e:
            print(f"Error during summarization: {e}")
            return self
        
        # Aktualisiere den State mit der neuen Zusammenfassung
        return self.update_summary(summary)
        
            
    
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

#llm-knoten
def llm_node(state: State):
    messages = []
    
    # Füge die Systemnachricht hinzu (erste Nachricht)
    if state.graph_state:
        messages.append({"role": state.graph_state[0].type, "content": state.graph_state[0].content})
    
    # Falls eine Summary vorhanden ist, füge sie als zweite Nachricht hinzu
    if state.summary:
        messages.append({"role": state.summary.type, "content": state.summary.content})
    
    # Füge die restlichen Nachrichten aus graph_state hinzu (außer der Systemnachricht)
    messages.extend([{"role": msg.type, "content": msg.content} for msg in state.graph_state[1:]])
    
    # Rufe das LLM mit den Nachrichten auf
    try:
        result_ai = llm_open_ai.invoke(messages)
    except Exception as e:
        print(f"Error during LLM invocation: {e}")
        return state
    
    # Aktualisiere den State mit dem Ergebnis
    return state.update_with(result_ai)
    