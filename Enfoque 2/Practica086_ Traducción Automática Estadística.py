# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 13:43:57 2025

@author: elvin
"""

"""
Sistema de Traducción Automática Estadística (Statistical Machine Translation - SMT)

Este sistema implementa un modelo de traducción basado en:
1. Modelo de lenguaje (n-gramas)
2. Modelo de traducción (alineamiento de palabras)
3. Decodificación (búsqueda del mejor candidato)
"""

import math
from collections import defaultdict, Counter
from itertools import permutations
import numpy as np

class StatisticalMT:
    def __init__(self):
        """
        Inicializa el sistema de traducción estadística.
        
        Atributos:
        - lm: Modelo de lenguaje (frecuencias de n-gramas)
        - tm: Modelo de traducción (probabilidades léxicas)
        - vocab: Vocabulario del lenguaje objetivo
        - max_len: Longitud máxima de frase permitida
        """
        self.lm = defaultdict(Counter)  # Modelo de lenguaje (n-gramas)
        self.tm = defaultdict(dict)     # Modelo de traducción {src_word: {tgt_word: prob}}
        self.vocab = set()             # Vocabulario del lenguaje objetivo
        self.max_len = 20              # Longitud máxima de frase a traducir

    def train_language_model(self, sentences, n=3):
        """
        Entrena un modelo de lenguaje n-grama.
        
        Args:
            sentences: Lista de oraciones (cada oración es lista de palabras)
            n: Orden del n-grama (por defecto trigramas)
        """
        for sentence in sentences:
            # Prepara la oración con tokens de inicio/fin
            padded = ['<s>'] * (n-1) + sentence + ['</s>']
            
            # Calcula n-gramas para la oración actual
            for i in range(len(padded) - n + 1):
                # El contexto son las n-1 palabras anteriores
                context = tuple(padded[i:i+n-1])
                # La palabra objetivo es la siguiente
                word = padded[i+n-1]
                # Actualiza el contador para este n-grama
                self.lm[context][word] += 1
        
        # Convierte conteos a probabilidades (suavizado add-one)
        for context in self.lm:
            total = sum(self.lm[context].values()) + len(self.lm[context])
            for word in self.lm[context]:
                self.lm[context][word] = (self.lm[context][word] + 1) / total
        
        # Actualiza el vocabulario
        self.vocab = set(word for context in self.lm for word in self.lm[context])

    def train_translation_model(self, src_sentences, tgt_sentences):
        """
        Entrena el modelo de traducción usando conteos de alineamiento.
        
        Args:
            src_sentences: Lista de oraciones en lenguaje fuente
            tgt_sentences: Lista de oraciones en lenguaje objetivo
        """
        # Primero cuenta co-ocurrencias de palabras
        cooc_counts = defaultdict(Counter)
        src_vocab = set()
        
        for src_sent, tgt_sent in zip(src_sentences, tgt_sentences):
            for src_word in src_sent:
                src_vocab.add(src_word)
                for tgt_word in tgt_sent:
                    cooc_counts[src_word][tgt_word] += 1
        
        # Calcula probabilidades léxicas P(tgt|src)
        for src_word in cooc_counts:
            total = sum(cooc_counts[src_word].values())
            for tgt_word in cooc_counts[src_word]:
                self.tm[src_word][tgt_word] = cooc_counts[src_word][tgt_word] / total

    def lm_probability(self, sentence, n=3):
        """
        Calcula la probabilidad logarítmica de una oración según el modelo de lenguaje.
        
        Args:
            sentence: Lista de palabras de la oración
            n: Orden del n-grama
            
        Returns:
            float: Log probabilidad de la oración
        """
        padded = ['<s>'] * (n-1) + sentence + ['</s>']
        log_prob = 0.0
        
        for i in range(len(padded) - n + 1):
            context = tuple(padded[i:i+n-1])
            word = padded[i+n-1]
            
            # Probabilidad suavizada para palabras desconocidas
            prob = self.lm[context].get(word, 1 / (sum(self.lm[context].values()) + len(self.vocab)))
            log_prob += math.log(prob)
            
        return log_prob

    def translate_sentence(self, src_sentence, beam_size=5):
        """
        Traduce una oración usando búsqueda por haz (beam search).
        
        Args:
            src_sentence: Lista de palabras de la oración fuente
            beam_size: Tamaño del haz para la búsqueda
            
        Returns:
            tuple: (oración traducida, puntuación)
        """
        # Preprocesamiento: elimina palabras desconocidas
        src_sentence = [w for w in src_sentence if w in self.tm]
        
        if not src_sentence:
            return [], -float('inf')
        
        # Inicializa el haz con oraciones vacías
        beam = [([], 0.0)]  # (oración, puntuación)
        
        for i in range(self.max_len):
            new_beam = []
            
            for sentence, score in beam:
                # Si la última palabra es </s>, mantenla sin cambios
                if sentence and sentence[-1] == '</s>':
                    new_beam.append((sentence, score))
                    continue
                
                # Genera posibles extensiones
                for word in self.vocab.union(['</s>']):
                    new_sent = sentence + [word]
                    
                    # Calcula puntuación combinada (modelo de lenguaje + traducción)
                    lm_score = self.lm_probability(new_sent)
                    tm_score = 0.0
                    
                    for src_word in src_sentence:
                        # Probabilidad de traducción suavizada
                        best_tm = max(self.tm[src_word].get(word, 1e-6) for word in new_sent)
                        tm_score += math.log(best_tm)
                    
                    # Ponderación de modelos (puede ajustarse)
                    total_score = 0.7 * lm_score + 0.3 * tm_score
                    new_beam.append((new_sent, total_score))
            
            # Selecciona las mejores hipótesis
            beam = sorted(new_beam, key=lambda x: x[1], reverse=True)[:beam_size]
            
            # Termina si todas las hipótesis terminaron con </s>
            if all(sent[-1] == '</s>' for sent, _ in beam):
                break
        
        # Devuelve la mejor traducción
        best_translation, best_score = max(beam, key=lambda x: x[1])
        
        # Elimina tokens especiales para la salida final
        final_translation = [w for w in best_translation if w not in ['<s>', '</s>']]
        
        return final_translation, best_score

    def evaluate_translation(self, references, hypotheses):
        """
        Evalúa la calidad de traducción usando BLEU score simplificado.
        
        Args:
            references: Lista de listas de referencias (cada referencia es lista de palabras)
            hypotheses: Lista de hipótesis de traducción
            
        Returns:
            float: Puntuación BLEU aproximada
        """
        total_score = 0.0
        
        for refs, hyp in zip(references, hypotheses):
            # Precisión de n-gramas (simplificada)
            ngram_counts = Counter()
            ngram_matches = Counter()
            
            # Calcula para n-gramas de 1 a 4
            for n in range(1, 5):
                # Extrae n-gramas de la hipótesis
                hyp_ngrams = [tuple(hyp[i:i+n]) for i in range(len(hyp)-n+1)]
                ngram_counts[n] += len(hyp_ngrams)
                
                # Cuenta matches en las referencias
                max_matches = 0
                for ref in refs:
                    ref_ngrams = [tuple(ref[i:i+n]) for i in range(len(ref)-n+1)]
                    matches = sum(1 for ng in hyp_ngrams if ng in ref_ngrams)
                    max_matches = max(max_matches, matches)
                
                ngram_matches[n] += max_matches
            
            # Calcula BLEU score (simplificado)
            precisions = [ngram_matches[n]/ngram_counts[n] for n in range(1,5)]
            bp = min(1, math.exp(1 - len(refs[0])/len(hyp)))  # Penalización por brevedad
            bleu = bp * math.exp(sum(math.log(p) for p in precisions) / 4)
            total_score += bleu
        
        return total_score / len(references)

# Ejemplo de uso
if __name__ == "__main__":
    print("Entrenando modelo de traducción estadística...")
    
    # 1. Preparar datos de entrenamiento (ejemplo bilingüe español-inglés)
    spanish_sentences = [
        ["el", "gato", "está", "en", "la", "casa"],
        ["el", "perro", "persigue", "al", "gato"],
        ["la", "casa", "es", "grande"]
    ]
    
    english_sentences = [
        ["the", "cat", "is", "in", "the", "house"],
        ["the", "dog", "chases", "the", "cat"],
        ["the", "house", "is", "big"]
    ]
    
    # 2. Crear e instanciar el modelo
    smt = StatisticalMT()
    
    # 3. Entrenar modelos
    smt.train_language_model(english_sentences, n=3)  # Modelo de lenguaje inglés
    smt.train_translation_model(spanish_sentences, english_sentences)  # Modelo de traducción
    
    # 4. Probar traducción
    test_sentence = ["el", "gato", "persigue", "al", "perro"]
    translation, score = smt.translate_sentence(test_sentence)
    
    print(f"\nOración fuente: {' '.join(test_sentence)}")
    print(f"Traducción: {' '.join(translation)}")
    print(f"Puntuación: {score:.2f}")
    
    # 5. Evaluación (con datos de prueba)
    references = [
        [["the", "cat", "chases", "the", "dog"]],
        [["the", "dog", "chases", "the", "cat"]]
    ]
    hypotheses = [
        ["the", "cat", "follows", "the", "dog"],
        ["the", "dog", "runs", "after", "the", "cat"]
    ]
    
    bleu_score = smt.evaluate_translation(references, hypotheses)
    print(f"\nBLEU score promedio: {bleu_score:.4f}")