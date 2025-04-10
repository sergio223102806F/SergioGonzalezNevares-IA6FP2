# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 13:48:24 2025

@author: elvin
"""

import numpy as np
from collections import defaultdict
import math
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

def voi_solve_csp(csp, max_iter=100, exploration_factor=0.1):
    """Resuelve CSP usando el concepto de Valor de la Información"""
    # Historial de conflictos para cada asignación variable-valor
    conflict_history = defaultdict(lambda: defaultdict(int))
    
    # Asignación actual
    asignacion = {}
    
    for _ in range(max_iter):
        if len(asignacion) == len(csp.variables):
            break
            
        # Seleccionar variable no asignada con mayor VOI
        unassigned = [v for v in csp.variables if v not in asignacion]
        if not unassigned:
            break
            
        selected_var = select_variable_by_voi(unassigned, csp, conflict_history, asignacion, exploration_factor)
        
        # Seleccionar valor con menor conflicto esperado
        selected_val = select_value_by_voi(selected_var, csp, conflict_history, asignacion)
        
        # Asignar el valor
        asignacion[selected_var] = selected_val
        
        # Actualizar historial de conflictos
        update_conflict_history(selected_var, selected_val, asignacion, csp, conflict_history)
    
    # Verificar consistencia final
    if all(consistente(var, asignacion[var], asignacion, csp) for var in csp.variables):
        return asignacion
    else:
        # Si no es consistente, intentar reparar
        return repair_solution(asignacion, csp, conflict_history)

def select_variable_by_voi(unassigned, csp, conflict_history, asignacion, exploration_factor):
    """Selecciona variable basada en el Valor de la Información"""
    voi_scores = []
    
    for var in unassigned:
        # Calcular incertidumbre actual (entropía de los conflictos)
        conflict_counts = [conflict_history[var][val] for val in csp.dominios[var]]
        total_conflicts = sum(conflict_counts) + 1e-6  # Evitar división por cero
        probabilities = [count/total_conflicts for count in conflict_counts]
        current_entropy = -sum(p * math.log(p+1e-6) for p in probabilities)
        
        # Calcular reducción esperada de entropía para cada posible valor
        expected_entropy_reduction = 0
        for val in csp.dominios[var]:
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
        
        voi_scores.append(voi + exploration_bonus)
    
    # Seleccionar variable con mayor VOI
    return unassigned[np.argmax(voi_scores)]

def select_value_by_voi(var, csp, conflict_history, asignacion):
    """Selecciona valor basado en VOI y conflicto esperado"""
    conflict_scores = []
    
    for val in csp.dominios[var]:
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
    """Estima el número de conflictos que produciría una