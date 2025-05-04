"""
INDUCCIÓN GRAMATICAL AUTOMÁTICA - 
----------------------------------------------------------
Sistema que aprende gramáticas formales a partir de ejemplos positivos de un lenguaje,
utilizando el algoritmo de inducción gramatical OSTIA (Onward Subsequential Transducer Inference Algorithm).
"""

# ============ IMPORTACIONES ============
from typing import List, Dict, Tuple, Set, Optional
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum, auto
import random

# ============ DEFINICIÓN DE TIPOS ============
class GrammarType(Enum):
    """Tipos de gramáticas que pueden generarse"""
    REGULAR = auto()      # Gramáticas regulares
    CONTEXT_FREE = auto() # Gramáticas libres de contexto

@dataclass
class Production:
    """Producción gramatical A -> α"""
    lhs: str       # Lado izquierdo (non-terminal)
    rhs: List[str] # Lado derecho (terminales y non-terminales)

@dataclass
class Grammar:
    """Estructura para gramáticas inducidas"""
    type: GrammarType
    non_terminals: Set[str]
    terminals: Set[str]
    productions: List[Production]
    start_symbol: str

# ============ ALGORITMO OSTIA (SIMPLIFICADO) ============
class OSTIA:
    """Implementación simplificada del algoritmo OSTIA para inducción gramatical"""
    
    def __init__(self):
        self.state_counter = 0
        self.transitions = defaultdict(dict)
        self.final_states = set()
    
    def induce_grammar(self, examples: List[List[str]]) -> Grammar:
        """
        Induce una gramática a partir de ejemplos positivos
        
        Args:
            examples: Lista de secuencias de terminales (ejemplos positivos)
            
        Returns:
            Gramática inducida
        """
        # Paso 1: Construir el árbol de prefijos comunes
        self._build_prefix_tree(examples)
        
        # Paso 2: Generalizar mediante fusión de estados
        self._merge_states()
        
        # Paso 3: Convertir a gramática regular
        return self._to_grammar()
    
    def _build_prefix_tree(self, examples: List[List[str]]) -> None:
        """Construye un árbol de prefijos a partir de ejemplos"""
        initial_state = self._new_state()
        
        for example in examples:
            current_state = initial_state
            for symbol in example:
                if symbol not in self.transitions[current_state]:
                    new_state = self._new_state()
                    self.transitions[current_state][symbol] = new_state
                current_state = self.transitions[current_state][symbol]
            self.final_states.add(current_state)
    
    def _merge_states(self) -> None:
        """Fusiona estados compatibles para generalizar"""
        # Versión simplificada - en OSTIA real se usa un algoritmo más complejo
        states = list(self.transitions.keys())
        
        for i, state1 in enumerate(states):
            for state2 in states[i+1:]:
                if self._are_states_compatible(state1, state2):
                    self._merge_two_states(state1, state2)
    
    def _are_states_compatible(self, s1: int, s2: int) -> bool:
        """Determina si dos estados pueden fusionarse"""
        # Simplificación: estados con transiciones similares
        return (self.transitions[s1].keys() == self.transitions[s2].keys() and
                (s1 in self.final_states) == (s2 in self.final_states))
    
    def _merge_two_states(self, s1: int, s2: int) -> None:
        """Fusiona dos estados en el autómata"""
        # Reemplazar todas las transiciones a s2 con s1
        for state, transitions in self.transitions.items():
            for symbol, target in transitions.items():
                if target == s2:
                    self.transitions[state][symbol] = s1
        
        # Fusionar transiciones
        self.transitions[s1].update(self.transitions[s2])
        del self.transitions[s2]
        
        # Manejar estados finales
        if s2 in self.final_states:
            self.final_states.remove(s2)
    
    def _to_grammar(self) -> Grammar:
        """Convierte el autómata a una gramática regular"""
        non_terminals = {f"q{state}" for state in self.transitions}
        terminals = set()
        productions = []
        
        # Convertir transiciones a producciones
        for state, transitions in self.transitions.items():
            for symbol, target in transitions.items():
                productions.append(Production(
                    lhs=f"q{state}",
                    rhs=[symbol, f"q{target}"]
                ))
                terminals.add(symbol)
        
        # Producciones para estados finales
        for state in self.final_states:
            productions.append(Production(
                lhs=f"q{state}",
                rhs=["ε"]  # Producción epsilon
            ))
        
        return Grammar(
            type=GrammarType.REGULAR,
            non_terminals=non_terminals,
            terminals=terminals,
            productions=productions,
            start_symbol="q0"
        )
    
    def _new_state(self) -> int:
        """Genera un nuevo estado para el autómata"""
        self.state_counter += 1
        return self.state_counter - 1

