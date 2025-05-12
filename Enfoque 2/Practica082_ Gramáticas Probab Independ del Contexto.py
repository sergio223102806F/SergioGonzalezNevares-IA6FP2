# -*- coding: utf-8 -*-                                                     # Define la codificación de caracteres del archivo como UTF-8
"""
Created on Sat Apr 26 18:14:50 2025                                         # Indica la fecha y hora de creación del archivo
                                                                           #
@author: elvin                                                              # Define el autor del archivo
"""

"""
Implementación de Gramáticas Probabilísticas Independientes del Contexto (PCFG)

Esta clase permite:
1. Definir producciones gramaticales con probabilidades
2. Normalizar automáticamente las probabilidades
3. Generar oraciones aleatorias según las probabilidades
"""

import random                                                               # Importa la biblioteca random para la generación aleatoria
from collections import defaultdict                                         # Importa defaultdict para diccionarios con valores predeterminados

class PCFG:                                                                 # Define una nueva clase llamada PCFG
    def __init__(self):                                                     # Define el constructor de la clase PCFG
        """
        Inicializa una gramática PCFG vacía                                 # Documentación del constructor
        
        Atributos:
            productions: Diccionario que almacena las reglas de producción # Diccionario para almacenar las reglas de producción
                         Formato: {lhs: [(rhs, probability), ...]}          # Formato del diccionario de producciones
            start_symbol: Símbolo inicial de la gramática                  # Símbolo inicial de la gramática
        """
        # defaultdict permite crear automáticamente listas vacías para nuevas claves # Permite crear listas vacías automáticamente para nuevas claves
        self.productions = defaultdict(list)                              # Inicializa un diccionario defaultdict para las producciones
        # El símbolo inicial se establecerá con la primera producción añadida # El símbolo inicial se establecerá con la primera producción
        self.start_symbol = None                                          # Inicializa el símbolo inicial como None

    def add_production(self, lhs, rhs, probability):                       # Define el método para añadir una producción
        """
        Añade una regla de producción a la gramática                       # Documentación del método add_production
        
        Parámetros:
            lhs (str): Símbolo no terminal (lado izquierdo de la producción) # Símbolo no terminal
            rhs (list): Lista de símbolos (lado derecho de la producción)    # Lista de símbolos
            probability (float): Probabilidad de esta producción (0-1)      # Probabilidad de la producción
        
        Lanza:
            ValueError: Si rhs no es lista o la probabilidad es inválida    # Error si rhs no es lista o probabilidad inválida
        """
        # Validación de tipos y valores                                  # Comentario sobre la validación de tipos y valores
        if not isinstance(rhs, list):                                     # Si rhs no es una lista
            raise ValueError("El lado derecho debe ser una lista de símbolos") # Lanza un error si el lado derecho no es una lista
        if not (0 <= probability <= 1):                                  # Si la probabilidad no está entre 0 y 1
            raise ValueError("La probabilidad debe estar entre 0 y 1")    # Lanza un error si la probabilidad es inválida

        # Añadir la producción al diccionario                           # Comentario sobre la adición de la producción
        self.productions[lhs].append((rhs, probability))                  # Añade la producción al diccionario

        # Establecer el símbolo inicial si es la primera producción      # Comentario sobre el establecimiento del símbolo inicial
        if self.start_symbol is None:                                    # Si el símbolo inicial aún no se ha establecido
            self.start_symbol = lhs                                      # Establece el símbolo inicial

    def normalize(self):                                                  # Define el método para normalizar las probabilidades
        """
        Normaliza las probabilidades para que sumen 1 en cada no terminal # Documentación del método normalize
        
        Esto corrige posibles inconsistencias donde las probabilidades    # Correge posibles inconsistencias en las probabilidades
        de las producciones para un mismo no terminal no suman exactamente 1. # de las producciones para un mismo no terminal
        """
        for lhs in self.productions:                                     # Itera sobre cada símbolo no terminal
            # Calcular la suma total de probabilidades para este no terminal # Calcula la suma total de probabilidades
            total = sum(prob for _, prob in self.productions[lhs])      # Suma las probabilidades de las producciones para el no terminal

            # Solo normalizar si la suma es positiva (evitar división por cero) # Normaliza solo si la suma es positiva
            if total > 0:                                                 # Si la suma total es mayor que 0
                normalized_productions = []                              # Inicializa una lista para las producciones normalizadas
                # Recalcular cada probabilidad dividiendo por el total    # Recalcula cada probabilidad
                for rhs, prob in self.productions[lhs]:                  # Itera sobre las producciones del no terminal
                    normalized_productions.append((rhs, prob/total))    # Añade la producción con la probabilidad normalizada
                # Reemplazar las producciones originales con las normalizadas # Reemplaza las producciones originales
                self.productions[lhs] = normalized_productions           # Actualiza las producciones del no terminal

    def generate_sentence(self, symbol=None):                            # Define el método para generar una oración
        """
        Genera una oración aleatoria expandiendo recursivamente los símbolos # Documentación del método generate_sentence
        
        Parámetros:
            symbol (str): Símbolo desde el que comenzar la generación    # Símbolo inicial para la generación
                          (None para usar el símbolo inicial de la gramática) # Usa el símbolo inicial si no se especifica
                          
        Retorna:
            str: Oración generada concatenando los símbolos terminales     # Oración generada
        """
        # Usar símbolo inicial si no se especifica uno                   # Usa el símbolo inicial si no se especifica
        if symbol is None:                                               # Si el símbolo no se especifica
            symbol = self.start_symbol                                  # Usa el símbolo inicial

        # Caso base: si es un símbolo terminal (no tiene producciones)    # Caso base: símbolo terminal
        if symbol not in self.productions:                              # Si el símbolo no tiene producciones
            return symbol                                                # Retorna el símbolo

        # Seleccionar una producción aleatoria según las probabilidades  # Selecciona una producción aleatoria
        productions = self.productions[symbol]                          # Obtiene las producciones para el símbolo actual
        # Extraer solo las probabilidades para random.choices           # Extrae las probabilidades
        probs = [prob for _, prob in productions]                      # Crea una lista de probabilidades
        # Elegir una producción (random.choices retorna una lista, tomamos el primer elemento) # Elige una producción
        chosen_rhs = random.choices(productions, weights=probs, k=1)[0][0] # Elige una producción basada en las probabilidades

        # Generar recursivamente cada símbolo del lado derecho         # Genera recursivamente cada símbolo
        sentence_parts = []                                            # Inicializa una lista para las partes de la oración
        for s in chosen_rhs:                                            # Itera sobre los símbolos del lado derecho
            sentence_parts.append(self.generate_sentence(s))          # Genera recursivamente la parte de la oración

        # Unir todos los componentes con espacios                      # Une las partes de la oración con espacios
        return ' '.join(sentence_parts)                                # Retorna la oración generada

    def print_grammar(self):                                             # Define el método para imprimir la gramática
        """Muestra todas las producciones de la gramática en formato legible""" # Documentación del método print_grammar
        print("Gramática PCFG:")                                        # Imprime el encabezado de la gramática
        # Ordenar los símbolos no terminales alfabéticamente           # Ordena los símbolos no terminales
        for lhs in sorted(self.productions.keys()):                    # Itera sobre los símbolos no terminales ordenados
            # Mostrar cada producción para este no terminal            # Muestra cada producción
            for rhs, prob in self.productions[lhs]:                  # Itera sobre las producciones del no terminal
                # Formatear la producción como "S → NP VP [p=0.8]"      # Formatea la producción para imprimir
                print(f"{lhs} → {' '.join(rhs)} [p={prob:.3f}]")      # Imprime la producción formateada


