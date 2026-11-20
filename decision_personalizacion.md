# Decision de personalizacion

## 1. El problema
El clasificador de errores del cliente no responde con un formato consistente.

## 2. Resultado del metodo de decision
- RAG: 5 puntos
- PEFT: 4 puntos
- Fine-tuning completo: 3 puntos

## 3. Tecnica elegida y por que
RAG
1. Reducción directa del consumo de tokens y costos
Los manuales de taller, tablas de códigos OBD2 (P/B/C/U) y procedimientos específicos por motor ocupan mucho espacio. Si intentaras meter todo ese corpus en el system prompt o reenviarlo en cada consulta, gastarías tokens de entrada innecesariamente y saturarías el contexto. Con RAG,  divide el texto en fragmentos (chunks) y Chroma recupera solo los más relevantes (k=3) para esa consulta específica.

2. Menos "alucinaciones" y mayor precisión técnica
En diagnóstico automotriz, inventar un paso de prueba, un valor o un componente puede hacer perder tiempo o generar diagnósticos erróneos. Al instruir al modelo para que responda apoyándose en el contexto recuperado del corpus —y admita cuando el dato no está—, anclas la respuesta a la documentación que tú controlas.

3. Actualización inmediata sin reentrenar nada
Los catálogos de fallas, boletines técnicos o notas por marca/modelo/año/motor crecen con el tiempo. Con RAG (y un archivo externo como corpus_obd2.txt), basta con agregar o editar texto y volver a indexar los chunks en Chroma. Hacer fine-tuning cada vez que añades códigos o procedimientos sería lento, costoso y poco práctico para un proyecto iterativo.

4. Trazabilidad y control de la fuente
Cuando el diagnóstico proviene de un fragmento recuperado del corpus, sabes exactamente de qué nota o manual salió la recomendación. Esto facilita auditar respuestas, detectar vacíos en tu base de conocimiento y mejorar los chunks o el tamaño de ventana (chunk_size / chunk_overlap) según qué códigos consulten más los usuarios.

5. Buena sinergia con la memoria de sesión
El retriever aporta el conocimiento técnico puntual del código actual, mientras RunnableWithMessageHistory conserva el hilo de la conversación (el vehículo consultado, pruebas ya descartadas o preguntas de seguimiento). Separar ambos roles mantiene el prompt limpio y enfocado.

## 4. Que necesitarias para ejecutarla
Corpus ejemplo
Código P0300: Fallo de encendido aleatorio o en múltiples cilindros.
Significado: El PCM detecta fallos de combustión intermitentes o repetitivos en dos o más cilindros sin aislarse a uno solo.
Causas probables: 1) Bujías desgastadas, con calibración incorrecta o contaminadas; 2) Bobinas de encendido, cables de alta tensión o módulos de encendido defectuosos; 3) Inyectores sucios/obstruidos, baja presión de combustible o fuga de vacío en el múltiple de admisión.
Pasos de diagnóstico: 1) Leer datos congelados (*freeze frame*), RPM, carga del motor y compensaciones de combustible (LTFT/STFT); 2) Inspeccionar estado de bujías y bobinas (intercambiar bobinas entre cilindros si aplica); 3) Verificar presión de combustible y estanqueidad de vacío.
Solución recomendada y dificultad: Reemplazar bujías o bobinas dañadas, limpiar inyectores o corregir fugas de vacío según hallazgos. Dificultad: Media.