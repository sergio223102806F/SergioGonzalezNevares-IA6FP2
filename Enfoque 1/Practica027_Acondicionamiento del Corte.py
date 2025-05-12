# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 13:40:24 2025

@author: elvin

Implementación del algoritmo de Acondicionamiento del Corte (Cut Conditioning)
para resolver problemas CSP mediante descomposición en subproblemas más pequeños.
"""

import networkx as nx  # Importa NetworkX para manipulación de grafos
import random         # Importa módulo para generación de números aleatorios

class CSP:
    def __init__(self, variables, dominios, restricciones):
        """
        Inicializa un problema CSP (Constraint Satisfaction Problem).
        
        Parámetros:
            variables:    Lista de variables del problema          (list)
            dominios:     Diccionario {variable: valores_posibles} (dict)
            restricciones: Lista de pares de variables restringidas (list)
        """
        self.variables     = variables       # Lista de variables del problema
        self.dominios      = dominios        # Dominios para cada variable
        self.restricciones = restricciones   # Restricciones entre variables
        self.vecinos       = {v: set() for v in variables}  # Grafo de vecindad
        
        for (v1, v2) in restricciones:      # Construye relación de vecindad
            self.vecinos[v1].add(v2)        # Agrega v2 como vecino de v1
            self.vecinos[v2].add(v1)        # Agrega v1 como vecino de v2

def cut_conditioning(csp, corte=None):
    """
    Algoritmo de Acondicionamiento del Corte para resolver CSP.
    
    Parámetros:
        csp:    Instancia del problema CSP        (CSP)
        corte:  Conjunto de aristas de corte      (set, opcional)
    
    Retorna:
        Solución completa o None si no hay solución (dict/None)
    """
    if not corte:                              # Si no se proporciona corte
        corte = encontrar_corte_minimo(csp)     # Encuentra corte mínimo
    
    componentes = obtener_componentes_conexas(csp, corte)  # Obtiene componentes
    soluciones = []                             # Almacena soluciones parciales
    
    for comp in componentes:                   # Resuelve cada subproblema
        subcsp = crear_subcsp(comp, csp)       # Crea CSP para componente
        sol = backtracking({}, subcsp)          # Resuelve con backtracking
        if sol is None:                        # Si subproblema no tiene solución
            return None                        # Problema completo no tiene solución
        soluciones.append(sol)                 # Agrega solución parcial
    
    return combinar_soluciones(soluciones, corte)  # Combina soluciones

def encontrar_corte_minimo(csp):
    """
    Encuentra un corte mínimo en el grafo de restricciones.
    
    Parámetros:
        csp: Instancia del problema CSP        (CSP)
    
    Retorna:
        Conjunto de aristas que forman el corte mínimo (set)
    """
    grafo = nx.Graph()                        # Crea grafo NetworkX
    grafo.add_edges_from(csp.restricciones)    # Añade restricciones como aristas
    return nx.minimum_edge_cut(grafo)          # Calcula corte mínimo

def obtener_componentes_conexas(csp, corte):
    """
    Obtiene componentes conexas después de remover el corte.
    
    Parámetros:
        csp:   Instancia del problema CSP        (CSP)
        corte: Conjunto de aristas de corte      (set)
    
    Retorna:
        Lista de componentes conexas             (list)
    """
    grafo = nx.Graph()                         # Crea grafo NetworkX
    # Añade aristas que no están en el corte
    grafo.add_edges_from([e for e in csp.restricciones if e not in corte])
    return list(nx.connected_components(grafo)) # Retorna componentes conexas

def crear_subcsp(componente, csp):
    """
    Crea un sub-CSP para un componente conexo.
    
    Parámetros:
        componente: Conjunto de variables del componente (set)
        csp:        Instancia del problema CSP original (CSP)
    
    Retorna:
        Subproblema CSP para el componente      (CSP)
    """
    # Filtra restricciones dentro del componente
    restricciones = [(v1, v2) for (v1, v2) in csp.restricciones 
                    if v1 in componente and v2 in componente]
    return CSP(componente,                      # Retorna nuevo CSP
              {v: csp.dominios[v] for v in componente},  # Con dominios reducidos
              restricciones)                    # Y restricciones del componente

def combinar_soluciones(soluciones, corte):
    """
    Combina soluciones de subproblemas en una solución global.
    
    Parámetros:
        soluciones: Lista de soluciones parciales (list)
        corte:      Conjunto de aristas de corte  (set)
    
    Retorna:
        Solución combinada                       (dict)
    """
    solucion_final = {}                         # Solución combinada
    for sol in soluciones:                      # Para cada solución parcial
        solucion_final.update(sol)              # Agrega asignaciones
    return solucion_final                       # Retorna solución completa

def backtracking(asignacion, csp):
    """
    Algoritmo de Backtracking básico para resolver subproblemas CSP.
    
    Parámetros:
        asignacion: Asignación parcial actual    (dict)
        csp:        Instancia del problema CSP   (CSP)
    
    Retorna:
        Solución completa o None si no hay solución (dict/None)
    """
    if len(asignacion) == len(csp.variables):   # Si asignación completa
        return asignacion                       # Retorna solución
    
    # Selecciona variable no asignada con MRV
    var = min([v for v in csp.variables if v not in asignacion],
              key=lambda v: len(csp.dominios[v]))
    
    for valor in csp.dominios[var]:             # Prueba valores en orden
        if consistente(var, valor, asignacion, csp):  # Si es consistente
            asignacion[var] = valor             # Realiza asignación
            resultado = backtracking(asignacion, csp)  # Llamada recursiva
            if resultado is not None:            # Si encontró solución
                return resultado                # Retórnala
            del asignacion[var]                 # Backtrack (deshacer)
    
    return None                                # No hay solución

def consistente(var, valor, asignacion, csp):
    """
    Verifica si una asignación es consistente con las restricciones.
    
    Parámetros:
        var:        Variable a asignar          (any)
        valor:      Valor a verificar           (any)
        asignacion: Asignación parcial actual   (dict)
        csp:        Instancia del problema CSP  (CSP)
    
    Retorna:
        True si es consistente, False si no     (bool)
    """
    return all(cumple_restriccion(valor, asignacion[vecino])  # Todas las
              for vecino in csp.vecinos[var]                  # restricciones
              if vecino in asignacion)                        # deben cumplirse

def cumple_restriccion(valor1, valor2):
    """
    Función de restricción para Sudoku (valores diferentes).
    
    Parámetros:
        valor1: Primer valor a comparar        (any)
        valor2: Segundo valor a comparar       (any)
    
    Retorna:
        True si cumplen restricción, False si no (bool)
    """
    return valor1 != valor2                    # Restricción básica

def crear_sudoku_4x4():
    """
    Crea una instancia CSP para un Sudoku 4x4.
    
    Retorna:
        Problema CSP configurado para Sudoku 4x4 (CSP)
    """
    variables = [(i,j) for i in range(4) for j in range(4)]  # 16 celdas
    dominios = {(i,j): list(range(1,5)) for i,j in variables}  # Valores 1-4
    
    restricciones = []                         # Lista de restricciones
    
    # Restricciones de filas y columnas
    for i in range(4):                         # Para cada celda
        for j in range(4):
            for k in range(4):
                if k != j: restricciones.append(((i,j), (i,k)))  # Misma fila
                if k != i: restricciones.append(((i,j), (k,j)))  # Misma columna
    
    # Restricciones de cajas 2x2
    for bi in [0,2]:                          # Para cada bloque 2x2
        for bj in [0,2]:
            caja = [(bi+i, bj+j) for i in range(2) for j in range(2)]
            for i, v1 in enumerate(caja):      # Todas combinaciones
                for v2 in caja[i+1:]:          # únicas en caja
                    restricciones.append((v1, v2))
    
    return CSP(variables, dominios, restricciones)  # Retorna CSP configurado

if __name__ == "__main__":
    # Configuración y resolución del Sudoku 4x4
    sudoku = crear_sudoku_4x4()               # Crea instancia CSP
    
    # Asignar pistas iniciales (valores fijos)
    pistas = {                                # Diccionario de pistas
        (0,0):1, (0,2):3,                    # Valores iniciales
        (1,1):4, (3,3):2                     # para algunas celdas
    }
    for (i,j), val in pistas.items():        # Fija valores en dominios
        sudoku.dominios[(i,j)] = [val]
    
    # Resolver con Acondicionamiento del Corte
    solucion = cut_conditioning(sudoku)      # Ejecuta algoritmo
    
    # Mostrar solución
    print("\n" + "="*40)
    print(" SOLUCIÓN SUDOKU 4x4 ".center(40, "="))
    print("="*40)
    if solucion:                             # Si encontró solución
        for i in range(4):                   # Imprime cada fila
            print([solucion[(i,j)] for j in range(4)])
    else:
        print("No se encontró solución")      # Mensaje de fallo
    print("="*40)