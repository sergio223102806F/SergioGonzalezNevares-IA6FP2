# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 14:39:06 2025

@author: elvin
"""

"""
Este código implementa el algoritmo de unificación utilizado en sistemas lógicos y de programación lógica.
La unificación es el proceso de hacer que dos términos lógicos sean idénticos encontrando sustituciones para las variables.
"""

from typing import Dict, Optional, Union, List
from collections import defaultdict

# Definición de tipos para términos lógicos
Term = Union[str, 'Variable', 'Compound']
Substitution = Dict['Variable', Term]

class Variable:
    """Representa una variable lógica (como X, Y en Prolog)"""
    
    def __init__(self, name: str):
        self.name = name
        
    def __repr__(self):
        return f"Variable('{self.name}')"
    
    def __eq__(self, other):
        return isinstance(other, Variable) and self.name == other.name
    
    def __hash__(self):
        return hash(self.name)

class Compound:
    """Representa un término compuesto (functor con argumentos)"""
    
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

def unify(term1: Term, term2: Term, substitution: Optional[Substitution] = None) -> Optional[Substitution]:
    """
    Algoritmo de unificación que encuentra la sustitución más general (MGU) que hace que 
    los dos términos sean iguales.
    
    Args:
        term1: Primer término a unificar
        term2: Segundo término a unificar
        substitution: Sustitución acumulada (usada en llamadas recursivas)
        
    Returns:
        Diccionario con las sustituciones necesarias o None si no hay unificación posible
    """
    if substitution is None:
        substitution = {}
        
    # Paso 1: Si ya tenemos una sustitución para estos términos, usarla
    term1 = apply_substitution(term1, substitution)
    term2 = apply_substitution(term2, substitution)
    
    # Paso 2: Si son idénticos, no hay nada que hacer
    if term1 == term2:
        return substitution
    
    # Paso 3: Si uno es variable, sustituir
    if isinstance(term1, Variable):
        return unify_variable(term1, term2, substitution)
    
    if isinstance(term2, Variable):
        return unify_variable(term2, term1, substitution)
    
    # Paso 4: Si ambos son compuestos, unificar functor y argumentos
    if isinstance(term1, Compound) and isinstance(term2, Compound):
        if term1.functor != term2.functor or len(term1.args) != len(term2.args):
            return None  # No pueden unificarse
        
        for arg1, arg2 in zip(term1.args, term2.args):
            substitution = unify(arg1, arg2, substitution)
            if substitution is None:
                return None
                
        return substitution
    
    # Paso 5: No hay unificación posible
    return None

def unify_variable(v: Variable, term: Term, substitution: Substitution) -> Optional[Substitution]:
    """
    Maneja la unificación cuando uno de los términos es una variable.
    
    Args:
        v: Variable a unificar
        term: Término con el que unificar
        substitution: Sustitución actual
        
    Returns:
        Nueva sustitución o None si falla
    """
    # Si la variable ya está en la sustitución, unificar con su valor
    if v in substitution:
        return unify(substitution[v], term, substitution)
    
    # Comprobar ocurrencia: la variable no puede unificarse con un término que la contenga
    if isinstance(term, Variable) and term in substitution:
        return unify(v, substitution[term], substitution)
    
    if occurs_check(v, term, substitution):
        return None  # Fallo por ocurrencia
    
    # Crear nueva sustitución
    new_substitution = substitution.copy()
    new_substitution[v] = term
    return new_substitution

def occurs_check(v: Variable, term: Term, substitution: Substitution) -> bool:
    """
    Comprueba si una variable aparece dentro de un término (evita ciclos infinitos).
    
    Args:
        v: Variable a buscar
        term: Término donde buscar
        substitution: Sustitución actual
        
    Returns:
        True si la variable aparece en el término, False en caso contrario
    """
    term = apply_substitution(term, substitution)
    
    if v == term:
        return True
    
    if isinstance(term, Compound):
        return any(occurs_check(v, arg, substitution) for arg in term.args)
    
    return False

def apply_substitution(term: Term, substitution: Substitution) -> Term:
    """
    Aplica una sustitución a un término.
    
    Args:
        term: Término original
        substitution: Sustitución a aplicar
        
    Returns:
        Término con las variables sustituidas
    """
    if isinstance(term, Variable):
        return substitution.get(term, term)
    
    if isinstance(term, Compound):
        return Compound(term.functor, [apply_substitution(arg, substitution) for arg in term.args])
    
    return term

def pretty_print_substitution(substitution: Optional[Substitution]) -> str:
    """
    Formatea una sustitución para mostrarla de manera legible.
    
    Args:
        substitution: Sustitución a mostrar
        
    Returns:
        Cadena formateada con la sustitución
    """
    if substitution is None:
        return "No hay unificación posible"
    
    if not substitution:
        return "No se necesitan sustituciones (los términos ya son idénticos)"
    
    items = [f"{var.name} = {term}" for var, term in substitution.items()]
    return "Sustitución más general (MGU):\n  " + "\n  ".join(items)

def ejemplos_unificacion():
    """
    Ejemplos prácticos de unificación con diferentes casos.
    """
    # Ejemplo 1: Unificación simple de variables
    X = Variable('X')
    Y = Variable('Y')
    term1 = X
    term2 = Compound('a', [])
    print("\n=== Ejemplo 1 ===")
    print(f"Unificar: {term1} con {term2}")
    result = unify(term1, term2)
    print(pretty_print_substitution(result))
    
    # Ejemplo 2: Unificación de términos compuestos
    term3 = Compound('f', [X, Compound('b', [])])
    term4 = Compound('f', [Compound('a', []), Y])
    print("\n=== Ejemplo 2 ===")
    print(f"Unificar: {term3} con {term4}")
    result = unify(term3, term4)
    print(pretty_print_substitution(result))
    
    # Ejemplo 3: Unificación con ocurrencia (debe fallar)
    term5 = Compound('f', [X, X])
    term6 = Compound('f', [Y, Compound('g', [Y])])
    print("\n=== Ejemplo 3 ===")
    print(f"Unificar: {term5} con {term6}")
    result = unify(term5, term6)
    print(pretty_print_substitution(result))
    
    # Ejemplo 4: Unificación más compleja
    Z = Variable('Z')
    term7 = Compound('h', [X, Compound('f', [Y]), Y])
    term8 = Compound('h', [Compound('a', []), Z, X])
    print("\n=== Ejemplo 4 ===")
    print(f"Unificar: {term7} con {term8}")
    result = unify(term7, term8)
    print(pretty_print_substitution(result))
    
    # Ejemplo 5: Unificación de listas (representadas como compuestos)
    # lista [a, b, X] se representa como cons(a, cons(b, cons(X, nil)))
    nil = Compound('nil', [])
    def cons(head, tail):
        return Compound('cons', [head, tail])
    
    lista1 = cons(X, cons(Y, cons(Compound('a', []), nil)))
    lista2 = cons(Compound('b', []), cons(Z, cons(W, nil)))
    W = Variable('W')
    print("\n=== Ejemplo 5 ===")
    print(f"Unificar: {lista1} con {lista2}")
    result = unify(lista1, lista2)
    print(pretty_print_substitution(result))

if __name__ == "__main__":
    print("=== Sistema de Unificación Lógica ===")
    ejemplos_unificacion()