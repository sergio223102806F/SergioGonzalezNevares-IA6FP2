# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 14:14:07 2025

@author: elvin
"""

import numpy as np                   # Importa numpy para operaciones numéricas
from collections import defaultdict  # Importa defaultdict para diccionarios por defecto
import random                       # Importa random para generación aleatoria
from pgmpy.models import DynamicBayesianNetwork as DBN  # Importa DBN de pgmpy
from pgmpy.factors.discrete import TabularCPD          # Importa CPDs tabulares

class DBN_CSP:                      # Clase para CSP con Red Bayesiana Dinámica
    def __init__(self, variables, dominios, restricciones):
        """Constructor que inicializa el DBN-CSP:
        variables: Lista de variables del problema
        dominios: Diccionario {variable: valores_posibles}
        restricciones: Lista de tuplas de variables con restricciones
        """
        self.variables = variables   # Almacena las variables del problema
        self.dominios = dominios     # Almacena los dominios de cada variable
        self.restricciones = restricciones  # Almacena las restricciones
        
        # Diccionario de vecinos para cada variable
        self.vecinos = {v: set() for v in variables}  # Inicializa conjuntos vacíos
        for (v1, v2) in restricciones:  # Para cada restricción
            self.vecinos[v1].add(v2)    # Añade v2 como vecino de v1
            self.vecinos[v2].add(v1)    # Añade v1 como vecino de v2 (no dirigido)
        
        # Mapeo de variables a índices para la DBN
        self.var_to_idx = {v: i for i, v in enumerate(variables)}  # Variable -> índice
        self.idx_to_var = {i: v for v, i in self.var_to_idx.items()}  # Índice -> variable
        
        # Inicializar la Red Bayesiana Dinámica
        self.initialize_dbn()        # Configura estructura y parámetros de la DBN

    def initialize_dbn(self):
        """Inicializa la estructura de la Red Bayesiana Dinámica"""
        self.dbn = DBN()            # Crea una nueva DBN vacía
        
        # Añadir nodos para cada paso de tiempo (t=0 y t=1)
        for var in self.variables:   # Para cada variable en el CSP
            self.dbn.add_node(f"{var}_0")  # Nodo en tiempo 0
            self.dbn.add_node(f"{var}_1")  # Nodo en tiempo 1
        
        # Añadir arcos intra-temporales (dependencias entre variables en mismo tiempo)
        for (v1, v2) in self.restricciones:  # Para cada restricción en el CSP
            self.dbn.add_edge(f"{v1}_0", f"{v2}_0")  # Dependencia en tiempo 0
            self.dbn.add_edge(f"{v1}_1", f"{v2}_1")  # Dependencia en tiempo 1
        
        # Añadir arcos inter-temporales (cómo evolucionan las variables)
        for var in self.variables:   # Para cada variable
            self.dbn.add_edge(f"{var}_0", f"{var}_1")  # Dependencia temporal
        
        # Crear CPDs (Distribuciones de Probabilidad Condicional)
        self.initialize_cpds()       # Inicializa las distribuciones de probabilidad

    def initialize_cpds(self):
        """Inicializa las distribuciones de probabilidad condicional"""
        self.cpds = []              # Lista para almacenar todas las CPDs
        n_values = len(next(iter(self.dominios.values())))  # Tamaño del dominio (asumimos igual)
        
        # CPDs para tiempo 0 (distribución inicial)
        for var in self.variables:   # Para cada variable
            cpd = TabularCPD(        # Crea CPD tabular
                variable=f"{var}_0",  # Variable objetivo
                variable_card=n_values,  # Número de valores posibles
                values=[[1.0/n_values] for _ in range(n_values)],  # Distribución uniforme
                state_names={f"{var}_0": list(map(str, self.dominios[var]))}  # Nombres estados
            )
            self.cpds.append(cpd)    # Añade CPD a la lista
            self.dbn.add_cpds(cpd)   # Añade CPD a la DBN
        
        # CPDs para tiempo 1 (transiciones y restricciones)
        for var in self.variables:   # Para cada variable
            neighbors = self.vecinos[var]  # Obtiene vecinos en el CSP
            
            # Crear matriz de transición considerando restricciones
            transition_table = np.zeros((n_values, n_values))  # Inicializa matriz
            
            for i, val in enumerate(self.dominios[var]):  # Para cada valor actual
                for j, new_val in enumerate(self.dominios[var]):  # Para cada nuevo valor
                    # Verificar conflictos con vecinos
                    conflict = any(not cumple_restriccion(new_val, self.dominios[vecino][k]) 
                                 for vecino in neighbors 
                                 for k in range(n_values))
                    # Asignar probabilidad según consistencia
                    transition_table[j][i] = 0.1 if conflict else 0.9
            
            # Normalizar filas para que sumen 1
            transition_table = transition_table / transition_table.sum(axis=1, keepdims=True)
            
            # Crear CPD para la transición
            cpd = TabularCPD(
                variable=f"{var}_1",  # Variable objetivo
                variable_card=n_values,  # Número de valores
                values=transition_table.T.tolist(),  # Valores de transición
                evidence=[f"{var}_0"],  # Variable de evidencia
                evidence_card=[n_values],  # Número de valores de evidencia
                state_names={            # Nombres de estados
                    f"{var}_1": list(map(str, self.dominios[var])),
                    f"{var}_0": list(map(str, self.dominios[var]))
                }
            )
            self.cpds.append(cpd)    # Añade CPD a la lista
            self.dbn.add_cpds(cpd)   # Añade CPD a la DBN
        
        # Verificar que el modelo es correcto
        self.dbn.check_model()       # Valida la estructura y parámetros

    def solve(self, steps=10, n_samples=100):
        """Resuelve el CSP usando inferencia en la DBN:
        steps: Número de pasos temporales
        n_samples: Número de muestras a generar
        """
        from pgmpy.inference import DBNInference  # Importa inferencia para DBN
        
        dbn_infer = DBNInference(self.dbn)  # Crea objeto para inferencia
        
        # Muestrear trayectorias para encontrar soluciones
        solutions = []               # Lista para almacenar soluciones válidas
        for _ in range(n_samples):   # Generar n_samples muestras
            sample = self.sample_trajectory(dbn_infer, steps)  # Muestrea trayectoria
            if self.is_valid_solution(sample):  # Si es solución válida
                solutions.append(sample)  # Añade a soluciones
        
        # Seleccionar la mejor solución encontrada
        if solutions:                # Si se encontraron soluciones válidas
            # Calcular puntuación basada en restricciones satisfechas
            scores = [self.solution_score(sol) for sol in solutions]
            best_solution = solutions[np.argmax(scores)]  # Selecciona mejor
            return best_solution
        else:
            # Si no hay soluciones válidas, devolver la mejor parcial
            return self.get_best_partial_solution(dbn_infer, steps)

    def sample_trajectory(self, dbn_infer, steps):
        """Muestrea una trayectoria de la DBN:
        dbn_infer: Objeto de inferencia para DBN
        steps: Número de pasos temporales
        """
        samples = []                 # Almacena todos los estados muestreados
        current_state = {}           # Estado actual durante el muestreo
        
        for step in range(steps):    # Para cada paso temporal
            if step == 0:            # Primer paso (sin evidencia previa)
                sample = {}          # Diccionario para el estado muestreado
                for var in self.variables:  # Para cada variable
                    # Inferir distribución para esta variable
                    prob = dbn_infer.forward_inference([f"{var}_0"]).values
                    # Muestrear valor según distribución
                    val = random.choices(self.dominios[var], weights=prob)[0]
                    sample[var] = val  # Almacena valor muestreado
            else:                    # Pasos subsiguientes
                # Crear evidencia del estado anterior
                evidence = {f"{var}_0": str(current_state[var]) for var in self.variables}
                
                sample = {}          # Nuevo estado a muestrear
                for var in self.variables:  # Para cada variable
                    # Inferir distribución dado el estado anterior
                    prob = dbn_infer.forward_inference(
                        [f"{var}_1"], 
                        evidence=evidence
                    ).values
                    # Muestrear nuevo valor
                    val = random.choices(self.dominios[var], weights=prob)[0]
                    sample[var] = val  # Almacena valor muestreado
            
            samples.append(sample)   # Añade estado a la trayectoria
            current_state = sample  # Actualiza estado actual
        
        return samples[-1]          # Devuelve el último estado muestreado

    def is_valid_solution(self, solution):
        """Verifica si una solución es válida:
        solution: Asignación a verificar
        """
        return all(consistente(var, solution[var], solution, self) 
               for var in self.variables)

    def solution_score(self, solution):
        """Calcula la puntuación de una solución:
        solution: Asignación a evaluar
        """
        return sum(consistente(var, solution[var], solution, self) 
               for var in self.variables)

    def get_best_partial_solution(self, dbn_infer, steps):
        """Obtiene la mejor solución parcial cuando no se encuentra una completa:
        dbn_infer: Objeto de inferencia para DBN
        steps: Número de pasos temporales
        """
        sample = self.sample_trajectory(dbn_infer, steps)  # Muestrea trayectoria
        return sample                 # Devuelve la muestra (puede mejorarse)

def cumple_restriccion(valor1, valor2):
    """Función de restricción para el sudoku (valores diferentes):
    valor1: Primer valor a comparar
    valor2: Segundo valor a comparar
    """
    return valor1 != valor2           # Restricción básica de desigualdad

def consistente(var, valor, asignacion, csp):
    """Verifica consistencia de una asignación:
    var: Variable asignada
    valor: Valor asignado
    asignacion: Asignación parcial actual
    csp: Instancia del problema CSP
    """
    return all(cumple_restriccion(valor, asignacion[vecino])
              for vecino in csp.vecinos[var] if vecino in asignacion)

# Ejemplo: Sudoku 4x4
def crear_sudoku_4x4():
    """Crea una instancia de Sudoku 4x4 como DBN_CSP"""
    variables = [(i,j) for i in range(4) for j in range(4)]  # 16 celdas
    dominios = {(i,j): list(range(1,5)) for i,j in variables}  # Valores 1-4
    
    restricciones = []
    # Restricciones de filas y columnas
    for i in range(4):
        for j in range(4):
            for k in range(4):
                if k != j: restricciones.append(((i,j), (i,k)))  # Misma fila
                if k != i: restricciones.append(((i,j), (k,j)))  # Misma columna
    # Restricciones de cajas 2x2
    for bi in [0,2]:
        for bj in [0,2]:
            caja = [(bi+i, bj+j) for i in range(2) for j in range(2)]
            for i, v1 in enumerate(caja):
                for v2 in caja[i+1:]:
                    restricciones.append((v1, v2))  # Misma caja
    
    return DBN_CSP(variables, dominios, restricciones)  # Retorna instancia DBN_CSP

if __name__ == "__main__":            # Bloque principal de ejecución
    np.random.seed(42)                # Fija semilla para reproducibilidad
    random.seed(42)                   # Fija semilla para aleatoriedad
    
    sudoku = crear_sudoku_4x4()       # Crea instancia de Sudoku
    
    # Asignar algunas pistas (evidencia fija)
    pistas = {(0,0):1, (0,2):3, (1,1):4, (3,3):2}
    for (i,j), val in pistas.items():
        # Fijar estas variables en la DBN (distribución determinista)
        sudoku.dbn.add_cpds(TabularCPD(
            variable=f"({i},{j})_0",  # Variable en tiempo 0
            variable_card=4,          # 4 valores posibles (1-4)
            values=[[1.0 if k == val-1 else 0.0 for k in range(4)]],  # Probabilidades
            state_names={f"({i},{j})_0": ['1','2','3','4']}  # Nombres de estados
        ))
        sudoku.dbn.add_cpds(TabularCPD(
            variable=f"({i},{j})_1",  # Variable en tiempo 1
            variable_card=4,          # 4 valores posibles
            values=[[1.0 if k == val-1 else 0.0 for k in range(4)]],  # Probabilidades
            evidence=[f"({i},{j})_0"],  # Depende de su valor en t=0
            evidence_card=[4],        # 4 valores posibles de evidencia
            state_names={            # Nombres de estados
                f"({i},{j})_1": ['1','2','3','4'],
                f"({i},{j})_0": ['1','2','3','4']
            }
        ))
    
    # Resolver con DBN
    solucion = sudoku.solve(steps=20, n_samples=1000)  # Ejecuta algoritmo
    
    # Mostrar resultados
    if solucion and sudoku.is_valid_solution(solucion):
        print("Solución encontrada:")
        for i in range(4):            # Imprime solución como matriz 4x4
            print([solucion.get((i,j), 0) for j in range(4)])
    else:
        print("Solución parcial encontrada:")
        for i in range(4):            # Imprime solución parcial
            print([solucion.get((i,j), 0) for j in range(4)])
        print("Nota: La solución no satisface todas las restricciones")