from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage
from dotenv import load_dotenv
import os
from rich import print

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

##Posso iniciar um modelo com a função init_chat_model, isso tira a dependência de eu importar diretamente a biblioteca do provedor no começo do código, o langchain faz isso para nós e automaticamente cria um objeto do tipo específico. 
llm = init_chat_model("openai:gpt-5-nano")
print(llm)
