from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI #modelo de lenguaje de Google Gemini
from langchain_core.prompts import PromptTemplate #plantilla de prompt
from langchain_core.output_parsers import StrOutputParser #parsea la salida del modelo a texto
from langchain_core.runnables import (RunnableBranch, RunnablePassthrough, RunnableLambda) #Bifurcaciones/Branches/Ramificaciones

import logging #genera archivos de log con errores y advertencias

logging.basicConfig( 
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='errores.log', 
    filemode='a',
    encoding='utf-8',
    force=True
)

logger = logging.getLogger(__name__)

load_dotenv()
modelo = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")

plantilla_clasificacion = PromptTemplate.from_template(
    "Clasifica el siguiente mensaje de soporte en una sola palabra:" 
    "pregunta, queja o sugerencia. Responde en un solo parrafo:  \n\n {mensaje}"
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
    PromptTemplate.from_template("responde esta pregunta tecnica con precision, en un solo parrafo : \n\n {mensaje}")
    | modelo
    | StrOutputParser()
)


cadena_queja = (
    PromptTemplate.from_template ("Responde esta queja con empatía, reconociendo el problema antes de ofrecer una solución, en un solo parrafo : \n\n {mensaje}")
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


def fallback_con_log(x):
    logger.warning("cadena principal falló, api, tokens o modelo no disponible, se ejecuta fallback, error  : %s", x.get("error"))
    return "Gracias por tu mensaje. Lo hemos recibido y estamos trabajando en ello. Te responderemos lo antes posible."

respuesta_generica = RunnableLambda(
    fallback_con_log
)

cadena_robusta = cadena_con_enrutamiento.with_fallbacks([respuesta_generica], exception_key="error")



def procesar_mensaje_seguro (cadena, mensaje):
    try:
        return cadena.invoke({"mensaje": mensaje})
    except Exception as error:
        logger.error("error al procesar el mensaje: %s", error)
        return "no pudimos procesar tu mensaje. Por favor, intenta de nuevo más tarde."

if __name__ == "__main__": #solamente se ejecuta si se ejecuta el archivo directamente, no si se importa como módulo
    mensaje = "Error U0140-87, maxus t60 d20"
    print(procesar_mensaje_seguro(cadena_robusta, mensaje))