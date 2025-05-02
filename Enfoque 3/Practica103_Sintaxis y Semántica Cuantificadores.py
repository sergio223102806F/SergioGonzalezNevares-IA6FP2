# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 15:39:36 2025

@author: elvin
"""

"""
Este código muestra ejemplos de cómo trabajar con cuantificadores universales y existenciales
en Python, tanto para listas como para conjuntos. Los cuantificadores son conceptos fundamentales
en lógica matemática que nos permiten expresar afirmaciones sobre "todos" o "algunos" elementos
de un conjunto.
"""

def cuantificador_universal(conjunto, condicion):
    """
    Implementa el cuantificador universal (∀): Verifica si TODOS los elementos del conjunto
    satisfacen la condición dada.
    
    Args:
        conjunto (iterable): Colección de elementos a verificar
        condicion (function): Función que toma un elemento y devuelve True/False
    
    Returns:
        bool: True si todos los elementos satisfacen la condición, False en caso contrario
    """
    return all(condicion(x) for x in conjunto)

def cuantificador_existencial(conjunto, condicion):
    """
    Implementa el cuantificador existencial (∃): Verifica si ALGÚN elemento del conjunto
    satisface la condición dada.
    
    Args:
        conjunto (iterable): Colección de elementos a verificar
        condicion (function): Función que toma un elemento y devuelve True/False
    
    Returns:
        bool: True si al menos un elemento satisface la condición, False en caso contrario
    """
    return any(condicion(x) for x in conjunto)

def ejemplos():
    """
    Ejemplos prácticos de uso de los cuantificadores con diferentes tipos de datos
    y condiciones.
    """
    
    # Ejemplo 1: Verificar si todos los números en una lista son positivos
    numeros = [2, 4, 6, 8, 10]
    todos_positivos = cuantificador_universal(numeros, lambda x: x > 0)
    print(f"¿Todos los números {numeros} son positivos? {todos_positivos}")
    
    # Ejemplo 2: Verificar si algún número en una lista es par
    numeros2 = [1, 3, 5, 7, 8, 9]
    algun_par = cuantificador_existencial(numeros2, lambda x: x % 2 == 0)
    print(f"¿Algún número en {numeros2} es par? {algun_par}")
    
    # Ejemplo 3: Con strings - verificar si todas las palabras tienen más de 3 letras
    palabras = ["casa", "perro", "gato", "sol"]
    todas_largas = cuantificador_universal(palabras, lambda p: len(p) > 3)
    print(f"¿Todas las palabras en {palabras} tienen más de 3 letras? {todas_largas}")
    
    # Ejemplo 4: Con conjuntos - verificar si existe un múltiplo de 5
    conjunto_nums = {12, 17, 23, 30, 41}
    existe_multiplo5 = cuantificador_existencial(conjunto_nums, lambda x: x % 5 == 0)
    print(f"¿Existe un múltiplo de 5 en {conjunto_nums}? {existe_multiplo5}")

def equivalencias_logicas():
    """
    Demuestra equivalencias lógicas importantes con cuantificadores:
    1. La negación de un universal es un existencial con la condición negada
    2. La negación de un existencial es un universal con la condición negada
    """
    numeros = [1, 3, 5, 7, 9]
    
    # Condición original: es par
    condicion = lambda x: x % 2 == 0
    
    # Equivalencia 1: ¬∀x P(x) ≡ ∃x ¬P(x)
    no_todos = not cuantificador_universal(numeros, condicion)
    existe_no = cuantificador_existencial(numeros, lambda x: not condicion(x))
    print(f"\nEquivalencia 1: ¬∀x P(x) ≡ ∃x ¬P(x) -> {no_todos == existe_no}")
    
    # Equivalencia 2: ¬∃x P(x) ≡ ∀x ¬P(x)
    no_existe = not cuantificador_existencial(numeros, condicion)
    todos_no = cuantificador_universal(numeros, lambda x: not condicion(x))
    print(f"Equivalencia 2: ¬∃x P(x) ≡ ∀x ¬P(x) -> {no_existe == todos_no}")

if __name__ == "__main__":
    print("=== Ejemplos básicos de cuantificadores ===")
    ejemplos()
    
    print("\n=== Equivalencias lógicas de cuantificadores ===")
    equivalencias_logicas()