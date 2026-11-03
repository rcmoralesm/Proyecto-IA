from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI #modelo de lenguaje de Google Gemini
from langchain_core.prompts import PromptTemplate #plantilla de prompt
from langchain_core.output_parsers import StrOutputParser #parsea la salida del modelo a texto
from langchain_core.prompts import ChatPromptTemplate  #plantilla incluyendo el rol del modelo e instrucciones

load_dotenv()

#API_KEY = os.getenv("GEMINI_API_KEY")
#modelo = ChatGoogleGenerativeAI(model="gemini-3.6-flash", google_api_key=API_KEY)
modelo = ChatGoogleGenerativeAI(model="gemini-3.6-flash")
#respuesta = modelo.invoke("¿Cuál es la capital de Chile?")
#print(respuesta.content)

#f-strings
plantilla = PromptTemplate.from_template(
    "Explica el concepto de {tema} en un parrafo que comienza en {area}."
                                         )
#prompt =  plantilla.invoke({
#    "tema": "tokenizacion", "area": "procesamiento de texto"
#                        })
#print(prompt.text)

cadena_simple = plantilla | modelo | StrOutputParser()

respuesta = cadena_simple.invoke(
    {"tema": "embeddings", "area": "busqueda semántica"}
)
print(respuesta)
plantilla_conrol = ChatPromptTemplate.from_messages([
    ("system", "Eres un experto en el área correspondiente, vas a responder siempre con texto simple para el usuario."),
    ("human", "Explica el concepto de {tema} en un párrafo, para alguien que recien comienza en {area}")
])