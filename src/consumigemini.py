import os
from pathlib import Path

import requests
from dotenv import load_dotenv

ruta_env = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(ruta_env, override=True)


def obtener_respuesta_gemini(pregunta):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Error: no se encontró GEMINI_API_KEY en el .env"

    modelo = "gemini-3.8-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}"

    body = {
        "contents": [
            {"parts": [{"text": pregunta}]}
        ]
    }

    respuesta = requests.post(url, json=body)
    datos = respuesta.json()

    if respuesta.status_code != 200:
        return f"Error {respuesta.status_code}: {datos['error']['message']}"

    return datos["candidates"][0]["content"]["parts"][0]["text"]


print(obtener_respuesta_gemini("cuenta un chiste"))