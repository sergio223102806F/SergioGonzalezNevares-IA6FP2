"""
JERARQUÍA DE CHOMSKY -
----------------------------------------------
Este código implementa las 4 clases de gramáticas formales
de la Jerarquía de Chomsky con verificadores para cada tipo.
"""

# ============ IMPORTACIONES ============
from typing import Dict, List, Set, Tuple  # Importa tipos para anotación de tipos
from enum import Enum, auto  # Importa Enum para definir tipos de gramáticas

# ============ DEFINICIONES DE TIPOS ============
# Símbolos se representan como strings
Symbol = str  # Define el tipo Symbol como string

# Producción: (cabeza, cuerpo)
Production = Tuple[Symbol, List[Symbol]]  # Define el tipo Production como una tupla de un Symbol y una lista de Symbols

# Gramática: tupla con (V, Σ, P, S)
Grammar = Tuple[Set[Symbol], Set[Symbol], List[Production], Symbol]  # Define el tipo Grammar como una tupla de conjuntos de Symbols, una lista de Productions y un Symbol

# ============ CLASIFICACIÓN DE GRAMÁTICAS ============
class GrammarType(Enum):
    """Enumeración de los tipos de gramáticas según Chomsky"""
    TYPE_0 = auto()    # Sin restricciones
    TYPE_1 = auto()    # Sensibles al contexto
    TYPE_2 = auto()    # Libres de contexto
    TYPE_3 = auto()    # Regulares

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
    V, Σ, P, S = grammar  # Desempaqueta la gramática en sus componentes

    for head, body in P:  # Itera sobre cada producción de la gramática
        # Caso ε-production (solo permitido si head es S)
        if not body:  # Si el cuerpo de la producción está vacío (ε)
            if head != S:  # La cabeza debe ser el símbolo inicial S
                return False  # Si no es S, no es una gramática regular
            continue  # Pasa a la siguiente producción
        
        # Verifica estructura de producciones
        if len(body) == 1:  # A → a
            if body[0] not in Σ:  # El único símbolo del cuerpo debe ser un terminal
                return False  # Si no es un terminal, no es regular
        elif len(body) == 2:  # A → aB o A → Ba
            # Derecho-lineal (aB) o izquierdo-lineal (Ba)
            if not ((body[0] in Σ and body[1] in V) or  # Verifica si es aB
                    (body[0] in V and body[1] in Σ)):  # o Ba
                return False  # Si no cumple ninguna, no es regular
        else:
            return False  # Si la longitud del cuerpo no es 1 o 2, no es regular
            
    return True  # Si todas las producciones cumplen, es regular

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
    V, Σ, P, S = grammar  # Desempaqueta la gramática

    for head, body in P:  # Itera sobre las producciones
        # La cabeza debe ser un único no terminal
        if head not in V:  # Verifica que la cabeza sea un no terminal
            return False  # Si no lo es, no es libre de contexto
            
        # El cuerpo puede ser cualquier cadena de símbolos
        for symbol in body:  # Itera sobre los símbolos del cuerpo
            if symbol not in V and symbol not in Σ:  # Verifica que sean terminales o no terminales
                return False  # Si no lo son, no es libre de contexto
                
    return True  # Si todas las producciones cumplen, es libre de contexto

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
    V, Σ, P, S = grammar  # Desempaqueta la gramática
    
    # Verifica si S → ε es la única producción especial
    s_epsilon = False
    for head, body in P:  # Itera sobre las producciones
        if head == S and not body:  # Si es la producción S → ε
            s_epsilon = True
            continue  # Pasa a la siguiente producción
            
        # Verifica |γ| ≥ 1
        if len(body) < len(head):  # El cuerpo no puede ser más corto que la cabeza
            return False  # Si lo es, no es sensible al contexto
            
        # Verifica que la producción mantenga contexto
        # (implementación simplificada)
        if len(head) == 1 and head not in V:  # La cabeza debe contener al menos un no terminal.
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
    V, _, P, _ = grammar  # Desempaqueta la gramática, no necesita Σ ni S

    for head, _ in P:  # Itera sobre las producciones
        # Al menos un símbolo en la cabeza
        if not head:  # Verifica que la cabeza no esté vacía
            return False  # Si está vacía, la gramática no es válida
            
    return True  # Si la gramática llega a este punto, es de tipo 0

# ============ CLASIFICADOR COMPLETO ============
def classify_grammar(grammar: Grammar) -> GrammarType:
    """
    Determina el tipo de gramática según la Jerarquía de Chomsky

    Args:
        grammar: Gramática a clasificar

    Returns:
        GrammarType: El tipo más restrictivo que cumple
    """
    if is_type_3(grammar):  # Primero verifica si es Tipo 3
        return GrammarType.TYPE_3  # Si lo es, retorna Tipo 3
    elif is_type_2(grammar):  # Luego verifica si es Tipo 2
        return GrammarType.TYPE_2  # Si lo es, retorna Tipo 2
    elif is_type_1(grammar):  # Luego verifica si es Tipo 1
        return GrammarType.TYPE_1  # Si lo es, retorna Tipo 1
    elif is_type_0(grammar):  # Finalmente verifica si es Tipo 0
        return GrammarType.TYPE_0  # Si lo es, retorna Tipo 0
    else:
        raise ValueError("Gramática no válida")  # Si no cumple ningún tipo, lanza un error

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
        
    return (V, Σ, P, S)  # Retorna la gramática creada

# ============ FUNCIÓN PRINCIPAL ============
def main():
    """Demostración de la clasificación de gramáticas"""
    print("=== DEMOSTRACIÓN JERARQUÍA DE CHOMSKY ===")
    
    for i in range(1, 5):  # Itera sobre los números de gramática de 1 a 4
        grammar = create_sample_grammar(i)  # Crea una gramática de ejemplo
        grammar_type = classify_grammar(grammar)  # Clasifica la gramática
        print(f"\nGramática {i}: {grammar_type.name}")  # Imprime el tipo de la gramática
        
        # Mostrar producciones
        print("Producciones:")
        for prod in grammar[2]:  # Itera sobre las producciones de la gramática
            print(f"{prod[0]} → {' '.join(prod[1]) if prod[1] else 'ε'}")  # Imprime cada producción con formato

if __name__ == "__main__":
    main()  # Llama a la función principal si el script se ejecuta directamente

