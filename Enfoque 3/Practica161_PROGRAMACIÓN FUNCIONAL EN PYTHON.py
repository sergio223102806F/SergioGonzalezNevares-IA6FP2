# =============================================
# PROGRAMACIÓN FUNCIONAL EN PYTHON
# =============================================

# ----------------------------
# 1. LISTAS (Estructuras de datos)
# ----------------------------
# Las listas son colecciones ordenadas y mutables
numeros = [1, 2, 3, 4, 5]  # Lista de números
frutas = ["manzana", "banana", "naranja"]  # Lista de strings

# ----------------------------
# 2. FUNCIONES (Ciudadanas de primera clase)
# ----------------------------
# Definición de función tradicional
def suma(a, b):
    """Suma dos números y devuelve el resultado"""
    return a + b

# Función que toma otra función como parámetro
def aplicar_funcion(func, x, y):
    """Aplica una función a dos argumentos"""
    return func(x, y)

# ----------------------------
# 3. FUNCIONES LAMBDA (Anónimas)
# ----------------------------
# Lambda para duplicar un número
doble = lambda x: x * 2

# Lambda para sumar dos números
sumar = lambda a, b: a + b

# ----------------------------
# 4. RECURSIVIDAD
# ----------------------------
# Función recursiva para calcular factorial
def factorial(n):
    """Calcula el factorial de n recursivamente"""
    if n == 0:  # Caso base
        return 1
    else:       # Caso recursivo
        return n * factorial(n - 1)

# Función recursiva para Fibonacci
def fibonacci(n):
    """Calcula el n-ésimo número de Fibonacci"""
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

# =============================================
# EJEMPLOS PRÁCTICOS
# =============================================

if __name__ == "__main__":
    print("\n=== LISTAS Y OPERACIONES FUNCIONALES ===")
    # Map: aplicar función a cada elemento
    print("Dobles:", list(map(doble, numeros)))
    
    # Filter: filtrar elementos
    print("Pares:", list(filter(lambda x: x % 2 == 0, numeros)))
    
    # Reduce: acumular valores (requiere importar functools)
    from functools import reduce
    print("Suma total:", reduce(lambda a, b: a + b, numeros))
    
    print("\n=== FUNCIONES Y LAMBDAS ===")
    print("Suma tradicional:", suma(5, 3))
    print("Suma con lambda:", sumar(5, 3))
    print("Aplicar función:", aplicar_funcion(suma, 10, 20))
    
    print("\n=== RECURSIVIDAD ===")
    print("Factorial de 5:", factorial(5))
    print("Fibonacci(6):", fibonacci(6))
    
    print("\n=== USO AVANZADO ===")
    # List comprehension (alternativa funcional a map/filter)
    cuadrados_pares = [x**2 for x in numeros if x % 2 == 0]
    print("Cuadrados de pares:", cuadrados_pares)
    
    # Función que devuelve otra función
    def crear_multiplicador(n):
        return lambda x: x * n
    
    duplicador = crear_multiplicador(2)
    print("Duplicar 15:", duplicador(15))