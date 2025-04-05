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
    
    
    h_query = HumanMessage(content=input("User:\n"))
    query = [sys_msg, h_query]
    initial_state = State(graph_state=query)
    
    result = graph.invoke(initial_state)
    print(type(result))
    print(result)

    
    

    
    #display(Image(graph.get_graph().draw_mermaid_png()))
     
    #query = input("User:\n")

    #response = llm.invoke(query)
    
    #print(response.content)
    
    
    #def node_1(state):
    #    print("_____node_1_____")
    #    respone = llm.invoke(state["graph_state"])
    #    return {"graph_state": state['graph_state'] +f"{respone.content}"}
    



    #builder = StateGraph(State)
    

if __name__ == "__main__":
    main()