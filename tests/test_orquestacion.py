from unittest.mock import MagicMock

from langchain_core.runnables import RunnableLambda
from langchain_google_genai import ChatGoogleGenerativeAI #modelo de lenguaje de Google Gemini

from enrutamiento import (
    cadena_pregunta,
    cadena_queja,
    cadena_sugerencia,
    fallback_con_log,
    respuesta_generica,
    procesar_mensaje_seguro,

)

def test_falla_de_api_activa_el_fallback():
    """La API se cae desde la primera llamada (la clasificación)."""
 
    def modelo_caido(_entrada):
        raise TimeoutError("API no disponible")
 
    modelo = cargar_modulo(RunnableLambda(modelo_caido))
 
    respuesta = modelo.procesar_mensaje_seguro(
        modelo.cadena_robusta, "Error U0140-87, maxus t60 d20"
    )
 
    assert respuesta.startswith(MENSAJE_FALLBACK)