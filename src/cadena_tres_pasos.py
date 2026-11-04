from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI #modelo de lenguaje de Google Gemini
from langchain_core.prompts import PromptTemplate #plantilla de prompt
from langchain_core.output_parsers import StrOutputParser #parsea la salida del modelo a texto
from langchain_core.prompts import ChatPromptTemplate  #plantilla incluyendo el rol del modelo e instrucciones

load_dotenv()

modelo = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")

#############PASO 1: EXTRACCION DE PUNTOS CLAVES##########################

plantilla_extraccion = PromptTemplate.from_template("lee Marca, Modelo, Motor y Error odb2, " \
"Responde de manera clara y concisa y devuelve solo sus 3 puntos claves: \n\n {texto}")

paso_extraccion = plantilla_extraccion | modelo | StrOutputParser()

texto_prueba = """Marca: maxus
Modelo: t60
Motor: d20
Error OBD2: U0140-87"""

# puntos = paso_extraccion.invoke({
#     "texto": texto_prueba
#     })
# print(puntos)

plantilla_simplificacion = PromptTemplate.from_template("" \
"simplifica el siguiente texto, manteniendo su significado: " \
"\n\n {puntos}")

#############PASO 1: EXTRACCION DE PUNTOS CLAVES##########################
#############PASO 2: SIMPLIFICACION DE PUNTOS CLAVES######################

paso_simplificacion = plantilla_simplificacion | modelo | StrOutputParser()

# simple = paso_simplificacion.invoke({
#     "puntos": puntos
# })
# print(simple)

#############PASO 2: SIMPLIFICACION DE PUNTOS CLAVES######################
#############PASO 3: FORMATO######################

plantilla_formato = PromptTemplate.from_template("Eres un ingeniería automotriz, que responde a " \
    "preguntas sobre fallas y errores de vehículos. Responde de manera clara y concisa y devuelve solo sus 3 puntos claves"
"\n\n {texto_simple}")

paso_formato = plantilla_formato | modelo | StrOutputParser()

# formato = paso_formato.invoke({
#     "texto_simple": simple
# })
# print(formato)

#############PASO 3: FORMATO######################

cadena_tres_pasos = (
                      plantilla_extraccion 
                    | modelo
                    | StrOutputParser()
                    | (lambda puntos: {"puntos": puntos})
                    | plantilla_simplificacion
                    | modelo
                    | StrOutputParser()
                    | (lambda simple: {"texto_simple": simple})
                    | plantilla_formato
                    | modelo
                    | StrOutputParser()
)

respuesta = cadena_tres_pasos.invoke({"texto": texto_prueba})
print(respuesta) 
