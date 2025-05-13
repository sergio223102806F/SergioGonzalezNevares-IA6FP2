```python
# -*- coding: utf-8 -*-                                                     # Define la codificación de caracteres del archivo como UTF-8
"""
Created on Sun Apr 27 16:26:19 2025                                         # Indica la fecha y hora de creación del archivo
                                                                           #
@author: elvin                                                              # Define el autor del archivo
"""

"""
Este código implementa un agente lógico que utiliza una base de conocimiento 
y razonamiento lógico para tomar decisiones. El agente puede:
1. Percibir su entorno
2. Actualizar su base de conocimiento
3. Realizar inferencias lógicas
4. Seleccionar acciones apropiadas
"""

from typing import Dict, List, Set, Optional, Union                       # Importa tipos para anotaciones de tipo
from collections import defaultdict                                      # Importa defaultdict desde el módulo collections

# ==============================================                           # Separador de sección
# Definición de la Base de Conocimiento                                 # Título de la sección
# ==============================================                           # Separador de sección

class KnowledgeBase:                                                   # Define una clase llamada KnowledgeBase
    """Base de conocimiento para el agente lógico"""                    # Documentación de la clase KnowledgeBase
    
    def __init__(self):                                                     # Define el constructor de la clase
        self.facts: Set[str] = set()                                      # Inicializa un conjunto para almacenar los hechos conocidos
        self.rules: Dict[str, List[List[str]]] = defaultdict(list)        # Inicializa un diccionario con listas vacías como valor predeterminado para las reglas
        
    def add_fact(self, fact: str):                                         # Define el método para agregar un hecho
        """Añade un hecho a la base de conocimiento"""                     # Documentación del método add_fact
        self.facts.add(fact)                                               # Agrega el hecho al conjunto de hechos
        
    def add_rule(self, conclusion: str, premises: List[str]):             # Define el método para agregar una regla
        """Añade una regla (premisas => conclusión)"""                    # Documentación del método add_rule
        self.rules[conclusion].append(premises)                           # Agrega la lista de premisas a la lista de reglas para la conclusión dada
        
    def infer(self, query: str) -> bool:                                  # Define el método para realizar inferencias
        """
        Realiza inferencia hacia adelante para determinar si un hecho se sigue de la KB
        
        Args:
            query: Hecho a verificar
            
        Returns:
            True si el hecho puede ser inferido, False en caso contrario
        """
        # Si el hecho ya está en la KB                                   # Comentario para verificar si el hecho ya existe
        if query in self.facts:                                           # Si la consulta está en el conjunto de hechos
            return True                                                   # Retorna True
            
        # Verificar reglas que puedan inferir el hecho                   # Comentario para verificar las reglas
        for premises in self.rules.get(query, []):                       # Itera sobre las listas de premisas para la consulta
            if all(self.infer(p) for p in premises):                      # Si todas las premisas pueden ser inferidas recursivamente
                self.add_fact(query)                                     # Añade el nuevo hecho inferido a la base de conocimiento
                return True                                               # Retorna True
                
        return False                                                      # Retorna False si no se puede inferir el hecho

# ==============================================                           # Separador de sección
# Definición del Agente Lógico                                           # Título de la sección
# ==============================================                           # Separador de sección

class LogicalAgent:                                                    # Define una clase llamada LogicalAgent
    """Agente que utiliza razonamiento lógico para actuar"""             # Documentación de la clase LogicalAgent
    
    def __init__(self):                                                     # Define el constructor de la clase
        self.kb = KnowledgeBase()                                        # Inicializa una instancia de la clase KnowledgeBase
        self.actions = {}                                                # Inicializa un diccionario para las acciones disponibles
        self.initialize_knowledge()                                      # Llama al método para inicializar el conocimiento
        
    def initialize_knowledge(self):                                       # Define el método para inicializar el conocimiento
        """Inicializa el conocimiento básico del agente"""                # Documentación del método initialize_knowledge
        # Ejemplo de reglas para un mundo de wumpus simple               # Comentario para las reglas del mundo wumpus
        self.kb.add_rule("hedor", ["cerca_wumpus"])                       # Agrega la regla: cerca_wumpus => hedor
        self.kb.add_rule("brillo", ["cerca_oro"])                         # Agrega la regla: cerca_oro => brillo
        self.kb.add_rule("peligro", ["hedor"])                           # Agrega la regla: hedor => peligro
        self.kb.add_rule("seguro", ["no_hedor"])                         # Agrega la regla: no_hedor => seguro
        
        # Acciones posibles                                               # Comentario para las acciones posibles
        self.actions = {                                                 # Define un diccionario de acciones y sus métodos correspondientes
            "avanzar": self.avanzar,
            "girar_izquierda": self.girar_izquierda,
            "girar_derecha": self.girar_derecha,
            "agarrar": self.agarrar,
            "salir": self.salir
        }
        
    def perceive(self, perception: Dict[str, bool]):                       # Define el método para procesar las percepciones
        """
        Procesa las percepciones del entorno y actualiza la KB
        
        Args:
            perception: Diccionario de percepciones (ej. {"hedor": True, "brillo": False})
        """
        for p, value in perception.items():                              # Itera sobre los items del diccionario de percepciones
            if value:                                                     # Si el valor de la percepción es True
                self.kb.add_fact(p)                                      # Agrega la percepción como un hecho a la base de conocimiento
            else:                                                        # Si el valor de la percepción es False
                self.kb.add_fact(f"no_{p}")                               # Agrega la negación de la percepción como un hecho
                
    def choose_action(self) -> str:                                      # Define el método para elegir una acción
        """
        Selecciona una acción basada en el conocimiento actual
        
        Returns:
            Nombre de la acción seleccionada
        """
        # Prioridad 1: Agarrar oro si está cerca                         # Comentario para la prioridad de agarrar oro
        if self.kb.infer("brillo"):                                      # Si se puede inferir que el oro está cerca
            return "agarrar"                                              # Retorna la acción "agarrar"
            
        # Prioridad 2: Evitar peligro                                    # Comentario para la prioridad de evitar el peligro
        if self.kb.infer("peligro"):                                     # Si se puede inferir que hay peligro
            return "girar_derecha"                                        # Retorna la acción "girar_derecha" para evitar
            
        # Prioridad 3: Moverse a lugares seguros                         # Comentario para la prioridad de moverse a lugares seguros
        if self.kb.infer("seguro"):                                      # Si se puede inferir que el lugar es seguro
            return "avanzar"                                              # Retorna la acción "avanzar"
            
        # Default: Explorar                                               # Comentario para la acción por defecto
        return "girar_izquierda"                                        # Retorna la acción "girar_izquierda" para explorar
        
    def execute_action(self, action: str):                              # Define el método para ejecutar una acción
        """
        Ejecuta una acción y actualiza el conocimiento
        
        Args:
            action: Nombre de la acción a ejecutar
        """
        if action in self.actions:                                      # Si la acción está en el diccionario de acciones
            self.actions[action]()                                      # Llama al método correspondiente a la acción
        else:                                                          # Si la acción no se encuentra
            print(f"Acción desconocida: {action}")                     # Imprime un mensaje de acción desconocida
            
    # Métodos de acciones                                               # Comentario para los métodos de acción
    def avanzar(self):                                                  # Define el método para la acción "avanzar"
        """Acción de avanzar en la dirección actual"""                   # Documentación del método avanzar
        print("El agente avanza hacia adelante")                       # Imprime un mensaje indicando la acción
        # Actualizar KB con posibles consecuencias                     # Comentario para actualizar la base de conocimiento
        self.kb.add_fact("movimiento_realizado")                      # Agrega el hecho "movimiento_realizado" a la base de conocimiento
        
    def girar_izquierda(self):                                          # Define el método para la acción "girar_izquierda"
        """Acción de girar a la izquierda"""                           # Documentación del método girar_izquierda
        print("El agente gira 90 grados a la izquierda")                 # Imprime un mensaje indicando la acción
        
    def girar_derecha(self):                                           # Define el método para la acción "girar_derecha"
        """Acción de girar a la derecha"""                            # Documentación del método girar_derecha
        print("El agente gira 90 grados a la derecha")                  # Imprime un mensaje indicando la acción
        
    def agarrar(self):                                                 # Define el método para la acción "agarrar"
        """Acción de agarrar un objeto"""                              # Documentación del método agarrar
        print("El agente intenta agarrar un objeto")                    # Imprime un mensaje indicando la acción
        self.kb.add_fact("objeto_agarrado")                            # Agrega el hecho "objeto_agarrado" a la base de conocimiento
        
    def salir(self):                                                    # Define el método para la acción "salir"
        """Acción de salir del entorno"""                              # Documentación del método salir
        print("El agente sale del entorno")                           # Imprime un mensaje indicando la acción

# ==============================================                           # Separador de sección
# Ejemplo de Simulación                                                # Título de la sección
# ==============================================                           # Separador de sección

def simulate_agent():                                                 # Define la función para simular al agente
    """Simula el funcionamiento del agente en un entorno"""           # Documentación de la función simulate_agent
    agent = LogicalAgent()                                            # Crea una instancia de la clase LogicalAgent
    
    # Ciclo de percepción-acción                                       # Comentario para el ciclo de percepción-acción
    for step in range(5):                                             # Itera 5 veces para simular pasos
        print(f"\n--- Paso {step + 1} ---")                         # Imprime el número del paso actual
        
        # Percepciones del entorno (ejemplo)                           # Comentario para las percepciones del entorno
        if step == 0:                                                 # En el primer paso
            perception = {"hedor": True, "brillo": False}            # Define las percepciones
        elif step == 2:                                               # En el tercer paso
            perception = {"brillo": True, "hedor": False}            # Define las percepciones
        else:                                                          # En los demás pasos
            perception = {"hedor": False, "brillo": False}           # Define las percepciones
            
        print(f"Percepciones: {perception}")                         # Imprime las percepciones actuales
        agent.perceive(perception)                                   # El agente procesa las percepciones
        
        # Seleccionar y ejecutar acción                                  # Comentario para la selección y ejecución de la acción
        action = agent.choose_action()                                 # El agente elige una acción
        print(f"Acción seleccionada: {action}")                       # Imprime la acción seleccionada
        agent.execute_action(action)                                  # El agente ejecuta la acción
        
        # Condición de terminación                                      # Comentario para la condición de terminación
        if action == "salir":                                         # Si la acción es "salir"
            break                                                      # Termina la simulación

if __name__ == "__main__":                                                 # Bloque de código que se ejecuta cuando el script se llama directamente
    print("=== Simulación de Agente Lógico ===")                       # Imprime un encabezado para la simulación
    simulate_agent()                                                   # Llama a la función para simular al agente
```