# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 14:44:30 2025

@author: elvin
"""

import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv1D, LSTM, Dense, Dropout, Bidirectional
from tensorflow.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt

tfd = tfp.distributions

class NeuralSpeechRecognizer:
    def __init__(self, phonemes, words, max_seq_length, acoustic_dim=13):
        """
        phonemes: Lista de fonemas
        words: Diccionario de palabras a fonemas
        max_seq_length: Máxima longitud de secuencia
        acoustic_dim: Dimensiones de características acústicas (MFCCs)
        """
        self.phonemes = phonemes
        self.words = words
        self.max_seq_length = max_seq_length
        self.acoustic_dim = acoustic_dim
        
        # Mapeos de fonemas
        self.phoneme_to_idx = {p:i for i,p in enumerate(phonemes)}
        self.idx_to_phoneme = {i:p for i,p in enumerate(phonemes)}
        
        # Construir modelo
        self.model = self.build_probabilistic_model()
    
    def build_probabilistic_model(self):
        """Construye red neuronal con salida probabilística"""
        # Entrada para características acústicas
        inputs = Input(shape=(self.max_seq_length, self.acoustic_dim))
        
        # Capa convolucional para extraer patrones locales
        x = Conv1D(64, 5, activation='relu', padding='same')(inputs)
        x = Dropout(0.3)(x)
        
        # Capa Bidireccional LSTM para contexto temporal
        x = Bidirectional(LSTM(128, return_sequences=True))(x)
        x = Dropout(0.4)(x)
        
        # Capa densa intermedia
        x = Dense(64, activation='relu')(x)
        
        # Salida probabilística
        phoneme_probs = Dense(len(self.phonemes), activation='softmax')(x)
        
        # Distribución categórica para cada paso de tiempo
        def output_distribution(params):
            return tfd.Categorical(probs=params)
        
        outputs = Lambda(output_distribution)(phoneme_probs)
        
        # Modelo completo
        model = Model(inputs=inputs, outputs=outputs)
        
        # Función de pérdida personalizada
        def nll_loss(y_true, y_pred):
            return -y_pred.log_prob(y_true)
        
        # Compilar modelo
        model.compile(optimizer=tf.keras.optimizers.Adam(0.001),
                     loss=nll_loss,
                     metrics=['accuracy'])
        
        return model
    
    def preprocess_data(self, audio_features, phoneme_sequences):
        """Preprocesa datos para entrenamiento"""
        # Padding de características acústicas
        X = tf.keras.preprocessing.sequence.pad_sequences(
            audio_features, 
            maxlen=self.max_seq_length, 
            padding='post', 
            dtype='float32'
        )
        
        # Convertir secuencias de fonemas a índices
        y = [[self.phoneme_to_idx[p] for p in seq] for seq in phoneme_sequences]
        y = tf.keras.preprocessing.sequence.pad_sequences(
            y, 
            maxlen=self.max_seq_length, 
            padding='post', 
            value=-1
        )
        
        return X, y
    
    def train(self, X_train, y_train, X_val=None, y_val=None, epochs=50, batch_size=32):
        """Entrena el modelo"""
        early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
        
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val) if X_val is not None else None,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stop] if X_val is not None else None,
            verbose=1
        )
        
        return history
    
    def predict_phonemes(self, audio_features):
        """Predice fonemas para características dadas"""
        # Preprocesamiento
        X = tf.keras.preprocessing.sequence.pad_sequences(
            [audio_features], 
            maxlen=self.max_seq_length, 
            padding='post', 
            dtype='float32'
        )
        
        # Obtener probabilidades
        probs = self.model(X).mean().numpy()[0]
        
        # Secuencia más probable
        phoneme_indices = np.argmax(probs, axis=-1)
        phoneme_sequence = [self.idx_to_phoneme[idx] for idx in phoneme_indices if idx != -1]
        
        return phoneme_sequence, probs
    
    def predict_words(self, audio_features):
        """Reconoce palabras completas"""
        phonemes, _ = self.predict_phonemes(audio_features)
        
        # Algoritmo de búsqueda de palabras
        recognized_words = []
        buffer = []
        
        for phoneme in phonemes:
            buffer.append(phoneme)
            
            # Verificar palabras conocidas
            for word, word_phonemes in self.words.items():
                if buffer == word_phonemes:
                    recognized_words.append(word)
                    buffer = []
                    break
        
        return recognized_words, phonemes
    
    def uncertainty_analysis(self, audio_features, num_samples=100):
        """Analiza incertidumbre usando Dropout como aproximación bayesiana"""
        # Activar dropout durante inferencia
        logits = []
        for _ in range(num_samples):
            logits.append(self.model(audio_features[np.newaxis, ...]).mean().numpy())
        
        logits = np.array(logits)
        mean_probs = tf.nn.softmax(np.mean(logits, axis=0)).numpy()[0]
        std_probs = tf.nn.softmax(np.std(logits, axis=0)).numpy()[0]
        
        return {
            'mean_probs': mean_probs,
            'std_probs': std_probs,
            'entropy': -np.sum(mean_probs * np.log(mean_probs + 1e-10), axis=-1)
        }

# Ejemplo de uso
if __name__ == "__main__":
    # Configuración
    phonemes = ['p', 'a', 't', 'e', 'l', 'o', 'm', 'n', 's', 'i', 'd', 'r']
    words = {
        'pato': ['p', 'a', 't', 'o'],
        'mesa': ['m', 'e', 's', 'a'],
        'limon': ['l', 'i', 'm', 'o', 'n'],
        'radio': ['r', 'a', 'd', 'i', 'o']
    }
    max_seq_length = 30
    
    # Crear reconocedor
    recognizer = NeuralSpeechRecognizer(phonemes, words, max_seq_length)
    
    # Generar datos de ejemplo (simulado)
    def generate_mfccs(length):
        return np.random.normal(size=(length, 13))
    
    X_train = [generate_mfccs(np.random.randint(5, 15)) for _ in range(200)]
    y_train = [random.choice(list(words.values())) for _ in range(200)]
    
    X_val = [generate_mfccs(np.random.randint(5, 15)) for _ in range(50)]
    y_val = [random.choice(list(words.values())) for _ in range(50)]
    
    # Preprocesar
    X_train_prep, y_train_prep = recognizer.preprocess_data(X_train, y_train)
    X_val_prep, y_val_prep = recognizer.preprocess_data(X_val, y_val)
    
    # Entrenar
    history = recognizer.train(X_train_prep, y_train_prep, X_val_prep, y_val_prep, epochs=30)
    
    # Visualizar entrenamiento
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Entrenamiento')
    plt.plot(history.history['val_loss'], label='Validación')
    plt.title('Pérdida')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history['accuracy'], label='Entrenamiento')
    plt.plot(history.history['val_accuracy'], label='Validación')
    plt.title('Precisión')
    plt.legend()
    plt.show()
    
    # Probar reconocimiento
    test_word = 'pato'
    test_audio = generate_mfccs(len(words[test_word]))
    
    words_pred, phonemes_pred = recognizer.predict_words(test_audio)
    print(f"\nPalabra original: {test_word} ({' '.join(words[test_word])})")
    print(f"Palabra reconocida: {words_pred} ({' '.join(phonemes_pred)})")
    
    # Análisis de incertidumbre
    uncertainty = recognizer.uncertainty_analysis(test_audio)
    print("\nAnálisis de incertidumbre:")
    for i, phoneme in enumerate(phonemes_pred):
        print(f"{phoneme}:")
        print(f"  Entropía: {uncertainty['entropy'][i]:.3f}")
        print(f"  Desviación estándar: {np.mean(uncertainty['std_probs'][i]):.3f}")