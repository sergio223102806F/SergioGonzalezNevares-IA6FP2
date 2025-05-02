# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 14:39:08 2025

@author: elvin
"""

"""
Este código implementa un sistema que simula características clave de Prolog y CLIPS,
mostrando cómo funcionan estos lenguajes de programación lógica.
"""

from typing import Dict, List, Optional, Set, Tuple, Union
from collections import defaultdict

## --------------------------------------------------
## Parte 1: Simulador de Prolog
## --------------------------------------------------

class PrologEngine:
    """
    Motor de inferencia estilo Prolog con unificación y backtracking.
    Implementa un subconjunto básico de funcionalidades de Prolog.
    """
    
    def __init__(self):
        self.rules: Dict[str, List[Tuple[List[Term], Term]]] = defaultdict(list)
        self.facts: Set[Term] = set()
        
    def add_fact(self, fact: Term):
        """Añade un hecho a la base de conocimiento (como 'padre(juan, maria).')"""
        self.facts.add(fact)
        
    def add_rule(self, head: Term, body: List[Term]):
        """Añade una regla (como 'abuelo(X,Z) :- padre(X,Y), padre(Y,Z).')"""
        self.rules[head.functor].append((body, head))
        
    def query(self, goal: Term) -> List[Dict[Variable, Term]]:
        """
        Ejecuta una consulta y devuelve todas las sustituciones que la satisfacen.
        
        Args:
            goal: Término a probar (como 'padre(juan, X)')
            
        Returns:
            Lista de sustituciones (cada una representa una solución)
        """
        solutions = []
        self._prove([goal], {}, solutions)
        return solutions
        
    def _prove(self, goals: List[Term], subst: Dict[Variable, Term], 
               solutions: List[Dict[Variable, Term]]):
        """
        Función recursiva que implementa el backtracking para probar objetivos.
        """
        if not goals:
            # No hay más objetivos que probar - solución encontrada
            solutions.append(subst.copy())
            return
            
        current_goal = goals[0]
        remaining_goals = goals[1:]
        
        # 1. Intentar unificar con hechos
        for fact in self.facts:
            new_subst = unify(current_goal, fact, subst.copy())
            if new_subst is not None:
                self._prove(remaining_goals, new_subst, solutions)
        
        # 2. Intentar unificar con reglas
        if current_goal.functor in self.rules:
            for body, head in self.rules[current_goal.functor]:
                new_subst = unify(current_goal, head, subst.copy())
                if new_subst is not None:
                    # Reemplazar variables en el cuerpo de la regla
                    substituted_body = [apply_substitution(t, new_subst) for t in body]
                    self._prove(substituted_body + remaining_goals, new_subst, solutions)

## --------------------------------------------------
## Parte 2: Simulador de CLIPS
## --------------------------------------------------

class CLIPSEngine:
    """
    Motor de reglas estilo CLIPS con encadenamiento hacia adelante.
    Implementa un subconjunto básico de funcionalidades de CLIPS.
    """
    
    def __init__(self):
        self.rules: List[Rule] = []
        self.facts: Set[Fact] = set()
        self.agenda: List[Rule] = []
        
    def add_fact(self, fact: Fact):
        """Añade un hecho a la memoria de trabajo"""
        if fact not in self.facts:
            self.facts.add(fact)
            self._update_agenda(fact)
            
    def add_rule(self, name: str, conditions: List[Condition], actions: List[str]):
        """Añade una regla (como '(defrule mi-regla (hecho ?x) => (print ?x))'"""
        self.rules.append((name, conditions, actions))
        
    def run(self):
        """Ejecuta el motor de reglas hasta que la agenda esté vacía"""
        while self.agenda:
            rule_name, _, actions = self.agenda.pop(0)
            print(f"\nEjecutando regla: {rule_name}")
            for action in actions:
                print("  Acción:", action)
                
    def _update_agenda(self, new_fact: Fact):
        """Actualiza la agenda cuando se añaden nuevos hechos"""
        for rule in self.rules:
            name, conditions, actions = rule
            if self._check_conditions(conditions):
                if rule not in self.agenda:
                    self.agenda.append(rule)
                    
    def _check_conditions(self, conditions: List[Condition]) -> bool:
        """Verifica si todas las condiciones de una regla se satisfacen"""
        # Implementación simplificada - en CLIPS real esto usa el algoritmo RETE
        for cond in conditions:
            if not any(self._match_fact(fact, cond) for fact in self.facts):
                return False
        return True
        
    def _match_fact(self, fact: Fact, pattern: Condition) -> bool:
        """Determina si un hecho coincide con un patrón"""
        # Implementación simplificada de matching
        return fact == pattern

## --------------------------------------------------
## Parte 3: Ejemplos de uso
## --------------------------------------------------

def ejemplo_prolog():
    """Ejemplo de uso del motor Prolog"""
    print("\n=== Ejemplo Prolog ===")
    
    # Crear motor Prolog
    pl = PrologEngine()
    
    # Definir hechos de familia
    pl.add_fact(Compound("padre", [Atom("juan"), Atom("maria")]))
    pl.add_fact(Compound("padre", [Atom("juan"), Atom("pedro")]))
    pl.add_fact(Compound("padre", [Atom("pedro"), Atom("ana")]))
    
    # Definir reglas
    X, Y, Z = Variable("X"), Variable("Y"), Variable("Z")
    pl.add_rule(
        Compound("abuelo", [X, Z]),
        [Compound("padre", [X, Y]), Compound("padre", [Y, Z])]
    )
    
    # Consulta: ¿Quiénes son los abuelos de ana?
    print("\nConsulta: abuelo(X, ana)")
    solutions = pl.query(Compound("abuelo", [X, Atom("ana")]))
    
    for sol in solutions:
        print(f"X = {sol[X]}")

def ejemplo_clips():
    """Ejemplo de uso del motor CLIPS"""
    print("\n=== Ejemplo CLIPS ===")
    
    # Crear motor CLIPS
    clips = CLIPSEngine()
    
    # Definir hechos
    clips.add_fact("(persona juan 35)")
    clips.add_fact("(persona maria 12)")
    clips.add_fact("(persona pedro 70)")
    
    # Definir reglas
    clips.add_rule(
        "regla-edad",
        ["(persona ?n ?e)"],
        ["(print ?n tiene edad ?e)"]
    )
    
    clips.add_rule(
        "regla-menor",
        ["(persona ?n ?e)", "(test (< ?e 18))"],
        ["(print ?n es menor de edad)"]
    )
    
    # Ejecutar el motor
    print("\nEjecutando reglas...")
    clips.run()

## --------------------------------------------------
## Tipos y funciones auxiliares (compartidos)
## --------------------------------------------------

# Definición de términos lógicos (compartidos por ambos motores)
Atom = str
Fact = str
Condition = str
Term = Union[Atom, Variable, Compound]

class Variable:
    """Variable lógica como en Prolog"""
    def __init__(self, name: str):
        self.name = name
        
    def __repr__(self):
        return f"Variable({self.name})"
        
    def __eq__(self, other):
        return isinstance(other, Variable) and self.name == other.name
        
    def __hash__(self):
        return hash(self.name)

class Compound:
    """Término compuesto como en Prolog"""
    def __init__(self, functor: str, args: List[Term]):
        self.functor = functor
        self.args = args
        
    def __repr__(self):
        args_str = ", ".join(map(str, self.args))
        return f"{self.functor}({args_str})"
        
    def __eq__(self, other):
        return (isinstance(other, Compound) and 
                self.functor == other.functor and 
                self.args == other.args)

# Funciones de unificación (similares a las del ejemplo anterior)
def unify(term1: Term, term2: Term, subst: Dict[Variable, Term]) -> Optional[Dict[Variable, Term]]:
    """Unificación de términos con sustitución acumulada"""
    # Implementación simplificada (ver ejemplo completo en unificación anterior)
    pass
    
def apply_substitution(term: Term, subst: Dict[Variable, Term]) -> Term:
    """Aplica una sustitución a un término"""
    # Implementación simplificada
    pass

if __name__ == "__main__":
    print("=== Simuladores de Prolog y CLIPS en Python ===")
    
    # Ejecutar ejemplos
    ejemplo_prolog()
    ejemplo_clips()