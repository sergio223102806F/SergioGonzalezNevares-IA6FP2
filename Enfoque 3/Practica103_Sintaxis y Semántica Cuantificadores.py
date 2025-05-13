# -*- coding: utf-8 -*-                                                     # Define la codificación de caracteres del archivo como UTF-8
"""
Created on Sun Apr 27 15:39:36 2025                                         # Indica la fecha y hora de creación del archivo
                                                                           #
@author: elvin                                                              # Define el autor del archivo
"""

"""
Este código muestra ejemplos de cómo trabajar con cuantificadores universales y existenciales
en Python, tanto para listas como para conjuntos. Los cuantificadores son conceptos fundamentales
en lógica matemática que nos permiten expresar afirmaciones sobre "todos" o "algunos" elementos
de un conjunto.
"""

def cuantificador_universal(conjunto, condicion):                           # Define una función llamada cuantificador_universal
    """
    Implementa el cuantificador universal (∀): Verifica si TODOS los elementos del conjunto
    satisfacen la condición dada.
    
    Args:
        conjunto (iterable): Colección de elementos a verificar
        condicion (function): Función que toma un elemento y devuelve True/False
    
    Returns:
        bool: True si todos los elementos satisfacen la condición, False en caso contrario
    """
    return all(condicion(x) for x in conjunto)                              # Retorna True si la función condición devuelve True para todos los elementos del conjunto

def cuantificador_existencial(conjunto, condicion):                         # Define una función llamada cuantificador_existencial
    """
    Implementa el cuantificador existencial (∃): Verifica si ALGÚN elemento del conjunto
    satisface la condición dada.
    
    Args:
        conjunto (iterable): Colección de elementos a verificar
        condicion (function): Función que toma un elemento y devuelve True/False
    
    Returns:
        bool: True si al menos un elemento satisface la condición, False en caso contrario
    """
    return any(condicion(x) for x in conjunto)                              # Retorna True si la función condición devuelve True para al menos un elemento del conjunto

def ejemplos():                                                             # Define una función llamada ejemplos
    """
    Ejemplos prácticos de uso de los cuantificadores con diferentes tipos de datos
    y condiciones.
    """
    
    # Ejemplo 1: Verificar si todos los números en una lista son positivos    # Comentario del Ejemplo 1
    numeros = [2, 4, 6, 8, 10]                                              # Define una lista de números
    todos_positivos = cuantificador_universal(numeros, lambda x: x > 0)      # Aplica el cuantificador universal para verificar si todos los números son positivos
    print(f"¿Todos los números {numeros} son positivos? {todos_positivos}") # Imprime el resultado del Ejemplo 1
    
    # Ejemplo 2: Verificar si algún número en una lista es par            # Comentario del Ejemplo 2
    numeros2 = [1, 3, 5, 7, 8, 9]                                           # Define otra lista de números
    algun_par = cuantificador_existencial(numeros2, lambda x: x % 2 == 0)   # Aplica el cuantificador existencial para verificar si algún número es par
    print(f"¿Algún número en {numeros2} es par? {algun_par}")              # Imprime el resultado del Ejemplo 2
    
    # Ejemplo 3: Con strings - verificar si todas las palabras tienen más de 3 letras # Comentario del Ejemplo 3
    palabras = ["casa", "perro", "gato", "sol"]                             # Define una lista de palabras
    todas_largas = cuantificador_universal(palabras, lambda p: len(p) > 3)  # Aplica el cuantificador universal para verificar si todas las palabras tienen más de 3 letras
    print(f"¿Todas las palabras en {palabras} tienen más de 3 letras? {todas_largas}") # Imprime el resultado del Ejemplo 3
    
    # Ejemplo 4: Con conjuntos - verificar si existe un múltiplo de 5        # Comentario del Ejemplo 4
    conjunto_nums = {12, 17, 23, 30, 41}                                    # Define un conjunto de números
    existe_multiplo5 = cuantificador_existencial(conjunto_nums, lambda x: x % 5 == 0) # Aplica el cuantificador existencial para verificar si existe un múltiplo de 5
    print(f"¿Existe un múltiplo de 5 en {conjunto_nums}? {existe_multiplo5}") # Imprime el resultado del Ejemplo 4

def equivalencias_logicas():                                                # Define una función llamada equivalencias_logicas
    """
    Demuestra equivalencias lógicas importantes con cuantificadores:
    1. La negación de un universal es un existencial con la condición negada
    2. La negación de un existencial es un universal con la condición negada
    """
    numeros = [1, 3, 5, 7, 9]                                              # Define una lista de números
    
    # Condición original: es par                                           # Comentario de la condición original
    condicion = lambda x: x % 2 == 0                                       # Define una función lambda para verificar si un número es par
    
    # Equivalencia 1: ¬∀x P(x) ≡ ∃x ¬P(x)                                 # Comentario de la Equivalencia 1
    no_todos = not cuantificador_universal(numeros, condicion)            # Calcula la negación de "todos los números son pares"
    existe_no = cuantificador_existencial(numeros, lambda x: not condicion(x)) # Calcula "existe un número que no es par"
    print(f"\nEquivalencia 1: ¬∀x P(x) ≡ ∃x ¬P(x) -> {no_todos == existe_no}") # Imprime el resultado de la Equivalencia 1
    
    # Equivalencia 2: ¬∃x P(x) ≡ ∀x ¬P(x)                                 # Comentario de la Equivalencia 2
    no_existe = not cuantificador_existencial(numeros, condicion)         # Calcula la negación de "existe un número par"
    todos_no = cuantificador_universal(numeros, lambda x: not condicion(x)) # Calcula "todos los números no son pares"
    print(f"Equivalencia 2: ¬∃x P(x) ≡ ∀x ¬P(x) -> {no_existe == todos_no}") # Imprime el resultado de la Equivalencia 2

if __name__ == "__main__":                                                 # Bloque de código que se ejecuta cuando el script se llama directamente
    print("=== Ejemplos básicos de cuantificadores ===")                   # Imprime un encabezado para los ejemplos básicos
    ejemplos()                                                             # Llama a la función ejemplos
    
    print("\n=== Equivalencias lógicas de cuantificadores ===")           # Imprime un encabezado para las equivalencias lógicas
    equivalencias_logicas()                                                # Llama a la función equivalencias_logicas