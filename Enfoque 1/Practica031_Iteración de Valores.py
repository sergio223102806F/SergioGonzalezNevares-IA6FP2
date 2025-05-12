# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 13:48:25 2025

@author: elvin

Implementación de CSP usando Iteración de Valores (Value Iteration)
para resolver problemas de satisfacción de restricciones.
"""

import networkx as nx      # Importa NetworkX para manipulación de grafos
from collections import deque  # Importa deque para estructuras de datos eficientes

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

def value_iteration_csp(csp, max_iter=100, tol=1e-4):
    """
    Resuelve un CSP usando el algoritmo de Iteración de Valores.
    
    Parámetros:
        csp:      Instancia del problema CSP        (CSP)
        max_iter: Máximo número de iteraciones      (int)
        tol:      Tolerancia para convergencia      (float)
    
    Retorna:
        Asignación solución o None si no converge   (dict/None)
    """
    # Inicializar valores (probabilidades o puntuaciones)
    values = {
        var: {val: 1.0 for val in csp.dominios[var]}  # Valores iniciales uniformes
        for var in csp.variables
    }
    
    for _ in range(max_iter):               # Bucle principal de iteración
        delta = 0                           # Para medir cambio máximo
        new_values = {var: {} for var in csp.variables}  # Nuevos valores
        
        # Actualizar valores para cada variable
        for var in csp.variables:           # Para cada variable en CSP
            for val in csp.dominios[var]:   # Para cada valor posible
                total = 0                   # Acumulador de consistencia
                
                # Calcular consistencia con vecinos
                for vecino in csp.vecinos[var]:  # Para cada variable vecina
                    for vec_val in csp.dominios[vecino]:  # Para cada valor vecino
                        if cumple_restriccion(val, vec_val):  # Si son consistentes
                            total += values[vecino][vec_val]  # Suma valor actual
                
                # Normalizar y almacenar nuevo valor
                divisor = max(1, len(csp.dominios[var]) * len(csp.vecinos[var]))
                new_val = total / divisor   # Promedio de consistencia
                new_values[var][val] = new_val  # Almacena nuevo valor
                delta = max(delta, abs(new_val - values[var][val]))  # Actualiza delta
        
        values = new_values                 # Actualiza valores para siguiente iteración
        
        if delta < tol:                     # Verificar convergencia
            break                           # Salir si convergió
    
    # Seleccionar asignación más probable
    asignacion = {
        var: max(values[var].items(), key=lambda x: x[1])[0]  # Mejor valor
        for var in csp.variables
    }
    
    # Verificar consistencia de la solución
    if all(consistente(var, asignacion[var], asignacion, csp)
           for var in csp.variables):
        return asignacion                   # Retorna solución si es consistente
    else:
        # Usar backtracking guiado por valores si no es consistente
        return backtracking_value_guided({}, csp, values)

def backtracking_value_guided(asignacion, csp, values):
    """
    Backtracking guiado por los valores de la iteración de valores.
    
    Parámetros:
        asignacion: Asignación parcial actual          (dict)
        csp:        Instancia del problema CSP        (CSP)
        values:     Valores calculados por iteración   (dict)
    
    Retorna:
        Solución completa o None si no hay solución   (dict/None)
    """
    if len(asignacion) == len(csp.variables):  # Si asignación completa
        return asignacion                      # Retorna solución
    
    # Seleccionar variable no asignada con MRV
    var = min([v for v in csp.variables if v not in asignacion],
              key=lambda v: len(csp.dominios[v]))
    
    # Ordenar valores por score descendente (guiado por values)
    valores_ordenados = sorted(csp.dominios[var],
                              key=lambda val: -values[var][val])
    
    for valor in valores_ordenados:          # Probar valores en orden guiado
        if consistente(var, valor, asignacion, csp):  # Si es consistente
            asignacion[var] = valor         # Realizar asignación
            resultado = backtracking_value_guided(asignacion, csp, values)
            if resultado is not None:       # Si encontró solución
                return resultado            # Retórnala
            del asignacion[var]             # Backtrack (deshacer)
    return None                             # No hay solución

def consistente(var, valor, asignacion, csp):
    """
    Verifica si una asignación es consistente con las restricciones.
    
    Parámetros:
        var:        Variable a asignar                 (any)
        valor:      Valor a verificar                  (any)
        asignacion: Asignación parcial actual          (dict)
        csp:        Instancia del problema CSP        (CSP)
    
    Retorna:
        True si es consistente, False si no           (bool)
    """
    return all(cumple_restriccion(valor, asignacion[vecino])  # Todas las
              for vecino in csp.vecinos[var]                  # restricciones
              if vecino in asignacion)                        # deben cumplirse

def cumple_restriccion(valor1, valor2):
    """
    Función de restricción para Sudoku (valores diferentes).
    
    Parámetros:
        valor1: Primer valor a comparar               (any)
        valor2: Segundo valor a comparar              (any)
    
    Retorna:
        True si cumplen restricción, False si no      (bool)
    """
    return valor1 != valor2                           # Restricción básica

def crear_sudoku_4x4():
    """
    Crea una instancia CSP para un Sudoku 4x4.
    
    Retorna:
        Problema CSP configurado para Sudoku 4x4      (CSP)
    """
    variables = [(i,j) for i in range(4) for j in range(4)]  # 16 celdas
    dominios  = {(i,j): list(range(1,5)) for i,j in variables}  # Valores 1-4
    
    restricciones = []                                # Lista de restricciones
    
    # Restricciones de filas y columnas
    for i in range(4):                                # Para cada celda
        for j in range(4):
            for k in range(4):
                if k != j: restricciones.append(((i,j), (i,k)))  # Misma fila
                if k != i: restricciones.append(((i,j), (k,j)))  # Misma columna
    
    # Restricciones de cajas 2x2
    for bi in [0,2]:                                 # Para cada bloque 2x2
        for bj in [0,2]:
            caja = [(bi+i, bj+j) for i in range(2) for j in range(2)]
            for i, v1 in enumerate(caja):            # Todas combinaciones
                for v2 in caja[i+1:]:                # únicas en caja
                    restricciones.append((v1, v2))
    
    return CSP(variables, dominios, restricciones)   # Retorna CSP configurado

if __name__ == "__main__":
    # Configuración y resolución del Sudoku 4x4
    sudoku = crear_sudoku_4x4()                     # Crea instancia CSP
    
    # Asignar pistas iniciales (valores fijos)
    pistas = {                                      # Diccionario de pistas
        (0,0):1, (0,2):3,                          # Valores iniciales
        (1,1):4, (3,3):2                           # para algunas celdas
    }
    for (i,j), val in pistas.items():              # Fija valores en dominios
        sudoku.dominios[(i,j)] = [val]
    
    # Resolver con Iteración de Valores
    solucion = value_iteration_csp(sudoku)         # Ejecuta algoritmo
    
    # Mostrar solución
    print("\n" + "="*40)
    print(" SOLUCIÓN SUDOKU 4x4 ".center(40, "="))
    print("="*40)
    if solucion:                                   # Si encontró solución
        for i in range(4):                        # Imprime cada fila
            print([solucion[(i,j)] for j in range(4)])
    else:
        print("No se encontró solución")           # Mensaje de fallo
    print("="*40)