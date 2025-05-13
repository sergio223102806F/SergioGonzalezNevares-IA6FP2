# -*- coding: utf-8 -*-                                                     # Define la codificación de caracteres del archivo como UTF-8
"""
Created on Sun Apr 27 16:26:20 2025                                         # Indica la fecha y hora de creación del archivo
                                                                           #
@author: elvin                                                              # Define el autor del archivo
"""
"""
Implementación de un sistema de Lógica por Defecto (Default Logic)

Características:
- Soporte para reglas por defecto con justificaciones
- Mecanismo de extensión para calcular conclusiones creíbles
- Base de conocimiento con hechos y reglas por defecto
"""

from typing import List, Dict, Set, Tuple, Optional                       # Importa tipos para anotaciones de tipo
from collections import defaultdict                                      # Importa defaultdict desde el módulo collections

# ============================================================================= # Separador de sección
# 1. DEFINICIÓN DE LA BASE DE CONOCIMIENTO                                        # Título de la sección
# ============================================================================= # Separador de sección

class DefaultLogic:                                                      # Define una clase llamada DefaultLogic
    """
    Sistema de Lógica por Defecto que permite:                           # Documentación de la clase DefaultLogic
    - Añadir reglas por defecto (default rules)
    - Calcular extensiones (conjuntos de creencias consistentes)
    - Realizar inferencias basadas en las extensiones
    """
    
    def __init__(self):                                                     # Define el constructor de la clase
        # Hechos básicos (ground facts)                                   # Comentario para los hechos básicos
        self.facts: Set[str] = set()                                       # Inicializa un conjunto para almacenar los hechos
        
        # Reglas por defecto: (premisas, justificación, conclusión)        # Comentario para las reglas por defecto
        self.default_rules: List[Tuple[List[str], List[str], str]] = []    # Inicializa una lista para almacenar las reglas por defecto
        
        # Conjunto de todas las proposiciones en el sistema                 # Comentario para todas las proposiciones
        self.propositions: Set[str] = set()                                # Inicializa un conjunto para almacenar todas las proposiciones
    
    def add_fact(self, fact: str):                                         # Define el método para añadir un hecho
        """Añade un hecho a la base de conocimiento"""                     # Documentación del método add_fact
        self.facts.add(fact)                                               # Añade el hecho al conjunto de hechos
        self.propositions.add(fact)                                        # Añade el hecho al conjunto de proposiciones
    
    def add_default_rule(self, prerequisites: List[str], justifications: List[str], conclusion: str): # Define el método para añadir una regla por defecto
        """
        Añade una regla por defecto al sistema.                            # Documentación del método add_default_rule
        
        Formato: prerequisitos : justificaciones / conclusión             # Comentario para el formato de la regla
        
        Args:
            prerequisites: Hechos que deben ser ciertos para aplicar la regla
            justifications: Hechos que no deben ser refutados
            conclusion: Conclusión de la regla
        """
        self.default_rules.append((prerequisites, justifications, conclusion)) # Añade la regla por defecto como una tupla a la lista
        self.propositions.add(conclusion)                                 # Añade la conclusión al conjunto de proposiciones
        for p in prerequisites + justifications:                           # Itera sobre los prerequisitos y las justificaciones
            self.propositions.add(p)                                     # Añade cada prerequisito y justificación al conjunto de proposiciones
    
    def compute_extensions(self) -> List[Set[str]]:                        # Define el método para calcular las extensiones
        """
        Calcula todas las extensiones del sistema de lógica por defecto. # Documentación del método compute_extensions
        
        Returns:
            Lista de extensiones (conjuntos de conclusiones consistentes)
        """
        # Algoritmo simplificado para encontrar extensiones               # Comentario para el algoritmo de extensiones
        extensions = []                                                  # Inicializa una lista para almacenar las extensiones
        self._compute_extension(set(self.facts), [], extensions)         # Llama a la función auxiliar para calcular las extensiones
        return extensions                                                  # Retorna la lista de extensiones
    
    def _compute_extension(self, current_extension: Set[str],             # Define el método auxiliar recursivo para calcular extensiones
                           applied_rules: List[int],                      # Argumento para las reglas aplicadas
                           all_extensions: List[Set[str]]):              # Argumento para todas las extensiones
        """
        Función auxiliar recursiva para calcular extensiones.             # Documentación del método _compute_extension
        
        Args:
            current_extension: Conjunto actual de conclusiones
            applied_rules: Índices de reglas ya aplicadas
            all_extensions: Lista para acumular extensiones encontradas
        """
        # Encontrar reglas aplicables no usadas aún                       # Comentario para encontrar reglas aplicables
        new_rules = []                                                   # Inicializa una lista para las nuevas reglas aplicables
        for i, (pre, just, concl) in enumerate(self.default_rules):      # Itera sobre las reglas por defecto con su índice
            if i not in applied_rules:                                   # Si la regla no ha sido aplicada aún
                # Verificar prerequisitos                               # Comentario para verificar prerequisitos
                pre_ok = all(p in current_extension for p in pre)       # Verifica si todos los prerequisitos están en la extensión actual
                # Verificar que justificaciones no sean refutadas         # Comentario para verificar justificaciones
                just_ok = all(not (j in current_extension) for j in just) # Verifica si ninguna de las justificaciones está en la extensión actual
                
                if pre_ok and just_ok:                                   # Si los prerequisitos se cumplen y las justificaciones no son refutadas
                    new_rules.append((i, concl))                         # Añade el índice de la regla y la conclusión a la lista de nuevas reglas
        
        # Caso base: no hay más reglas aplicables                        # Comentario para el caso base
        if not new_rules:                                               # Si no hay nuevas reglas aplicables
            if current_extension not in all_extensions:                 # Si la extensión actual no está ya en la lista de todas las extensiones
                all_extensions.append(current_extension.copy())        # Añade una copia de la extensión actual a la lista de todas las extensiones
            return                                                       # Termina la recursión
        
        # Procesar cada regla aplicable                                  # Comentario para procesar cada regla aplicable
        for rule_idx, conclusion in new_rules:                           # Itera sobre las nuevas reglas aplicables
            new_extension = current_extension.copy()                   # Crea una copia de la extensión actual
            new_extension.add(conclusion)                              # Añade la conclusión de la regla a la nueva extensión
            new_applied = applied_rules.copy()                         # Crea una copia de las reglas ya aplicadas
            new_applied.append(rule_idx)                               # Añade el índice de la regla actual a la lista de reglas aplicadas
            self._compute_extension(new_extension, new_applied, all_extensions) # Llama recursivamente a la función con la nueva extensión y las reglas aplicadas
    
    def query(self, proposition: str) -> str:                           # Define el método para realizar una consulta
        """
        Realiza una consulta sobre una proposición.                     # Documentación del método query
        
        Args:
            proposition: Proposición a consultar
            
        Returns:
            "True" si está en todas las extensiones,
            "False" si no está en ninguna,
            "Unknown" si está en algunas pero no en otras
        """
        extensions = self.compute_extensions()                          # Calcula todas las extensiones
        if not extensions:                                              # Si no hay extensiones
            return "False"                                               # Retorna False
        
        results = [prop in ext for ext in extensions]                  # Crea una lista de booleanos indicando si la proposición está en cada extensión
        if all(results):                                                # Si la proposición está en todas las extensiones
            return "True"                                                # Retorna True
        elif not any(results):                                         # Si la proposición no está en ninguna extensión
            return "False"                                               # Retorna False
        else:                                                          # Si la proposición está en algunas pero no en otras
            return "Unknown"                                             # Retorna Unknown

