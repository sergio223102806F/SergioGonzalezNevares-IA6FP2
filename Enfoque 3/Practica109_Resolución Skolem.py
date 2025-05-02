# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 16:24:09 2025

@author: elvin
"""

"""
Este código implementa el proceso de skolemización, una técnica utilizada en lógica 
para eliminar cuantificadores existenciales mediante la introducción de funciones de Skolem.
La skolemización es un paso esencial en la conversión a forma normal clausal para la resolución en lógica de primer orden.
"""

from typing import Dict, List, Optional, Set, Union
from collections import defaultdict

# ==============================================
# Definición de tipos para términos y fórmulas lógicas
# ==============================================

# Tipo genérico para términos lógicos (variables, constantes, funciones)
Term = Union['Variable', 'Constant', 'Function', 'Predicate']

class Variable:
    """Representa una variable en lógica de primer orden"""
    def __init__(self, name: str):
        self.name = name  # Nombre de la variable (ej. 'X', 'Y')
        
    def __repr__(self):
        return f"Variable('{self.name}')"  # Representación para debugging
    
    def __eq__(self, other):
        # Dos variables son iguales si tienen el mismo nombre
        return isinstance(other, Variable) and self.name == other.name
    
    def __hash__(self):
        # Permite usar variables en diccionarios y conjuntos
        return hash(self.name)

class Constant:
    """Representa una constante en lógica de primer orden"""
    def __init__(self, name: str):
        self.name = name  # Nombre de la constante (ej. 'a', 'b')
        
    def __repr__(self):
        return f"Constant('{self.name}')"
    
    def __eq__(self, other):
        # Dos constantes son iguales si tienen el mismo nombre
        return isinstance(other, Constant) and self.name == other.name

class Function:
    """Representa una función en lógica de primer orden"""
    def __init__(self, name: str, args: List[Term]):
        self.name = name    # Nombre de la función (ej. 'f', 'g')
        self.args = args    # Lista de argumentos de la función
        
    def __repr__(self):
        args_str = ", ".join(map(str, self.args))
        return f"{self.name}({args_str})"  # Representación como f(X, Y)
    
    def __eq__(self, other):
        # Dos funciones son iguales si tienen mismo nombre y argumentos
        return (isinstance(other, Function) and 
                self.name == other.name and 
                self.args == other.args)

class Predicate:
    """Representa un predicado en lógica de primer orden"""
    def __init__(self, name: str, args: List[Term]):
        self.name = name    # Nombre del predicado (ej. 'P', 'Q')
        self.args = args     # Lista de argumentos del predicado
        
    def __repr__(self):
        args_str = ", ".join(map(str, self.args))
        return f"{self.name}({args_str})"  # Representación como P(X, Y)
    
    def __eq__(self, other):
        # Dos predicados son iguales si tienen mismo nombre y argumentos
        return (isinstance(other, Predicate) and 
                self.name == other.name and 
                self.args == other.args)

# ==============================================
# Definición de cuantificadores y fórmulas
# ==============================================

class Quantifier:
    """Clase base abstracta para cuantificadores"""
    pass

class Forall(Quantifier):
    """Cuantificador universal ∀"""
    def __init__(self, var: Variable, formula: 'Formula'):
        self.var = var       # Variable cuantificada
        self.formula = formula  # Fórmula dentro del alcance del cuantificador
        
    def __repr__(self):
        return f"∀{self.var}. {self.formula}"  # Representación como ∀X. P(X)

class Exists(Quantifier):
    """Cuantificador existencial ∃"""
    def __init__(self, var: Variable, formula: 'Formula'):
        self.var = var       # Variable cuantificada
        self.formula = formula  # Fórmula dentro del alcance del cuantificador
        
    def __repr__(self):
        return f"∃{self.var}. {self.formula}"  # Representación como ∃X. P(X)

class Formula:
    """Clase base abstracta para fórmulas lógicas"""
    pass

class AtomicFormula(Formula):
    """Fórmula atómica (predicado)"""
    def __init__(self, predicate: Predicate):
        self.predicate = predicate  # Predicado que forma la fórmula atómica
        
    def __repr__(self):
        return str(self.predicate)  # Representación como P(X)

class Negation(Formula):
    """Negación de una fórmula"""
    def __init__(self, formula: Formula):
        self.formula = formula  # Fórmula negada
        
    def __repr__(self):
        return f"¬{self.formula}"  # Representación como ¬P(X)

class Connective(Formula):
    """Clase base abstracta para conectivos lógicos"""
    pass

class And(Connective):
    """Conjunción lógica ∧"""
    def __init__(self, left: Formula, right: Formula):
        self.left = left    # Fórmula izquierda
        self.right = right  # Fórmula derecha
        
    def __repr__(self):
        return f"({self.left} ∧ {self.right})"  # Representación como (P ∧ Q)

class Or(Connective):
    """Disyunción lógica ∨"""
    def __init__(self, left: Formula, right: Formula):
        self.left = left    # Fórmula izquierda
        self.right = right  # Fórmula derecha
        
    def __repr__(self):
        return f"({self.left} ∨ {self.right})"  # Representación como (P ∨ Q)

class Implication(Connective):
    """Implicación →"""
    def __init__(self, left: Formula, right: Formula):
        self.left = left    # Premisa
        self.right = right  # Conclusión
        
    def __repr__(self):
        return f"({self.left} → {self.right})"  # Representación como (P → Q)

# ==============================================
# Implementación del algoritmo de Skolemización
# ==============================================

class Skolemizer:
    """
    Clase que implementa el algoritmo de skolemización para convertir fórmulas
    de lógica de primer orden en forma normal skolem (sin cuantificadores existenciales).
    """
    
    def __init__(self):
        self.skolem_counter = 0  # Contador para generar nombres únicos de funciones Skolem
        self.quantified_vars = []  # Lista de variables cuantificadas (para seguimiento)
        
    def skolemize(self, formula: Formula) -> Formula:
        """
        Método principal que inicia el proceso de skolemización.
        
        Args:
            formula: Fórmula lógica a skolemizar
            
        Returns:
            Fórmula skolemizada (sin cuantificadores existenciales)
        """
        return self._skolemize(formula)
        
    def _skolemize(self, formula: Formula, universal_vars: List[Variable] = None) -> Formula:
        """
        Función recursiva que procesa cada tipo de fórmula para aplicar skolemización.
        
        Args:
            formula: Fórmula o subfórmula a procesar
            universal_vars: Lista de variables universales en el contexto actual
            
        Returns:
            Fórmula procesada con skolemización aplicada
        """
        # Inicializar lista de variables universales si es la primera llamada
        if universal_vars is None:
            universal_vars = []
            
        # Caso base: fórmula atómica (no necesita procesamiento)
        if isinstance(formula, AtomicFormula):
            return formula
            
        # Negación: skolemizar la subfórmula
        elif isinstance(formula, Negation):
            return Negation(self._skolemize(formula.formula, universal_vars))
            
        # Conjunción: skolemizar ambas partes
        elif isinstance(formula, And):
            return And(
                self._skolemize(formula.left, universal_vars),
                self._skolemize(formula.right, universal_vars)
            )
            
        # Disyunción: skolemizar ambas partes
        elif isinstance(formula, Or):
            return Or(
                self._skolemize(formula.left, universal_vars),
                self._skolemize(formula.right, universal_vars)
            )
            
        # Implicación: skolemizar ambas partes
        elif isinstance(formula, Implication):
            return Implication(
                self._skolemize(formula.left, universal_vars),
                self._skolemize(formula.right, universal_vars)
            )
            
        # Cuantificador universal: añadir variable al contexto y skolemizar el cuerpo
        elif isinstance(formula, Forall):
            new_universal_vars = universal_vars + [formula.var]
            return Forall(formula.var, self._skolemize(formula.formula, new_universal_vars))
            
        # Cuantificador existencial: reemplazar con función de Skolem
        elif isinstance(formula, Exists):
            # Crear una nueva función de Skolem con las variables universales actuales como argumentos
            skolem_func = self._create_skolem_function(universal_vars)
            
            # Reemplazar la variable existencial con la función de Skolem en la subfórmula
            substituted = self._substitute(formula.formula, formula.var, skolem_func)
            
            # Continuar skolemizando el resultado (sin el cuantificador existencial)
            return self._skolemize(substituted, universal_vars)
            
        else:
            raise ValueError(f"Tipo de fórmula no soportado: {type(formula)}")
    
    def _create_skolem_function(self, universal_vars: List[Variable]) -> Function:
        """
        Crea una nueva función de Skolem basada en las variables universales actuales.
        
        Args:
            universal_vars: Lista de variables universales en el contexto actual
            
        Returns:
            Nueva función de Skolem con las variables universales como argumentos
        """
        self.skolem_counter += 1  # Incrementar contador para nombre único
        skolem_name = f"sk{self.skolem_counter}"  # Generar nombre (sk1, sk2, ...)
        
        if universal_vars:
            # Si hay variables universales, crear función con esos argumentos
            return Function(skolem_name, universal_vars)
        else:
            # Si no hay variables universales, crear constante de Skolem (función 0-aria)
            return Function(skolem_name, [])
    
    def _substitute(self, formula: Formula, var: Variable, replacement: Term) -> Formula:
        """
        Sustituye todas las ocurrencias de una variable en una fórmula por un término.
        
        Args:
            formula: Fórmula donde realizar la sustitución
            var: Variable a reemplazar
            replacement: Término que reemplazará a la variable
            
        Returns:
            Fórmula con la sustitución aplicada
        """
        # Fórmula atómica: sustituir en los argumentos del predicado
        if isinstance(formula, AtomicFormula):
            new_args = [replacement if arg == var else arg for arg in formula.predicate.args]
            return AtomicFormula(Predicate(formula.predicate.name, new_args))
            
        # Negación: sustituir en la subfórmula
        elif isinstance(formula, Negation):
            return Negation(self._substitute(formula.formula, var, replacement))
            
        # Conjunción: sustituir en ambas partes
        elif isinstance(formula, And):
            return And(
                self._substitute(formula.left, var, replacement),
                self._substitute(formula.right, var, replacement)
            )
            
        # Disyunción: sustituir en ambas partes
        elif isinstance(formula, Or):
            return Or(
                self._substitute(formula.left, var, replacement),
                self._substitute(formula.right, var, replacement)
            )
            
        # Implicación: sustituir en ambas partes
        elif isinstance(formula, Implication):
            return Implication(
                self._substitute(formula.left, var, replacement),
                self._substitute(formula.right, var, replacement)
            )
            
        # Cuantificador: sustituir solo si no es la variable ligada
        elif isinstance(formula, Quantifier):
            if formula.var == var:
                return formula  # No sustituir variables ligadas con el mismo nombre
            else:
                new_formula = self._substitute(formula.formula, var, replacement)
                if isinstance(formula, Forall):
                    return Forall(formula.var, new_formula)
                else:
                    return Exists(formula.var, new_formula)
        else:
            raise ValueError(f"Tipo de fórmula no soportado: {type(formula)}")

# ==============================================
# Ejemplos de uso y demostración
# ==============================================

def ejemplo_skolemizacion():
    """
    Función que demuestra el proceso de skolemización con varios ejemplos.
    """
    skolemizer = Skolemizer()
    
    # Ejemplo 1: Fórmula simple con cuantificador existencial
    X = Variable('X')
    Y = Variable('Y')
    P = Predicate('P', [X, Y])
    formula1 = Exists(Y, AtomicFormula(P))
    
    print("\n=== Ejemplo 1 ===")
    print("Fórmula original:", formula1)
    skolemized = skolemizer.skolemize(formula1)
    print("Fórmula skolemizada:", skolemized)
    
    # Ejemplo 2: Fórmula con cuantificador universal seguido de existencial
    formula2 = Forall(X, Exists(Y, AtomicFormula(P)))
    
    print("\n=== Ejemplo 2 ===")
    print("Fórmula original:", formula2)
    skolemized = skolemizer.skolemize(formula2)
    print("Fórmula skolemizada:", skolemized)
    
    # Ejemplo 3: Fórmula compleja con múltiples cuantificadores anidados
    Z = Variable('Z')
    Q = Predicate('Q', [X, Y, Z])
    formula3 = Exists(X, Forall(Y, Exists(Z, AtomicFormula(Q))))
    
    print("\n=== Ejemplo 3 ===")
    print("Fórmula original:", formula3)
    skolemized = skolemizer.skolemize(formula3)
    print("Fórmula skolemizada:", skolemized)
    
    # Ejemplo 4: Fórmula con cuantificador existencial en contexto de universal
    R = Predicate('R', [X, Y])
    formula4 = Forall(X, 
                    Or(
                        Negation(AtomicFormula(R)),
                        Exists(Y, AtomicFormula(R))
                    ))
    
    print("\n=== Ejemplo 4 ===")
    print("Fórmula original:", formula4)
    skolemized = skolemizer.skolemize(formula4)
    print("Fórmula skolemizada:", skolemized)

if __name__ == "__main__":
    print("=== Skolemización en Lógica de Primer Orden ===")
    ejemplo_skolemizacion()