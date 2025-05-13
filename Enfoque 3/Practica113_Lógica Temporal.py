# -*- coding: utf-8 -*-                                                     # Define la codificación de caracteres del archivo como UTF-8
"""
Created on Sun Apr 27 16:26:20 2025                                         # Indica la fecha y hora de creación del archivo
                                                                           #
@author: elvin                                                              # Define el autor del archivo
"""

"""
Implementación de Lógica Temporal Lineal (LTL) con operadores temporales

Este código define:
1. Estructuras para fórmulas temporales (◯, ◊, □, U)
2. Modelos de tiempo lineal (trazas temporales)
3. Evaluador semántico (verdad de fórmulas en instantes temporales)
"""

from typing import Union, List, Dict, Set                                        # Importa tipos para anotaciones de tipo
from enum import Enum, auto                                                   # Importa Enum y auto desde el módulo enum

# ============================================================================= # Separador de sección
# 1. DEFINICIÓN DE FÓRMULAS TEMPORALES                                        # Título de la sección
# ============================================================================= # Separador de sección

class TemporalOperator(Enum):                                               # Define una clase llamada TemporalOperator que hereda de Enum
    """Operadores temporales básicos"""                                     # Documentación de la clase TemporalOperator
    NEXT = auto()                                                          # Define el operador NEXT (◯) con un valor automático
    EVENTUALLY = auto()                                                    # Define el operador EVENTUALLY (◊) con un valor automático
    ALWAYS = auto()                                                        # Define el operador ALWAYS (□) con un valor automático
    UNTIL = auto()                                                         # Define el operador UNTIL (U) con un valor automático

Formula = Union['Atom', 'Not', 'And', 'Or', 'Implication', 'TemporalFormula'] # Define un tipo llamado Formula que puede ser cualquiera de las clases de fórmulas

class Atom:                                                            # Define una clase llamada Atom
    """Proposición atómica (ej. 'llueve', 'p')"""                         # Documentación de la clase Atom
    def __init__(self, name: str):                                         # Define el constructor de la clase
        self.name = name                                                # Inicializa el nombre del átomo
        
    def __repr__(self):                                                    # Define la representación en string del objeto
        return self.name                                                 # Retorna el nombre del átomo

class Not:                                                             # Define una clase llamada Not
    """Negación lógica (¬φ)"""                                          # Documentación de la clase Not
    def __init__(self, formula: Formula):                                 # Define el constructor de la clase
        self.formula = formula                                          # Inicializa la subfórmula a negar
        
    def __repr__(self):                                                    # Define la representación en string del objeto
        return f"¬{self.formula}"                                       # Retorna la representación como ¬φ

class And:                                                             # Define una clase llamada And
    """Conjunción lógica (φ ∧ ψ)"""                                    # Documentación de la clase And
    def __init__(self, left: Formula, right: Formula):                     # Define el constructor de la clase
        self.left = left                                                  # Inicializa la parte izquierda de la conjunción
        self.right = right                                                # Inicializa la parte derecha
        
    def __repr__(self):                                                    # Define la representación en string del objeto
        return f"({self.left} ∧ {self.right})"                             # Retorna la representación como (φ ∧ ψ)

class Or:                                                              # Define una clase llamada Or
    """Disyunción lógica (φ ∨ ψ)"""                                     # Documentación de la clase Or
    def __init__(self, left: Formula, right: Formula):                     # Define el constructor de la clase
        self.left = left                                                  # Inicializa la parte izquierda
        self.right = right                                                # Inicializa la parte derecha
        
    def __repr__(self):                                                    # Define la representación en string del objeto
        return f"({self.left} ∨ {self.right})"                             # Retorna la representación como (φ ∨ ψ)

class Implication:                                                     # Define una clase llamada Implication
    """Implicación lógica (φ → ψ)"""                                    # Documentación de la clase Implication
    def __init__(self, antecedent: Formula, consequent: Formula):         # Define el constructor de la clase
        self.antecedent = antecedent                                      # Inicializa la premisa (φ)
        self.consequent = consequent                                      # Inicializa la conclusión (ψ)
        
    def __repr__(self):                                                    # Define la representación en string del objeto
        return f"({self.antecedent} → {self.consequent})"                 # Retorna la representación como (φ → ψ)

