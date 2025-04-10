# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 12:17:20 2025

@author: elvin
"""

import random

def algoritmo_genetico(func_aptitud, genes_posibles, tam_poblacion=50, 
                      prob_mutacion=0.1, elitismo=0.1, generaciones=100):
    # Crear población inicial aleatoria
    poblacion = [''.join(random.choice(genes_posibltes)) 
                for _ in range(tam_poblacion)]
    
    for _ in range(generaciones):
        # Evaluar aptitud de cada individuo
        aptitudes = [(ind, func_aptitud(ind)) for ind in poblacion]
        
        # Ordenar por aptitud (mayor es mejor)
        aptitudes.sort(key=lambda x: -x[1])
        
        # Seleccionar padres (elitismo: los mejores pasan directamente)
        padres = [ind for ind, _ in aptitudes[:int(elitismo*tam_poblacion)]]
        
        # Completar con selección por torneo
        while len(padres) < tam_poblacion:
            torneo = random.sample(aptitudes, k=3)  # Torneo de 3 individuos
            ganador = max(torneo, key=lambda x: x[1])[0]
            padres.append(ganador)
        
        # Reproducción (cruce de un punto)
        nueva_gen = []
        for i in range(0, len(padres), 2):
            if i+1 >= len(padres): 
                nueva_gen.append(padres[i])
                break
            punto_cruce = random.randint(1, len(padres[i])-1)
            hijo1 = padres[i][:punto_cruce] + padres[i+1][punto_cruce:]
            hijo2 = padres[i+1][:punto_cruce] + padres[i][punto_cruce:]
            nueva_gen.extend([hijo1, hijo2])
        
        # Mutación
        poblacion = []
        for ind in nueva_gen:
            if random.random() < prob_mutacion:
                gen = random.randint(0, len(ind)-1)
                ind = ind[:gen] + random.choice(genes_posibles) + ind[gen+1:]
            poblacion.append(ind)
    
    # Devolver el mejor individuo encontrado
    return max(poblacion, key=func_aptitud)

# Ejemplo: Encontrar la cadena "HOLA MUNDO"
def aptitud_objetivo(cadena):
    objetivo = "HOLA MUNDO"
    return sum(1 for a, b in zip(cadena, objetivo) if a == b)

# Parámetros
GENES = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
LONGITUD = 10

# Ejecutar
solucion = algoritmo_genetico(
    func_aptitud=aptitud_objetivo,
    genes_posibles=GENES,
    tam_poblacion=100,
    prob_mutacion=0.2,
    generaciones=500
)

print(f"Mejor solución encontrada: '{solucion}' (Aptitud: {aptitud_objetivo(solucion)}/{len('HOLA MUNDO')})")