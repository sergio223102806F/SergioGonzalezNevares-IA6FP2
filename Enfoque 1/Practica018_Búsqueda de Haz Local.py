# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 12:14:38 2025

@author: elvin
"""

import random

def busqueda_haz_local(funcion_objetivo, generar_vecinos, estados_iniciales, k=3, max_iter=100):
    # k = número de estados que mantendremos (tamaño del haz)
    estados_actuales = estados_iniciales[:k]  # Tomamos los primeros k estados
    
    for _ in range(max_iter):
        # Generar todos los vecinos de todos los estados actuales
        vecinos = []
        for estado in estados_actuales:
            vecinos.extend(generar_vecinos(estado))
        
        # Si no hay vecinos, terminar
        if not vecinos:
            break
        
        # Evaluar todos los vecinos y seleccionar los k mejores
        estados_evaluados = [(estado, funcion_objetivo(estado)) for estado in vecinos]
        estados_evaluados.sort(key=lambda x: -x[1])  # Ordenar de mayor a menor (para maximización)
        estados_actuales = [estado for estado, _ in estados_evaluados[:k]]
    
    # Devolver el mejor estado encontrado
    mejor_estado = max(estados_actuales, key=funcion_objetivo)
    return mejor_estado

# Ejemplo: Maximizar función -(x-4)² + 10
def funcion_ejemplo(x):
    return -(x - 4)**2 + 10  # Máximo en x=4 (valor=10)

def generar_vecinos(x, paso=0.5):
    return [x + paso, x - paso]  # Vecinos simples

# Prueba con 5 estados iniciales aleatorios
random.seed(42)
estados_iniciales = [random.uniform(0, 10) for _ in range(5)]
solucion = busqueda_haz_local(
    funcion_objetivo=funcion_ejemplo,
    generar_vecinos=lambda x: generar_vecinos(x, 0.3),
    estados_iniciales=estados_iniciales,
    k=3,  # Tamaño del haz
    max_iter=50
)

print(f"Solución encontrada: x = {solucion:.4f}, Valor = {funcion_ejemplo(solucion):.4f}")