# -*- coding: utf-8 -*- 
"""
Created on Wed Apr  9 14:24:39 2025

@author: elvin  # Autor del script
"""

# Importa el paquete numpy para operaciones matemáticas y de matrices
import numpy as np
# Importa defaultdict para crear diccionarios con valores por defecto
from collections import defaultdict
# Importa el módulo random para operaciones aleatorias
import random
# Importa product para generar combinaciones de valores (no se usa en este script)
from itertools import product

# Clase que representa un CSP probabilístico (Problema de Satisfacción de Restricciones con incertidumbre)
class ProbabilisticCSP:
    def __init__(self, variables, dominios, restricciones):
        # Inicializa las variables, dominios y restricciones del CSP
        self.variables = variables
        self.dominios = dominios
        self.restricciones = restricciones
        # Inicializa un diccionario con los vecinos (variables relacionadas por restricciones)
        self.vecinos = {v: set() for v in variables}
        for (v1, v2) in restricciones:
            # Añade v2 como vecino de v1 y viceversa
            self.vecinos[v1].add(v2)
            self.vecinos[v2].add(v1)
        
        # Inicializa las probabilidades de cumplimiento de restricciones
        self.prob_restricciones = self.initialize_constraint_probabilities()
        
        # Inicializa la distribución de probabilidad para los valores de cada variable
        self.prob_variables = {
            v: {val: 1/len(dominios[v]) for val in dominios[v]} 
            for v in variables
        }

    # Método que inicializa una matriz de probabilidades para cada restricción
    def initialize_constraint_probabilities(self):
        """Inicializa probabilidades para cada restricción"""
        prob_restricciones = {}
        for (v1, v2) in self.restricciones:
            # Matriz de probabilidades donde cada celda representa P(cumple | v1=a, v2=b)
            prob_restricciones[(v1, v2)] = np.ones((len(self.dominios[v1]), 
                                                    len(self.dominios[v2]))) * 0.9
            # Se asume 90% de probabilidad de cumplimiento, 10% de falla (incertidumbre)
        return prob_restricciones

    # Método que resuelve el CSP probabilístico usando recocido simulado (simulated annealing)
    def solve(self, max_iter=100, temp_init=1.0, temp_end=0.01):
        """Resuelve el CSP probabilístico usando simulated annealing"""
        # Genera una solución aleatoria inicial
        current_solution = {v: random.choice(list(self.dominios[v])) 
                            for v in self.variables}
        # Calcula la energía (inverso de la probabilidad) de la solución actual
        current_energy = self.energy(current_solution)
        
        # Guarda la mejor solución encontrada hasta el momento
        best_solution = dict(current_solution)
        best_energy = current_energy
        
        # Ciclo principal del algoritmo de recocido simulado
        for i in range(max_iter):
            # Calcula la temperatura actual basada en la iteración
            temp = temp_init - (temp_init - temp_end) * (i / max_iter)
            
            # Selecciona una variable a modificar
            var = self.select_variable(current_solution)
            
            # Crea una nueva solución candidata
            new_solution = dict(current_solution)
            new_val = self.select_new_value(var, current_solution)
            new_solution[var] = new_val
            # Calcula la energía de la nueva solución
            new_energy = self.energy(new_solution)
            
            # Criterio de aceptación: acepta si mejora o con cierta probabilidad si empeora
            if new_energy < current_energy or \
               random.random() < np.exp((current_energy - new_energy) / temp):
                # Acepta la nueva solución
                current_solution = new_solution
                current_energy = new_energy
                
                # Actualiza la mejor solución si es la mejor encontrada
                if new_energy < best_energy:
                    best_solution = dict(new_solution)
                    best_energy = new_energy
        
        # Devuelve la mejor solución encontrada y su energía
        return best_solution, best_energy

    # Método para seleccionar la variable más incierta o conflictiva
    def select_variable(self, solution):
        """Selecciona variable basada en incertidumbre y conflictos"""
        # Calcula incertidumbre como 1 - probabilidad actual del valor asignado
        uncertainty = {v: 1 - self.prob_variables[v][solution[v]] 
                       for v in self.variables}
        
        # Calcula conflictos como suma de (1 - probabilidad de cumplimiento de restricción)
        conflict = {
            v: sum(1 - self.prob_restricciones[(v, n)][solution[v]][solution[n]] 
                   for n in self.vecinos[v] if (v, n) in self.prob_restricciones)
            for v in self.variables
        }
        
        # Combina incertidumbre y conflictos para seleccionar la variable con mayor score
        scores = {v: uncertainty[v] + conflict[v] for v in self.variables}
        return max(scores.keys(), key=lambda x: scores[x])

    # Método para seleccionar un nuevo valor para una variable según las probabilidades
    def select_new_value(self, var, solution):
        """Selecciona nuevo valor basado en probabilidades y restricciones"""
        probs = []
        for val in self.dominios[var]:
            # Comienza con la probabilidad del valor de la variable
            prob = self.prob_variables[var][val]
            
            # Ajusta la probabilidad según los valores de los vecinos
            for neighbor in self.vecinos[var]:
                if (var, neighbor) in self.prob_restricciones:
                    neighbor_val = solution[neighbor]
                    prob *= self.prob_restricciones[(var, neighbor)][val][neighbor_val]
                elif (neighbor, var) in self.prob_restricciones:
                    neighbor_val = solution[neighbor]
                    prob *= self.prob_restricciones[(neighbor, var)][neighbor_val][val]
            
            # Añade la probabilidad ajustada a la lista
            probs.append(prob)
        
        # Convierte la lista en un array numpy
        probs = np.array(probs)
        # Normaliza las probabilidades para que sumen 1
        probs = probs / probs.sum()
        
        # Escoge un nuevo valor aleatorio según la distribución de probabilidades
        return random.choices(list(self.dominios[var]), weights=probs)[0]

    # Método que calcula la energía de una solución (menor es mejor)
    def energy(self, solution):
        """Calcula la energía (inverso de la probabilidad) de una solución"""
        prob = 1.0  # Inicializa la probabilidad total como 1
        
        # Multiplica la probabilidad de cada valor individual
        for var in self.variables:
            prob *= self.prob_variables[var][solution[var]]
        
        # Multiplica la probabilidad de cumplimiento de cada restricción
        for (v1, v2) in self.restricciones:
            val1 = solution[v1]
            val2 = solution[v2]
            prob *= self.prob_restricciones[(v1, v2)][val1][val2]
        
        # Devuelve la energía como el logaritmo negativo de la probabilidad (evita log(0) con 1e-10)
        return -np.log(prob + 1e-10)

    # Método para actualizar las probabilidades según observaciones
    def update_probabilities(self, observations):
        """Actualiza probabilidades basado en observaciones"""
        for (v1, v2), satisfies in observations.items():
            # Obtiene los valores actuales de las variables
            val1 = observations['current_values'][v1]
            val2 = observations['current_values'][v2]
            
            # Actualiza la probabilidad usando un aprendizaje tipo Bayes con tasa alpha
            alpha = 0.1  # Tasa de aprendizaje
            current_p = self.prob_restricciones[(v1, v2)][val1][val2]
            new_p = current_p * (1 - alpha) + satisfies * alpha
            self.prob_restricciones[(v1, v2)][val1][val2] = new_p
            
            # Asegura que las probabilidades se mantengan en el rango [0.01, 0.99]
            self.prob_restricciones[(v1, v2)] = np.clip(
                self.prob_restricciones[(v1, v2)], 0.01, 0.99)

