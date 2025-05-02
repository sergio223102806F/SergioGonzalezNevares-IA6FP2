# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 18:14:50 2025

@author: elvin
"""

"""
Implementación de Gramáticas Probabilísticas Independientes del Contexto (PCFG)

Esta clase permite:
1. Definir producciones gramaticales con probabilidades
2. Normalizar automáticamente las probabilidades
3. Generar oraciones aleatorias según las probabilidades
"""

import random
from collections import defaultdict

class PCFG:
    def __init__(self):
        """
        Inicializa una gramática PCFG vacía
        
        Atributos:
            productions: Diccionario que almacena las reglas de producción
                         Formato: {lhs: [(rhs, probability), ...]}
            start_symbol: Símbolo inicial de la gramática
        """
        # defaultdict permite crear automáticamente listas vacías para nuevas claves
        self.productions = defaultdict(list)
        # El símbolo inicial se establecerá con la primera producción añadida
        self.start_symbol = None
    
    def add_production(self, lhs, rhs, probability):
        """
        Añade una regla de producción a la gramática
        
        Parámetros:
            lhs (str): Símbolo no terminal (lado izquierdo de la producción)
            rhs (list): Lista de símbolos (lado derecho de la producción)
            probability (float): Probabilidad de esta producción (0-1)
            
        Lanza:
            ValueError: Si rhs no es lista o la probabilidad es inválida
        """
        # Validación de tipos y valores
        if not isinstance(rhs, list):
            raise ValueError("El lado derecho debe ser una lista de símbolos")
        if not (0 <= probability <= 1):
            raise ValueError("La probabilidad debe estar entre 0 y 1")
            
        # Añadir la producción al diccionario
        self.productions[lhs].append((rhs, probability))
        
        # Establecer el símbolo inicial si es la primera producción
        if self.start_symbol is None:
            self.start_symbol = lhs
    
    def normalize(self):
        """
        Normaliza las probabilidades para que sumen 1 en cada no terminal
        
        Esto corrige posibles inconsistencias donde las probabilidades
        de las producciones para un mismo no terminal no suman exactamente 1.
        """
        for lhs in self.productions:
            # Calcular la suma total de probabilidades para este no terminal
            total = sum(prob for _, prob in self.productions[lhs])
            
            # Solo normalizar si la suma es positiva (evitar división por cero)
            if total > 0:
                normalized_productions = []
                # Recalcular cada probabilidad dividiendo por el total
                for rhs, prob in self.productions[lhs]:
                    normalized_productions.append((rhs, prob/total))
                # Reemplazar las producciones originales con las normalizadas
                self.productions[lhs] = normalized_productions
    
    def generate_sentence(self, symbol=None):
        """
        Genera una oración aleatoria expandiendo recursivamente los símbolos
        
        Parámetros:
            symbol (str): Símbolo desde el que comenzar la generación
                         (None para usar el símbolo inicial de la gramática)
                         
        Retorna:
            str: Oración generada concatenando los símbolos terminales
        """
        # Usar símbolo inicial si no se especifica uno
        if symbol is None:
            symbol = self.start_symbol
        
        # Caso base: si es un símbolo terminal (no tiene producciones)
        if symbol not in self.productions:
            return symbol
            
        # Seleccionar una producción aleatoria según las probabilidades
        productions = self.productions[symbol]
        # Extraer solo las probabilidades para random.choices
        probs = [prob for _, prob in productions]
        # Elegir una producción (random.choices retorna una lista, tomamos el primer elemento)
        chosen_rhs = random.choices(productions, weights=probs, k=1)[0][0]
        
        # Generar recursivamente cada símbolo del lado derecho
        sentence_parts = []
        for s in chosen_rhs:
            sentence_parts.append(self.generate_sentence(s))
        
        # Unir todos los componentes con espacios
        return ' '.join(sentence_parts)
    
    def print_grammar(self):
        """Muestra todas las producciones de la gramática en formato legible"""
        print("Gramática PCFG:")
        # Ordenar los símbolos no terminales alfabéticamente
        for lhs in sorted(self.productions.keys()):
            # Mostrar cada producción para este no terminal
            for rhs, prob in self.productions[lhs]:
                # Formatear la producción como "S → NP VP [p=0.8]"
                print(f"{lhs} → {' '.join(rhs)} [p={prob:.3f}]")


def main():
    """Función principal con ejemplo de uso completo"""
    
    # 1. Crear instancia de la gramática
    grammar = PCFG()
    
    # 2. Definir las producciones gramaticales
    # Estructura básica de oración
    grammar.add_production('S', ['NP', 'VP'], 1.0)  # Oración → FraseNominal FraseVerbal
    
    # Frases nominales (sujeto)
    grammar.add_production('NP', ['Det', 'N'], 0.7)       # Artículo + Sustantivo
    grammar.add_production('NP', ['N'], 0.3)              # Solo sustantivo
    grammar.add_production('NP', ['Det', 'Adj', 'N'], 0.2) # Artículo + Adjetivo + Sustantivo
    
    # Frases verbales (predicado)
    grammar.add_production('VP', ['V', 'NP'], 0.8)  # Verbo + Objeto
    grammar.add_production('VP', ['V'], 0.2)        # Verbo intransitivo
    
    # Artículos/determinantes
    grammar.add_production('Det', ['el'], 0.5)
    grammar.add_production('Det', ['un'], 0.5)
    
    # Sustantivos
    grammar.add_production('N', ['gato'], 0.4)
    grammar.add_production('N', ['perro'], 0.4)
    grammar.add_production('N', ['ratón'], 0.2)
    
    # Verbos
    grammar.add_production('V', ['persigue'], 0.6)
    grammar.add_production('V', ['muerde'], 0.3)
    grammar.add_production('V', ['duerme'], 0.1)
    
    # Adjetivos
    grammar.add_production('Adj', ['grande'], 0.5)
    grammar.add_production('Adj', ['pequeño'], 0.5)
    
    # 3. Normalizar probabilidades (asegurar que sumen 1)
    grammar.normalize()
    
    # 4. Mostrar la gramática completa
    grammar.print_grammar()
    
    # 5. Generar y mostrar 10 oraciones de ejemplo
    print("\nOraciones generadas:")
    for i in range(10):
        sentence = grammar.generate_sentence()
        # Formatear con mayúscula inicial y punto final
        print(f"{i+1}. {sentence.capitalize()}.")


if __name__ == "__main__":
    # Ejecutar el ejemplo principal al llamar directamente al script
    main()