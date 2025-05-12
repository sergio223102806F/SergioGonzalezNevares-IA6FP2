# -*- coding: utf-8 -*-
"""
Script para modelo de lenguaje probabilístico con capacidades de pronunciación
Created on Wed Apr  9 14:51:17 2025
@author: elvin
"""

# Importación de librerías numéricas y de deep learning
import numpy as np  # Para operaciones numéricas
import tensorflow as tf  # Framework de deep learning
import tensorflow_probability as tfp  # Extensiones probabilísticas de TensorFlow

# Importación de capas y modelos de Keras
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense, Lambda  # Capas de red neuronal
from tensorflow.keras.models import Model  # Clase para construir modelos

# Importación de estructuras de datos y visualización
from collections import defaultdict, Counter  # Para conteos y mapeos
import matplotlib.pyplot as plt  # Para visualización

# Alias corto para distribuciones de TensorFlow Probability
tfd = tfp.distributions

class ProbabilisticLanguageModel:
    def __init__(self, vocab, phonemes, word_to_phonemes, max_seq_length):
        """
        Inicializa el modelo probabilístico de lenguaje y pronunciación
        
        Args:
            vocab: Lista de palabras en el vocabulario
            phonemes: Lista de fonemas posibles
            word_to_phonemes: Diccionario {palabra: [fonemas]}
            max_seq_length: Máxima longitud de secuencias de entrada
        """
        # Vocabulario y datos lingüísticos
        self.vocab = vocab  # Lista de palabras conocidas
        self.phonemes = phonemes  # Lista de fonemas posibles
        self.word_to_phonemes = word_to_phonemes  # Mapeo palabra-fonemas
        self.max_seq_length = max_seq_length  # Longitud máxima de secuencias
        
        # Mapeos de palabras y fonemas a índices numéricos
        self.word_to_idx = {w:i for i,w in enumerate(vocab)}  # Diccionario palabra->índice
        self.idx_to_word = {i:w for i,w in enumerate(vocab)}  # Diccionario índice->palabra
        self.phoneme_to_idx = {p:i for i,p in enumerate(phonemes)}  # Diccionario fonema->índice
        
        # Hiperparámetros del modelo
        self.embed_dim = 64  # Dimensión del embedding de palabras
        self.lstm_units = 128  # Unidades en capa LSTM
        self.hidden_dim = 64  # Dimensión de capa oculta
        
        # Construcción de los modelos
        self.language_model = self.build_language_model()  # Modelo de lenguaje
        self.pronunciation_model = self.build_pronunciation_model()  # Modelo de pronunciación
        
        # Estadísticas lingüísticas
        self.word_freq = defaultdict(int)  # Frecuencias de palabras
        self.phoneme_transitions = self.calculate_transition_probs()  # Probabilidades de transición fonémica
    
    def build_language_model(self):
        """Construye el modelo neuronal de lenguaje probabilístico"""
        # Capa de entrada para índices de palabras
        inputs = Input(shape=(self.max_seq_length,))
        
        # Capa de embedding para representar palabras como vectores
        x = Embedding(len(self.vocab), self.embed_dim)(inputs)
        
        # Capa LSTM para capturar dependencias temporales
        x = LSTM(self.lstm_units, return_sequences=True)(x)
        
        # Capa densa con softmax para distribución de probabilidad
        word_probs = Dense(len(self.vocab), activation='softmax')(x)
        
        # Función para convertir salida en distribución probabilística
        def output_distribution(params):
            return tfd.Categorical(probs=params)
        
        # Capa Lambda para aplicar la conversión a distribución
        outputs = Lambda(output_distribution)(word_probs)
        
        # Construcción del modelo completo
        model = Model(inputs=inputs, outputs=outputs)
        
        # Función de pérdida (negative log-likelihood)
        def nll_loss(y_true, y_pred):
            return -y_pred.log_prob(y_true)
        
        # Compilación del modelo con optimizador Adam
        model.compile(optimizer='adam', loss=nll_loss)
        
        return model
    
    def build_pronunciation_model(self):
        """Construye modelo para mapear palabras a fonemas"""
        # Capa de entrada para índices de palabras
        inputs = Input(shape=(self.max_seq_length,))
        
        # Capa de embedding para palabras
        x = Embedding(len(self.vocab), self.embed_dim)(inputs)
        
        # Capa LSTM para secuencias fonéticas
        x = LSTM(self.lstm_units, return_sequences=True)(x)
        
        # Capa densa oculta con activación ReLU
        x = Dense(self.hidden_dim, activation='relu')(x)
        
        # Capa de salida con softmax para probabilidades de fonemas
        phoneme_probs = Dense(len(self.phonemes), activation='softmax')(x)
        
        # Conversión a distribución probabilística
        def output_distribution(params):
            return tfd.Categorical(probs=params)
        
        # Capa Lambda para salida distribucional
        outputs = Lambda(output_distribution)(phoneme_probs)
        
        # Construcción del modelo completo
        model = Model(inputs=inputs, outputs=outputs)
        
        # Función de pérdida (negative log-likelihood)
        def nll_loss(y_true, y_pred):
            return -y_pred.log_prob(y_true)
        
        # Compilación del modelo
        model.compile(optimizer='adam', loss=nll_loss)
        
        return model
    
    def calculate_transition_probs(self):
        """Calcula probabilidades de transición entre fonemas"""
        transitions = defaultdict(Counter)  # Diccionario para conteos de transiciones
        
        # Contar transiciones entre fonemas en todas las palabras
        for word, phonemes in self.word_to_phonemes.items():
            for i in range(len(phonemes)-1):
                current = phonemes[i]  # Fonema actual
                next_p = phonemes[i+1]  # Fonema siguiente
                transitions[current][next_p] += 1  # Incrementar conteo
        
        # Normalizar conteos a probabilidades
        probs = {}
        for current, counts in transitions.items():
            total = sum(counts.values())  # Total de ocurrencias del fonema actual
            probs[current] = {next_p: count/total for next_p, count in counts.items()}
        
        return probs
    
    def update_language_stats(self, text_corpus):
        """Actualiza estadísticas de frecuencia de palabras"""
        for sentence in text_corpus:
            words = sentence.split()  # Dividir texto en palabras
            for word in words:
                self.word_freq[word] += 1  # Incrementar conteo de palabra
    
    def predict_next_word(self, context_words, num_candidates=5):
        """Predice la siguiente palabra dado un contexto"""
        # Convertir palabras de contexto a índices
        context_idx = [self.word_to_idx[w] for w in context_words if w in self.word_to_idx]
        
        # Si no hay contexto válido, devolver palabras más frecuentes
        if not context_idx:
            return sorted(self.word_freq.items(), key=lambda x: -x[1])[:num_candidates]
        
        # Aplicar padding al contexto para longitud fija
        context_padded = tf.keras.preprocessing.sequence.pad_sequences(
            [context_idx], maxlen=self.max_seq_length, padding='pre')
        
        # Obtener predicciones del modelo
        preds = self.language_model(context_padded).mean().numpy()[0][-1]
        
        # Obtener índices de las palabras más probables
        top_indices = np.argsort(preds)[-num_candidates:][::-1]
        
        # Devolver palabras y sus probabilidades
        return [(self.idx_to_word[i], preds[i]) for i in top_indices]
    
    def word_to_phoneme_prob(self, word):
        """Convierte una palabra a su secuencia fonética con probabilidades"""
        # Verificar si la palabra está en el vocabulario
        if word not in self.word_to_idx:
            return None
        
        # Obtener índice de la palabra y aplicar padding
        word_idx = self.word_to_idx[word]
        word_input = tf.keras.preprocessing.sequence.pad_sequences(
            [[word_idx]], maxlen=self.max_seq_length)
        
        # Obtener distribución de fonemas del modelo
        phoneme_dist = self.pronunciation_model(word_input).mean().numpy()[0]
        
        # Construir secuencia más probable de fonemas
        phoneme_seq = []
        for t in range(phoneme_dist.shape[0]):
            # Usar umbral para descartar predicciones débiles
            if np.max(phoneme_dist[t]) > 0.1:
                phoneme_idx = np.argmax(phoneme_dist[t])
                phoneme_seq.append(self.phonemes[phoneme_idx])
        
        return phoneme_seq, phoneme_dist
    
    def recognize_speech(self, audio_features, acoustic_model, context=None, beam_width=3):
        """
        Integra modelo acústico y de lenguaje para reconocimiento de voz
        
        Args:
            audio_features: Características acústicas extraídas del audio
            acoustic_model: Modelo que mapea audio a fonemas
            context: Contexto lingüístico previo (opcional)
            beam_width: Ancho para beam search (búsqueda por haz)
        """
        # Implementación de reconocimiento de voz integrado
        # (Nota: El código completo de esta función no estaba incluido en el original)