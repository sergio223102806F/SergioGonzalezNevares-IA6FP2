"""
INDUCCIÓN GRAMATICAL AUTOMÁTICA - 
----------------------------------------------------------
Sistema que aprende gramáticas formales a partir de ejemplos positivos de un lenguaje,
utilizando el algoritmo de inducción gramatical OSTIA (Onward Subsequential Transducer Inference Algorithm).
"""

# ============ IMPORTACIONES ============
from typing import List, Dict, Tuple, Set, Optional  # Tipos para type hints
from collections import defaultdict                  # Diccionario con valores por defecto
from dataclasses import dataclass                   # Para clases de datos
from enum import Enum, auto                         # Para enumeraciones
import random                                       # Para generación aleatoria

# ============ DEFINICIÓN DE TIPOS ============
class GrammarType(Enum):                            # Enumeración de tipos de gramática
    """Tipos de gramáticas que pueden generarse"""
    REGULAR = auto()      # Gramáticas regulares      # Tipo regular
    CONTEXT_FREE = auto() # Gramáticas libres de contexto # Tipo libre de contexto

@dataclass
class Production:                                   # Clase para producciones
    """Producción gramatical A -> α"""
    lhs: str       # Lado izquierdo (non-terminal)   # Símbolo no terminal
    rhs: List[str] # Lado derecho (terminales y non-terminales) # Parte derecha

@dataclass
class Grammar:                                     # Clase para gramáticas
    """Estructura para gramáticas inducidas"""
    type: GrammarType                              # Tipo de gramática
    non_terminals: Set[str]                        # Conjunto de no terminales
    terminals: Set[str]                            # Conjunto de terminales
    productions: List[Production]                  # Lista de producciones
    start_symbol: str                              # Símbolo inicial

# ============ ALGORITMO OSTIA (SIMPLIFICADO) ============
class OSTIA:                                       # Implementación de OSTIA
    """Implementación simplificada del algoritmo OSTIA para inducción gramatical"""
    
    def __init__(self):                            # Constructor
        self.state_counter = 0                     # Contador de estados
        self.transitions = defaultdict(dict)       # Transiciones del autómata
        self.final_states = set()                  # Estados finales
    
    def induce_grammar(self, examples: List[List[str]]) -> Grammar: # Método principal
        """
        Induce una gramática a partir de ejemplos positivos
        
        Args:
            examples: Lista de secuencias de terminales (ejemplos positivos) # Ejemplos
            
        Returns:
            Gramática inducida                     # Gramática resultante
        """
        # Paso 1: Construir el árbol de prefijos comunes
        self._build_prefix_tree(examples)          # Construir árbol
        
        # Paso 2: Generalizar mediante fusión de estados
        self._merge_states()                       # Fusionar estados
        
        # Paso 3: Convertir a gramática regular
        return self._to_grammar()                  # Convertir a gramática
    
    def _build_prefix_tree(self, examples: List[List[str]]) -> None: # Construir árbol
        """Construye un árbol de prefijos a partir de ejemplos"""
        initial_state = self._new_state()          # Crear estado inicial
        
        for example in examples:                   # Para cada ejemplo
            current_state = initial_state          # Comenzar en estado inicial
            for symbol in example:                # Para cada símbolo
                if symbol not in self.transitions[current_state]: # Si no hay transición
                    new_state = self._new_state()  # Crear nuevo estado
                    self.transitions[current_state][symbol] = new_state # Añadir transición
                current_state = self.transitions[current_state][symbol] # Mover al siguiente estado
            self.final_states.add(current_state)   # Marcar como estado final
    
    def _merge_states(self) -> None:               # Fusión de estados
        """Fusiona estados compatibles para generalizar"""
        # Versión simplificada - en OSTIA real se usa un algoritmo más complejo
        states = list(self.transitions.keys())     # Obtener todos los estados
        
        for i, state1 in enumerate(states):        # Comparar cada par de estados
            for state2 in states[i+1:]:
                if self._are_states_compatible(state1, state2): # Si son compatibles
                    self._merge_two_states(state1, state2) # Fusionarlos
    
    def _are_states_compatible(self, s1: int, s2: int) -> bool: # Compatibilidad
        """Determina si dos estados pueden fusionarse"""
        # Simplificación: estados con transiciones similares
        return (self.transitions[s1].keys() == self.transitions[s2].keys() and # Mismas transiciones
                (s1 in self.final_states) == (s2 in self.final_states)) # Mismo estado final
    
    def _merge_two_states(self, s1: int, s2: int) -> None: # Fusión de dos estados
        """Fusiona dos estados en el autómata"""
        # Reemplazar todas las transiciones a s2 con s1
        for state, transitions in self.transitions.items(): # Para cada estado
            for symbol, target in transitions.items(): # Para cada transición
                if target == s2:                   # Si apunta a s2
                    self.transitions[state][symbol] = s1 # Redirigir a s1
        
        # Fusionar transiciones
        self.transitions[s1].update(self.transitions[s2]) # Combinar transiciones
        del self.transitions[s2]                   # Eliminar s2
        
        # Manejar estados finales
        if s2 in self.final_states:               # Si s2 era final
            self.final_states.remove(s2)          # Eliminarlo
    
    def _to_grammar(self) -> Grammar:             # Conversión a gramática
        """Convierte el autómata a una gramática regular"""
        non_terminals = {f"q{state}" for state in self.transitions} # Crear no terminales
        terminals = set()                         # Inicializar terminales
        productions = []                          # Inicializar producciones
        
        # Convertir transiciones a producciones
        for state, transitions in self.transitions.items(): # Para cada estado
            for symbol, target in transitions.items(): # Para cada transición
                productions.append(Production(    # Crear producción
                    lhs=f"q{state}",              # No terminal origen
                    rhs=[symbol, f"q{target}"]    # Terminal + no terminal destino
                ))
                terminals.add(symbol)             # Añadir símbolo terminal
        
        # Producciones para estados finales
        for state in self.final_states:           # Para cada estado final
            productions.append(Production(        # Crear producción epsilon
                lhs=f"q{state}",                  # No terminal
                rhs=["ε"]                         # Producción vacía
            ))
        
        return Grammar(                           # Retornar gramática
            type=GrammarType.REGULAR,             # Tipo regular
            non_terminals=non_terminals,          # No terminales
            terminals=terminals,                  # Terminales
            productions=productions,              # Producciones
            start_symbol="q0"                     # Símbolo inicial
        )
    
    def _new_state(self) -> int:                  # Nuevo estado
        """Genera un nuevo estado para el autómata"""
        self.state_counter += 1                   # Incrementar contador
        return self.state_counter - 1             # Retornar nuevo estado

