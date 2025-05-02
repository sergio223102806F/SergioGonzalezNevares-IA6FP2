# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 16:26:20 2025

@author: elvin
"""

"""
Implementación de Lógica Temporal Lineal (LTL) con operadores temporales

Este código define:
1. Estructuras para fórmulas temporales (◯, ◊, □, U)
2. Modelos de tiempo lineal (trazas temporales)
3. Evaluador semántico (verdad de fórmulas en instantes temporales)
"""

from typing import Union, List, Dict, Set
from enum import Enum, auto

# =============================================================================
# 1. DEFINICIÓN DE FÓRMULAS TEMPORALES
# =============================================================================

class TemporalOperator(Enum):
    """Operadores temporales básicos"""
    NEXT = auto()      # ◯ (próximo)
    EVENTUALLY = auto() # ◊ (eventualmente)
    ALWAYS = auto()    # □ (siempre)
    UNTIL = auto()     # U (hasta)

Formula = Union['Atom', 'Not', 'And', 'Or', 'Implication', 'TemporalFormula']

class Atom:
    """Proposición atómica (ej. 'llueve', 'p')"""
    def __init__(self, name: str):
        self.name = name
    
    def __repr__(self):
        return self.name

class Not:
    """Negación lógica (¬φ)"""
    def __init__(self, formula: Formula):
        self.formula = formula
    
    def __repr__(self):
        return f"¬{self.formula}"

class And:
    """Conjunción lógica (φ ∧ ψ)"""
    def __init__(self, left: Formula, right: Formula):
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"({self.left} ∧ {self.right})"

class Or:
    """Disyunción lógica (φ ∨ ψ)"""
    def __init__(self, left: Formula, right: Formula):
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"({self.left} ∨ {self.right})"

class Implication:
    """Implicación lógica (φ → ψ)"""
    def __init__(self, antecedent: Formula, consequent: Formula):
        self.antecedent = antecedent
        self.consequent = consequent
    
    def __repr__(self):
        return f"({self.antecedent} → {self.consequent})"

class TemporalFormula:
    """Fórmula con operador temporal"""
    def __init__(self, operator: TemporalOperator, *formulas: Formula):
        self.operator = operator
        self.formulas = formulas  # Fórmulas afectadas por el operador
    
    def __repr__(self):
        op_symbol = {
            TemporalOperator.NEXT: "◯",
            TemporalOperator.EVENTUALLY: "◊",
            TemporalOperator.ALWAYS: "□",
            TemporalOperator.UNTIL: "U"
        }[self.operator]
        
        if self.operator == TemporalOperator.UNTIL:
            return f"({self.formulas[0]} {op_symbol} {self.formulas[1]})"
        return f"{op_symbol}{self.formulas[0]}"

# =============================================================================
# 2. MODELOS TEMPORALES (TRACE)
# =============================================================================

class TemporalModel:
    """
    Modelo temporal basado en trazas lineales.
    
    Componentes:
    - states: Lista de estados (cada estado es un conjunto de átomos verdaderos)
    - current_time: Instante temporal actual (índice en states)
    """
    
    def __init__(self, states: List[Set[Atom]]):
        self.states = states
        self.current_time = 0
    
    def evaluate(self, formula: Formula, time: int = None) -> bool:
        """
        Evalúa una fórmula temporal en un instante dado.
        
        Args:
            formula: Fórmula a evaluar
            time: Instante temporal (None = usa current_time)
            
        Returns:
            bool: True si la fórmula es verdadera en ese instante
        """
        if time is None:
            time = self.current_time
        
        # Caso base: átomo
        if isinstance(formula, Atom):
            return formula in self.states[time]
        
        # Operadores lógicos clásicos
        elif isinstance(formula, Not):
            return not self.evaluate(formula.formula, time)
        elif isinstance(formula, And):
            return (self.evaluate(formula.left, time) and 
                    self.evaluate(formula.right, time))
        elif isinstance(formula, Or):
            return (self.evaluate(formula.left, time) or 
                    self.evaluate(formula.right, time))
        elif isinstance(formula, Implication):
            return ((not self.evaluate(formula.antecedent, time)) or 
                    self.evaluate(formula.consequent, time))
        
        # Operadores temporales
        elif isinstance(formula, TemporalFormula):
            # ◯φ (Próximo): φ debe cumplirse en el siguiente estado
            if formula.operator == TemporalOperator.NEXT:
                return time + 1 < len(self.states) and self.evaluate(formula.formulas[0], time + 1)
            
            # ◊φ (Eventualmente): φ debe cumplirse en algún estado futuro
            elif formula.operator == TemporalOperator.EVENTUALLY:
                return any(self.evaluate(formula.formulas[0], t) for t in range(time, len(self.states)))
            
            # □φ (Siempre): φ debe cumplirse en todos los estados futuros
            elif formula.operator == TemporalOperator.ALWAYS:
                return all(self.evaluate(formula.formulas[0], t) for t in range(time, len(self.states)))
            
            # φ U ψ (Hasta): φ debe cumplirse hasta que ψ se haga verdadero
            elif formula.operator == TemporalOperator.UNTIL:
                phi, psi = formula.formulas
                for t in range(time, len(self.states)):
                    if self.evaluate(psi, t):
                        return True
                    if not self.evaluate(phi, t):
                        return False
                return False
        
        raise ValueError(f"Fórmula no reconocida: {formula}")

# =============================================================================
# 3. EJEMPLOS DE USO
# =============================================================================

def ejemplo_alarma():
    """Ejemplo: 'Si la alarma suena, eventualmente alguien la apagará'"""
    # Definir átomos
    alarma = Atom("alarma")
    apagada = Atom("apagada")
    
    # Crear traza temporal
    states = [
        {alarma},        # t0: alarma activada
        {alarma},        # t1: sigue sonando
        {alarma, apagada}, # t2: alguien la apaga
        {apagada}        # t3: permanece apagada
    ]
    
    model = TemporalModel(states)
    
    # Fórmula: alarma → ◊apagada
    formula = Implication(alarma, TemporalFormula(TemporalOperator.EVENTUALLY, apagada))
    
    # Evaluar en cada instante
    print("\nEvaluación de 'alarma → ◊apagada':")
    for t in range(len(states)):
        model.current_time = t
        print(f"En t={t}: {model.evaluate(formula)}")

def ejemplo_reactivo():
    """Ejemplo: 'El sistema siempre reacciona dentro de 2 pasos'"""
    estimulo = Atom("estimulo")
    respuesta = Atom("respuesta")
    
    states = [
        {estimulo},       # t0: estímulo
        {},               # t1: procesando
        {respuesta},      # t2: respuesta
        {},               # t3: inactivo
        {estimulo},       # t4: nuevo estímulo
        {respuesta}       # t5: respuesta rápida
    ]
    
    model = TemporalModel(states)
    
    # Fórmula: □(estimulo → ◯◯respuesta)
    formula = TemporalFormula(
        TemporalOperator.ALWAYS,
        Implication(
            estimulo,
            TemporalFormula(TemporalOperator.NEXT,
                TemporalFormula(TemporalOperator.NEXT, respuesta)
        )
    )
    
    print("\nEvaluación de '□(estimulo → ◯◯respuesta)':")
    for t in range(len(states)):
        model.current_time = t
        print(f"En t={t}: {model.evaluate(formula)}")

if __name__ == "__main__":
    print("=== DEMOSTRACIÓN DE LÓGICA TEMPORAL ===")
    ejemplo_alarma()
    ejemplo_reactivo()