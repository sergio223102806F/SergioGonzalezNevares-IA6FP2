# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 13:34:57 2025

@author: elvin
"""

import random

class CSP:
    def __init__(self, variables, dominios, restricciones):
        self.variables = variables
        self.dominios = dominios
        self.restricciones = restricciones
        self.vecinos = {v: set() for v in variables}
        for (v1, v2) in restricciones:
            self.vecinos[v1].add(v2)
            self.vecinos[v2].add(v1)

def minimos_conflictos(csp, max_iter=1000):
    """Algoritmo de mínimos conflictos"""
    # Asignación inicial aleatoria (respetando pistas fijas)
    asignacion = {}
    for var in csp.variables:
        if len(csp.dominios[var]) == 1:  # Pista fija
            asignacion[var] = csp.dominios[var][0]
        else:
            asignacion[var] = random.choice(csp.dominios[var])
    
    for _ in range(max_iter):
        conflicto_vars = [v for v in csp.variables if contar_conflictos(v, asignacion[v], asignacion, csp) > 0]
        
        if not conflicto_vars:
            return asignacion  # Solución encontrada
        
        # Seleccionar variable conflictiva aleatoria
        var = random.choice(conflicto_vars)
        
        # Seleccionar valor que minimiza conflictos
        valores_ordenados = sorted(csp.dominios[var],
                                 key=lambda v: contar_conflictos(var, v, asignacion, csp))
        mejor_valor = valores_ordenados[0]
        asignacion[var] = mejor_valor
    
    return None  # No se encontró solución en max_iter

def contar_conflictos(var, valor, asignacion, csp):
    """Cuenta cuántas restricciones viola esta asignación"""
    return sum(1 for vecino in csp.vecinos[var] 
              if vecino in asignacion and not cumple_restriccion(valor, asignacion[vecino]))

def cumple_restriccion(valor1, valor2):
    """Función de restricción para Sudoku (valores diferentes)"""
    return valor1 != valor2

# Ejemplo: Sudoku 9x9
def crear_sudoku_9x9():
    variables = [(i,j) for i in range(9) for j in range(9)]
    dominios = {(i,j): list(range(1,10)) for i,j in variables}
    
    restricciones = []
    # Restricciones de fila y columna
    for i in range(9):
        for j in range(9):
            for k in range(9):
                if k != j: restricciones.append(((i,j), (i,k)))
                if k != i: restricciones.append(((i,j), (k,j)))
    # Restricciones de caja 3x3
    for bi in range(0,9,3):
        for bj in range(0,9,3):
            caja = [(bi+i, bj+j) for i in range(3) for j in range(3)]
            for i, v1 in enumerate(caja):
                for v2 in caja[i+1:]:
                    restricciones.append((v1, v2))
    
    return CSP(variables, dominios, restricciones)

# Ejemplo de uso
if __name__ == "__main__":
    sudoku = crear_sudoku_9x9()
    
    # Asignar pistas fijas (ejemplo medio)
    pistas = {
        (0,0):5, (0,4):3, (0,8):7,
        (1,2):6, (2,5):9, (3,1):1,
        (4,4):7, (5,7):4, (6,3):5,
        (7,6):2, (8,0):3, (8,4):1
    }
    for (i,j), val in pistas.items():
        sudoku.dominios[(i,j)] = [val]
    
    # Resolver con mínimos conflictos
    solucion = minimos_conflictos(sudoku, max_iter=10000)
    
    if solucion:
        print("Solución encontrada:")
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("-"*21)
            fila = []
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    fila.append("|")
                fila.append(str(solucion[(i,j)]))
            print(" ".join(fila))
    else:
        print("No se encontró solución en el número máximo de iteraciones")