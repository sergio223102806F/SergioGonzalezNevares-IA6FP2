# -*- coding: utf-8 -*-                                                     # Define la codificación de caracteres del archivo como UTF-8
"""
Created on Sun Apr 27 14:39:08 2025                                         # Indica la fecha y hora de creación del archivo
                                                                           #
@author: elvin                                                              # Define el autor del archivo
"""

"""
Este código implementa un sistema que simula características clave de Prolog y CLIPS,
mostrando cómo funcionan estos lenguajes de programación lógica.
"""

from typing import Dict, List, Optional, Set, Tuple, Union                     # Importa tipos para anotaciones de tipo
from collections import defaultdict                                      # Importa defaultdict desde el módulo collections

## --------------------------------------------------                         # Separador de sección
## Parte 1: Simulador de Prolog                                             # Título de la sección
## --------------------------------------------------                         # Separador de sección

class PrologEngine:                                                      # Define una clase llamada PrologEngine
    """
    Motor de inferencia estilo Prolog con unificación y backtracking.      # Documentación de la clase PrologEngine
    Implementa un subconjunto básico de funcionalidades de Prolog.
    """
    
    def __init__(self):                                                     # Define el constructor de la clase
        self.rules: Dict[str, List[Tuple[List[Term], Term]]] = defaultdict(list) # Inicializa un diccionario para las reglas de Prolog
        self.facts: Set[Term] = set()                                       # Inicializa un conjunto para los hechos de Prolog
        
    def add_fact(self, fact: Term):                                         # Define el método para añadir un hecho
        """Añade un hecho a la base de conocimiento (como 'padre(juan, maria).')""" # Documentación del método add_fact
        self.facts.add(fact)                                               # Añade el hecho al conjunto de hechos
        
    def add_rule(self, head: Term, body: List[Term]):                       # Define el método para añadir una regla
        """Añade una regla (como 'abuelo(X,Z) :- padre(X,Y), padre(Y,Z).')""" # Documentación del método add_rule
        self.rules[head.functor].append((body, head))                       # Añade la regla al diccionario de reglas
        
    def query(self, goal: Term) -> List[Dict[Variable, Term]]:            # Define el método para realizar una consulta
        """
        Ejecuta una consulta y devuelve todas las sustituciones que la satisfacen. # Documentación del método query
        
        Args:
            goal: Término a probar (como 'padre(juan, X)')
            
        Returns:
            Lista de sustituciones (cada una representa una solución)
        """
        solutions = []                                                   # Inicializa una lista para almacenar las soluciones
        self._prove([goal], {}, solutions)                               # Llama al método _prove para encontrar las soluciones
        return solutions                                                   # Retorna la lista de soluciones
        
    def _prove(self, goals: List[Term], subst: Dict[Variable, Term],         # Define el método recursivo para probar objetivos
               solutions: List[Dict[Variable, Term]]):                    # Argumento para almacenar las soluciones
        """
        Función recursiva que implementa el backtracking para probar objetivos. # Documentación del método _prove
        """
        if not goals:                                                       # Si no hay más objetivos
            # No hay más objetivos que probar - solución encontrada         # Comentario para solución encontrada
            solutions.append(subst.copy())                                  # Añade una copia de la sustitución actual a las soluciones
            return                                                           # Termina la recursión
            
        current_goal = goals[0]                                            # Obtiene el primer objetivo de la lista
        remaining_goals = goals[1:]                                        # Obtiene los objetivos restantes
        
        # 1. Intentar unificar con hechos                                  # Comentario para unificación con hechos
        for fact in self.facts:                                           # Itera sobre los hechos
            new_subst = unify(current_goal, fact, subst.copy())           # Intenta unificar el objetivo actual con el hecho
            if new_subst is not None:                                      # Si la unificación tiene éxito
                self._prove(remaining_goals, new_subst, solutions)        # Llama recursivamente a _prove con los objetivos restantes y la nueva sustitución
        
        # 2. Intentar unificar con reglas                                   # Comentario para unificación con reglas
        if current_goal.functor in self.rules:                            # Si el functor del objetivo actual está en las reglas
            for body, head in self.rules[current_goal.functor]:           # Itera sobre las reglas con la misma cabeza functor
                new_subst = unify(current_goal, head, subst.copy())       # Intenta unificar el objetivo actual con la cabeza de la regla
                if new_subst is not None:                                  # Si la unificación tiene éxito
                    # Reemplazar variables en el cuerpo de la regla       # Comentario para reemplazar variables
                    substituted_body = [apply_substitution(t, new_subst) for t in body] # Aplica la sustitución al cuerpo de la regla
                    self._prove(substituted_body + remaining_goals, new_subst, solutions) # Llama recursivamente a _prove con el nuevo cuerpo, los objetivos restantes y la nueva sustitución

## --------------------------------------------------                         # Separador de sección
## Parte 2: Simulador de CLIPS                                              # Título de la sección
## --------------------------------------------------                         # Separador de sección

