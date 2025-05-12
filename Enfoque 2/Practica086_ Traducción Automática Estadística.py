# -*- coding: utf-8 -*-                                                     # Define la codificación de caracteres del archivo como UTF-8
"""
Created on Sun Apr 27 13:43:57 2025                                         # Indica la fecha y hora de creación del archivo
                                                                           #
@author: elvin                                                              # Define el autor del archivo
"""

"""
Sistema de Traducción Automática Estadística (Statistical Machine Translation - SMT)

Este sistema implementa un modelo de traducción basado en:
1. Modelo de lenguaje (n-gramas)
2. Modelo de traducción (alineamiento de palabras)
3. Decodificación (búsqueda del mejor candidato)
"""

import math                                                               # Importa la biblioteca math para operaciones matemáticas
from collections import defaultdict, Counter                                # Importa defaultdict para diccionarios con valores predeterminados y Counter para contar elementos
from itertools import permutations                                         # Importa permutations para generar todas las posibles ordenaciones
import numpy as np                                                          # Importa la biblioteca numpy para computación numérica

class StatisticalMT:                                                      # Define una nueva clase llamada StatisticalMT
    def __init__(self):                                                     # Define el constructor de la clase StatisticalMT
        """
        Inicializa el sistema de traducción estadística.                   # Documentación del constructor
        
        Atributos:                                                         # Documentación de los atributos
        - lm: Modelo de lenguaje (frecuencias de n-gramas)                 # Atributo para almacenar el modelo de lenguaje (n-gramas)
        - tm: Modelo de traducción (probabilidades léxicas)               # Atributo para almacenar el modelo de traducción (probabilidades léxicas)
        - vocab: Vocabulario del lenguaje objetivo                         # Atributo para almacenar el vocabulario del lenguaje objetivo
        - max_len: Longitud máxima de frase permitida                     # Atributo para almacenar la longitud máxima de frase permitida
        """
        self.lm = defaultdict(Counter)  # Modelo de lenguaje (n-gramas)   # Inicializa un defaultdict de Counter para el modelo de lenguaje
        self.tm = defaultdict(dict)     # Modelo de traducción {src_word: {tgt_word: prob}} # Inicializa un defaultdict de diccionarios para el modelo de traducción
        self.vocab = set()               # Vocabulario del lenguaje objetivo # Inicializa un conjunto vacío para el vocabulario del lenguaje objetivo
        self.max_len = 20                # Longitud máxima de frase a traducir # Establece la longitud máxima de frase a traducir

    def train_language_model(self, sentences, n=3):                        # Define el método para entrenar el modelo de lenguaje
        """
        Entrena un modelo de lenguaje n-grama.                             # Documentación del método
        
        Args:                                                             # Documentación de los argumentos
            sentences: Lista de oraciones (cada oración es lista de palabras) # Lista de oraciones para entrenar el modelo de lenguaje
            n: Orden del n-grama (por defecto trigramas)                   # Orden del n-grama a utilizar (por defecto 3 para trigramas)
        """
        for sentence in sentences:                                         # Itera sobre cada oración en la lista de oraciones
            # Prepara la oración con tokens de inicio/fin                  # Comentario explicando la siguiente acción
            padded = ['<s>'] * (n-1) + sentence + ['</s>']              # Añade tokens de inicio ('<s>') y fin ('</s>') a la oración
            
            # Calcula n-gramas para la oración actual                     # Comentario explicando la siguiente acción
            for i in range(len(padded) - n + 1):                          # Itera sobre la oración para generar n-gramas
                # El contexto son las n-1 palabras anteriores              # Comentario explicando la siguiente acción
                context = tuple(padded[i:i+n-1])                           # Crea una tupla con las n-1 palabras anteriores como contexto
                # La palabra objetivo es la siguiente                       # Comentario explicando la siguiente acción
                word = padded[i+n-1]                                      # Obtiene la palabra que sigue al contexto
                # Actualiza el contador para este n-grama                  # Comentario explicando la siguiente acción
                self.lm[context][word] += 1                               # Incrementa el contador de la palabra para el contexto dado
        
        # Convierte conteos a probabilidades (suavizado add-one)          # Comentario explicando la siguiente acción
        for context in self.lm:                                           # Itera sobre cada contexto en el modelo de lenguaje
            total = sum(self.lm[context].values()) + len(self.lm[context]) # Calcula el total de conteos para el contexto más el tamaño del vocabulario para suavizado
            for word in self.lm[context]:                               # Itera sobre cada palabra para el contexto
                self.lm[context][word] = (self.lm[context][word] + 1) / total # Calcula la probabilidad suavizada (add-one)
        
        # Actualiza el vocabulario                                        # Comentario explicando la siguiente acción
        self.vocab = set(word for context in self.lm for word in self.lm[context]) # Crea un conjunto con todas las palabras del modelo de lenguaje

    def train_translation_model(self, src_sentences, tgt_sentences):        # Define el método para entrenar el modelo de traducción
        """
        Entrena el modelo de traducción usando conteos de alineamiento.    # Documentación del método
        
        Args:                                                             # Documentación de los argumentos
            src_sentences: Lista de oraciones en lenguaje fuente           # Lista de oraciones en el lenguaje fuente
            tgt_sentences: Lista de oraciones en lenguaje objetivo         # Lista de oraciones correspondientes en el lenguaje objetivo
        """
        # Primero cuenta co-ocurrencias de palabras                      # Comentario explicando la siguiente acción
        cooc_counts = defaultdict(Counter)                               # Inicializa un defaultdict de Counter para contar co-ocurrencias
        src_vocab = set()                                                # Inicializa un conjunto vacío para el vocabulario del lenguaje fuente
        
        for src_sent, tgt_sent in zip(src_sentences, tgt_sentences):     # Itera sobre pares de oraciones fuente y objetivo
            for src_word in src_sent:                                    # Itera sobre cada palabra en la oración fuente
                src_vocab.add(src_word)                                  # Añade la palabra al vocabulario fuente
                for tgt_word in tgt_sent:                                # Itera sobre cada palabra en la oración objetivo
                    cooc_counts[src_word][tgt_word] += 1                 # Incrementa el contador de co-ocurrencia para el par de palabras
        
        # Calcula probabilidades léxicas P(tgt|src)                      # Comentario explicando la siguiente acción
        for src_word in cooc_counts:                                     # Itera sobre cada palabra fuente
            total = sum(cooc_counts[src_word].values())                  # Calcula el total de co-ocurrencias para la palabra fuente
            for tgt_word in cooc_counts[src_word]:                      # Itera sobre cada palabra objetivo que co-ocurre con la palabra fuente
                self.tm[src_word][tgt_word] = cooc_counts[src_word][tgt_word] / total # Calcula la probabilidad léxica P(tgt|src)

    def lm_probability(self, sentence, n=3):                             # Define el método para calcular la probabilidad de una oración con el modelo de lenguaje
        """
        Calcula la probabilidad logarítmica de una oración según el modelo de lenguaje. # Documentación del método
        
        Args:                                                             # Documentación de los argumentos
            sentence: Lista de palabras de la oración                     # Lista de palabras de la oración para calcular la probabilidad
            n: Orden del n-grama                                         # Orden del n-grama del modelo de lenguaje
            
        Returns:                                                          # Documentación del valor de retorno
            float: Log probabilidad de la oración                         # La probabilidad logarítmica de la oración según el modelo de lenguaje
        """
        padded = ['<s>'] * (n-1) + sentence + ['</s>']              # Añade tokens de inicio y fin a la oración
        log_prob = 0.0                                                   # Inicializa la probabilidad logarítmica en 0
        
        for i in range(len(padded) - n + 1):                          # Itera sobre la oración para calcular la probabilidad de cada n-grama
            context = tuple(padded[i:i+n-1])                           # Obtiene el contexto (n-1 palabras anteriores)
            word = padded[i+n-1]                                      # Obtiene la palabra actual
            
            # Probabilidad suavizada para palabras desconocidas           # Comentario explicando la siguiente acción
            prob = self.lm[context].get(word, 1 / (sum(self.lm[context].values()) + len(self.vocab))) # Obtiene la probabilidad de la palabra dado el contexto con suavizado
            log_prob += math.log(prob)                                  # Suma el logaritmo de la probabilidad a la probabilidad total
            
        return log_prob                                                  # Retorna la probabilidad logarítmica de la oración

    def translate_sentence(self, src_sentence, beam_size=5):             # Define el método para traducir una oración
        """
        Traduce una oración usando búsqueda por haz (beam search).       # Documentación del método
        
        Args:                                                             # Documentación de los argumentos
            src_sentence: Lista de palabras de la oración fuente          # Lista de palabras de la oración en el lenguaje fuente a traducir
            beam_size: Tamaño del haz para la búsqueda                   # Número de hipótesis a mantener en cada paso de la búsqueda
            
        Returns:                                                          # Documentación del valor de retorno
            tuple: (oración traducida, puntuación)                       # Una tupla conteniendo la mejor oración traducida y su puntuación
        """
        # Preprocesamiento: elimina palabras desconocidas                 # Comentario explicando la siguiente acción
        src_sentence = [w for w in src_sentence if w in self.tm]        # Filtra las palabras de la oración fuente que no están en el modelo de traducción
        
        if not src_sentence:                                              # Si la oración fuente está vacía después del preprocesamiento
            return [], -float('inf')                                     # Retorna una lista vacía y una puntuación de infinito negativo
        
        # Inicializa el haz con oraciones vacías                         # Comentario explicando la siguiente acción
        beam = [([], 0.0)]  # (oración, puntuación)                       # Inicializa el haz con una oración vacía y puntuación 0
        
        for i in range(self.max_len):                                     # Itera hasta la longitud máxima permitida
            new_beam = []                                                 # Inicializa una nueva lista para el siguiente haz
            
            for sentence, score in beam:                                 # Itera sobre cada hipótesis en el haz actual
                # Si la última palabra es </s>, mantenla sin cambios       # Comentario explicando la siguiente acción
                if sentence and sentence[-1] == '</s>':                 # Si la hipótesis actual ya terminó
                    new_beam.append((sentence, score))                   # La mantiene en el nuevo haz
                    continue
                
                # Genera posibles extensiones                             # Comentario explicando la siguiente acción
                for word in self.vocab.union(['</s>']):                 # Itera sobre cada palabra en el vocabulario objetivo más el token de fin
                    new_sent = sentence + [word]                          # Crea una nueva hipótesis extendiendo la actual con la palabra
                    
                    # Calcula puntuación combinada (modelo de lenguaje + traducción) # Comentario explicando la siguiente acción
                    lm_score = self.lm_probability(new_sent)              # Calcula la probabilidad de la nueva hipótesis según el modelo de lenguaje
                    tm_score = 0.0                                        # Inicializa la puntuación del modelo de traducción
                    
                    for src_word in src_sentence:                        # Itera sobre cada palabra en la oración fuente
                        # Probabilidad de traducción suavizada             # Comentario explicando la siguiente acción
                        best_tm = max(self.tm[src_word].get(word, 1e-6) for word in new_sent) # Obtiene la máxima probabilidad de traducción de la palabra fuente a alguna palabra en la hipótesis
                        tm_score += math.log(best_tm)                     # Suma el logaritmo de la mejor probabilidad de traducción
                    
                    # Ponderación de modelos (puede ajustarse)              # Comentario explicando la siguiente acción
                    total_score = 0.7 * lm_score + 0.3 * tm_score          # Combina las puntuaciones del modelo de lenguaje y traducción con pesos
                    new_beam.append((new_sent, total_score))             # Añade la nueva hipótesis y su puntuación al nuevo haz
            
            # Selecciona las mejores hipótesis                             # Comentario explicando la siguiente acción
            beam = sorted(new_beam, key=lambda x: x[1], reverse=True)[:beam_size] # Ordena el nuevo haz por puntuación descendente y selecciona las mejores hipótesis
            
            # Termina si todas las hipótesis terminaron con </s>          # Comentario explicando la siguiente acción
            if all(sent[-1] == '</s>' for sent, _ in beam):             # Verifica si todas las hipótesis en el haz terminan con el token de fin
                break                                                   # Si es así, termina la búsqueda
        
        # Devuelve la mejor traducción                                   # Comentario explicando la siguiente acción
        best_translation, best_score = max(beam, key=lambda x: x[1])    # Selecciona la hipótesis con la mejor puntuación del haz final
        
        # Elimina tokens especiales para la salida final                 # Comentario explicando la siguiente acción
        final_translation = [w for w in best_translation if w not in ['<s>', '</s>']] # Filtra los tokens de inicio y fin de la mejor traducción
        
        return final_translation, best_score                             # Retorna la mejor traducción y su puntuación

    def evaluate_translation(self, references, hypotheses):              # Define el método para evaluar la traducción
        """
        Evalúa la calidad de traducción usando BLEU score simplificado. # Documentación del método
        
        Args:                                                             # Documentación de los argumentos
            references: Lista de listas de referencias (cada referencia es lista de palabras) # Lista de oraciones de referencia (cada una es una lista de posibles traducciones)
            hypotheses: Lista de hipótesis de traducción                 # Lista de oraciones generadas por el sistema de traducción
            
        Returns:                                                          # Documentación del valor de retorno
            float: Puntuación BLEU aproximada                           # La puntuación BLEU promedio para las hipótesis dadas
        """
        total_score = 0.0                                                # Inicializa la puntuación total en 0
        
        for refs, hyp in zip(references, hypotheses):                   # Itera sobre cada par de referencias e hipótesis
            # Precisión de n-gramas (simplificada)                       # Comentario explicando la siguiente acción
            ngram_counts = Counter()                                     # Inicializa un contador para los n-gramas de la hipótesis
            ngram_matches = Counter()                                    # Inicializa un contador para los n-gramas coincidentes
            
            # Calcula para n-gramas de 1 a 4                             # Comentario explicando la siguiente acción
            for n in range(1, 5):                                         # Itera para n-gramas de tamaño 1 a 4
                # Extrae n-gramas de la hipótesis                       # Comentario explicando la siguiente acción
                hyp_ngrams = [tuple(hyp[i:i+n]) for i in range(len(hyp)-n+1)] # Genera todos los n-gramas de la hipótesis
                ngram_counts[n] += len(hyp_ngrams)                       # Incrementa el contador total de n-gramas para este tamaño
                
                # Cuenta matches en las referencias                       # Comentario explicando la siguiente acción
                max_matches = 0                                          # Inicializa el máximo de coincidencias en 0 para las referencias
                for ref in refs:                                         # Itera sobre cada oración de referencia
                    ref_ngrams = [tuple(ref[i:i+n]) for i in range(len(ref)-n+1)] # Genera todos los n-gramas de la referencia
                    matches = sum(1 for ng in hyp_ngrams if ng in ref_ngrams) # Cuenta cuántos n-gramas de la hipótesis están en la referencia
                    max_matches = max(max_matches, matches)             # Actualiza el máximo de coincidencias si es mayor
                    
                ngram_matches[n] += max_matches                         # Incrementa el contador de n-gramas coincidentes
            
            # Calcula BLEU score (simplificado)                          # Comentario explicando la siguiente acción
            precisions = [ngram_matches[n]/ngram_counts[n] for n in range(1,5)] # Calcula la precisión para cada tamaño de n-grama
            bp = min(1, math.exp(1 - len(refs[0])/len(hyp)))             # Calcula la penalización por brevedad (Brevity Penalty)
            bleu = bp * math.exp(sum(math.log(p) for p in precisions) / 4) # Calcula la puntuación BLEU aproximada
            total_score += bleu                                          # Suma la puntuación BLEU de esta hipótesis a la puntuación total
            
        return total_score / len(references)                             # Retorna la puntuación BLEU promedio

# Ejemplo de uso
if __name__ == "__main__":                                               # Bloque que se ejecuta cuando el script se llama directamente
    print("Entrenando modelo de traducción estadística...")             # Imprime un mensaje indicando el inicio del entrenamiento
    
    # 1. Preparar datos de entrenamiento (ejemplo bilingüe español-inglés) # Comentario explicando la siguiente sección
    spanish_sentences = [                                              # Lista de oraciones en español para entrenamiento
        ["el", "gato", "está", "en", "la", "casa"],
        ["el", "perro", "persigue", "al",]
        ]