class TemporalFormula:                                                 # Define una clase llamada TemporalFormula
    """Fórmula con operador temporal"""                                  # Documentación de la clase TemporalFormula
    def __init__(self, operator: TemporalOperator, *formulas: Formula): # Define el constructor de la clase
        self.operator = operator                                        # Inicializa el operador temporal
        self.formulas = formulas                                        # Inicializa las fórmulas afectadas por el operador
        
    def __repr__(self):                                                    # Define la representación en string del objeto
        op_symbol = {                                                    # Define un diccionario para mapear operadores a símbolos
            TemporalOperator.NEXT: "◯",
            TemporalOperator.EVENTUALLY: "◊",
            TemporalOperator.ALWAYS: "□",
            TemporalOperator.UNTIL: "U"
        }[self.operator]                                                 # Obtiene el símbolo del operador actual
        
        if self.operator == TemporalOperator.UNTIL:                      # Si el operador es UNTIL
            return f"({self.formulas[0]} {op_symbol} {self.formulas[1]})" # Retorna la representación como (φ U ψ)
        return f"{op_symbol}{self.formulas[0]}"                             # Retorna la representación como ◯φ, ◊φ, □φ

# ============================================================================= # Separador de sección
# 2. MODELOS TEMPORALES (TRACE)                                           # Título de la sección
# ============================================================================= # Separador de sección

class TemporalModel:                                                     # Define una clase llamada TemporalModel
    """
    Modelo temporal basado en trazas lineales.                         # Documentación de la clase TemporalModel
    
    Componentes:
    - states: Lista de estados (cada estado es un conjunto de átomos verdaderos)
    - current_time: Instante temporal actual (índice en states)
    """
    
    def __init__(self, states: List[Set[Atom]]):                           # Define el constructor de la clase
        self.states = states                                              # Inicializa la lista de estados
        self.current_time = 0                                           # Inicializa el instante temporal actual a 0
        
    def evaluate(self, formula: Formula, time: int = None) -> bool:      # Define el método para evaluar una fórmula en un instante dado
        """
        Evalúa una fórmula temporal en un instante dado.                # Documentación del método evaluate
        
        Args:
            formula: Fórmula a evaluar
            time: Instante temporal (None = usa current_time)
            
        Returns:
            bool: True si la fórmula es verdadera en ese instante
        """
        if time is None:                                                  # Si no se proporciona un instante temporal
            time = self.current_time                                      # Usa el instante temporal actual
        
        # Caso base: átomo                                                 # Comentario para el caso base
        if isinstance(formula, Atom):                                     # Si la fórmula es un átomo
            return formula in self.states[time]                           # Retorna True si el átomo está en el conjunto de átomos del estado en el tiempo dado
        
        # Operadores lógicos clásicos                                      # Comentario para los operadores lógicos
        elif isinstance(formula, Not):                                    # Si la fórmula es una negación
            return not self.evaluate(formula.formula, time)              # Retorna la negación del valor de verdad de la subfórmula en el tiempo dado
        elif isinstance(formula, And):                                    # Si la fórmula es una conjunción
            return (self.evaluate(formula.left, time) and                # Retorna True si ambas subfórmulas son verdaderas en el tiempo dado
                    self.evaluate(formula.right, time))
        elif isinstance(formula, Or):                                     # Si la fórmula es una disyunción
            return (self.evaluate(formula.left, time) or                 # Retorna True si alguna de las subfórmulas es verdadera en el tiempo dado
                    self.evaluate(formula.right, time))
        elif isinstance(formula, Implication):                           # Si la fórmula es una implicación
            return ((not self.evaluate(formula.antecedent, time)) or     # Retorna True si el antecedente es falso o el consecuente es verdadero en el tiempo dado
                    self.evaluate(formula.consequent, time))
        
        # Operadores temporales                                            # Comentario para los operadores temporales
        elif isinstance(formula, TemporalFormula):                       # Si la fórmula es una fórmula temporal
            # ◯φ (Próximo): φ debe cumplirse en el siguiente estado      # Comentario para el operador NEXT
            if formula.operator == TemporalOperator.NEXT:                # Si el operador es NEXT
                return time + 1 < len(self.states) and self.evaluate(formula.formulas[0], time + 1) # Retorna True si hay un siguiente estado y φ es verdadero en él
            
            # ◊φ (Eventualmente): φ debe cumplirse en algún estado futuro # Comentario para el operador EVENTUALLY
            elif formula.operator == TemporalOperator.EVENTUALLY:          # Si el operador es EVENTUALLY
                return any(self.evaluate(formula.formulas[0], t) for t in range(time, len(self.states))) # Retorna True si φ es verdadero en algún estado desde el tiempo actual hasta el final
            
            # □φ (Siempre): φ debe cumplirse en todos los estados futuros  # Comentario para el operador ALWAYS
            elif formula.operator == TemporalOperator.ALWAYS:            # Si el operador es ALWAYS
                return all(self.evaluate(formula.formulas[0], t) for t in range(time, len(self.states))) # Retorna True si φ es verdadero en todos los estados desde el tiempo actual hasta el final
            
            # φ U ψ (Hasta): φ debe cumplirse hasta que ψ se haga verdadero # Comentario para el operador UNTIL
            elif formula.operator == TemporalOperator.UNTIL:             # Si el operador es UNTIL
                phi, psi = formula.formulas                             # Desempaqueta las subfórmulas φ y ψ
                for t in range(time, len(self.states)):                 # Itera sobre los estados desde el tiempo actual hasta el final
                    if self.evaluate(psi, t):                           # Si ψ es verdadero en el tiempo t
                        return True                                       # Retorna True
                    if not self.evaluate(phi, t):                       # Si φ no es verdadero en el tiempo t
                        return False                                      # Retorna False
                return False                                              # Si ψ nunca se hace verdadero, retorna False
        
        raise ValueError(f"Fórmula no reconocida: {formula}")           # Lanza un error si la fórmula no es reconocida

