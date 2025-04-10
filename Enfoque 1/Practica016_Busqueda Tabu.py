# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 11:36:52 2025

@author: elvin
"""

import random

def busqueda_tabu(funcion_objetivo, estado_inicial, generar_vecinos, max_iter=100, tam_tabu=5):
    mejor_estado = estado_inicial
    mejor_valor = funcion_objetivo(estado_inicial)
    estado_actual = estado_inicial
    lista_tabu = []
    
    for _ in range(max_iter):
        vecinos = generar_vecinos(estado_actual)
        mejor_vecino = None
        mejor_valor_vecino = -float('inf')
        
        # Evaluar vecinos no tabú
        for vecino in vecinos:
            if vecino not in lista_tabu:
                valor = funcion_objetivo(vecino)
                if valor > mejor_valor_vecino:  # Maximización
                    mejor_vecino = vecino
                    mejor_valor_vecino = valor
        
        # Si no hay vecinos válidos, terminar
        if mejor_vecino is None:
            break
        
        # Actualizar mejor solución global
        if mejor_valor_vecino > mejor_valor:
            mejor_estado = mejor_vecino
            mejor_valor = mejor_valor_vecino
        
        # Mover al mejor vecino y actualizar lista tabú
        estado_actual = mejor_vecino
        lista_tabu.append(mejor_vecino)
        
        # Mantener tamaño de lista tabú
        if len(lista_tabu) > tam_tabu:
            lista_tabu.pop(0)
    
    return mejor_estado

# Ejemplo: Maximizar función cuadrática
def funcion_ejemplo(x):
    return -(x - 3)**2 + 10  # Máximo en x=3

def generar_vecinos(x, paso=0.5):
    return [x + paso, x - paso, x + paso*2, x - paso*2]  # Vecinos cercanos

# Prueba
solucion = busqueda_tabu(
    funcion_objetivo=funcion_ejemplo,
    estado_inicial=random.uniform(0, 6),  # Punto inicial aleatorio
    generar_vecinos=generar_vecinos,
    max_iter=50,
    tam_tabu=5
)

print(f"Solución encontrada: x = {solucion:.2f}, f(x) = {funcion_ejemplo(solucion):.2f}")