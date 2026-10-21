import os
import requests
from dotenv import load_dotenv

import time
  
load_dotenv()



  #funcion para armar la peticion
def armar_peticion(pregunta):
     api_key = os.getenv("GEMINI_API_KEY")
     modelo = "gemini-3.5-flash-lite"
     link_base="https://generativelanguage.googleapis.com/v1beta/models/"
     url = f"{link_base}{modelo}:generateContent?key={api_key}"
     body = {
         "contents": 
             [{"parts": [{"text": pregunta}]}
              ]
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
    url, body = armar_peticion(pregunta) #obtiene url y body

    inicio = time.perf_counter() #Empezar el contador

    #url = resultado de armar_peticion
    #body = resultado de armar_peticion
    datos = enviar_peticion(url, body)

    fin = time.perf_counter() #Termina el contador
    latencia = fin - inicio
    print(f"Latencia: {latencia:.2f} segundos")

    costo = calcular_costo(datos, 0.00000075, 0.00000375)
    print(f"Costo de la petición: ${costo:.6f} USD")
    return extraer_texto(datos)

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


try:
    print(obtener_dato_de_prueba("Maxus t60 2.0 Error ODB2 u1563-16"))
except (ValueError, RuntimeError) as error:
    print("no se pudo obtener el texto generado:", os.error)
