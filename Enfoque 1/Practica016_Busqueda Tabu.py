# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 11:36:52 2025

@author: elvin

Algoritmo de Búsqueda Tabú para optimización de funciones.
Implementa una metaheurística para encontrar máximos globales evitando mínimos locales.
"""

import random  # Importa módulo para generación de números aleatorios

def busqueda_tabu(funcion_objetivo, estado_inicial, generar_vecinos, max_iter=100, tam_tabu=5):
    """
    Implementa el algoritmo de Búsqueda Tabú para optimización.
    
    Parámetros:
        funcion_objetivo: Función a maximizar                          (callable)
        estado_inicial:   Punto inicial para la búsqueda               (any)
        generar_vecinos:  Función que genera estados vecinos           (callable)
        max_iter:         Número máximo de iteraciones                (int)
        tam_tabu:         Tamaño máximo de la lista tabú              (int)
    
    Retorna:
        El mejor estado encontrado durante la búsqueda                 (any)
    """
    mejor_estado    = estado_inicial          # Almacena el mejor estado encontrado
    mejor_valor     = funcion_objetivo(estado_inicial)  # Valor del mejor estado
    estado_actual   = estado_inicial          # Estado actual de la búsqueda
    lista_tabu      = []                      # Lista de soluciones prohibidas
    
    for _ in range(max_iter):                 # Bucle principal del algoritmo
        vecinos          = generar_vecinos(estado_actual)  # Genera vecinos
        mejor_vecino     = None               # Mejor vecino no tabú encontrado
        mejor_valor_vecino = -float('inf')    # Valor del mejor vecino (maximización)
        
        for vecino in vecinos:                # Evalúa todos los vecinos generados
            if vecino not in lista_tabu:      # Considera solo vecinos no tabú
                valor = funcion_objetivo(vecino)  # Evalúa la función objetivo
                if valor > mejor_valor_vecino:    # Encuentra mejor vecino válido
                    mejor_vecino     = vecino
                    mejor_valor_vecino = valor
        
        if mejor_vecino is None:              # Si no hay vecinos válidos
            break                             # Termina la búsqueda
        
        if mejor_valor_vecino > mejor_valor:  # Actualiza mejor solución global
            mejor_estado = mejor_vecino
            mejor_valor  = mejor_valor_vecino
        
        estado_actual = mejor_vecino          # Mueve al mejor vecino encontrado
        lista_tabu.append(mejor_vecino)       # Añade movimiento a lista tabú
        
        if len(lista_tabu) > tam_tabu:        # Mantiene tamaño fijo de lista tabú
            lista_tabu.pop(0)                 # Elimina el elemento más antiguo
    
    return mejor_estado                       # Devuelve el mejor estado encontrado

def funcion_ejemplo(x):
    """
    Función cuadrática de ejemplo con máximo en x=3.
    
    Parámetros:
        x: Valor de entrada para evaluar      (float)
    
    Retorna:
        Valor de la función en x              (float)
    """
    return -(x - 3)**2 + 10  # Máximo en x=3 con valor 10

def generar_vecinos(x, paso=0.5):
    """
    Genera soluciones vecinas para un punto dado.
    
    Parámetros:
        x:    Valor actual                    (float)
        paso: Tamaño del paso para vecinos    (float)
    
    Retorna:
        Lista de valores vecinos              (list)
    """
    return [x + paso, x - paso, x + paso*2, x - paso*2]  # Vecinos simétricos

if __name__ == "__main__":
    random.seed(42)  # Fija semilla para resultados reproducibles
    
    # Configuración y ejecución del algoritmo
    solucion = busqueda_tabu(
        funcion_objetivo = funcion_ejemplo,   # Función a optimizar
        estado_inicial   = random.uniform(0, 6),  # Punto inicial aleatorio
        generar_vecinos  = generar_vecinos,   # Estrategia de generación de vecinos
        max_iter         = 50,                # Límite de iteraciones
        tam_tabu         = 5                  # Tamaño de memoria tabú
    )
    
    # Presentación de resultados
    print("\n" + "="*50)
    print(" RESULTADOS DE BÚSQUEDA TABÚ ".center(50, "="))
    print("="*50)
    print(f" Solución encontrada: x = {solucion:.4f}".ljust(49) + " ")
    print(f" Valor de la función: f(x) = {funcion_ejemplo(solucion):.4f}".ljust(49) + " ")
    print("="*50)