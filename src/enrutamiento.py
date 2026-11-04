from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI #modelo de lenguaje de Google Gemini
from langchain_core.prompts import PromptTemplate #plantilla de prompt
from langchain_core.output_parsers import StrOutputParser #parsea la salida del modelo a texto
from langchain_core.runnables import (RunnableBranch, RunnablePassthrough) #Bifurcaciones/Branches/Ramificaciones

load_dotenv()
modelo = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")

plantilla_clasificacion = PromptTemplate.from_template(
    "Clasifica el siguiente mensaje de soporte en una sola palabra:" 
    "pregunta, queja o sugerencia. Responde en una sola palabra \n\n {mensaje}"
    )

paso_clasificacion = (
    plantilla_clasificacion 
    | modelo 
    | StrOutputParser()
    | (lambda texto: texto.strip().lower())
    )

#mensaje_prueba = "mi telefono no enciende"
#clasificacion = paso_clasificacion.invoke({"mensaje":mensaje_prueba})

cadena_pregunta = (
    PromptTemplate.from_template("responde esta pregunta tecnica con precision: \n\n {mensaje}")
    | modelo
    | StrOutputParser()
)


cadena_queja = (
    PromptTemplate.from_template ("Responde esta queja con empatía, reconociendo el problema antes de ofrecer una solución: \n\n {mensaje}")
    | modelo
    | StrOutputParser()
)

cadena_sugerencia = (
    PromptTemplate.from_template ("Responde a esta sugerencia con gratitud y consideración, en un solo parrafo \n\n {mensaje}")
    | modelo
    | StrOutputParser()
)

# caminos = runnableBranch(
#     (condicion_1, rama_1),#if
#     (condicion_2, rama_2),#elif
#     (condicion_3, rama_3),#elif
#     rama_por_defecto #else
# ) #cada condicion debe ser una funcion; suele ser un lambda que recibe un diccionario y devuelve un booleano. Cada rama debe ser
#  un Runnable, que puede ser una cadena de runnables.

bifurcacion = RunnableBranch(
    (lambda x: x["clasificacion"] == "queja", cadena_queja), #if x["clasificacion"] == "queja", ejecuta cadena_queja
    (lambda x: x["clasificacion"] == "sugerencia", cadena_sugerencia), #elif x["clasificacion"] == "sugerencia", ejecuta cadena_sugerencia
    cadena_pregunta #else: cadena_pregunta, si no es ninguna de las anteriores, devuelve el mensaje original
    )

cadena_con_enrutamiento = (
    RunnablePassthrough.assign(clasificacion=paso_clasificacion) #pasa el mensaje original al siguiente paso
    | bifurcacion #ejecuta la bifurcacion, que devuelve la respuesta correspondiente    
    )

resultado = cadena_con_enrutamiento.invoke(
    {"mensaje": "deberian tener mas agentes"}
)

print(resultado)