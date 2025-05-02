# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 18:07:18 2025

@author: elvin
"""

# Importación de bibliotecas esenciales
import numpy as np  # Para operaciones numéricas eficientes
import matplotlib.pyplot as plt  # Para visualización de gráficos
from sklearn.datasets import make_classification, make_moons, make_circles  # Para generar datasets de prueba

class Perceptron:
    """
    Implementación del algoritmo Perceptrón para clasificación binaria.
    Este modelo solo puede aprender fronteras de decisión lineales.
    """
    
    def __init__(self, lr=0.01, epochs=1000):
        """
        Inicializa el perceptrón con parámetros de entrenamiento.
        
        Args:
            lr (float): Tasa de aprendizaje (learning rate)
            epochs (int): Número máximo de iteraciones de entrenamiento
        """
        self.lr = lr          # Controla el tamaño de los ajustes en los pesos
        self.epochs = epochs  # Límite de iteraciones para el entrenamiento
        self.weights = None   # Almacenará los pesos aprendidos
        self.bias = None      # Almacenará el sesgo (bias) aprendido
    
    def fit(self, X, y):
        """
        Entrena el modelo perceptrón con los datos proporcionados.
        
        Args:
            X (ndarray): Matriz de características (n_samples, n_features)
            y (ndarray): Vector de etiquetas (n_samples,)
        """
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)  # Inicializa pesos en cero
        self.bias = 0  # Inicializa el bias en cero
        
        # Bucle principal de entrenamiento
        for _ in range(self.epochs):
            for idx, x_i in enumerate(X):  # Itera sobre cada muestra
                # Calcula la condición de clasificación correcta
                condition = y[idx] * (np.dot(x_i, self.weights) + self.bias) >= 0
                
                # Si la clasificación es incorrecta, ajusta pesos y bias
                if not condition:
                    self.weights += self.lr * y[idx] * x_i  # Actualiza pesos
                    self.bias += self.lr * y[idx]  # Actualiza bias
    
    def predict(self, X):
        """
        Realiza predicciones sobre nuevos datos.
        
        Args:
            X (ndarray): Datos a predecir (n_samples, n_features)
            
        Returns:
            ndarray: Vector de predicciones (-1 o 1 para cada muestra)
        """
        return np.sign(np.dot(X, self.weights) + self.bias)  # Aplica función signo


def test_separabilidad():
    """
    Función para demostrar el concepto de separabilidad lineal.
    Genera tres tipos de datasets y muestra el rendimiento del perceptrón en cada uno.
    """
    # 1. Generación de datasets sintéticos
    # Dataset linealmente separable
    X_linear, y_linear = make_classification(
        n_samples=100, n_features=2, n_classes=2, 
        n_clusters_per_class=1, random_state=42)
    
    # Dataset no lineal (forma de lunas)
    X_moons, y_moons = make_moons(n_samples=100, noise=0.1, random_state=42)
    
    # Dataset no lineal (círculos concéntricos)
    X_circles, y_circles = make_circles(n_samples=100, noise=0.05, random_state=42)
    
    # 2. Preparación de etiquetas (convertir a -1 y 1)
    y_linear = np.where(y_linear == 0, -1, 1)
    y_moons = np.where(y_moons == 0, -1, 1)
    y_circles = np.where(y_circles == 0, -1, 1)
    
    # 3. Configuración de la figura para visualización
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Lista de datasets a evaluar
    datasets = [
        ("Linealmente Separable", X_linear, y_linear),
        ("No Lineal (Lunas)", X_moons, y_moons),
        ("No Lineal (Círculos)", X_circles, y_circles)
    ]
    
    # 4. Evaluación del perceptrón en cada dataset
    for idx, (title, X, y) in enumerate(datasets):
        # Crear y entrenar perceptrón
        perceptron = Perceptron()
        perceptron.fit(X, y)
        
        # Calcular precisión
        y_pred = perceptron.predict(X)
        accuracy = np.mean(y_pred == y)
        
        # Graficar puntos de datos
        axes[idx].scatter(X[:, 0], X[:, 1], c=y, cmap='bwr', edgecolors='k')
        
        # Crear malla para visualizar frontera de decisión
        x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
        y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
        xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100),
                            np.linspace(y_min, y_max, 100))
        
        # Predecir para toda la malla
        Z = perceptron.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)
        
        # Dibujar frontera de decisión
        axes[idx].contourf(xx, yy, Z, alpha=0.3, cmap='bwr')
        
        # Configurar título y etiquetas
        axes[idx].set_title(f"{title}\nPrecisión: {accuracy:.2%}")
        axes[idx].set_xlabel("Feature 1")
        axes[idx].set_ylabel("Feature 2")
    
    # Mostrar gráficos
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Ejecutar la demostración
    test_separabilidad()