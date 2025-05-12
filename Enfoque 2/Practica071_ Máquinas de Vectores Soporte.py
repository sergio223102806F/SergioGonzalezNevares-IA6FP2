# -*- coding: utf-8 -*-                                                     # Define la codificación de caracteres del archivo como UTF-8
"""
Created on Sat Apr 26 17:19:38 2025                                         # Indica la fecha y hora de creación del archivo
                                                                           #
@author: elvin                                                              # Define el autor del archivo
"""

import numpy as np                                                          # Importa la biblioteca NumPy y la asigna el alias 'np' para operaciones numéricas
from sklearn.base import BaseEstimator                                      # Importa la clase BaseEstimator de scikit-learn para crear estimadores personalizados

class SVM(BaseEstimator):                                                   # Define una nueva clase llamada SVM que hereda de BaseEstimator
    def __init__(self, learning_rate=0.001, lambda_param=0.01, n_iters=1000): # Define el constructor de la clase SVM con valores predeterminados para los parámetros
        """
        Parámetros:                                                         # Documentación de los parámetros del constructor
        learning_rate: Tasa de aprendizaje para el descenso de gradiente     # Descripción del parámetro learning_rate
        lambda_param: Parámetro de regularización                           # Descripción del parámetro lambda_param
        n_iters: Número de iteraciones de entrenamiento                     # Descripción del parámetro n_iters
        """
        self.lr = learning_rate                                             # Asigna el valor de learning_rate al atributo self.lr
        self.lambda_param = lambda_param                                     # Asigna el valor de lambda_param al atributo self.lambda_param
        self.n_iters = n_iters                                               # Asigna el valor de n_iters al atributo self.n_iters
        self.w = None  # Vector de pesos                                     # Inicializa el atributo self.w (vector de pesos) como None
        self.b = None  # Sesgo (bias)                                        # Inicializa el atributo self.b (sesgo) como None

    def fit(self, X, y):                                                    # Define el método fit para entrenar el modelo SVM
        # Convertir etiquetas a -1 y 1 (requerido por SVM)                   # Comentario indicando la conversión de etiquetas
        y_ = np.where(y <= 0, -1, 1)                                         # Convierte las etiquetas <= 0 a -1 y > 0 a 1 usando NumPy
        n_samples, n_features = X.shape                                     # Obtiene el número de muestras y características de la matriz de datos X

        # Inicializar parámetros                                            # Comentario indicando la inicialización de parámetros
        self.w = np.zeros(n_features)                                       # Inicializa el vector de pesos self.w con ceros, con una dimensión igual al número de características
        self.b = 0                                                          # Inicializa el sesgo self.b a 0

        # Descenso de gradiente                                             # Comentario indicando el algoritmo de descenso de gradiente
        for _ in range(self.n_iters):                                       # Itera sobre el número de iteraciones definido
            for idx, x_i in enumerate(X):                                   # Itera sobre cada muestra (x_i) y su índice (idx) en la matriz de datos X
                # Condición para vectores soporte                             # Comentario indicando la condición para los vectores soporte
                condition = y_[idx] * (np.dot(x_i, self.w) - self.b) >= 1   # Calcula la condición para determinar si la muestra está correctamente clasificada con un margen >= 1
                if condition:                                               # Si la condición se cumple (la muestra está correctamente clasificada fuera o en el margen)
                    # Actualizar pesos (sin violar margen)                    # Comentario indicando la actualización de pesos sin violar el margen
                    self.w -= self.lr * (2 * self.lambda_param * self.w)    # Actualiza el vector de pesos aplicando la regularización
                else:                                                      # Si la condición no se cumple (la muestra está mal clasificada o dentro del margen)
                    # Actualizar pesos y sesgo                               # Comentario indicando la actualización de pesos y el sesgo
                    self.w -= self.lr * (2 * self.lambda_param * self.w - np.dot(x_i, y_[idx])) # Actualiza el vector de pesos considerando el error de clasificación
                    self.b -= self.lr * y_[idx]                             # Actualiza el sesgo considerando el error de clasificación

    def predict(self, X):                                                  # Define el método predict para realizar predicciones sobre nuevos datos
        # Calcular el hiperplano de decisión                                 # Comentario indicando el cálculo del hiperplano de decisión
        approx = np.dot(X, self.w) - self.b                                 # Calcula la distancia de cada muestra al hiperplano de decisión
        return np.sign(approx)  # Clasificar en -1 o 1                      # Devuelve la predicción (-1 o 1) basada en el signo de la distancia al hiperplano
   