# ============ INDUCCIÓN DE GRAMÁTICAS LIBRES DE CONTEXTO ============
class CFGInducer:
    """Algoritmo para inducir gramáticas libres de contexto"""
    
    def induce_grammar(self, examples: List[List[str]]) -> Grammar:
        """
        Induce una gramática libre de contexto usando enfoque de k-testable
        
        Args:
            examples: Ejemplos positivos del lenguaje
            
        Returns:
            Gramática libre de contexto inducida
        """
        # Paso 1: Extraer patrones frecuentes
        patterns = self._extract_patterns(examples)
        
        # Paso 2: Generar producciones
        productions = self._generate_productions(patterns)
        
        # Paso 3: Construir gramática
        terminals = self._extract_terminals(examples)
        non_terminals = {prod.lhs for prod in productions}
        
        return Grammar(
            type=GrammarType.CONTEXT_FREE,
            non_terminals=non_terminals,
            terminals=terminals,
            productions=productions,
            start_symbol="S"
        )
    
    def _extract_patterns(self, examples: List[List[str]]) -> Dict[str, int]:
        """Extrae patrones frecuentes de los ejemplos"""
        patterns = defaultdict(int)
        k = 2  # Longitud de patrones a extraer
        
        for example in examples:
            for i in range(len(example) - k + 1):
                pattern = tuple(example[i:i+k])
                patterns[pattern] += 1
        
        return patterns
    
    def _generate_productions(self, patterns: Dict[str, int]) -> List[Production]:
        """Genera producciones basadas en patrones frecuentes"""
        productions = []
        threshold = 2  # Mínimo de ocurrencias para considerar un patrón
        
        # Producción inicial
        productions.append(Production("S", ["A"]))
        
        # Generar producciones para patrones frecuentes
        for pattern, count in patterns.items():
            if count >= threshold:
                # Crear no terminal para el patrón
                nt_name = f"{pattern[0]}_{pattern[1]}"
                
                # Producción S -> aB
                productions.append(Production(
                    "S",
                    [pattern[0], nt_name]
                ))
                
                # Producción B -> b
                productions.append(Production(
                    nt_name,
                    [pattern[1]]
                ))
        
        # Producciones para cadenas cortas
        productions.append(Production("S", ["A", "B"]))
        productions.append(Production("A", ["a"]))
        productions.append(Production("B", ["b"]))
        
        return productions
    
    def _extract_terminals(self, examples: List[List[str]]) -> Set[str]:
        """Extrae símbolos terminales de los ejemplos"""
        terminals = set()
        for example in examples:
            for symbol in example:
                terminals.add(symbol)
        return terminals

# ============ EJEMPLO DE USO ============
def generate_examples(grammar: Grammar, n: int = 10) -> List[List[str]]:
    """Genera ejemplos positivos a partir de una gramática (para simulación)"""
    examples = []
    
    for _ in range(n):
        example = []
        current_symbols = [grammar.start_symbol]
        
        while current_symbols:
            symbol = current_symbols.pop(0)
            
            # Buscar producción aleatoria para el símbolo
            productions = [p for p in grammar.productions if p.lhs == symbol]
            if not productions:
                continue
                
            chosen_prod = random.choice(productions)
            
            for s in chosen_prod.rhs:
                if s in grammar.terminals:
                    example.append(s)
                else:
                    current_symbols.append(s)
        
        examples.append(example)
    
    return examples

def print_grammar(grammar: Grammar) -> None:
    """Muestra una gramática de forma legible"""
    print(f"\nGramática {grammar.type.name}:")
    print(f"Símbolo inicial: {grammar.start_symbol}")
    print("Producciones:")
    
    # Agrupar producciones por lhs
    productions_by_lhs = defaultdict(list)
    for prod in grammar.productions:
        productions_by_lhs[prod.lhs].append(" ".join(prod.rhs))
    
    for lhs, rhs_list in productions_by_lhs.items():
        rhs_str = " | ".join(rhs_list)
        print(f"  {lhs} -> {rhs_str}")

if __name__ == "__main__":
    print("=== DEMOSTRACIÓN DE INDUCCIÓN GRAMATICAL ===")
    
    # Gramática de ejemplo para generar datos de entrenamiento
    target_grammar = Grammar(
        type=GrammarType.REGULAR,
        non_terminals={"S", "A", "B"},
        terminals={"a", "b"},
        productions=[
            Production("S", ["a", "A"]),
            Production("A", ["b", "B"]),
            Production("B", ["a", "A"]),
            Production("B", ["b"])
        ],
        start_symbol="S"
    )
    
    # Generar ejemplos positivos
    examples = generate_examples(target_grammar, 20)
    print("\nEjemplos generados:")
    for i, example in enumerate(examples[:5], 1):
        print(f"Ejemplo {i}: {' '.join(example)}")
    print("... (mostrando 5 de 20)")
    
    # Inducir gramática regular
    print("\nInduciendo gramática regular con OSTIA:")
    ostia = OSTIA()
    induced_regular = ostia.induce_grammar(examples)
    print_grammar(induced_regular)
    
    # Inducir gramática libre de contexto
    print("\nInduciendo gramática libre de contexto:")
    cfg_inducer = CFGInducer()
    induced_cfg = cfg_inducer.induce_grammar(examples)
    print_grammar(induced_cfg)