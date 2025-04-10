# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 13:31:07 2025

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

def forward_checking(asignacion, csp, dominios):
    if len(asignacion) == len(csp.variables):
        return asignacion
    
    var = seleccionar_variable(asignacion, dominios)
    
    for valor in orden_valores(var, asignacion, csp, dominios):
        if consistente(var, valor, asignacion, csp):
            asignacion[var] = valor
            nuevos_dominios = actualizar_dominios(var, valor, asignacion, csp, dominios)
            
            if dominios_consistentes(nuevos_dominios):
                resultado = forward_checking(asignacion, csp, nuevos_dominios)
                if resultado is not None:
                    return resultado
            
            del asignacion[var]
    return None

def actualizar_dominios(var, valor, asignacion, csp, dominios):
    """Reduce dominios de variables vecinas"""
    nuevos_dominios = {v: list(dominios[v]) for v in dominios}
    nuevos_dominios[var] = [valor]
    
    for vecino in csp.vecinos[var]:
        if vecino not in asignacion:
            nuevos_dominios[vecino] = [
                v for v in nuevos_dominios[vecino] 
                if cumple_restriccion(valor, v)
            ]
    return nuevos_dominios

def dominios_consistentes(dominios):
    return all(len(dominios[v]) > 0 for v in dominios)

def seleccionar_variable(asignacion, dominios):
    no_asignadas = [v for v in dominios if v not in asignacion]
    return min(no_asignadas, key=lambda v: len(dominios[v]))

def orden_valores(var, asignacion, csp, dominios):
    return sorted(dominios[var],
                key=lambda v: contar_conflictos(var, v, asignacion, csp))

def contar_conflictos(var, valor, asignacion, csp):
    return sum(1 for vecino in csp.vecinos[var] 
              if vecino in asignacion and not cumple_restriccion(valor, asignacion[vecino]))

def cumple_restriccion(valor1, valor2):
    return valor1 != valor2

def consistente(var, valor, asignacion, csp):
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
    
    return CSP(variables, dominios, restricciones)

# Uso
sudoku = crear_sudoku_4x4()
pistas = {(0,0):1, (0,2):3, (1,1):4, (3,3):2}
for (i,j), val in pistas.items():
    sudoku.dominios[(i,j)] = [val]

solucion = forward_checking({}, sudoku, sudoku.dominios.copy())

if solucion:
    print("Solución encontrada:")
    for i in range(4):
        print([solucion[(i,j)] for j in range(4)])
else:
    print("No se encontró solución")