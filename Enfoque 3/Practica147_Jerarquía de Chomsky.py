"""
JERARQUÍA DE CHOMSKY - 
----------------------------------------------
Este código implementa las 4 clases de gramáticas formales 
de la Jerarquía de Chomsky con verificadores para cada tipo.
"""

# ============ IMPORTACIONES ============
from typing import Dict, List, Set, Tuple
from enum import Enum, auto

# ============ DEFINICIONES DE TIPOS ============
# Símbolos se representan como strings
Symbol = str

# Producción: (cabeza, cuerpo)
Production = Tuple[Symbol, List[Symbol]]

# Gramática: tupla con (V, Σ, P, S)
Grammar = Tuple[Set[Symbol], Set[Symbol], List[Production], Symbol]

# ============ CLASIFICACIÓN DE GRAMÁTICAS ============
class GrammarType(Enum):
    """Enumeración de los tipos de gramáticas según Chomsky"""
    TYPE_0 = auto()   # Sin restricciones
    TYPE_1 = auto()   # Sensibles al contexto
    TYPE_2 = auto()   # Libres de contexto
    TYPE_3 = auto()   # Regulares

# ============ VERIFICADORES PARA CADA TIPO ============
def is_type_3(grammar: Grammar) -> bool:
    """
    Verifica si es una gramática Tipo 3 (Regular)
    
    Criterios:
    - Producciones de la forma:
      A → aB | a | ε (derecho-lineal)
      A → Ba | a | ε (izquierdo-lineal)
    
    Args:
        grammar: Gramática a verificar
        
    Returns:
        bool: True si cumple con Tipo 3
    """
    V, Σ, P, S = grammar
    
    for head, body in P:
        # Caso ε-production (solo permitido si head es S)
        if not body:
            if head != S:
                return False
            continue
            
        # Verifica estructura de producciones
        if len(body) == 1:  # A → a
            if body[0] not in Σ:
                return False
        elif len(body) == 2:  # A → aB o A → Ba
            # Derecho-lineal (aB) o izquierdo-lineal (Ba)
            if not ((body[0] in Σ and body[1] in V) or 
                   (body[0] in V and body[1] in Σ)):
                return False
        else:
            return False
            
    return True

def is_type_2(grammar: Grammar) -> bool:
    """
    Verifica si es una gramática Tipo 2 (Libre de contexto)
    
    Criterios:
    - Producciones de la forma A → α
    - |α| ≥ 0
    - Solo un símbolo no terminal en la cabeza
    
    Args:
        grammar: Gramática a verificar
        
    Returns:
        bool: True si cumple con Tipo 2
    """
    V, Σ, P, S = grammar
    
    for head, body in P:
        # La cabeza debe ser un único no terminal
        if head not in V:
            return False
            
        # El cuerpo puede ser cualquier cadena de símbolos
        for symbol in body:
            if symbol not in V and symbol not in Σ:
                return False
                
    return True

def is_type_1(grammar: Grammar) -> bool:
    """
    Verifica si es una gramática Tipo 1 (Sensible al contexto)
    
    Criterios:
    - Producciones de la forma αAβ → αγβ
    - |γ| ≥ 1 (no contractivas)
    - Excepción: S → ε permitida si S no aparece en cuerpos
    
    Args:
        grammar: Gramática a verificar
        
    Returns:
        bool: True si cumple con Tipo 1
    """
    V, Σ, P, S = grammar
    
    # Verifica si S → ε es la única producción especial
    s_epsilon = False
    for head, body in P:
        if head == S and not body:
            s_epsilon = True
            continue
            
        # Verifica |γ| ≥ 1
        if len(body) < len(head):
            return False
            
        # Verifica que la producción mantenga contexto
        # (implementación simplificada)
        if len(head) == 1 and head not in V:
            return False
            
    # Si existe S → ε, verifica que S no aparezca en cuerpos
    if s_epsilon:
        for _, body in P:
            if S in body:
                return False
                
    return True

def is_type_0(grammar: Grammar) -> bool:
    """
    Verifica si es una gramática Tipo 0 (Sin restricciones)
    
    Criterios:
    - Solo requiere que la cabeza tenga al menos un no terminal
    
    Args:
        grammar: Gramática a verificar
        
    Returns:
        bool: True si es Tipo 0 (siempre verdadero si es gramática válida)
    """
    V, _, P, _ = grammar
    
    for head, _ in P:
        # Al menos un símbolo en la cabeza
        if not head:
            return False
            
    return True

# ============ CLASIFICADOR COMPLETO ============
def classify_grammar(grammar: Grammar) -> GrammarType:
    """
    Determina el tipo de gramática según la Jerarquía de Chomsky
    
    Args:
        grammar: Gramática a clasificar
        
    Returns:
        GrammarType: El tipo más restrictivo que cumple
    """
    if is_type_3(grammar):
        return GrammarType.TYPE_3
    elif is_type_2(grammar):
        return GrammarType.TYPE_2
    elif is_type_1(grammar):
        return GrammarType.TYPE_1
    elif is_type_0(grammar):
        return GrammarType.TYPE_0
    else:
        raise ValueError("Gramática no válida")

# ============ EJEMPLOS DE GRAMÁTICAS ============
def create_sample_grammar(grammar_num: int) -> Grammar:
    """
    Crea gramáticas de ejemplo para testing
    
    Args:
        grammar_num: Número de gramática (1-4)
        
    Returns:
        Grammar: Gramática de ejemplo
    """
    # Gramática Regular (Tipo 3)
    if grammar_num == 1:
        V = {'S', 'A'}
        Σ = {'a', 'b'}
        P = [('S', ['a', 'A']),
             ('A', ['b', 'S']),
             ('A', ['a'])]
        S = 'S'
    
    # Gramática Libre de Contexto (Tipo 2)
    elif grammar_num == 2:
        V = {'S'}
        Σ = {'a', 'b'}
        P = [('S', ['a', 'S', 'b']),
             ('S', [])]
        S = 'S'
    
    # Gramática Sensible al Contexto (Tipo 1)
    elif grammar_num == 3:
        V = {'S', 'B'}
        Σ = {'a', 'b', 'c'}
        P = [('S', ['a', 'B', 'c']),
             ('a', 'B', ['a', 'b']),
             ('B', ['b'])]
        S = 'S'
    
    # Gramática Sin Restricciones (Tipo 0)
    elif grammar_num == 4:
        V = {'S', 'A'}
        Σ = {'a', 'b'}
        P = [('S', ['A', 'A', 'A']),
             ('A', ['S']),
             ('S', ['a']),
             ('A', ['b'])]
        S = 'S'
    
    return (V, Σ, P, S)

# ============ FUNCIÓN PRINCIPAL ============
def main():
    """Demostración de la clasificación de gramáticas"""
    print("=== DEMOSTRACIÓN JERARQUÍA DE CHOMSKY ===")
    
    for i in range(1, 5):
        grammar = create_sample_grammar(i)
        grammar_type = classify_grammar(grammar)
        print(f"\nGramática {i}: {grammar_type.name}")
        
        # Mostrar producciones
        print("Producciones:")
        for prod in grammar[2]:
            print(f"{prod[0]} → {' '.join(prod[1]) if prod[1] else 'ε'}")

if __name__ == "__main__":
    main()
