import json
from os import error
import time
from prompts.banco import BANCO_DE_PROMPTS
from consumo_gemini_curso import armar_peticion, enviar_peticion, extraer_texto, parsear_respuesta_json

registro = {}

try:

    for prompt in BANCO_DE_PROMPTS:
            exitos = 0
            intentos = 2
            for intento in range(intentos):
                url, body = armar_peticion(
                    "gemini-3.5-flash-lite", 
                    prompt["ejemplo_usuario"], 
                    prompt["system_instruction"],
                    prompt["response_schema"]
                )
                respuesta = enviar_peticion(url, body)
                texto = extraer_texto(respuesta)

    try:
            datos = parsear_respuesta_json(texto, prompt ["claves_requeridas"])
            exitos += 1 #exitos++

    except ValueError as error:
                print(f"intento {intento + 1} falló:{error}")
    time.sleep(1)
        
    print(f"{prompt["nombre"]}:{exitos}/{intentos} respuestas validas")
    registro[prompt["nombre"]] = {"exitos": exitos, "intentos": intentos}
    #cuando termine de recorrer los prompts quiero guardar esa info en registro_resultados.json
    with open("src/prompts/registro_resultados.json", "w", encoding="utf-8") as archivo:
        json.dump(registro, archivo, indent=2, ensure_ascii=False)   


except (ValueError, RuntimeError) as error:
    print("no se pudo completar la operacion:", error)
