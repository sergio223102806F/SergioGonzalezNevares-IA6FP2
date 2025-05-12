# -*- coding: utf-8 -*-
"""
Script para reconocimiento de voz profundo con capacidades probabilísticas
Creado el Miércoles 9 de Abril 2025
Autor: elvin
"""

# Importación de la librería numpy para operaciones numéricas
import numpy as np

# Importación del framework TensorFlow para deep learning
import tensorflow as tf

# Importación de TensorFlow Probability para modelos probabilísticos
import tensorflow_probability as tfp

# Importación de la clase Model de Keras para construir modelos
from tensorflow.keras.models import Model

# Importación de capas específicas de Keras
from tensorflow.keras.layers import Input  # Capa de entrada
from tensorflow.keras.layers import LSTM  # Capa LSTM para secuencias
from tensorflow.keras.layers import Dense  # Capa densa completamente conectada
from tensorflow.keras.layers import Lambda  # Capa para operaciones personalizadas

# Importación de callback para detención temprana
from tensorflow.keras.callbacks import EarlyStopping

# Importación de Counter para conteo de frecuencias
from collections import Counter

# Importación de pyplot para visualización
import matplotlib.pyplot as plt

# Alias para el módulo de distribuciones de TensorFlow Probability
tfd = tfp.distributions

