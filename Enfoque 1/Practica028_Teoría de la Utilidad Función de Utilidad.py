# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 13:46:32 2025

@author: elvin
"""

import numpy as np
from collections import defaultdict

class AgenteUtilidad:
    def __init__(self, estados, acciones, funcion_utilidad, funcion_transicion, gamma=0.9):
        """
        estados: Lista de estados posibles
        acciones: Lista de acciones posibles
        funcion_utilidad: dict {estado: valor_utilidad}
        funcion_transicion: dict {(estado, accion): {'estado': nuevo_estado, 'prob': probabilidad}}
        gamma: Factor de descuento (0-1)
        """
        self.estados = estados
        self.acciones = acciones
        self.utilidad = funcion_utilidad.copy()
        self.transicion = funcion_transicion
        self.gamma = gamma
    
    def tomar_decision(self, estado_actual):
        """Selecciona la acción que maximiza la utilidad esperada"""
        mejor_accion = None
        max_utilidad = -np.inf
        
        for accion in self.acciones:
            utilidad_accion = self.calcular_utilidad_accion(estado_actual, accion)
            if utilidad_accion > max_utilidad:
                max_utilidad = utilidad_accion
                mejor_accion = accion
        
        return mejor_accion
    
    def calcular_utilidad_accion(self, estado, accion):
        """Calcula la utilidad esperada de una acción"""
        if (estado, accion) not in self.transicion:
            return -np.inf  # Acción no permitida desde este estado
        
        utilidad_esperada = 0
        for resultado in self.transicion[(estado, accion)]:
            nuevo_estado = resultado['estado']
            probabilidad = resultado['prob']
            recompensa = self.utilidad[nuevo_estado]
            utilidad_esperada += probabilidad * (recompensa + self.gamma * self.utilidad[nuevo_estado])
        
        return utilidad_esperada
    
    def actualizar_utilidades(self, iteraciones=100):
        """Iteración de valor para calcular utilidades óptimas"""
        for _ in range(iteraciones):
            nuevas_utilidades = defaultdict(float)
            for estado in self.estados:
                max_utilidad = -np.inf
                for accion in self.acciones:
                    utilidad_accion = self.calcular_utilidad_accion(estado, accion)
                    if utilidad_accion > max_utilidad:
                        max_utilidad = utilidad_accion
                nuevas_utilidades[estado] = max_utilidad if max_utilidad != -np.inf else self.utilidad[estado]
            self.utilidad = dict(nuevas_utilidades)

# Ejemplo: Decisión de inversión
if __name__ == "__main__":
    # Definición del problema
    estados = ['bajo', 'medio', 'alto']
    acciones = ['conservador', 'moderado', 'agresivo']
    
    # Función de utilidad inicial (puede ser aprendida)
    funcion_utilidad = {
        'bajo': 2,
        'medio': 5,
        'alto': 10
    }
    
    # Función de transición (modelo del entorno)
    funcion_transicion = {
        ('bajo', 'conservador'): [{'estado': 'bajo', 'prob': 0.7}, {'estado': 'medio', 'prob': 0.3}],
        ('bajo', 'moderado'): [{'estado': 'bajo', 'prob': 0.4}, {'estado': 'medio', 'prob': 0.5}, {'estado': 'alto', 'prob': 0.1}],
        ('bajo', 'agresivo'): [{'estado': 'bajo', 'prob': 0.1}, {'estado': 'medio', 'prob': 0.3}, {'estado': 'alto', 'prob': 0.6}],
        
        ('medio', 'conservador'): [{'estado': 'bajo', 'prob': 0.3}, {'estado': 'medio', 'prob': 0.7}],
        ('medio', 'moderado'): [{'estado': 'bajo', 'prob': 0.2}, {'estado': 'medio', 'prob': 0.5}, {'estado': 'alto', 'prob': 0.3}],
        ('medio', 'agresivo'): [{'estado': 'bajo', 'prob': 0.1}, {'estado': 'medio', 'prob': 0.4}, {'estado': 'alto', 'prob': 0.5}],
        
        ('alto', 'conservador'): [{'estado': 'medio', 'prob': 0.4}, {'estado': 'alto', 'prob': 0.6}],
        ('alto', 'moderado'): [{'estado': 'medio', 'prob': 0.3}, {'estado': 'alto', 'prob': 0.7}],
        ('alto', 'agresivo'): [{'estado': 'medio', 'prob': 0.2}, {'estado': 'alto', 'prob': 0.8}]
    }
    
    # Crear agente
    agente = AgenteUtilidad(estados, acciones, funcion_utilidad, funcion_transicion, gamma=0.9)
    
    # Calcular utilidades óptimas
    print("Utilidades iniciales:", agente.utilidad)
    agente.actualizar_utilidades(iteraciones=50)
    print("Utilidades óptimas calculadas:", agente.utilidad)
    
    # Tomar decisiones en diferentes estados
    for estado in estados:
        decision = agente.tomar_decision(estado)
        print(f"En estado '{estado}', la mejor acción es '{decision}'")