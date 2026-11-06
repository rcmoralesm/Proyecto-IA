from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool #herramientas
from langchain_classic.agents import (
    AgentExecutor,
    create_tool_calling_agent
)
from langchain_core.prompts import (
    ChatPromptTemplate, #me permite agregar system_intruction y user (human)
    MessagesPlaceholder
    )

load_dotenv()

modelo = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")

#Tool/herramienta es una funcion comun en python. 
# descripion en lenguaje natural sera lo que modelo lea (prompt) para decidir si elige o no esa herramnuienta
@tool
def buscar_en_documentacion(consulta:str) -> str:
    """
    Busca información relevante en la documentación interna del producto. Usar cuando la pregunta es sobre cómo
    funciona algo del sistema.
    """
    documentacion = {
        "reintentos": "El cliente reintenta hasta 3 veces ante un TimeoutError, con espera creciente.",
        "costos": "El costo se calcula a partir de totalTokenCount, según la tarifa vigente."
    }

    for clave, texto in documentacion.items():
        if clave in consulta.lower():
            return texto
    return "No se encontró información sobre esa consulta en la documentación."

@tool
def calcular(expresion: str) -> str:
    """Evalúa una expresión aritmética simple, como '340 + 215'. 
        Usar cuando la pregunta requiere un cálculo numérico.
    """
    permitido = set("0123456789+-*/().")
    if not set(expresion) <= permitido:
        return "Expresión no permitida."
    try:
        return str(eval(expresion))
    except Exception as e:
        return f"Error al evaluar la expresión: {e}"

heramientas = [buscar_en_documentacion, calcular] #lista de herramientas

#plantilla, con system instructions
prompt_agente = ChatPromptTemplate.from_messages([
    (
        "system", "Eres un asistente que responde preguntas usando las herramientas disponibles cuando las necesites."
    ),
    (
        "human", "{entrada}"
    ),
    MessagesPlaceholder("agent_scratchpad") 
    #El espacio donde LangChain va anotando, pasos/ciclos razonar-actual-observar, que herramientas llamos y que de volvieton
])

#agente: modelo, herramientas, promt formato

agente = create_tool_calling_agent(
modelo, heramientas, prompt_agente
)
#orquestador: es el que controla el ciclo entre razonar interactual observar

ejecutor_agente = AgentExecutor(
agent=agente,
tools=heramientas,
verbose=True, #imprime los pasos que va siguiendo
)

resultado = ejecutor_agente.invoke(
    {"entrada":"¿cuanto es 340+215?"}
)
print ("respuesta final:", resultado["output"])