# Definición de la clase principal del reconocedor de voz
class DeepSpeechRecognition:
    # Método constructor de la clase
    def __init__(self, phonemes, words, max_seq_length):
        """
        Inicializa el reconocedor de voz con configuraciones básicas
        
        Parámetros:
            phonemes: Lista de fonemas del idioma (lista de strings)
            words: Diccionario de palabras a fonemas (dict {str: [str]})
            max_seq_length: Máxima longitud de secuencia (int)
        """
        
        # Almacenamiento de los fonemas del modelo
        self.phonemes = phonemes
        
        # Almacenamiento del vocabulario de palabras
        self.words = words
        
        # Longitud máxima de secuencia permitida
        self.max_seq_length = max_seq_length
        
        # Creación de mapeo fonema -> índice numérico
        self.phoneme_to_idx = {p:i for i,p in enumerate(phonemes)}
        
        # Creación de mapeo índice numérico -> fonema
        self.idx_to_phoneme = {i:p for i,p in enumerate(phonemes)}
        
        # Copia del diccionario palabras a fonemas
        self.word_to_phonemes = words
        
        # Configuración de hiperparámetros de la red neuronal
        
        # Dimensión del espacio de embedding
        self.embedding_dim = 64
        
        # Número de unidades en capa LSTM
        self.lstm_units = 128
        
        # Dimensión de capa oculta
        self.hidden_dim = 64
        
        # Construcción del modelo neuronal
        self.model = self.build_probabilistic_model()

    # Método para construir la red neuronal
    def build_probabilistic_model(self):
        """Construye y compila el modelo neuronal probabilístico"""
        
        # Definición de la capa de entrada para características acústicas
        # Shape: (None, max_seq_length, 13) donde 13 son típicos coeficientes MFCC
        input_features = Input(shape=(self.max_seq_length, 13), name='input_features')
        
        # Primera capa densa para transformación inicial de características
        # Activa con ReLU para no linealidad
        x = Dense(self.embedding_dim, activation='relu')(input_features)
        
        # Capa LSTM para procesamiento de secuencias temporales
        # return_sequences=True para mantener la dimensión temporal
        x = LSTM(self.lstm_units, return_sequences=True)(x)
        
        # Capa densa oculta adicional
        x = Dense(self.hidden_dim, activation='relu')(x)
        
        # Capa de salida con softmax para distribución de probabilidad
        # Salida shape: (None, max_seq_length, len(phonemes))
        phoneme_probs = Dense(len(self.phonemes), activation='softmax', name='phoneme_probs')(x)
        
        # Función para envolver las probabilidades en una distribución categórica
        def phoneme_distribution(params):
            """Crea distribución categórica a partir de probabilidades"""
            return tfd.Categorical(probs=params, name='phoneme_distribution')
        
        # Capa Lambda para aplicar la conversión a distribución probabilística
        phoneme_output = Lambda(lambda x: phoneme_distribution(x), name='phoneme_output')(phoneme_probs)
        
        # Construcción del modelo completo especificando entradas y salidas
        model = Model(inputs=input_features, outputs=phoneme_output)
        
        # Definición de función de pérdida personalizada
        def neg_log_likelihood(y_true, y_pred):
            """Negative log likelihood loss para distribución categórica"""
            return -y_pred.log_prob(y_true)
        
        # Compilación del modelo con optimizador Adam y métrica de accuracy
        model.compile(optimizer='adam', loss=neg_log_likelihood, metrics=['accuracy'])
        
        # Retorno del modelo compilado
        return model

    # Método para preprocesamiento de datos
    def preprocess_data(self, audio_features, phoneme_sequences):
        """
        Prepara los datos para entrenamiento
        
        Parámetros:
            audio_features: Lista de arrays con características acústicas
            phoneme_sequences: Lista de secuencias de fonemas correspondientes
            
        Retorna:
            Tupla (X, y) con datos preprocesados
        """
        
        # Aplicación de padding a las características acústicas
        # maxlen: trunca o paddea a la longitud máxima
        # padding='post': añade ceros al final
        # dtype: tipo float32 para compatibilidad con GPU
        X = tf.keras.preprocessing.sequence.pad_sequences(
            audio_features, 
            maxlen=self.max_seq_length, 
            padding='post', 
            dtype='float32')
        
        # Conversión de fonemas a índices numéricos
        y = [[self.phoneme_to_idx[p] for p in seq] for seq in phoneme_sequences]
        
        # Aplicación de padding a las secuencias de fonemas
        # Usamos -1 como valor de padding para ignorar en la pérdida
        y = tf.keras.preprocessing.sequence.pad_sequences(
            y, 
            maxlen=self.max_seq_length, 
            padding='post', 
            value=-1)
        
        # Retorno de los datos preprocesados
        return X, y

    # Método para entrenar el modelo
    def train(self, X_train, y_train, X_val=None, y_val=None, epochs=50, batch_size=32):
        """
        Entrena el modelo con los datos proporcionados
        
        Parámetros:
            X_train: Características de entrenamiento
            y_train: Etiquetas de entrenamiento
            X_val: Características de validación (opcional)
            y_val: Etiquetas de validación (opcional)
            epochs: Número máximo de épocas
            batch_size: Tamaño del batch
            
        Retorna:
            Objeto History con el historial de entrenamiento
        """
        
        # Configuración de early stopping para evitar sobreajuste
        # Monitoriza la pérdida de validación
        # Paciencia de 5 épocas sin mejora
        # Restaura los mejores pesos al final
        early_stopping = EarlyStopping(
            monitor='val_loss', 
            patience=5, 
            restore_best_weights=True)
        
        # Usar callback solo si hay datos de validación
        callbacks = [early_stopping] if X_val is not None else []
        
        # Entrenamiento del modelo con los datos proporcionados
        history = self.model.fit(
            X_train, y_train,  # Datos de entrenamiento
            validation_data=(X_val, y_val) if X_val is not None else None,  # Datos de validación
            epochs=epochs,  # Número de épocas
            batch_size=batch_size,  # Tamaño del batch
            callbacks=callbacks  # Callbacks configurados
        )
        
        # Retorno del historial de entrenamiento
        return history

    # Método para predecir fonemas
    def predict_phonemes(self, audio_features):
        """
        Predice la secuencia de fonemas para características de audio dadas
        
        Parámetros:
            audio_features: Array con características acústicas
            
        Retorna:
            Tupla (secuencia_fonemas, probabilidades)
        """
        
        # Preprocesamiento de las características de audio
        X = tf.keras.preprocessing.sequence.pad_sequences(
            [audio_features],  # Lista de un solo elemento
            maxlen=self.max_seq_length, 
            padding='post', 
            dtype='float32')
        
        # Obtención de probabilidades del modelo
        probs = self.model.predict(X)[0]  # Tomamos el primer (y único) elemento
        
        # Conversión de probabilidades a índices de fonemas
        phoneme_indices = np.argmax(probs, axis=-1)
        
        # Filtrado de valores de padding (-1) y conversión a fonemas
        phoneme_sequence = [self.idx_to_phoneme[idx] for idx in phoneme_indices if idx != -1]
        
        # Retorno de la secuencia y probabilidades
        return phoneme_sequence, probs

    # Método para predecir palabras completas
    def predict_words(self, audio_features):
        """
        Reconoce palabras completas a partir de características de audio
        
        Parámetros:
            audio_features: Array con características acústicas
            
        Retorna:
            Tupla (lista_palabras, secuencia_fonemas)
        """
        
        # Primero obtenemos la secuencia de fonemas
        phoneme_sequence, _ = self.predict_phonemes(audio_features)
        
        # Inicialización de variables para el algoritmo de matching
        recognized_words = []  # Lista para almacenar palabras reconocidas
        current_pos = 0  # Posición actual en la secuencia
        
        # Iteramos hasta recorrer toda la secuencia
        while current_pos < len(phoneme_sequence):
            best_match = None  # Mejor coincidencia encontrada
            best_match_length = 0  # Longitud de la mejor coincidencia
            
            # Buscamos en todas las palabras conocidas
            for word, word_phonemes in self.word_to_phonemes.items():
                word_length = len(word_phonemes)
                
                # Verificamos si hay suficiente secuencia restante
                if current_pos + word_length > len(phoneme_sequence):
                    continue
                
                # Bandera para verificar coincidencia
                match = True
                
                # Comparamos cada fonema
                for i in range(word_length):
                    if phoneme_sequence[current_pos + i] != word_phonemes[i]:
                        match = False
                        break
                
                # Actualizamos la mejor coincidencia si corresponde
                if match and word_length > best_match_length:
                    best_match = word
                    best_match_length = word_length
            
            # Si encontramos coincidencia, la agregamos a los resultados
            if best_match:
                recognized_words.append(best_match)
                current_pos += best_match_length
            else:
                # Si no hay coincidencia, avanzamos una posición
                current_pos += 1
        
        # Retornamos las palabras reconocidas y la secuencia fonética
        return recognized_words, phoneme_sequence

    # Método para estimar incertidumbre
    def uncertainty_estimation(self, audio_features, num_samples=10):
        """
        Estima la incertidumbre en las predicciones usando muestreo
        
        Parámetros:
            audio_features: Array con características acústicas
            num_samples: Número de muestras para estimación
            
        Retorna:
            Diccionario con métricas de incertidumbre
        """
        
        # Preprocesamiento de las características
        X = tf.keras.preprocessing.sequence.pad_sequences(
            [audio_features], 
            maxlen=self.max_seq_length, 
            padding='post', 
            dtype='float32')
        
        # Creación de submodelo que devuelve probabilidades directas
        prob_model = Model(
            inputs=self.model.inputs, 
            outputs=self.model.get_layer('phoneme_probs').output)
        
        # Generación de múltiples muestras de probabilidad
        sampled_probs = []
        for _ in range(num_samples):
            sampled_probs.append(prob_model.predict(X)[0])
        
        # Conversión a array numpy
        sampled_probs = np.array(sampled_probs)
        
        # Cálculo de estadísticas de incertidumbre
        
        # Probabilidades promedio
        mean_probs = np.mean(sampled_probs, axis=0)
        
        # Desviación estándar de probabilidades
        std_probs = np.std(sampled_probs, axis=0)
        
        # Cálculo de entropía (medida de incertidumbre)
        entropy = -np.sum(mean_probs * np.log(mean_probs + 1e-10), axis=-1)
        
        # Retorno de métricas en diccionario
        return {
            'mean_probs': mean_probs,
            'std_probs': std_probs,
            'entropy': entropy
        }

