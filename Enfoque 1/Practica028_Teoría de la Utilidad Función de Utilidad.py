# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 13:46:32 2025

@author: elvin
"""

import numpy as np                   # Importa numpy para operaciones numéricas
from collections import defaultdict  # Importa defaultdict para diccionarios con valores por defecto

class AgenteUtilidad:                # Clase para representar un agente basado en utilidad
    def __init__(self, estados, acciones, funcion_utilidad, funcion_transicion, gamma=0.9):
        """
        Constructor del agente:
        estados: Lista de estados posibles
        acciones: Lista de acciones posibles
        funcion_utilidad: dict {estado: valor_utilidad}
        funcion_transicion: dict {(estado, accion): {'estado': nuevo_estado, 'prob': probabilidad}}
        gamma: Factor de descuento (0-1)
        """
        self.estados = estados       # Almacena los estados posibles
        self.acciones = acciones     # Almacena las acciones posibles
        self.utilidad = funcion_utilidad.copy()  # Copia la función de utilidad
        self.transicion = funcion_transicion  # Almacena la función de transición
        self.gamma = gamma           # Factor de descuento para recompensas futuras
    
    def tomar_decision(self, estado_actual):
        """Selecciona la acción que maximiza la utilidad esperada"""
        mejor_accion = None          # Inicializa la mejor acción como None
        max_utilidad = -np.inf       # Inicializa la máxima utilidad con -infinito
        
        for accion in self.acciones: # Itera sobre todas las acciones posibles
            utilidad_accion = self.calcular_utilidad_accion(estado_actual, accion)
            if utilidad_accion > max_utilidad:  # Si encontramos una acción mejor
                max_utilidad = utilidad_accion # Actualiza la máxima utilidad
                mejor_accion = accion           # Actualiza la mejor acción
        
        return mejor_accion          # Devuelve la mejor acción encontrada
    
    def calcular_utilidad_accion(self, estado, accion):
        """Calcula la utilidad esperada de una acción en un estado dado"""
        if (estado, accion) not in self.transicion:
            return -np.inf           # Si la acción no está permitida, devuelve -infinito
        
        utilidad_esperada = 0        # Inicializa la utilidad esperada
        
        for resultado in self.transicion[(estado, accion)]:  # Itera sobre resultados posibles
            nuevo_estado = resultado['estado']    # Obtiene el nuevo estado
            probabilidad = resultado['prob']       # Obtiene la probabilidad
            recompensa = self.utilidad[nuevo_estado]  # Obtiene la recompensa
            # Calcula la utilidad esperada con factor de descuento
            utilidad_esperada += probabilidad * (recompensa + self.gamma * self.utilidad[nuevo_estado])
        
        return utilidad_esperada     # Devuelve la utilidad esperada calculada
    
    def actualizar_utilidades(self, iteraciones=100):
        """Iteración de valor para calcular utilidades óptimas"""
        for _ in range(iteraciones): # Realiza el número especificado de iteraciones
            nuevas_utilidades = defaultdict(float)  # Crea un diccionario para nuevas utilidades
            
            for estado in self.estados:  # Itera sobre todos los estados
                max_utilidad = -np.inf   # Inicializa la máxima utilidad
                
                for accion in self.acciones:  # Itera sobre todas las acciones
                    utilidad_accion = self.calcular_utilidad_accion(estado, accion)
                    if utilidad_accion > max_utilidad:  # Si encontramos mejor utilidad
                        max_utilidad = utilidad_accion  # Actualiza la máxima utilidad
                
                # Asigna la nueva utilidad (mantiene la actual si no hay acciones válidas)
                nuevas_utilidades[estado] = max_utilidad if max_utilidad != -np.inf else self.utilidad[estado]
            
            self.utilidad = dict(nuevas_utilidades)  # Actualiza las utilidades del agente

# Ejemplo: Decisión de inversión
if __name__ == "__main__":            # Bloque principal de ejecución
    # Definición del problema
    estados = ['bajo', 'medio', 'alto']  # Estados posibles del sistema
    acciones = ['conservador', 'moderado', 'agresivo']  # Acciones disponibles
    
    # Función de utilidad inicial
    funcion_utilidad = {
        'bajo': 2,      # Utilidad para estado bajo
        'medio': 5,     # Utilidad para estado medio
        'alto': 10      # Utilidad para estado alto
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
    print("Utilidades iniciales:", agente.utilidad)  # Muestra utilidades iniciales
    agente.actualizar_utilidades(iteraciones=50)    # Ejecuta 50 iteraciones de actualización
    print("Utilidades óptimas calculadas:", agente.utilidad)  # Muestra utilidades optimizadas
    
    # Tomar decisiones en diferentes estados
    for estado in estados:           # Itera sobre todos los estados
        decision = agente.tomar_decision(estado)  # Obtiene la mejor decisión
        print(f"En estado '{estado}', la mejor acción es '{decision}'")  # Muestra resultado