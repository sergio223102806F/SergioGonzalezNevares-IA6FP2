# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 13:28:09 2025

@author: elvin
"""

class CSP:
    def __init__(self, variables, dominios, restricciones):
        self.variables = variables      # Lista de variables
        self.dominios = dominios        # Diccionario {variable: [valores]}
        self.restricciones = restricciones  # Lista de tuplas (var1, var2)
        self.vecinos = {v: set() for v in variables}
        for (v1, v2) in restricciones:
            self.vecinos[v1].add(v2)
            self.vecinos[v2].add(v1)

def backtracking(asignacion, csp):
    if len(asignacion) == len(csp.variables):
        return asignacion
    
    var = seleccionar_variable_no_asignada(asignacion, csp)
    for valor in orden_valores(var, asignacion, csp):
        if es_consistente(var, valor, asignacion, csp):
            asignacion[var] = valor
            resultado = backtracking(asignacion, csp)
            if resultado is not None:
                return resultado
            del asignacion[var]
    return None

def seleccionar_variable_no_asignada(asignacion, csp):
    # Heurística MRV (Minimum Remaining Values)
    no_asignadas = [v for v in csp.variables if v not in asignacion]
    return min(no_asignadas, key=lambda v: len(csp.dominios[v]))

def orden_valores(var, asignacion, csp):
    # Heurística LCV (Least Constraining Value)
    return sorted(csp.dominios[var],
                key=lambda v: contar_conflictos(var, v, asignacion, csp))

def contar_conflictos(var, valor, asignacion, csp):
    total = 0
    for vecino in csp.vecinos[var]:
        if vecino in asignacion and not cumple_restriccion(valor, asignacion[vecino]):
            total += 1
    return total

def cumple_restriccion(valor1, valor2):
    # Restricción genérica (personalizar según problema)
    return valor1 != valor2

def es_consistente(var, valor, asignacion, csp):
    for vecino in csp.vecinos[var]:
        if vecino in asignacion and not cumple_restriccion(valor, asignacion[vecino]):
            return False
    return True

# Ejemplo: Sudoku 4x4
def crear_sudoku_4x4():
    variables = [(i,j) for i in range(4) for j in range(4)]
    dominios = {(i,j): list(range(1,5)) for i,j in variables}
    
    # Restricciones: filas, columnas y cajas 2x2
    restricciones = []
    for i in range(4):
        for j in range(4):
            for k in range(4):
                if k != j: restricciones.append(((i,j), (i,k)))  # Misma fila
                if k != i: restricciones.append(((i,j), (k,j)))  # Misma columna
    
    # Cajas 2x2
    for bi in [0,2]:
        for bj in [0,2]:
            for i in range(2):
                for j in range(2):
                    for k in range(2):
                        for l in range(2):
                            if (i,j) != (k,l):
                                restricciones.append(((bi+i, bj+j), (bi+k, bj+l)))
    
    return CSP(variables, dominios, restricciones)

# Uso
sudoku = crear_sudoku_4x4()
# Asignar pistas (valores fijos)
sudoku.dominios[(0,0)] = [1]
sudoku.dominios[(0,2)] = [3]
sudoku.dominios[(1,1)] = [4]
sudoku.dominios[(3,3)] = [2]

solucion = backtracking({}, sudoku)

# Mostrar solución
for i in range(4):
    print([solucion[(i,j)] for j in range(4)])