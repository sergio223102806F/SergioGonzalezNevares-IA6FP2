# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 14:14:07 2025

@author: elvin
"""

import numpy as np
from collections import defaultdict
import random
from pgmpy.models import DynamicBayesianNetwork as DBN
from pgmpy.factors.discrete import TabularCPD

class DBN_CSP:
    def __init__(self, variables, dominios, restricciones):
        self.variables = variables
        self.dominios = dominios
        self.restricciones = restricciones
        self.vecinos = {v: set() for v in variables}
        for (v1, v2) in restricciones:
            self.vecinos[v1].add(v2)
            self.vecinos[v2].add(v1)
        
        # Mapeo de variables a índices para la DBN
        self.var_to_idx = {v: i for i, v in enumerate(variables)}
        self.idx_to_var = {i: v for v, i in self.var_to_idx.items()}
        
        # Inicializar la Red Bayesiana Dinámica
        self.initialize_dbn()

    def initialize_dbn(self):
        """Inicializa la estructura de la Red Bayesiana Dinámica"""
        self.dbn = DBN()
        
        # Añadir nodos para cada paso de tiempo
        for var in self.variables:
            self.dbn.add_node(f"{var}_0")  # Nodo en tiempo 0
            self.dbn.add_node(f"{var}_1")  # Nodo en tiempo 1
        
        # Añadir arcos intra-temporales (dependencias entre variables en mismo tiempo)
        for (v1, v2) in self.restricciones:
            self.dbn.add_edge(f"{v1}_0", f"{v2}_0")
            self.dbn.add_edge(f"{v1}_1", f"{v2}_1")
        
        # Añadir arcos inter-temporales (cómo evolucionan las variables)
        for var in self.variables:
            self.dbn.add_edge(f"{var}_0", f"{var}_1")
        
        # Crear CPDs (Distribuciones de Probabilidad Condicional)
        self.initialize_cpds()

    def initialize_cpds(self):
        """Inicializa las distribuciones de probabilidad condicional"""
        self.cpds = []
        n_values = len(next(iter(self.dominios.values())))  # Asumimos mismo tamaño de dominio
        
        # CPDs para tiempo 0 (distribución inicial)
        for var in self.variables:
            cpd = TabularCPD(
                variable=f"{var}_0",
                variable_card=n_values,
                values=[[1.0/n_values] for _ in range(n_values)],
                state_names={f"{var}_0": list(map(str, self.dominios[var]))}
            )
            self.cpds.append(cpd)
            self.dbn.add_cpds(cpd)
        
        # CPDs para tiempo 1 (transiciones y restricciones)
        for var in self.variables:
            # Obtener vecinos en el CSP
            neighbors = self.vecinos[var]
            
            # Crear matriz de transición considerando restricciones
            transition_table = np.zeros((n_values, n_values))
            
            for i, val in enumerate(self.dominios[var]):
                for j, new_val in enumerate(self.dominios[var]):
                    # Probabilidad de transición (favor valores consistentes)
                    conflict = any(not cumple_restriccion(new_val, self.dominios[vecino][k]) 
                                 for vecino in neighbors 
                                 for k in range(n_values))
                    transition_table[j][i] = 0.1 if conflict else 0.9
            
            # Normalizar filas
            transition_table = transition_table / transition_table.sum(axis=1, keepdims=True)
            
            cpd = TabularCPD(
                variable=f"{var}_1",
                variable_card=n_values,
                values=transition_table.T.tolist(),
                evidence=[f"{var}_0"],
                evidence_card=[n_values],
                state_names={
                    f"{var}_1": list(map(str, self.dominios[var])),
                    f"{var}_0": list(map(str, self.dominios[var]))
                }
            )
            self.cpds.append(cpd)
            self.dbn.add_cpds(cpd)
        
        # Verificar modelo
        self.dbn.check_model()

    def solve(self, steps=10, n_samples=100):
        """Resuelve el CSP usando inferencia en la DBN"""
        # Inferencia por muestreo
        from pgmpy.inference import DBNInference
        
        dbn_infer = DBNInference(self.dbn)
        
        # Muestrear trayectorias
        solutions = []
        for _ in range(n_samples):
            sample = self.sample_trajectory(dbn_infer, steps)
            if self.is_valid_solution(sample):
                solutions.append(sample)
        
        # Seleccionar la mejor solución
        if solutions:
            # Calcular puntuación basada en restricciones satisfechas
            scores = [self.solution_score(sol) for sol in solutions]
            best_solution = solutions[np.argmax(scores)]
            return best_solution
        else:
            # Si no se encontraron soluciones válidas, devolver la mejor parcial
            return self.get_best_partial_solution(dbn_infer, steps)

    def sample_trajectory(self, dbn_infer, steps):
        """Muestrea una trayectoria de la DBN"""
        samples = []
        current_state = {}
        
        for step in range(steps):
            # Muestrear del paso actual
            if step == 0:
                sample = {}
                for var in self.variables:
                    prob = dbn_infer.forward_inference([f"{var}_0"]).values
                    val = random.choices(self.dominios[var], weights=prob)[0]
                    sample[var] = val
            else:
                # Actualizar evidencia para el siguiente paso
                evidence = {f"{var}_0": str(current_state[var]) for var in self.variables}
                
                sample = {}
                for var in self.variables:
                    prob = dbn_infer.forward_inference(
                        [f"{var}_1"], 
                        evidence=evidence
                    ).values
                    val = random.choices(self.dominios[var], weights=prob)[0]
                    sample[var] = val
            
            samples.append(sample)
            current_state = sample
        
        # Devolver el último estado de la trayectoria
        return samples[-1]

    def is_valid_solution(self, solution):
        """Verifica si una solución es válida"""
        return all(consistente(var, solution[var], solution, self) 
               for var in self.variables)

    def solution_score(self, solution):
        """Calcula la puntuación de una solución"""
        return sum(consistente(var, solution[var], solution, self) 
               for var in self.variables)

    def get_best_partial_solution(self, dbn_infer, steps):
        """Obtiene la mejor solución parcial cuando no se encuentra una completa"""
        # Implementación simplificada - en la práctica se puede usar inferencia más sofisticada
        sample = self.sample_trajectory(dbn_infer, steps)
        return sample

def cumple_restriccion(valor1, valor2):
    """Función de restricción para el sudoku (valores diferentes)"""
    return valor1 != valor2

def consistente(var, valor, asignacion, csp):
    """Verifica consistencia de una asignación"""
    return all(cumple_restriccion(valor, asignacion[vecino])
              for vecino in csp.vecinos[var] if vecino in asignacion)

# Ejemplo: Sudoku 4x4
def crear_sudoku_4x4():
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
    
    return DBN_CSP(variables, dominios, restricciones)

if __name__ == "__main__":
    np.random.seed(42)
    random.seed(42)
    
    sudoku = crear_sudoku_4x4()
    
    # Asignar algunas pistas (evidencia fija)
    pistas = {(0,0):1, (0,2):3, (1,1):4, (3,3):2}
    for (i,j), val in pistas.items():
        # Fijar estas variables en la DBN (no muestrear sus valores)
        sudoku.dbn.add_cpds(TabularCPD(
            variable=f"({i},{j})_0",
            variable_card=4,
            values=[[1.0 if k == val-1 else 0.0 for k in range(4)]],
            state_names={f"({i},{j})_0": ['1','2','3','4']}
        ))
        sudoku.dbn.add_cpds(TabularCPD(
            variable=f"({i},{j})_1",
            variable_card=4,
            values=[[1.0 if k == val-1 else 0.0 for k in range(4)]],
            evidence=[f"({i},{j})_0"],
            evidence_card=[4],
            state_names={
                f"({i},{j})_1": ['1','2','3','4'],
                f"({i},{j})_0": ['1','2','3','4']
            }
        ))
    
    # Resolver con DBN
    solucion = sudoku.solve(steps=20, n_samples=1000)
    
    if solucion and sudoku.is_valid_solution(solucion):
        print("Solución encontrada:")
        for i in range(4):
            print([solucion.get((i,j), 0) for j in range(4)])
    else:
        print("Solución parcial encontrada:")
        for i in range(4):
            print([solucion.get((i,j), 0) for j in range(4)])
        print("Nota: La solución no satisface todas las restricciones")