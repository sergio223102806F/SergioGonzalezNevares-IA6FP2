# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 13:33:01 2025

@author: elvin
"""

class CSP:
    def __init__(self, variables, dominios, restricciones):
        self.variables = variables
        self.dominios = dominios
        self.restricciones = restricciones
        self.vecinos = {v: set() for v in variables}
        for (v1, v2) in restricciones:
            self.vecinos[v1].add(v2)
            self.vecinos[v2].add(v1)

def backjumping(asignacion, csp, nivel=0, conflictos=None):
    """
    Algoritmo de Salto Atrás Dirigido por Conflictos
    - nivel: profundidad actual en el árbol de búsqueda
    - conflictos: diccionario {variable: {niveles de conflicto}}
    """
    if len(asignacion) == len(csp.variables):
        return asignacion
    
    conflictos = conflictos or {v: set() for v in csp.variables}
    var = seleccionar_variable(asignacion, csp)
    
    for valor in orden_valores(var, asignacion, csp):
        if consistente(var, valor, asignacion, csp):
            asignacion[var] = valor
            resultado = backjumping(asignacion, csp, nivel+1, conflictos)
            if resultado is not None:
                return resultado
            del asignacion[var]
        else:
            # Registrar conflictos
            for vecino in csp.vecinos[var]:
                if vecino in asignacion:
                    conflictos[var].add(nivel_dict[vecino])
    
    # Determinar nivel de salto (máximo nivel de conflicto)
    if conflictos[var]:
        nivel_salto = max(conflictos[var])
        # Propagación de conflictos
        for v in conflictos:
            if nivel_dict[v] < nivel_dict[var]:
                conflictos[v].update(conflictos[var])
        return backjumping(asignacion, csp, nivel_salto, conflictos)
    else:
        return None  # No hay solución desde este punto

# Funciones auxiliares
def seleccionar_variable(asignacion, csp):
    no_asignadas = [v for v in csp.variables if v not in asignacion]
    return min(no_asignadas, key=lambda v: len(csp.dominios[v]))

def orden_valores(var, asignacion, csp):
    return sorted(csp.dominios[var],
                key=lambda v: contar_conflictos(var, v, asignacion, csp))

def contar_conflictos(var, valor, asignacion, csp):
    return sum(1 for vecino in csp.vecinos[var] 
              if vecino in asignacion and not cumple_restriccion(valor, asignacion[vecino]))

def cumple_restriccion(valor1, valor2):
    return valor1 != valor2

def consistente(var, valor, asignacion, csp):
    return all(cumple_restriccion(valor, asignacion[vecino])
              for vecino in csp.vecinos[var] if vecino in asignacion)

# Mapeo de variables a niveles (para seguimiento de conflictos)
nivel_dict = {}

# Ejemplo: Sudoku 4x4
def crear_sudoku_4x4():
    variables = [(i,j) for i in range(4) for j in range(4)]
    dominios = {(i,j): list(range(1,5)) for i,j in variables}
    
    restricciones = []
    # Filas y columnas
    for i in range(4):
        for j in range(4):
            nivel_dict[(i,j)] = i*4 + j  # Asignar nivel único
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

# Uso
if __name__ == "__main__":
    sudoku = crear_sudoku_4x4()
    # Asignar algunas pistas
    pistas = {(0,0):1, (0,2):3, (1,1):4, (3,3):2}
    for (i,j), val in pistas.items():
        sudoku.dominios[(i,j)] = [val]
    
    solucion = backjumping({}, sudoku)
    
    if solucion:
        print("Solución encontrada:")
        for i in range(4):
            print([solucion[(i,j)] for j in range(4)])
    else:
        print("No se encontró solución")