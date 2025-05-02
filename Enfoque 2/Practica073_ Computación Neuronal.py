# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 17:36:38 2025

@author: elvin
"""

# Importación de bibliotecas necesarias
import numpy as np  # Para operaciones numéricas eficientes
import matplotlib.pyplot as plt  # Para visualización de resultados

class RedNeuronal:
    def __init__(self, capas=[2, 4, 1], tasa_aprendizaje=0.1):
        """
        Constructor de la red neuronal
        Args:
            capas: lista con número de neuronas en cada capa (ej. [entrada, oculta, salida])
            tasa_aprendizaje: factor que controla el tamaño de los ajustes en los pesos
        """
        self.capas = capas  # Configuración de la arquitectura de la red
        self.lr = tasa_aprendizaje  # Tasa de aprendizaje (learning rate)
        
        # Inicialización de pesos y sesgos (biases)
        self.pesos = []  # Lista para almacenar matrices de pesos
        self.sesgos = []  # Lista para almacenar vectores de sesgo
        
        # Inicialización Xavier/Glorot para mejores resultados en el entrenamiento
        for i in range(len(capas)-1):  # Para cada conexión entre capas
            # Inicialización de pesos con distribución normal ajustada
            w = np.random.randn(capas[i], capas[i+1]) * np.sqrt(2./capas[i])
            # Inicialización de sesgos en cero
            b = np.zeros((1, capas[i+1]))
            self.pesos.append(w)  # Añade pesos inicializados
            self.sesgos.append(b)  # Añade sesgos inicializados
    
    def sigmoide(self, x):
        """Función de activación sigmoide (transforma valores a rango 0-1)"""
        return 1 / (1 + np.exp(-x))
    
    def derivada_sigmoide(self, x):
        """Derivada de la función sigmoide (usada en backpropagation)"""
        return x * (1 - x)
    
    def forward(self, X):
        """Propagación hacia adelante (calcula las salidas de la red)"""
        self.activaciones = [X]  # Almacena activaciones de cada capa
        self.zs = []  # Almacena valores z (antes de aplicar activación)
        
        # Para cada capa de la red...
        for i in range(len(self.pesos)):
            # Calcula combinación lineal de entradas y pesos
            z = np.dot(self.activaciones[-1], self.pesos[i]) + self.sesgos[i]
            # Aplica función de activación
            a = self.sigmoide(z)
            self.zs.append(z)  # Guarda valor antes de activación
            self.activaciones.append(a)  # Guarda valor después de activación
        
        return self.activaciones[-1]  # Devuelve salida final de la red
    
    def backward(self, X, y, output):
        """Propagación hacia atrás (calcula gradientes y ajusta pesos)"""
        m = X.shape[0]  # Número de ejemplos de entrenamiento
        
        # Error en la capa de salida
        error = output - y
        
        # Listas para almacenar gradientes
        dW = []  # Gradientes de los pesos
        db = []  # Gradientes de los sesgos
        
        # Backpropagation (comenzando desde la última capa)
        for i in reversed(range(len(self.pesos))):
            # Cálculo del delta (error propagado)
            if i == len(self.pesos)-1:  # Para capa de salida
                delta = error * self.derivada_sigmoide(output)
            else:  # Para capas ocultas
                delta = np.dot(delta, self.pesos[i+1].T) * self.derivada_sigmoide(self.activaciones[i+1])
            
            # Calcula gradientes para pesos y sesgos
            dw = np.dot(self.activaciones[i].T, delta) / m
            dbias = np.sum(delta, axis=0, keepdims=True) / m
            
            # Guarda gradientes (en orden inverso)
            dW.insert(0, dw)
            db.insert(0, dbias)
        
        # Actualiza pesos y sesgos usando gradiente descendente
        for i in range(len(self.pesos)):
            self.pesos[i] -= self.lr * dW[i]  # Ajuste de pesos
            self.sesgos[i] -= self.lr * db[i]  # Ajuste de sesgos
    
    def entrenar(self, X, y, epocas=1000, verbose=True):
        """Método para entrenar la red neuronal"""
        for epoca in range(epocas):
            # Paso forward (cálculo de predicciones)
            output = self.forward(X)
            # Paso backward (ajuste de pesos)
            self.backward(X, y, output)
            
            # Mostrar progreso del entrenamiento
            if verbose and epoca % 100 == 0:
                # Cálculo del error cuadrático medio
                perdida = np.mean(np.square(output - y))
                print(f"Época {epoca}, Pérdida: {perdida:.4f}")
    
    def predecir(self, X, umbral=0.5):
        """Método para hacer predicciones después del entrenamiento"""
        y_pred = self.forward(X)  # Obtiene predicciones continuas
        return (y_pred > umbral).astype(int)  # Convierte a predicciones binarias
    
    def graficar_perdida(self, X, y, epocas=1000):
        """Método para visualizar la reducción del error durante el entrenamiento"""
        perdidas = []  # Almacena valores de pérdida
        
        for _ in range(epocas):
            output = self.forward(X)
            self.backward(X, y, output)
            perdida = np.mean(np.square(output - y))
            perdidas.append(perdida)  # Guarda valor de pérdida
        
        # Configuración del gráfico
        plt.plot(perdidas)
        plt.title("Curva de Aprendizaje")
        plt.xlabel("Época")
        plt.ylabel("Pérdida")
        plt.show()

# Bloque principal de ejecución
if __name__ == "__main__":
    # Datos de entrenamiento (compuerta XOR)
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])  # Entradas
    y = np.array([[0], [1], [1], [0]])  # Salidas esperadas
    
    # Crear instancia de la red neuronal
    rn = RedNeuronal(capas=[2, 4, 1], tasa_aprendizaje=0.1)
    
    # Entrenamiento de la red
    print("Entrenando la red neuronal...")
    rn.entrenar(X, y, epocas=5000)
    
    # Visualización de la curva de aprendizaje
    rn.graficar_perdida(X, y, epocas=5000)
    
    # Predicción final
    print("\nPredicciones finales:")
    for i in range(len(X)):
        prediccion = rn.predecir(X[i:i+1])[0][0]
        print(f"Entrada: {X[i]}, Predicción: {prediccion}")
    
    # Visualización de la frontera de decisión
    plt.figure(figsize=(8, 6))
    # Crear malla para evaluación
    x_min, x_max = -0.5, 1.5
    y_min, y_max = -0.5, 1.5
    h = 0.01
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), 
                         np.arange(y_min, y_max, h))
    
    # Predecir para toda la malla
    Z = rn.predecir(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    # Graficar resultados
    plt.contourf(xx, yy, Z, alpha=0.8)
    plt.scatter(X[:, 0], X[:, 1], c=y.ravel(), edgecolors='k')
    plt.title("Frontera de Decisión para XOR")
    plt.show()