class CLIPSEngine:                                                      # Define una clase llamada CLIPSEngine
    """
    Motor de reglas estilo CLIPS con encadenamiento hacia adelante.       # Documentación de la clase CLIPSEngine
    Implementa un subconjunto básico de funcionalidades de CLIPS.
    """
    
    def __init__(self):                                                     # Define el constructor de la clase
        self.rules: List[Rule] = []                                       # Inicializa una lista para las reglas de CLIPS
        self.facts: Set[Fact] = set()                                       # Inicializa un conjunto para los hechos de CLIPS
        self.agenda: List[Rule] = []                                       # Inicializa una lista para la agenda de reglas
        
    def add_fact(self, fact: Fact):                                         # Define el método para añadir un hecho
        """Añade un hecho a la memoria de trabajo"""                       # Documentación del método add_fact
        if fact not in self.facts:                                       # Si el hecho no está ya en el conjunto de hechos
            self.facts.add(fact)                                          # Añade el hecho al conjunto de hechos
            self._update_agenda(fact)                                    # Actualiza la agenda con el nuevo hecho
            
    def add_rule(self, name: str, conditions: List[Condition], actions: List[str]): # Define el método para añadir una regla
        """Añade una regla (como '(defrule mi-regla (hecho ?x) => (print ?x))'""" # Documentación del método add_rule
        self.rules.append((name, conditions, actions))                     # Añade la regla a la lista de reglas
        
    def run(self):                                                          # Define el método para ejecutar el motor
        """Ejecuta el motor de reglas hasta que la agenda esté vacía"""     # Documentación del método run
        while self.agenda:                                                  # Mientras haya reglas en la agenda
            rule_name, _, actions = self.agenda.pop(0)                     # Obtiene y remueve la primera regla de la agenda
            print(f"\nEjecutando regla: {rule_name}")                     # Imprime el nombre de la regla que se está ejecutando
            for action in actions:                                         # Itera sobre las acciones de la regla
                print("  Acción:", action)                                  # Imprime cada acción
                
    def _update_agenda(self, new_fact: Fact):                               # Define el método para actualizar la agenda
        """Actualiza la agenda cuando se añaden nuevos hechos"""           # Documentación del método _update_agenda
        for rule in self.rules:                                           # Itera sobre las reglas
            name, conditions, actions = rule                               # Desempaqueta la regla
            if self._check_conditions(conditions):                         # Verifica si las condiciones de la regla se cumplen con los hechos actuales
                if rule not in self.agenda:                               # Si la regla no está ya en la agenda
                    self.agenda.append(rule)                               # Añade la regla a la agenda
                    
    def _check_conditions(self, conditions: List[Condition]) -> bool:      # Define el método para verificar las condiciones
        """Verifica si todas las condiciones de una regla se satisfacen""" # Documentación del método _check_conditions
        # Implementación simplificada - en CLIPS real esto usa el algoritmo RETE # Comentario sobre la simplificación
        for cond in conditions:                                           # Itera sobre las condiciones
            if not any(self._match_fact(fact, cond) for fact in self.facts): # Verifica si algún hecho coincide con la condición
                return False                                               # Si ninguna coincide, retorna False
        return True                                                        # Si todas las condiciones coinciden con algún hecho, retorna True
        
    def _match_fact(self, fact: Fact, pattern: Condition) -> bool:        # Define el método para hacer coincidir un hecho con un patrón
        """Determina si un hecho coincide con un patrón"""                 # Documentación del método _match_fact
        # Implementación simplificada de matching                          # Comentario sobre la simplificación del matching
        return fact == pattern                                           # Retorna True si el hecho es igual al patrón

## --------------------------------------------------                         # Separador de sección
## Parte 3: Ejemplos de uso                                              # Título de la sección
## --------------------------------------------------                         # Separador de sección

def ejemplo_prolog():                                                     # Define la función para el ejemplo de Prolog
    """Ejemplo de uso del motor Prolog"""                                  # Documentación de la función ejemplo_prolog
    print("\n=== Ejemplo Prolog ===")                                   # Imprime un encabezado
    
    # Crear motor Prolog                                                 # Comentario para la creación del motor Prolog
    pl = PrologEngine()                                                  # Crea una instancia de PrologEngine
    
    # Definir hechos de familia                                            # Comentario para la definición de hechos
    pl.add_fact(Compound("padre", [Atom("juan"), Atom("maria")]))         # Añade el hecho padre(juan, maria)
    pl.add_fact(Compound("padre", [Atom("juan"), Atom("pedro")]))         # Añade el hecho padre(juan, pedro)
    pl.add_fact(Compound("padre", [Atom("pedro"), Atom("ana")]))           # Añade el hecho padre(pedro, ana)
    
    # Definir reglas                                                      # Comentario para la definición de reglas
    X, Y, Z = Variable("X"), Variable("Y"), Variable("Z")               # Crea instancias de Variable
    pl.add_rule(                                                         # Añade la regla abuelo(X, Z) :- padre(X, Y), padre(Y, Z)
        Compound("abuelo", [X, Z]),
        [Compound("padre", [X, Y]), Compound("padre", [Y, Z])]
    )
    
    # Consulta: ¿Quiénes son los abuelos de ana?                         # Comentario para la consulta
    print("\nConsulta: abuelo(X, ana)")                                  # Imprime la consulta
    solutions = pl.query(Compound("abuelo", [X, Atom("ana")]))           # Realiza la consulta
    
    for sol in solutions:                                               # Itera sobre las soluciones
        print(f"X = {sol[X]}")                                          # Imprime el valor de X en cada solución

