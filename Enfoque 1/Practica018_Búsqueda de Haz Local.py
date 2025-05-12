# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 12:14:38 2025

@author: elvin

Implementación de búsqueda por haz local para optimización.
Mantiene un conjunto de k mejores estados en cada iteración.
"""

import random  # Importa módulo para generación de números aleatorios

def busqueda_haz_local(funcion_objetivo, generar_vecinos, estados_iniciales, k=3, max_iter=100):
    """
    Implementa el algoritmo de búsqueda por haz local.
    
    Parámetros:
        funcion_objetivo: Función a maximizar                       (callable)
        generar_vecinos:  Función que genera estados vecinos        (callable)
        estados_iniciales: Población inicial de estados             (list)
        k:               Tamaño del haz (k mejores estados)         (int)
        max_iter:        Número máximo de iteraciones               (int)
    
    Retorna:
        El mejor estado encontrado                                  (any)
    """
    estados_actuales = estados_iniciales[:k]  # Inicializa con primeros k estados
    
    for _ in range(max_iter):                 # Bucle principal del algoritmo
        # Generar todos los vecinos de los estados actuales
        vecinos = []                         # Lista para almacenar vecinos
        for estado in estados_actuales:      # Para cada estado en el haz
            vecinos.extend(generar_vecinos(estado))  # Genera y añade vecinos
        
        if not vecinos:                      # Si no hay vecinos disponibles
            break                            # Termina la búsqueda
        
        # Evaluar y seleccionar los k mejores vecinos
        estados_evaluados = [(estado, funcion_objetivo(estado))  # Evalúa
                            for estado in vecinos]               # todos los vecinos
        estados_evaluados.sort(key=lambda x: -x[1])  # Ordena descendente por valor
        estados_actuales = [estado for estado, _ in estados_evaluados[:k]]  # Top k
    
    # Determinar y devolver el mejor estado encontrado
    mejor_estado = max(estados_actuales,     # Busca el máximo
                      key=funcion_objetivo)  # según función objetivo
    return mejor_estado

def funcion_ejemplo(x):
    """
    Función cuadrática de ejemplo con máximo en x=4.
    
    Parámetros:
        x: Valor de entrada para evaluar      (float)
    
    Retorna:
        Valor de la función en x              (float)
    """
    return -(x - 4)**2 + 10  # Máximo en x=4 con valor 10

def generar_vecinos(x, paso=0.5):
    """
    Genera estados vecinos para un punto dado.
    
    Parámetros:
        x:    Valor actual                    (float)
        paso: Tamaño del paso para vecinos    (float)
    
    Retorna:
        Lista con dos vecinos                 (list)
    """
    return [x + paso, x - paso]  # Vecinos simétricos alrededor de x

if __name__ == "__main__":
    # Configuración de la prueba
    random.seed(42)                           # Semilla para reproducibilidad
    estados_iniciales = [random.uniform(0, 10)  # Genera 5 estados iniciales
                      for _ in range(5)]      # en rango [0, 10]
    
    # Ejecución del algoritmo
    solucion = busqueda_haz_local(
        funcion_objetivo = funcion_ejemplo,    # Función a maximizar
        generar_vecinos  = lambda x: generar_vecinos(x, 0.3),  # Paso de 0.3
        estados_iniciales = estados_iniciales, # Población inicial
        k                = 3,                  # Tamaño del haz
        max_iter         = 50                  # Límite de iteraciones
    )
    
    # Presentación de resultados
    print("\n" + "="*50)
    print(" RESULTADOS BÚSQUEDA POR HAZ LOCAL ".center(50, "="))
    print("="*50)
    print(f" Solución encontrada: x = {solucion:.4f}".ljust(49) + " ")
    print(f" Valor de la función: {funcion_ejemplo(solucion):.4f}".ljust(49) + " ")
    print("="*50)