# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 11:12:40 2025

@author: elvin
"""

def hill_climbing(funcion_objetivo, estado_inicial, generar_vecinos):
    estado_actual = estado_inicial
    valor_actual = funcion_objetivo(estado_actual)
    
    while True:
        vecinos = generar_vecinos(estado_actual)
        if not vecinos:  # No hay más vecinos
            return estado_actual
        
        # Evaluar todos los vecinos
        mejor_vecino = None
        mejor_valor = valor_actual
        
        for vecino in vecinos:
            valor_vecino = funcion_objetivo(vecino)
            if valor_vecino > mejor_valor:  # Maximización (usar < para minimización)
                mejor_vecino = vecino
                mejor_valor = valor_vecino
        
        if mejor_vecino is None:  # No hay mejor vecino
            return estado_actual
        
        # Moverse al mejor vecino encontrado
        estado_actual = mejor_vecino
        valor_actual = mejor_valor

# Ejemplo de uso: encontrar máximo de una función cuadrática
def funcion_ejemplo(x):
    return -(x - 3)**2 + 10  # Máximo en x=3 con valor 10

def generar_vecinos(x, paso=0.1):
    return [x + paso, x - paso]  # Vecinos cercanos

# Prueba
punto_inicial = 0.0
solucion = hill_climbing(funcion_ejemplo, punto_inicial, generar_vecinos)
print(f"Solución encontrada: x = {solucion:.2f}, f(x) = {funcion_ejemplo(solucion):.2f}")