# Bloque principal de ejecución (ejemplo de uso)
if __name__ == "__main__":
    # Configuración de ejemplo para demostración
    
    # Lista de fonemas del modelo
    phonemes = ['p', 'a', 't', 'e', 'l', 'o', 'm', 'n', 's', 'i']
    
    # Vocabulario con su representación fonética
    words = {
        'pat': ['p', 'a', 't'],
        'pato': ['p', 'a', 't', 'o'],
        'tel': ['t', 'e', 'l'],
        'mesa': ['m', 'e', 's', 'a'],
        'limon': ['l', 'i', 'm', 'o', 'n']
    }
    
    # Longitud máxima de secuencia
    max_seq_length = 20
    
    # Instanciación del reconocedor
    recognizer = DeepSpeechRecognition(phonemes, words, max_seq_length)
    
    # Mostrar resumen de la arquitectura del modelo
    recognizer.model.summary()
    
    # Función auxiliar para generar datos de ejemplo
    def generate_example_data(num_samples=100):
        """Genera datos de ejemplo simulados"""
        import random  # Importación local para generación aleatoria
        
        X = []  # Lista para características
        y = []  # Lista para etiquetas
        
        for _ in range(num_samples):
            # Selección aleatoria de una palabra
            word = random.choice(list(words.keys()))
            phoneme_seq = words[word]
            
            # Generación de características acústicas aleatorias (simulación)
            audio_features = np.random.randn(len(phoneme_seq), 13)
            
            # Almacenamiento de los datos generados
            X.append(audio_features)
            y.append(phoneme_seq)
        
        return X, y
    
    # Generación de datos de entrenamiento y validación
    X_train, y_train = generate_example_data(200)  # 200 muestras de entrenamiento
    X_val, y_val = generate_example_data(50)  # 50 muestras de validación
    
    # Preprocesamiento de los datos generados
    X_train_prep, y_train_prep = recognizer.preprocess_data(X_train, y_train)
    X_val_prep, y_val_prep = recognizer.preprocess_data(X_val, y_val)
    
    # Entrenamiento del modelo
    history = recognizer.train(
        X_train_prep, y_train_prep,  # Datos de entrenamiento
        X_val_prep, y_val_prep,  # Datos de validación
        epochs=30  # Número de épocas
    )
    
    # Visualización del progreso del entrenamiento
    
    # Creación de figura con 2 subplots
    plt.figure(figsize=(12, 4))
    
    # Subplot para la pérdida
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Train Loss')  # Pérdida entrenamiento
    plt.plot(history.history['val_loss'], label='Validation Loss')  # Pérdida validación
    plt.xlabel('Epoch')  # Etiqueta eje x
    plt.ylabel('Loss')  # Etiqueta eje y
    plt.legend()  # Mostrar leyenda
    
    # Subplot para la precisión
    plt.subplot(1, 2, 2)
    plt.plot(history.history['accuracy'], label='Train Accuracy')  # Precisión entrenamiento
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')  # Precisión validación
    plt.xlabel('Epoch')  # Etiqueta eje x
    plt.ylabel('Accuracy')  # Etiqueta eje y
    plt.legend()  # Mostrar leyenda
    
    # Mostrar los gráficos
    plt.show()
    
    # Prueba de reconocimiento con palabra de ejemplo
    
    # Palabra de prueba
    test_word = 'pato'
    
    # Secuencia fonética de la palabra de prueba
    test_phonemes = words[test_word]
    
    # Generación de características acústicas simuladas
    test_audio = np.random.randn(len(test_phonemes), 13)
    
    # Predicción usando el modelo entrenado
    predicted_words, predicted_phonemes = recognizer.predict_words(test_audio)
    
    # Impresión de resultados
    print(f"\nPalabra original: {test_word} ({' '.join(test_phonemes)})")
    print(f"Palabra reconocida: {predicted_words} ({' '.join(predicted_phonemes)})")
    
    # Cálculo de métricas de incertidumbre
    uncertainty = recognizer.uncertainty_estimation(test_audio)
    
    # Impresión de métricas de incertidumbre
    print("\nIncertidumbre en las predicciones:")
    for i, phoneme in enumerate(predicted_phonemes):
        print(f"{phoneme}: Entropía={uncertainty['entropy'][i]:.3f}, Std={np.mean(uncertainty['std_probs'][i]):.3f}")