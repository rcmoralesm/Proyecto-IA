from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI #modelo de lenguaje de Google Gemini
from langchain_core.prompts import PromptTemplate #plantilla de prompt
from langchain_core.output_parsers import StrOutputParser #parsea la salida del modelo a texto
from langchain_core.prompts import ChatPromptTemplate  #plantilla incluyendo el rol del modelo e instrucciones

load_dotenv()

modelo = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

#############PASO 1: EXTRACCION DE PUNTOS CLAVES##########################

plantilla_extraccion = PromptTemplate.from_template("lee el siguiente texto y devuelve solo sus 3 puntos claves, " \
"uno por linea, sin desarrollarlos: \n\n {texto}")

paso_extraccion = plantilla_extraccion | modelo | StrOutputParser()

texto_prueba=("Los modelos de lenguaje grandes generan texto "

    "prediciendo un token a la vez, basándose en el "

    "texto que ya generaron antes. Cada token puede "

    "ser una palabra completa, parte de una palabra, "

    "o un signo de puntuación. Antes de que el modelo "

    "genere una respuesta, el texto de entrada se "

    "divide en tokens, un proceso llamado tokenización.")

puntos = paso_extraccion.invoke({
    "texto": texto_prueba
    })
print(puntos)

plantilla_simplificacion = PromptTemplate.from_template("" \
"simplifica el siguiente texto, manteniendo su significado: " \
"\n\n {puntos}")

#############PASO 1: EXTRACCION DE PUNTOS CLAVES##########################
#############PASO 2: SIMPLIFICACION DE PUNTOS CLAVES######################

paso_simplificacion = plantilla_simplificacion | modelo | StrOutputParser()

simple = paso_simplificacion.invoke({
    "puntos": puntos
})
print(simple)

#############PASO 2: SIMPLIFICACION DE PUNTOS CLAVES######################
#############PASO 3: FORMATO######################

plantilla_fortmato = PromptTemplate.from_template("Convierte este texto en una lista de viñetas markdows de maximo 3 ñineas, sin introduccion: " \
"\n\n {texto_simple}")

paso_formato = plantilla_fortmato | modelo | StrOutputParser()

formato = paso_formato.invoke({
    "texto_simple": simple
})
print(formato)

#############PASO 3: FORMATO######################