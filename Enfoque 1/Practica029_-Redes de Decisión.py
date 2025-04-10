# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 13:48:24 2025

@author: elvin
"""

import numpy as np
from collections import defaultdict
import random

class POMDP_CSP:
    def __init__(self, variables, dominios, restricciones):
        self.variables = variables
        self.dominios = dominios
        self.restricciones = restricciones
        self.vecinos = {v: set() for v in variables}
        for (v1, v2) in restricciones:
            self.vecinos[v1].add(v2)
            self.vecinos[v2].add(v1)
        
        # Espacio de creencias (distribución de probabilidad sobre estados)
        self.belief = self.initial_belief()
    
    def initial_belief(self):
        """Inicializa la creencia como distribución uniforme sobre asignaciones posibles"""
        # Simplificación: creencia independiente para cada variable
        belief = {}
        for var in self.variables:
            belief[var] = {val: 1.0/len(self.dominios[var]) for val in self.dominios[var]}
        return belief
    
    def update_belief(self, var, val, obs_conflictos):
        """Actualiza la creencia basada en una acción y observación"""
        # Actualizar la creencia sobre la variable asignada
        for v in self.belief:
            if v == var:
                # Certeza después de la asignación
                self.belief[v] = {val: 1.0}
            else:
                # Actualizar creencia basada en observación de conflictos
                if obs_conflictos > 0:
                    # Reducir probabilidad de valores que causan conflictos
                    for val_v in self.belief[v]:
                        conflictos = sum(1 for vecino in self.vecinos[v] 
                                      if vecino == var and not cumple_restriccion(val_v, val))
                        self.belief[v][val_v] *= (0.5 ** conflictos)
                
                # Normalizar
                total = sum(self.belief[v].values())
                if total > 0:
                    for val_v in self.belief[v]:
                        self.belief[v][val_v] /= total

def pomdp_solve_csp(csp, max_iter=100, horizon=10, n_samples=100):
    """Resuelve el CSP usando aproximación de POMDP"""
    # Implementación usando aproximación de muestreo de creencias
    
    # Función de valor Q aproximada
    Q = defaultdict(float)
    
    # Historial de mejores políticas encontradas
    best_policy = None
    best_score = -float('inf')
    
    for _ in range(max_iter):
        # Muestrear estados de la creencia actual
        states = [sample_state(csp.belief) for _ in range(n_samples)]
        
        # Evaluar política greedy basada en Q actual
        policy = {}
        total_score = 0
        
        for t in range(horizon):
            # Seleccionar acción para cada estado muestreado
            action_counts = defaultdict(int)
            
            for state in states:
                # Encontrar variable no asignada con mayor incertidumbre
                unassigned = [v for v in csp.variables if v not in state]
                if not unassigned:
                    continue
                
                var = max(unassigned, key=lambda v: entropy(csp.belief[v]))
                
                # Seleccionar mejor valor según Q y creencia
                best_val = max(csp.dominios[var], 
                             key=lambda val: Q.get((var, val), 0) * csp.belief[var].get(val, 0))
                
                action_counts[(var, best_val)] += 1
            
            if not action_counts:
                break
                
            # Seleccionar acción más frecuente
            action = max(action_counts.items(), key=lambda x: x[1])[0]
            var, val = action
            policy[var] = val
            
            # Simular acción y observación para cada estado
            new_states = []
            total_score = 0
            
            for state in states:
                if var in state:
                    continue
                
                # Aplicar acción
                new_state = state.copy()
                new_state[var] = val
                
                # Observar conflictos (simulado)
                obs_conflictos = sum(1 for vecino in csp.vecinos[var] 
                                   if vecino in new_state and 
                                   not cumple_restriccion(val, new_state[vecino]))
                
                # Actualizar creencia (simulado)
                csp.update_belief(var, val, obs_conflictos)
                
                # Calcular recompensa
                reward = -obs_conflictos
                total_score += reward
                
                new_states.append(new_state)
            
            states = new_states
            
            if not states:
                break
        
        # Actualizar mejor política si corresponde
        if total_score > best_score:
            best_score = total_score
            best_policy = policy
    
    # Verificar si la política es solución válida
    if best_policy and all(consistente(var, best_policy[var], best_policy, csp) 
                         for var in csp.variables if var in best_policy):
        # Completar asignación si es necesario
        for var in csp.variables:
            if var not in best_policy:
                best_policy[var] = max(csp.dominios[var], 
                                     key=lambda val: csp.belief[var].get(val, 0))
        return best_policy
    else:
        # Usar búsqueda con información de creencia
        return pomdp_backtracking({}, csp)

def pomdp_backtracking(asignacion, csp):
    """Backtracking usando la creencia del POMDP como guía"""
    if len(asignacion) == len(csp.variables):
        return asignacion
    
    # Seleccionar variable con mayor entropía (más incertidumbre)
    unassigned = [v for v in csp.variables if v not in asignacion]
    var = max(unassigned, key=lambda v: entropy(csp.belief[v]))
    
    # Ordenar valores por probabilidad en la creencia
    valores_ordenados = sorted(csp.dominios[var], 
                             key=lambda val: -csp.belief[var].get(val, 0))
    
    for valor in valores_ordenados:
        if consistente(var, valor, asignacion, csp):
            asignacion[var] = valor
            
            # Simular observación de conflictos
            obs_conflictos = sum(1 for vecino in csp.vecinos[var] 
                               if vecino in asignacion and 
                               not cumple_restriccion(valor, asignacion[vecino]))
            
            # Actualizar creencia localmente
            old_belief = {v: dict(csp.belief[v]) for v in csp.belief}
            csp.update_belief(var, valor, obs_conflictos)
            
            resultado = pomdp_backtracking(asignacion, csp)
            if resultado is not None:
                return resultado
            
            # Restaurar creencia
            csp.belief = old_belief
            del asignacion[var]
    return None

def sample_state(belief):
    """Muestrea un estado de la distribución de creencia"""
    state = {}
    for var in belief:
        probs = list(belief[var].values())
        vals = list(belief[var].keys())
        state[var] = random.choices(vals, weights=probs)[0]
    return state

def entropy(dist):
    """Calcula la entropía de una distribución discreta"""
    probs = [p for p in dist.values() if p > 0]
    return -sum(p * np.log(p) for p in probs) if probs else 0

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
    
    return POMDP_CSP(variables, dominios, restricciones)

if __name__ == "__main__":
    np.random.seed(42)
    random.seed(42)
    
    sudoku = crear_sudoku_4x4()
    
    # Asignar algunas pistas
    pistas = {(0,0):1, (0,2):3, (1,1):4, (3,3):2}
    for (i,j), val in pistas.items():
        sudoku.dominios[(i,j)] = [val]
        sudoku.belief[(i,j)] = {val: 1.0}  # Certeza absoluta en las pistas
    
    # Resolver con POMDP
    solucion = pomdp_solve_csp(sudoku)
    
    if solucion:
        print("Solución encontrada:")
        for i in range(4):
            print([solucion.get((i,j), 0) for j in range(4)])
    else:
        print("No se encontró solución")