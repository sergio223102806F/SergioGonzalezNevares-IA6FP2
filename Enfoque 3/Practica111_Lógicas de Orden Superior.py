
# -*- coding: utf-8 -*-                                      # Especifica la codificación del archivo como UTF-8
"""
Created on Sun Apr 27 16:26:19 2025

@author: elvin
"""

"""
Este código implementa un sistema básico para trabajar con lógicas de orden superior (HOL),
permitiendo expresar y manipular predicados sobre predicados, funciones como argumentos,
y cuantificación sobre propiedades.
"""

from typing import Dict, List, Set, Optional, Union, Callable  # Importa tipos para type hints
from collections import defaultdict                           # Para diccionarios con valores por defecto

# ==============================================
# Definición de tipos para términos y fórmulas
# ==============================================

Term = Union['Variable', 'Constant', 'FunctionApplication', 'LambdaAbstraction']  # Tipos de términos
Formula = Union['AtomicFormula', 'Negation', 'And', 'Or', 'Implication', 'QuantifiedFormula']  # Tipos de fórmulas

class Variable:
    """Variable en lógica de orden superior"""
    def __init__(self, name: str, type: str = 'entity'):
        self.name = name                                      # Nombre de la variable (ej. 'x', 'P')
        self.type = type                                      # Tipo: 'entity', 'property', etc.
        
    def __repr__(self):
        return f"{self.name}:{self.type}"                     # Representación nombre:tipo

class Constant:
    """Constante en lógica de orden superior"""
    def __init__(self, name: str, type: str = 'entity'):
        self.name = name                                      # Nombre de la constante (ej. 'a')
        self.type = type                                      # Tipo de la constante
        
    def __repr__(self):
        return f"{self.name}:{self.type}"                     # Representación nombre:tipo

class FunctionApplication:
    """Aplicación de función en lógica de orden superior"""
    def __init__(self, function: Term, argument: Term):
        self.function = function                              # Función a aplicar
        self.argument = argument                              # Argumento de la función
        
    def __repr__(self):
        return f"{self.function}({self.argument})"           # Representación f(arg)

class LambdaAbstraction:
    """Abstracción lambda para definir propiedades/funciones"""
    def __init__(self, variable: Variable, body: Term):
        self.variable = variable                              # Variable ligada
        self.body = body                                      # Cuerpo de la abstracción
        
    def __repr__(self):
        return f"λ{self.variable}.{self.body}"                # Representación λx.body

class AtomicFormula:
    """Fórmula atómica en lógica de orden superior"""
    def __init__(self, predicate: Term, *args: Term):
        self.predicate = predicate                            # Predicado/relación
        self.arguments = args                                 # Argumentos del predicado
        
    def __repr__(self):
        args = ', '.join(map(str, self.arguments))            # Convierte args a string
        return f"{self.predicate}({args})"                    # Representación pred(arg1, arg2)

class Negation:
    """Negación de una fórmula"""
    def __init__(self, formula: Formula):
        self.formula = formula                                # Fórmula a negar
        
    def __repr__(self):
        return f"¬{self.formula}"                             # Representación ¬formula

class And:
    """Conjunción lógica"""
    def __init__(self, left: Formula, right: Formula):
        self.left = left                                      # Fórmula izquierda
        self.right = right                                    # Fórmula derecha
        
    def __repr__(self):
        return f"({self.left} ∧ {self.right})"               # Representación (A ∧ B)

class Or:
    """Disyunción lógica"""
    def __init__(self, left: Formula, right: Formula):
        self.left = left                                      # Fórmula izquierda
        self.right = right                                    # Fórmula derecha
        
    def __repr__(self):
        return f"({self.left} ∨ {self.right})"               # Representación (A ∨ B)

class Implication:
    """Implicación lógica"""
    def __init__(self, antecedent: Formula, consequent: Formula):
        self.antecedent = antecedent                          # Premisa (antecedente)
        self.consequent = consequent                          # Conclusión (consecuente)
        
    def __repr__(self):
        return f"({self.antecedent} → {self.consequent})"    # Representación (A → B)

