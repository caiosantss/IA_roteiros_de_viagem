from langgraph.graph.state import StateGraph, CompiledStateGraph
from langgraph.constants import START, END
from langgraph.checkpoint.memory import InMemorySaver
from ReactAgent.state import State
from ReactAgent.utils import load_llm
from ReactAgent.tools import TOOLS


def call_llm(state: State) -> State:
    result = load_llm().bind_tools(TOOLS).invoke(state["messages"])
    
    #State=messages: [Anottated[Sequence[BaseMessage], add_message]]
    return {"messages" : [result]}

def build_graph() -> CompiledStateGraph:
    builder = StateGraph(State)
    
    builder.add_node("call_llm", call_llm)
    
    builder.add_edge(START, "call_llm")
    builder.add_edge("call_llm", END)
    
    return builder.compile(checkpointer=InMemorySaver())