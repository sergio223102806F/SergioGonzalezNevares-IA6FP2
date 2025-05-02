# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 14:39:07 2025

@author: elvin
"""

"""
Este código implementa ambos tipos de encadenamiento lógico:
1. Encadenamiento hacia adelante (forward chaining)
2. Encadenamiento hacia atrás (backward chaining)
"""

from typing import Dict, List, Set, Tuple, Optional
from collections import deque

# Definición de tipos
Rule = Tuple[List[str], str]  # (premisas, conclusión)
KnowledgeBase = Dict[str, List[Rule]]  # Mapa de conclusiones a reglas

class InferenceEngine:
    """
    Motor de inferencia que soporta ambos tipos de encadenamiento.
    """
    
    def __init__(self):
        self.kb: KnowledgeBase = defaultdict(list)  # Base de conocimiento
        self.facts: Set[str] = set()               # Hechos conocidos
        self.agenda: deque = deque()               # Agenda para encadenamiento hacia adelante
        
    def add_rule(self, premises: List[str], conclusion: str):
        """
        Añade una regla a la base de conocimiento.
        
        Args:
            premises: Lista de premisas
            conclusion: Conclusión de la regla
        """
        rule = (premises, conclusion)
        self.kb[conclusion].append(rule)
        
    def add_fact(self, fact: str):
        """
        Añade un hecho a la base de conocimiento y lo pone en la agenda.
        
        Args:
            fact: Hecho a añadir
        """
        if fact not in self.facts:
            self.facts.add(fact)
            self.agenda.append(fact)
    
    def forward_chain(self) -> Set[str]:
        """
        Encadenamiento hacia adelante: parte de los hechos conocidos y aplica
        reglas hasta que no se pueden derivar nuevos hechos.
        
        Returns:
            Conjunto de todos los hechos derivados
        """
        derived_facts = set()
        
        while self.agenda:
            fact = self.agenda.popleft()
            
            # Para cada regla que tenga esta fact como premisa
            for conclusion, rules in self.kb.items():
                for rule in rules:
                    premises, rule_conclusion = rule
                    
                    if fact in premises:
                        # Verificar si todas las premisas se cumplen
                        if all(p in self.facts for p in premises):
                            # Añadir conclusión si es nueva
                            if rule_conclusion not in self.facts:
                                self.add_fact(rule_conclusion)
                                derived_facts.add(rule_conclusion)
        
        return derived_facts
    
    def backward_chain(self, goal: str, visited: Optional[Set[str]] = None) -> bool:
        """
        Encadenamiento hacia atrás: intenta demostrar un objetivo buscando
        reglas que lo concluyan y demostrando sus premisas recursivamente.
        
        Args:
            goal: Objetivo a demostrar
            visited: Conjunto de objetivos ya visitados (para evitar ciclos)
            
        Returns:
            True si el objetivo puede ser demostrado, False en caso contrario
        """
        if visited is None:
            visited = set()
            
        # Si el objetivo ya es un hecho conocido
        if goal in self.facts:
            return True
            
        # Si ya hemos visitado este objetivo (evitar ciclos)
        if goal in visited:
            return False
            
        visited.add(goal)
        
        # Buscar reglas que concluyan este objetivo
        for rule in self.kb.get(goal, []):
            premises, _ = rule
            
            # Intentar demostrar todas las premisas
            if all(self.backward_chain(p, visited) for p in premises):
                self.add_fact(goal)  # Añadir como hecho conocido
                return True
                
        return False
    
    def explain(self, fact: str, depth: int = 0) -> Optional[str]:
        """
        Genera una explicación de cómo se derivó un hecho.
        
        Args:
            fact: Hecho a explicar
            depth: Profundidad actual (para indentación)
            
        Returns:
            Cadena con la explicación o None si el hecho no se conoce
        """
        if fact not in self.facts:
            return None
            
        explanation = []
        indent = "  " * depth
        
        # Buscar reglas que hayan concluido este hecho
        rules_used = []
        for rule in self.kb.get(fact, []):
            premises, _ = rule
            if all(p in self.facts for p in premises):
                rules_used.append(rule)
        
        if rules_used:
            # Tomar la primera regla que se usó
            premises, _ = rules_used[0]
            explanation.append(f"{indent}{fact} se deriva de:")
            
            for p in premises:
                premise_explanation = self.explain(p, depth + 1)
                if premise_explanation:
                    explanation.append(premise_explanation)
                else:
                    explanation.append(f"{indent}  {p} (hecho conocido)")
        else:
            explanation.append(f"{indent}{fact} (hecho conocido)")
        
        return "\n".join(explanation)

def medical_example():
    """
    Ejemplo médico que muestra ambos tipos de encadenamiento.
    """
    engine = InferenceEngine()
    
    # Añadir reglas
    engine.add_rule(["fiebre", "tos"], "gripe")
    engine.add_rule(["fiebre", "erupcion"], "dengue")
    engine.add_rule(["gripe", "dolor_muscular"], "gripe_grave")
    engine.add_rule(["dengue", "dolor_articular"], "dengue_grave")
    engine.add_rule(["gripe_grave"], "hospitalizar")
    engine.add_rule(["dengue_grave"], "hospitalizar")
    
    # Encadenamiento hacia adelante
    print("=== Encadenamiento hacia adelante ===")
    engine.add_fact("fiebre")
    engine.add_fact("tos")
    engine.add_fact("dolor_muscular")
    
    derived = engine.forward_chain()
    print("\nHechos derivados:")
    for fact in derived:
        print(f"- {fact}")
    
    print("\nExplicación para 'hospitalizar':")
    print(engine.explain("hospitalizar") or "No se puede explicar")
    
    # Encadenamiento hacia atrás
    print("\n=== Encadenamiento hacia atrás ===")
    engine2 = InferenceEngine()
    
    # Añadir las mismas reglas
    engine2.add_rule(["fiebre", "tos"], "gripe")
    engine2.add_rule(["fiebre", "erupcion"], "dengue")
    engine2.add_rule(["gripe", "dolor_muscular"], "gripe_grave")
    engine2.add_rule(["dengue", "dolor_articular"], "dengue_grave")
    engine2.add_rule(["gripe_grave"], "hospitalizar")
    engine2.add_rule(["dengue_grave"], "hospitalizar")
    
    # Añadir hechos básicos
    engine2.add_fact("fiebre")
    engine2.add_fact("erupcion")
    engine2.add_fact("dolor_articular")
    
    # Demostrar un objetivo
    goal = "hospitalizar"
    result = engine2.backward_chain(goal)
    
    print(f"\n¿Se puede demostrar '{goal}'? {result}")
    print("\nExplicación:")
    print(engine2.explain(goal) or "No se puede explicar")

if __name__ == "__main__":
    print("=== Sistemas de Encadenamiento Hacia Adelante y Atrás ===")
    medical_example()