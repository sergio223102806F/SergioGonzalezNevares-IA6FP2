# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 13:33:01 2025

@author: elvin
"""

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

def ac3(csp, dominios=None):
    """Algoritmo AC-3 para propagación de restricciones"""
    dominios = dominios or {v: list(csp.dominios[v]) for v in csp.variables}
    cola = deque((xi, xj) for xi in csp.variables for xj in csp.vecinos[xi])
    
    while cola:
        xi, xj = cola.popleft()
        if revisar(xi, xj, dominios, csp):
            if not dominios[xi]:
                return False  # Dominio vacío, inconsistencia
            for xk in csp.vecinos[xi]:
                if xk != xj:
                    cola.append((xk, xi))
    return dominios

def revisar(xi, xj, dominios, csp):
    """Elimina valores inconsistentes de xi respecto a xj"""
    revisado = False
    for x in list(dominios[xi]):
        # Si no hay valor en xj que satisfaga la restricción con x
        if not any(cumple_restriccion(x, y) for y in dominios[xj]):
            dominios[xi].remove(x)
            revisado = True
    return revisado

def backtracking_ac3(asignacion, csp, dominios):
    """Backtracking con propagación AC-3"""
    if len(asignacion) == len(csp.variables):
        return asignacion
    
    var = seleccionar_variable(asignacion, dominios)
    for valor in orden_valores(var, asignacion, csp, dominios):
        if consistente(var, valor, asignacion, csp):
            asignacion[var] = valor
            nuevos_dominios = {v: list(dominios[v]) for v in dominios}
            nuevos_dominios[var] = [valor]
            
            # Propagación de restricciones AC-3
            if ac3(csp, nuevos_dominios):
                resultado = backtracking_ac3(asignacion, csp, nuevos_dominios)
                if resultado is not None:
                    return resultado
            
            del asignacion[var]
    return None

# Funciones auxiliares (iguales que en implementaciones anteriores)
def seleccionar_variable(asignacion, dominios):
    no_asignadas = [v for v in dominios if v not in asignacion]
    return min(no_asignadas, key=lambda v: len(dominios[v]))

def orden_valores(var, asignacion, csp, dominios):
    return sorted(dominios[var], key=lambda v: contar_conflictos(var, v, asignacion, csp))

def contar_conflictos(var, valor, asignacion, csp):
    return sum(1 for vecino in csp.vecinos[var] 
              if vecino in asignacion and not cumple_restriccion(valor, asignacion[vecino]))

def cumple_restriccion(valor1, valor2):
    return valor1 != valor2

def consistente(var, valor, asignacion, csp):
    return all(cumple_restriccion(valor, asignacion[vecino])
              for vecino in csp.vecinos[var] if vecino in asignacion)

# Ejemplo: Sudoku 9x9 (implementación reducida)
def crear_sudoku_9x9():
    variables = [(i,j) for i in range(9) for j in range(9)]
    dominios = {(i,j): list(range(1,10)) for i,j in variables}
    
    restricciones = []
    # Filas y columnas
    for i in range(9):
        for j in range(9):
            for k in range(9):
                if k != j: restricciones.append(((i,j), (i,k)))
                if k != i: restricciones.append(((i,j), (k,j)))
    # Cajas 3x3
    for bi in range(0,9,3):
        for bj in range(0,9,3):
            caja = [(bi+i, bj+j) for i in range(3) for j in range(3)]
            for i, v1 in enumerate(caja):
                for v2 in caja[i+1:]:
                    restricciones.append((v1, v2))
    
    return CSP(variables, dominios, restricciones)

# Uso con un Sudoku de ejemplo
if __name__ == "__main__":
    sudoku = crear_sudoku_9x9()
    
    # Asignar algunas pistas (valores iniciales)
    pistas = {
        (0,0):5, (0,4):3, (0,8):7,
        (1,2):6, (2,5):9, (3,1):1,
        (4,4):7, (5,7):4, (6,3):5,
        (7,6):2, (8,0):3, (8,4):1
    }
    
    for (i,j), val in pistas.items():
        sudoku.dominios[(i,j)] = [val]
    
    # Preprocesamiento con AC-3
    dominios_reducidos = ac3(sudoku)
    
    if dominios_reducidos:
        print("Preprocesamiento AC-3 completado. Dominios reducidos:")
        for i in range(9):
            print([len(dominios_reducidos[(i,j)]) for j in range(9)])
        
        # Resolver con Backtracking + AC-3
        solucion = backtracking_ac3({}, sudoku, dominios_reducidos)
        
        if solucion:
            print("\nSolución encontrada:")
            for i in range(9):
                print([solucion[(i,j)] for j in range(9)])
        else:
            print("No se encontró solución")
    else:
        print("El problema es inconsistente después de AC-3")