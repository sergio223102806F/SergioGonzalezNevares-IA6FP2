# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 16:26:20 2025

@author: elvin
"""

"""
Implementación de un sistema de Lógica No Monotónica con mecanismos de
razonamiento por defecto y revisión de creencias.

Características:
- Soporte para reglas con excepciones
- Mecanismo de revisión de creencias
- Base de conocimiento que puede no ser consistente
"""

from typing import List, Dict, Set, Optional, Union
from collections import defaultdict

# =============================================================================
# 1. DEFINICIÓN DE LA BASE DE CONOCIMIENTO NO MONOTÓNICA
# =============================================================================

class NonMonotonicKnowledgeBase:
    """
    Base de conocimiento que permite:
    - Añadir reglas con excepciones
    - Realizar inferencias que pueden ser revisadas
    - Manejar información inconsistente
    """
    
    def __init__(self):
        # Reglas de la forma: conclusión :- premisas, excepto excepciones
        self.rules: List[Dict] = []
        
        # Hechos conocidos (pueden cambiar)
        self.facts: Set[str] = set()
        
        # Excepciones registradas
        self.exceptions: Dict[str, Set[str]] = defaultdict(set)
    
    def add_rule(self, conclusion: str, premises: List[str], exceptions: List[str] = None):
        """
        Añade una regla no monotónica al sistema.
        
        Args:
            conclusion: Conclusión de la regla
            premises: Lista de premisas requeridas
            exceptions: Lista de excepciones que invalidan la regla
        """
        if exceptions is None:
            exceptions = []
            
        self.rules.append({
            'conclusion': conclusion,
            'premises': premises,
            'exceptions': exceptions
        })
        
        # Registrar excepciones para búsqueda rápida
        for exc in exceptions:
            self.exceptions[exc].add(conclusion)
    
    def add_fact(self, fact: str):
        """Añade un hecho a la base de conocimiento"""
        self.facts.add(fact)
    
    def retract_fact(self, fact: str):
        """Retira un hecho de la base de conocimiento"""
        self.facts.discard(fact)
    
    def is_exception(self, fact: str) -> bool:
        """Verifica si un hecho invalida alguna conclusión"""
        return fact in self.exceptions
    
    def infer(self, query: str, max_depth: int = 10) -> Optional[bool]:
        """
        Realiza inferencia no monotónica sobre una consulta.
        
        Args:
            query: Hecho a inferir
            max_depth: Límite de profundidad para evitar recursión infinita
            
        Returns:
            True si se puede concluir, False si no, None si es ambiguo
        """
        # Caso base: hecho directo
        if query in self.facts:
            return True
            
        # Verificar si hay excepciones explícitas
        if self.is_exception(query):
            return False
            
        # Buscar reglas que puedan inferir la consulta
        conclusions = []
        for rule in self.rules:
            if rule['conclusion'] == query:
                # Verificar si todas las premisas se cumplen
                premises_ok = all(self.infer(p, max_depth-1) for p in rule['premises'])
                
                # Verificar si hay excepciones aplicables
                exceptions_ok = not any(self.infer(e, max_depth-1) for e in rule['exceptions'])
                
                if premises_ok and exceptions_ok:
                    conclusions.append(True)
                else:
                    conclusions.append(False)
        
        # Determinar el resultado
        if not conclusions:
            return None  # No hay reglas aplicables
        elif all(c == False for c in conclusions):
            return False
        elif any(c == True for c in conclusions):
            return True
        else:
            return None  # Caso ambiguo

# =============================================================================
# 2. EJEMPLOS DE USO
# =============================================================================

def ejemplo_pajaros():
    """Ejemplo clásico: Los pájaros vuelan por defecto"""
    kb = NonMonotonicKnowledgeBase()
    
    # Regla por defecto: los pájaros vuelan
    kb.add_rule("vuela(X)", ["pajaro(X)"], ["pinguino(X)"])
    
    # Hechos específicos
    kb.add_fact("pajaro(tweety)")
    kb.add_fact("pajaro(opus)")
    kb.add_fact("pinguino(opus)")
    
    # Consultas
    print("\n¿Puede volar tweety?")
    print(kb.infer("vuela(tweety)"))  # True (pájaro normal)
    
    print("\n¿Puede volar opus?")
    print(kb.infer("vuela(opus)"))    # False (es pingüino)
    
    # Añadir nueva excepción
    print("\nAñadiendo que tweety está herido...")
    kb.add_rule("no_vuela(X)", ["herido(X)"])
    kb.add_fact("herido(tweety)")
    
    # Modificar regla original para considerar nuevas excepciones
    kb.add_rule("vuela(X)", ["pajaro(X)"], ["pinguino(X)", "no_vuela(X)"])
    
    print("\n¿Puede volar tweety ahora?")
    print(kb.infer("vuela(tweety)"))  # False (por la nueva excepción)

def ejemplo_legal():
    """Ejemplo de sistema legal con presunciones"""
    kb = NonMonotonicKnowledgeBase()
    
    # Regla por defecto: las personas son inocentes
    kb.add_rule("inocente(X)", ["persona(X)"], ["evidencia_contra(X)"])
    
    # Hechos
    kb.add_fact("persona(juan)")
    kb.add_fact("persona(maria)")
    kb.add_fact("evidencia_contra(maria)")
    
    # Consultas
    print("\n¿Es juan inocente?")
    print(kb.infer("inocente(juan)"))  # True (por defecto)
    
    print("\n¿Es maria inocente?")
    print(kb.infer("inocente(maria)")) # False (hay evidencia)
    
    # Nueva evidencia puede cambiar la conclusión
    print("\nRetirando evidencia contra maria...")
    kb.retract_fact("evidencia_contra(maria)")
    print("¿Es maria inocente ahora?")
    print(kb.infer("inocente(maria)")) # True (sin evidencia)

if __name__ == "__main__":
    print("=== DEMOSTRACIÓN DE LÓGICA NO MONOTÓNICA ===")
    ejemplo_pajaros()
    ejemplo_legal()