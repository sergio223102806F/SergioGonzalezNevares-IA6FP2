# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 16:26:20 2025

@author: elvin
"""
"""
Implementación de un sistema de Lógica por Defecto (Default Logic)

Características:
- Soporte para reglas por defecto con justificaciones
- Mecanismo de extensión para calcular conclusiones creíbles
- Base de conocimiento con hechos y reglas por defecto
"""

from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict

# =============================================================================
# 1. DEFINICIÓN DE LA BASE DE CONOCIMIENTO
# =============================================================================

class DefaultLogic:
    """
    Sistema de Lógica por Defecto que permite:
    - Añadir reglas por defecto (default rules)
    - Calcular extensiones (conjuntos de creencias consistentes)
    - Realizar inferencias basadas en las extensiones
    """
    
    def __init__(self):
        # Hechos básicos (ground facts)
        self.facts: Set[str] = set()
        
        # Reglas por defecto: (premisas, justificación, conclusión)
        self.default_rules: List[Tuple[List[str], List[str], str]] = []
        
        # Conjunto de todas las proposiciones en el sistema
        self.propositions: Set[str] = set()
    
    def add_fact(self, fact: str):
        """Añade un hecho a la base de conocimiento"""
        self.facts.add(fact)
        self.propositions.add(fact)
    
    def add_default_rule(self, prerequisites: List[str], justifications: List[str], conclusion: str):
        """
        Añade una regla por defecto al sistema.
        
        Formato: prerequisitos : justificaciones / conclusión
        
        Args:
            prerequisites: Hechos que deben ser ciertos para aplicar la regla
            justifications: Hechos que no deben ser refutados
            conclusion: Conclusión de la regla
        """
        self.default_rules.append((prerequisites, justifications, conclusion))
        self.propositions.add(conclusion)
        for p in prerequisites + justifications:
            self.propositions.add(p)
    
    def compute_extensions(self) -> List[Set[str]]:
        """
        Calcula todas las extensiones del sistema de lógica por defecto.
        
        Returns:
            Lista de extensiones (conjuntos de conclusiones consistentes)
        """
        # Algoritmo simplificado para encontrar extensiones
        extensions = []
        self._compute_extension(set(self.facts), [], extensions)
        return extensions
    
    def _compute_extension(self, current_extension: Set[str], 
                          applied_rules: List[int], 
                          all_extensions: List[Set[str]]):
        """
        Función auxiliar recursiva para calcular extensiones.
        
        Args:
            current_extension: Conjunto actual de conclusiones
            applied_rules: Índices de reglas ya aplicadas
            all_extensions: Lista para acumular extensiones encontradas
        """
        # Encontrar reglas aplicables no usadas aún
        new_rules = []
        for i, (pre, just, concl) in enumerate(self.default_rules):
            if i not in applied_rules:
                # Verificar prerequisitos
                pre_ok = all(p in current_extension for p in pre)
                # Verificar que justificaciones no sean refutadas
                just_ok = all(not (j in current_extension) for j in just)
                
                if pre_ok and just_ok:
                    new_rules.append((i, concl))
        
        # Caso base: no hay más reglas aplicables
        if not new_rules:
            if current_extension not in all_extensions:
                all_extensions.append(current_extension.copy())
            return
        
        # Procesar cada regla aplicable
        for rule_idx, conclusion in new_rules:
            new_extension = current_extension.copy()
            new_extension.add(conclusion)
            new_applied = applied_rules.copy()
            new_applied.append(rule_idx)
            self._compute_extension(new_extension, new_applied, all_extensions)
    
    def query(self, proposition: str) -> str:
        """
        Realiza una consulta sobre una proposición.
        
        Args:
            proposition: Proposición a consultar
            
        Returns:
            "True" si está en todas las extensiones,
            "False" si no está en ninguna,
            "Unknown" si está en algunas pero no en otras
        """
        extensions = self.compute_extensions()
        if not extensions:
            return "False"
        
        results = [prop in ext for ext in extensions]
        if all(results):
            return "True"
        elif not any(results):
            return "False"
        else:
            return "Unknown"

# =============================================================================
# 2. EJEMPLOS DE USO
# =============================================================================

def ejemplo_pajaros():
    """Ejemplo clásico: Los pájaros vuelan por defecto"""
    dl = DefaultLogic()
    
    # Hechos
    dl.add_fact("pajaro(tweety)")
    dl.add_fact("pajaro(opus)")
    dl.add_fact("pinguino(opus)")
    
    # Regla por defecto: los pájaros vuelan a menos que sean pingüinos
    dl.add_default_rule(
        prerequisites=["pajaro(X)"],
        justifications=["pinguino(X)"],
        conclusion="vuela(X)"
    )
    
    # Calcular extensiones
    extensions = dl.compute_extensions()
    
    print("\nExtensiones encontradas:")
    for i, ext in enumerate(extensions, 1):
        print(f"Extensión {i}: {ext}")
    
    # Consultas
    print("\n¿Vuela tweety?")
    print(dl.query("vuela(tweety)"))  # True (pájaro normal)
    
    print("\n¿Vuela opus?")
    print(dl.query("vuela(opus)"))    # False (es pingüino)

def ejemplo_legal():
    """Ejemplo de sistema legal con presunciones"""
    dl = DefaultLogic()
    
    # Hechos
    dl.add_fact("persona(juan)")
    dl.add_fact("persona(maria)")
    dl.add_fact("evidencia_contra(maria)")
    
    # Regla por defecto: las personas son inocentes a menos que haya evidencia
    dl.add_default_rule(
        prerequisites=["persona(X)"],
        justifications=["evidencia_contra(X)"],
        conclusion="inocente(X)"
    )
    
    # Otra regla: quienes tienen evidencia son culpables
    dl.add_default_rule(
        prerequisites=["evidencia_contra(X)"],
        justifications=[],
        conclusion="culpable(X)"
    )
    
    extensions = dl.compute_extensions()
    print("\nExtensiones encontradas:")
    for i, ext in enumerate(extensions, 1):
        print(f"Extensión {i}: {ext}")
    
    # Consultas
    print("\n¿Es juan inocente?")
    print(dl.query("inocente(juan)"))  # True
    
    print("\n¿Es maria inocente?")
    print(dl.query("inocente(maria)")) # False
    
    print("\n¿Es maria culpable?")
    print(dl.query("culpable(maria)")) # True

if __name__ == "__main__":
    print("=== DEMOSTRACIÓN DE LÓGICA POR DEFECTO ===")
    ejemplo_pajaros()
    ejemplo_legal()