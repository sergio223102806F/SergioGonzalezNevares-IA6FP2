# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 14:43:16 2025

@author: elvin
"""

# Importación de bibliotecas necesarias
import random  # Para generación de números aleatorios
from collections import defaultdict  # Para crear diccionarios con valores por defecto

def likelihood_weighting(evidencia, red_bayesiana, n_muestras):
    """
    Función principal que realiza inferencia aproximada usando Ponderación de Verosimilitud.
    
    Args:
        evidencia (dict): Diccionario con las variables observadas y sus valores {var: valor}
        red_bayesiana (dict): Representación de la red bayesiana con estructura y probabilidades
        n_muestras (int): Número de muestras a generar para la aproximación
        
    Returns:
        dict: Distribución de probabilidad aproximada para las variables de consulta
    """
    # Inicializar contadores para las variables de consulta
    distribucion = defaultdict(float)  # Almacena los pesos acumulados por cada valor
    pesos_totales = 0.0  # Acumula la suma total de todos los pesos
    
    # Generar las muestras ponderadas
    for _ in range(n_muestras):
        # Obtener una muestra y su peso correspondiente
        muestra, peso = generar_muestra_ponderada(evidencia, red_bayesiana)
        pesos_totales += peso  # Acumular el peso total
        
        # Actualizar la distribución con la muestra ponderada
        for variable in muestra:
            # Solo consideramos variables no observadas (las de consulta)
            if variable not in evidencia:
                # La clave es una tupla (variable, valor) y sumamos el peso
                distribucion[(variable, muestra[variable])] += peso
    
    # Normalizar la distribución dividiendo cada peso por el total
    for key in distribucion:
        distribucion[key] /= pesos_totales
        
    return dict(distribucion)  # Convertimos a diccionario regular antes de devolver

def generar_muestra_ponderada(evidencia, red_bayesiana):
    """
    Genera una muestra ponderada según la evidencia.
    
    Args:
        evidencia (dict): Variables observadas con sus valores fijos
        red_bayesiana (dict): Estructura completa de la red bayesiana
        
    Returns:
        tuple: (muestra, peso) donde:
               - muestra es un diccionario con los valores asignados a todas las variables
               - peso es el peso de verosimilitud calculado para esta muestra
    """
    muestra = {}  # Almacenará los valores asignados a cada variable
    peso = 1.0    # Inicializa el peso de la muestra
    
    # IMPORTANTE: Las variables deben procesarse en orden topológico (padres antes que hijos)
    # En un caso real, debería calcularse automáticamente el orden topológico
    # Aquí usamos un orden fijo como ejemplo
    orden = ['A', 'B', 'C']  # Ejemplo: A es raíz, luego B, luego C
    
    # Procesar cada variable en orden
    for variable in orden:
        if variable in evidencia:
            # Caso 1: Variable observada (está en la evidencia)
            valor = evidencia[variable]  # Tomamos el valor fijado
            
            # Obtenemos los padres de esta variable en la red
            padres = red_bayesiana[variable]['padres']
            
            # Obtenemos los valores de los padres en la muestra actual
            valores_padres = tuple(muestra[padre] for padre in padres)
            
            # Obtenemos la probabilidad condicional P(variable|padres)
            prob = red_bayesiana[variable]['tabla'][valores_padres][valor]
            
            # Actualizamos el peso multiplicando por esta probabilidad
            peso *= prob
            
            # Fijamos el valor observado en la muestra
            muestra[variable] = valor
        else:
            # Caso 2: Variable no observada (no está en la evidencia)
            padres = red_bayesiana[variable]['padres']
            
            # Obtenemos los valores de los padres en la muestra actual
            valores_padres = tuple(muestra[padre] for padre in padres)
            
            # Obtenemos la distribución condicional P(variable|padres)
            prob_dist = red_bayesiana[variable]['tabla'][valores_padres]
            
            # Muestreamos un valor de esta distribución
            valor = muestrear_distribucion(prob_dist)
            
            # Almacenamos el valor muestreado
            muestra[variable] = valor
    
    return muestra, peso

def muestrear_distribucion(prob_dist):
    """
    Muestrea un valor de una distribución discreta usando el método de transformada inversa.
    
    Args:
        prob_dist (dict): Distribución de probabilidad como {valor: probabilidad}
        
    Returns:
        Valor muestreado según la distribución dada
    """
    rand = random.random()  # Genera un número aleatorio entre 0 y 1
    acumulado = 0.0  # Acumula probabilidades para el método de transformada inversa
    
    # Iteramos sobre cada valor y su probabilidad
    for valor, prob in prob_dist.items():
        acumulado += prob  # Sumamos la probabilidad al acumulado
        
        # Si el número aleatorio cae en este intervalo, devolvemos el valor
        if rand <= acumulado:
            return valor
    
    # Por si hay errores de redondeo (debería ser casi imposible llegar aquí)
    return list(prob_dist.keys())[-1]

# Ejemplo de uso principal
if __name__ == "__main__":
    # Definir una red bayesiana simple (ejemplo con 3 variables A->B->C)
    red_bayesiana = {
        'A': {
            'padres': [],  # Variable raíz sin padres
            'tabla': {
                (): {'a1': 0.6, 'a2': 0.4}  # Distribución marginal P(A)
            }
        },
        'B': {
            'padres': ['A'],  # B tiene como padre a A
            'tabla': {
                ('a1',): {'b1': 0.7, 'b2': 0.3},  # P(B|A=a1)
                ('a2',): {'b1': 0.2, 'b2': 0.8}   # P(B|A=a2)
            }
        },
        'C': {
            'padres': ['B'],  # C tiene como padre a B
            'tabla': {
                ('b1',): {'c1': 0.9, 'c2': 0.1},  # P(C|B=b1)
                ('b2',): {'c1': 0.4, 'c2': 0.6}   # P(C|B=b2)
            }
        }
    }
    
    # Definir evidencia (por ejemplo, hemos observado que C='c1')
    evidencia = {'C': 'c1'}
    
    # Realizar inferencia con likelihood weighting
    n_muestras = 10000  # Número de muestras a generar (mayor -> más precisión)
    distribucion = likelihood_weighting(evidencia, red_bayesiana, n_muestras)
    
    # Mostrar resultados de forma ordenada
    print("Distribución aproximada usando Ponderación de Verosimilitud:")
    # Ordenamos los resultados para mostrarlos consistentemente
    for (variable, valor), prob in sorted(distribucion.items()):
        # Formateamos la salida con 4 decimales
        print(f"P({variable}={valor} | evidencia) = {prob:.4f}")