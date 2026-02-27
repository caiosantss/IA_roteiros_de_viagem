from typing import Sequence, TypedDict, Annotated
from langchain.globals import set_debug
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables.config import RunnableConfig
from rich import print
from rich.markdown import Markdown
import threading
from dotenv import load_dotenv
import os
from pydantic import SecretStr

set_debug(True)

# Import Api Key e/or Base Url to local LLM
load_dotenv()
api_key = os.getenv("LM_STUDIO_API_KEY") or ""
base_url = os.getenv("LM_STUDIO_BASE_URL")


# Init LLM
llm = ChatOpenAI(
    model="google/gemma-3-1b", base_url=base_url, api_key=SecretStr(api_key)
)


# 1. Def State
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    # Anotated[type, metadata (reducer in this case that langchain will read and use)]


# 2. Def node
def call_llm(state: AgentState) -> AgentState:
    # Trigger do reducer
    llm_response = llm.invoke(state["messages"])
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

#5 Create a checkpointer - short term memory
checkpointer = InMemorySaver()
# 5.1 Compile graph
graph = builder.compile(checkpointer=checkpointer)
#Creating thread id to safe at checkpointer the session
config = RunnableConfig(configurable={'thread_id': threading.get_ident()})

if __name__ == "__main__":
    # 6 Run graph

    # Gerenciando histórico manualmente sem checkpointers para ententimento.
    while True:
        user_input = input("Digite a sua mensagem: ")
        print()

        if user_input.lower() in ["q", "quit"]:
            print("Bye!")
            print(Markdown("---"))
            break

        human_message = HumanMessage(user_input)

        result = graph.invoke({"messages": human_message}, config=config)

        print(Markdown(result["messages"][-1].content))
        print(Markdown("---"))