def ejemplo_clips():                                                      # Define la función para el ejemplo de CLIPS
    """Ejemplo de uso del motor CLIPS"""                                   # Documentación de la función ejemplo_clips
    print("\n=== Ejemplo CLIPS ===")                                    # Imprime un encabezado
    
    # Crear motor CLIPS                                                  # Comentario para la creación del motor CLIPS
    clips = CLIPSEngine()                                                # Crea una instancia de CLIPSEngine
    
    # Definir hechos                                                     # Comentario para la definición de hechos
    clips.add_fact("(persona juan 35)")                                  # Añade el hecho (persona juan 35)
    clips.add_fact("(persona maria 12)")                                 # Añade el hecho (persona maria 12)
    clips.add_fact("(persona pedro 70)")                                 # Añade el hecho (persona pedro 70)
    
    # Definir reglas                                                      # Comentario para la definición de reglas
    clips.add_rule(                                                      # Añade la regla regla-edad
        "regla-edad",
        ["(persona ?n ?e)"],
        ["(print ?n tiene edad ?e)"]
    )
    
    clips.add_rule(                                                      # Añade la regla regla-menor
        "regla-menor",
        ["(persona ?n ?e)", "(test (< ?e 18))"],
        ["(print ?n es menor de edad)"]
    )
    
    # Ejecutar el motor                                                  # Comentario para la ejecución del motor
    print("\nEjecutando reglas...")                                     # Imprime un mensaje
    clips.run()                                                          # Ejecuta el motor de CLIPS

## --------------------------------------------------                         # Separador de sección
## Tipos y funciones auxiliares (compartidos)                              # Título de la sección
## --------------------------------------------------                         # Separador de sección

# Definición de términos lógicos (compartidos por ambos motores)          # Comentario para la definición de términos
Atom = str                                                               # Define Atom como un string
Fact = str                                                               # Define Fact como un string
Condition = str                                                          # Define Condition como un string
Term = Union[Atom, Variable, Compound]                                   # Define Term como la unión de Atom, Variable y Compound

class Variable:                                                         # Define una clase llamada Variable
    """Variable lógica como en Prolog"""                                  # Documentación de la clase Variable
    def __init__(self, name: str):                                         # Define el constructor de la clase
        self.name = name                                                # Inicializa el nombre de la variable
        
    def __repr__(self):                                                    # Define la representación en string del objeto
        return f"Variable({self.name})"                                  # Retorna la representación de la variable
        
    def __eq__(self, other):                                               # Define la igualdad entre variables
        return isinstance(other, Variable) and self.name == other.name   # Retorna True si ambos son Variables y tienen el mismo nombre
        
    def __hash__(self):                                                    # Define el hash de la variable
        return hash(self.name)                                            # Retorna el hash del nombre

class Compound:                                                         # Define una clase llamada Compound
    """Término compuesto como en Prolog"""                                 # Documentación de la clase Compound
    def __init__(self, functor: str, args: List[Term]):                     # Define el constructor de la clase
        self.functor = functor                                          # Inicializa el functor
        self.args = args                                                  # Inicializa la lista de argumentos
        
    def __repr__(self):                                                    # Define la representación en string del objeto
        args_str = ", ".join(map(str, self.args))                         # Convierte los argumentos a strings y los une con ", "
        return f"{self.functor}({args_str})"                             # Retorna la representación del término compuesto
        
    def __eq__(self, other):                                               # Define la igualdad entre términos compuestos
        return (isinstance(other, Compound) and                          # Retorna True si ambos son Compound, tienen el mismo functor
                self.functor == other.functor and
                self.args == other.args)

# Funciones de unificación (similares a las del ejemplo anterior)        # Comentario para las funciones de unificación
def unify(term1: Term, term2: Term, subst: Dict[Variable, Term]) -> Optional[Dict[Variable, Term]]: # Define la función unify
    """Unificación de términos con sustitución acumulada"""             # Documentación de la función unify
    # Implementación simplificada (ver ejemplo completo en unificación anterior) # Comentario sobre la simplificación
    pass                                                                 # Placeholder para la implementación
    
def apply_substitution(term: Term, subst: Dict[Variable, Term]) -> Term: # Define la función apply_substitution
    """Aplica una sustitución a un término"""                           # Documentación de la función apply_substitution
    # Implementación simplificada                                        # Comentario sobre la simplificación
    pass                                                                 # Placeholder para la implementación

if __name__ == "__main__":                                                 # Bloque de código que se ejecuta cuando el script se llama directamente
    print("=== Simuladores de Prolog y CLIPS en Python ===")             # Imprime un encabezado
    
    # Ejecutar ejemplos                                                  # Comentario para la ejecución de ejemplos
    ejemplo_prolog()                                                       # Llama a la función del ejemplo de Prolog
    ejemplo_clips()                                                        # Llama a la función del ejemplo de CLIPS