# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 12:17:20 2025

@author: elvin

Implementación de un algoritmo genético básico para optimización.
Incluye selección por torneo, cruce de un punto y mutación aleatoria.
"""

import random  # Importa módulo para generación de números aleatorios

def algoritmo_genetico(func_aptitud, genes_posibles, tam_poblacion=50, 
                      prob_mutacion=0.1, elitismo=0.1, generaciones=100):
    """
    Implementa un algoritmo genético básico para encontrar soluciones óptimas.
    
    Parámetros:
        func_aptitud:   Función de evaluación de aptitud               (callable)
        genes_posibles: Caracteres/genes posibles para solución       (str/list)
        tam_poblacion:  Tamaño de la población                       (int)
        prob_mutacion: Probabilidad de mutación por gen              (float)
        elitismo:      Porcentaje de élite que pasa directo          (float)
        generaciones:  Número máximo de generaciones                (int)
    
    Retorna:
        El mejor individuo encontrado                                (str)
    """
    # Crear población inicial aleatoria
    poblacion = [''.join(random.choice(genes_posibles)  # Genera individuos aleatorios
                for _ in range(tam_poblacion)]          # Población de tamaño dado
    
    for _ in range(generaciones):                       # Bucle por generaciones
        # Evaluar aptitud de cada individuo
        aptitudes = [(ind, func_aptitud(ind))          # Calcula aptitud
                     for ind in poblacion]             # Para cada individuo
        
        # Ordenar por aptitud (mayor es mejor)
        aptitudes.sort(key=lambda x: -x[1])            # Orden descendente
        
        # Seleccionar padres (elitismo: los mejores pasan directamente)
        padres = [ind for ind, _ in                    # Selecciona elite
                 aptitudes[:int(elitismo*tam_poblacion)]]  
        
        # Completar con selección por torneo
        while len(padres) < tam_poblacion:             # Hasta completar población
            torneo = random.sample(aptitudes, k=3)     # Selecciona 3 aleatorios
            ganador = max(torneo, key=lambda x: x[1])[0]  # Elige el mejor del torneo
            padres.append(ganador)                     # Añade a padres
            
        # Reproducción (cruce de un punto)
        nueva_gen = []                                 # Nueva generación
        for i in range(0, len(padres), 2):             # Por pares de padres
            if i+1 >= len(padres):                     # Si hay número impar
                nueva_gen.append(padres[i])             # Añade el último padre
                break
            punto_cruce = random.randint(1, len(padres[i])-1)  # Punto aleatorio
            hijo1 = padres[i][:punto_cruce] + padres[i+1][punto_cruce:]  # Cruce
            hijo2 = padres[i+1][:punto_cruce] + padres[i][punto_cruce:]  # Cruce
            nueva_gen.extend([hijo1, hijo2])           # Añade hijos
            
        # Mutación
        poblacion = []                                 # Nueva población
        for ind in nueva_gen:                          # Para cada individuo
            if random.random() < prob_mutacion:        # Probabilidad de mutar
                gen = random.randint(0, len(ind)-1)    # Elige gen aleatorio
                ind = ind[:gen] + random.choice(genes_posibles) + ind[gen+1:]  # Mutación
            poblacion.append(ind)                      # Añade a población
    
    # Devolver el mejor individuo encontrado
    return max(poblacion, key=func_aptitud)           # Mejor solución final

def aptitud_objetivo(cadena):
    """
    Función de aptitud para ejemplo de cadena objetivo.
    
    Parámetros:
        cadena: Cadena a evaluar                      (str)
    
    Retorna:
        Puntuación de similitud con objetivo          (int)
    """
    objetivo = "HOLA MUNDO"                           # Cadena objetivo
    return sum(1 for a, b in zip(cadena, objetivo)   # Cuenta coincidencias
             if a == b)                              # Por posición

# Parámetros del algoritmo
GENES     = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "            # Caracteres posibles
LONGITUD  = 10                                       # Longitud de cadena

# Ejecución del algoritmo genético
solucion = algoritmo_genetico(
    func_aptitud  = aptitud_objetivo,                # Función objetivo
    genes_posibles = GENES,                          # Genes disponibles
    tam_poblacion = 100,                             # Tamaño población
    prob_mutacion = 0.2,                             # Probabilidad mutación
    generaciones  = 500                              # Número generaciones
)

# Presentación de resultados
print("\n" + "="*50)                                  # Línea decorativa
print(" RESULTADO ALGORITMO GENÉTICO ".center(50, "="))  # Título
print("="*50)                                         # Línea decorativa
print(f" Mejor solución encontrada: '{solucion}'".ljust(49) + " ")
print(f" Aptitud: {aptitud_objetivo(solucion)}/{len('HOLA MUNDO')}".ljust(49) + " ")
print("="*50)                                         # Línea decorativa