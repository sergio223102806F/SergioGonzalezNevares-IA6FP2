# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 13:59:11 2025

@author: elvin
"""

import networkx as nx                # Importa networkx para operaciones con grafos
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

def policy_iteration_csp(csp, max_iter=100, tol=1e-4):
    """Resuelve CSP usando Iteración de Políticas:
    csp: Instancia del problema CSP
    max_iter: Máximo de iteraciones permitidas
    tol: Tolerancia para convergencia
    """
    # Inicializa política con valores aleatorios
    politica = {var: random.choice(csp.dominios[var]) for var in csp.variables}
    
    for _ in range(max_iter):        # Realiza máximo de iteraciones
        # Paso de Evaluación: Calcular calidad de la política actual
        valores = evaluate_policy(politica, csp)
        
        # Paso de Mejora: Actualizar política basada en valores
        politica_mejorada, policy_changed = improve_policy(politica, valores, csp)
        
        # Verificar convergencia (si política no cambió)
        if not policy_changed:
            break                   # Termina el bucle si convergió
            
        politica = politica_mejorada # Actualiza la política
    
    # Verificar si la política final es solución válida
    if all(consistente(var, politica[var], politica, csp) 
           for var in csp.variables):
        return politica              # Retorna solución si es válida
    else:
        # Si no es válida, usa backtracking guiado por política
        return backtracking_policy_guided({}, csp, politica)

def evaluate_policy(politica, csp):
    """Evalúa la política actual calculando valores:
    politica: Asignación actual (diccionario)
    csp: Instancia del problema CSP
    """
    valores = defaultdict(float)     # Diccionario para almacenar valores
    
    # Calcula calidad para cada variable en la política
    for var in csp.variables:       # Para cada variable
        val = politica[var]         # Valor asignado en la política
        # Cuenta conflictos con vecinos
        conflictos = sum(1 for vecino in csp.vecinos[var] 
                      if not cumple_restriccion(val, politica[vecino]))
        # Valor inversamente proporcional a conflictos
        valores[var] = 1.0 / (1.0 + conflictos)  
    
    return valores                  # Retorna valores calculados

def improve_policy(politica, valores, csp):
    """Mejora la política basada en los valores:
    politica: Política actual a mejorar
    valores: Valores calculados en evaluate_policy
    csp: Instancia del problema CSP
    """
    nueva_politica = {}             # Nueva política a construir
    policy_changed = False          # Flag para detectar cambios
    
    for var in csp.variables:       # Para cada variable
        best_val = None             # Mejor valor encontrado
        best_score = -float('inf')  # Mejor puntuación encontrada
        
        for val in csp.dominios[var]:  # Evalúa cada valor posible
            score = 0               # Puntuación para este valor
            for vecino in csp.vecinos[var]:
                # Suma valores de vecinos si no hay conflicto
                if cumple_restriccion(val, politica[vecino]):
                    score += valores[vecino]
            
            # Actualiza mejor valor (con aleatoriedad para evitar estancamiento)
            if score > best_score or (score == best_score and random.random() < 0.1):
                best_score = score
                best_val = val
        
        nueva_politica[var] = best_val  # Asigna mejor valor
        if best_val != politica[var]:    # Verifica si hubo cambio
            policy_changed = True
    
    return nueva_politica, policy_changed  # Retorna nueva política y flag

def backtracking_policy_guided(asignacion, csp, politica):
    """Backtracking guiado por la política:
    asignacion: Asignación parcial actual
    csp: Instancia del problema CSP
    politica: Política para guiar la búsqueda
    """
    if len(asignacion) == len(csp.variables):  # Si asignación completa
        return asignacion                     # Retorna solución
    
    # Selecciona variable no asignada con dominio más pequeño
    var = min([v for v in csp.variables if v not in asignacion],
              key=lambda v: len(csp.dominios[v]))
    
    # Ordena valores por proximidad al valor de la política
    valores_ordenados = sorted(csp.dominios[var],
                             key=lambda val: abs(val - politica[var]))
    
    for valor in valores_ordenados:   # Prueba valores en orden
        if consistente(var, valor, asignacion, csp):  # Si es consistente
            asignacion[var] = valor   # Asigna valor
            # Llama recursivamente
            resultado = backtracking_policy_guided(asignacion, csp, politica)
            if resultado is not None:  # Si encontró solución
                return resultado       # Retorna solución
            del asignacion[var]       # Deshace asignación
    return None                      # No encontró solución

def consistente(var, valor, asignacion, csp):
    """Verifica si una asignación es consistente:
    var: Variable a verificar
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
    import random                     # Importa random para generación aleatoria
    
    sudoku = crear_sudoku_4x4()       # Crea instancia de Sudoku 4x4
    
    # Asigna algunas pistas iniciales
    pistas = {(0,0):1, (0,2):3, (1,1):4, (3,3):2}
    for (i,j), val in pistas.items():
        sudoku.dominios[(i,j)] = [val]  # Fija valores de pistas
    
    # Resuelve usando Iteración de Políticas
    solucion = policy_iteration_csp(sudoku)
    
    # Muestra resultados
    if solucion:                      # Si encontró solución
        print("Solución encontrada:")
        for i in range(4):            # Imprime el tablero solución
            print([solucion[(i,j)] for j in range(4)])
    else:
        print("No se encontró solución")  # Mensaje si no hay solución