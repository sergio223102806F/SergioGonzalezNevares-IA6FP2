# -*- coding: utf-8 -*-                                                     # Define la codificación de caracteres del archivo como UTF-8
"""
Created on Sun Apr 27 16:26:20 2025                                         # Indica la fecha y hora de creación del archivo
                                                                           #
@author: elvin                                                              # Define el autor del archivo
"""

"""
Implementación de Lógica Modal con semántica de Kripke

Este código define:
1. Estructuras para fórmulas modales (□, ◇)
2. Modelos de Kripke (mundos posibles, relación de accesibilidad)
3. Evaluador semántico (verdad de fórmulas en mundos)
"""

from typing import Union, Dict, Set                                        # Importa tipos para anotaciones de tipo

# ============================================================================= # Separador de sección
# 1. DEFINICIÓN DE FÓRMULAS MODALES                                        # Título de la sección
# ============================================================================= # Separador de sección

# Tipo genérico para fórmulas                                               # Comentario para el tipo genérico de fórmulas
Formula = Union['Atom', 'Not', 'And', 'Or', 'Implication', 'Box', 'Diamond'] # Define un tipo llamado Formula que puede ser cualquiera de las clases de fórmulas

class Atom:                                                            # Define una clase llamada Atom
    """Representa una proposición atómica (ej. 'llueve', 'p')"""         # Documentación de la clase Atom
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

class Box:                                                             # Define una clase llamada Box
    """Operador de necesidad (□φ) - 'Es necesario que φ'"""           # Documentación de la clase Box
    def __init__(self, formula: Formula):                                 # Define el constructor de la clase
        self.formula = formula                                          # Inicializa la fórmula dentro del operador
        
    def __repr__(self):                                                    # Define la representación en string del objeto
        return f"□{self.formula}"                                       # Retorna la representación como □φ

class Diamond:                                                         # Define una clase llamada Diamond
    """Operador de posibilidad (◇φ) - 'Es posible que φ'"""           # Documentación de la clase Diamond
    def __init__(self, formula: Formula):                                 # Define el constructor de la clase
        self.formula = formula                                          # Inicializa la fórmula dentro del operador
        
    def __repr__(self):                                                    # Define la representación en string del objeto
        return f"◇{self.formula}"                                       # Retorna la representación como ◇φ

# ============================================================================= # Separador de sección
# 2. MODELOS DE KRIPKE (SEMÁNTICA)                                        # Título de la sección
# ============================================================================= # Separador de sección

class KripkeModel:                                                     # Define una clase llamada KripkeModel
    """
    Modelo de Kripke para evaluar fórmulas modales.                    # Documentación de la clase KripkeModel
    
    Componentes:
    - worlds: Conjunto de mundos posibles (ej. 'w1', 'w2')
    - relations: Relación de accesibilidad entre mundos (R ⊆ W × W)
    - valuations: Asignación de verdad para átomos en cada mundo (V: W → 2^Atoms)
    """
    
    def __init__(self):                                                     # Define el constructor de la clase
        self.worlds: Set[str] = set()                                      # Inicializa un conjunto para los mundos posibles
        self.relations: Dict[str, Set[str]] = {}                           # Inicializa un diccionario para la relación de accesibilidad
        self.valuations: Dict[str, Set[Atom]] = {}                          # Inicializa un diccionario para la asignación de verdad
        
    def add_world(self, world: str):                                       # Define el método para añadir un mundo
        """Añade un mundo al modelo (si no existe)"""                       # Documentación del método add_world
        if world not in self.worlds:                                      # Si el mundo no existe en el conjunto de mundos
            self.worlds.add(world)                                         # Añade el mundo al conjunto de mundos
            self.relations[world] = set()                                 # Inicializa un conjunto vacío para las relaciones del mundo
            self.valuations[world] = set()                                # Inicializa un conjunto vacío para la valuación del mundo
            
    def add_relation(self, from_world: str, to_world: str):                # Define el método para añadir una relación
        """Establece que 'from_world' accede a 'to_world'"""               # Documentación del método add_relation
        self.add_world(from_world)                                        # Asegura que el mundo origen existe
        self.add_world(to_world)                                          # Asegura que el mundo destino existe
        self.relations[from_world].add(to_world)                           # Añade el mundo destino al conjunto de mundos accesibles desde el mundo origen
        
    def set_valuation(self, world: str, atom: Atom):                      # Define el método para establecer la valuación
        """Marca un átomo como verdadero en un mundo específico"""          # Documentación del método set_valuation
        self.add_world(world)                                             # Asegura que el mundo existe
        self.valuations[world].add(atom)                                   # Añade el átomo al conjunto de átomos verdaderos en el mundo
        
    def is_true_in_world(self, formula: Formula, world: str) -> bool:      # Define el método para evaluar la verdad de una fórmula en un mundo
        """
        Evalúa si una fórmula es verdadera en un mundo dado.              # Documentación del método is_true_in_world
        
        Args:
            formula: Fórmula a evaluar
            world: Mundo donde evaluar
            
        Returns:
            bool: True si la fórmula es verdadera en el mundo
        """
        # Caso base: átomo                                                 # Comentario para el caso base
        if isinstance(formula, Atom):                                     # Si la fórmula es un átomo
            return formula in self.valuations.get(world, set())           # Retorna True si el átomo está en la valuación del mundo, False en caso contrario
        
        # Negación (¬φ)                                                  # Comentario para la negación
        elif isinstance(formula, Not):                                    # Si la fórmula es una negación
            return not self.is_true_in_world(formula.formula, world)      # Retorna la negación del valor de verdad de la subfórmula en el mundo
        
        # Conjunción (φ ∧ ψ)                                               # Comentario para la conjunción
        elif isinstance(formula, And):                                    # Si la fórmula es una conjunción
            return (self.is_true_in_world(formula.left, world) and        # Retorna True si ambas subfórmulas son verdaderas en el mundo
                    self.is_true_in_world(formula.right, world))
        
        # Disyunción (φ ∨ ψ)                                                # Comentario para la disyunción
        elif isinstance(formula, Or):                                     # Si la fórmula es una disyunción
            return (self.is_true_in_world(formula.left, world) or         # Retorna True si alguna de las subfórmulas es verdadera en el mundo
                    self.is_true_in_world(formula.right, world))
        
        # Implicación (φ → ψ)                                              # Comentario para la implicación
        elif isinstance(formula, Implication):                           # Si la fórmula es una implicación
            return ((not self.is_true_in_world(formula.antecedent, world)) or # Retorna True si el antecedente es falso o el consecuente es verdadero en el mundo
                    self.is_true_in_world(formula.consequent, world))
        
        # Necesidad (□φ)                                                 # Comentario para la necesidad
        elif isinstance(formula, Box):                                    # Si la fórmula es una necesidad
            # □φ es verdadero en w si φ es verdadero en todos los mundos accesibles desde w # Comentario explicando la semántica de la necesidad
            for accessible_world in self.relations.get(world, set()):    # Itera sobre todos los mundos accesibles desde el mundo actual
                if not self.is_true_in_world(formula.formula, accessible_world): # Si la fórmula no es verdadera en algún mundo accesible
                    return False                                          # Retorna False
            return True                                                   # Si la fórmula es verdadera en todos los mundos accesibles, retorna True
        
        # Posibilidad (◇φ)                                               # Comentario para la posibilidad
        elif isinstance(formula, Diamond):                                # Si la fórmula es una posibilidad
            # ◇φ es verdadero en w si φ es verdadero en al menos un mundo accesible # Comentario explicando la semántica de la posibilidad
            for accessible_world in self.relations.get(world, set()):    # Itera sobre todos los mundos accesibles desde el mundo actual
                if self.is_true_in_world(formula.formula, accessible_world): # Si la fórmula es verdadera en algún mundo accesible
                    return True                                           # Retorna True
            return False                                                  # Si la fórmula no es verdadera en ningún mundo accesible, retorna False
        
        else:                                                          # Si el tipo de fórmula no es soportado
            raise ValueError(f"Tipo de fórmula no soportado: {type(formula)}") # Lanza un error

