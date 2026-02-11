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


class Restaurante(BaseModel):
    cidade:str = Field("A cidade recomendada para visitar")
    restaurante:str = Field("O restaurante recomendado para visitar")


parseador_destino = JsonOutputParser(pydantic_object=Destino)
parseador_restaurante = JsonOutputParser(pydantic_object=Restaurante)

#Prompt Template para destino - cidade
prompt_destino = PromptTemplate(
template="""
Sugira uma única cidade dado o meu interesse por {interesse}.
{formato_de_saida}
""",
input_variables=["interesse"],

#Criamos uma váriavel intermediária, que não é enviada como um input mas sera usada como instrução do nosso formato de saída.
partial_variables= {"formato_de_saida": parseador_destino.get_format_instructions()}
)  

#Prompt Template para restaurante - pegar cidade da cadeia anterior

prompt_restaurante = PromptTemplate(
template=""" 
Sugira um restaurante para eu comer em um jantar com minha amada na cidade: {cidade}.
{formato de saida} 
""",
partial_variables= {"formato de saida": parseador_restaurante.get_format_instructions()})
                                  

modelo = ChatOpenAI(
    model="gpt-5-nano",
    temperature=1,
    api_key=api_key
)

# Cadeias

cadeia_destino = prompt_destino | modelo | parseador_destino

cadeia_restaurante = prompt_restaurante | modelo | parseador_restaurante

# Unificando cadeias

cadeia_main = (cadeia_destino | cadeia_restaurante)



# Agora só precisamos chamar a cadeia e passar um dicionário informando as váriaveis de entrada.
resposta = cadeia_main.invoke({
    
    "interesse" : "História, cultura e gastronomia, e que seja um destino de fácil acesso para brasileiros"
    
})


print(resposta)