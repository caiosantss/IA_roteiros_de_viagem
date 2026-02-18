# Chat com memória
import os

from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

modelo = ChatOpenAI(model="gpt-5-nano", temperature=1, api_key=api_key)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Você é um assistente de viagem que ajuda os usuários a escolherem destinos turísticos com base em seus interesses e preferências.",
        ),
        # Histórico sempre vai ser o placeholder do prompt.
        ("placeholder", "{historico}"),
        ("human", "{query}"),
    ]
)

cadeia = prompt | modelo | StrOutputParser()

memoria = {}
sessao = "sessao1"


# Padrao singleton - garante que haja apenas uma instância de memória por sessão.
def historico_por_sessao(sessao: str):
    if sessao not in memoria:
        # InMemoryChatMessageHistory: Vive apenas na RAM, guarda mensagens em uma lista ordenada.
        memoria[sessao] = InMemoryChatMessageHistory()
    return memoria[sessao]


lista_perguntas = [
    "Quero visitar uma praia com águas cristalinas, no Brasil, me recomente uma.",
    "Qual é a melhor época do ano para visitar essa praia?",
]

cadeia_com_memoria = RunnableWithMessageHistory(
    runnable=cadeia,
    # Vai receber entrada pela váriavel passada na config do invoke.
    get_session_history=historico_por_sessao,
    input_messages_key="query",
    history_messages_key="historico",
)


for pergunta in lista_perguntas:
    resposta = cadeia_com_memoria.invoke(
        {
            "query": pergunta,
        },
        # config do runnable: variável de sessao que é usada apra recuperar o histórico dentro de runnable.
        config={"session_id": sessao},
    )
    print(f"Usuário: {pergunta}")
    print(f"IA: {resposta} \n")
