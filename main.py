import os
from langchain_core.messages import HumanMessage

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from models import *
from nodes import *


def main():
    
    memory = MemorySaver()
    config = {"configurable": {"thread_id": 1}}
        
    #contruct Graph
    graph_builder = StateGraph(State)
    graph_builder.add_node("llm_node", llm_node)
    
    #logic of the graph
    graph_builder.add_edge(START, "llm_node")
    graph_builder.add_edge("llm_node", END)
    
    # Add
    #graph = graph_builder.compile()
    graph_memory = graph_builder.compile(checkpointer=memory)
    
     #initialisierung des states ausserhalb der schleife für persistenz
    state = State.with_sys_msg()
    
    #Main loop
    while True:
        
        #einlesen user-query
        user_input = input("User ('exit', 'quit' or 'bye' to end conversation):\n")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye")
            break
        h_query = HumanMessage(content=user_input)
        
        #user-query an state anhängen und graph ausführen
        state.update_with(h_query)
        result = graph_memory.invoke(state, config)
        
        #state-objekt updaten
        #state = result
        
        #ergebnisse ausgeben:
        print(type(result))
        print(result["graph_state"][-1].content)
        
        if len(state.graph_state) > 3:
            state = state.delete_message(-3, None)
    

if __name__ == "__main__":
    main()