```python
# -*- coding: utf-8 -*-                                                     # Define la codificación de caracteres del archivo como UTF-8
"""
Created on Sun Apr 27 14:39:07 2025                                         # Indica la fecha y hora de creación del archivo
                                                                           #
@author: elvin                                                              # Define el autor del archivo
"""

"""
Este código implementa ambos tipos de encadenamiento lógico:
1. Encadenamiento hacia adelante (forward chaining)
2. Encadenamiento hacia atrás (backward chaining)
"""

from typing import Dict, List, Set, Tuple, Optional                       # Importa tipos para anotaciones de tipo
from collections import deque                                             # Importa deque desde el módulo collections

# Definición de tipos                                                     # Comentario para la definición de tipos
Rule = Tuple[List[str], str]                                            # Define un tipo llamado Rule como una tupla de lista de strings y un string (premisas, conclusión)
KnowledgeBase = Dict[str, List[Rule]]                                   # Define un tipo llamado KnowledgeBase como un diccionario donde las claves son strings (conclusiones) y los valores son listas de Rules

class InferenceEngine:                                                 # Define una clase llamada InferenceEngine
    """
    Motor de inferencia que soporta ambos tipos de encadenamiento.     # Documentación de la clase InferenceEngine
    """
    
    def __init__(self):                                                     # Define el constructor de la clase
        self.kb: KnowledgeBase = defaultdict(list)                        # Inicializa un diccionario con listas vacías como valor predeterminado para la base de conocimiento
        self.facts: Set[str] = set()                                       # Inicializa un conjunto para almacenar los hechos conocidos
        self.agenda: deque = deque()                                       # Inicializa una cola doble para la agenda del encadenamiento hacia adelante
        
    def add_rule(self, premises: List[str], conclusion: str):             # Define el método para añadir una regla
        """
        Añade una regla a la base de conocimiento.                       # Documentación del método add_rule
        
        Args:
            premises: Lista de premisas
            conclusion: Conclusión de la regla
        """
        rule = (premises, conclusion)                                    # Crea una tupla representando la regla
        self.kb[conclusion].append(rule)                                  # Añade la regla a la lista de reglas para la conclusión dada
        
    def add_fact(self, fact: str):                                         # Define el método para añadir un hecho
        """
        Añade un hecho a la base de conocimiento y lo pone en la agenda. # Documentación del método add_fact
        
        Args:
            fact: Hecho a añadir
        """
        if fact not in self.facts:                                       # Si el hecho no está ya en el conjunto de hechos
            self.facts.add(fact)                                          # Añade el hecho al conjunto de hechos
            self.agenda.append(fact)                                        # Añade el hecho a la agenda para el encadenamiento hacia adelante
        
    def forward_chain(self) -> Set[str]:                                 # Define el método para el encadenamiento hacia adelante
        """
        Encadenamiento hacia adelante: parte de los hechos conocidos y aplica
        reglas hasta que no se pueden derivar nuevos hechos.
        
        Returns:
            Conjunto de todos los hechos derivados
        """
        derived_facts = set()                                            # Inicializa un conjunto para almacenar los hechos derivados
        
        while self.agenda:                                                # Mientras haya hechos en la agenda
            fact = self.agenda.popleft()                                  # Obtiene y remueve el hecho más antiguo de la agenda
            
            # Para cada regla que tenga esta fact como premisa              # Comentario para la iteración sobre las reglas
            for conclusion, rules in self.kb.items():                     # Itera sobre las conclusiones y sus listas de reglas en la base de conocimiento
                for rule in rules:                                       # Itera sobre las reglas para la conclusión actual
                    premises, rule_conclusion = rule                      # Desempaqueta las premisas y la conclusión de la regla
                    
                    if fact in premises:                                  # Si el hecho actual está en las premisas de la regla
                        # Verificar si todas las premisas se cumplen         # Comentario para la verificación de las premisas
                        if all(p in self.facts for p in premises):        # Si todos los elementos de las premisas están en el conjunto de hechos conocidos
                            # Añadir conclusión si es nueva                 # Comentario para añadir la conclusión
                            if rule_conclusion not in self.facts:        # Si la conclusión de la regla no está en el conjunto de hechos conocidos
                                self.add_fact(rule_conclusion)            # Añade la conclusión al conjunto de hechos conocidos y a la agenda
                                derived_facts.add(rule_conclusion)       # Añade la conclusión al conjunto de hechos derivados
        
        return derived_facts                                             # Retorna el conjunto de todos los hechos derivados
    
    def backward_chain(self, goal: str, visited: Optional[Set[str]] = None) -> bool: # Define el método para el encadenamiento hacia atrás
        """
        Encadenamiento hacia atrás: intenta demostrar un objetivo buscando
        reglas que lo concluyan y demostrando sus premisas recursivamente.
        
        Args:
            goal: Objetivo a demostrar
            visited: Conjunto de objetivos ya visitados (para evitar ciclos)
            
        Returns:
            True si el objetivo puede ser demostrado, False en caso contrario
        """
        if visited is None:                                               # Si el conjunto de objetivos visitados no se proporciona
            visited = set()                                              # Inicializa un conjunto vacío para los objetivos visitados
            
        # Si el objetivo ya es un hecho conocido                        # Comentario para la verificación del objetivo como hecho
        if goal in self.facts:                                           # Si el objetivo está en el conjunto de hechos conocidos
            return True                                                   # Retorna True
            
        # Si ya hemos visitado este objetivo (evitar ciclos)             # Comentario para la verificación de objetivos visitados
        if goal in visited:                                           # Si el objetivo ya ha sido visitado
            return False                                                  # Retorna False para evitar ciclos
            
        visited.add(goal)                                                # Añade el objetivo actual al conjunto de objetivos visitados
        
        # Buscar reglas que concluyan este objetivo                     # Comentario para la búsqueda de reglas para el objetivo
        for rule in self.kb.get(goal, []):                               # Itera sobre las reglas que tienen el objetivo como conclusión
            premises, _ = rule                                           # Obtiene las premisas de la regla
            
            # Intentar demostrar todas las premisas                      # Comentario para intentar demostrar las premisas
            if all(self.backward_chain(p, visited) for p in premises):  # Verifica recursivamente si todas las premisas pueden ser demostradas
                self.add_fact(goal)                                      # Añade el objetivo como un hecho conocido
                return True                                               # Retorna True si todas las premisas se pueden demostrar
                
        return False                                                      # Retorna False si no se encuentra una regla o no se pueden demostrar las premisas
    
    def explain(self, fact: str, depth: int = 0) -> Optional[str]:      # Define el método para generar una explicación
        """
        Genera una explicación de cómo se derivó un hecho.               # Documentación del método explain
        
        Args:
            fact: Hecho a explicar
            depth: Profundidad actual (para indentación)
            
        Returns:
            Cadena con la explicación o None si el hecho no se conoce
        """
        if fact not in self.facts:                                       # Si el hecho no está en el conjunto de hechos conocidos
            return None                                                   # Retorna None
            
        explanation = []                                                 # Inicializa una lista para almacenar las líneas de la explicación
        indent = "  " * depth                                           # Crea una cadena de indentación basada en la profundidad
        
        # Buscar reglas que hayan concluido este hecho                   # Comentario para buscar reglas para el hecho
        rules_used = []                                                  # Inicializa una lista para las reglas utilizadas
        for rule in self.kb.get(fact, []):                               # Itera sobre las reglas que tienen el hecho como conclusión
            premises, _ = rule                                           # Obtiene las premisas de la regla
            if all(p in self.facts for p in premises):                  # Si todas las premisas de la regla son hechos conocidos
                rules_used.append(rule)                                  # Añade la regla a la lista de reglas utilizadas
        
        if rules_used:                                                   # Si se encontraron reglas utilizadas
            # Tomar la primera regla que se usó                          # Comentario para tomar la primera regla
            premises, _ = rules_used[0]                                  # Obtiene las premisas de la primera regla utilizada
            explanation.append(f"{indent}{fact} se deriva de:")          # Añade una línea a la explicación
            
            for p in premises:                                           # Itera sobre las premisas de la regla
                premise_explanation = self.explain(p, depth + 1)        # Obtiene la explicación de la premisa recursivamente
                if premise_explanation:                                  # Si se encontró una explicación para la premisa
                    explanation.append(premise_explanation)              # Añade la explicación de la premisa a la explicación
                else:                                                      # Si la premisa es un hecho conocido
                    explanation.append(f"{indent}  {p} (hecho conocido)") # Añade una línea indicando que la premisa es un hecho conocido
        else:                                                          # Si no se encontraron reglas utilizadas (el hecho es básico)
            explanation.append(f"{indent}{fact} (hecho conocido)")       # Añade una línea indicando que el hecho es conocido
        
        return "\n".join(explanation)                                   # Une las líneas de la explicación con saltos de línea

def medical_example():                                                # Define la función para el ejemplo médico
    """
    Ejemplo médico que muestra ambos tipos de encadenamiento.        # Documentación de la función medical_example
    """
    engine = InferenceEngine()                                       # Crea una instancia de la clase InferenceEngine
    
    # Añadir reglas                                                    # Comentario para añadir reglas
    engine.add_rule(["fiebre", "tos"], "gripe")                       # Añade la regla: fiebre Y tos => gripe
    engine.add_rule(["fiebre", "erupcion"], "dengue")                   # Añade la regla: fiebre Y erupcion => dengue
    engine.add_rule(["gripe", "dolor_muscular"], "gripe_grave")         # Añade la regla: gripe Y dolor_muscular => gripe_grave
    engine.add_rule(["dengue", "dolor_articular"], "dengue_grave")       # Añade la regla: dengue Y dolor_articular => dengue_grave
    engine.add_rule(["gripe_grave"], "hospitalizar")                   # Añade la regla: gripe_grave => hospitalizar
    engine.add_rule(["dengue_grave"], "hospitalizar")                  # Añade la regla: dengue_grave => hospitalizar
    
    # Encadenamiento hacia adelante                                    # Comentario para el encadenamiento hacia adelante
    print("=== Encadenamiento hacia adelante ===")                     # Imprime un encabezado
    engine.add_fact("fiebre")                                         # Añade el hecho "fiebre"
    engine.add_fact("tos")                                            # Añade el hecho "tos"
    engine.add_fact("dolor_muscular")                                 # Añade el hecho "dolor_muscular"
    
    derived = engine.forward_chain()                                   # Ejecuta el encadenamiento hacia adelante
    print("\nHechos derivados:")                                     # Imprime un encabezado
    for fact in derived:                                             # Itera sobre los hechos derivados
        print(f"- {fact}")                                            # Imprime cada hecho derivado
    
    print("\nExplicación para 'hospitalizar':")                      # Imprime un encabezado para la explicación
    print(engine.explain("hospitalizar") or "No se puede explicar") # Intenta explicar el hecho "hospitalizar"
    
    # Encadenamiento hacia atrás                                       # Comentario para el encadenamiento hacia atrás
    print("\n=== Encadenamiento hacia atrás ===")                      # Imprime un encabezado
    engine2 = InferenceEngine()                                      # Crea una nueva instancia del motor de inferencia
    
    # Añadir las mismas reglas                                         # Comentario para añadir las mismas reglas
    engine2.add_rule(["fiebre", "tos"], "gripe")                      # Añade la regla: fiebre Y tos => gripe
    engine2.add_rule(["fiebre", "erupcion"], "dengue")                  # Añade la regla: fiebre Y erupcion => dengue
    engine2.add_rule(["gripe", "dolor_muscular"], "gripe_grave")        # Añade la regla: gripe Y dolor_muscular => gripe_grave
    engine2.add_rule(["dengue", "dolor_articular"], "dengue_grave")      # Añade la regla: dengue Y dolor_articular => dengue_grave
    engine2.add_rule(["gripe_grave"], "hospitalizar")                  # Añade la regla: gripe_grave => hospitalizar
    engine2.add_rule(["dengue_grave"], "hospitalizar")                 # Añade la regla: dengue_grave => hospitalizar
    
    # Añadir hechos básicos                                            # Comentario para añadir hechos básicos
    engine2.add_fact("fiebre")                                        # Añade el hecho "fiebre"
    engine2.add_fact("erupcion")                                      # Añade el hecho "erupcion"
    engine2.add_fact("dolor_articular")                               # Añade el hecho "dolor_articular"
    
    # Demostrar un objetivo                                           # Comentario para demostrar un objetivo
    goal = "hospitalizar"                                            # Define el objetivo a demostrar
    result = engine2.backward_chain(goal)                            # Ejecuta el encadenamiento hacia atrás para el objetivo
    
    print(f"\n¿Se puede demostrar '{goal}'? {result}")             # Imprime el resultado de la demostración
    print("\nExplicación:")                                        # Imprime un encabezado para la explicación
    print(engine2.explain(goal) or "No se puede explicar")        # Intenta explicar el objetivo

if __name__ == "__main__":                                                # Bloque de código que se ejecuta cuando el script se llama directamente
    print("=== Sistemas de Encadenamiento Hacia Adelante y Atrás ===")    # Imprime un encabezado
    medical_example()                                                     # Llama a la función del ejemplo médico
```