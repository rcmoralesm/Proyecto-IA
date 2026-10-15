estudiante = {
    "nombre": "Ana",
    "edad": 24,
    "curso": {
        "nombre": "Python",
        "calificacion": 92
    },
    "tareas": [
        {
            "titulo": "Variables",
            "completada": True
        },
        {
            "titulo": "Consumo de APIs",
            "completada": False
        }
    ]
}

# El nombre de la estudiante
print(estudiante["nombre"]) 

# La calificación del curso
print(estudiante["curso"]["calificacion"])  

# El título de la segunda tarea
print(estudiante["tareas"][1]["titulo"]) 

# Si la primera tarea está completada
print(estudiante["tareas"][0]["completada"])