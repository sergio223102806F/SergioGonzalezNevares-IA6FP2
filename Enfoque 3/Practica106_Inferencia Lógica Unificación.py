Aquí está el código con comentarios añadidos a la derecha de cada línea:

```python
# -*- coding: utf-8 -*-                                      # Especifica la codificación del archivo como UTF-8
"""
Created on Sun Apr 27 14:39:06 2025

@author: elvin
"""

"""
Este código implementa el algoritmo de unificación utilizado en sistemas lógicos y de programación lógica.
La unificación es el proceso de hacer que dos términos lógicos sean idénticos encontrando sustituciones para las variables.
"""

from typing import Dict, Optional, Union, List                     # Importa tipos para type hints
from collections import defaultdict                               # Importa defaultdict para su posible uso futuro

# Definición de tipos para términos lógicos
Term = Union[str, 'Variable', 'Compound']                        # Un término puede ser string, Variable o Compound
Substitution = Dict['Variable', Term]                            # Una sustitución mapea Variables a Terms

class Variable:
    """Representa una variable lógica (como X, Y en Prolog)"""
    
    def __init__(self, name: str):                                # Constructor de Variable
        self.name = name                                          # Asigna el nombre de la variable
        
    def __repr__(self):                                          # Representación formal para debugging
        return f"Variable('{self.name}')"                        # Devuelve cadena con formato Variable('nombre')
    
    def __eq__(self, other):                                     # Comparación de igualdad
        return isinstance(other, Variable) and self.name == other.name  # Son iguales si son ambas Variables con mismo nombre
    
    def __hash__(self):                                          # Método hash para usar en diccionarios
        return hash(self.name)                                   # Hash basado en el nombre

class Compound:
    """Representa un término compuesto (functor con argumentos)"""
    
    def __init__(self, functor: str, args: List[Term]):          # Constructor de Compound
        self.functor = functor                                   # Nombre del functor (ej. 'f', 'cons')
        self.args = args                                         # Lista de argumentos del término
        
    def __repr__(self):                                          # Representación formal para debugging
        args_str = ", ".join(map(str, self.args))                # Convierte argumentos a cadena separada por comas
        return f"{self.functor}({args_str})"                     # Devuelve cadena con formato functor(arg1, arg2)
    
    def __eq__(self, other):                                     # Comparación de igualdad
        return (isinstance(other, Compound) and                  # Son iguales si ambos son Compounds
                self.functor == other.functor and                # con mismo functor
                self.args == other.args)                          # y mismos argumentos

def unify(term1: Term, term2: Term, substitution: Optional[Substitution] = None) -> Optional[Substitution]:
    """
    Algoritmo de unificación que encuentra la sustitución más general (MGU) que hace que 
    los dos términos sean iguales.
    """
    if substitution is None:                                     # Si no se proporciona sustitución
        substitution = {}                                        # Inicializa con diccionario vacío
        
    # Paso 1: Si ya tenemos una sustitución para estos términos, usarla
    term1 = apply_substitution(term1, substitution)              # Aplica sustitución a term1
    term2 = apply_substitution(term2, substitution)              # Aplica sustitución a term2
    
    # Paso 2: Si son idénticos, no hay nada que hacer
    if term1 == term2:                                           # Si términos son iguales
        return substitution                                      # Retorna sustitución actual
    
    # Paso 3: Si uno es variable, sustituir
    if isinstance(term1, Variable):                              # Si term1 es Variable
        return unify_variable(term1, term2, substitution)        # Unifica variable con term2
    
    if isinstance(term2, Variable):                              # Si term2 es Variable
        return unify_variable(term2, term1, substitution)        # Unifica variable con term1
    
    # Paso 4: Si ambos son compuestos, unificar functor y argumentos
    if isinstance(term1, Compound) and isinstance(term2, Compound):  # Si ambos son Compounds
        if term1.functor != term2.functor or len(term1.args) != len(term2.args):  # Si functores o aridad no coinciden
            return None                                          # No hay unificación posible
        
        for arg1, arg2 in zip(term1.args, term2.args):          # Para cada par de argumentos
            substitution = unify(arg1, arg2, substitution)       # Unifica recursivamente
            if substitution is None:                             # Si falla alguna unificación
                return None                                      # Propaga el fallo
                
        return substitution                                      # Retorna sustitución exitosa
    
    # Paso 5: No hay unificación posible
    return None                                                 # Retorna None si no se pudo unificar

def unify_variable(v: Variable, term: Term, substitution: Substitution) -> Optional[Substitution]:
    """
    Maneja la unificación cuando uno de los términos es una variable.
    """
    # Si la variable ya está en la sustitución, unificar con su valor
    if v in substitution:                                       # Si variable ya tiene sustitución
        return unify(substitution[v], term, substitution)       # Unifica el término sustituido con term
    
    # Comprobar ocurrencia: la variable no puede unificarse con un término que la contenga
    if isinstance(term, Variable) and term in substitution:     # Si term es Variable con sustitución
        return unify(v, substitution[term], substitution)       # Unifica v con su término sustituido
    
    if occurs_check(v, term, substitution):                     # Comprueba ocurrencia de v en term
        return None                                            # Fallo por ocurrencia
    
    # Crear nueva sustitución
    new_substitution = substitution.copy()                      # Copia la sustitución actual
    new_substitution[v] = term                                  # Añade nueva sustitución v -> term
    return new_substitution                                     # Retorna nueva sustitución

def occurs_check(v: Variable, term: Term, substitution: Substitution) -> bool:
    """
    Comprueba si una variable aparece dentro de un término (evita ciclos infinitos).
    """
    term = apply_substitution(term, substitution)               # Aplica sustitución al término
    
    if v == term:                                               # Si la variable es el término
        return True                                             # Ocurrencia encontrada
    
    if isinstance(term, Compound):                              # Si el término es compuesto
        return any(occurs_check(v, arg, substitution) for arg in term.args)  # Busca en cada argumento
    
    return False                                               # No hay ocurrencia

def apply_substitution(term: Term, substitution: Substitution) -> Term:
    """
    Aplica una sustitución a un término.
    """
    if isinstance(term, Variable):                              # Si el término es Variable
        return substitution.get(term, term)                     # Retorna su sustitución o la variable misma
    
    if isinstance(term, Compound):                              # Si el término es Compound
        return Compound(term.functor, [apply_substitution(arg, substitution) for arg in term.args])  # Aplica sustitución a cada argumento
    
    return term                                                 # Retorna término sin cambios (string)

def pretty_print_substitution(substitution: Optional[Substitution]) -> str:
    """
    Formatea una sustitución para mostrarla de manera legible.
    """
    if substitution is None:                                    # Si no hay sustitución
        return "No hay unificación posible"                     # Mensaje de fallo
    
    if not substitution:                                        # Si sustitución vacía
        return "No se necesitan sustituciones (los términos ya son idénticos)"  # Mensaje informativo
    
    items = [f"{var.name} = {term}" for var, term in substitution.items()]  # Formatea cada sustitución
    return "Sustitución más general (MGU):\n  " + "\n  ".join(items)  # Retorna cadena formateada

def ejemplos_unificacion():
    """
    Ejemplos prácticos de unificación con diferentes casos.
    """
    # Ejemplo 1: Unificación simple de variables
    X = Variable('X')                                           # Crea variable X
    Y = Variable('Y')                                           # Crea variable Y
    term1 = X                                                   # Término 1 es X
    term2 = Compound('a', [])                                   # Término 2 es a()
    print("\n=== Ejemplo 1 ===")                                # Encabezado ejemplo
    print(f"Unificar: {term1} con {term2}")                     # Muestra términos a unificar
    result = unify(term1, term2)                                # Intenta unificación
    print(pretty_print_substitution(result))                     # Muestra resultado
    
    # Ejemplo 2: Unificación de términos compuestos
    term3 = Compound('f', [X, Compound('b', [])])               # Término f(X, b())
    term4 = Compound('f', [Compound('a', []), Y])               # Término f(a(), Y)
    print("\n=== Ejemplo 2 ===")                                # Encabezado ejemplo
    print(f"Unificar: {term3} con {term4}")                     # Muestra términos a unificar
    result = unify(term3, term4)                                # Intenta unificación
    print(pretty_print_substitution(result))                     # Muestra resultado
    
    # Ejemplo 3: Unificación con ocurrencia (debe fallar)
    term5 = Compound('f', [X, X])                               # Término f(X, X)
    term6 = Compound('f', [Y, Compound('g', [Y])])              # Término f(Y, g(Y))
    print("\n=== Ejemplo 3 ===")                                # Encabezado ejemplo
    print(f"Unificar: {term5} con {term6}")                     # Muestra términos a unificar
    result = unify(term5, term6)                                # Intenta unificación
    print(pretty_print_substitution(result))                     # Muestra resultado
    
    # Ejemplo 4: Unificación más compleja
    Z = Variable('Z')                                           # Crea variable Z
    term7 = Compound('h', [X, Compound('f', [Y]), Y])           # Término h(X, f(Y), Y)
    term8 = Compound('h', [Compound('a', []), Z, X])            # Término h(a(), Z, X)
    print("\n=== Ejemplo 4 ===")                                # Encabezado ejemplo
    print(f"Unificar: {term7} con {term8}")                     # Muestra términos a unificar
    result = unify(term7, term8)                                # Intenta unificación
    print(pretty_print_substitution(result))                     # Muestra resultado
    
    # Ejemplo 5: Unificación de listas (representadas como compuestos)
    nil = Compound('nil', [])                                   # Representación de lista vacía
    def cons(head, tail):                                       # Función auxiliar para construir listas
        return Compound('cons', [head, tail])                   # Representación cons(head, tail)
    
    lista1 = cons(X, cons(Y, cons(Compound('a', []), nil)))     # Lista [X, Y, a]
    lista2 = cons(Compound('b', []), cons(Z, cons(W, nil)))     # Lista [b, Z, W]
    W = Variable('W')                                           # Crea variable W
    print("\n=== Ejemplo 5 ===")                                # Encabezado ejemplo
    print(f"Unificar: {lista1} con {lista2}")                   # Muestra listas a unificar
    result = unify(lista1, lista2)                              # Intenta unificación
    print(pretty_print_substitution(result))                     # Muestra resultado

if __name__ == "__main__":                                      # Si se ejecuta como script principal
    print("=== Sistema de Unificación Lógica ===")              # Mensaje de inicio
    ejemplos_unificacion()                                      # Ejecuta ejemplos de unificación
