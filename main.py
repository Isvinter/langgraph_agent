import os
from typing import Literal
from typing_extensions import TypedDict
from IPython.display import Image, display

from langchain_google_genai import ChatGoogleGenerativeAI 

from langchain_core.messages import HumanMessage, SystemMessage

from langgraph.graph import StateGraph, START, END

from models import *
from nodes import *



def main():
        
    #contruct Graph
    graph_builder = StateGraph(State)
    graph_builder.add_node("llm_node", llm_node)
    
    #logic of the graph
    graph_builder.add_edge(START, "llm_node")
    graph_builder.add_edge("llm_node", END)
    
    # Add
    graph = graph_builder.compile()
    
    #initialisierung des states ausserhalb der schleife für persistenz
    state = State()
    state = graph_state_reducer(state, sys_msg)
    
    #Main loop
    while True:
        
        #einlesen user-query
        user_input = input("User ('exit', 'quit' or 'bye' to end conversation):\n")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye")
            break
        h_query = HumanMessage(content=user_input)
        
        #user-query an state anhängen und graph ausführen
        state = graph_state_reducer(state, h_query)
        result = graph.invoke(state)
        
        #ergebnisse ausgeben:
        print(type(result))
        print(result)
    

if __name__ == "__main__":
    main()