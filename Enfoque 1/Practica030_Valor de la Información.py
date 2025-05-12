# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 13:48:24 2025

@author: elvin
"""

import numpy as np                   # Importa numpy para operaciones numéricas
from collections import defaultdict  # Importa defaultdict para diccionarios con valores por defecto
import math                         # Importa math para funciones matemáticas
import random                       # Importa random para generación de números aleatorios

class CSP:                          # Clase para representar un Problema de Satisfacción de Restricciones
    def __init__(self, variables, dominios, restricciones):
        """Constructor del CSP:
        variables: Lista de variables del problema
        dominios: Diccionario {variable: valores_posibles}
        restricciones: Lista de tuplas (var1, var2) indicando restricciones entre variables
        """
        self.variables = variables   # Almacena las variables del problema
        self.dominios = dominios     # Almacena los dominios de cada variable
        self.restricciones = restricciones  # Almacena las restricciones entre variables
        
        # Crea diccionario de vecinos para cada variable
        self.vecinos = {v: set() for v in variables}  # Inicializa conjuntos vacíos
        for (v1, v2) in restricciones:  # Para cada restricción
            self.vecinos[v1].add(v2)    # Añade v2 como vecino de v1
            self.vecinos[v2].add(v1)    # Añade v1 como vecino de v2 (grafo no dirigido)

def voi_solve_csp(csp, max_iter=100, exploration_factor=0.1):
    """Resuelve CSP usando el concepto de Valor de la Información:
    csp: Instancia del problema CSP
    max_iter: Número máximo de iteraciones
    exploration_factor: Factor para balancear exploración/explotación
    """
    # Historial de conflictos para cada asignación variable-valor
    conflict_history = defaultdict(lambda: defaultdict(int))
    
    # Asignación actual (solución parcial)
    asignacion = {}                   # Diccionario vacío para almacenar asignaciones
    
    for _ in range(max_iter):         # Realiza máximo de iteraciones
        if len(asignacion) == len(csp.variables):  # Si todas las variables están asignadas
            break                    # Termina el bucle
            
        # Seleccionar variable no asignada con mayor VOI (Valor de la Información)
        unassigned = [v for v in csp.variables if v not in asignacion]  # Variables sin asignar
        if not unassigned:           # Si no hay variables sin asignar
            break                    # Termina el bucle
            
        # Selecciona variable basada en VOI
        selected_var = select_variable_by_voi(unassigned, csp, conflict_history, asignacion, exploration_factor)
        
        # Seleccionar valor con menor conflicto esperado
        selected_val = select_value_by_voi(selected_var, csp, conflict_history, asignacion)
        
        # Asignar el valor seleccionado
        asignacion[selected_var] = selected_val
        
        # Actualizar historial de conflictos
        update_conflict_history(selected_var, selected_val, asignacion, csp, conflict_history)
    
    # Verificar consistencia final de la solución
    if all(consistente(var, asignacion[var], asignacion, csp) for var in csp.variables):
        return asignacion             # Devuelve solución si es consistente
    else:
        # Si no es consistente, intentar reparar la solución
        return repair_solution(asignacion, csp, conflict_history)

def select_variable_by_voi(unassigned, csp, conflict_history, asignacion, exploration_factor):
    """Selecciona variable basada en el Valor de la Información:
    unassigned: Lista de variables no asignadas
    csp: Instancia del problema CSP
    conflict_history: Historial de conflictos
    asignacion: Asignación actual
    exploration_factor: Factor de exploración
    """
    voi_scores = []                  # Lista para almacenar puntuaciones VOI
    
    for var in unassigned:           # Para cada variable no asignada
        # Calcular incertidumbre actual (entropía de los conflictos)
        conflict_counts = [conflict_history[var][val] for val in csp.dominios[var]]
        total_conflicts = sum(conflict_counts) + 1e-6  # Evitar división por cero
        probabilities = [count/total_conflicts for count in conflict_counts]
        current_entropy = -sum(p * math.log(p+1e-6) for p in probabilities)  # Calcula entropía
        
        # Calcular reducción esperada de entropía para cada posible valor
        expected_entropy_reduction = 0
        for val in csp.dominios[var]: # Para cada valor posible
            # Simular asignación y estimar nueva entropía
            temp_conflicts = estimate_conflicts(var, val, asignacion, csp)
            new_probabilities = [(conflict_history[var][v] + (1 if v == val else 0)*temp_conflicts/(total_conflicts+1) 
                              for v in csp.dominios[var]]
            new_entropy = -sum((p/(sum(new_probabilities)+1e-6)) * math.log((p/(sum(new_probabilities)+1e-6))+1e-6) 
                         for p in new_probabilities)
            expected_entropy_reduction += (current_entropy - new_entropy) * (1/(conflict_history[var][val]+1))
        
        # VOI = reducción esperada de entropía
        voi = expected_entropy_reduction
        
        # Factor de exploración (probabilidad de seleccionar variables menos exploradas)
        exploration_bonus = exploration_factor * (1 / (sum(conflict_history[var].values()) + 1))
        
        voi_scores.append(voi + exploration_bonus)  # Añade puntuación total
    
    # Seleccionar variable con mayor VOI
    return unassigned[np.argmax(voi_scores)]

def select_value_by_voi(var, csp, conflict_history, asignacion):
    """Selecciona valor basado en VOI y conflicto esperado:
    var: Variable a asignar
    csp: Instancia del problema CSP
    conflict_history: Historial de conflictos
    asignacion: Asignación actual
    """
    conflict_scores = []             # Lista para almacenar puntuaciones de conflicto
    
    for val in csp.dominios[var]:   # Para cada valor posible
        # Calcular conflicto esperado
        conflict_score = estimate_conflicts(var, val, asignacion, csp)
        
        # Considerar historial de conflictos
        historical_conflict = conflict_history[var][val]
        
        # Balance entre explotación (valores conocidos) y exploración (valores poco probados)
        total_trials = sum(conflict_history[var].values())
        exploration_bonus = math.sqrt(2 * math.log(total_trials + 1) / (conflict_history[var][val] + 1)
        
        conflict_scores.append(conflict_score + historical_conflict - exploration_bonus)
    
    # Seleccionar valor con menor score de conflicto
    return csp.dominios[var][np.argmin(conflict_scores)]

def estimate_conflicts(var, val, asignacion, csp):
    """Estima el número de conflictos que produciría una asignación:
    var: Variable a asignar
    val: Valor a asignar
    asignacion: Asignación actual
    csp: Instancia del problema CSP
    """
    conflict_count = 0               # Contador de conflictos
    
    # Verificar conflictos con variables ya asignadas
    for vecino in csp.vecinos[var]:  # Para cada variable vecina
        if vecino in asignacion:     # Si está asignada
            if not cumple_restriccion(val, asignacion[vecino]):  # Si hay conflicto
                conflict_count += 1  # Incrementa contador
                
    return conflict_count            # Devuelve número estimado de conflictos

def update_conflict_history(var, val, asignacion, csp, conflict_history):
    """Actualiza el historial de conflictos:
    var: Variable asignada
    val: Valor asignado
    asignacion: Asignación actual
    csp: Instancia del problema CSP
    conflict_history: Historial de conflictos a actualizar
    """
    # Contar conflictos reales producidos por esta asignación
    actual_conflicts = 0
    for vecino in csp.vecinos[var]:  # Para cada variable vecina
        if vecino in asignacion:      # Si está asignada
            if not cumple_restriccion(val, asignacion[vecino]):  # Si hay conflicto
                actual_conflicts += 1  # Incrementa contador
    
    # Actualizar historial para esta asignación
    conflict_history[var][val] += actual_conflicts

def repair_solution(asignacion, csp, conflict_history):
    """Intenta reparar una solución inconsistente:
    asignacion: Asignación actual (inconsistente)
    csp: Instancia del problema CSP
    conflict_history: Historial de conflictos
    """
    # Identificar variables en conflicto
    conflicted_vars = [var for var in csp.variables 
                      if not consistente(var, asignacion[var], asignacion, csp)]
    
    for var in conflicted_vars:      # Para cada variable en conflicto
        # Seleccionar nuevo valor con menor conflicto histórico
        best_val = min(csp.dominios[var], key=lambda v: conflict_history[var][v])
        asignacion[var] = best_val   # Reasignar valor
        
    # Verificar si la reparación fue exitosa
    if all(consistente(var, asignacion[var], asignacion, csp) for var in csp.variables):
        return asignacion            # Devuelve solución reparada
    else:
        return None                  # No se pudo reparar

def consistente(var, valor, asignacion, csp):
    """Verifica si una asignación es consistente:
    var: Variable asignada
    valor: Valor asignado
    asignacion: Asignación actual
    csp: Instancia del problema CSP
    """
    # Verifica restricciones con todas las variables vecinas asignadas
    for vecino in csp.vecinos[var]:  # Para cada variable vecina
        if vecino in asignacion:      # Si está asignada
            if not cumple_restriccion(valor, asignacion[vecino]):  # Si hay conflicto
                return False          # Asignación no es consistente
    return True                       # Asignación es consistente

def cumple_restriccion(valor1, valor2):
    """Función de restricción genérica (puede ser personalizada):
    valor1: Valor de la primera variable
    valor2: Valor de la segunda variable
    """
    return valor1 != valor2           # Restricción básica de desigualdad