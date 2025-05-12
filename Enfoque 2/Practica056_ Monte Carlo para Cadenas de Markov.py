# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 15:05:57 2025

@author: elvin
"""

# Importación de librerías necesarias
import random  # Para generar números aleatorios
from collections import defaultdict  # Para crear diccionarios con valores por defecto

# Función principal para realizar muestreo de Gibbs en una red bayesiana
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
    # Obtener todas las variables de la red
    variables = list(red_bayesiana.keys())
    # Identificar variables no observadas (sin evidencia)
    variables_no_evidencia = [var for var in variables if var not in evidencia]
    
    # Inicializar el estado actual de la muestra
    muestra_actual = {}
    for var in variables:
        if var in evidencia:
            muestra_actual[var] = evidencia[var]  # Asignar valor observado
        else:
            # Elegir valor aleatorio inicial para variables no observadas
            valores_posibles = list(red_bayesiana[var]['tabla'][()].keys())
            muestra_actual[var] = random.choice(valores_posibles)
    
    # Inicializar contador de frecuencias de muestras
    contadores = defaultdict(int)
    total_muestras = 0  # Contador de muestras efectivas
    
    # Etapa de burn-in (descartar muestras iniciales para estabilizar)
    for _ in range(burn_in):
        muestra_actual = paso_gibbs(muestra_actual, red_bayesiana, variables_no_evidencia)
    
    # Etapa principal de muestreo
    muestras = []  # Lista para almacenar muestras tomadas
    for i in range(n_muestras * lag):
        # Realizar un paso del muestreo de Gibbs
        muestra_actual = paso_gibbs(muestra_actual, red_bayesiana, variables_no_evidencia)
        
        # Guardar muestra cada cierto número de iteraciones (según lag)
        if i % lag == 0:
            muestras.append(muestra_actual.copy())  # Guardar copia de la muestra actual
            total_muestras += 1  # Incrementar el conteo de muestras
            
            # Contar ocurrencias de valores de variables no observadas
            for var in variables_no_evidencia:
                contadores[(var, muestra_actual[var])] += 1
    
    # Calcular distribución de probabilidad a partir de las frecuencias
    distribucion = {k: v/total_muestras for k, v in contadores.items()}
    
    return distribucion  # Retornar distribución aproximada

# Función para realizar un solo paso del muestreo de Gibbs
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
    nueva_muestra = muestra_actual.copy()  # Copiar estado actual
    
    # Iterar sobre cada variable no observada
    for var in variables_no_evidencia:
        # Calcular la distribución condicional para esa variable
        dist_cond = distribucion_condicional(var, nueva_muestra, red_bayesiana)
        # Muestrear nuevo valor de la distribución condicional
        nuevo_valor = muestrear_distribucion(dist_cond)
        # Actualizar valor de la variable en la muestra
        nueva_muestra[var] = nuevo_valor
    
    return nueva_muestra  # Retornar nueva muestra

# Función para calcular la distribución condicional de una variable
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
    # Obtener valores actuales de los padres en la muestra
    valores_padres = tuple(muestra[padre] for padre in padres)
    
    # Obtener la distribución P(variable | padres)
    p_variable_dado_padres = red_bayesiana[variable]['tabla'][valores_padres]
    
    # Identificar los hijos de la variable actual
    hijos = []
    for var in red_bayesiana:
        if variable in red_bayesiana[var]['padres']:
            hijos.append(var)
    
    # Calcular la distribución multiplicando por P(hijos | sus padres)
    distribucion = {}
    for valor in p_variable_dado_padres:
        probabilidad = p_variable_dado_padres[valor]  # Probabilidad inicial
        
        # Multiplicar por la probabilidad de los hijos
        for hijo in hijos:
            padres_hijo = red_bayesiana[hijo]['padres']
            valores_padres_hijo = []
            
            for padre in padres_hijo:
                if padre == variable:
                    valores_padres_hijo.append(valor)  # Usar el valor propuesto
                else:
                    valores_padres_hijo.append(muestra[padre])  # Usar valor actual
            
            valores_padres_hijo = tuple(valores_padres_hijo)
            prob_hijo = red_bayesiana[hijo]['tabla'][valores_padres_hijo][muestra[hijo]]
            probabilidad *= prob_hijo  # Producto de probabilidades
        
        distribucion[valor] = probabilidad  # Guardar probabilidad final para ese valor
    
    # Normalizar la distribución para que sume 1
    total = sum(distribucion.values())
    if total > 0:
        distribucion = {k: v/total for k, v in distribucion.items()}
    
    return distribucion  # Retornar distribución condicional normalizada

# Función auxiliar para muestrear un valor de una distribución discreta
def muestrear_distribucion(prob_dist):
    """
    Muestrea un valor de una distribución discreta.
    
    Args:
        prob_dist (dict): Distribución de probabilidad {valor: probabilidad}
        
    Returns:
        Valor muestreado
    """
    rand = random.random()  # Generar número aleatorio en [0, 1]
    acumulado = 0.0  # Inicializar acumulador de probabilidad
    for valor, prob in prob_dist.items():
        acumulado += prob  # Sumar probabilidad
        if rand <= acumulado:
            return valor  # Retornar valor correspondiente
    return list(prob_dist.keys())[-1]  # Retorno por defecto si no se encontró antes

# Bloque principal para ejecutar un ejemplo de uso
if __name__ == "__main__":
    # Definir red bayesiana de prueba
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
    
    # Definir evidencia (por ejemplo, que C = 'c1')
    evidencia = {'C': 'c1'}
    
    # Parámetros del muestreo MCMC
    n_muestras = 5000  # Número de muestras a recolectar después del burn-in
    burn_in = 1000     # Número de muestras a descartar al inicio
    lag = 5            # Separación entre muestras para reducir autocorrelación
    
    # Ejecutar el muestreo de Gibbs para inferencia
    distribucion = muestreo_gibbs(red_bayesiana, evidencia, n_muestras, burn_in, lag)
    
    # Mostrar resultados de la inferencia
    print("\nDistribución aproximada usando MCMC (Gibbs sampling):")
    for (variable, valor), prob in sorted(distribucion.items()):
        print(f"P({variable}={valor} | evidencia) = {prob:.4f}")
