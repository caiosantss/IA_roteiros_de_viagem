from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain.globals import set_debug
from pydantic import Field, BaseModel, SecretStr
from dotenv import load_dotenv
import os


#Ativando modo debug -> True

set_debug(True)

load_dotenv()
raw_api_key = os.getenv("OPENAI_API_KEY")

if raw_api_key is None:
    raise ValueError("Api Key not found in .env file")


api_key = SecretStr(raw_api_key)


#Defininfo um modelo de dados (base) para a resposta. Um Schema do pydantic.
class Destino(BaseModel):
    cidade:str = Field("A cidade recomendada para visitar")
    motivo:str = Field("O motivo pelo qual a cidade é recomendada")


parseador = JsonOutputParser(pydantic_object=Destino)


prompt_cidade = PromptTemplate(
template="""
Sugira uma única cidade dado o meu interesse por {interesse}.
{formato_de_saida}
""",
input_variables=["interesse"],

#Criamos uma váriavel intermediária, que não é enviada como um input mas sera usada como instrução do nosso formato de saída.
partial_variables= {"formato_de_saida": parseador.get_format_instructions()}
)  
                                  

modelo = ChatOpenAI(
    model="gpt-5-nano",
    temperature=1,
    api_key=api_key
)

# Criando uma chain com LCEL, o que deixa o código mais modular.
cadeia = prompt_cidade | modelo | parseador

# Agora só precisamos chamar a cadeia e passar um dicionário informando as váriaveis de entrada.
resposta = cadeia.invoke({
    
    "interesse" : "História, cultura e gastronomia, e que seja um destino de fácil acesso para brasileiros"
    
})


# Como criamos uma cadeia com StrOutPutParser, a resposta já é uma string, então podemos imprimir diretamente.
print(resposta)