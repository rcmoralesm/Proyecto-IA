
def recomendar_estrategia(respuestas):
    puntos = {"RAG": 0, "Fine-tuning completo": 0, "PEFT": 0}

    if respuestas["informacion_cambia_seguido"]:
        puntos["RAG"] += 3
    if respuestas["problema_de_formato_o_tono"]:
        puntos["PEFT"] += 2
        puntos["Fine-tuning completo"] += 1
    if respuestas["dataset_grande_y_de_calidad"]:
        puntos["Fine-tuning completo"] += 2
        puntos["PEFT"] += 1
    if respuestas["presupuesto_limitado_o_iterar_rapido"]:
        puntos["RAG"] += 2
        puntos["PEFT"] += 1
    if respuestas["necesita_multiples_variantes"]:
        puntos["PEFT"] += 2

    maximo = max(puntos.values())
    ganadoras = [tecnica for tecnica, p in puntos.items() if p == maximo]
    return puntos, ganadoras
 
 
# EJEMPLO comentado (no lo uses tal cual): asi luce el diccionario ya respondido
# para el clasificador de errores del cliente de las lecciones anteriores.
# Cada valor es True o False, y al lado queda anotada la evidencia que lo sustenta.
#
# respuestas_mi_caso = {
#     "informacion_cambia_seguido": False,        	# los tipos de error casi no cambian
#     "problema_de_formato_o_tono": True,         	# 7 de 20 respuestas no traen el JSON esperado
#     "dataset_grande_y_de_calidad": True,        	# 200 ejemplos etiquetados y revisados
#     "presupuesto_limitado_o_iterar_rapido": False,  # hay presupuesto y no hay urgencia
#     "necesita_multiples_variantes": False,      	# un solo clasificador para todo el sistema
# }
 
# Tu turno: reemplaza None por True o False en cada clave, apoyandote en la tabla de arriba.
respuestas_mi_caso = {
	"informacion_cambia_seguido": True,  # True/False, sobre tu propio proyecto
	"problema_de_formato_o_tono": True,
	"dataset_grande_y_de_calidad": True,
	"presupuesto_limitado_o_iterar_rapido": True,
	"necesita_multiples_variantes": False,
}
 
if any(valor is None for valor in respuestas_mi_caso.values()):
	raise SystemExit("Completa las cinco respuestas con True o False antes de continuar.")
 
puntos, ganadoras = recomendar_estrategia(respuestas_mi_caso)
print(puntos)
print("candidatas:", ganadoras)


def generar_esqueleto_decision(problema, puntos, ganadoras):
	empate = len(ganadoras) > 1
	lineas = []
	lineas.append("# Decision de personalizacion")
	lineas.append("")
	lineas.append("## 1. El problema")
	lineas.append(problema)
	lineas.append("")
	lineas.append("## 2. Resultado del metodo de decision")

	for tecnica, p in sorted(puntos.items(), key=lambda x: -x[1]):
		lineas.append(f"- {tecnica}: {p} puntos")
	if empate:
		lineas.append("")
		lineas.append(f"**Empate entre: {', '.join(ganadoras)}**")
	lineas.append("")
	lineas.append("## 3. Tecnica elegida y por que")
	if empate:
		lineas.append(
			"[COMPLETAR: el puntaje no resolvio el empate solo -- "
			"justifica aqui con criterio propio]"
		)
	else:
		lineas.append(f"[COMPLETAR: por que {ganadoras[0]} responde mejor a este caso]")
	lineas.append("")
	lineas.append("## 4. Que necesitarias para ejecutarla")
	lineas.append(
		"[COMPLETAR: corpus faltante, o cantidad de ejemplos etiquetados que faltan]"
	)
	return "\n".join(lineas)
 
 
esqueleto = generar_esqueleto_decision(
	# Reemplaza este texto por la descripcion de tu propio problema
	"El clasificador de errores del cliente no responde con un formato consistente.",
	puntos,
	ganadoras,
)
print(esqueleto)
 
with open("decision_personalizacion.md", "w", encoding="utf-8") as f:
	f.write(esqueleto)