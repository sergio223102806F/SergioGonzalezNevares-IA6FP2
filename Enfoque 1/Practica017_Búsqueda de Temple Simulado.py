# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 12:10:12 2025

@author: elvin
"""

import random  # Importa el módulo random para generación de números aleatorios

def temple_simulado(funcion_objetivo, estado_inicial, generar_vecino, temp_inicial=1000, enfriamiento=0.95, iter_por_temp=100):
    # Implementación del algoritmo de Temple Simulado (Simulated Annealing)
    estado_actual = estado_inicial  # Inicializa el estado actual con el estado inicial proporcionado
    mejor_estado = estado_actual  # Guarda el mejor estado encontrado (inicialmente el estado inicial)
    mejor_valor = funcion_objetivo(estado_actual)  # Calcula el valor del mejor estado
    temp = temp_inicial  # Establece la temperatura inicial
    
    # Función de aproximación a exp() usando serie de Taylor (3 términos)
    def aprox_exp(x):
        # Aproximación polinómica de la función exponencial para valores pequeños de x
        return 1 + x + (x**2)/2  # Serie de Taylor truncada hasta el segundo orden
    
    # Bucle principal del algoritmo
    while temp > 0.1:  # Continúa mientras la temperatura sea mayor que 0.1
        # Realiza un número fijo de iteraciones para cada temperatura
        for _ in range(iter_por_temp):
            vecino = generar_vecino(estado_actual)  # Genera un estado vecino al actual
            # Calcula la diferencia entre el valor del vecino y el estado actual
            delta = funcion_objetivo(vecino) - funcion_objetivo(estado_actual)
            
            # Criterio de aceptación con aproximación exp()
            if delta > 0 or (temp > 0 and random.random() < aprox_exp(delta / temp)):
                # Acepta el nuevo estado si es mejor o según probabilidad basada en temperatura
                estado_actual = vecino  # Actualiza el estado actual
                # Actualiza el mejor estado si encontramos uno mejor
                if funcion_objetivo(estado_actual) > mejor_valor:
                    mejor_estado = estado_actual
                    mejor_valor = funcion_objetivo(estado_actual)
        
        temp *= enfriamiento  # Reduce la temperatura según el factor de enfriamiento
    
    return mejor_estado  # Devuelve el mejor estado encontrado

# Función de ejemplo para minimizar: (x-3)² + 7
def funcion_costo(x):
    # Función cuadrática con mínimo en x=3 y valor mínimo de 7
    return (x - 3)**2 + 7  # Forma canónica de parábola con vértice en (3,7)

def generar_vecino(x, paso=0.5):
    # Genera un estado vecino perturbando el estado actual con un valor aleatorio
    return x + random.uniform(-paso, paso)  # Valor aleatorio uniforme en [x-paso, x+paso]

# Bloque principal de ejecución
if __name__ == "__main__":
    random.seed(42)  # Fija la semilla aleatoria para reproducibilidad
    
    # Ejecuta el algoritmo de Temple Simulado
    solucion = temple_simulado(
        funcion_objetivo=funcion_costo,  # Función a minimizar
        estado_inicial=random.uniform(-10, 10),  # Estado inicial aleatorio en [-10,10]
        generar_vecino=generar_vecino  # Función para generar vecinos
    )
    
    # Muestra los resultados encontrados
    print(f"Solución: x = {solucion:.4f}, Costo = {funcion_costo(solucion):.4f}")