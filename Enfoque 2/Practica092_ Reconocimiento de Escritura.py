# -*- coding: utf-8 -*-                                                     # Define la codificación de caracteres del archivo como UTF-8
"""
Created on Sun Apr 27 14:19:35 2025                                         # Indica la fecha y hora de creación del archivo
                                                                           #
@author: elvin                                                              # Define el autor del archivo
"""

import tensorflow as tf                                                    # Importa la biblioteca TensorFlow para aprendizaje automático
from tensorflow.keras.datasets import mnist                                 # Importa el dataset MNIST desde Keras
from tensorflow.keras.models import Sequential                               # Importa la clase Sequential para crear modelos
from tensorflow.keras.layers import Dense, Flatten                           # Importa las capas Dense (totalmente conectada) y Flatten (aplanar la entrada)
import numpy as np                                                          # Importa la biblioteca NumPy para operaciones numéricas
import matplotlib.pyplot as plt                                           # Importa la biblioteca Matplotlib para visualización

# Cargar el dataset MNIST                                                  # Comentario indicando la carga del dataset MNIST
(x_train, y_train), (x_test, y_test) = mnist.load_data()                   # Carga los datos de entrenamiento y prueba del dataset MNIST

# Normalizar los datos (de 0-255 a 0-1)                                     # Comentario indicando la normalización de los datos
x_train = x_train / 255.0                                                 # Normaliza los datos de entrenamiento dividiéndolos por 255.0
x_test = x_test / 255.0                                                   # Normaliza los datos de prueba dividiéndolos por 255.0

# Crear el modelo                                                         # Comentario indicando la creación del modelo
modelo = Sequential([                                                     # Crea un modelo secuencial
    Flatten(input_shape=(28, 28)),                                        # Aplana la entrada de imágenes de 28x28 píxeles a un vector de 784
    Dense(128, activation='relu'),                                       # Añade una capa densa con 128 neuronas y función de activación ReLU
    Dense(10, activation='softmax')  # 10 salidas para los dígitos 0-9      # Añade una capa densa de salida con 10 neuronas (una por cada dígito) y función de activación softmax
])

# Compilar el modelo                                                      # Comentario indicando la compilación del modelo
modelo.compile(optimizer='adam',                                          # Compila el modelo con el optimizador Adam
               loss='sparse_categorical_crossentropy',                    # Define la función de pérdida como entropía cruzada categórica dispersa
               metrics=['accuracy'])                                      # Define la métrica de evaluación como precisión

# Entrenar el modelo                                                      # Comentario indicando el entrenamiento del modelo
modelo.fit(x_train, y_train, epochs=5)                                    # Entrena el modelo usando los datos de entrenamiento durante 5 épocas

# Evaluar el modelo                                                       # Comentario indicando la evaluación del modelo
test_loss, test_acc = modelo.evaluate(x_test, y_test)                     # Evalúa el modelo usando los datos de prueba
print(f'\nPrecisión en las pruebas: {test_acc:.4f}')                     # Imprime la precisión del modelo en los datos de prueba

# Probar el modelo con una imagen de prueba                             # Comentario indicando la prueba del modelo con una imagen
indice = np.random.randint(0, len(x_test))                               # Genera un índice aleatorio para seleccionar una imagen de prueba
imagen = x_test[indice]                                                  # Selecciona una imagen de prueba aleatoria
imagen_exp = np.expand_dims(imagen, axis=0)                              # Expande las dimensiones de la imagen para que coincida con la entrada esperada del modelo

# Mostrar la imagen                                                      # Comentario indicando la visualización de la imagen
plt.imshow(imagen, cmap='gray')                                          # Muestra la imagen de prueba en escala de grises
plt.title('Imagen de prueba')                                            # Establece el título de la imagen mostrada
plt.show()                                                               # Muestra la gráfica de la imagen

# Predecir                                                               # Comentario indicando la predicción
prediccion = modelo.predict(imagen_exp)                                  # Realiza una predicción usando el modelo para la imagen de prueba
print(f'Número predicho: {np.argmax(prediccion)}')                     # Imprime el número predicho (el índice con la probabilidad más alta)
