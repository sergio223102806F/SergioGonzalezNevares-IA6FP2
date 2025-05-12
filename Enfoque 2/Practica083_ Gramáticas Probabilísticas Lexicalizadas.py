# -*- coding: utf-8 -*-                                                     # Define la codificación de caracteres del archivo como UTF-8
"""
Created on Sat Apr 26 18:47:36 2025                                         # Indica la fecha y hora de creación del archivo
                                                                           #
@author: elvin                                                              # Define el autor del archivo
"""

"""
Implementación de Gramáticas Probabilísticas Lexicalizadas (LPCFG)

Esta extensión de PCFG incorpora:
1. Información léxica en las producciones
2. Probabilidades dependientes de palabras específicas
3. Generación más realista basada en léxico
"""

import random                                                               # Importa la biblioteca random para la generación de números aleatorios
from collections import defaultdict                                         # Importa defaultdict para crear diccionarios con valores predeterminados

class LexicalizedPCFG:                                                      # Define una nueva clase llamada LexicalizedPCFG
    def __init__(self):                                                     # Define el constructor de la clase LexicalizedPCFG
        """
        Inicializa una gramática LPCFG vacía                                 # Documentación del constructor
        
        Atributos:
            productions: Diccionario de producciones lexicalizadas          # Diccionario para almacenar las producciones lexicalizadas
                         Formato: {(lhs, head): [((rhs, head_index), probability), ...]} # Define el formato del diccionario de producciones
            lexicon: Diccionario de probabilidades léxicas                  # Diccionario para almacenar las probabilidades léxicas
                     Formato: {(pos_tag, word): probability}                # Define el formato del diccionario léxico
            start_symbol: Símbolo inicial de la gramática                  # Símbolo inicial de la gramática
        """
        self.productions = defaultdict(list)                              # Inicializa un diccionario defaultdict para las producciones
        self.lexicon = defaultdict(float)                                   # Inicializa un diccionario defaultdict para el léxico con valores float predeterminados
        self.start_symbol = None                                          # Inicializa el símbolo inicial como None
        self.head_tags = {}                                               # Inicializa un diccionario para almacenar los POS tags que pueden ser heads

    def add_head_tag(self, pos_tag):                                       # Define el método para añadir un POS tag como head
        """
        Registra un POS tag como posible head (núcleo)                    # Documentación del método add_head_tag
        
        Parámetros:
            pos_tag (str): Etiqueta gramatical que puede ser núcleo (ej. 'N', 'V') # El POS tag a registrar como head
        """
        self.head_tags[pos_tag] = True                                    # Marca el pos_tag como un posible head

    def add_production(self, lhs, rhs, head_index, probability):          # Define el método para añadir una producción lexicalizada
        """
        Añade una producción lexicalizada a la gramática                   # Documentación del método add_production
        
        Parámetros:
            lhs (tuple): (símbolo no terminal, head)                      # Tupla que representa el lado izquierdo (símbolo no terminal y su head)
            rhs (list): Lista de símbolos (terminales o no terminales)     # Lista de símbolos en el lado derecho de la producción
            head_index (int): Índice en rhs que indica el head de la producción # Índice del head dentro de la lista de símbolos del lado derecho
            probability (float): Probabilidad de esta producción (0-1)    # Probabilidad de la producción
        
        Lanza:
            ValueError: Si los parámetros son inválidos                   # Lanza un error si los parámetros no cumplen con las validaciones
        """
        # Validaciones
        if not isinstance(lhs, tuple) or len(lhs) != 2:                   # Verifica si lhs es una tupla de tamaño 2
            raise ValueError("lhs debe ser tupla (symbol, head)")        # Lanza un error si lhs no tiene el formato correcto
        if not isinstance(rhs, list):                                     # Verifica si rhs es una lista
            raise ValueError("rhs debe ser una lista")                   # Lanza un error si rhs no es una lista
        if not 0 <= head_index < len(rhs):                               # Verifica si head_index está dentro del rango de rhs
            raise ValueError("head_index fuera de rango")               # Lanza un error si head_index está fuera de los límites de rhs
        if not (0 <= probability <= 1):                                  # Verifica si la probabilidad está entre 0 y 1
            raise ValueError("Probabilidad debe estar entre 0 y 1")      # Lanza un error si la probabilidad está fuera del rango válido

        # Añadir producción
        self.productions[lhs].append(((tuple(rhs), head_index), probability)) # Añade la producción a la lista de producciones para el lado izquierdo dado

        # Establecer símbolo inicial si es la primera producción
        if self.start_symbol is None:                                    # Verifica si el símbolo inicial aún no ha sido establecido
            self.start_symbol = lhs                                      # Establece el símbolo inicial con el lado izquierdo de la primera producción

    def add_lexical_entry(self, pos_tag, word, probability):             # Define el método para añadir una entrada léxica
        """
        Añade una entrada léxica a la gramática                           # Documentación del método add_lexical_entry
        
        Parámetros:
            pos_tag (str): Categoría gramatical (ej. 'N', 'V')           # Etiqueta de la parte del discurso (POS tag) de la palabra
            word (str): Palabra concreta (ej. 'perro', 'corre')           # La palabra léxica
            probability (float): Probabilidad de esta palabra dado su POS tag # Probabilidad de la palabra dada su etiqueta POS
        """
        self.lexicon[(pos_tag, word)] = probability                     # Añade la entrada léxica al diccionario del léxico

    def normalize(self):                                                  # Define el método para normalizar las probabilidades
        """
        Normaliza todas las probabilidades para que sumen 1:              # Documentación del método normalize
        1. Para cada lhs en producciones                               # Normaliza las probabilidades de las producciones para cada lado izquierdo
        2. Para cada POS tag en el léxico                             # Normaliza las probabilidades de las palabras para cada POS tag en el léxico
        """
        # Normalizar producciones
        for lhs in self.productions:                                     # Itera sobre cada lado izquierdo (símbolo no terminal y su head) en las producciones
            total = sum(prob for _, prob in self.productions[lhs])      # Calcula la suma total de las probabilidades para las producciones de este lado izquierdo
            if total > 0:                                                 # Verifica si la suma total es mayor que cero para evitar división por cero
                self.productions[lhs] = [((rhs, hi), prob/total)          # Normaliza cada probabilidad dividiéndola por la suma total
                                            for (rhs, hi), prob in self.productions[lhs]] # Recorre las producciones y sus probabilidades para este lado izquierdo
        
        # Normalizar léxico por POS tag
        pos_totals = defaultdict(float)                                   # Inicializa un diccionario defaultdict para almacenar la suma de probabilidades por POS tag
        for (pos, _), prob in self.lexicon.items():                      # Itera sobre cada entrada en el léxico (POS tag y palabra) y su probabilidad
            pos_totals[pos] += prob                                      # Suma la probabilidad a la suma total para el POS tag correspondiente
        
        for (pos, word), prob in list(self.lexicon.items()):             # Itera sobre cada entrada en el léxico (creando una lista para permitir la modificación)
            if pos_totals[pos] > 0:                                      # Verifica si la suma total para este POS tag es mayor que cero
                self.lexicon[(pos, word)] = prob / pos_totals[pos]      # Normaliza la probabilidad de la palabra dividiéndola por la suma total de su POS tag

    def generate_sentence(self, symbol=None):                            # Define el método para generar una oración
        """
        Genera una oración lexicalizada recursivamente                   # Documentación del método generate_sentence
        
        Parámetros:
            symbol (tuple): (símbolo no terminal, head word) o None para empezar # El símbolo actual a expandir (con su head) o None para comenzar con el símbolo inicial
        
        Retorna:
            tuple: (oración generada, head word actual)                  # Tupla que contiene la oración generada (lista de palabras) y la palabra head actual
        """
        if symbol is None:                                               # Verifica si no se proporcionó un símbolo inicial
            symbol = (self.start_symbol[0], None)                       # Establece el símbolo inicial con el símbolo inicial de la gramática y head como None
        
        lhs, current_head = symbol                                      # Desempaqueta el símbolo actual en el símbolo no terminal y la palabra head actual
        
        # Caso terminal (palabra léxica)                                 # Maneja el caso en que el símbolo actual es un POS tag (terminal en este nivel)
        if lhs in self.head_tags:                                       # Verifica si el símbolo actual es un POS tag que puede ser un head
            if current_head is None:                                    # Si no hay una head especificada (para la primera vez que se genera un terminal)
                # Seleccionar palabra basada en el POS tag               # Selecciona una palabra del léxico basada en el POS tag actual
                words_probs = [(w, p) for (pt, w), p in self.lexicon.items() if pt == lhs] # Filtra las palabras del léxico que tienen el POS tag actual
                if not words_probs:                                     # Si no hay palabras para este POS tag en el léxico
                    raise ValueError(f"No hay palabras para POS tag {lhs}") # Lanza un error si no se encuentran palabras para el POS tag
                
                words, probs = zip(*words_probs)                         # Separa las palabras y sus probabilidades de la lista filtrada
                chosen_word = random.choices(words, weights=probs, k=1)[0] # Elige una palabra aleatoriamente basada en sus probabilidades
                return chosen_word, chosen_word                           # Retorna la palabra elegida como la palabra generada y como su propia head
            else:                                                        # Si ya hay una head especificada (para mantener la consistencia léxica)
                return current_head, current_head                       # Retorna la head actual como la palabra generada y como su propia head
        
        # Caso no terminal                                             # Maneja el caso en que el símbolo actual es un símbolo no terminal
        if (lhs, current_head) not in self.productions:                 # Verifica si no hay producciones para este símbolo no terminal y su head actual
            raise ValueError(f"No hay producciones para {lhs} con head {current_head}") # Lanza un error si no se encuentran producciones
        
        # Seleccionar producción                                       # Selecciona una producción para expandir el símbolo no terminal actual
        productions = self.productions[(lhs, current_head)]              # Obtiene la lista de producciones para el símbolo no terminal y su head
        probs = [prob for _, prob in productions]                      # Extrae las probabilidades de las producciones
        chosen_rhs, head_index = random.choices(productions, weights=probs, k=1)[0][0] # Elige una producción aleatoriamente basada en sus probabilidades y obtiene el lado derecho y el índice del head
        
        # Procesar cada símbolo del lado derecho                       # Procesa recursivamente cada símbolo en el lado derecho de la producción elegida
        sentence_parts = []                                            # Inicializa una lista para almacenar las partes generadas de la oración
        new_head = current_head                                      # Inicializa la nueva head con la head actual
        for i, s in enumerate(chosen_rhs):                             # Itera sobre cada símbolo en el lado derecho de la producción
            # Determinar si este símbolo es el head                     # Determina si el símbolo actual es el head de esta producción
            is_head = (i == head_index)                               # Verifica si el índice actual coincide con el índice del head de la producción
            next_head = new_head if not is_head else None             # Si no es el head, pasa la head actual; si es el head, pasa None para que se genere una nueva head si es un terminal
            
            generated, sub_head = self.generate_sentence((s, next_head)) # Llama recursivamente a generate_sentence para el símbolo actual y la posible siguiente head
            sentence_parts.append(generated)                           # Añade la parte generada de la oración a la lista
            
            if is_head:                                                # Si el símbolo actual es el head de la producción
                new_head = sub_head                                    # Actualiza la nueva head con la head generada por la sub-llamada
        
        return ' '.join(sentence_parts), new_head                     # Retorna la oración generada (unida por espacios) y la palabra head actual

    def print_grammar(self):                                             # Define el método para imprimir la gramática
        """Muestra la gramática y léxico en formato legible"""         # Documentación del método print_grammar
        print("Gramática Lexicalizada:")                                # Imprime un encabezado para la gramática lexicalizada
        for (lhs, head), prods in sorted(self.productions.items()):    # Itera sobre cada lado izquierdo (símbolo no terminal y su head) en las producciones, ordenado alfabéticamente
            print(f"\n{lhs}[{head if head else '_'}] →")              # Imprime el lado izquierdo de la producción, mostrando la head si existe o '_' si no
            for (rhs, hi), prob in sorted(prods, key=lambda x: -x[1]): # Itera sobre cada producción para este lado izquierdo, ordenado por probabilidad descendente
                rhs_display = []                                       # Inicializa una lista para almacenar la representación del lado derecho
                for i, symbol in enumerate(rhs):                       # Itera sobre cada símbolo en el lado derecho
                    if i == hi:                                        # Si el índice actual coincide con el índice del head
                        rhs_display.append(f"*{symbol}*")              # Marca el head con asteriscos
                    else:                                              # Si no es el head
                        rhs_display.append(symbol)                     # Añade el símbolo a la lista tal cual
                print(f"  {' '.join(rhs_display)} [p={prob:.3f}]")   # Imprime la producción formateada con el lado derecho y la probabilidad
        
        print("\nLéxico:")                                            # Imprime un encabezado para el léxico
        for (pos, word), prob in sorted(self.lexicon.items()):        # Itera sobre cada entrada en el léxico (POS tag y palabra), ordenado alfabéticamente
            print(f"  {pos} → {word} [p={prob:.3f}]")                 # Imprime la entrada léxica formateada con el POS tag, la palabra y su probabilidad