# ============================================================================= # Separador de sección
# 3. EJEMPLOS DE USO                                                      # Título de la sección
# ============================================================================= # Separador de sección

def ejemplo_lluvia():                                                    # Define la función para el ejemplo de la lluvia
    """Ejemplo: 'Si es necesario que llueva, entonces el suelo está mojado'""" # Documentación de la función ejemplo_lluvia
    # Crear modelo                                                      # Comentario para la creación del modelo
    model = KripkeModel()                                               # Crea una instancia de la clase KripkeModel
    
    # Definir mundos                                                     # Comentario para la definición de mundos
    model.add_world("w1")                                                # Añade el mundo w1
    model.add_world("w2")                                                # Añade el mundo w2
    
    # Establecer relaciones (w1 accede a w2 y viceversa)               # Comentario para establecer las relaciones
    model.add_relation("w1", "w2")                                       # Añade la relación de accesibilidad de w1 a w2
    model.add_relation("w2", "w1")                                       # Añade la relación de accesibilidad de w2 a w1
    
    # Definir átomos                                                     # Comentario para la definición de átomos
    llueve = Atom("llueve")                                              # Crea un átomo llamado "llueve"
    suelo_mojado = Atom("suelo_mojado")                                  # Crea un átomo llamado "suelo_mojado"
    
    # Asignar valuaciones:                                               # Comentario para la asignación de valuaciones
    model.set_valuation("w1", llueve)                                   # El átomo "llueve" es verdadero en w1
    model.set_valuation("w1", suelo_mojado)                              # El átomo "suelo_mojado" es verdadero en w1
    model.set_valuation("w2", suelo_mojado)                              # El átomo "suelo_mojado" es verdadero en w2
    
    # Fórmula: □(llueve → suelo_mojado)                                  # Comentario para la definición de la fórmula
    formula = Box(Implication(llueve, suelo_mojado))                   # Crea la fórmula modal □(llueve → suelo_mojado)
    
    # Evaluar en todos los mundos                                        # Comentario para la evaluación en todos los mundos
    print("\nEvaluación de □(llueve → suelo_mojado):")                 # Imprime un encabezado
    for world in model.worlds:                                         # Itera sobre los mundos del modelo
        print(f"- En {world}: {model.is_true_in_world(formula, world)}") # Imprime el valor de verdad de la fórmula en cada mundo

if __name__ == "__main__":                                                 # Bloque de código que se ejecuta cuando el script se llama directamente
    print("=== DEMOSTRACIÓN DE LÓGICA MODAL ===")                      # Imprime un encabezado
    ejemplo_lluvia()                                                       # Llama a la función del ejemplo de la lluvia
```