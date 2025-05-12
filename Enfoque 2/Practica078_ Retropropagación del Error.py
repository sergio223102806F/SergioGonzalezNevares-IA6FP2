# -*- coding: utf-8 -*-                                                     # Define la codificación de caracteres del archivo como UTF-8
"""
Created on Sat Apr 26 18:14:49 2025                                         # Indica la fecha y hora de creación del archivo
                                                                           #
@author: elvin                                                              # Define el autor del archivo
"""

import numpy as np                                                          # Importa la biblioteca NumPy y la asigna el alias 'np'
import matplotlib.pyplot as plt                                             # Importa la biblioteca Matplotlib y la asigna el alias 'plt'

class NeuralNetwork:                                                      # Define una nueva clase llamada NeuralNetwork
    def __init__(self, layers=[2, 4, 1], learning_rate=0.1):              # Define el constructor de la clase NeuralNetwork con valores predeterminados
        """
        Inicializa la red neuronal con:                                    # Documentación del constructor
        - layers: Lista con número de neuronas en cada capa (ej. [entrada, oculta, salida]) # Descripción del argumento 'layers'
        - learning_rate: Tasa de aprendizaje para el descenso de gradiente # Descripción del argumento 'learning_rate'
        """
        self.layers = layers                                                # Asigna la lista de capas al atributo self.layers
        self.lr = learning_rate                                             # Asigna la tasa de aprendizaje al atributo self.lr

        # Inicialización de pesos y sesgos                                # Comentario indicando la inicialización de pesos y sesgos
        self.weights = []                                                 # Inicializa una lista vacía para almacenar los pesos
        self.biases = []                                                  # Inicializa una lista vacía para almacenar los sesgos
        for i in range(len(layers)-1):                                     # Itera sobre las capas para inicializar pesos y sesgos
            # Inicialización Xavier/Glorot para mejores resultados         # Comentario indicando el tipo de inicialización
            w = np.random.randn(layers[i], layers[i+1]) * np.sqrt(2./layers[i]) # Inicializa los pesos con distribución normal y escalado
            b = np.zeros((1, layers[i+1]))                                 # Inicializa los sesgos con ceros
            self.weights.append(w)                                         # Agrega la matriz de pesos a la lista de pesos
            self.biases.append(b)                                           # Agrega el vector de sesgos a la lista de sesgos

    def sigmoid(self, x):                                                  # Define la función sigmoide
        """Función de activación sigmoide (rango 0-1)"""                   # Documentación de la función sigmoide
        return 1 / (1 + np.exp(-x))                                        # Calcula y devuelve el valor de la función sigmoide

    def sigmoid_derivative(self, x):                                       # Define la derivada de la función sigmoide
        """Derivada de la sigmoide (para backpropagation)"""              # Documentación de la derivada de la sigmoide
        return x * (1 - x)                                                 # Calcula y devuelve la derivada de la función sigmoide

    def forward(self, X):                                                  # Define el método para la propagación hacia adelante
        """Propagación hacia adelante"""                                   # Documentación del método forward
        self.activations = [X]  # Almacena activaciones de todas las capas # Inicializa la lista de activaciones con la entrada
        self.z_values = []    # Almacena valores antes de la activación    # Inicializa la lista de valores z

        for i in range(len(self.weights)):                                 # Itera sobre las capas de la red
            # Calcula la combinación lineal de entradas y pesos           # Comentario indicando el cálculo lineal
            z = np.dot(self.activations[-1], self.weights[i]) + self.biases[i] # Calcula la suma ponderada de las entradas más el sesgo
            # Aplica función de activación                               # Comentario indicando la aplicación de la activación
            a = self.sigmoid(z)                                           # Aplica la función sigmoide al valor z
            self.z_values.append(z)                                        # Agrega el valor z a la lista de valores z
            self.activations.append(a)                                     # Agrega la activación a la lista de activaciones

        return self.activations[-1]  # Devuelve la salida final             # Devuelve la activación de la última capa

    def backward(self, X, y, output):                                      # Define el método para la propagación hacia atrás
        """Propagación hacia atrás (backpropagation)"""                     # Documentación del método backward
        m = X.shape[0]  # Número de muestras                             # Obtiene el número de muestras

        # 1. Calcular error en la capa de salida                         # Comentario indicando el cálculo del error de salida
        error = output - y                                               # Calcula el error entre la salida de la red y la salida esperada

        # Listas para almacenar gradientes                               # Comentario indicando la inicialización de listas de gradientes
        dW = []  # Gradientes de pesos                                    # Inicializa una lista vacía para los gradientes de los pesos
        db = []  # Gradientes de sesgos                                   # Inicializa una lista vacía para los gradientes de los sesgos

        # Backpropagation (de atrás hacia adelante)                      # Comentario indicando la dirección de la backpropagation
        for i in reversed(range(len(self.weights))):                     # Itera sobre las capas en orden inverso
            if i == len(self.weights)-1:  # Capa de salida               # Si es la última capa (capa de salida)
                delta = error * self.sigmoid_derivative(output)          # Calcula el delta para la capa de salida
            else:  # Capas ocultas                                       # Si es una capa oculta
                delta = np.dot(delta, self.weights[i+1].T) * self.sigmoid_derivative(self.activations[i+1]) # Calcula el delta para la capa oculta

            # Calcular gradientes                                        # Comentario indicando el cálculo de los gradientes
            dw = np.dot(self.activations[i].T, delta) / m                # Calcula el gradiente de los pesos para la capa actual
            dbias = np.sum(delta, axis=0, keepdims=True) / m             # Calcula el gradiente de los sesgos para la capa actual

            # Guardar gradientes (orden inverso)                          # Comentario indicando el almacenamiento de los gradientes
            dW.insert(0, dw)                                             # Inserta el gradiente de los pesos al principio de la lista
            db.insert(0, dbias)                                           # Inserta el gradiente de los sesgos al principio de la lista

        # Actualizar pesos y sesgos (descenso de gradiente)             # Comentario indicando la actualización de pesos y sesgos
        for i in range(len(self.weights)):                               # Itera sobre las capas
            self.weights[i] -= self.lr * dW[i]                           # Actualiza los pesos usando el descenso de gradiente
            self.biases[i] -= self.lr * db[i]                            # Actualiza los sesgos usando el descenso de gradiente

    def train(self, X, y, epochs=1000, verbose=True):                   # Define el método para entrenar la red neuronal
        """Entrena la red neuronal"""                                   # Documentación del método train
        for epoch in range(epochs):                                       # Itera sobre el número de épocas
            # Forward pass                                             # Comentario indicando la propagación hacia adelante
            output = self.forward(X)                                     # Realiza una pasada hacia adelante a través de la red

            # Backward pass                                            # Comentario indicando la propagación hacia atrás
            self.backward(X, y, output)                                  # Realiza una pasada hacia atrás para calcular y aplicar los gradientes

            # Mostrar progreso                                         # Comentario indicando la visualización del progreso
            if verbose and epoch % 100 == 0:                             # Si verbose es True y la época es un múltiplo de 100
                loss = np.mean(np.square(output - y))                    # Calcula la pérdida (error cuadrático medio)
                print(f"Época {epoch}, Pérdida: {loss:.4f}")           # Imprime la época actual y la pérdida

    def predict(self, X, threshold=0.5):                                # Define el método para realizar predicciones
        """Realiza predicciones"""                                      # Documentación del método predict
        output = self.forward(X)                                     # Realiza una pasada hacia adelante para obtener la salida
        return (output > threshold).astype(int)                         # Aplica un umbral a la salida para obtener la predicción binaria


