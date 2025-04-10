# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 14:38:41 2025

@author: elvin
"""
import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense, Lambda
from tensorflow.keras.callbacks import EarlyStopping
from collections import Counter
import matplotlib.pyplot as plt

tfd = tfp.distributions

class DeepSpeechRecognition:
    def __init__(self, phonemes, words, max_seq_length):
        """
        phonemes: Lista de fonemas posibles
        words: Diccionario {palabra: [secuencia de fonemas]}
        max_seq_length: Longitud máxima de secuencia de entrada
        """
        self.phonemes = phonemes
        self.words = words
        self.max_seq_length = max_seq_length
        self.phoneme_to_idx = {p:i for i,p in enumerate(phonemes)}
        self.idx_to_phoneme = {i:p for i,p in enumerate(phonemes)}
        self.word_to_phonemes = words
        
        # Hiperparámetros del modelo
        self.embedding_dim = 64
        self.lstm_units = 128
        self.hidden_dim = 64
        
        # Construir el modelo
        self.model = self.build_probabilistic_model()
    
    def build_probabilistic_model(self):
        """Construye un modelo de aprendizaje profundo probabilístico"""
        # Entrada para características acústicas (ej: MFCCs)
        input_features = Input(shape=(self.max_seq_length, 13), name='input_features')
        
        # Capa de embedding para características acústicas
        x = Dense(self.embedding_dim, activation='relu')(input_features)
        
        # Capa LSTM para modelar dependencias temporales
        x = LSTM(self.lstm_units, return_sequences=True)(x)
        
        # Capa oculta
        x = Dense(self.hidden_dim, activation='relu')(x)
        
        # Salida probabilística para cada paso de tiempo
        phoneme_probs = Dense(len(self.phonemes), activation='softmax', name='phoneme_probs')(x)
        
        # Capa de distribución de probabilidad
        def phoneme_distribution(params):
            return tfd.Categorical(probs=params, name='phoneme_distribution')
        
        phoneme_output = Lambda(lambda x: phoneme_distribution(x), name='phoneme_output')(phoneme_probs)
        
        # Modelo completo
        model = Model(inputs=input_features, outputs=phoneme_output)
        
        # Función de pérdida personalizada para la distribución
        def neg_log_likelihood(y_true, y_pred):
            return -y_pred.log_prob(y_true)
        
        # Compilar el modelo
        model.compile(optimizer='adam', loss=neg_log_likelihood, metrics=['accuracy'])
        
        return model
    
    def preprocess_data(self, audio_features, phoneme_sequences):
        """
        Preprocesa datos para entrenamiento:
        - audio_features: Lista de arrays con características acústicas (ej: MFCCs)
        - phoneme_sequences: Lista de secuencias de fonemas correspondientes
        """
        # Padding de secuencias
        X = tf.keras.preprocessing.sequence.pad_sequences(
            audio_features, maxlen=self.max_seq_length, padding='post', dtype='float32')
        
        # Convertir fonemas a índices
        y = [[self.phoneme_to_idx[p] for p in seq] for seq in phoneme_sequences]
        y = tf.keras.preprocessing.sequence.pad_sequences(
            y, maxlen=self.max_seq_length, padding='post', value=-1)
        
        return X, y
    
    def train(self, X_train, y_train, X_val=None, y_val=None, epochs=50, batch_size=32):
        """Entrena el modelo"""
        early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
        
        callbacks = [early_stopping] if X_val is not None else []
        
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val) if X_val is not None else None,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks
        )
        
        return history
    
    def predict_phonemes(self, audio_features):
        """Predice secuencia de fonemas para características de audio dadas"""
        # Preprocesar entrada
        X = tf.keras.preprocessing.sequence.pad_sequences(
            [audio_features], maxlen=self.max_seq_length, padding='post', dtype='float32')
        
        # Obtener probabilidades
        probs = self.model.predict(X)[0]
        
        # Obtener fonemas más probables
        phoneme_indices = np.argmax(probs, axis=-1)
        phoneme_sequence = [self.idx_to_phoneme[idx] for idx in phoneme_indices if idx != -1]
        
        return phoneme_sequence, probs
    
    def predict_words(self, audio_features):
        """Reconstruye palabras a partir de la secuencia de fonemas predicha"""
        phoneme_sequence, _ = self.predict_phonemes(audio_features)
        
        # Reconstruir palabras usando algoritmo de coincidencia aproximada
        recognized_words = []
        current_pos = 0
        
        while current_pos < len(phoneme_sequence):
            best_match = None
            best_match_length = 0
            
            # Buscar la palabra más larga que coincida
            for word, word_phonemes in self.word_to_phonemes.items():
                word_length = len(word_phonemes)
                if current_pos + word_length > len(phoneme_sequence):
                    continue
                
                match = True
                for i in range(word_length):
                    if phoneme_sequence[current_pos + i] != word_phonemes[i]:
                        match = False
                        break
                
                if match and word_length > best_match_length:
                    best_match = word
                    best_match_length = word_length
            
            if best_match:
                recognized_words.append(best_match)
                current_pos += best_match_length
            else:
                current_pos += 1
        
        return recognized_words, phoneme_sequence
    
    def uncertainty_estimation(self, audio_features, num_samples=10):
        """Estima incertidumbre usando muestreo Monte Carlo"""
        X = tf.keras.preprocessing.sequence.pad_sequences(
            [audio_features], maxlen=self.max_seq_length, padding='post', dtype='float32')
        
        # Crear modelo que devuelva las probabilidades en lugar de la distribución
        prob_model = Model(inputs=self.model.inputs, 
                         outputs=self.model.get_layer('phoneme_probs').output)
        
        # Muestrear varias veces (simulando dropout durante la inferencia)
        sampled_probs = []
        for _ in range(num_samples):
            sampled_probs.append(prob_model.predict(X)[0])
        
        sampled_probs = np.array(sampled_probs)
        
        # Calcular estadísticas de incertidumbre
        mean_probs = np.mean(sampled_probs, axis=0)
        std_probs = np.std(sampled_probs, axis=0)
        entropy = -np.sum(mean_probs * np.log(mean_probs + 1e-10), axis=-1)
        
        return {
            'mean_probs': mean_probs,
            'std_probs': std_probs,
            'entropy': entropy
        }

# Ejemplo de uso
if __name__ == "__main__":
    # Configuración del ejemplo
    phonemes = ['p', 'a', 't', 'e', 'l', 'o', 'm', 'n', 's', 'i']
    words = {
        'pat': ['p', 'a', 't'],
        'pato': ['p', 'a', 't', 'o'],
        'tel': ['t', 'e', 'l'],
        'mesa': ['m', 'e', 's', 'a'],
        'limon': ['l', 'i', 'm', 'o', 'n']
    }
    max_seq_length = 20
    
    # Crear reconocedor
    recognizer = DeepSpeechRecognition(phonemes, words, max_seq_length)
    
    # Mostrar arquitectura del modelo
    recognizer.model.summary()
    
    # Generar datos de ejemplo (en la práctica, usar datos reales)
    def generate_example_data(num_samples=100):
        X = []
        y = []
        
        for _ in range(num_samples):
            # Seleccionar palabra aleatoria
            word = random.choice(list(words.keys()))
            phoneme_seq = words[word]
            
            # Generar características acústicas aleatorias (simuladas)
            # En la práctica, usar MFCCs u otras características reales
            audio_features = np.random.randn(len(phoneme_seq), 13)
            
            X.append(audio_features)
            y.append(phoneme_seq)
        
        return X, y
    
    X_train, y_train = generate_example_data(200)
    X_val, y_val = generate_example_data(50)
    
    # Preprocesar datos
    X_train_prep, y_train_prep = recognizer.preprocess_data(X_train, y_train)
    X_val_prep, y_val_prep = recognizer.preprocess_data(X_val, y_val)
    
    # Entrenar modelo
    history = recognizer.train(X_train_prep, y_train_prep, X_val_prep, y_val_prep, epochs=30)
    
    # Visualizar entrenamiento
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()
    
    # Probar reconocimiento
    test_word = 'pato'
    test_phonemes = words[test_word]
    test_audio = np.random.randn(len(test_phonemes), 13)  # Simular características
    
    # Realizar predicción
    predicted_words, predicted_phonemes = recognizer.predict_words(test_audio)
    print(f"\nPalabra original: {test_word} ({' '.join(test_phonemes)})")
    print(f"Palabra reconocida: {predicted_words} ({' '.join(predicted_phonemes)})")
    
    # Estimar incertidumbre
    uncertainty = recognizer.uncertainty_estimation(test_audio)
    print("\nIncertidumbre en las predicciones:")
    for i, phoneme in enumerate(predicted_phonemes):
        print(f"{phoneme}: Entropía={uncertainty['entropy'][i]:.3f}, Std={np.mean(uncertainty['std_probs'][i]):.3f}")