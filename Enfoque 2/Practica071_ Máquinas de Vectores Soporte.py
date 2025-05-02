# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 17:19:38 2025

@author: elvin
"""

import numpy as np
from sklearn.base import BaseEstimator

class SVM(BaseEstimator):
    def __init__(self, learning_rate=0.001, lambda_param=0.01, n_iters=1000):
        """
        Parámetros:
        learning_rate: Tasa de aprendizaje para el descenso de gradiente
        lambda_param: Parámetro de regularización
        n_iters: Número de iteraciones de entrenamiento
        """
        self.lr = learning_rate
        self.lambda_param = lambda_param
        self.n_iters = n_iters
        self.w = None  # Vector de pesos
        self.b = None  # Sesgo (bias)

    def fit(self, X, y):
        # Convertir etiquetas a -1 y 1 (requerido por SVM)
        y_ = np.where(y <= 0, -1, 1)
        n_samples, n_features = X.shape
        
        # Inicializar parámetros
        self.w = np.zeros(n_features)
        self.b = 0

        # Descenso de gradiente
        for _ in range(self.n_iters):
            for idx, x_i in enumerate(X):
                # Condición para vectores soporte
                condition = y_[idx] * (np.dot(x_i, self.w) - self.b) >= 1
                if condition:
                    # Actualizar pesos (sin violar margen)
                    self.w -= self.lr * (2 * self.lambda_param * self.w)
                else:
                    # Actualizar pesos y sesgo
                    self.w -= self.lr * (2 * self.lambda_param * self.w - np.dot(x_i, y_[idx]))
                    self.b -= self.lr * y_[idx]

    def predict(self, X):
        # Calcular el hiperplano de decisión
        approx = np.dot(X, self.w) - self.b
        return np.sign(approx)  # Clasificar en -1 o 1
    
   