# Ejemplo de uso con compuerta XOR                                    # Comentario indicando el ejemplo de uso
if __name__ == "__main__":                                               # Asegura que el código dentro solo se ejecute si el script es el principal
    # Datos de entrenamiento (XOR)                                     # Comentario indicando los datos de entrenamiento
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])                      # Define los datos de entrada para la compuerta XOR
    y = np.array([[0], [1], [1], [0]])                                 # Define las salidas esperadas para la compuerta XOR

    # Crear y entrenar red neuronal                                   # Comentario indicando la creación y entrenamiento de la red
    nn = NeuralNetwork(layers=[2, 4, 1], learning_rate=0.1)           # Crea una instancia de la clase NeuralNetwork
    print("Entrenando la red neuronal...")                            # Imprime un mensaje indicando el inicio del entrenamiento
    nn.train(X, y, epochs=5000)                                        # Entrena la red neuronal con los datos XOR durante 5000 épocas

    # Predicciones finales                                           # Comentario indicando las predicciones finales
    print("\nPredicciones finales:")                                  # Imprime un encabezado para las predicciones
    for i in range(len(X)):                                           # Itera sobre los datos de entrada
        prediction = nn.predict(X[i:i+1])[0][0]                      # Realiza una predicción para la entrada actual
        print(f"Entrada: {X[i]}, Predicción: {prediction}")         # Imprime la entrada y la predicción correspondiente

    # Visualización de la frontera de decisión                      # Comentario indicando la visualización de la frontera
    plt.figure(figsize=(8, 6))                                        # Crea una nueva figura para el gráfico
    x_min, x_max = -0.5, 1.5                                         # Define los límites del eje x
    y_min, y_max = -0.5, 1.5                                         # Define los límites del eje y
    h = 0.01                                                         # Define la granularidad de la malla
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),                 # Crea una malla de puntos en el espacio de entrada
                         np.arange(y_min, y_max, h))

    Z = nn.predict(np.c_[xx.ravel(), yy.ravel()])                     # Realiza predicciones para todos los puntos de la malla
    Z = Z.reshape(xx.shape)                                           # Redimensiona las predicciones para que coincidan con la forma de la malla

    plt.contourf(xx, yy, Z, alpha=0.8)                               # Dibuja las regiones de decisión
    plt.scatter(X[:, 0], X[:, 1], c=y.ravel(), edgecolors='k')       # Dibuja los puntos de datos con colores según la etiqueta
    plt.title("Frontera de Decisión para XOR")                        # Establece el título del gráfico
    plt.show()                                                         # Muestra el gráfico