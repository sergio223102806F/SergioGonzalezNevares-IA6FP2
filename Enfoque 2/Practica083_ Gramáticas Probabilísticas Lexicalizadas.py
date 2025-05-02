# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 18:47:36 2025

@author: elvin
"""

"""
Implementación de Gramáticas Probabilísticas Lexicalizadas (LPCFG)

Esta extensión de PCFG incorpora:
1. Información léxica en las producciones
2. Probabilidades dependientes de palabras específicas
3. Generación más realista basada en léxico
"""

import random
from collections import defaultdict

class LexicalizedPCFG:
    def __init__(self):
        """
        Inicializa una gramática LPCFG vacía
        
        Atributos:
            productions: Diccionario de producciones lexicalizadas
                        Formato: {(lhs, head): [((rhs, head_index), probability), ...]}
            lexicon: Diccionario de probabilidades léxicas
                     Formato: {(pos_tag, word): probability}
            start_symbol: Símbolo inicial de la gramática
        """
        self.productions = defaultdict(list)
        self.lexicon = defaultdict(float)
        self.start_symbol = None
        self.head_tags = {}  # Almacena qué POS tags pueden ser heads

    def add_head_tag(self, pos_tag):
        """
        Registra un POS tag como posible head (núcleo)
        
        Parámetros:
            pos_tag (str): Etiqueta gramatical que puede ser núcleo (ej. 'N', 'V')
        """
        self.head_tags[pos_tag] = True

    def add_production(self, lhs, rhs, head_index, probability):
        """
        Añade una producción lexicalizada a la gramática
        
        Parámetros:
            lhs (tuple): (símbolo no terminal, head)
            rhs (list): Lista de símbolos (terminales o no terminales)
            head_index (int): Índice en rhs que indica el head de la producción
            probability (float): Probabilidad de esta producción (0-1)
            
        Lanza:
            ValueError: Si los parámetros son inválidos
        """
        # Validaciones
        if not isinstance(lhs, tuple) or len(lhs) != 2:
            raise ValueError("lhs debe ser tupla (symbol, head)")
        if not isinstance(rhs, list):
            raise ValueError("rhs debe ser una lista")
        if not 0 <= head_index < len(rhs):
            raise ValueError("head_index fuera de rango")
        if not (0 <= probability <= 1):
            raise ValueError("Probabilidad debe estar entre 0 y 1")

        # Añadir producción
        self.productions[lhs].append(((tuple(rhs), head_index), probability))
        
        # Establecer símbolo inicial si es la primera producción
        if self.start_symbol is None:
            self.start_symbol = lhs

    def add_lexical_entry(self, pos_tag, word, probability):
        """
        Añade una entrada léxica a la gramática
        
        Parámetros:
            pos_tag (str): Categoría gramatical (ej. 'N', 'V')
            word (str): Palabra concreta (ej. 'perro', 'corre')
            probability (float): Probabilidad de esta palabra dado su POS tag
        """
        self.lexicon[(pos_tag, word)] = probability

    def normalize(self):
        """
        Normaliza todas las probabilidades para que sumen 1:
        1. Para cada lhs en producciones
        2. Para cada POS tag en el léxico
        """
        # Normalizar producciones
        for lhs in self.productions:
            total = sum(prob for _, prob in self.productions[lhs])
            if total > 0:
                self.productions[lhs] = [((rhs, hi), prob/total) 
                                      for (rhs, hi), prob in self.productions[lhs]]
        
        # Normalizar léxico por POS tag
        pos_totals = defaultdict(float)
        for (pos, _), prob in self.lexicon.items():
            pos_totals[pos] += prob
            
        for (pos, word), prob in list(self.lexicon.items()):
            if pos_totals[pos] > 0:
                self.lexicon[(pos, word)] = prob / pos_totals[pos]

    def generate_sentence(self, symbol=None):
        """
        Genera una oración lexicalizada recursivamente
        
        Parámetros:
            symbol (tuple): (símbolo no terminal, head word) o None para empezar
            
        Retorna:
            tuple: (oración generada, head word actual)
        """
        if symbol is None:
            symbol = (self.start_symbol[0], None)
        
        lhs, current_head = symbol
        
        # Caso terminal (palabra léxica)
        if lhs in self.head_tags:
            if current_head is None:
                # Seleccionar palabra basada en el POS tag
                words_probs = [(w, p) for (pt, w), p in self.lexicon.items() if pt == lhs]
                if not words_probs:
                    raise ValueError(f"No hay palabras para POS tag {lhs}")
                
                words, probs = zip(*words_probs)
                chosen_word = random.choices(words, weights=probs, k=1)[0]
                return chosen_word, chosen_word
            else:
                return current_head, current_head
        
        # Caso no terminal
        if (lhs, current_head) not in self.productions:
            raise ValueError(f"No hay producciones para {lhs} con head {current_head}")
        
        # Seleccionar producción
        productions = self.productions[(lhs, current_head)]
        probs = [prob for _, prob in productions]
        chosen_rhs, head_index = random.choices(productions, weights=probs, k=1)[0][0]
        
        # Procesar cada símbolo del lado derecho
        sentence_parts = []
        new_head = current_head
        for i, s in enumerate(chosen_rhs):
            # Determinar si este símbolo es el head
            is_head = (i == head_index)
            next_head = new_head if not is_head else None
            
            generated, sub_head = self.generate_sentence((s, next_head))
            sentence_parts.append(generated)
            
            if is_head:
                new_head = sub_head
        
        return ' '.join(sentence_parts), new_head

    def print_grammar(self):
        """Muestra la gramática y léxico en formato legible"""
        print("Gramática Lexicalizada:")
        for (lhs, head), prods in sorted(self.productions.items()):
            print(f"\n{lhs}[{head if head else '_'}] →")
            for (rhs, hi), prob in sorted(prods, key=lambda x: -x[1]):
                rhs_display = []
                for i, symbol in enumerate(rhs):
                    if i == hi:
                        rhs_display.append(f"*{symbol}*")
                    else:
                        rhs_display.append(symbol)
                print(f"  {' '.join(rhs_display)} [p={prob:.3f}]")
        
        print("\nLéxico:")
        for (pos, word), prob in sorted(self.lexicon.items()):
            print(f"  {pos} → {word} [p={prob:.3f}]")


def main():
    """Ejemplo completo de gramática lexicalizada"""
    
    # 1. Crear gramática
    grammar = LexicalizedPCFG()
    
    # 2. Definir qué tags pueden ser heads
    grammar.add_head_tag('N')  # Sustantivos
    grammar.add_head_tag('V')  # Verbos
    
    # 3. Añadir producciones (con heads lexicalizados)
    
    # Oración → NP[head] VP[head]
    grammar.add_production(('S', None), ['NP', 'VP'], 0, 1.0)
    
    # NP → Det N*[head] (el núcleo es el sustantivo)
    grammar.add_production(('NP', None), ['Det', 'N'], 1, 0.7)
    # NP → N*[head] (solo sustantivo)
    grammar.add_production(('NP', None), ['N'], 0, 0.3)
    
    # VP → V*[head] NP (el núcleo es el verbo)
    grammar.add_production(('VP', None), ['V', 'NP'], 0, 1.0)
    
    # Producciones lexicalizadas para determinantes
    grammar.add_production(('Det', 'el'), ['el'], 0, 0.6)
    grammar.add_production(('Det', 'un'), ['un'], 0, 0.4)
    
    # 4. Añadir léxico
    grammar.add_lexical_entry('N', 'gato', 0.4)
    grammar.add_lexical_entry('N', 'perro', 0.4)
    grammar.add_lexical_entry('N', 'ratón', 0.2)
    
    grammar.add_lexical_entry('V', 'persigue', 0.6)
    grammar.add_lexical_entry('V', 'muerde', 0.3)
    grammar.add_lexical_entry('V', 'duerme', 0.1)
    
    # 5. Normalizar probabilidades
    grammar.normalize()
    
    # 6. Mostrar gramática
    grammar.print_grammar()
    
    # 7. Generar oraciones
    print("\nOraciones generadas:")
    for i in range(10):
        sentence, _ = grammar.generate_sentence()
        print(f"{i+1}. {sentence.capitalize()}.")


if __name__ == "__main__":
    main()