# Límites de autonomía: Agente de diagnóstico de códigos OBD2

## Herramientas y nivel de riesgo

- validar_datos_vehiculo (marca, modelo, año, motor): bajo (solo verifica entradas; un dato mal validado puede llevar a una solución para otro motor)
- consultar_codigo_obd2: bajo (solo lectura; el riesgo es que el código tenga significados distintos según el fabricante)
- buscar_procedimiento_reparacion: medio (la fuente puede ser incorrecta, desactualizada o no corresponder a ese vehículo)
- generar_solucion: alto (el texto final es lo que el usuario ejecuta; un error puede dañar el vehículo o causar un accidente)
- recomendar_repuestos o enlaces de compra (si aplica): medio (costo para el usuario y posible sesgo comercial)

## Herramientas que requieren aprobación humana

- generar_solucion para códigos de sistemas críticos de seguridad (frenos/ABS, airbag, dirección, estabilidad, combustible, transmisión): una persona calificada revisa antes de entregar, o la respuesta se limita a "no conducir y acudir a un taller"
- Cualquier cambio en la base de códigos o procedimientos que usa el agente: revisión humana antes de publicarse
- recomendar_repuestos (si se implementa): aprobación de la lista de fuentes permitidas

## Riesgos asociados al proyecto

- Seguridad física: instrucciones para reparar frenos, airbag o combustible sin la capacitación ni las herramientas adecuadas
- Diagnóstico incorrecto: un código suele tener varias causas posibles, y presentar una sola como la solución lleva a cambiar piezas sin necesidad
- Alucinación: procedimientos, torques o piezas inventados que suenan creíbles
- Datos del vehículo erróneos o incompletos: mismo código, distinta causa según motor, año o versión
- Exceso de confianza: respuestas sin indicar incertidumbre ni alternativas
- Daño por borrar códigos o ignorar alertas, con vehículos que siguen circulando con una falla grave
- Responsabilidad: el usuario puede tomar la respuesta como diagnóstico profesional definitivo
- Fuentes desactualizadas o con derechos de autor (manuales de fabricante

## Revisión de trazas

- Frecuencia: semanal, más revisión inmediata ante cualquier cambio de instrucciones o de la base de conocimiento; además, muestreo de las respuestas sobre códigos críticos
- Qué se busca: bucles de llamadas repetidas, herramientas usadas fuera de su propósito, soluciones sin fuente que las respalde, soluciones que ignoran marca, año o motor ingresados, ausencia de advertencias en códigos críticos, respuestas con total certeza donde el código admite varias causas, intentos de saltarse la aprobación humana

## Qué hacer ante un comportamiento inesperado

1. Desactivar la entrega de soluciones para los códigos críticos (modo "consulte un taller") mientras se investiga.
2. Guardar la traza completa de la sesión y los datos ingresados.
3. Identificar la entrada que provocó la respuesta inesperada y qué fuente usó el agente.
4. Si hubo una respuesta peligrosa ya entregada, contactar al usuario afectado cuando sea posible.
5. Corregir instrucciones, fuentes o permisos y probar con un conjunto de códigos conocidos, incluidos los críticos.
6. Reactivar con aprobación humana en las respuestas de riesgo alto hasta confirmar que el problema se resolvió.