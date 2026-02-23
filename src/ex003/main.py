from typing import Sequence, TypedDict, Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.graph.message import Messages
from rich import print
from rich.markdown import Markdown
from dotenv import load_dotenv
import os
from pydantic import SecretStr


# Import Api Key e/or Base Url to local LLM
load_dotenv()
api_key = os.getenv("LM_STUDIO_API_KEY") or ""
base_url = os.getenv("LM_STUDIO_BASE_URL")


# Init LLM
llm = ChatOpenAI(
    model="google/gemma-3-1b", base_url=base_url, api_key=SecretStr(api_key)
)


# Reducer for log only
def reducer(a: Messages, b: Messages) -> Messages:
    print(f">Reducer - {a=},  {b=}")
    print()
    return add_messages(a, b)


# 1. Def State
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], reducer]
    # Anotated[type, metadata (reducer in this case that langchain will read and use)]


# 2. Def node
def call_llm(state: AgentState) -> AgentState:
    # Trigger do reducer
    llm_response = llm.invoke(state["messages"])
    # llm_response = AIMessage("Como você está?")
    print(f">call_llm: {llm_response=}")
    print()
    return {"messages": [llm_response]}


# 3. Def o StateGraph : Builder do graph
"""
StateGraph(shared_state): A graph whose nodes communicate by reading and writing to a !!shared state.!!
"""
builder = StateGraph(
    AgentState, config_schema=None, input=AgentState, output=AgentState
)


# 4 Add nodes to graph
# 4.1 Define node
builder.add_node("call_llm", call_llm)
# 4.2 Define edges
builder.add_edge(START, "call_llm")
builder.add_edge("call_llm", END)


# 5 Compile graph
graph = builder.compile()


if __name__ == "__main__":
    # 6 Run graph
    current_messages: Sequence[BaseMessage] = []

    # Gerenciando histórico manualmente sem checkpointers para ententimento.
    while True:
        user_input = input("Digite a sua mensagem: ")

        if user_input.lower() in ["q", "quit"]:
            print("Bye!")
            print(Markdown("---"))
            break

        human_message = HumanMessage(user_input)
        current_messages = [*current_messages, human_message]

        result = graph.invoke({"messages": current_messages})
        current_messages = result["messages"]

        print(Markdown(result["messages"][-1].content))
        print(Markdown("---"))
