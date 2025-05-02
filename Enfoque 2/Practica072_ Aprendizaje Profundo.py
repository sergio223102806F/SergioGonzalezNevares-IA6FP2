# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 17:35:06 2025

@author: elvin
"""

import numpy as np

class NeuralNetwork:
    def __init__(self, layers=[2, 4, 1], learning_rate=0.1):
        """
        Inicializa una red neuronal completamente conectada
        
        Parámetros:
        layers : lista con el número de neuronas en cada capa 
                (ej. [2, 4, 1] = 2 entradas, 1 capa oculta con 4 neuronas, 1 salida)
        learning_rate : tasa de aprendizaje para el descenso de gradiente
        """
        self.layers = layers
        self.lr = learning_rate
        self.weights = []
        self.biases = []
        
        # Inicialización de pesos y sesgos
        for i in range(len(layers)-1):
            # Pesos con inicialización Xavier/Glorot (ajustados por tamaño de capa)
            w = np.random.randn(layers[i], layers[i+1]) * np.sqrt(2./layers[i])
            b = np.zeros((1, layers[i+1]))
            self.weights.append(w)
            self.biases.append(b)
    
    def sigmoid(self, x):
        """Función de activación sigmoide"""
        return 1 / (1 + np.exp(-x))
    
    def sigmoid_derivative(self, x):
        """Derivada de la sigmoide (para backpropagation)"""
        return x * (1 - x)
    
    def forward(self, X):
        """Propagación hacia adelante (forward pass)"""
        self.activations = [X]  # Almacena activaciones de todas las capas
        self.z_values = []      # Almacena valores z (antes de activación)
        
        for i in range(len(self.weights)):
            z = np.dot(self.activations[-1], self.weights[i]) + self.biases[i]
            a = self.sigmoid(z)
            self.z_values.append(z)
            self.activations.append(a)
        
        return self.activations[-1]
    
    def backward(self, X, y, output):
        """Propagación hacia atrás (backpropagation)"""
        m = X.shape[0]  # Número de ejemplos
        
        # Calcula error en la capa de salida
        error = output - y
        dW = []
        db = []
        
        # Backpropagation
        for i in reversed(range(len(self.weights))):
            # Gradiente de la función de pérdida respecto a z
            if i == len(self.weights)-1:
                delta = error * self.sigmoid_derivative(output)
            else:
                delta = np.dot(delta, self.weights[i+1].T) * self.sigmoid_derivative(self.activations[i+1])
            
            # Calcula gradientes para pesos y sesgos
            dw = np.dot(self.activations[i].T, delta) / m
            dbias = np.sum(delta, axis=0, keepdims=True) / m
            
            dW.insert(0, dw)  # Insertamos al inicio para mantener orden
            db.insert(0, dbias)
        
        # Actualiza pesos y sesgos
        for i in range(len(self.weights)):
            self.weights[i] -= self.lr * dW[i]
            self.biases[i] -= self.lr * db[i]
    
    def train(self, X, y, epochs=1000):
        """Entrena la red neuronal"""
        for epoch in range(epochs):
            # Forward pass
            output = self.forward(X)
            
            # Backward pass
            self.backward(X, y, output)
            
            # Mostrar progreso (opcional)
            if epoch % 100 == 0:
                loss = np.mean(np.square(output - y))
                print(f"Época {epoch}, Pérdida: {loss:.4f}")
    
    def predict(self, X):
        """Realiza predicciones"""
        return self.forward(X)