# ============================================================================= # Separador de sección
# 2. EJEMPLOS DE USO                                                      # Título de la sección
# ============================================================================= # Separador de sección

def ejemplo_pajaros():                                                    # Define la función para el ejemplo de los pájaros
    """Ejemplo clásico: Los pájaros vuelan por defecto"""                 # Documentación de la función ejemplo_pajaros
    dl = DefaultLogic()                                                 # Crea una instancia de la clase DefaultLogic
    
    # Hechos                                                           # Comentario para los hechos
    dl.add_fact("pajaro(tweety)")                                       # Añade el hecho "pajaro(tweety)"
    dl.add_fact("pajaro(opus)")                                         # Añade el hecho "pajaro(opus)"
    dl.add_fact("pinguino(opus)")                                       # Añade el hecho "pinguino(opus)"
    
    # Regla por defecto: los pájaros vuelan a menos que sean pingüinos   # Comentario para la regla por defecto
    dl.add_default_rule(                                               # Añade la regla por defecto
        prerequisites=["pajaro(X)"],
        justifications=["pinguino(X)"],
        conclusion="vuela(X)"
    )
    
    # Calcular extensiones                                              # Comentario para calcular extensiones
    extensions = dl.compute_extensions()                                # Calcula las extensiones
    
    print("\nExtensiones encontradas:")                                # Imprime un encabezado
    for i, ext in enumerate(extensions, 1):                           # Itera sobre las extensiones con su índice
        print(f"Extensión {i}: {ext}")                                 # Imprime cada extensión
    
    # Consultas                                                        # Comentario para las consultas
    print("\n¿Vuela tweety?")                                         # Imprime la consulta
    print(dl.query("vuela(tweety)"))                                   # Realiza la consulta y la imprime (True)
    
    print("\n¿Vuela opus?")                                           # Imprime la consulta
    print(dl.query("vuela(opus)"))                                     # Realiza la consulta y la imprime (False)

