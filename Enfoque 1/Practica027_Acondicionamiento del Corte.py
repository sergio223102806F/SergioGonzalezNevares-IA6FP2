# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 13:40:24 2025

@author: elvin
"""

import networkx as nx
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

def cut_conditioning(csp, corte=None):
    """Acondicionamiento del Corte para CSP"""
    if not corte:
        corte = encontrar_corte_minimo(csp)
    
    # Resolver subproblemas independientes
    componentes = obtener_componentes_conexas(csp, corte)
    soluciones = []
    
    for comp in componentes:
        subcsp = crear_subcsp(comp, csp)
        sol = backtracking({}, subcsp)
        if sol is None:
            return None  # Un subproblema no tiene solución
        soluciones.append(sol)
    
    # Combinar soluciones
    return combinar_soluciones(soluciones, corte)

def encontrar_corte_minimo(csp):
    """Encuentra un corte mínimo en el grafo de restricciones"""
    grafo = nx.Graph()
    grafo.add_edges_from(csp.restricciones)
    return nx.minimum_edge_cut(grafo)

def obtener_componentes_conexas(csp, corte):
    """Obtiene componentes conexas después de remover el corte"""
    grafo = nx.Graph()
    grafo.add_edges_from([e for e in csp.restricciones if e not in corte])
    return list(nx.connected_components(grafo))

def crear_subcsp(componente, csp):
    """Crea un sub-CSP para un componente conexo"""
    restricciones = [(v1, v2) for (v1, v2) in csp.restricciones 
                    if v1 in componente and v2 in componente]
    return CSP(componente, {v: csp.dominios[v] for v in componente}, restricciones)

def combinar_soluciones(soluciones, corte):
    """Combina soluciones de subproblemas"""
    solucion_final = {}
    for sol in soluciones:
        solucion_final.update(sol)
    return solucion_final

# Algoritmo de Backtracking base (necesario para los subproblemas)
def backtracking(asignacion, csp):
    if len(asignacion) == len(csp.variables):
        return asignacion
    var = min([v for v in csp.variables if v not in asignacion],
              key=lambda v: len(csp.dominios[v]))
    for valor in csp.dominios[var]:
        if consistente(var, valor, asignacion, csp):
            asignacion[var] = valor
            resultado = backtracking(asignacion, csp)
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
    
    # Resolver con acondicionamiento del corte
    solucion = cut_conditioning(sudoku)
    
    if solucion:
        print("Solución encontrada:")
        for i in range(4):
            print([solucion[(i,j)] for j in range(4)])
    else:
        print("No se encontró solución")