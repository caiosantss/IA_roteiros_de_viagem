#Langgraph conditional edge
import operator
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from rich import print
from dataclasses import dataclass

# Definir o State - Dataclass ou Typedict

@dataclass
class State:
    nodes_path: Annotated[list[str], operator.add]
    current_number: int = 0


# Definir os Nodes

def node_a(state: State) -> State:
    output_state: State = State(nodes_path=["A"], current_number=state.current_number)
    print("> node_a", f"{state=}", f"{output_state=}")
    return output_state

#Node não altera estado, cria novos e reducer faz a concatenação deles.

def node_b(state: State) -> State:
    output_state: State = State(nodes_path=["B"], current_number=state.current_number)
    print("> node_b", f"{state=}", f"{output_state=}")
    return output_state

def node_c(state: State) -> State:
    output_state: State = State(nodes_path=["C"], current_number=state.current_number)
    print("> node_c", f"{state=}", f"{output_state=}")
    return output_state

#Função condicional, que será usada dentro de "add_conditional_edges"
def the_conditioner(state:State): 
    if state.current_number >= 10:
        #Retorna literalmente o nome do node
        return "C"
    return "B"
    


# Criar buider do grafo

builder = StateGraph(State)

#Criar Nodes

builder.add_node("A", node_a)
builder.add_node("B", node_b)
builder.add_node("C", node_c)

# Definir os Edges

builder.add_edge(START, "A")
"""
    add_conditional_edges(source, path, path_map)
    Args:
        source: The starting node.
        path: The callable that determines the next node or nodes.
        path_map: Optional mapping of paths to node names. If omitted the paths returned by `path` should be node names.
"""
builder.add_conditional_edges("A", the_conditioner, ["B", "C"])
builder.add_edge("B", END)
builder.add_edge("C", END)

#Compilar Graph

graph = builder.compile()

#Gerando código do grafo para visualizar no https://mermaid.live
print(graph.get_graph().draw_mermaid()) 

#Pegar resultado
#Indo para o Node C baseado na função de condicional e no conditional edge
resultado = graph.invoke(State(nodes_path=[], current_number=20))
print(f"{resultado=}")

