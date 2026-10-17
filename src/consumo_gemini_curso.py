import os
import requests
from dotenv import load_dotenv
  
load_dotenv()

  #funcion para armar la peticion
def armar_peticion(pregunta):
     api_key = os.getenv("GEMINI_API_KEY")
     modelo = "gemini-3.8-flash"
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

def obtener_dato_de_prueba(pregunta):
     url, body = armar_peticion(pregunta)
     datos = enviar_peticion(url, body)
     return extraer_texto(datos)

try:
    print(obtener_dato_de_prueba("si una adivinanza?"))
except (ValueError, RuntimeError) as error:
    print("no se pudo obtener el texto generado:", os.error)