class QuantifiedFormula:
    """Fórmula cuantificada (universal o existencial)"""
    def __init__(self, quantifier: str, variable: Variable, formula: Formula):
        self.quantifier = quantifier                          # 'forall' o 'exists'
        self.variable = variable                              # Variable cuantificada
        self.formula = formula                                # Fórmula dentro del alcance
        
    def __repr__(self):
        return f"{self.quantifier} {self.variable}. {self.formula}"  # Representación ∀x.A

# ==============================================
# Sistema de Tipos para HOL
# ==============================================

class TypeSystem:
    """Sistema de tipos para lógica de orden superior"""
    
    def __init__(self):
        self.type_hierarchy = {                              # Jerarquía de tipos
            'entity': set(),                                 # Entidades básicas
            'property': {'entity'},                          # Propiedades de entidades
            'property2': {'property'},                       # Propiedades de propiedades
            'function': {'entity', 'property'}               # Funciones que devuelven valores
        }
        
    def is_subtype(self, subtype: str, supertype: str) -> bool:
        """Verifica si un tipo es subtipo de otro"""
        if subtype == supertype:
            return True                                      # Todo tipo es subtipo de sí mismo
        return supertype in self.type_hierarchy.get(subtype, set())  # Verifica jerarquía

# ==============================================
# Motor de Inferencia para HOL
# ==============================================

class HOLInferenceEngine:
    """Motor de inferencia básico para lógica de orden superior"""
    
    def __init__(self):
        self.type_system = TypeSystem()                      # Sistema de tipos asociado
        self.knowledge_base = set()                          # Base de conocimiento (fórmulas)
        
    def add_formula(self, formula: Formula):
        """Añade una fórmula a la base de conocimiento"""
        self.knowledge_base.add(formula)                     # Almacena fórmula en KB
        
    def check_type(self, term: Term, expected_type: str) -> bool:
        """Verifica si un término tiene el tipo esperado"""
        if isinstance(term, Variable) or isinstance(term, Constant):
            return self.type_system.is_subtype(term.type, expected_type)  # Comprueba tipos
        return True                                          # Simplificación para otros casos
        
    def unify(self, term1: Term, term2: Term, substitution: Dict[Variable, Term] = None) -> Optional[Dict[Variable, Term]]:
        """Unificación para términos de orden superior"""
        if substitution is None:
            substitution = {}                                # Inicializa sustitución vacía
            
        # Implementación simplificada de unificación
        if isinstance(term1, Variable):
            if self.check_type(term1, term2.type if hasattr(term2, 'type') else 'entity'):
                substitution[term1] = term2                  # Sustituye variable por término
                return substitution
        elif isinstance(term2, Variable):
            if self.check_type(term2, term1.type if hasattr(term1, 'type') else 'entity'):
                substitution[term2] = term1                  # Sustituye variable por término
                return substitution
        elif isinstance(term1, Constant) and isinstance(term2, Constant):
            if term1.name == term2.name and term1.type == term2.type:
                return substitution                          # Coincidencia de constantes
        # ... otros casos de unificación
        
        return None                                         # Fallo de unificación
        
    def prove(self, formula: Formula, assumptions: Set[Formula] = None, depth: int = 0, max_depth: int = 10) -> bool:
        """
        Intenta probar una fórmula a partir de la base de conocimiento.
        """
        if assumptions is None:
            assumptions = set()                              # Inicializa suposiciones
            
        if depth > max_depth:
            return False                                     # Evita recursión infinita
            
        # Si la fórmula está en KB o suposiciones
        if formula in self.knowledge_base or formula in assumptions:
            return True                                      # Prueba exitosa
            
        # Caso para conjunciones
        if isinstance(formula, And):
            return (self.prove(formula.left, assumptions, depth+1, max_depth) and 
                    self.prove(formula.right, assumptions, depth+1, max_depth))
                    
        # Caso para disyunciones
        elif isinstance(formula, Or):
            return (self.prove(formula.left, assumptions, depth+1, max_depth) or 
                    self.prove(formula.right, assumptions, depth+1, max_depth))
                    
        # Caso para implicaciones
        elif isinstance(formula, Implication):
            new_assumptions = assumptions.copy()
            new_assumptions.add(formula.antecedent)         # Añade antecedente a suposiciones
            return self.prove(formula.consequent, new_assumptions, depth+1, max_depth)
            
        # Caso para fórmulas cuantificadas
        elif isinstance(formula, QuantifiedFormula):
            if formula.quantifier == 'forall':
                # Instanciación de universal con constante fresca
                const = Constant(f'c_{depth}', formula.variable.type)
                instantiated = self.substitute(formula.formula, formula.variable, const)
                return self.prove(instantiated, assumptions, depth+1, max_depth)
            elif formula.quantifier == 'exists':
                # Búsqueda de testigo existencial (simplificado)
                for known in self.knowledge_base:
                    pass                                    # Implementación real sería más compleja
                    
        # Otras estrategias de prueba...
        return False                                        # Fallo en la prueba
        
    def substitute(self, formula: Formula, variable: Variable, replacement: Term) -> Formula:
        """Sustituye una variable por un término en una fórmula"""
        if isinstance(formula, AtomicFormula):
            new_args = [replacement if arg == variable else arg for arg in formula.arguments]
            return AtomicFormula(formula.predicate, *new_args)  # Sustituye en args atómicos
        # ... otros casos de sustitución
        return formula

