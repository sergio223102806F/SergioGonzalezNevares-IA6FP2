# -*- coding: utf-8 -*-                                                     # Define la codificación de caracteres del archivo como UTF-8
"""
Created on Sun Apr 27 16:26:20 2025                                         # Indica la fecha y hora de creación del archivo
                                                                           #
@author: elvin                                                              # Define el autor del archivo
"""

"""
Implementación de un sistema de Lógica No Monotónica con mecanismos de
razonamiento por defecto y revisión de creencias.

Características:
- Soporte para reglas con excepciones
- Mecanismo de revisión de creencias
- Base de conocimiento que puede no ser consistente
"""

from typing import List, Dict, Set, Optional, Union                       # Importa tipos para anotaciones de tipo
from collections import defaultdict                                      # Importa defaultdict desde el módulo collections

# ============================================================================= # Separador de sección
# 1. DEFINICIÓN DE LA BASE DE CONOCIMIENTO NO MONOTÓNICA                     # Título de la sección
# ============================================================================= # Separador de sección

class NonMonotonicKnowledgeBase:                                         # Define una clase llamada NonMonotonicKnowledgeBase
    """
    Base de conocimiento que permite:                                  # Documentación de la clase
    - Añadir reglas con excepciones
    - Realizar inferencias que pueden ser revisadas
    - Manejar información inconsistente
    """
    
    def __init__(self):                                                     # Define el constructor de la clase
        # Reglas de la forma: conclusión :- premisas, excepto excepciones    # Comentario de la estructura de las reglas
        self.rules: List[Dict] = []                                       # Inicializa una lista para almacenar las reglas
        
        # Hechos conocidos (pueden cambiar)                                # Comentario de los hechos conocidos
        self.facts: Set[str] = set()                                       # Inicializa un conjunto para almacenar los hechos
        
        # Excepciones registradas                                          # Comentario de las excepciones registradas
        self.exceptions: Dict[str, Set[str]] = defaultdict(set)           # Inicializa un diccionario con conjuntos vacíos como valor predeterminado para las excepciones
    
    def add_rule(self, conclusion: str, premises: List[str], exceptions: List[str] = None): # Define el método para añadir una regla
        """
        Añade una regla no monotónica al sistema.                        # Documentación del método add_rule
        
        Args:
            conclusion: Conclusión de la regla
            premises: Lista de premisas requeridas
            exceptions: Lista de excepciones que invalidan la regla
        """
        if exceptions is None:                                           # Si no se proporcionan excepciones
            exceptions = []                                              # Inicializa una lista vacía de excepciones
            
        self.rules.append({                                              # Añade la regla como un diccionario a la lista de reglas
            'conclusion': conclusion,
            'premises': premises,
            'exceptions': exceptions
        })
        
        # Registrar excepciones para búsqueda rápida                      # Comentario para registrar las excepciones
        for exc in exceptions:                                           # Itera sobre las excepciones de la regla
            self.exceptions[exc].add(conclusion)                         # Añade la conclusión a la lista de conclusiones que la excepción invalida
    
    def add_fact(self, fact: str):                                         # Define el método para añadir un hecho
        """Añade un hecho a la base de conocimiento"""                     # Documentación del método add_fact
        self.facts.add(fact)                                               # Añade el hecho al conjunto de hechos
    
    def retract_fact(self, fact: str):                                    # Define el método para retractar un hecho
        """Retira un hecho de la base de conocimiento"""                    # Documentación del método retract_fact
        self.facts.discard(fact)                                           # Elimina el hecho del conjunto de hechos
    
    def is_exception(self, fact: str) -> bool:                             # Define el método para verificar si un hecho es una excepción
        """Verifica si un hecho invalida alguna conclusión"""                # Documentación del método is_exception
        return fact in self.exceptions                                    # Retorna True si el hecho está registrado como una excepción
    
    def infer(self, query: str, max_depth: int = 10) -> Optional[bool]:   # Define el método para realizar inferencias
        """
        Realiza inferencia no monotónica sobre una consulta.             # Documentación del método infer
        
        Args:
            query: Hecho a inferir
            max_depth: Límite de profundidad para evitar recursión infinita
            
        Returns:
            True si se puede concluir, False si no, None si es ambiguo
        """
        # Caso base: hecho directo                                         # Comentario del caso base
        if query in self.facts:                                           # Si la consulta es un hecho conocido
            return True                                                   # Retorna True
            
        # Verificar si hay excepciones explícitas                         # Comentario para verificar excepciones explícitas
        if self.is_exception(query):                                      # Si la consulta es una excepción
            return False                                                  # Retorna False
            
        # Buscar reglas que puedan inferir la consulta                   # Comentario para buscar reglas relevantes
        conclusions = []                                                 # Inicializa una lista para almacenar los posibles resultados
        for rule in self.rules:                                           # Itera sobre las reglas
            if rule['conclusion'] == query:                              # Si la conclusión de la regla coincide con la consulta
                # Verificar si todas las premisas se cumplen              # Comentario para verificar las premisas
                premises_ok = all(self.infer(p, max_depth-1) for p in rule['premises']) # Verifica recursivamente si todas las premisas son verdaderas
                
                # Verificar si hay excepciones aplicables                 # Comentario para verificar las excepciones
                exceptions_ok = not any(self.infer(e, max_depth-1) for e in rule['exceptions']) # Verifica recursivamente si alguna excepción es verdadera
                
                if premises_ok and exceptions_ok:                        # Si las premisas son verdaderas y no hay excepciones verdaderas
                    conclusions.append(True)                             # Añade True a la lista de resultados
                else:                                                      # En caso contrario
                    conclusions.append(False)                            # Añade False a la lista de resultados
        
        # Determinar el resultado                                         # Comentario para determinar el resultado final
        if not conclusions:                                               # Si no hay reglas aplicables
            return None                                                   # Retorna None (ambiguo)
        elif all(c == False for c in conclusions):                       # Si todas las conclusiones son False
            return False                                                  # Retorna False
        elif any(c == True for c in conclusions):                        # Si alguna conclusión es True
            return True                                                   # Retorna True
        else:                                                          # En otros casos (mezcla de True y False)
            return None                                                   # Retorna None (ambiguo)

