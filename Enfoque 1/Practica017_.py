# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 12:10:12 2025

@author: elvin
"""

import random

def temple_simulado(funcion_objetivo, estado_inicial, generar_vecino, temp_inicial=1000, enfriamiento=0.95, iter_por_temp=100):
    estado_actual = estado_inicial
    mejor_estado = estado_actual
    mejor_valor = funcion_objetivo(estado_actual)
    temp = temp_inicial
    
    # Función de aproximación a exp() usando serie de Taylor (3 términos)
    def aprox_exp(x):
        return 1 + x + (x**2)/2  # Aproximación suficiente para el rango que usamos
    
    while temp > 0.1:
        for _ in range(iter_por_temp):
            vecino = generar_vecino(estado_actual)
            delta = funcion_objetivo(vecino) - funcion_objetivo(estado_actual)
            
            # Criterio de aceptación con aproximación exp()
            if delta > 0 or (temp > 0 and random.random() < aprox_exp(delta / temp)):
                estado_actual = vecino
                if funcion_objetivo(estado_actual) > mejor_valor:
                    mejor_estado = estado_actual
                    mejor_valor = funcion_objetivo(estado_actual)
        
        temp *= enfriamiento
    
    return mejor_estado

# Ejemplo de uso minimizando (x-3)² + 7
def funcion_costo(x):
    return (x - 3)**2 + 7  # Mínimo en x=3 (valor=7)

def generar_vecino(x, paso=0.5):
    return x + random.uniform(-paso, paso)

# Prueba
random.seed(42)
solucion = temple_simulado(
    funcion_objetivo=funcion_costo,
    estado_inicial=random.uniform(-10, 10),
    generar_vecino=generar_vecino
)

print(f"Solución: x = {solucion:.4f}, Costo = {funcion_costo(solucion):.4f}")