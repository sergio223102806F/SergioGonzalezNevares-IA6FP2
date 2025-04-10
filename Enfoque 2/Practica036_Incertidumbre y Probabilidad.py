# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 14:24:39 2025

@author: elvin
"""

import numpy as np
from collections import defaultdict
import random
from itertools import product

class ProbabilisticCSP:
    def __init__(self, variables, dominios, restricciones):
        self.variables = variables
        self.dominios = dominios
        self.restricciones = restricciones
        self.vecinos = {v: set() for v in variables}
        for (v1, v2) in restricciones:
            self.vecinos[v1].add(v2)
            self.vecinos[v2].add(v1)
        
        # Modelamos incertidumbre en las restricciones
        self.prob_restricciones = self.initialize_constraint_probabilities()
        
        # Distribución de probabilidad inicial para cada variable
        self.prob_variables = {v: {val: 1/len(dominios[v]) for val in dominios[v]} 
                             for v in variables}

    def initialize_constraint_probabilities(self):
        """Inicializa probabilidades para cada restricción"""
        prob_restricciones = {}
        for (v1, v2) in self.restricciones:
            # Matriz de probabilidad: P(cumple | v1=a, v2=b)
            prob_restricciones[(v1, v2)] = np.ones((len(self.dominios[v1]), 
                                                 len(self.dominios[v2]))) * 0.9
            # 10% de probabilidad de que la restricción falle (incertidumbre)
        return prob_restricciones

    def solve(self, max_iter=100, temp_init=1.0, temp_end=0.01):
        """Resuelve el CSP probabilístico usando simulated annealing"""
        current_solution = {v: random.choice(list(self.dominios[v])) 
                          for v in self.variables}
        current_energy = self.energy(current_solution)
        
        best_solution = dict(current_solution)
        best_energy = current_energy
        
        for i in range(max_iter):
            temp = temp_init - (temp_init - temp_end) * (i / max_iter)
            
            # Seleccionar variable para cambiar
            var = self.select_variable(current_solution)
            
            # Generar nueva solución candidata
            new_solution = dict(current_solution)
            new_val = self.select_new_value(var, current_solution)
            new_solution[var] = new_val
            new_energy = self.energy(new_solution)
            
            # Criterio de aceptación
            if new_energy < current_energy or \
               random.random() < np.exp((current_energy - new_energy) / temp):
                current_solution = new_solution
                current_energy = new_energy
                
                if new_energy < best_energy:
                    best_solution = dict(new_solution)
                    best_energy = new_energy
        
        return best_solution, best_energy

    def select_variable(self, solution):
        """Selecciona variable basada en incertidumbre y conflictos"""
        # Variables con mayor incertidumbre en su valor actual
        uncertainty = {v: 1 - self.prob_variables[v][solution[v]] 
                      for v in self.variables}
        
        # Variables involucradas en restricciones más inciertas
        conflict = {v: sum(1 - self.prob_restricciones[(v, n)][solution[v]][solution[n]] 
                   for n in self.vecinos[v] if (v, n) in self.prob_restricciones)
                   for v in self.variables}
        
        # Combinar métricas
        scores = {v: uncertainty[v] + conflict[v] for v in self.variables}
        return max(scores.keys(), key=lambda x: scores[x])

    def select_new_value(self, var, solution):
        """Selecciona nuevo valor basado en probabilidades y restricciones"""
        # Calcular probabilidad para cada valor considerando restricciones
        probs = []
        for val in self.dominios[var]:
            prob = self.prob_variables[var][val]
            
            # Considerar restricciones con vecinos
            for neighbor in self.vecinos[var]:
                if (var, neighbor) in self.prob_restricciones:
                    neighbor_val = solution[neighbor]
                    prob *= self.prob_restricciones[(var, neighbor)][val][neighbor_val]
                elif (neighbor, var) in self.prob_restricciones:
                    neighbor_val = solution[neighbor]
                    prob *= self.prob_restricciones[(neighbor, var)][neighbor_val][val]
            
            probs.append(prob)
        
        # Normalizar probabilidades
        probs = np.array(probs)
        probs = probs / probs.sum()
        
        # Muestrear nuevo valor
        return random.choices(list(self.dominios[var]), weights=probs)[0]

    def energy(self, solution):
        """Calcula la energía (inverso de la probabilidad) de una solución"""
        # Probabilidad de la asignación
        prob = 1.0
        
        # Probabilidad de los valores individuales
        for var in self.variables:
            prob *= self.prob_variables[var][solution[var]]
        
        # Probabilidad de satisfacer restricciones
        for (v1, v2) in self.restricciones:
            val1 = solution[v1]
            val2 = solution[v2]
            prob *= self.prob_restricciones[(v1, v2)][val1][val2]
        
        # Energía es el negativo del logaritmo de la probabilidad
        return -np.log(prob + 1e-10)  # Evitar log(0)

    def update_probabilities(self, observations):
        """Actualiza probabilidades basado en observaciones"""
        for (v1, v2), satisfies in observations.items():
            val1 = observations['current_values'][v1]
            val2 = observations['current_values'][v2]
            
            # Actualizar probabilidad de restricción usando regla de Bayes
            alpha = 0.1  # Tasa de aprendizaje
            current_p = self.prob_restricciones[(v1, v2)][val1][val2]
            new_p = current_p * (1 - alpha) + satisfies * alpha
            self.prob_restricciones[(v1, v2)][val1][val2] = new_p
            
            # Mantener probabilidades en rango válido
            self.prob_restricciones[(v1, v2)] = np.clip(
                self.prob_restricciones[(v1, v2)], 0.01, 0.99)

def cumple_restriccion(valor1, valor2):
    """Función de restricción base (puede tener incertidumbre)"""
    return valor1 != valor2

# Ejemplo: Sudoku 4x4 con incertidumbre
def crear_sudoku_4x4_incierto():
    variables = [(i,j) for i in range(4) for j in range(4)]
    dominios = {(i,j): list(range(1,5)) for i,j in variables}
    
    restricciones = []
    # Filas y columnas
    for i in range(4):
        for j in range(4):
            for k in range(4):
                if k != j: restricciones.append(((i,j), (i,k)))
                if k != i: restricciones.append(((i,j), (k,j)))
    # Cajas 2x2
    for bi in [0,2]:
        for bj in [0,2]:
            caja = [(bi+i, bj+j) for i in range(2) for j in range(2)]
            for i, v1 in enumerate(caja):
                for v2 in caja[i+1:]:
                    restricciones.append((v1, v2))
    
    return ProbabilisticCSP(variables, dominios, restricciones)

if __name__ == "__main__":
    np.random.seed(42)
    random.seed(42)
    
    # Crear CSP con incertidumbre
    sudoku = crear_sudoku_4x4_incierto()
    
    # Introducir pistas con cierta probabilidad
    pistas = {(0,0):1, (0,2):3, (1,1):4, (3,3):2}
    for (i,j), val in pistas.items():
        # Fijar valores pero con cierta incertidumbre (90% de confianza)
        sudoku.prob_variables[(i,j)] = {v: 0.1/3 if v != val else 0.9 
                                      for v in sudoku.dominios[(i,j)]}
    
    # Resolver el CSP probabilístico
    solucion, energia = sudoku.solve(max_iter=1000)
    
    print("Solución encontrada (energía = {:.2f}):".format(energia))
    for i in range(4):
        print([solucion.get((i,j), 0) for j in range(4)])
    
    # Evaluar calidad de la solución
    conflictos = 0
    for (i,j), (k,l) in sudoku.restricciones:
        if not cumple_restriccion(solucion.get((i,j), 0), solucion.get((k,l), 0)):
            conflictos += 1
    
    print("\nNúmero de restricciones violadas:", conflictos)
    print("Tasa de éxito: {:.1f}%".format(
        (1 - conflictos/len(sudoku.restricciones)) * 100))