# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 13:28:09 2025

@author: elvin

Implementación de un resolvedor de problemas de satisfacción de restricciones (CSP).
Incluye backtracking con heurísticas MRV y LCV para resolver Sudoku 4x4.
"""

class CSP:
    def __init__(self, variables, dominios, restricciones):
        """
        Inicializa un problema CSP (Constraint Satisfaction Problem).
        
        Parámetros:
            variables:    Lista de variables del problema          (list)
            dominios:     Diccionario de dominios por variable    (dict)
            restricciones: Lista de pares de variables restringidas (list)
        """
        self.variables     = variables      # Lista de variables del problema
        self.dominios      = dominios       # Dominios para cada variable
        self.restricciones = restricciones  # Restricciones binarias
        self.vecinos       = {v: set() for v in variables}  # Grafo de vecinos
        
        for (v1, v2) in restricciones:     # Construye relación de vecindad
            self.vecinos[v1].add(v2)       # Agrega v2 como vecino de v1
            self.vecinos[v2].add(v1)       # Agrega v1 como vecino de v2

def backtracking(asignacion, csp):
    """
    Algoritmo de backtracking recursivo para CSP con heurísticas.
    
    Parámetros:
        asignacion: Asignación parcial actual          (dict)
        csp:        Instancia del problema CSP        (CSP)
    
    Retorna:
        Solución completa o None si no hay solución   (dict/None)
    """
    if len(asignacion) == len(csp.variables):  # Si asignación está completa
        return asignacion                      # Retorna solución
    
    var = seleccionar_variable_no_asignada(asignacion, csp)  # Selecciona variable
    for valor in orden_valores(var, asignacion, csp):         # Ordena valores
        if es_consistente(var, valor, asignacion, csp):       # Verifica consistencia
            asignacion[var] = valor                           # Asigna valor
            resultado = backtracking(asignacion, csp)         # Busca recursivamente
            if resultado is not None:                         # Si encontró solución
                return resultado                              # Retórnala
            del asignacion[var]                               # Elimina asignación
    return None                                              # No encontró solución

def seleccionar_variable_no_asignada(asignacion, csp):
    """
    Selecciona variable no asignada usando heurística MRV (Minimum Remaining Values).
    
    Parámetros:
        asignacion: Asignación parcial actual          (dict)
        csp:        Instancia del problema CSP        (CSP)
    
    Retorna:
        Variable no asignada con menor dominio        (any)
    """
    no_asignadas = [v for v in csp.variables if v not in asignacion]  # Filtra no asignadas
    return min(no_asignadas, key=lambda v: len(csp.dominios[v]))      # Selecciona por MRV

def orden_valores(var, asignacion, csp):
    """
    Ordena valores del dominio usando heurística LCV (Least Constraining Value).
    
    Parámetros:
        var:        Variable a ordenar valores        (any)
        asignacion: Asignación parcial actual          (dict)
        csp:        Instancia del problema CSP        (CSP)
    
    Retorna:
        Lista de valores ordenados por LCV            (list)
    """
    return sorted(csp.dominios[var],                 # Ordena valores del dominio
                key=lambda v: contar_conflictos(var, v, asignacion, csp))  # Por conflictos

def contar_conflictos(var, valor, asignacion, csp):
    """
    Cuenta conflictos potenciales para un valor dado.
    
    Parámetros:
        var:        Variable evaluada                 (any)
        valor:      Valor a evaluar                   (any)
        asignacion: Asignación parcial actual          (dict)
        csp:        Instancia del problema CSP        (CSP)
    
    Retorna:
        Número de conflictos potenciales              (int)
    """
    total = 0                                        # Contador de conflictos
    for vecino in csp.vecinos[var]:                  # Para cada variable vecina
        if vecino in asignacion and not cumple_restriccion(valor, asignacion[vecino]):
            total += 1                               # Incrementa si hay conflicto
    return total                                     # Retorna total conflictos

def cumple_restriccion(valor1, valor2):
    """
    Verifica si dos valores cumplen las restricciones (para Sudoku: deben ser diferentes).
    
    Parámetros:
        valor1: Primer valor a comparar               (any)
        valor2: Segundo valor a comparar              (any)
    
    Retorna:
        True si cumplen restricción, False si no      (bool)
    """
    return valor1 != valor2                          # Restricción de desigualdad

def es_consistente(var, valor, asignacion, csp):
    """
    Verifica si una asignación es consistente con las restricciones.
    
    Parámetros:
        var:        Variable asignada                 (any)
        valor:      Valor asignado                    (any)
        asignacion: Asignación parcial actual          (dict)
        csp:        Instancia del problema CSP        (CSP)
    
    Retorna:
        True si es consistente, False si no           (bool)
    """
    for vecino in csp.vecinos[var]:                  # Para cada variable vecina
        if vecino in asignacion:                     # Si está asignada
            if not cumple_restriccion(valor, asignacion[vecino]):  # Verifica
                return False                         # No es consistente
    return True                                      # Todas las restricciones OK

def crear_sudoku_4x4():
    """
    Crea una instancia CSP para un Sudoku 4x4.
    
    Retorna:
        Problema CSP configurado para Sudoku 4x4      (CSP)
    """
    variables = [(i,j) for i in range(4) for j in range(4)]  # 16 celdas
    dominios = {(i,j): list(range(1,5)) for i,j in variables}  # Valores 1-4
    
    restricciones = []                                # Lista de restricciones
    # Restricciones de filas y columnas
    for i in range(4):                                # Para cada fila/columna
        for j in range(4):
            for k in range(4):
                if k != j: restricciones.append(((i,j), (i,k)))  # Misma fila
                if k != i: restricciones.append(((i,j), (k,j)))  # Misma columna
    
    # Restricciones de cajas 2x2
    for bi in [0,2]:                                 # Para cada bloque inicial
        for bj in [0,2]:
            for i in range(2):                       # Dentro del bloque
                for j in range(2):
                    for k in range(2):
                        for l in range(2):
                            if (i,j) != (k,l):       # Evita autoreferencia
                                restricciones.append(((bi+i, bj+j), (bi+k, bj+l)))
    
    return CSP(variables, dominios, restricciones)   # Retorna CSP configurado

if __name__ == "__main__":
    # Configuración y resolución del Sudoku 4x4
    sudoku = crear_sudoku_4x4()                      # Crea instancia CSP
    
    # Asignar pistas iniciales (valores fijos)
    sudoku.dominios[(0,0)] = [1]                     # Pista en (0,0)
    sudoku.dominios[(0,2)] = [3]                     # Pista en (0,2)
    sudoku.dominios[(1,1)] = [4]                     # Pista en (1,1)
    sudoku.dominios[(3,3)] = [2]                     # Pista en (3,3)
    
    solucion = backtracking({}, sudoku)               # Resuelve el Sudoku
    
    # Mostrar solución en formato de cuadrícula
    print("\n" + "="*25)
    print(" SOLUCIÓN SUDOKU 4x4 ".center(25, "="))
    print("="*25)
    for i in range(4):                                # Para cada fila
        fila = [solucion[(i,j)] for j in range(4)]    # Obtiene valores
        print(" ".join(map(str, fila)).center(25))     # Imprime fila
    print("="*25)