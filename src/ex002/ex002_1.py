#Langgraph node/edge

import operator
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END, add_messages
from rich import print

# Definir o State


class State(TypedDict):
    nodes_path: Annotated[list[str], operator.add]


# Definir os Nodes

def node_a(state: State) -> State:
    return {"nodes_path": ["A"]}

#Node não altera estado, cria novos e reducer faz a concatenação deles.

def node_b(state: State) -> State:
    return {"nodes_path": ["B"]}

# Criar buider do grafo

builder = StateGraph(State)

#Criar Nodes

builder.add_node("A", node_a)
builder.add_node("B", node_b)

# Definir os Edges

builder.add_edge(START, "A")
builder.add_edge("A", "B")
builder.add_edge("B", END)

#Compilar Graph

graph = builder.compile()

#Pegar resultado

resultado = graph.invoke({"nodes_path": []})
print(f"{resultado=}")

