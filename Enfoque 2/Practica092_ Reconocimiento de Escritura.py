# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 14:19:35 2025

@author: elvin
"""

import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
import numpy as np
import matplotlib.pyplot as plt

# Cargar el dataset MNIST
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Normalizar los datos (de 0-255 a 0-1)
x_train = x_train / 255.0
x_test = x_test / 255.0

# Crear el modelo
modelo = Sequential([
    Flatten(input_shape=(28, 28)),
    Dense(128, activation='relu'),
    Dense(10, activation='softmax')  # 10 salidas para los dígitos 0-9
])

# Compilar el modelo
modelo.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])

# Entrenar el modelo
modelo.fit(x_train, y_train, epochs=5)

# Evaluar el modelo
test_loss, test_acc = modelo.evaluate(x_test, y_test)
print(f'\nPrecisión en las pruebas: {test_acc:.4f}')

# Probar el modelo con una imagen de prueba
indice = np.random.randint(0, len(x_test))
imagen = x_test[indice]
imagen_exp = np.expand_dims(imagen, axis=0)

# Mostrar la imagen
plt.imshow(imagen, cmap='gray')
plt.title('Imagen de prueba')
plt.show()

# Predecir
prediccion = modelo.predict(imagen_exp)
print(f'Número predicho: {np.argmax(prediccion)}')