# Función auxiliar que define si dos valores cumplen una restricción (no ser iguales)
def cumple_restriccion(valor1, valor2):
    """Función de restricción base (puede tener incertidumbre)"""
    return valor1 != valor2

# Función que crea un CSP probabilístico modelando un Sudoku 4x4
def crear_sudoku_4x4_incierto():
    # Define variables como coordenadas (i,j) de una grilla 4x4
    variables = [(i,j) for i in range(4) for j in range(4)]
    # Define el dominio de cada celda: números del 1 al 4
    dominios = {(i,j): list(range(1,5)) for i,j in variables}
    
    restricciones = []  # Lista de restricciones
    
    # Agrega restricciones de fila y columna
    for i in range(4):
        for j in range(4):
            for k in range(4):
                if k != j: restricciones.append(((i,j), (i,k)))
                if k != i: restricciones.append(((i,j), (k,j)))
    
    # Agrega restricciones de cajas 2x2
    for bi in [0,2]:
        for bj in [0,2]:
            caja = [(bi+i, bj+j) for i in range(2) for j in range(2)]
            for i, v1 in enumerate(caja):
                for v2 in caja[i+1:]:
                    restricciones.append((v1, v2))
    
    # Devuelve el objeto CSP construido
    return ProbabilisticCSP(variables, dominios, restricciones)

# Bloque principal que se ejecuta si el script se corre directamente
if __name__ == "__main__":
    # Fija la semilla aleatoria para reproducibilidad
    np.random.seed(42)
    random.seed(42)
    
    # Crea un sudoku con restricciones inciertas
    sudoku = crear_sudoku_4x4_incierto()
    
    # Define algunas pistas (valores predefinidos)
    pistas = {(0,0):1, (0,2):3, (1,1):4, (3,3):2}
    for (i,j), val in pistas.items():
        # Asigna la probabilidad de cada valor, favoreciendo la pista con 90%
        sudoku.prob_variables[(i,j)] = {
            v: 0.1/3 if v != val else 0.9 
            for v in sudoku.dominios[(i,j)]
        }
    
    # Resuelve el sudoku usando el CSP probabilístico
    solucion, energia = sudoku.solve(max_iter=1000)
    
    # Imprime la solución encontrada y su energía
    print("Solución encontrada (energía = {:.2f}):".format(energia))
    for i in range(4):
        print([solucion.get((i,j), 0) for j in range(4)])
    
    # Cuenta cuántas restricciones fueron violadas en la solución
    conflictos = 0
    for (i,j), (k,l) in sudoku.restricciones:
        if not cumple_restriccion(solucion.get((i,j), 0), solucion.get((k,l), 0)):
            conflictos += 1
    
    # Muestra resultados del desempeño
    print("\nNúmero de restricciones violadas:", conflictos)
    print("Tasa de éxito: {:.1f}%".format(
        (1 - conflictos/len(sudoku.restricciones)) * 100))
