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
    print(estudiante["nombre"])  # Esto generará un KeyError
except KeyError:
    print("Error: La clave 'edad' no existe en el diccionario.")


def dividir():
    try:
        num1 = int(input("Ingrese el primer número: "))
        num2 = int(input("Ingrese el segundo número: "))
        resultado = num1 / num2
        print(f"El resultado de la división es: {resultado}")
    except ZeroDivisionError:
        print("Error: El segundo número no puede ser cero.")
    except ValueError:
        print("Error: solo numeros enteros son permitidos.")
    except Exception as error:
        print(f"Error inesperado: {error}")
    finally:
            print("Fin de la operación de división.")
dividir()
      
try:
    bebidas = ["coca-cola", "pepsi", "fanta"]
    bebidad_deseada = input("Ingrese el nombre de la bebida que desea: ")
    if bebidad_deseada not in bebidas:
        raise ValueError("La bebida ingresada no está disponible.")
    else:
        print(f"¡Disfruta tu {bebidad_deseada}!")
except ValueError as error:
    print(f"Error: {error}")
        