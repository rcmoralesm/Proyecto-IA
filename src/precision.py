from collections import Counter
from pipeline_limpieza import procesar_texto
from cliente import consultar_modelo
import json


def contar_coincidencias(
    tokens_referencia: list[str],
    tokens_respuesta: list[str],
) -> int:
    """Cuenta las coincidencias entre referencia y respuesta."""
    conteo_referencia = Counter(tokens_referencia)
    conteo_respuesta = Counter(tokens_respuesta)
    interseccion = conteo_referencia & conteo_respuesta
    return sum(interseccion.values())

def calcular_precision_cobertura_f1(
    tokens_referencia: list[str],
    tokens_respuesta: list[str],
) -> dict[str, float]:
    """Calcula precisión, cobertura y F1 de dos listas de tokens."""
    coincidencias = contar_coincidencias(
        tokens_referencia, tokens_respuesta
    )

    if not tokens_respuesta or not tokens_referencia:
        return {"precision": 0.0, "cobertura": 0.0, "f1": 0.0}

    precision = coincidencias / len(tokens_respuesta)
    cobertura = coincidencias / len(tokens_referencia)

    if precision + cobertura == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * cobertura / (precision + cobertura)

    resultado = {
        "precision": precision,
        "cobertura": cobertura,
        "f1": f1,
    }

    return resultado

def calcular_metricas(texto_referencia, texto_respuesta):
    tokens_referencia = procesar_texto(texto_referencia)
    tokens_respuesta = procesar_texto(texto_respuesta)
    
    return calcular_precision_cobertura_f1(
        tokens_referencia, tokens_respuesta
    )

casos = [
    #1
    (
    "U0255-87",
    "Lost communication with Instrument Pack (IPK)",
    ),
    #2
    (
	"U011187", 
     "Abnormal communication between OBC and BMS CAN (598 or 603 message Iost)"),
    #3
    (
    "IJ0424-62",
    "Signal comparison failure, VIN not equal to VIN in IPK",
    ),
    #4
    (
        "U0155-87",
        "Lost communication with Instrument Pack (IPK)",
    ),
    #5
    (
        "U0140-87",
        "Communication with Body Control Module (BCM) interrupted",
    ),
    #6
    (
        "U0210-OO",
        "ODO backup VIN code error",
    ),
    #7
    (
        "U025587",
        "FHM LIN message no receive",
    ),
    #8
    (
        "1-1011187",
        "Abnormal communication between OBC and BMS CAN",
    ),
    #9
    (
        "B1006-31",
        "FL sensor not receiving corresponding RF signal (travel distance in 10 minutes larger than 20kph)",
    ),
    #10
    (
        "BID81-14",
        "Rear right corner sensor signal line short to ground or open circuit",
    ),
	    #1
    (
        "Bl D82-76",
        "Rear left comer sensor aftershock time fault",
    ),
    #2
    (
	"U0126-87", 
     "Lost communication with Steering Angle Sensor (SAS)"),
    #3
    (
        "U0322-87",
        "Lost communication with Body Control Module (BCM)",
    ),
    #4
    (
        "U025587",
        "FHM LIN message no receive",
    ),
    #5
    (
        "U011187",
        "Lost Communication With BMS",
    ),
    #6
    (
        "U025587",
        "Lost Communication With IPK",
    ),
    #7
    (
        "U0424-62",
        "Signal comparison failure, VIN not equal to VIN in IPK",
    ),
]

resultados = []

for consulta, referencia in casos:
    respuesta = consultar_modelo(consulta, system_instruction="Responde en español con una definición breve, " \
    "en una sola oración de máximo 10 palabras.")
    
    metricas = calcular_metricas(referencia, respuesta)
    
    print("Consulta:", consulta)
    print("Respuesta:", respuesta)
    print("Métricas:", metricas)
    
    resultados.append({
        "consulta": consulta,
        "respuesta": respuesta,
        **metricas,
    })
    
resultados = sorted(resultados, key=lambda r: r["f1"])

with open(
    "resultados_metricas.json", "w", encoding="utf-8"
) as archivo:
    json.dump(resultados, archivo, indent=2, ensure_ascii=False)

def resumir_metricas(resultados):
    if not resultados:
        return {
            "precision_promedio": 0,
            "cobertura_promedio": 0,
            "f1_promedio": 0,
        }
    n = len(resultados)
    return {
        "precision_promedio": sum(
            r["precision"] for r in resultados
        ) / n,
        "cobertura_promedio": sum(
            r["cobertura"] for r in resultados
        ) / n,
        "f1_promedio": sum(r["f1"] for r in resultados) / n,
    }
    
print("Promedios")
print(resumir_metricas(resultados))
    
peores_casos = sorted(resultados, key=lambda r: r["f1"])

for caso in peores_casos[:3]:
    print(caso["consulta"], caso["f1"])
    
    
# referencia = procesar_texto(
#     "Python es un lenguaje de programación interpretado."
# )

# texto_respuesta = consultar_modelo("¿Qué es Python?",
#                                    system_instruction="Responde en español con una definición breve, en una sola oración de máximo 15 palabras. Sin listas, ejemplos ni introducciones.")

# respuesta = procesar_texto(texto_respuesta)
# resultado = calcular_precision_cobertura_f1(referencia, respuesta)

# print("Respuesta:", texto_respuesta)
# print("Tokens de referencia:", len(referencia))
# print("Tokens de respuesta:", len(respuesta))
# print(resultado)