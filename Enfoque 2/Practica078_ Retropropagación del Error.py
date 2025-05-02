# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 18:14:49 2025

@author: elvin
"""

import numpy as np
import matplotlib.pyplot as plt

class NeuralNetwork:
    def __init__(self, layers=[2, 4, 1], learning_rate=0.1):
        """
        Inicializa la red neuronal con:
        - layers: Lista con número de neuronas en cada capa (ej. [entrada, oculta, salida])
        - learning_rate: Tasa de aprendizaje para el descenso de gradiente
        """
        self.layers = layers
        self.lr = learning_rate
        
        # Inicialización de pesos y sesgos
        self.weights = []
        self.biases = []
        for i in range(len(layers)-1):
            # Inicialización Xavier/Glorot para mejores resultados
            w = np.random.randn(layers[i], layers[i+1]) * np.sqrt(2./layers[i])
            b = np.zeros((1, layers[i+1]))
            self.weights.append(w)
            self.biases.append(b)
    
    def sigmoid(self, x):
        """Función de activación sigmoide (rango 0-1)"""
        return 1 / (1 + np.exp(-x))
    
    def sigmoid_derivative(self, x):
        """Derivada de la sigmoide (para backpropagation)"""
        return x * (1 - x)
    
    def forward(self, X):
        """Propagación hacia adelante"""
        self.activations = [X]  # Almacena activaciones de todas las capas
        self.z_values = []      # Almacena valores antes de la activación
        
        for i in range(len(self.weights)):
            # Calcula la combinación lineal de entradas y pesos
            z = np.dot(self.activations[-1], self.weights[i]) + self.biases[i]
            # Aplica función de activación
            a = self.sigmoid(z)
            self.z_values.append(z)
            self.activations.append(a)
        
        return self.activations[-1]  # Devuelve la salida final
    
    def backward(self, X, y, output):
        """Propagación hacia atrás (backpropagation)"""
        m = X.shape[0]  # Número de muestras
        
        # 1. Calcular error en la capa de salida
        error = output - y
        
        # Listas para almacenar gradientes
        dW = []  # Gradientes de pesos
        db = []  # Gradientes de sesgos
        
        # Backpropagation (de atrás hacia adelante)
        for i in reversed(range(len(self.weights))):
            if i == len(self.weights)-1:  # Capa de salida
                delta = error * self.sigmoid_derivative(output)
            else:  # Capas ocultas
                delta = np.dot(delta, self.weights[i+1].T) * self.sigmoid_derivative(self.activations[i+1])
            
            # Calcular gradientes
            dw = np.dot(self.activations[i].T, delta) / m
            dbias = np.sum(delta, axis=0, keepdims=True) / m
            
            # Guardar gradientes (orden inverso)
            dW.insert(0, dw)
            db.insert(0, dbias)
        
        # Actualizar pesos y sesgos (descenso de gradiente)
        for i in range(len(self.weights)):
            self.weights[i] -= self.lr * dW[i]
            self.biases[i] -= self.lr * db[i]
    
    def train(self, X, y, epochs=1000, verbose=True):
        """Entrena la red neuronal"""
        for epoch in range(epochs):
            # Forward pass
            output = self.forward(X)
            
            # Backward pass
            self.backward(X, y, output)
            
            # Mostrar progreso
            if verbose and epoch % 100 == 0:
                loss = np.mean(np.square(output - y))
                print(f"Época {epoch}, Pérdida: {loss:.4f}")
    
    def predict(self, X, threshold=0.5):
        """Realiza predicciones"""
        output = self.forward(X)
        return (output > threshold).astype(int)


# Ejemplo de uso con compuerta XOR
if __name__ == "__main__":
    # Datos de entrenamiento (XOR)
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([[0], [1], [1], [0]])
    
    # Crear y entrenar red neuronal
    nn = NeuralNetwork(layers=[2, 4, 1], learning_rate=0.1)
    print("Entrenando la red neuronal...")
    nn.train(X, y, epochs=5000)
    
    # Predicciones finales
    print("\nPredicciones finales:")
    for i in range(len(X)):
        prediction = nn.predict(X[i:i+1])[0][0]
        print(f"Entrada: {X[i]}, Predicción: {prediction}")
    
    # Visualización de la frontera de decisión
    plt.figure(figsize=(8, 6))
    x_min, x_max = -0.5, 1.5
    y_min, y_max = -0.5, 1.5
    h = 0.01
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    
    Z = nn.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    plt.contourf(xx, yy, Z, alpha=0.8)
    plt.scatter(X[:, 0], X[:, 1], c=y.ravel(), edgecolors='k')
    plt.title("Frontera de Decisión para XOR")
    plt.show()