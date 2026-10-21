import os
import requests
from pathlib import Path
from dotenv import load_dotenv

import time

load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)

LINK_BASE = "https://generativelanguage.googleapis.com/v1beta/models/"
INTENTOS = 4

# modelos a probar y su precio por token (entrada, salida)
# OJO: verifica nombres y precios en la tabla oficial de Google
PRECIO_ENTRADA = 0.00000010  # el valor real de la página de precios
PRECIO_SALIDA = 0.00000030
PRECIOS = {
    "gemini-3.1-flash-lite": (0.00000025, 0.0000015),
    "gemini-3.5-flash-lite": (0.0000003, 0.0000025),
    "gemini-3.6-flash": (0.00000075, 0.00000375),
}


#funcion para armar la peticion
def armar_peticion(pregunta, modelo):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("No se encontró GEMINI_API_KEY en el .env")
    url = f"{LINK_BASE}{modelo}:generateContent?key={api_key}"
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
    except requests.exceptions.ConnectionError:
        raise RuntimeError("Error: No se pudo conectar al servidor. Verifica tu conexión a Internet.")
    except requests.exceptions.Timeout:
        raise RuntimeError("Error: La solicitud ha excedido el tiempo de espera.")
    if respuesta.status_code != 200:
        raise RuntimeError(f"Error {respuesta.status_code}: {respuesta.text}")
    try:
        return respuesta.json()
    except requests.exceptions.JSONDecodeError:
        raise RuntimeError("la respuesta del servidor no llego.")


#funcion para extraer el texto de la respuesta
def extraer_texto(datos):#gemini
    try:
        return datos["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise RuntimeError("Error: no recibe el texto generado.")


#def calcular_costo(datos: dict, precio_entrada: float, precio_salida: float) -> float:
def calcular_costo(datos, precio_entrada, precio_salida):
    #datos = {dict... "usageMetadata": {"totalTokens": 100, "inputTokens": 60, "outputTokens": 40}}
    uso = datos.get("usageMetadata", {})
    # ejemplo de cómo viene "usageMetadata" (solo referencia, no se asigna):
    # uso = {
    #     "promptTokenCount": 11,
    #     "candidatesTokenCount": 100,
    #     "totalTokenCount": 680,
    #     "promptTokensDetails": [
    #         {
    #             "modality": "TEXT",
    #             "tokenCount": 11
    #         }
    #     ],
    #     "thoughtsTokenCount": 569,
    #     "serviceTier": "standard"
    # }
    tokens_entrada = uso.get("promptTokenCount", 0)
    tokens_salida = uso.get("candidatesTokenCount", 0)
    tokens_razonamiento = uso.get("thoughtsTokenCount", 0) #revisar si existe este campo, si no existe poner 0s
    costo = (tokens_entrada * precio_entrada) + (tokens_salida * precio_salida) + (tokens_razonamiento * precio_salida)
    return costo


def medir_modelo(pregunta, modelo):
    precio_entrada, precio_salida = PRECIOS[modelo]

    latencias = []
    for i in range(INTENTOS):
        url, body = armar_peticion(pregunta, modelo)
        inicio = time.perf_counter() #empieza el contador de tiempo
        respuesta_json = enviar_peticion(url, body)
        fin = time.perf_counter() #termina el contador de tiempo
        latencias.append(fin - inicio)
        print(f"Intento {i + 1}: {latencias[-1]:.2f} segundos")
        time.sleep(1) #pausa para no pasar el límite del plan gratuito

    latencia_promedio = sum(latencias) / len(latencias)
    print(f"Latencia promedio: {latencia_promedio:.2f} segundos")

    costo = calcular_costo(respuesta_json, precio_entrada, precio_salida)
    print(f"Costo de la última petición: {costo:.6f} USD")

    return latencia_promedio, costo, extraer_texto(respuesta_json)


def probar_modelos(pregunta):
    resultados = []
    for modelo in PRECIOS:
        print(f"\n=== Modelo: {modelo} ===")
        try:
            latencia, costo, texto = medir_modelo(pregunta, modelo)
            print(texto)
            resultados.append((modelo, latencia, costo, "OK"))
        except (ValueError, RuntimeError) as error:
            # si un modelo falla, se registra y se sigue con el siguiente
            print("no se pudo obtener el texto generado:", error)
            resultados.append((modelo, None, None, "ERROR"))

    print("\n=== Resumen ===")
    print(f"{'Modelo':<28}{'Latencia prom. (s)':>20}{'Costo (USD)':>14}  Estado")
    for modelo, latencia, costo, estado in resultados:
        l = f"{latencia:.2f}" if latencia is not None else "-"
        c = f"{costo:.6f}" if costo is not None else "-"
        print(f"{modelo:<28}{l:>20}{c:>14}  {estado}")


if __name__ == "__main__":
    probar_modelos("Maxus t60 2.0 Error ODB2 u1563-16?")