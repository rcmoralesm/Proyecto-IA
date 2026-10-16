try:
    x = 10
    y = 0
    z = x / y
except ZeroDivisionError:
    print("Error: División por cero no permitida.")

    try:
        numero = int("hola") #except ValueError:
        print(numero)
    except ValueError:
        print("Error: El valor ingresado no es un número válido.")
    try:
        texto = "Hola"
        num = 22
        frase = texto + num  # except TypeError:
    except TypeError:
        print("tipos de datos incompatibles para la concatenación.")
try:
    frutas = ["manzana", "banana", "naranja"]
    print(frutas[5]) # Esto generará un IndexError
except IndexError:
    print("Error: Índice fuera de rango.")

    estudiante = {
        "nombre": "Juan",
        "apellido": "Pérez",
    }
    print(estudiante["edad"])  # Esto generará un KeyError
except KeyError:
    print("Error: La clave 'edad' no existe en el diccionario.")