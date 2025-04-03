# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 10:33:19 2025

@author: elvin
"""

import random                                     # Para generación aleatoria

class AlgoritmoGenetico:                         # Clase principal del AG
    def __init__(self, tam_poblacion,            # Constructor con parámetros
                 longitud_gen, funcion_aptitud,
                 prob_mutacion=0.01,
                 prob_cruce=0.7):
        self.tam_poblacion = tam_poblacion       # Tamaño de la población
        self.longitud_gen = longitud_gen         # Longitud del cromosoma
        self.funcion_aptitud = funcion_aptitud   # Función objetivo
        self.prob_mutacion = prob_mutacion       # Probabilidad de mutación
        self.prob_cruce = prob_cruce             # Probabilidad de cruce
        self.poblacion = []                      # Almacena la población actual

    def inicializar_poblacion(self):             # Crea población inicial
        self.poblacion = [[random.randint(0, 1)  # Genera genes binarios
                          for _ in range(self.longitud_gen)]
                          for _ in range(self.tam_poblacion)]

    def evaluar_poblacion(self):                 # Calcula aptitud para todos
        return [self.funcion_aptitud(ind)        # Evalúa cada individuo
                for ind in self.poblacion]

    def seleccionar(self, aptitudes):            # Selección por torneo
        seleccionados = []
        for _ in range(2):                       # Selecciona 2 padres
            idx1, idx2 = random.sample(range(len(self.poblacion)), 2)
            ganador = idx1 if aptitudes[idx1] > aptitudes[idx2] else idx2
            seleccionados.append(self.poblacion[ganador])
        return seleccionados

    def cruzar(self, padre1, padre2):            # Cruce en un punto
        if random.random() < self.prob_cruce:    # Decide si hay cruce
            punto = random.randint(1,            # Elige punto de cruce
                                  self.longitud_gen-1)
            return (padre1[:punto] + padre2[punto:],  # Hijo 1
                    padre2[:punto] + padre1[punto:])  # Hijo 2
        return padre1, padre2                    # Sin cambios

    def mutar(self, individuo):                  # Mutación bit a bit
        return [gen ^ (random.random() < self.prob_mutacion)  # Flip con probabilidad
                for gen in individuo]

    def evolucionar(self):                       # Paso de evolución
        aptitudes = self.evaluar_poblacion()
        nueva_poblacion = []
        for _ in range(self.tam_poblacion // 2): # Genera nueva población
            padres = self.seleccionar(aptitudes)
            hijo1, hijo2 = self.cruzar(*padres)
            nueva_poblacion.extend([self.mutar(hijo1),
                                   self.mutar(hijo2)])
        self.poblacion = nueva_poblacion

    def mejor_individuo(self):                   # Encuentra el mejor
        aptitudes = self.evaluar_poblacion()
        idx = aptitudes.index(max(aptitudes))    # Índice del máximo
        return self.poblacion[idx], aptitudes[idx]

# --- Función de ejemplo: Maximizar cantidad de 1s ---
def contar_unos(cromosoma):                      # Función de aptitud
    return sum(cromosoma)                        # Cuenta los 1s

if __name__ == "__main__":
    # Configuración del algoritmo
    ag = AlgoritmoGenetico(
        tam_poblacion=50,                        # 50 individuos
        longitud_gen=20,                         # Cromosomas de 20 bits
        funcion_aptitud=contar_unos,             # Objetivo: maximizar 1s
        prob_mutacion=0.05,                     # 5% de probabilidad de mutación
        prob_cruce=0.8                           # 80% de probabilidad de cruce
    )
    
    ag.inicializar_poblacion()                   # Población inicial
    
    # Evolución por generaciones
    for generacion in range(100):
        ag.evolucionar()
        mejor, aptitud = ag.mejor_individuo()
        print(f"Gen {generacion}: Mejor aptitud = {aptitud}")
        
        if aptitud == ag.longitud_gen:           # Solución óptima encontrada
            print(f"¡Solución perfecta en gen {generacion}: {mejor}")
            break