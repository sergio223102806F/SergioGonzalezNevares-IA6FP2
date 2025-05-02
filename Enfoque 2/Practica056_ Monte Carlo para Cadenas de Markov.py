# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 15:05:57 2025

@author: elvin
"""

import random
from collections import defaultdict

def muestreo_gibbs(red_bayesiana, evidencia, n_muestras, burn_in=100, lag=5):
    """
    Implementación del muestreo de Gibbs para inferencia aproximada en redes bayesianas.
    
    Args:
        red_bayesiana (dict): Representación de la red bayesiana
        evidencia (dict): Variables observadas con sus valores {var: valor}
        n_muestras (int): Número de muestras a generar después del burn-in
        burn_in (int): Número de muestras iniciales a descartar (período de quemado)
        lag (int): Número de pasos entre muestras para reducir autocorrelación
        
    Returns:
        dict: Distribución de probabilidad aproximada para las variables de consulta
    """
    # Inicialización
    variables = list(red_bayesiana.keys())
    variables_no_evidencia = [var for var in variables if var not in evidencia]
    
    # Inicializar muestra actual con valores aleatorios para variables no observadas
    muestra_actual = {}
    for var in variables:
        if var in evidencia:
            muestra_actual[var] = evidencia[var]
        else:
            # Muestrear valor inicial aleatorio
            valores_posibles = list(red_bayesiana[var]['tabla'][()].keys())
            muestra_actual[var] = random.choice(valores_posibles)
    
    # Almacenar resultados
    contadores = defaultdict(int)
    total_muestras = 0
    
    # Fase de burn-in (quemado)
    for _ in range(burn_in):
        muestra_actual = paso_gibbs(muestra_actual, red_bayesiana, variables_no_evidencia)
    
    # Fase de muestreo principal
    muestras = []
    for i in range(n_muestras * lag):
        muestra_actual = paso_gibbs(muestra_actual, red_bayesiana, variables_no_evidencia)
        
        # Tomar muestra cada 'lag' iteraciones
        if i % lag == 0:
            muestras.append(muestra_actual.copy())
            total_muestras += 1
            
            # Actualizar contadores
            for var in variables_no_evidencia:
                contadores[(var, muestra_actual[var])] += 1
    
    # Calcular distribuciones de probabilidad
    distribucion = {k: v/total_muestras for k, v in contadores.items()}
    
    return distribucion

def paso_gibbs(muestra_actual, red_bayesiana, variables_no_evidencia):
    """
    Realiza un paso completo del muestreo de Gibbs.
    
    Args:
        muestra_actual (dict): Estado actual de la cadena de Markov
        red_bayesiana (dict): Estructura de la red bayesiana
        variables_no_evidencia (list): Variables a muestrear
        
    Returns:
        dict: Nueva muestra después de un paso completo de Gibbs
    """
    nueva_muestra = muestra_actual.copy()
    
    # Muestrear cada variable no observada en orden
    for var in variables_no_evidencia:
        # Calcular distribución condicional P(var | Markov Blanket(var))
        dist_cond = distribucion_condicional(var, nueva_muestra, red_bayesiana)
        
        # Muestrear nuevo valor de esta distribución
        nuevo_valor = muestrear_distribucion(dist_cond)
        nueva_muestra[var] = nuevo_valor
    
    return nueva_muestra

def distribucion_condicional(variable, muestra, red_bayesiana):
    """
    Calcula la distribución condicional de una variable dado su manta de Markov.
    
    Args:
        variable (str): Variable a muestrear
        muestra (dict): Estado actual de todas las variables
        red_bayesiana (dict): Estructura de la red
        
    Returns:
        dict: Distribución condicional {valor: probabilidad}
    """
    # Obtener padres de la variable
    padres = red_bayesiana[variable]['padres']
    valores_padres = tuple(muestra[padre] for padre in padres)
    
    # Probabilidad P(variable | padres)
    p_variable_dado_padres = red_bayesiana[variable]['tabla'][valores_padres]
    
    # Obtener hijos de la variable
    hijos = []
    for var in red_bayesiana:
        if variable in red_bayesiana[var]['padres']:
            hijos.append(var)
    
    # Calcular producto con P(hijos | sus padres) para cada valor de la variable
    distribucion = {}
    for valor in p_variable_dado_padres:
        # Iniciar con P(variable | padres)
        probabilidad = p_variable_dado_padres[valor]
        
        # Multiplicar por P(hijo | sus padres) para cada hijo
        for hijo in hijos:
            padres_hijo = red_bayesiana[hijo]['padres']
            valores_padres_hijo = []
            
            for padre in padres_hijo:
                if padre == variable:
                    valores_padres_hijo.append(valor)
                else:
                    valores_padres_hijo.append(muestra[padre])
            
            valores_padres_hijo = tuple(valores_padres_hijo)
            prob_hijo = red_bayesiana[hijo]['tabla'][valores_padres_hijo][muestra[hijo]]
            probabilidad *= prob_hijo
        
        distribucion[valor] = probabilidad
    
    # Normalizar la distribución
    total = sum(distribucion.values())
    if total > 0:
        distribucion = {k: v/total for k, v in distribucion.items()}
    
    return distribucion

def muestrear_distribucion(prob_dist):
    """
    Muestrea un valor de una distribución discreta.
    
    Args:
        prob_dist (dict): Distribución de probabilidad {valor: probabilidad}
        
    Returns:
        Valor muestreado
    """
    rand = random.random()
    acumulado = 0.0
    for valor, prob in prob_dist.items():
        acumulado += prob
        if rand <= acumulado:
            return valor
    return list(prob_dist.keys())[-1]

# Ejemplo de uso
if __name__ == "__main__":
    # Definir la misma red bayesiana del ejemplo anterior para comparación
    red_bayesiana = {
        'A': {
            'padres': [],
            'tabla': {
                (): {'a1': 0.6, 'a2': 0.4}
            }
        },
        'B': {
            'padres': ['A'],
            'tabla': {
                ('a1',): {'b1': 0.7, 'b2': 0.3},
                ('a2',): {'b1': 0.2, 'b2': 0.8}
            }
        },
        'C': {
            'padres': ['B'],
            'tabla': {
                ('b1',): {'c1': 0.9, 'c2': 0.1},
                ('b2',): {'c1': 0.4, 'c2': 0.6}
            }
        }
    }
    
    # Definir evidencia (por ejemplo, C='c1')
    evidencia = {'C': 'c1'}
    
    # Parámetros del MCMC
    n_muestras = 5000  # Número de muestras después del burn-in
    burn_in = 1000     # Muestras iniciales a descartar
    lag = 5            # Pasos entre muestras
    
    # Realizar inferencia con MCMC (Gibbs sampling)
    distribucion = muestreo_gibbs(red_bayesiana, evidencia, n_muestras, burn_in, lag)
    
    # Mostrar resultados
    print("\nDistribución aproximada usando MCMC (Gibbs sampling):")
    for (variable, valor), prob in sorted(distribucion.items()):
        print(f"P({variable}={valor} | evidencia) = {prob:.4f}")