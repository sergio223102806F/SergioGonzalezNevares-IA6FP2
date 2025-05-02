# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 14:43:15 2025

@author: elvin
"""

import random
from collections import defaultdict

class MuestreoDirecto:
    def __init__(self, red_bayesiana):
        """Inicializa el muestreador con una red bayesiana existente"""
        self.red = red_bayesiana  # Almacena la red bayesiana
        self.nodos_ordenados = self.orden_topologico()  # Ordena los nodos para muestreo
    
    def orden_topologico(self):
        """Calcula el orden topológico de los nodos (padres antes que hijos)"""
        visitados = set()  # Nodos ya procesados
        orden = []  # Resultado del ordenamiento
        
        def dfs(nodo):
            """Recorrido en profundidad para orden topológico"""
            if nodo not in visitados:
                visitados.add(nodo)
                for hijo in self.red.estructura[nodo]:  # Visitar hijos primero
                    dfs(hijo)
                orden.append(nodo)  # Añadir nodo después de procesar hijos
        
        for nodo in self.red.nodos:  # Procesar todos los nodos no visitados
            if nodo not in visitados:
                dfs(nodo)
        return orden[::-1]  # Invertir para obtener el orden correcto
    
    def generar_muestra(self):
        """Genera una muestra completa de todas las variables de la red"""
        muestra = {}  # Diccionario para almacenar los valores muestreados
        
        for nodo in self.nodos_ordenados:  # Muestrear en orden topológico
            padres = self.red.nodos[nodo].padres  # Obtener padres del nodo
            
            if not padres:  # Si no tiene padres (nodo raíz)
                # Usar probabilidad marginal P(X=True)
                prob = self.red.nodos[nodo].tabla_prob[True]
            else:
                # Obtener valores de los padres ya muestreados
                padres_vals = tuple(muestra[p.nombre] for p in padres)
                # Obtener P(X=True|padres)
                prob = self.red.nodos[nodo].tabla_prob.get(padres_vals, {}).get(True, 0)
            
            # Muestrear el valor basado en la probabilidad
            muestra[nodo] = random.random() < prob  # True si random() < prob
            
        return muestra
    
    def inferencia(self, consulta, evidencias={}, n_muestras=10000):
        """
        Realiza inferencia estadística por muestreo directo
        
        Args:
            consulta: Tupla (nodo, valor) que queremos estimar
            evidencias: Diccionario {nodo: valor} de variables observadas
            n_muestras: Número total de muestras a generar
            
        Returns:
            float: Probabilidad estimada P(consulta|evidencias)
        """
        muestras_validas = 0  # Contador de muestras consistentes con evidencias
        muestras_consulta = 0  # Contador de muestras que cumplen la consulta
        
        for _ in range(n_muestras):
            muestra = self.generar_muestra()  # Generar nueva muestra
            
            # Verificar si la muestra es consistente con las evidencias
            consistente = all(muestra[n] == v for n, v in evidencias.items())
            
            if consistente:
                muestras_validas += 1
                if muestra[consulta[0]] == consulta[1]:  # Si cumple la consulta
                    muestras_consulta += 1
        
        # Calcular probabilidad condicional
        return muestras_consulta / muestras_validas if muestras_validas > 0 else 0