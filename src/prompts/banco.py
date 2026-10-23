BANCO_DE_PROMPTS = [
    {
        ##Prompt 1
        "nombre": "diagnostico_escaner",
        ##Instrucciones del sistema
        "system_instruction": (
            "Eres un técnico automotriz experto en diagnóstico de camionetas diésel. "
            "Responde SIEMPRE en español y solo con el JSON pedido. "
            "Interpreta el código de falla que te entregue el usuario. "
            "Si no estás seguro del significado exacto para esa marca y modelo, "
            "dilo con un nivel de confianza bajo; no inventes. "
            "El campo 'gravedad' va de 1 (leve) a 5 (crítico) y 'confianza' de 0 a 1."
        ),

        ##Ejemplo de usuario
        "ejemplo_usuario": "Código error U1563-16 en Maxus T60 2.0 diésel.",

        ##Claves esperadas en la respuesta
        "claves_requeridas": [
            "codigo",
            "significado",
            "causas_probables",
            "gravedad",
            "seguro_conducir",
            "confianza",
        ],
        ##respuesta esperada
        "response_schema": {
        ##definiciones de las respuestas esperadas
            "type": "OBJECT","properties": 
            {
                "codigo": {"type": "STRING"},
                "significado": {"type": "STRING"},
                "causas_probables": {"type": "ARRAY","items": {"type": "STRING"},},
                "gravedad": {"type": "NUMBER"},
                "seguro_conducir": {"type": "BOOLEAN"},
                "confianza": {"type": "NUMBER"},
            },
            "required": [
                "codigo",
                "significado",
                "causas_probables",
                "gravedad",
                "seguro_conducir",
                "confianza",
            ],
        },
    },
    {
        ##Prompt 2
        "nombre": "clasificacion_sintoma_cliente",
        "system_instruction": (
            "Eres el recepcionista técnico de un taller que restaura camionetas de trabajo. "
            "Clasifica el síntoma que describe el cliente. Responde SIEMPRE en español "
            "y solo con el JSON pedido. 'categoria' debe ser una de: motor, transmision, "
            "frenos, suspension, electrico, carroceria, otro. "
            "'nivel_urgencia' va de 1 (puede esperar) a 5 (detener el vehículo ya). "
            "No des un diagnóstico definitivo, solo orienta la revisión."
        ),
        "ejemplo_usuario": (
            "La camioneta humea blanco al encender en las mañanas frías, "
        ),
        "claves_requeridas": [
            "categoria",
            "nivel_urgencia",
            "sintomas_detectados",
            "primera_revision",
        ],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "categoria": {"type": "STRING"},
                "nivel_urgencia": {"type": "NUMBER"},
                "sintomas_detectados": {
                    "type": "ARRAY",
                    "items": {"type": "STRING"},
                },
                "primera_revision": {"type": "STRING"},
            },
            "required": [
                "categoria",
                "nivel_urgencia",
                "sintomas_detectados",
                "primera_revision",
            ],
        },
    },
    {
        ##Prompt 3
        "nombre": "checklist_inspeccion_restauracion",
        "system_instruction": (
            "Eres un jefe de taller que evalúa camionetas usadas para restaurarlas y revenderlas. "
            "Entrega una lista corta y priorizada de puntos a inspeccionar, "
            "pensando en bajo costo y en un equipo de cinco personas. "
            "'riesgo_compra' va de 1 (bajo) a 5 (alto). No inventes datos del vehículo."
        ),
        "ejemplo_usuario": (
            "Llegó una camioneta minera de doble cabina, 2021, 80.000 km, "
            "con uso en faena de altura y polvo. Quiero restaurarla para reventa."
        ),
        "claves_requeridas": [
            "vehiculo",
            "puntos_criticos",
            "riesgo_compra",
            "recomendacion",
        ],
        "response_schema": {"type": "OBJECT",
            "properties": {
                "vehiculo": {"type": "STRING"},
                "puntos_criticos": {"type": "ARRAY",
                "items": {"type": "STRING"},
                },
                "riesgo_compra": {"type": "NUMBER"},
                "recomendacion": {"type": "STRING"},
            },
            "required": [
                "vehiculo",
                "puntos_criticos",
                "riesgo_compra",
                "recomendacion",
            ],
        },
    },
    
]