# ============================================================================= # Separador de sección
# 2. EJEMPLOS DE USO                                                      # Título de la sección
# ============================================================================= # Separador de sección

def ejemplo_pajaros():                                                    # Define la función para el ejemplo de los pájaros
    """Ejemplo clásico: Los pájaros vuelan por defecto"""                 # Documentación de la función ejemplo_pajaros
    kb = NonMonotonicKnowledgeBase()                                    # Crea una instancia de la clase NonMonotonicKnowledgeBase
    
    # Regla por defecto: los pájaros vuelan                             # Comentario de la regla por defecto
    kb.add_rule("vuela(X)", ["pajaro(X)"], ["pinguino(X)"])             # Añade la regla: si X es un pájaro, entonces X vuela, excepto si X es un pingüino
    
    # Hechos específicos                                               # Comentario de los hechos específicos
    kb.add_fact("pajaro(tweety)")                                       # Añade el hecho: tweety es un pájaro
    kb.add_fact("pajaro(opus)")                                         # Añade el hecho: opus es un pájaro
    kb.add_fact("pinguino(opus)")                                       # Añade el hecho: opus es un pingüino
    
    # Consultas                                                        # Comentario de las consultas
    print("\n¿Puede volar tweety?")                                     # Imprime la consulta
    print(kb.infer("vuela(tweety)"))                                    # Realiza la inferencia y la imprime (True)
    
    print("\n¿Puede volar opus?")                                       # Imprime la consulta
    print(kb.infer("vuela(opus)"))                                      # Realiza la inferencia y la imprime (False)
    
    # Añadir nueva excepción                                            # Comentario de la nueva excepción
    print("\nAñadiendo que tweety está herido...")                     # Imprime la acción
    kb.add_rule("no_vuela(X)", ["herido(X)"])                           # Añade la regla: si X está herido, entonces X no vuela
    kb.add_fact("herido(tweety)")                                       # Añade el hecho: tweety está herido
    
    # Modificar regla original para considerar nuevas excepciones       # Comentario de la modificación de la regla original
    kb.add_rule("vuela(X)", ["pajaro(X)"], ["pinguino(X)", "no_vuela(X)"]) # Reemplaza la regla original añadiendo la nueva excepción
    
    print("\n¿Puede volar tweety ahora?")                               # Imprime la consulta
    print(kb.infer("vuela(tweety)"))                                    # Realiza la inferencia y la imprime (False)

def ejemplo_legal():                                                     # Define la función para el ejemplo legal
    """Ejemplo de sistema legal con presunciones"""                      # Documentación de la función ejemplo_legal
    kb = NonMonotonicKnowledgeBase()                                    # Crea una instancia de la clase NonMonotonicKnowledgeBase
    
    # Regla por defecto: las personas son inocentes                     # Comentario de la regla por defecto legal
    kb.add_rule("inocente(X)", ["persona(X)"], ["evidencia_contra(X)"]) # Añade la regla: si X es una persona, entonces X es inocente, excepto si hay evidencia contra X
    
    # Hechos                                                           # Comentario de los hechos legales
    kb.add_fact("persona(juan)")                                        # Añade el hecho: juan es una persona
    kb.add_fact("persona(maria)")                                       # Añade el hecho: maria es una persona
    kb.add_fact("evidencia_contra(maria)")                              # Añade el hecho: hay evidencia contra maria
    
    # Consultas                                                        # Comentario de las consultas legales
    print("\n¿Es juan inocente?")                                       # Imprime la consulta
    print(kb.infer("inocente(juan)"))                                   # Realiza la inferencia y la imprime (True)
    
    print("\n¿Es maria inocente?")                                      # Imprime la consulta
    print(kb.infer("inocente(maria)"))                                  # Realiza la inferencia y la imprime (False)
    
    # Nueva evidencia puede cambiar la conclusión                      # Comentario de la nueva evidencia
    print("\nRetirando evidencia contra maria...")                     # Imprime la acción
    kb.retract_fact("evidencia_contra(maria)")                          # Retracta el hecho: hay evidencia contra maria
    print("¿Es maria inocente ahora?")                                  # Imprime la consulta
    print(kb.infer("inocente(maria)"))                                  # Realiza la inferencia y la imprime (True)

if __name__ == "__main__":                                                 # Bloque de código que se ejecuta cuando el script se llama directamente
    print("=== DEMOSTRACIÓN DE LÓGICA NO MONOTÓNICA ===")                 # Imprime un encabezado para la demostración
    ejemplo_pajaros()                                                      # Llama a la función ejemplo_pajaros
    ejemplo_legal()                                                        # Llama a la función ejemplo_legal