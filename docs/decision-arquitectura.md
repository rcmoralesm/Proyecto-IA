# Decisión de arquitectura: elección de modelo

Fecha de comparacion: Martes 20 de octubre del 2026
Nombre de la aplicacion: "scanner IA"
  
 ## Modelo elegido

  Elegi el modelo:
  mi mini aplicacion sirve para obtener fallas claras y precisas sobre los codigos de falla que entrega un scanner automotriz
  los requisitos que necesito cumplir son
que la IA permita recepcionar codigos escritos como imagenes con el diagnostico del scanner y entrege en un lenguaje siemple la respuesta

 ## Diagrama de arquitectura

 [diagrama de arquitecruta - (docs/diagrama_arquitectura.pdf)]
  
 ## Comparación de candidatos

Nombre: "gemini-3.1-flash-lite"
-

Precio_entrada: 0.00000075 

Precio_salida: 0.00000375

------------------------------
Nombre: "gemini-3.6-flash"
-

Precio_entrada: 0.00000010

Precio_salida: 0.00000030

------------------------------

Nombre": "gemini-3.8-flash"
-
Precio_entrada: 0.00000250

Precio_salida: 0.00001000

##Preguntas y/o condiciones:
-

Se realizo una sola pregunta ya que los modelos no estan contestando.

Pregunta: Maxus t60 2.0, Error ODB2 u1563-16

| Modelo | Intentos exitosos | Latencia promedio | Costo por respuesta | Estado |
|---|---|---|---|---|
| gemini-3.6-flash | 2 de 4 | 41,15 s | $0,000609 – $0,000733 | Respondió |
| gemini-3.1-flash-lite | 0 de 4 | n/d | n/d | Solo errores 429 y 500 |
| gemini-3.8-flash | 0 de 4 | n/d | n/d | Solo errores 429 y 500 |



    Fuente sobre las tarifas:
   https://ai.google.dev/gemini-api/docs/pricing?hl=es_419

 ## Justificación

Los fallos de los otros dos son del servidor (429 = límite de peticiones, 500 = error interno), no de la calidad del modelo. Por eso no puedo clasificarlos en respuesta, precio ni calidad: no hay datos.

Calidad de las dos respuestas de gemini-3.6-flash

Aquí hay un problema más serio: las dos respuestas se contradicen entre sí sobre qué significa el mismo código U1563-16.

Intento 1: dice que es el módulo de bujías de incandescencia (precalentamiento).
Intento 2: dice que es el sensor inteligente de batería (IBS) o el alternador.

Ambas suenan seguras y técnicas, pero no pueden ser las dos correctas.
  
 ## Alternativa descartada y por qué

recomendación
Repitir la prueba de los otros dos modelos cuando baje la carga del servidor. 
Corre más intentos del modelo que sí respondió y mide qué tan consistente es, porque hoy no lo es.
evitar respuestas en inglés.
Con estos datos, lo único que puedo decir es que gemini-3.6-flash es barato (menos de una milésima de dólar por consulta) pero lento (33–48 s) e inconsistente en el contenido.