from unittest.mock import patch, Mock
import pytest

from src.consumo_gemini_curso import enviar_peticion, armar_peticion

######enviar_peticion######
def test_enviar_peticion_credencial_invalida():
    respuesta_falsa = Mock(status_code=401)
    with patch("src.consumo_gemini_curso.requests.post", return_value=respuesta_falsa):
        with pytest.raises(ValueError):
            enviar_peticion("https://ejemplo.invalid",{"pregunta": "test"})

def test_enviar_peticion_limite_de_uso():
    respuesta_falsa = Mock(status_code=429)
    with patch("src.consumo_gemini_curso.requests.post", return_value=respuesta_falsa):
        with pytest.raises(TimeoutError):
            enviar_peticion("https://ejemplo.invalid",{"pregunta": "test"})

def test_enviar_peticion_exito():
    respuesta_falsa = Mock(status_code=200)
    respuesta_falsa.json.return_value = {"texto": "respuesta simulada"}
    with patch("src.consumo_gemini_curso.requests.post", return_value=respuesta_falsa):
        resultado = enviar_peticion("https://ejemplo.invalid",{"pregunta": "test"})
        assert resultado == {"texto": "respuesta simulada"}
######enviar_peticion######

######con_reintento######
from cliente import con_reintento
from cliente import consultar_modelo
from unittest.mock import patch

def test_con_reintento():
    funcion = Mock(side_effect=TimeoutError("simulado"))
    with patch("cliente.time.sleep") as mock_sleep:
        with pytest.raises(TimeoutError, match="simulado"):
            con_reintento(funcion, intentos=3)
    assert funcion.call_count == 3   # hizo los 3 intentos
    assert mock_sleep.called         # esperó entre intentos


def test_consultar_modelo():
    error_simulado = TimeoutError("simulado")

    with patch("cliente.armar_peticion", return_value=("https://x", {})), \
         patch("cliente.con_reintento", side_effect=error_simulado) as mock_reintento, \
         patch("cliente.registrar_costo") as mock_costo:
        with pytest.raises(RuntimeError, match="no respondió") as info:
            consultar_modelo("pregunta de prueba")

    mock_reintento.assert_called_once()
    mock_costo.assert_not_called()
    assert info.value.__context__ is error_simulado

######con_reintento######


######registrar_costo######
import cliente

@pytest.fixture(autouse=True)
def reiniciar_costo_total():
    cliente.costo_total_sesion = 0
    yield

def test_registrar_costo_calcula_por_tokens():
    respuesta_falsa = {"usageMetadata": {"totalTokenCount": 1000}}

    costo = cliente.registrar_costo(respuesta_falsa)

    assert costo == pytest.approx(cliente.COSTO_POR_1000_TOKENS)
    assert cliente.costo_total_sesion == pytest.approx(cliente.COSTO_POR_1000_TOKENS)

def test_costo_total():
    assert cliente.registrar_costo({}) == 0
    assert cliente.costo_total_sesion == 0
######registrar_costo######