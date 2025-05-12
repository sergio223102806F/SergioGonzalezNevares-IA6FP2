# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 14:13:41 2025

@author: elvin
"""

import numpy as np                   # Importa numpy para operaciones numéricas
from collections import defaultdict  # Importa defaultdict para diccionarios por defecto

class CSP:                          # Clase para representar un Problema de Satisfacción de Restricciones
    def __init__(self, variables, dominios, restricciones):
        """Constructor que inicializa el CSP:
        variables: Lista de variables del problema
        dominios: Diccionario {variable: valores_posibles}
        restricciones: Lista de tuplas (var1, var2) con restricciones
        """
        self.variables = variables   # Almacena las variables del problema
        self.dominios = dominios     # Almacena los dominios de cada variable
        self.restricciones = restricciones  # Almacena las restricciones
        
        # Diccionario de vecinos para cada variable
        self.vecinos = {v: set() for v in variables}  # Inicializa conjuntos vacíos
        for (v1, v2) in restricciones:  # Para cada restricción
            self.vecinos[v1].add(v2)    # Añade v2 como vecino de v1
            self.vecinos[v2].add(v1)    # Añade v1 como vecino de v2 (no dirigido)

def mdp_solve_csp(csp, gamma=0.9, max_iter=100, tol=1e-4):
    """Resuelve un CSP modelándolo como un MDP (Proceso de Decisión Markoviano):
    csp: Instancia del problema CSP
    gamma: Factor de descuento para recompensas futuras
    max_iter: Máximo de iteraciones permitidas
    tol: Tolerancia para convergencia
    """
    # Inicializar función de valor para cada asignación posible
    V = defaultdict(float)           # Diccionario para almacenar valores
    
    # Función de recompensa: penaliza conflictos entre variables
    def recompensa(asignacion, var, val):
        """Calcula recompensa por asignar un valor a una variable:
        asignacion: Asignación parcial actual
        var: Variable que se está asignando
        val: Valor que se está probando
        """
        conflictos = sum(1 for vecino in csp.vecinos[var] 
                      if vecino in asignacion and not cumple_restriccion(val, asignacion[vecino]))
        return -conflictos            # Recompensa negativa por conflictos
    
    # Iteración de valor para actualizar V
    for _ in range(max_iter):        # Realiza máximo de iteraciones
        delta = 0                    # Para medir cambio en valores
        # Actualizar valores para cada variable y valor posible
        for var in csp.variables:    # Para cada variable en el CSP
            for val in csp.dominios[var]:  # Para cada valor posible
                old_v = V[(var, val)] # Guarda valor anterior
                max_q = -float('inf') # Inicializa máximo valor Q
                
                # Considerar el mejor valor para los vecinos
                for vecino in csp.vecinos[var]:  # Para cada variable vecina
                    for vec_val in csp.dominios[vecino]:  # Para cada valor posible
                        if cumple_restriccion(val, vec_val):  # Si no hay conflicto
                            # Calcula valor Q para esta acción
                            q_val = recompensa({var: val}, vecino, vec_val) + gamma * V[(vecino, vec_val)]
                            if q_val > max_q:    # Actualiza máximo
                                max_q = q_val
                
                # Actualiza valor V para esta asignación
                if csp.vecinos[var]:  # Si tiene vecinos
                    V[(var, val)] = recompensa({}, var, val) + gamma * (max_q if max_q != -float('inf') else 0)
                else:                 # Si no tiene vecinos
                    V[(var, val)] = recompensa({}, var, val)
                
                # Actualiza delta para verificar convergencia
                delta = max(delta, abs(V[(var, val)] - old_v))
        
        if delta < tol:              # Si convergió
            break                    # Termina las iteraciones
    
    # Extraer la política óptima (asignación de valores)
    politica = {}                   # Diccionario para política óptima
    for var in csp.variables:       # Para cada variable
        # Selecciona valor con mayor valor V
        best_val = max(csp.dominios[var], key=lambda val: V[(var, val)])
        politica[var] = best_val    # Asigna mejor valor
    
    # Verificar si la política es solución válida
    if all(consistente(var, politica[var], politica, csp) for var in csp.variables):
        return politica              # Retorna solución si es válida
    else:
        # Si no es válida, usa backtracking con valores V como heurística
        return mdp_backtracking({}, csp, V)

def mdp_backtracking(asignacion, csp, V):
    """Backtracking usando los valores del MDP como heurística:
    asignacion: Asignación parcial actual
    csp: Instancia del problema CSP
    V: Diccionario de valores calculados
    """
    if len(asignacion) == len(csp.variables):  # Si asignación completa
        return asignacion                     # Retorna solución
    
    # Seleccionar variable no asignada con mayor impacto (según V)
    var = max([v for v in csp.variables if v not in asignacion],
             key=lambda v: max(V[(v, val)] for val in csp.dominios[v]))
    
    # Ordenar valores por su valor V (de mayor a menor)
    valores_ordenados = sorted(csp.dominios[var], key=lambda val: -V[(var, val)])
    
    for valor in valores_ordenados:   # Probar valores en orden
        if consistente(var, valor, asignacion, csp):  # Si es consistente
            asignacion[var] = valor   # Asignar valor
            # Llamada recursiva
            resultado = mdp_backtracking(asignacion, csp, V)
            if resultado is not None:  # Si encontró solución
                return resultado       # Retorna solución
            del asignacion[var]       # Deshace asignación
    return None                      # No encontró solución

def consistente(var, valor, asignacion, csp):
    """Verifica si una asignación es consistente:
    var: Variable que se está verificando
    valor: Valor asignado
    asignacion: Asignación parcial actual
    csp: Instancia del problema CSP
    """
    return all(cumple_restriccion(valor, asignacion[vecino])
              for vecino in csp.vecinos[var] if vecino in asignacion)

def cumple_restriccion(valor1, valor2):
    """Función de restricción básica (valores diferentes):
    valor1: Primer valor a comparar
    valor2: Segundo valor a comparar
    """
    return valor1 != valor2           # Restricción de desigualdad

def crear_sudoku_4x4():
    """Crea una instancia de Sudoku 4x4 como CSP"""
    variables = [(i,j) for i in range(4) for j in range(4)]  # 16 celdas
    dominios = {(i,j): list(range(1,5)) for i,j in variables}  # Valores 1-4
    
    restricciones = []
    # Restricciones de filas y columnas
    for i in range(4):
        for j in range(4):
            for k in range(4):
                if k != j: restricciones.append(((i,j), (i,k)))  # Misma fila
                if k != i: restricciones.append(((i,j), (k,j)))  # Misma columna
    # Restricciones de cajas 2x2
    for bi in [0,2]:
        for bj in [0,2]:
            caja = [(bi+i, bj+j) for i in range(2) for j in range(2)]
            for i, v1 in enumerate(caja):
                for v2 in caja[i+1:]:
                    restricciones.append((v1, v2))  # Misma caja
    
    return CSP(variables, dominios, restricciones)  # Retorna instancia CSP

if __name__ == "__main__":            # Bloque principal de ejecución
    sudoku = crear_sudoku_4x4()       # Crea instancia de Sudoku 4x4
    
    # Asignar algunas pistas iniciales
    pistas = {(0,0):1, (0,2):3, (1,1):4, (3,3):2}
    for (i,j), val in pistas.items():
        sudoku.dominios[(i,j)] = [val]  # Fija valores de pistas
    
    # Resolver con enfoque MDP
    solucion = mdp_solve_csp(sudoku)   # Obtiene solución
    
    if solucion:                       # Si encontró solución
        print("Solución encontrada:")
        for i in range(4):             # Imprime el tablero solución
            print([solucion[(i,j)] for j in range(4)])
    else:
        print("No se encontró solución")  # Mensaje si no hay solución