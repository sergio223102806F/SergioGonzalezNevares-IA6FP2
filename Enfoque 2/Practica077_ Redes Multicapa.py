# -*- coding: utf-8 -*-                                                     # Define la codificación de caracteres del archivo como UTF-8
"""
Created on Sat Apr 26 18:14:18 2025                                         # Indica la fecha y hora de creación del archivo
                                                                           #
@author: elvin                                                              # Define el autor del archivo
"""

# Importación de bibliotecas esenciales                                      # Comentario general sobre las importaciones
import numpy as np  # Para operaciones numéricas eficientes                 # Importa la biblioteca NumPy y la asigna el alias 'np'
import matplotlib.pyplot as plt  # Para visualización de gráficos        # Importa la biblioteca Matplotlib y la asigna el alias 'plt'
from sklearn.datasets import make_classification, make_moons, make_circles  # Para generar datasets de prueba # Importa funciones para crear conjuntos de datos

class Perceptron:                                                          # Define una nueva clase llamada Perceptron
    """
    Implementación del algoritmo Perceptrón para clasificación binaria.    # Documentación de la clase Perceptron
    Este modelo solo puede aprender fronteras de decisión lineales.         # Información sobre la capacidad del modelo
    """

    def __init__(self, lr=0.01, epochs=1000):                             # Define el constructor de la clase Perceptron con valores predeterminados
        """
        Inicializa el perceptrón con parámetros de entrenamiento.         # Documentación del constructor
        Args:                                                               # Inicio de la sección de argumentos
            lr (float): Tasa de aprendizaje (learning rate)                # Descripción del argumento 'lr'
            epochs (int): Número máximo de iteraciones de entrenamiento    # Descripción del argumento 'epochs'
        """
        self.lr = lr          # Controla el tamaño de los ajustes en los pesos # Asigna la tasa de aprendizaje al atributo self.lr
        self.epochs = epochs  # Límite de iteraciones para el entrenamiento  # Asigna el número máximo de épocas al atributo self.epochs
        self.weights = None   # Almacenará los pesos aprendidos               # Inicializa el atributo de pesos como None
        self.bias = None      # Almacenará el sesgo (bias) aprendido          # Inicializa el atributo de sesgo como None

    def fit(self, X, y):                                                    # Define el método para entrenar el Perceptrón
        """
        Entrena el modelo perceptrón con los datos proporcionados.         # Documentación del método fit
        Args:                                                               # Inicio de la sección de argumentos
            X (ndarray): Matriz de características (n_samples, n_features)  # Descripción del argumento 'X'
            y (ndarray): Vector de etiquetas (n_samples,)                   # Descripción del argumento 'y'
        """
        n_samples, n_features = X.shape                                     # Obtiene el número de muestras y características de la matriz de datos X
        self.weights = np.zeros(n_features)  # Inicializa pesos en cero     # Inicializa el vector de pesos con ceros
        self.bias = 0  # Inicializa el bias en cero                        # Inicializa el sesgo en cero

        # Bucle principal de entrenamiento                               # Comentario indicando el bucle de entrenamiento
        for _ in range(self.epochs):                                       # Itera sobre el número de épocas
            for idx, x_i in enumerate(X):  # Itera sobre cada muestra       # Itera sobre cada muestra (x_i) y su índice (idx) en la matriz de datos X
                # Calcula la condición de clasificación correcta           # Comentario indicando el cálculo de la condición
                condition = y[idx] * (np.dot(x_i, self.weights) + self.bias) >= 0 # Verifica si la muestra está correctamente clasificada

                # Si la clasificación es incorrecta, ajusta pesos y bias    # Comentario indicando el ajuste de parámetros
                if not condition:                                           # Si la condición no se cumple (clasificación incorrecta)
                    self.weights += self.lr * y[idx] * x_i  # Actualiza pesos # Actualiza el vector de pesos según la regla del Perceptrón
                    self.bias += self.lr * y[idx]  # Actualiza bias        # Actualiza el sesgo según la regla del Perceptrón

    def predict(self, X):                                                  # Define el método para realizar predicciones
        """
        Realiza predicciones sobre nuevos datos.                          # Documentación del método predict
        Args:                                                               # Inicio de la sección de argumentos
            X (ndarray): Datos a predecir (n_samples, n_features)          # Descripción del argumento 'X'

        Returns:                                                            # Inicio de la sección de retorno
            ndarray: Vector de predicciones (-1 o 1 para cada muestra)      # Descripción del valor de retorno
        """
        return np.sign(np.dot(X, self.weights) + self.bias)  # Aplica función signo # Calcula la salida y aplica la función signo para obtener la predicción


