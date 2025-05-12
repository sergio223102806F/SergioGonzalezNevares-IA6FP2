# -*- coding: utf-8 -*-                                                     # Define la codificación de caracteres del archivo como UTF-8
"""
Created on Sat Apr 26 17:35:06 2025                                         # Indica la fecha y hora de creación del archivo
                                                                           #
@author: elvin                                                              # Define el autor del archivo
"""

import numpy as np                                                          # Importa la biblioteca NumPy y la asigna el alias 'np' para operaciones numéricas

class NeuralNetwork:                                                        # Define una nueva clase llamada NeuralNetwork
    def __init__(self, layers=[2, 4, 1], learning_rate=0.1):                 # Define el constructor de la clase NeuralNetwork con valores predeterminados para los parámetros
        """
        Inicializa una red neuronal completamente conectada                  # Documentación de la inicialización de la red neuronal

        Parámetros:                                                         # Documentación de los parámetros del constructor
        layers : lista con el número de neuronas en cada capa               # Descripción del parámetro layers
                (ej. [2, 4, 1] = 2 entradas, 1 capa oculta con 4 neuronas, 1 salida) # Ejemplo de la estructura de la lista layers
        learning_rate : tasa de aprendizaje para el descenso de gradiente   # Descripción del parámetro learning_rate
        """
        self.layers = layers                                                # Asigna la lista de capas al atributo self.layers
        self.lr = learning_rate                                             # Asigna la tasa de aprendizaje al atributo self.lr
        self.weights = []                                                   # Inicializa una lista vacía para almacenar las matrices de pesos
        self.biases = []                                                    # Inicializa una lista vacía para almacenar los vectores de sesgos

        # Inicialización de pesos y sesgos                                    # Comentario indicando la inicialización de pesos y sesgos
        for i in range(len(layers)-1):                                      # Itera sobre las capas de la red neuronal (excepto la última)
            # Pesos con inicialización Xavier/Glorot (ajustados por tamaño de capa) # Comentario sobre la inicialización de pesos
            w = np.random.randn(layers[i], layers[i+1]) * np.sqrt(2./layers[i]) # Inicializa la matriz de pesos con números aleatorios usando la inicialización Xavier/Glorot
            b = np.zeros((1, layers[i+1]))                                  # Inicializa el vector de sesgos con ceros
            self.weights.append(w)                                          # Agrega la matriz de pesos a la lista self.weights
            self.biases.append(b)                                           # Agrega el vector de sesgos a la lista self.biases

    def sigmoid(self, x):                                                   # Define la función de activación sigmoide
        """Función de activación sigmoide"""                                 # Documentación de la función sigmoide
        return 1 / (1 + np.exp(-x))                                        # Calcula y devuelve el valor de la función sigmoide

    def sigmoid_derivative(self, x):                                        # Define la derivada de la función sigmoide
        """Derivada de la sigmoide (para backpropagation)"""                # Documentación de la derivada de la sigmoide
        return x * (1 - x)                                                  # Calcula y devuelve la derivada de la función sigmoide

    def forward(self, X):                                                   # Define el método para la propagación hacia adelante
        """Propagación hacia adelante (forward pass)"""                     # Documentación del forward pass
        self.activations = [X]                                              # Almacena las activaciones de todas las capas, comenzando con la entrada X
        self.z_values = []                                                  # Almacena los valores z (antes de la función de activación)

        for i in range(len(self.weights)):                                  # Itera sobre las capas de la red neuronal
            z = np.dot(self.activations[-1], self.weights[i]) + self.biases[i] # Calcula la suma ponderada de las entradas más el sesgo
            a = self.sigmoid(z)                                             # Aplica la función de activación sigmoide al valor z
            self.z_values.append(z)                                         # Almacena el valor z en la lista self.z_values
            self.activations.append(a)                                      # Almacena la activación en la lista self.activations

        return self.activations[-1]                                         # Devuelve la activación de la última capa (la salida de la red)

    def backward(self, X, y, output):                                       # Define el método para la propagación hacia atrás
        """Propagación hacia atrás (backpropagation)"""                    # Documentación del backpropagation
        m = X.shape[0]                                                     # Obtiene el número de ejemplos de entrenamiento

        # Calcula error en la capa de salida                                 # Comentario indicando el cálculo del error en la capa de salida
        error = output - y                                                 # Calcula la diferencia entre la salida predicha y la salida real
        dW = []                                                            # Inicializa una lista vacía para almacenar los gradientes de los pesos
        db = []                                                            # Inicializa una lista vacía para almacenar los gradientes de los sesgos

        # Backpropagation                                                  # Comentario indicando el proceso de backpropagation
        for i in reversed(range(len(self.weights))):                       # Itera sobre las capas de la red neuronal en orden inverso
            # Gradiente de la función de pérdida respecto a z                # Comentario indicando el cálculo del gradiente respecto a z
            if i == len(self.weights)-1:                                   # Para la capa de salida
                delta = error * self.sigmoid_derivative(output)            # Calcula el delta (error multiplicado por la derivada de la activación)
            else:                                                          # Para las capas ocultas
                delta = np.dot(delta, self.weights[i+1].T) * self.sigmoid_derivative(self.activations[i+1]) # Calcula el delta propagando el error hacia atrás

            # Calcula gradientes para pesos y sesgos                         # Comentario indicando el cálculo de los gradientes
            dw = np.dot(self.activations[i].T, delta) / m                  # Calcula el gradiente de los pesos
            dbias = np.sum(delta, axis=0, keepdims=True) / m               # Calcula el gradiente de los sesgos

            dW.insert(0, dw)                                                # Inserta el gradiente de los pesos al inicio de la lista dW
            db.insert(0, dbias)                                             # Inserta el gradiente de los sesgos al inicio de la lista db

        # Actualiza pesos y sesgos                                           # Comentario indicando la actualización de pesos y sesgos
        for i in range(len(self.weights)):                                  # Itera sobre las capas de la red neuronal
            self.weights[i] -= self.lr * dW[i]                              # Actualiza los pesos restando el gradiente multiplicado por la tasa de aprendizaje
            self.biases[i] -= self.lr * db[i]                               # Actualiza los sesgos restando el gradiente multiplicado por la tasa de aprendizaje

    def train(self, X, y, epochs=1000):                                     # Define el método para entrenar la red neuronal
        """Entrena la red neuronal"""                                      # Documentación del entrenamiento de la red
        for epoch in range(epochs):                                         # Itera sobre el número de épocas
            # Forward pass                                                   # Comentario indicando el forward pass
            output = self.forward(X)                                      # Realiza una pasada hacia adelante para obtener la salida

            # Backward pass                                                  # Comentario indicando el backward pass
            self.backward(X, y, output)                                   # Realiza una pasada hacia atrás para actualizar los pesos y sesgos

            # Mostrar progreso (opcional)                                    # Comentario indicando la visualización del progreso
            if epoch % 100 == 0:                                           # Imprime la pérdida cada 100 épocas
                loss = np.mean(np.square(output - y))                      # Calcula la pérdida (error cuadrático medio)
                print(f"Época {epoch}, Pérdida: {loss:.4f}")                # Imprime el número de época y la pérdida actual

    def predict(self, X):                                                  # Define el método para realizar predicciones
        """Realiza predicciones"""                                        # Documentación de la predicción
        return self.forward(X)                                             # Realiza una pasada hacia adelante y devuelve la salida como la predicción