# ============================================================================= # Separador de sección
# 3. EJEMPLOS DE USO                                                      # Título de la sección
# ============================================================================= # Separador de sección

def ejemplo_alarma():                                                    # Define la función para el ejemplo de la alarma
    """Ejemplo: 'Si la alarma suena, eventualmente alguien la apagará'""" # Documentación de la función ejemplo_alarma
    # Definir átomos                                                     # Comentario para la definición de átomos
    alarma = Atom("alarma")                                              # Crea un átomo llamado "alarma"
    apagada = Atom("apagada")                                            # Crea un átomo llamado "apagada"
    
    # Crear traza temporal                                               # Comentario para la creación de la traza
    states = [                                                         # Define la lista de estados
        {alarma},                                                      # t0: alarma activada
        {alarma},                                                      # t1: sigue sonando
        {alarma, apagada},                                              # t2: alguien la apaga
        {apagada}                                                       # t3: permanece apagada
    ]
    
    model = TemporalModel(states)                                        # Crea un modelo temporal con la traza definida
    
    # Fórmula: alarma → ◊apagada                                        # Comentario para la definición de la fórmula
    formula = Implication(alarma, TemporalFormula(TemporalOperator.EVENTUALLY, apagada)) # Crea la fórmula LTL
    
    # Evaluar en cada instante                                          # Comentario para la evaluación en cada instante
    print("\nEvaluación de 'alarma → ◊apagada':")                      # Imprime un encabezado
    for t in range(len(states)):                                        # Itera sobre los instantes de tiempo
        model.current_time = t                                         # Establece el instante temporal actual
        print(f"En t={t}: {model.evaluate(formula)}")                   # Evalúa la fórmula en el instante actual e imprime el resultado

def ejemplo_reactivo():                                                  # Define la función para el ejemplo reactivo
    """Ejemplo: 'El sistema siempre reacciona dentro de 2 pasos'"""     # Documentación de la función ejemplo_reactivo
    estimulo = Atom("estimulo")                                          # Crea un átomo llamado "estimulo"
    respuesta = Atom("respuesta")                                        # Crea un átomo llamado "respuesta"
    
    states = [                                                         # Define la lista de estados
        {estimulo},                                                      # t0: estímulo
        {},                                                            # t1: procesando
        {respuesta},                                                     # t2: respuesta
        {},                                                            # t3: inactivo
        {estimulo},                                                      # t4: nuevo estímulo
        {respuesta}                                                      # t5: respuesta rápida
    ]
    
    model = TemporalModel(states)                                        # Crea un modelo temporal con la traza definida
    
    # Fórmula: □(estimulo → ◯◯respuesta)                               # Comentario para la definición de la fórmula
    formula = TemporalFormula(                                         # Crea la fórmula LTL
        TemporalOperator.ALWAYS,
        Implication(
            estimulo,
            TemporalFormula(TemporalOperator.NEXT,
                TemporalFormula(TemporalOperator.NEXT, respuesta)
            )
        )
    )
    
    print("\nEvaluación de '□(estimulo → ◯◯respuesta)':")             # Imprime un encabezado
    for t in range(len(states)):                                        # Itera sobre los instantes de tiempo
        model.current_time = t                                         # Establece el instante temporal actual
        print(f"En t={t}: {model.evaluate(formula)}")                   # Evalúa la fórmula en el instante actual e imprime el resultado

if __name__ == "__main__":                                                 # Bloque de código que se ejecuta cuando el script se llama directamente
    print("=== DEMOSTRACIÓN DE LÓGICA TEMPORAL ===")                      # Imprime un encabezado
    ejemplo_alarma()                                                       # Llama a la función del ejemplo de la alarma
    ejemplo_reactivo()                                                     # Llama a la función del ejemplo reactivo