# ==============================================
# Ejemplos de uso
# ==============================================

def ejemplo_hol():
    """Ejemplos de lógica de orden superior"""
    # Crear variables y constantes
    x = Variable('x', 'entity')                              # Variable de entidad
    P = Variable('P', 'property')                            # Variable de propiedad
    Q = Variable('Q', 'property2')                           # Variable de propiedad de propiedades
    a = Constant('a', 'entity')                              # Constante de entidad
    
    # Ejemplo 1: Cuantificación sobre propiedades
    formula1 = QuantifiedFormula(
        'forall',
        P,
        Implication(
            AtomicFormula(P, a),                             # P(a)
            QuantifiedFormula(
                'exists',
                x,
                AtomicFormula(P, x)                          # ∃x.P(x)
            )
        )
    )
    
    # Ejemplo 2: Propiedades de propiedades
    formula2 = QuantifiedFormula(
        'forall',
        Q,
        Implication(
            AtomicFormula(Q, P),                             # Q(P)
            AtomicFormula(Q, LambdaAbstraction(x, AtomicFormula(P, x)))  # Q(λx.P(x))
        )
    )
    
    print("=== Ejemplo 1 ===")
    print("Fórmula HOL:", formula1)                          # Muestra primera fórmula
    
    print("\n=== Ejemplo 2 ===")
    print("Fórmula HOL:", formula2)                          # Muestra segunda fórmula
    
    # Crear motor de inferencia
    engine = HOLInferenceEngine()
    engine.add_formula(formula1)                             # Añade fórmula a KB
    
    # Intentar probar una instancia
    Pa = AtomicFormula(Variable('P', 'property'), a)         # P(a)
    exists_x_Px = QuantifiedFormula('exists', x, AtomicFormula(Variable('P', 'property'), x))  # ∃x.P(x)
    implication = Implication(Pa, exists_x_Px)               # P(a) → ∃x.P(x)
    
    print("\nIntentando probar:", implication)
    print("Resultado:", engine.prove(implication))           # Intenta probar la implicación

if __name__ == "__main__":
    print("=== Lógica de Orden Superior (HOL) ===")          # Título principal
    ejemplo_hol()                                            # Ejecuta ejemplos
```