def main():                                                             # Define la función principal
    """Ejemplo completo de gramática lexicalizada"""                 # Documentación de la función main
    
    # 1. Crear gramática                                               # Crea una instancia de la gramática lexicalizada
    grammar = LexicalizedPCFG()                                        # Inicializa un objeto de la clase LexicalizedPCFG
    
    # 2. Definir qué tags pueden ser heads                              # Define los POS tags que pueden actuar como heads
    grammar.add_head_tag('N')                                          # Los sustantivos pueden ser heads
    grammar.add_head_tag('V')                                          # Los verbos pueden ser heads
    
    # 3. Añadir producciones (con heads lexicalizados)                 # Añade las reglas de producción a la gramática, especificando el head en el lado derecho
    
    # Oración → NP[head] VP[head]                                      # Regla para la estructura de la oración, el head de la oración es el head del NP
    grammar.add_production(('S', None), ['NP', 'VP'], 0, 1.0)        # El head del S se hereda del NP (índice 0)
    
    # NP → Det N*[head] (el núcleo es el sustantivo)                   # Regla para la frase nominal con determinante y sustantivo, el sustantivo es el head
    grammar.add_production(('NP', None), ['Det', 'N'], 1, 0.7)        # El head del NP es el N (índice 1)
    # NP → N*[head] (solo sustantivo)                                 # Regla para la frase nominal que consiste solo en un sustantivo, el sustantivo es el head
    grammar.add_production(('NP', None), ['N'], 0, 0.3)              # El head del NP es el N (índice 0)
    
    # VP → V*[head] NP (el núcleo es el verbo)                       # Regla para la frase verbal con verbo y frase nominal, el verbo es el head
    grammar.add_production(('VP', None), ['V', 'NP'], 0, 1.0)        # El head del VP es el V (índice 0)
    
    # Producciones lexicalizadas para determinantes                   # Reglas para los determinantes, la palabra es el head
    grammar.add_production(('Det', 'el'), ['el'], 0, 0.6)            # El head del Det 'el' es 'el' (índice 0)
    grammar.add_production(('Det', 'un'), ['un'], 0, 0.4)            # El head del Det 'un' es 'un' (índice 0)
    
    # 4. Añadir léxico                                                 # Añade las entradas léxicas (palabras y sus POS tags con probabilidades)
    grammar.add_lexical_entry('N', 'gato', 0.4)                       # El sust