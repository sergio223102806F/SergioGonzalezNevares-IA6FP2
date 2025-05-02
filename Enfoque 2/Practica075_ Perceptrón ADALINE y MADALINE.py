# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 17:46:11 2025

@author: elvin
"""

# Importación de bibliotecas necesarias
import numpy as np  # Para operaciones numéricas eficientes
import matplotlib.pyplot as plt  # Para visualización de resultados
from sklearn.datasets import make_classification  # Para generar datos de ejemplo

class Perceptron:
    def __init__(self, learning_rate=0.01, n_iters=1000):
        """
        Constructor del Perceptrón
        Args:
            learning_rate: Controla el tamaño de los ajustes en los pesos
            n_iters: Número máximo de iteraciones de entrenamiento
        """
        self.lr = learning_rate  # Tasa de aprendizaje
        self.n_iters = n_iters  # Límite de épocas de entrenamiento
        self.weights = None  # Se inicializarán en fit()
        self.bias = None  # Sesgo (bias)
        self.errors = []  # Registrará errores por época

    def activation(self, x):
        """Función escalón (Heaviside) para clasificación binaria"""
        return np.where(x >= 0, 1, 0)  # 1 si x >= 0, 0 en otro caso

    def fit(self, X, y):
        """Método de entrenamiento"""
        n_samples, n_features = X.shape
        
        # 1. Inicialización de parámetros
        self.weights = np.zeros(n_features)  # Vector de pesos inicializado en 0
        self.bias = 0  # Sesgo inicial
        
        # 2. Bucle principal de entrenamiento
        for _ in range(self.n_iters):
            total_error = 0  # Contador de errores por época
            
            # 3. Iterar sobre cada muestra de entrenamiento
            for idx, x_i in enumerate(X):
                # 4. Calcular la salida lineal (producto punto + sesgo)
                linear_output = np.dot(x_i, self.weights) + self.bias
                
                # 5. Aplicar función de activación
                y_pred = self.activation(linear_output)
                
                # 6. Calcular error (diferencia entre predicción y valor real)
                error = y[idx] - y_pred
                total_error += abs(error)  # Sumar error absoluto
                
                # 7. Actualizar pesos y sesgo (Regla del Perceptrón)
                self.weights += self.lr * error * x_i
                self.bias += self.lr * error
            
            # 8. Registrar errores por época
            self.errors.append(total_error)
            
            # 9. Criterio de parada temprana (si clasifica todo correctamente)
            if total_error == 0:
                break

    def predict(self, X):
        """Método para hacer predicciones"""
        linear_output = np.dot(X, self.weights) + self.bias  # Cálculo lineal
        return self.activation(linear_output)  # Aplicar función escalón


class ADALINE:
    def __init__(self, learning_rate=0.01, n_iters=1000):
        """Inicializa ADALINE con parámetros de entrenamiento"""
        self.lr = learning_rate
        self.n_iters = n_iters
        self.weights = None
        self.bias = None
        self.losses = []  # Para registrar el error cuadrático medio

    def activation(self, x):
        """Función de identidad (sin transformación)"""
        return x  # ADALINE usa salida lineal durante entrenamiento

    def compute_loss(self, y_true, y_pred):
        """Calcula el error cuadrático medio"""
        return 0.5 * np.mean((y_true - y_pred)**2)  # Factor 0.5 para simplificar derivada

    def fit(self, X, y):
        """Entrenamiento con Regla Delta"""
        n_samples, n_features = X.shape
        
        # 1. Inicialización de parámetros
        self.weights = np.zeros(n_features)
        self.bias = 0
        
        # 2. Bucle de entrenamiento
        for _ in range(self.n_iters):
            # 3. Calcular predicciones (sin función de activación)
            linear_output = np.dot(X, self.weights) + self.bias
            y_pred = self.activation(linear_output)
            
            # 4. Calcular y almacenar pérdida
            loss = self.compute_loss(y, y_pred)
            self.losses.append(loss)
            
            # 5. Calcular gradientes (derivadas parciales)
            dw = -np.dot(X.T, (y - y_pred)) / n_samples  # Gradiente de pesos
            db = -np.mean(y - y_pred)  # Gradiente del sesgo
            
            # 6. Actualizar parámetros (Descenso de gradiente)
            self.weights -= self.lr * dw
            self.bias -= self.lr * db

    def predict(self, X):
        """Predicción con umbral en 0"""
        linear_output = np.dot(X, self.weights) + self.bias
        return np.where(linear_output >= 0, 1, 0)  # Clasificación binaria


class MADALINE:
    def __init__(self, learning_rate=0.01, n_iters=1000, n_units=2):
        """Inicializa red MADALINE con múltiples ADALINEs"""
        self.lr = learning_rate
        self.n_iters = n_iters
        self.n_units = n_units
        # Crear capa oculta de unidades ADALINE
        self.adalines = [ADALINE(learning_rate, n_iters) for _ in range(n_units)]
        # Pesos para la capa de salida
        self.output_weights = np.random.rand(n_units)  # Inicialización aleatoria
        self.output_bias = np.random.rand()  # Sesgo de salida
        self.losses = []  # Historial de pérdidas

    def activation(self, x):
        """Sigmoide para la capa de salida"""
        return 1 / (1 + np.exp(-x))  # Transforma a rango (0,1)

    def fit(self, X, y):
        """Entrenamiento en dos fases"""
        # Fase 1: Entrenar cada ADALINE individualmente
        for adaline in self.adalines:
            adaline.fit(X, y)
        
        # Fase 2: Entrenar capa de salida
        for _ in range(self.n_iters):
            # 1. Calcular salidas de la capa oculta
            hidden_outputs = np.array([
                adaline.activation(np.dot(X, adaline.weights) + adaline.bias) 
                for adaline in self.adalines
            ]).T  # Transponer para formato correcto
            
            # 2. Calcular salida final (con sigmoide)
            output = self.activation(
                np.dot(hidden_outputs, self.output_weights) + self.output_bias
            )
            
            # 3. Calcular y almacenar pérdida
            loss = 0.5 * np.mean((y - output)**2)
            self.losses.append(loss)
            
            # 4. Calcular error y delta para backpropagation
            error = output - y
            delta_output = error * output * (1 - output)  # Derivada de sigmoide
            
            # 5. Actualizar pesos de salida
            self.output_weights -= self.lr * np.dot(hidden_outputs.T, delta_output)
            self.output_bias -= self.lr * np.sum(delta_output)

    def predict(self, X):
        """Genera predicciones"""
        # 1. Calcular salidas de la capa oculta
        hidden_outputs = np.array([
            adaline.activation(np.dot(X, adaline.weights) + adaline.bias)
            for adaline in self.adalines
        ]).T
        
        # 2. Calcular salida final
        output = np.dot(hidden_outputs, self.output_weights) + self.output_bias
        
        # 3. Aplicar umbral de decisión
        return np.where(output >= 0.5, 1, 0)  # Clasificación binaria


# Bloque principal de ejecución
if __name__ == "__main__":
    # 1. Generar datos de clasificación binaria
    X, y = make_classification(
        n_samples=100,  # 100 muestras
        n_features=2,  # 2 características
        n_classes=2,  # 2 clases
        n_clusters_per_class=1,  # 1 grupo por clase
        random_state=42  # Semilla para reproducibilidad
    )
    
    # 2. Crear instancias de los modelos
    perceptron = Perceptron(learning_rate=0.01, n_iters=100)
    adaline = ADALINE(learning_rate=0.001, n_iters=200)
    madaline = MADALINE(learning_rate=0.001, n_iters=300, n_units=2)
    
    # 3. Entrenar modelos
    perceptron.fit(X, y)
    adaline.fit(X, y)
    madaline.fit(X, y)
    
    # 4. Visualizar curvas de aprendizaje
    plt.figure(figsize=(15, 5))
    
    # Gráfico del Perceptrón
    plt.subplot(131)
    plt.plot(perceptron.errors)
    plt.title("Perceptrón - Errores por época")
    plt.xlabel("Época")
    plt.ylabel("Errores")
    
    # Gráfico de ADALINE
    plt.subplot(132)
    plt.plot(adaline.losses)
    plt.title("ADALINE - Pérdida por época")
    plt.xlabel("Época")
    plt.ylabel("Error Cuadrático Medio")
    
    # Gráfico de MADALINE
    plt.subplot(133)
    plt.plot(madaline.losses)
    plt.title("MADALINE - Pérdida por época")
    plt.xlabel("Época")
    plt.ylabel("Error Cuadrático Medio")
    
    plt.tight_layout()  # Mejorar espaciado
    plt.show()
    
    # 5. Ejemplo de predicción
    test_sample = np.array([[1.5, -0.5]])  # Datos de prueba
    print(f"\nPredicciones para muestra {test_sample[0]}:")
    print(f"- Perceptrón: {perceptron.predict(test_sample)}")
    print(f"- ADALINE: {adaline.predict(test_sample)}")
    print(f"- MADALINE: {madaline.predict(test_sample)}")