# ============ INDUCCIÓN DE GRAMÁTICAS LIBRES DE CONTEXTO ============
class CFGInducer:                                 # Inductor de CFG
    """Algoritmo para inducir gramáticas libres de contexto"""
    
    def induce_grammar(self, examples: List[List[str]]) -> Grammar: # Método principal
        """
        Induce una gramática libre de contexto usando enfoque de k-testable
        
        Args:
            examples: Ejemplos positivos del lenguaje # Ejemplos de entrada
            
        Returns:
            Gramática libre de contexto inducida    # Gramática resultante
        """
        # Paso 1: Extraer patrones frecuentes
        patterns = self._extract_patterns(examples) # Extraer patrones
        
        # Paso 2: Generar producciones
        productions = self._generate_productions(patterns) # Generar producciones
        
        # Paso 3: Construir gramática
        terminals = self._extract_terminals(examples) # Extraer terminales
        non_terminals = {prod.lhs for prod in productions} # Obtener no terminales
        
        return Grammar(                           # Retornar gramática
            type=GrammarType.CONTEXT_FREE,        # Tipo libre de contexto
            non_terminals=non_terminals,          # No terminales
            terminals=terminals,                  # Terminales
            productions=productions,              # Producciones
            start_symbol="S"                      # Símbolo inicial
        )
    
    def _extract_patterns(self, examples: List[List[str]]) -> Dict[str, int]: # Extracción
        """Extrae patrones frecuentes de los ejemplos"""
        patterns = defaultdict(int)              # Diccionario de patrones
        k = 2  # Longitud de patrones a extraer  # Tamaño de patrones
        
        for example in examples:                 # Para cada ejemplo
            for i in range(len(example) - k + 1): # Para cada posición
                pattern = tuple(example[i:i+k])  # Obtener patrón
                patterns[pattern] += 1           # Incrementar conteo
        
        return patterns                          # Retornar patrones
    
    def _generate_productions(self, patterns: Dict[str, int]) -> List[Production]: # Generación
        """Genera producciones basadas en patrones frecuentes"""
        productions = []                          # Lista de producciones
        threshold = 2  # Mínimo de ocurrencias para considerar un patrón # Umbral
        
        # Producción inicial
        productions.append(Production("S", ["A"])) # Producción S -> A
        
        # Generar producciones para patrones frecuentes
        for pattern, count in patterns.items():  # Para cada patrón
            if count >= threshold:               # Si supera el umbral
                # Crear no terminal para el patrón
                nt_name = f"{pattern[0]}_{pattern[1]}" # Nombre compuesto
                
                # Producción S -> aB
                productions.append(Production(    # Añadir producción
                    "S",                         # Símbolo inicial
                    [pattern[0], nt_name]         # Parte derecha
                ))
                
                # Producción B -> b
                productions.append(Production(    # Añadir producción
                    nt_name,                     # No terminal
                    [pattern[1]]                  # Terminal
                ))
        
        # Producciones para cadenas cortas
        productions.append(Production("S", ["A", "B"])) # S -> AB
        productions.append(Production("A", ["a"]))     # A -> a
        productions.append(Production("B", ["b"]))     # B -> b
        
        return productions                          # Retornar producciones
    
    def _extract_terminals(self, examples: List[List[str]]) -> Set[str]: # Extracción
        """Extrae símbolos terminales de los ejemplos"""
        terminals = set()                         # Conjunto de terminales
        for example in examples:                  # Para cada ejemplo
            for symbol in example:                # Para cada símbolo
                terminals.add(symbol)             # Añadir al conjunto
        return terminals                          # Retornar terminales

