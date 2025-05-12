# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 14:13:42 2025

@author: elvin
"""

import numpy as np                   # Importa numpy para operaciones numéricas
from collections import defaultdict  # Importa defaultdict para diccionarios por defecto
import random                       # Importa random para generación aleatoria

class POMDP_CSP:                    # Clase para CSP con incertidumbre (POMDP)
    def __init__(self, variables, dominios, restricciones):
        """Constructor que inicializa el POMDP-CSP:
        variables: Lista de variables del problema
        dominios: Diccionario {variable: valores_posibles}
        restricciones: Lista de tuplas de variables con restricciones
        """
        self.variables = variables   # Almacena las variables del problema
        self.dominios = dominios     # Almacena los dominios de cada variable
        self.restricciones = restricciones  # Almacena las restricciones
        
        # Diccionario de vecinos para cada variable
        self.vecinos = {v: set() for v in variables}  # Inicializa conjuntos vacíos
        for (v1, v2) in restricciones:  # Para cada restricción
            self.vecinos[v1].add(v2)    # Añade v2 como vecino de v1
            self.vecinos[v2].add(v1)    # Añade v1 como vecino de v2 (no dirigido)
        
        # Espacio de creencias (distribución de probabilidad sobre estados)
        self.belief = self.initial_belief()  # Inicializa la creencia
    
    def initial_belief(self):
        """Inicializa la creencia como distribución uniforme:
        Returns:
            Diccionario con distribución inicial uniforme
        """
        belief = {}                   # Diccionario para almacenar creencias
        for var in self.variables:    # Para cada variable
            # Crea distribución uniforme sobre su dominio
            belief[var] = {val: 1.0/len(self.dominios[var]) for val in self.dominios[var]}
        return belief                 # Retorna creencia inicializada
    
    def update_belief(self, var, val, obs_conflictos):
        """Actualiza la creencia basada en acción y observación:
        var: Variable que fue asignada
        val: Valor que fue asignado
        obs_conflictos: Número de conflictos observados
        """
        # Actualiza creencia para todas las variables
        for v in self.belief:         # Para cada variable en la creencia
            if v == var:              # Para la variable asignada
                self.belief[v] = {val: 1.0}  # Certeza absoluta (asignación conocida)
            else:                     # Para otras variables
                if obs_conflictos > 0:  # Si hubo conflictos observados
                    # Reduce probabilidad de valores conflictivos
                    for val_v in self.belief[v]:
                        # Cuenta conflictos con la variable asignada
                        conflictos = sum(1 for vecino in self.vecinos[v] 
                                      if vecino == var and not cumple_restriccion(val_v, val))
                        # Reduce probabilidad exponencialmente con conflictos
                        self.belief[v][val_v] *= (0.5 ** conflictos)
                
                # Normaliza la distribución de probabilidad
                total = sum(self.belief[v].values())
                if total > 0:         # Evita división por cero
                    for val_v in self.belief[v]:
                        self.belief[v][val_v] /= total  # Normaliza probabilidades

def pomdp_solve_csp(csp, max_iter=100, horizon=10, n_samples=100):
    """Resuelve CSP usando aproximación POMDP:
    csp: Instancia del problema POMDP_CSP
    max_iter: Máximo de iteraciones
    horizon: Horizonte de planificación
    n_samples: Número de muestras por iteración
    """
    # Función de valor Q aproximada
    Q = defaultdict(float)           # Diccionario para valores Q
    
    # Historial de mejores políticas
    best_policy = None               # Mejor política encontrada
    best_score = -float('inf')       # Mejor puntuación encontrada
    
    for _ in range(max_iter):        # Realiza máximo de iteraciones
        # Muestrea estados de la creencia actual
        states = [sample_state(csp.belief) for _ in range(n_samples)]
        
        # Evalúa política greedy basada en Q actual
        policy = {}                  # Política actual
        total_score = 0              # Puntuación acumulada
        
        for t in range(horizon):     # Planifica hasta el horizonte
            # Selecciona acción para cada estado muestreado
            action_counts = defaultdict(int)  # Contador de acciones
            
            for state in states:     # Para cada estado muestreado
                # Encuentra variables no asignadas
                unassigned = [v for v in csp.variables if v not in state]
                if not unassigned:   # Si todas asignadas, continuar
                    continue
                
                # Selecciona variable con mayor incertidumbre (entropía)
                var = max(unassigned, key=lambda v: entropy(csp.belief[v]))
                
                # Selecciona mejor valor según Q y creencia
                best_val = max(csp.dominios[var], 
                             key=lambda val: Q.get((var, val), 0) * csp.belief[var].get(val, 0))
                
                action_counts[(var, best_val)] += 1  # Cuenta esta acción
            
            if not action_counts:    # Si no hay acciones posibles
                break               # Termina esta iteración
                
            # Selecciona acción más frecuente
            action = max(action_counts.items(), key=lambda x: x[1])[0]
            var, val = action       # Desempaqueta la acción
            policy[var] = val       # Añade a la política
            
            # Simula acción y observación para cada estado
            new_states = []         # Nuevos estados después de acción
            total_score = 0         # Reinicia puntuación
            
            for state in states:    # Para cada estado muestreado
                if var in state:    # Si ya está asignada, saltar
                    continue
                
                # Aplica acción (asignar valor)
                new_state = state.copy()
                new_state[var] = val
                
                # Observa conflictos (simulado)
                obs_conflictos = sum(1 for vecino in csp.vecinos[var] 
                                   if vecino in new_state and 
                                   not cumple_restriccion(val, new_state[vecino]))
                
                # Actualiza creencia (simulado)
                csp.update_belief(var, val, obs_conflictos)
                
                # Calcula recompensa (negativa de conflictos)
                reward = -obs_conflictos
                total_score += reward  # Acumula puntuación
                
                new_states.append(new_state)  # Añade nuevo estado
            
            states = new_states      # Actualiza estados para siguiente paso
            
            if not states:           # Si no quedan estados
                break               # Termina esta iteración
        
        # Actualiza mejor política si corresponde
        if total_score > best_score:  # Si mejora puntuación
            best_score = total_score  # Actualiza mejor puntuación
            best_policy = policy      # Actualiza mejor política
    
    # Verifica si la política es solución válida
    if best_policy and all(consistente(var, best_policy[var], best_policy, csp) 
                         for var in csp.variables if var in best_policy):
        # Completa asignación si es necesario
        for var in csp.variables:
            if var not in best_policy:
                # Asigna valor más probable según creencia
                best_policy[var] = max(csp.dominios[var], 
                                     key=lambda val: csp.belief[var].get(val, 0))
        return best_policy            # Retorna solución encontrada
    else:
        # Usa búsqueda con información de creencia
        return pomdp_backtracking({}, csp)  # Intenta con backtracking

def pomdp_backtracking(asignacion, csp):
    """Backtracking usando la creencia del POMDP como guía:
    asignacion: Asignación parcial actual
    csp: Instancia del problema
    """
    if len(asignacion) == len(csp.variables):  # Si asignación completa
        return asignacion                     # Retorna solución
    
    # Selecciona variable con mayor entropía (más incertidumbre)
    unassigned = [v for v in csp.variables if v not in asignacion]
    var = max(unassigned, key=lambda v: entropy(csp.belief[v]))
    
    # Ordena valores por probabilidad en creencia (mayor a menor)
    valores_ordenados = sorted(csp.dominios[var], 
                             key=lambda val: -csp.belief[var].get(val, 0))
    
    for valor in valores_ordenados:   # Prueba valores en orden
        if consistente(var, valor, asignacion, csp):  # Si es consistente
            asignacion[var] = valor   # Asigna valor
            
            # Simula observación de conflictos
            obs_conflictos = sum(1 for vecino in csp.vecinos[var] 
                               if vecino in asignacion and 
                               not cumple_restriccion(valor, asignacion[vecino]))
            
            # Guarda creencia anterior y actualiza localmente
            old_belief = {v: dict(csp.belief[v]) for v in csp.belief}
            csp.update_belief(var, valor, obs_conflictos)
            
            # Llama recursivamente
            resultado = pomdp_backtracking(asignacion, csp)
            if resultado is not None:  # Si encontró solución
                return resultado       # Retorna solución
            
            # Restaura creencia anterior
            csp.belief = old_belief
            del asignacion[var]       # Deshace asignación
    return None                      # No encontró solución

def sample_state(belief):
    """Muestrea un estado de la distribución de creencia:
    belief: Distribución de probabilidad sobre estados
    """
    state = {}                       # Estado a muestrear
    for var in belief:               # Para cada variable
        probs = list(belief[var].values())  # Probabilidades
        vals = list(belief[var].keys())     # Valores posibles
        # Muestrea valor según distribución
        state[var] = random.choices(vals, weights=probs)[0]
    return state                     # Retorna estado muestreado

def entropy(dist):
    """Calcula la entropía de una distribución discreta:
    dist: Diccionario {valor: probabilidad}
    """
    probs = [p for p in dist.values() if p > 0]  # Filtra probabilidades > 0
    return -sum(p * np.log(p) for p in probs) if probs else 0  # Calcula entropía

def consistente(var, valor, asignacion, csp):
    """Verifica si una asignación es consistente:
    var: Variable asignada
    valor: Valor asignado
    asignacion: Asignación parcial actual
    csp: Instancia del problema
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
    """Crea una instancia de Sudoku 4x4 como POMDP_CSP"""
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
    
    return POMDP_CSP(variables, dominios, restricciones)  # Retorna instancia

if __name__ == "__main__":            # Bloque principal de ejecución
    np.random.seed(42)                # Fija semilla para reproducibilidad
    random.seed(42)                   # Fija semilla para aleatoriedad
    
    sudoku = crear_sudoku_4x4()       # Crea instancia de Sudoku
    
    # Asigna algunas pistas iniciales
    pistas = {(0,0):1, (0,2):3, (1,1):4, (3,3):2}
    for (i,j), val in pistas.items():
        sudoku.dominios[(i,j)] = [val]  # Fija dominio a valor pista
        sudoku.belief[(i,j)] = {val: 1.0}  # Certeza absoluta en pistas
    
    # Resuelve con enfoque POMDP
    solucion = pomdp_solve_csp(sudoku)
    
    # Muestra resultados
    if solucion:                      # Si encontró solución
        print("Solución encontrada:")
        for i in range(4):            # Imprime el tablero solución
            print([solucion.get((i,j), 0) for j in range(4)])
    else:
        print("No se encontró solución")  # Mensaje si no hay solución