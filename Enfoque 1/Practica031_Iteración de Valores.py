# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 13:48:25 2025

@author: elvin
"""

import networkx as nx
from collections import deque

class CSP:
    def __init__(self, variables, dominios, restricciones):
        self.variables = variables
        self.dominios = dominios
        self.restricciones = restricciones
        self.vecinos = {v: set() for v in variables}
        for (v1, v2) in restricciones:
            self.vecinos[v1].add(v2)
            self.vecinos[v2].add(v1)

def value_iteration_csp(csp, max_iter=100, tol=1e-4):
    """Resuelve un CSP usando Iteración de Valores"""
    # Inicializar valores (probabilidades o puntuaciones) para cada asignación
    values = {
        var: {val: 1.0 for val in csp.dominios[var]}
        for var in csp.variables
    }
    
    for _ in range(max_iter):
        delta = 0
        new_values = {var: {} for var in csp.variables}
        
        # Actualizar valores para cada variable
        for var in csp.variables:
            for val in csp.dominios[var]:
                # Calcular nuevo valor basado en los vecinos
                total = 0
                for vecino in csp.vecinos[var]:
                    # Sumar la consistencia con cada asignación posible del vecino
                    for vec_val in csp.dominios[vecino]:
                        if cumple_restriccion(val, vec_val):
                            total += values[vecino][vec_val]
                
                # Normalizar (promedio de consistencia con vecinos)
                new_val = total / max(1, len(csp.dominios[var]) * len(csp.vecinos[var]))
                new_values[var][val] = new_val
                delta = max(delta, abs(new_val - values[var][val]))
        
        values = new_values
        
        # Verificar convergencia
        if delta < tol:
            break
    
    # Seleccionar la asignación más probable
    asignacion = {
        var: max(values[var].items(), key=lambda x: x[1])[0]
        for var in csp.variables
    }
    
    # Verificar si la asignación es consistente
    if all(consistente(var, asignacion[var], asignacion, csp)
           for var in csp.variables):
        return asignacion
    else:
        # Si no es consistente, usar backtracking con los valores como heurística
        return backtracking_value_guided({}, csp, values)

def backtracking_value_guided(asignacion, csp, values):
    """Backtracking guiado por los valores de iteración"""
    if len(asignacion) == len(csp.variables):
        return asignacion
    
    # Seleccionar variable no asignada con el dominio más restringido
    var = min([v for v in csp.variables if v not in asignacion],
              key=lambda v: len(csp.dominios[v]))
    
    # Ordenar valores por su score de la iteración de valores
    valores_ordenados = sorted(csp.dominios[var],
                              key=lambda val: -values[var][val])
    
    for valor in valores_ordenados:
        if consistente(var, valor, asignacion, csp):
            asignacion[var] = valor
            resultado = backtracking_value_guided(asignacion, csp, values)
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
    sudoku = crear_sudoku_4x4()
    
    # Asignar algunas pistas
    pistas = {(0,0):1, (0,2):3, (1,1):4, (3,3):2}
    for (i,j), val in pistas.items():
        sudoku.dominios[(i,j)] = [val]
    
    # Resolver con Iteración de Valores
    solucion = value_iteration_csp(sudoku)
    
    if solucion:
        print("Solución encontrada:")
        for i in range(4):
            print([solucion[(i,j)] for j in range(4)])
    else:
        print("No se encontró solución")