# ============ EJEMPLO DE USO ============
def generate_examples(grammar: Grammar, n: int = 10) -> List[List[str]]: # Generación
    """Genera ejemplos positivos a partir de una gramática (para simulación)"""
    examples = []                                # Lista de ejemplos
    
    for _ in range(n):                           # Generar n ejemplos
        example = []                             # Ejemplo actual
        current_symbols = [grammar.start_symbol] # Comenzar con símbolo inicial
        
        while current_symbols:                   # Mientras haya símbolos
            symbol = current_symbols.pop(0)      # Tomar primer símbolo
            
            # Buscar producción aleatoria para el símbolo
            productions = [p for p in grammar.productions if p.lhs == symbol] # Buscar producciones
            if not productions:                  # Si no hay producciones
                continue                         # Continuar
                
            chosen_prod = random.choice(productions) # Elegir producción aleatoria
            
            for s in chosen_prod.rhs:            # Para cada símbolo en parte derecha
                if s in grammar.terminals:       # Si es terminal
                    example.append(s)             # Añadir a ejemplo
                else:                            # Si es no terminal
                    current_symbols.append(s)     # Añadir para expandir
        
        examples.append(example)                 # Añadir ejemplo a lista
    
    return examples                              # Retornar ejemplos

def print_grammar(grammar: Grammar) -> None:     # Impresión de gramática
    """Muestra una gramática de forma legible"""
    print(f"\nGramática {grammar.type.name}:")   # Mostrar tipo
    print(f"Símbolo inicial: {grammar.start_symbol}") # Mostrar símbolo inicial
    print("Producciones:")                       # Encabezado
    
    # Agrupar producciones por lhs
    productions_by_lhs = defaultdict(list)       # Diccionario de producciones
    for prod in grammar.productions:             # Para cada producción
        productions_by_lhs[prod.lhs].append(" ".join(prod.rhs)) # Agrupar
    
    for lhs, rhs_list in productions_by_lhs.items(): # Para cada no terminal
        rhs_str = " | ".join(rhs_list)           # Unir producciones
        print(f"  {lhs} -> {rhs_str}")          # Mostrar producción

if __name__ == "__main__":                       # Punto de entrada
    print("=== DEMOSTRACIÓN DE INDUCCIÓN GRAMATICAL ===") # Título
    
    # Gramática de ejemplo para generar datos de entrenamiento
    target_grammar = Grammar(                    # Crear gramática objetivo
        type=GrammarType.REGULAR,                # Tipo regular
        non_terminals={"S", "A", "B"},           # No terminales
        terminals={"a", "b"},                    # Terminales
        productions=[                            # Producciones
            Production("S", ["a", "A"]),         # S -> aA
            Production("A", ["b", "B"]),         # A -> bB
            Production("B", ["a", "A"]),         # B -> aA
            Production("B", ["b"])               # B -> b
        ],
        start_symbol="S"                         # Símbolo inicial
    )
    
    # Generar ejemplos positivos
    examples = generate_examples(target_grammar, 20) # Generar 20 ejemplos
    print("\nEjemplos generados:")               # Encabezado
    for i, example in enumerate(examples[:5], 1): # Mostrar primeros 5
        print(f"Ejemplo {i}: {' '.join(example)}") # Mostrar ejemplo
    print("... (mostrando 5 de 20)")             # Indicar truncamiento
    
    # Inducir gramática regular
    print("\nInduciendo gramática regular con OSTIA:") # Encabezado
    ostia = OSTIA()                              # Crear instancia OSTIA
    induced_regular = ostia.induce_grammar(examples) # Inducir gramática
    print_grammar(induced_regular)               # Mostrar gramática
    
    # Inducir gramática libre de contexto
    print("\nInduciendo gramática libre de contexto:") # Encabezado
    cfg_inducer = CFGInducer()                    # Crear instancia CFGInducer
    induced_cfg = cfg_inducer.induce_grammar(examples) # Inducir gramática
    print_grammar(induced_cfg)                    # Mostrar gramática