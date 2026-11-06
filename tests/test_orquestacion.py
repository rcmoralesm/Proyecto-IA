import logging
from unittest.mock import MagicMock


from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda

from src.enrutamiento import *



def test_with_fallbacks_usa_respuesta_generica_ante_fallo_del_modelo():
    def fallar_a_proposito(datos):
        # Simula un fallo sin hacer una petición real.
        raise ConnectionError("simulado")
 
    cadena_falsa = RunnableLambda(fallar_a_proposito)
 
    # Misma construcción que cadena_robusta en enrutamiento.py.
    cadena_con_fallback = cadena_falsa.with_fallbacks(
        [respuesta_generica],
        exception_key="error",
    )
 
    resultado = cadena_con_fallback.invoke({
        "mensaje": "esto no funciona"
    })
 
    # Comprueba que respondió el fallback.
    assert resultado == (
        "Gracias por tu mensaje. Lo hemos recibido y estamos "
        "trabajando en ello. Te responderemos lo antes posible."
    )

def test_procesar_mensaje_seguro_no_propaga_excepciones():
    clasificacion_falsa = MagicMock()
 
    # En lugar de devolver una categoría, lanza una excepción.
    clasificacion_falsa.side_effect = ConnectionError("simulado")
 
    # Misma estructura que cadena_con_enrutamiento, sin el fallback.
    cadena_falsa = (
        RunnablePassthrough.assign(clasificacion=clasificacion_falsa)
        | bifurcacion
    )
 
    resultado = procesar_mensaje_seguro(
        cadena_falsa,
        "mensaje de prueba",
    )
 
    # El try/except debe entregar una respuesta.
    assert "no pudimos procesar" in resultado.lower()


def test_cadena_robusta_registra_la_causa_del_fallo(caplog, monkeypatch):
    # caplog es una herramienta de pytest para capturar registros.
    consultas = []
 
    def responder(_self, prompt, *_args, **_kwargs):
        consultas.append(prompt.to_string())
 
        if len(consultas) == 1:
            # La clasificación funciona y selecciona queja.
            return AIMessage(content="queja")
 
        # La segunda consulta, que genera la respuesta, falla.
        raise ConnectionError("simulado en la ruta")
 
    # Reemplaza las llamadas al modelo real de cadena_robusta.
    monkeypatch.setattr(ChatGoogleGenerativeAI, "invoke", responder)
 
    # Captura los registros WARNING y superiores de este módulo.
    with caplog.at_level(
        logging.WARNING,
        logger="src.enrutamiento",
    ):
        resultado = procesar_mensaje_seguro(
            cadena_robusta,
            "La app se cierra",
        )
 
    # Confirma que se llegó a la segunda consulta.
    assert len(consultas) == 2
 
    # Confirma que se eligió la ruta de quejas.
    assert "Responde esta queja" in consultas[1]
 
    # Confirma que actuó el fallback de cadena_robusta.
    assert resultado == (
        "Gracias por tu mensaje. Lo hemos recibido y estamos "
        "trabajando en ello. Te responderemos lo antes posible."
    )
 
    # Confirma que quedó registrada la causa del fallo.
    assert "simulado en la ruta" in caplog.text