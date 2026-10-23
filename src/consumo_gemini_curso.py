import os
import requests
from dotenv import load_dotenv

import time
import json
import re




load_dotenv()



  #funcion para armar la peticion
def armar_peticion(modelo,pregunta, system_instruction, response_schema):
     api_key = os.getenv("GEMINI_API_KEY")
     #modelo = "gemini-3.5-flash-lite"
     link_base="https://generativelanguage.googleapis.com/v1beta/models/"
     url = f"{link_base}{modelo}:generateContent?key={api_key}"
     body = {
         "systemInstruction": {
             "parts": [ {"text": system_instruction}]
            },
        "contents": 
             [{"parts": [{"text": pregunta}]}]
            }
     if response_schema is not None:
         body["generationConfig"] = {
             "responseMimeType": "application/json",
             "responseSchema": response_schema
         }
     return url, body

#armar la peticion, enviar la peticion y extraer el texto de la respuesta
  
def enviar_peticion(url, body):
    try:
     respuesta = requests.post(url, json=body, timeout=30)
    except requests.exceptions.connectionError:
        raise SystemExit("Error: No se pudo conectar al servidor. Verifica tu conexión a Internet.")
    except requests.exceptions.Timeout:
        raise SystemExit("Error: La solicitud ha excedido el tiempo de espera.")
    if respuesta.status_code != 200:
        raise SystemExit(f"Error {respuesta.status_code}: {respuesta.text}")
    try:
        return respuesta.json()
    except requests.exceptions.JSONDecodeError:
        raise SystemExit("la respuesta del servidor no llego.")

#funcion para extraer el texto de la respuesta
def extraer_texto(datos):#gemini
     try:
         return datos["candidates"][0]["content"]["parts"][0]["text"]
     except (KeyError, IndexError):
         raise RuntimeError("Error: no recibe el texto generado.")

def obtener_dato_de_prueba(pregunta): #pregunta = "Confirma la conexion"

    response_schema = {
        "type":"object",
        "properties": {
            "categoria": {"type":"string"},
            "confianza": {"type":"number"}
        },
        "required": ["categoria", "confianza"]
    }


    system_instruction = "Eres un asistente de ingeniería automotriz, que responde a " \
    "preguntas sobre fallas y errores de vehículos. Responde de manera clara y concisa, " \
    "proporcionando soluciones prácticas y pasos a seguir para resolver problemas automotrices. " \
    "Evita respuestas vagas o genéricas, y enfócate en brindar información útil y específica para ayudar al " \
    "usuario a solucionar su problema." \
    "Responde con un objeto JSON con Claves: 'categoria' y 'confianza'"

    url, body = armar_peticion("gemini-3.5-flash-lite",pregunta, system_instruction, response_schema) #obtiene url y body

    inicio = time.perf_counter() #Empezar el contador

    #url = resultado de armar_peticion
    #body = resultado de armar_peticion
    datos = enviar_peticion(url, body)

    fin = time.perf_counter() #Termina el contador
    latencia = fin - inicio
    print(f"Latencia: {latencia:.2f} segundos")

    costo = calcular_costo(datos, 0.00000075, 0.00000375)
    print(f"Costo de la petición: ${costo:.6f} USD")
    texto = extraer_texto(datos)
    datos_formateados = parsear_respuesta_json(texto, ["categoria", "confianza"])
    return datos_formateados
  

#def calcular_costo(datos: dict, precio_entrada: float, precio_salida: float) -> float:
def calcular_costo(datos, precio_entrada,precio_salida): 
    #datos = {dict... "usageMetadata": {"totalTokens": 100, "inputTokens": 60, "outputTokens": 40}}
    uso = datos["usageMetadata"]
    ...
    uso = { 
        "promptTokenCount": 11,
        "candidatesTokenCount": 100,
        "totalTokenCount": 680,
        "promptTokensDetails": [
            {
                "modality": "TEXT",
                "tokenCount": 11
            }
        ],
        "thoughtsTokenCount": 569,
        "serviceTier": "standard"
        }
    ...
    tokens_entrada = uso["promptTokenCount"]
    tokens_salida = uso["candidatesTokenCount"]
    tokens_razonamiento = uso["thoughtsTokenCount"] #revisar si existe este campo, si no existe poner 0s
    costo = (tokens_entrada * precio_entrada) + (tokens_salida * precio_salida) + (tokens_razonamiento * precio_salida)
    return costo    

def parsear_respuesta_json(texto, claves_requeridas=None):

    """
    claves_requeridas = ["categoria", "nivel"]
    """
    texto_limpio = texto.strip()
    texto_limpio = re.sub(r"^```(?:json)?\s*", "", texto_limpio) 
    texto_limpio = re.sub(r"\s*```$", "", texto_limpio)

    try:
        datos = json.loads(texto_limpio)
    except json.JSONDecodeError:  
        raise ValueError("Error al decodificar JSON")

    if claves_requeridas:
        """
        faltantes = []
        clave = "categoria"
        clave = "nivel"
        faltantes = ["nivel"]
        """
        faltantes = [clave for clave in claves_requeridas if clave not in datos]
        if faltantes:
            raise ValueError("la respuesta no tiene la estructura esperada." )
        return datos

try:
    print(obtener_dato_de_prueba("Maxus t60 2.0, Error ODB2 u1563-16"))
except (ValueError, RuntimeError, KeyError) as error:
    print("no se pudo obtener el texto generado:", error)