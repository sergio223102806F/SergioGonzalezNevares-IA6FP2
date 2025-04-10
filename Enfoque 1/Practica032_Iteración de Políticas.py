# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 13:59:11 2025

@author: elvin
"""

import networkx as nx
from collections import defaultdict

class CSP:
    def __init__(self, variables, dominios, restricciones):
        self.variables = variables
        self.dominios = dominios
        self.restricciones = restricciones
        self.vecinos = {v: set() for v in variables}
        for (v1, v2) in restricciones:
            self.vecinos[v1].add(v2)
            self.vecinos[v2].add(v1)

def policy_iteration_csp(csp, max_iter=100, tol=1e-4):
    """Resuelve un CSP usando Iteración de Políticas"""
    # Inicialización de la política (asignación inicial)
    politica = {var: random.choice(csp.dominios[var]) for var in csp.variables}
    
    for _ in range(max_iter):
        # Paso de Evaluación: Calcular qué tan buena es la política actual
        valores = evaluate_policy(politica, csp)
        
        # Paso de Mejora: Actualizar la política basada en los valores
        politica_mejorada, policy_changed = improve_policy(politica, valores, csp)
        
        # Verificar convergencia
        if not policy_changed:
            break
            
        politica = politica_mejorada
    
    # Verificar si la política final es solución válida
    if all(consistente(var, politica[var], politica, csp) 
           for var in csp.variables):
        return politica
    else:
        # Si no es solución válida, usar backtracking con política como heurística
        return backtracking_policy_guided({}, csp, politica)

def evaluate_policy(politica, csp):
    """Evalúa la política actual asignando valores a cada variable"""
    valores = defaultdict(float)
    
    # Calcular el número de restricciones satisfechas para cada variable
    for var in csp.variables:
        val = politica[var]
        conflictos = sum(1 for vecino in csp.vecinos[var] 
                      if not cumple_restriccion(val, politica[vecino]))
        valores[var] = 1.0 / (1.0 + conflictos)  # Valor más alto = mejor
    
    return valores

def improve_policy(politica, valores, csp):
    """Mejora la política basada en los valores calculados"""
    nueva_politica = {}
    policy_changed = False
    
    for var in csp.variables:
        # Encontrar el mejor valor para esta variable considerando los vecinos
        best_val = None
        best_score = -float('inf')
        
        for val in csp.dominios[var]:
            # Calcular puntuación para este valor
            score = 0
            for vecino in csp.vecinos[var]:
                # Asumimos que los vecinos mantienen su valor actual
                if cumple_restriccion(val, politica[vecino]):
                    score += valores[vecino]
            
            if score > best_score or (score == best_score and random.random() < 0.1):
                best_score = score
                best_val = val
        
        nueva_politica[var] = best_val
        if best_val != politica[var]:
            policy_changed = True
    
    return nueva_politica, policy_changed

def backtracking_policy_guided(asignacion, csp, politica):
    """Backtracking guiado por la política"""
    if len(asignacion) == len(csp.variables):
        return asignacion
    
    # Seleccionar variable no asignada con el dominio más restringido
    var = min([v for v in csp.variables if v not in asignacion],
              key=lambda v: len(csp.dominios[v]))
    
    # Ordenar valores según su proximidad al valor de la política
    valores_ordenados = sorted(csp.dominios[var],
                             key=lambda val: abs(val - politica[var]))
    
    for valor in valores_ordenados:
        if consistente(var, valor, asignacion, csp):
            asignacion[var] = valor
            resultado = backtracking_policy_guided(asignacion, csp, politica)
            if resultado is not None:
                return resultado
            del asignacion[var]
    return None

def consistente(var, valor, asignacion, csp):
    return all(cumple_restriccion(valor, asignacion[vecino])
              for vecino in csp.vecinos[var] if vecino in asignacion)

def cumple_restriccion(valor1, valor2):
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
    
    return CSP(variables, dominios, restricciones)

# Ejemplo de uso
if __name__ == "__main__":
    import random
    
    sudoku = crear_sudoku_4x4()
    
    # Asignar algunas pistas
    pistas = {(0,0):1, (0,2):3, (1,1):4, (3,3):2}
    for (i,j), val in pistas.items():
        sudoku.dominios[(i,j)] = [val]
    
    # Resolver con Iteración de Políticas
    solucion = policy_iteration_csp(sudoku)
    
    if solucion:
        print("Solución encontrada:")
        for i in range(4):
            print([solucion[(i,j)] for j in range(4)])
    else:
        print("No se encontró solución")