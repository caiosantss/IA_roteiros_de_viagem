from langchain.tools import tool
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage, ToolMessage
from langchain.tools import BaseTool
from rich import print
from dotenv import load_dotenv
from pydantic import SecretStr
import os


# 1 - Criar as Ferramentas

# Com o decorador tool, a função vira uma ferramenta da classe StructuredTool, que é uma subclasse de BaseTool.
@tool
def multiply(a: float, b:float) -> float: 
    # Docstring = Description da @tool
    """ Use this tool when you need to multiply two numbers (a and b) and get the result.
    Args: 
        a: Float multiplicand.
        b: Float multiplier.
        
        Returns:
        The product of a and b (a * b) as a float.
    """
    return a * b

# 2 - Criar o modelo de linguagem

load_dotenv() # Carrega as variáveis de ambiente do arquivo .env
api_key = os.getenv("GROQ_API_KEY") # Cria instancia da key do modelo que queremos.

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=SecretStr(api_key or "")
)

#3 - Criando manualmente a cadeia de mensagens para entender como funciona por baixo dos panos

system_message = SystemMessage(content="You are a helpful assistant. You have access to tools, when user ask something check if there is a tool that can help with the request and use it.")

human_message = HumanMessage(content="Olá, sou Caio. Pode me dizer quanto é 5 multiplicado por 2?")

messages: list[BaseMessage] = [system_message, human_message]

# Segundo llm instanciado com tools vinculadas, pega o mesmo llm criado anteriormente e vincula as ferramentas. 
tools: list[BaseTool] = [multiply]
#LLM chama a tool pelo nome somente, então criamos um dict com nome - ferramenta
tools_by_name = {tool.name: tool for tool in tools}
llm_with_tools = llm.bind_tools(tools)

#Enviamos ma mensagem especificamente para o llm com tools
llm_response = llm_with_tools.invoke(messages)
messages.append(llm_response)

#4 - Checar se a LLM está chamando a ferramenta
if isinstance(llm_response, AIMessage) and getattr(llm_response, "tool_calls", None):
    # Se entrar, significa que encontrou a lista de chamadas "tool_calls", queremos saber a última chamada da ferramenta para a tool
    call = llm_response.tool_calls[-1]
    name, args, id_ = call["name"], call["args"], call["id"]
    
    try:
        # Se a llm chamar o nome correto da ferramenta -> chamamos a tool e passamos os argumentos(parametros) -> coletamos o resultado em content.
        content = tools_by_name[name].invoke(args)
        status = "success"
    except (KeyError, IndexError, TypeError) as error:
        content = f"Please, fix the error: {error}"
        status = "error"
    
    #Criamos uma tool response: Aqui é onde nós criamos a chamada e a resposta para a IA, e mandamos de volta de modo que ela possa entender o resultado.
    tool_message = ToolMessage(content=content, tool_call_id=id_, status=status)
    messages.append(tool_message)
    
    llm_response = llm_with_tools.invoke(messages)
    messages.append(llm_response)
    
print(messages)