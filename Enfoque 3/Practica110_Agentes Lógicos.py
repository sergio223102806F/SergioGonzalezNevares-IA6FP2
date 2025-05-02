# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 16:26:19 2025

@author: elvin
"""

"""
Este código implementa un agente lógico que utiliza una base de conocimiento 
y razonamiento lógico para tomar decisiones. El agente puede:
1. Percibir su entorno
2. Actualizar su base de conocimiento
3. Realizar inferencias lógicas
4. Seleccionar acciones apropiadas
"""

from typing import Dict, List, Set, Optional, Union
from collections import defaultdict

# ==============================================
# Definición de la Base de Conocimiento
# ==============================================

class KnowledgeBase:
    """Base de conocimiento para el agente lógico"""
    
    def __init__(self):
        self.facts: Set[str] = set()  # Hechos conocidos
        self.rules: Dict[str, List[List[str]]] = defaultdict(list)  # Reglas de inferencia
        
    def add_fact(self, fact: str):
        """Añade un hecho a la base de conocimiento"""
        self.facts.add(fact)
        
    def add_rule(self, conclusion: str, premises: List[str]):
        """Añade una regla (premisas => conclusión)"""
        self.rules[conclusion].append(premises)
        
    def infer(self, query: str) -> bool:
        """
        Realiza inferencia hacia adelante para determinar si un hecho se sigue de la KB
        
        Args:
            query: Hecho a verificar
            
        Returns:
            True si el hecho puede ser inferido, False en caso contrario
        """
        # Si el hecho ya está en la KB
        if query in self.facts:
            return True
            
        # Verificar reglas que puedan inferir el hecho
        for premises in self.rules.get(query, []):
            if all(self.infer(p) for p in premises):
                self.add_fact(query)  # Añadir nuevo hecho inferido
                return True
                
        return False

# ==============================================
# Definición del Agente Lógico
# ==============================================

class LogicalAgent:
    """Agente que utiliza razonamiento lógico para actuar"""
    
    def __init__(self):
        self.kb = KnowledgeBase()  # Base de conocimiento
        self.actions = {}          # Acciones disponibles
        self.initialize_knowledge()  # Inicializar conocimiento básico
        
    def initialize_knowledge(self):
        """Inicializa el conocimiento básico del agente"""
        # Ejemplo de reglas para un mundo de wumpus simple
        self.kb.add_rule("hedor", ["cerca_wumpus"])
        self.kb.add_rule("brillo", ["cerca_oro"])
        self.kb.add_rule("peligro", ["hedor"])
        self.kb.add_rule("seguro", ["no_hedor"])
        
        # Acciones posibles
        self.actions = {
            "avanzar": self.avanzar,
            "girar_izquierda": self.girar_izquierda,
            "girar_derecha": self.girar_derecha,
            "agarrar": self.agarrar,
            "salir": self.salir
        }
        
    def perceive(self, perception: Dict[str, bool]):
        """
        Procesa las percepciones del entorno y actualiza la KB
        
        Args:
            perception: Diccionario de percepciones (ej. {"hedor": True, "brillo": False})
        """
        for p, value in perception.items():
            if value:
                self.kb.add_fact(p)
            else:
                self.kb.add_fact(f"no_{p}")
                
    def choose_action(self) -> str:
        """
        Selecciona una acción basada en el conocimiento actual
        
        Returns:
            Nombre de la acción seleccionada
        """
        # Prioridad 1: Agarrar oro si está cerca
        if self.kb.infer("brillo"):
            return "agarrar"
            
        # Prioridad 2: Evitar peligro
        if self.kb.infer("peligro"):
            return "girar_derecha"  # Cambiar dirección para evitar
            
        # Prioridad 3: Moverse a lugares seguros
        if self.kb.infer("seguro"):
            return "avanzar"
            
        # Default: Explorar
        return "girar_izquierda"
        
    def execute_action(self, action: str):
        """
        Ejecuta una acción y actualiza el conocimiento
        
        Args:
            action: Nombre de la acción a ejecutar
        """
        if action in self.actions:
            self.actions[action]()
        else:
            print(f"Acción desconocida: {action}")
            
    # Métodos de acciones
    def avanzar(self):
        """Acción de avanzar en la dirección actual"""
        print("El agente avanza hacia adelante")
        # Actualizar KB con posibles consecuencias
        self.kb.add_fact("movimiento_realizado")
        
    def girar_izquierda(self):
        """Acción de girar a la izquierda"""
        print("El agente gira 90 grados a la izquierda")
        
    def girar_derecha(self):
        """Acción de girar a la derecha"""
        print("El agente gira 90 grados a la derecha")
        
    def agarrar(self):
        """Acción de agarrar un objeto"""
        print("El agente intenta agarrar un objeto")
        self.kb.add_fact("objeto_agarrado")
        
    def salir(self):
        """Acción de salir del entorno"""
        print("El agente sale del entorno")

# ==============================================
# Ejemplo de Simulación
# ==============================================

def simulate_agent():
    """Simula el funcionamiento del agente en un entorno"""
    agent = LogicalAgent()
    
    # Ciclo de percepción-acción
    for step in range(5):
        print(f"\n--- Paso {step + 1} ---")
        
        # Percepciones del entorno (ejemplo)
        if step == 0:
            perception = {"hedor": True, "brillo": False}
        elif step == 2:
            perception = {"brillo": True, "hedor": False}
        else:
            perception = {"hedor": False, "brillo": False}
            
        print(f"Percepciones: {perception}")
        agent.perceive(perception)
        
        # Seleccionar y ejecutar acción
        action = agent.choose_action()
        print(f"Acción seleccionada: {action}")
        agent.execute_action(action)
        
        # Condición de terminación
        if action == "salir":
            break

if __name__ == "__main__":
    print("=== Simulación de Agente Lógico ===")
    simulate_agent()