def main():                                                             # Define la función principal
    """Función principal con ejemplo de uso completo"""                 # Documentación de la función main

    # 1. Crear instancia de la gramática                              # Crea una instancia de la gramática
    grammar = PCFG()                                                   # Crea una instancia de la clase PCFG

    # 2. Definir las producciones gramaticales                         # Define las producciones gramaticales
    # Estructura básica de oración                                   # Estructura básica de la oración
    grammar.add_production('S', ['NP', 'VP'], 1.0)                     # Oración → FraseNominal FraseVerbal

    # Frases nominales (sujeto)                                      # Frases nominales (sujeto)
    grammar.add_production('NP', ['Det', 'N'], 0.7)                      # Artículo + Sustantivo
    grammar.add_production('NP', ['N'], 0.3)                            # Solo sustantivo
    grammar.add_production('NP', ['Det', 'Adj', 'N'], 0.2)              # Artículo + Adjetivo + Sustantivo

    # Frases verbales (predicado)                                     # Frases verbales (predicado)
    grammar.add_production('VP', ['V', 'NP'], 0.8)                      # Verbo + Objeto
    grammar.add_production('VP', ['V'], 0.2)                            # Verbo intransitivo

    # Artículos/determinantes                                        # Artículos/determinantes
    grammar.add_production('Det', ['el'], 0.5)
    grammar.add_production('Det', ['un'], 0.5)

    # Sustantivos                                                    # Sustantivos
    grammar.add_production('N', ['gato'], 0.4)
    grammar.add_production('N', ['perro'], 0.4)
    grammar.add_production('N', ['ratón'], 0.2)

    # Verbos                                                         # Verbos
    grammar.add_production('V', ['persigue'], 0.6)
    grammar.add_production('V', ['muerde'], 0.3)
    grammar.add_production('V', ['duerme'], 0.1)

    # Adjetivos                                                      # Adjetivos
    grammar.add_production('Adj', ['grande'], 0.5)
    grammar.add_production('Adj', ['pequeño'], 0.5)

    # 3. Normalizar probabilidades (asegurar que sumen 1)             # Normaliza las probabilidades
    grammar.normalize()

    # 4. Mostrar la gramática completa                               # Muestra la gramática completa
    grammar.print_grammar()

    # 5. Generar y mostrar 10 oraciones de ejemplo                   # Genera y muestra 10 oraciones de ejemplo
    print("\nOraciones generadas:")                                   # Imprime un encabezado para las oraciones generadas
    for i in range(10):                                               # Itera 10 veces
        sentence = grammar.generate_sentence()                       # Genera una oración
        # Formatear con mayúscula inicial y punto final              # Formatea la oración
        print(f"{i+1}. {sentence.capitalize()}.")                   # Imprime la oración formateada


if __name__ == "__main__":                                               # Asegura que el código dentro solo se ejecute si el script es el principal
    # Ejecutar el ejemplo principal al llamar directamente al script   # Ejecuta la función principal
    main()