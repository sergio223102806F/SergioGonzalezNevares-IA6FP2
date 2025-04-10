# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 14:51:17 2025

@author: elvin
"""

import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense, Lambda
from tensorflow.keras.models import Model
from collections import defaultdict, Counter
import matplotlib.pyplot as plt

tfd = tfp.distributions

class ProbabilisticLanguageModel:
    def __init__(self, vocab, phonemes, word_to_phonemes, max_seq_length):
        """
        vocab: Lista de palabras en el vocabulario
        phonemes: Lista de fonemas posibles
        word_to_phonemes: Mapeo de palabras a secuencias fonéticas
        max_seq_length: Longitud máxima de secuencias
        """
        self.vocab = vocab
        self.phonemes = phonemes
        self.word_to_phonemes = word_to_phonemes
        self.max_seq_length = max_seq_length
        
        # Mapeos
        self.word_to_idx = {w:i for i,w in enumerate(vocab)}
        self.idx_to_word = {i:w for i,w in enumerate(vocab)}
        self.phoneme_to_idx = {p:i for i,p in enumerate(phonemes)}
        
        # Hiperparámetros
        self.embed_dim = 64
        self.lstm_units = 128
        self.hidden_dim = 64
        
        # Construir modelos
        self.language_model = self.build_language_model()
        self.pronunciation_model = self.build_pronunciation_model()
        
        # Estadísticas del lenguaje
        self.word_freq = defaultdict(int)
        self.phoneme_transitions = self.calculate_transition_probs()
    
    def build_language_model(self):
        """Modelo de lenguaje neuronal probabilístico"""
        inputs = Input(shape=(self.max_seq_length,))
        
        # Embedding de palabras
        x = Embedding(len(self.vocab), self.embed_dim)(inputs)
        
        # Capa LSTM para contexto temporal
        x = LSTM(self.lstm_units, return_sequences=True)(x)
        
        # Distribución de probabilidad sobre el vocabulario
        word_probs = Dense(len(self.vocab), activation='softmax')(x)
        
        # Distribución categórica
        def output_distribution(params):
            return tfd.Categorical(probs=params)
        
        outputs = Lambda(output_distribution)(word_probs)
        
        model = Model(inputs=inputs, outputs=outputs)
        
        def nll_loss(y_true, y_pred):
            return -y_pred.log_prob(y_true)
        
        model.compile(optimizer='adam', loss=nll_loss)
        
        return model
    
    def build_pronunciation_model(self):
        """Modelo de pronunciación palabra-a-fonemas"""
        inputs = Input(shape=(self.max_seq_length,))
        
        # Embedding de palabras
        x = Embedding(len(self.vocab), self.embed_dim)(inputs)
        
        # Capa LSTM
        x = LSTM(self.lstm_units, return_sequences=True)(x)
        
        # Capa oculta
        x = Dense(self.hidden_dim, activation='relu')(x)
        
        # Salida para cada paso de tiempo
        phoneme_probs = Dense(len(self.phonemes), activation='softmax')(x)
        
        # Distribución de salida
        def output_distribution(params):
            return tfd.Categorical(probs=params)
        
        outputs = Lambda(output_distribution)(phoneme_probs)
        
        model = Model(inputs=inputs, outputs=outputs)
        
        def nll_loss(y_true, y_pred):
            return -y_pred.log_prob(y_true)
        
        model.compile(optimizer='adam', loss=nll_loss)
        
        return model
    
    def calculate_transition_probs(self):
        """Calcula probabilidades de transición entre fonemas"""
        transitions = defaultdict(Counter)
        
        for word, phonemes in self.word_to_phonemes.items():
            for i in range(len(phonemes)-1):
                current = phonemes[i]
                next_p = phonemes[i+1]
                transitions[current][next_p] += 1
        
        # Normalizar a probabilidades
        probs = {}
        for current, counts in transitions.items():
            total = sum(counts.values())
            probs[current] = {next_p: count/total for next_p, count in counts.items()}
        
        return probs
    
    def update_language_stats(self, text_corpus):
        """Actualiza estadísticas del lenguaje con nuevo texto"""
        for sentence in text_corpus:
            words = sentence.split()
            for word in words:
                self.word_freq[word] += 1
    
    def predict_next_word(self, context_words, num_candidates=5):
        """Predice siguiente palabra dado un contexto"""
        # Convertir contexto a índices
        context_idx = [self.word_to_idx[w] for w in context_words if w in self.word_to_idx]
        
        if not context_idx:
            # Si no hay contexto, devolver palabras más frecuentes
            return sorted(self.word_freq.items(), key=lambda x: -x[1])[:num_candidates]
        
        # Padding del contexto
        context_padded = tf.keras.preprocessing.sequence.pad_sequences(
            [context_idx], maxlen=self.max_seq_length, padding='pre')
        
        # Obtener predicciones
        preds = self.language_model(context_padded).mean().numpy()[0][-1]
        
        # Obtener candidatos más probables
        top_indices = np.argsort(preds)[-num_candidates:][::-1]
        return [(self.idx_to_word[i], preds[i]) for i in top_indices]
    
    def word_to_phoneme_prob(self, word):
        """Convierte palabra a fonemas con probabilidades"""
        if word not in self.word_to_idx:
            return None
        
        # Obtener índice de la palabra
        word_idx = self.word_to_idx[word]
        word_input = tf.keras.preprocessing.sequence.pad_sequences(
            [[word_idx]], maxlen=self.max_seq_length)
        
        # Obtener distribución de fonemas
        phoneme_dist = self.pronunciation_model(word_input).mean().numpy()[0]
        
        # Secuencia más probable
        phoneme_seq = []
        for t in range(phoneme_dist.shape[0]):
            if np.max(phoneme_dist[t]) > 0.1:  # Umbral
                phoneme_idx = np.argmax(phoneme_dist[t])
                phoneme_seq.append(self.phonemes[phoneme_idx])
        
        return phoneme_seq, phoneme_dist
    
    def recognize_speech(self, audio_features, acoustic_model, context=None, beam_width=3):
        """
        Reconoce habla integrando:
        - audio_features: Características acústicas del modelo acústico
        - acoustic_model: Modelo que mapea audio a fonemas
        - context: Contexto lingüístico previo
        - beam_width: Ancho del beam search