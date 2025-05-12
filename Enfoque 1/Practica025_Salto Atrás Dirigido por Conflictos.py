# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 13:34:57 2025

@author: elvin

Implementación del algoritmo de Mínimos Conflictos para resolver problemas CSP.
Este método es eficiente para problemas como Sudoku donde las soluciones son densas.
"""

import random  # Importa módulo para generación de números aleatorios

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

def minimos_conflictos(csp, max_iter=1000):
    """
    Algoritmo de Mínimos Conflictos para resolver CSP.
    
    Parámetros:
        csp:      Instancia del problema CSP        (CSP)
        max_iter: Máximo número de iteraciones      (int)
    
    Retorna:
        Asignación solución o None si no converge   (dict/None)
    """
    # Asignación inicial aleatoria (respetando pistas fijas)
    asignacion = {}                                # Diccionario de asignación
    for var in csp.variables:                      # Para cada variable
        if len(csp.dominios[var]) == 1:            # Si es pista fija
            asignacion[var] = csp.dominios[var][0]  # Asigna valor fijo
        else:
            asignacion[var] = random.choice(csp.dominios[var])  # Asignación aleatoria
    
    for _ in range(max_iter):                      # Bucle principal
        conflicto_vars = [v for v in csp.variables  # Variables en conflicto
                        if contar_conflictos(v, asignacion[v], asignacion, csp) > 0]
        
        if not conflicto_vars:                     # Si no hay conflictos
            return asignacion                      # Solución encontrada
        
        # Seleccionar variable conflictiva aleatoria
        var = random.choice(conflicto_vars)        # Estrategia aleatoria
        
        # Seleccionar valor que minimiza conflictos
        valores_ordenados = sorted(csp.dominios[var],  # Ordena valores
                                 key=lambda v: contar_conflictos(var, v, asignacion, csp))
        mejor_valor = valores_ordenados[0]         # Valor con menos conflictos
        asignacion[var] = mejor_valor              # Actualiza asignación
    
    return None                                    # No convergió en max_iter

def contar_conflictos(var, valor, asignacion, csp):
    """
    Cuenta el número de restricciones violadas por una asignación.
    
    Parámetros:
        var:        Variable evaluada                 (any)
        valor:      Valor asignado                    (any)
        asignacion: Asignación actual                 (dict)
        csp:        Instancia del problema CSP        (CSP)
    
    Retorna:
        Número de conflictos                          (int)
    """
    return sum(1 for vecino in csp.vecinos[var]      # Cuenta vecinos
              if vecino in asignacion and             # asignados que
              not cumple_restriccion(valor, asignacion[vecino]))  # violan restricción

def cumple_restriccion(valor1, valor2):
    """
    Función de restricción para Sudoku (valores deben ser diferentes).
    
    Parámetros:
        valor1: Primer valor a comparar               (any)
        valor2: Segundo valor a comparar              (any)
    
    Retorna:
        True si cumplen restricción, False si no      (bool)
    """
    return valor1 != valor2                           # Restricción básica

def crear_sudoku_9x9():
    """
    Crea una instancia CSP para un Sudoku 9x9.
    
    Retorna:
        Problema CSP configurado para Sudoku 9x9      (CSP)
    """
    variables = [(i,j) for i in range(9) for j in range(9)]  # 81 celdas
    dominios  = {(i,j): list(range(1,10)) for i,j in variables}  # Valores 1-9
    
    restricciones = []                                # Lista de restricciones
    
    # Restricciones de fila y columna
    for i in range(9):                                # Para cada celda
        for j in range(9):
            for k in range(9):
                if k != j: restricciones.append(((i,j), (i,k)))  # Misma fila
                if k != i: restricciones.append(((i,j), (k,j)))  # Misma columna
    
    # Restricciones de caja 3x3
    for bi in range(0,9,3):                           # Para cada bloque 3x3
        for bj in range(0,9,3):
            caja = [(bi+i, bj+j) for i in range(3) for j in range(3)]
            for i, v1 in enumerate(caja):             # Todas combinaciones
                for v2 in caja[i+1:]:                 # únicas en caja
                    restricciones.append((v1, v2))
    
    return CSP(variables, dominios, restricciones)    # Retorna CSP configurado

if __name__ == "__main__":
    # Configuración y resolución del Sudoku 9x9
    sudoku = crear_sudoku_9x9()                      # Crea instancia CSP
    
    # Asignar pistas fijas (ejemplo medio)
    pistas = {                                       # Diccionario de pistas
        (0,0):5, (0,4):3, (0,8):7,                  # Valores iniciales
        (1,2):6, (2,5):9, (3,1):1,                  # para algunas celdas
        (4,4):7, (5,7):4, (6,3):5,
        (7,6):2, (8,0):3, (8,4):1
    }
    for (i,j), val in pistas.items():               # Fija valores en dominios
        sudoku.dominios[(i,j)] = [val]
    
    # Resolver con Mínimos Conflictos
    solucion = minimos_conflictos(sudoku, max_iter=10000)  # Ejecuta algoritmo
    
    # Mostrar solución
    print("\n" + "="*60)
    print(" SOLUCIÓN SUDOKU 9x9 ".center(60, "="))
    print("="*60)
    if solucion:                                    # Si encontró solución
        for i in range(9):                          # Imprime cada fila
            if i % 3 == 0 and i != 0:              # Separador horizontal
                print("-"*21)
            fila = []
            for j in range(9):                     # Imprime cada celda
                if j % 3 == 0 and j != 0:          # Separador vertical
                    fila.append("|")
                fila.append(str(solucion[(i,j)]))   # Valor de la celda
            print(" ".join(fila))                   # Imprime fila completa
    else:
        print("No se encontró solución en el número máximo de iteraciones")
    print("="*60)