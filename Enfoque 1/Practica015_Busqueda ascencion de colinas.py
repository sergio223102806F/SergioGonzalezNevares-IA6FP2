# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 11:12:40 2025

@author: elvin

Algoritmo de Ascensión de Colinas (Hill Climbing) para optimización local.
Implementa una búsqueda local iterativa para encontrar máximos/mínimos de funciones.
"""

def hill_climbing(funcion_objetivo, estado_inicial, generar_vecinos):
    """
    Implementa el algoritmo de Ascensión de Colinas para optimización local.
    
    Parámetros:
        funcion_objetivo: Función a maximizar                          (callable)
        estado_inicial:   Punto inicial para la búsqueda               (any)
        generar_vecinos:  Función que genera estados vecinos           (callable)
    
    Retorna:
        El mejor estado encontrado localmente                          (any)
    """
    estado_actual = estado_inicial          # Estado actual de la búsqueda
    valor_actual  = funcion_objetivo(estado_actual)  # Valor del estado actual
    
    while True:                             # Bucle infinito hasta convergencia
        vecinos = generar_vecinos(estado_actual)  # Genera todos los vecinos
        if not vecinos:                     # Si no hay más vecinos
            return estado_actual            # Retorna solución actual
        
        # Evaluación de todos los vecinos
        mejor_vecino = None                 # Mejor vecino encontrado
        mejor_valor  = valor_actual         # Valor del mejor vecino
        
        for vecino in vecinos:              # Examina cada vecino
            valor_vecino = funcion_objetivo(vecino)  # Evalúa función objetivo
            if valor_vecino > mejor_valor:   # Comparación para maximización
                mejor_vecino = vecino        # Actualiza mejor vecino
                mejor_valor  = valor_vecino  # Actualiza mejor valor
        
        if mejor_vecino is None:            # Si no hay mejoras
            return estado_actual            # Retorna óptimo local
        
        # Movimiento a la mejor solución vecina
        estado_actual = mejor_vecino        # Actualiza estado actual
        valor_actual  = mejor_valor         # Actualiza valor actual

def funcion_ejemplo(x):
    """
    Función cuadrática de ejemplo con máximo en x=3.
    
    Parámetros:
        x: Valor de entrada para evaluar      (float)
    
    Retorna:
        Valor de la función en x              (float)
    """
    return -(x - 3)**2 + 10  # Máximo en x=3 con valor 10

def generar_vecinos(x, paso=0.1):
    """
    Genera soluciones vecinas para un punto dado.
    
    Parámetros:
        x:    Valor actual                    (float)
        paso: Tamaño del paso para vecinos    (float)
    
    Retorna:
        Lista de valores vecinos              (list)
    """
    return [x + paso, x - paso]  # Vecinos inmediatos (adelante/atrás)

if __name__ == "__main__":
    # Configuración y ejecución del algoritmo
    punto_inicial = 0.0                      # Punto de inicio de la búsqueda
    solucion = hill_climbing(
        funcion_objetivo = funcion_ejemplo,   # Función a optimizar
        estado_inicial   = punto_inicial,     # Punto inicial
        generar_vecinos  = generar_vecinos    # Estrategia de generación de vecinos
    )
    
    # Presentación de resultados
    print("\n" + "="*50)
    print(" RESULTADOS DE ASCENSIÓN DE COLINAS ".center(50, "="))
    print("="*50)
    print(f" Solución encontrada: x = {solucion:.4f}".ljust(49) + " ")
    print(f" Valor de la función: f(x) = {funcion_ejemplo(solucion):.4f}".ljust(49) + " ")
    print("="*50)