def ejemplo_legal():                                                     # Define la función para el ejemplo legal
    """Ejemplo de sistema legal con presunciones"""                      # Documentación de la función ejemplo_legal
    dl = DefaultLogic()                                                 # Crea una instancia de la clase DefaultLogic
    
    # Hechos                                                           # Comentario para los hechos
    dl.add_fact("persona(juan)")                                        # Añade el hecho "persona(juan)"
    dl.add_fact("persona(maria)")                                       # Añade el hecho "persona(maria)"
    dl.add_fact("evidencia_contra(maria)")                              # Añade el hecho "evidencia_contra(maria)"
    
    # Regla por defecto: las personas son inocentes a menos que haya evidencia # Comentario para la regla por defecto
    dl.add_default_rule(                                               # Añade la regla por defecto
        prerequisites=["persona(X)"],
        justifications=["evidencia_contra(X)"],
        conclusion="inocente(X)"
    )
    
    # Otra regla: quienes tienen evidencia son culpables                # Comentario para otra regla por defecto
    dl.add_default_rule(                                               # Añade otra regla por defecto
        prerequisites=["evidencia_contra(X)"],
        justifications=[],
        conclusion="culpable(X)"
    )
    
    extensions = dl.compute_extensions()                                # Calcula las extensiones
    print("\nExtensiones encontradas:")                                # Imprime un encabezado
    for i, ext in enumerate(extensions, 1):                           # Itera sobre las extensiones con su índice
        print(f"Extensión {i}: {ext}")                                 # Imprime cada extensión
    
    # Consultas                                                        # Comentario para las consultas
    print("\n¿Es juan inocente?")                                      # Imprime la consulta
    print(dl.query("inocente(juan)"))                                  # Realiza la consulta y la imprime (True)
    
    print("\n¿Es maria inocente?")                                     # Imprime la consulta
    print(dl.query("inocente(maria)"))                                 # Realiza la consulta y la imprime (False)
    
    print("\n¿Es maria culpable?")                                     # Imprime la consulta
    print(dl.query("culpable(maria)"))                                 # Realiza la consulta y la imprime (True)

if __name__ == "__main__":                                                 # Bloque de código que se ejecuta cuando el script se llama directamente
    print("=== DEMOSTRACIÓN DE LÓGICA POR DEFECTO ===")                 # Imprime un encabezado
    ejemplo_pajaros()                                                      # Llama a la función del ejemplo de los pájaros
    ejemplo_legal()                                                        # Llama a la función del ejemplo legal