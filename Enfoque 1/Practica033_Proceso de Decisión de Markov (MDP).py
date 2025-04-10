# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 14:13:41 2025

@author: elvin
"""

import numpy as np
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

def mdp_solve_csp(csp, gamma=0.9, max_iter=100, tol=1e-4):
    """Resuelve un CSP modelándolo como un MDP"""
    # Estados: asignaciones parciales o completas
    # Acciones: asignar un valor a una variable no asignada
    
    # Inicializar función de valor
    V = defaultdict(float)
    
    # Modelamos las recompensas: +1 por restricción satisfecha, -1 por conflicto
    def recompensa(asignacion, var, val):
        conflictos = sum(1 for vecino in csp.vecinos[var] 
                      if vecino in asignacion and not cumple_restriccion(val, asignacion[vecino]))
        return -conflictos
    
    for _ in range(max_iter):
        delta = 0
        # Iteración de políticas para actualizar V
        for var in csp.variables:
            for val in csp.dominios[var]:
                # Simular asignación y calcular recompensa esperada
                # (Aquí simplificamos el modelo MDP completo)
                old_v = V[(var, val)]
                max_q = -float('inf')
                
                # Considerar el mejor valor para los vecinos
                for vecino in csp.vecinos[var]:
                    for vec_val in csp.dominios[vecino]:
                        if cumple_restriccion(val, vec_val):
                            q_val = recompensa({var: val}, vecino, vec_val) + gamma * V[(vecino, vec_val)]
                            if q_val > max_q:
                                max_q = q_val
                
                if csp.vecinos[var]:
                    V[(var, val)] = recompensa({}, var, val) + gamma * (max_q if max_q != -float('inf') else 0)
                else:
                    V[(var, val)] = recompensa({}, var, val)
                
                delta = max(delta, abs(V[(var, val)] - old_v))
        
        if delta < tol:
            break
    
    # Extraer la política óptima (asignación de valores)
    politica = {}
    for var in csp.variables:
        best_val = max(csp.dominios[var], key=lambda val: V[(var, val)])
        politica[var] = best_val
    
    # Verificar si la política es solución válida
    if all(consistente(var, politica[var], politica, csp) for var in csp.variables):
        return politica
    else:
        # Si no es solución válida, usar backtracking con valores V como heurística
        return mdp_backtracking({}, csp, V)

def mdp_backtracking(asignacion, csp, V):
    """Backtracking usando los valores del MDP como heurística"""
    if len(asignacion) == len(csp.variables):
        return asignacion
    
    # Seleccionar variable no asignada con mayor impacto (según V)
    var = max([v for v in csp.variables if v not in asignacion],
             key=lambda v: max(V[(v, val)] for val in csp.dominios[v]))
    
    # Ordenar valores por su valor V
    valores_ordenados = sorted(csp.dominios[var], key=lambda val: -V[(var, val)])
    
    for valor in valores_ordenados:
        if consistente(var, valor, asignacion, csp):
            asignacion[var] = valor
            resultado = mdp_backtracking(asignacion, csp, V)
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

if __name__ == "__main__":
    sudoku = crear_sudoku_4x4()
    
    # Asignar algunas pistas
    pistas = {(0,0):1, (0,2):3, (1,1):4, (3,3):2}
    for (i,j), val in pistas.items():
        sudoku.dominios[(i,j)] = [val]
    
    # Resolver con MDP
    solucion = mdp_solve_csp(sudoku)
    
    if solucion:
        print("Solución encontrada:")
        for i in range(4):
            print([solucion[(i,j)] for j in range(4)])
    else:
        print("No se encontró solución")