def test_separabilidad():                                                # Define la función para probar la separabilidad lineal
    """
    Función para demostrar el concepto de separabilidad lineal.         # Documentación de la función test_separabilidad
    Genera tres tipos de datasets y muestra el rendimiento del perceptrón en cada uno. # Descripción del propósito de la función
    """
    # 1. Generación de datasets sintéticos                             # Comentario indicando la generación de datasets
    # Dataset linealmente separable                                    # Comentario para el dataset linealmente separable
    X_linear, y_linear = make_classification(                            # Genera un conjunto de datos linealmente separable
        n_samples=100, n_features=2, n_classes=2,
        n_clusters_per_class=1, random_state=42)

    # Dataset no lineal (forma de lunas)                               # Comentario para el dataset no lineal (lunas)
    X_moons, y_moons = make_moons(n_samples=100, noise=0.1, random_state=42) # Genera un conjunto de datos con forma de lunas

    # Dataset no lineal (círculos concéntricos)                       # Comentario para el dataset no lineal (círculos)
    X_circles, y_circles = make_circles(n_samples=100, noise=0.05, random_state=42) # Genera un conjunto de datos con forma de círculos

    # 2. Preparación de etiquetas (convertir a -1 y 1)                 # Comentario indicando la preparación de etiquetas
    y_linear = np.where(y_linear == 0, -1, 1)                           # Convierte etiquetas 0 a -1 y 1 a 1
    y_moons = np.where(y_moons == 0, -1, 1)                             # Convierte etiquetas 0 a -1 y 1 a 1
    y_circles = np.where(y_circles == 0, -1, 1)                         # Convierte etiquetas 0 a -1 y 1 a 1

    # 3. Configuración de la figura para visualización                # Comentario indicando la configuración de la figura
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))                   # Crea una figura con 3 subplots en una fila

    # Lista de datasets a evaluar                                      # Comentario indicando la lista de datasets
    datasets = [                                                       # Lista de tuplas con título, datos X e etiquetas y
        ("Linealmente Separable", X_linear, y_linear),
        ("No Lineal (Lunas)", X_moons, y_moons),
        ("No Lineal (Círculos)", X_circles, y_circles)
    ]

    # 4. Evaluación del perceptrón en cada dataset                   # Comentario indicando la evaluación del perceptrón
    for idx, (title, X, y) in enumerate(datasets):                    # Itera sobre cada dataset en la lista
        # Crear y entrenar perceptrón                                # Comentario indicando la creación y entrenamiento
        perceptron = Perceptron()                                      # Crea una instancia del Perceptrón
        perceptron.fit(X, y)                                         # Entrena el Perceptrón con los datos

        # Calcular precisión                                         # Comentario indicando el cálculo de la precisión
        y_pred = perceptron.predict(X)                                 # Realiza predicciones sobre los datos de entrenamiento
        accuracy = np.mean(y_pred == y)                                # Calcula la precisión del modelo

        # Graficar puntos de datos                                     # Comentario indicando el gráfico de los puntos
        axes[idx].scatter(X[:, 0], X[:, 1], c=y, cmap='bwr', edgecolors='k') # Dibuja los puntos de datos con colores según la etiqueta

        # Crear malla para visualizar frontera de decisión             # Comentario indicando la creación de la malla
        x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5         # Define los límites del eje x para la malla
        y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5         # Define los límites del eje y para la malla
        xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100),           # Crea una malla de puntos en el espacio de características
                             np.linspace(y_min, y_max, 100))

        # Predecir para toda la malla                                 # Comentario indicando la predicción para la malla
        Z = perceptron.predict(np.c_[xx.ravel(), yy.ravel()])         # Realiza predicciones para todos los puntos de la malla
        Z = Z.reshape(xx.shape)                                        # Redimensiona las predicciones para que coincidan con la forma de la malla

        # Dibujar frontera de decisión                               # Comentario indicando el dibujo de la frontera
        axes[idx].contourf(xx, yy, Z, alpha=0.3, cmap='bwr')           # Dibuja la frontera de decisión en el subplot

        # Configurar título y etiquetas                             # Comentario indicando la configuración del título y etiquetas
        axes[idx].set_title(f"{title}\nPrecisión: {accuracy:.2%}") # Establece el título del subplot con la precisión
        axes[idx].set_xlabel("Feature 1")                              # Establece la etiqueta del eje x
        axes[idx].set_ylabel("Feature 2")                              # Establece la etiqueta del eje y

    # Mostrar gráficos                                               # Comentario indicando la visualización de los gráficos
    plt.tight_layout()                                                 # Ajusta el espaciado entre subplots
    plt.show()                                                         # Muestra la figura


if __name__ == "__main__":                                               # Asegura que el código dentro solo se ejecute si el script es el principal
    # Ejecutar la demostración                                         # Comentario indicando la ejecución de la demostración
    test_separabilidad()                                               # Llama a la función para probar la separabilidad lineal