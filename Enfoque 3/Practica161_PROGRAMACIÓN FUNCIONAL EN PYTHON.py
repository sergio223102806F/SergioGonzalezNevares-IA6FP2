# =============================================
# PROGRAMACIÓN FUNCIONAL EN PYTHON
# =============================================

# ----------------------------
# 1. LISTAS (Estructuras de datos)
# ----------------------------
# Las listas son colecciones ordenadas y mutables
numeros = [1, 2, 3, 4, 5]  # Lista de números # Crea una lista llamada 'numeros' con los elementos 1, 2, 3, 4 y 5
frutas = ["manzana", "banana", "naranja"]  # Lista de strings # Crea una lista llamada 'frutas' con nombres de frutas

# ----------------------------
# 2. FUNCIONES (Ciudadanas de primera clase)
# ----------------------------
# Definición de función tradicional
def suma(a, b):
    """Suma dos números y devuelve el resultado""" # Docstring: Descripción de la función
    return a + b # Suma 'a' y 'b' y devuelve el resultado

# Función que toma otra función como parámetro
def aplicar_funcion(func, x, y):
    """Aplica una función a dos argumentos""" # Docstring
    return func(x, y) # Llama a la función 'func' con los argumentos 'x' e 'y'

# ----------------------------
# 3. FUNCIONES LAMBDA (Anónimas)
# ----------------------------
# Lambda para duplicar un número
doble = lambda x: x * 2 # Crea una función anónima que multiplica un número por 2 y la asigna a 'doble'

# Lambda para sumar dos números
sumar = lambda a, b: a + b # Crea una función anónima que suma dos números y la asigna a 'sumar'

# ----------------------------
# 4. RECURSIVIDAD
# ----------------------------
# Función recursiva para calcular factorial
def factorial(n):
    """Calcula el factorial de n recursivamente""" # Docstring
    if n == 0:  # Caso base # Si 'n' es 0
        return 1 # Devuelve 1 (caso base)
    else:        # Caso recursivo # De lo contrario
        return n * factorial(n - 1) # Multiplica 'n' por el factorial de 'n-1'

# Función recursiva para Fibonacci
def fibonacci(n):
    """Calcula el n-ésimo número de Fibonacci""" # Docstring
    if n <= 1: # Si 'n' es menor o igual a 1
        return n # Devuelve 'n'
    else: # De lo contrario, calcula la suma de los dos números de Fibonacci anteriores
        return fibonacci(n - 1) + fibonacci(n - 2)

# =============================================
# EJEMPLOS PRÁCTICOS
# =============================================

if __name__ == "__main__":
    print("\n=== LISTAS Y OPERACIONES FUNCIONALES ===")
    # Map: aplicar función a cada elemento
    print("Dobles:", list(map(doble, numeros))) # Aplica la función 'doble' a cada elemento de 'numeros'

    # Filter: filtrar elementos
    print("Pares:", list(filter(lambda x: x % 2 == 0, numeros))) # Filtra los números pares de 'numeros'

    # Reduce: acumular valores (requiere importar functools)
    from functools import reduce # Importa la función 'reduce' del módulo 'functools'
    print("Suma total:", reduce(lambda a, b: a + b, numeros)) # Suma todos los elementos de 'numeros'

    print("\n=== FUNCIONES Y LAMBDAS ===")
    print("Suma tradicional:", suma(5, 3)) # Llama a la función 'suma'
    print("Suma con lambda:", sumar(5, 3)) # Llama a la función anónima 'sumar'
    print("Aplicar función:", aplicar_funcion(suma, 10, 20)) # Llama a 'aplicar_funcion' con la función 'suma'

    print("\n=== RECURSIVIDAD ===")
    print("Factorial de 5:", factorial(5)) # Llama a la función 'factorial'
    print("Fibonacci(6):", fibonacci(6)) # Llama a la función 'fibonacci'

    print("\n=== USO AVANZADO ===")
    # List comprehension (alternativa funcional a map/filter)
    cuadrados_pares = [x**2 for x in numeros if x % 2 == 0] # Crea una lista con los cuadrados de los números pares en 'numeros'
    print("Cuadrados de pares:", cuadrados_pares) # Imprime la lista de cuadrados pares

    # Función que devuelve otra función
    def crear_multiplicador(n):
        return lambda x: x * n # Devuelve una función anónima que multiplica un número por 'n'

    duplicador = crear_multiplicador(2) # Crea una función que duplica un número
    print(duplicador(5))

    print("Duplicar 15:", duplicador(15))