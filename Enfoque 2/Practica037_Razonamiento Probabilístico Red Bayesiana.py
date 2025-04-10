# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 14:24:39 2025

@author: elvin
"""

import numpy as np
from collections import defaultdict
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
import networkx as nx
import matplotlib.pyplot as plt

class BayesianCSP:
    def __init__(self, variables, dominios, restricciones):
        self.variables = variables
        self.dominios = dominios
        self.restricciones = restricciones
        self.vecinos = {v: set() for v in variables}
        for (v1, v2) in restricciones:
            self.vecinos[v1].add(v2)
            self.vecinos[v2].add(v1)
        
        # Crear la red bayesiana
        self.model = self.build_bayesian_network()
        
    def build_bayesian_network(self):
        """Construye la red bayesiana para el CSP"""
        model = BayesianNetwork()
        
        # Añadir nodos para las variables del CSP
        model.add_nodes_from(self.variables)
        
        # Añadir arcos basados en las restricciones
        for (v1, v2) in self.restricciones:
            model.add_edge(v1, v2)
        
        # Definir las distribuciones de probabilidad condicional (CPDs)
        cpds = []
        for var in self.variables:
            # Si no tiene padres (variables no condicionadas)
            if len(model.get_parents(var)) == 0:
                cpd = TabularCPD(
                    variable=var,
                    variable_card=len(self.dominios[var]),
                    values=[[1.0/len(self.dominios[var]) for _ in self.dominios[var]]],
                    state_names={var: list(map(str, self.dominios[var]))}
                )
            else:
                # Construir CPD considerando las restricciones
                parents = list(model.get_parents(var))
                parent_cards = [len(self.dominios[p]) for p in parents]
                
                # Crear matriz de probabilidad condicional
                prob_table = []
                for val in self.dominios[var]:
                    row = []
                    # Generar todas las combinaciones de valores de los padres
                    for parent_vals in product(*[self.dominios[p] for p in parents]):
                        # Calcular probabilidad basada en satisfacción de restricciones
                        satisfies = all(cumple_restriccion(val, parent_vals[i]) 
                                      for i, p in enumerate(parents) 
                                      if (p, var) in self.restricciones or (var, p) in self.restricciones)
                        prob = 0.9 if satisfies else 0.1  # 90% de probabilidad si satisface restricciones
                        row.append(prob)
                    
                    # Normalizar la fila
                    row_sum = sum(row)
                    normalized_row = [p/row_sum for p in row]
                    prob_table.append(normalized_row)
                
                cpd = TabularCPD(
                    variable=var,
                    variable_card=len(self.dominios[var]),
                    values=prob_table,
                    evidence=parents,
                    evidence_card=parent_cards,
                    state_names={var: list(map(str, self.dominios[var])) | 
                                 {p: list(map(str, self.dominios[p])) for p in parents}
                )
            cpds.append(cpd)
        
        # Añadir CPDs al modelo
        model.add_cpds(*cpds)
        
        # Verificar que el modelo es válido
        assert model.check_model(), "La red bayesiana no es válida"
        
        return model
    
    def solve(self, evidence=None):
        """Resuelve el CSP usando inferencia probabilística"""
        if evidence is None:
            evidence = {}
        
        # Convertir evidencia al formato correcto
        formatted_evidence = {k: str(v) for k, v in evidence.items()}
        
        # Crear el objeto de inferencia
        infer = VariableElimination(self.model)
        
        # Realizar inferencia para cada variable
        solution = {}
        for var in self.variables:
            if var in evidence:
                solution[var] = evidence[var]
            else:
                # Calcular distribución posterior
                posterior = infer.query(variables=[var], evidence=formatted_evidence)
                # Seleccionar el valor más probable
                solution[var] = int(posterior.state_names[var][np.argmax(posterior.values)])
        
        return solution
    
    def visualize_network(self):
        """Visualiza la estructura de la red bayesiana"""
        nx.draw(self.model, with_labels=True, node_size=2000, node_color='skyblue', 
               font_size=10, font_weight='bold', arrowsize=20)
        plt.title("Red Bayesiana del CSP")
        plt.show()

def cumple_restriccion(valor1, valor2):
    """Función de restricción para el sudoku (valores diferentes)"""
    return valor1 != valor2

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
    
    return BayesianCSP(variables, dominios, restricciones)

if __name__ == "__main__":
    # Crear CSP probabilístico
    sudoku = crear_sudoku_4x4()
    
    # Visualizar la red (opcional)
    # sudoku.visualize_network()
    
    # Definir evidencia (pistas)
    pistas = {(0,0):1, (0,2):3, (1,1):4, (3,3):2}
    
    # Resolver usando inferencia bayesiana
    solucion = sudoku.solve(evidence=pistas)
    
    # Mostrar solución
    print("Solución encontrada:")
    for i in range(4):
        print([solucion.get((i,j), 0) for j in range(4)])
    
    # Evaluar solución
    conflictos = 0
    for (v1, v2) in sudoku.restricciones:
        if not cumple_restriccion(solucion[v1], solucion[v2]):
            conflictos += 1
    
    print("\nRestricciones violadas:", conflictos)
    print("Tasa de satisfacción: {:.1f}%".format(
        (1 - conflictos/len(sudoku.restricciones)) * 100))
    
    # Mostrar probabilidades posteriores para una celda específica
    infer = VariableElimination(sudoku.model)
    posterior = infer.query(variables=[(1,0)], evidence={k: str(v) for k, v in pistas.items()})
    print("\nDistribución posterior para celda (1,0):")
    for val, prob in zip(posterior.state_names[(1,0)], posterior.values):
        print(f"Valor {val}: {prob:.3f}")