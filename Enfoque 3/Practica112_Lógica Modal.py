# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 16:26:20 2025

@author: elvin
"""

"""
Implementación de Lógica Modal con semántica de Kripke

Este código define:
1. Estructuras para fórmulas modales (□, ◇)
2. Modelos de Kripke (mundos posibles, relación de accesibilidad)
3. Evaluador semántico (verdad de fórmulas en mundos)
"""

from typing import Union, Dict, Set

# =============================================================================
# 1. DEFINICIÓN DE FÓRMULAS MODALES
# =============================================================================

# Tipo genérico para fórmulas
Formula = Union['Atom', 'Not', 'And', 'Or', 'Implication', 'Box', 'Diamond']

class Atom:
    """Representa una proposición atómica (ej. 'llueve', 'p')"""
    def __init__(self, name: str):
        self.name = name  # Nombre del átomo (string)
    
    def __repr__(self):
        return self.name  # Representación como string

class Not:
    """Negación lógica (¬φ)"""
    def __init__(self, formula: Formula):
        self.formula = formula  # Subfórmula a negar
    
    def __repr__(self):
        return f"¬{self.formula}"  # Representación como ¬φ

class And:
    """Conjunción lógica (φ ∧ ψ)"""
    def __init__(self, left: Formula, right: Formula):
        self.left = left    # Parte izquierda de la conjunción
        self.right = right  # Parte derecha
    
    def __repr__(self):
        return f"({self.left} ∧ {self.right})"  # Representación como (φ ∧ ψ)

class Or:
    """Disyunción lógica (φ ∨ ψ)"""
    def __init__(self, left: Formula, right: Formula):
        self.left = left    # Parte izquierda
        self.right = right  # Parte derecha
    
    def __repr__(self):
        return f"({self.left} ∨ {self.right})"  # Representación como (φ ∨ ψ)

class Implication:
    """Implicación lógica (φ → ψ)"""
    def __init__(self, antecedent: Formula, consequent: Formula):
        self.antecedent = antecedent  # Premisa (φ)
        self.consequent = consequent  # Conclusión (ψ)
    
    def __repr__(self):
        return f"({self.antecedent} → {self.consequent})"  # Representación como (φ → ψ)

class Box:
    """Operador de necesidad (□φ) - 'Es necesario que φ'"""
    def __init__(self, formula: Formula):
        self.formula = formula  # Fórmula dentro del operador
    
    def __repr__(self):
        return f"□{self.formula}"  # Representación como □φ

class Diamond:
    """Operador de posibilidad (◇φ) - 'Es posible que φ'"""
    def __init__(self, formula: Formula):
        self.formula = formula  # Fórmula dentro del operador
    
    def __repr__(self):
        return f"◇{self.formula}"  # Representación como ◇φ

# =============================================================================
# 2. MODELOS DE KRIPKE (SEMÁNTICA)
# =============================================================================

class KripkeModel:
    """
    Modelo de Kripke para evaluar fórmulas modales.
    
    Componentes:
    - worlds: Conjunto de mundos posibles (ej. 'w1', 'w2')
    - relations: Relación de accesibilidad entre mundos (R ⊆ W × W)
    - valuations: Asignación de verdad para átomos en cada mundo (V: W → 2^Atoms)
    """
    
    def __init__(self):
        self.worlds: Set[str] = set()                # Conjunto de mundos
        self.relations: Dict[str, Set[str]] = {}     # Relaciones wRw'
        self.valuations: Dict[str, Set[Atom]] = {}   # Valuación por mundo
    
    def add_world(self, world: str):
        """Añade un mundo al modelo (si no existe)"""
        if world not in self.worlds:
            self.worlds.add(world)
            self.relations[world] = set()    # Inicializa relaciones
            self.valuations[world] = set()   # Inicializa valuación
    
    def add_relation(self, from_world: str, to_world: str):
        """Establece que 'from_world' accede a 'to_world'"""
        self.add_world(from_world)  # Asegura que existe el mundo origen
        self.add_world(to_world)    # Asegura que existe el mundo destino
        self.relations[from_world].add(to_world)  # Añade relación
    
    def set_valuation(self, world: str, atom: Atom):
        """Marca un átomo como verdadero en un mundo específico"""
        self.add_world(world)  # Asegura que el mundo existe
        self.valuations[world].add(atom)  # Añade átomo a valuación
    
    def is_true_in_world(self, formula: Formula, world: str) -> bool:
        """
        Evalúa si una fórmula es verdadera en un mundo dado.
        
        Args:
            formula: Fórmula a evaluar
            world: Mundo donde evaluar
            
        Returns:
            bool: True si la fórmula es verdadera en el mundo
        """
        # Caso base: átomo
        if isinstance(formula, Atom):
            return formula in self.valuations.get(world, set())
        
        # Negación (¬φ)
        elif isinstance(formula, Not):
            return not self.is_true_in_world(formula.formula, world)
        
        # Conjunción (φ ∧ ψ)
        elif isinstance(formula, And):
            return (self.is_true_in_world(formula.left, world) and 
                    self.is_true_in_world(formula.right, world))
        
        # Disyunción (φ ∨ ψ)
        elif isinstance(formula, Or):
            return (self.is_true_in_world(formula.left, world) or 
                   self.is_true_in_world(formula.right, world))
        
        # Implicación (φ → ψ)
        elif isinstance(formula, Implication):
            return ((not self.is_true_in_world(formula.antecedent, world)) or 
                    self.is_true_in_world(formula.consequent, world))
        
        # Necesidad (□φ)
        elif isinstance(formula, Box):
            # □φ es verdadero en w si φ es verdadero en todos los mundos accesibles desde w
            for accessible_world in self.relations.get(world, set()):
                if not self.is_true_in_world(formula.formula, accessible_world):
                    return False  # Si falla en alguno, □φ es falso
            return True  # φ se cumple en todos los mundos accesibles
        
        # Posibilidad (◇φ)
        elif isinstance(formula, Diamond):
            # ◇φ es verdadero en w si φ es verdadero en al menos un mundo accesible
            for accessible_world in self.relations.get(world, set()):
                if self.is_true_in_world(formula.formula, accessible_world):
                    return True  # Basta un mundo donde φ sea verdadero
            return False  # φ no se cumple en ningún mundo accesible
        
        else:
            raise ValueError(f"Tipo de fórmula no soportado: {type(formula)}")

# =============================================================================
# 3. EJEMPLOS DE USO
# =============================================================================

def ejemplo_lluvia():
    """Ejemplo: 'Si es necesario que llueva, entonces el suelo está mojado'"""
    # Crear modelo
    model = KripkeModel()
    
    # Definir mundos
    model.add_world("w1")  # Mundo donde llueve
    model.add_world("w2")  # Mundo donde no llueve
    
    # Establecer relaciones (w1 accede a w2 y viceversa)
    model.add_relation("w1", "w2")
    model.add_relation("w2", "w1")
    
    # Definir átomos
    llueve = Atom("llueve")
    suelo_mojado = Atom("suelo_mojado")
    
    # Asignar valuaciones:
    model.set_valuation("w1", llueve)          # En w1, llueve
    model.set_valuation("w1", suelo_mojado)    # En w1, suelo mojado
    model.set_valuation("w2", suelo_mojado)    # En w2, suelo mojado (por otras razones)
    
    # Fórmula: □(llueve → suelo_mojado)
    formula = Box(Implication(llueve, suelo_mojado))
    
    # Evaluar en todos los mundos
    print("\nEvaluación de □(llueve → suelo_mojado):")
    for world in model.worlds:
        print(f"- En {world}: {model.is_true_in_world(formula, world)}")

if __name__ == "__main__":
    print("=== DEMOSTRACIÓN DE LÓGICA MODAL ===")
    ejemplo_lluvia()