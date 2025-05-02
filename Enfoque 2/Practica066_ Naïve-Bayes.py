# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 15:55:38 2025

@author: elvin
"""

# Importación de bibliotecas necesarias
import numpy as np  # Para operaciones numéricas y manejo de arrays
from collections import defaultdict  # Para diccionarios con valores por defecto
from math import log, exp  # Para cálculos logarítmicos

class NaiveBayes:
    """
    Implementación del clasificador Naïve Bayes para atributos categóricos
    con suavizado de Laplace para manejar valores no vistos durante el entrenamiento.
    """

    def __init__(self, alpha=1):
        """
        Inicializa el clasificador Naïve Bayes.
        
        Args:
            alpha (float): Parámetro de suavizado de Laplace (default=1)
                          Valores más altos dan más peso a la probabilidad uniforme
        """
        self.alpha = alpha  # Para suavizado Laplace (evita probabilidades cero)
        self.class_probs = None  # Almacenará P(clase) - probabilidades a priori
        self.feature_probs = None  # Almacenará P(atributo|clase) - probabilidades condicionales
        self.classes = None  # Lista de clases únicas en los datos

    def fit(self, X, y):
        """
        Entrena el modelo con los datos de entrenamiento.
        
        Args:
            X (np.array): Matriz de características (n_muestras, n_características)
            y (np.array): Vector de etiquetas (n_muestras,)
        """
        n_samples, n_features = X.shape  # Obtener dimensiones de los datos
        self.classes = np.unique(y)  # Encontrar clases únicas
        n_classes = len(self.classes)  # Número de clases
        
        # 1. Calcular probabilidades a priori P(clase) = count(clase) / total_muestras
        self.class_probs = defaultdict(float)  # Diccionario para P(clase)
        class_counts = np.bincount(y)  # Contar ocurrencias de cada clase
        
        for cls in self.classes:
            self.class_probs[cls] = class_counts[cls] / n_samples  # Probabilidad de cada clase
        
        # 2. Calcular probabilidades condicionales P(atributo|clase)
        self.feature_probs = defaultdict(lambda: defaultdict(dict))  # Estructura anidada
        
        for cls in self.classes:
            # Filtrar muestras por clase actual
            X_cls = X[y == cls]  # Todas las muestras de esta clase
            
            for feature in range(n_features):
                # Contar valores únicos y sus frecuencias en este atributo
                feature_values, value_counts = np.unique(X_cls[:, feature], return_counts=True)
                total = value_counts.sum()  # Total de muestras en esta clase
                
                # Calcular probabilidad condicional con suavizado Laplace
                for value, count in zip(feature_values, value_counts):
                    # Fórmula: (count + alpha) / (total + alpha * n_valores_únicos)
                    prob = (count + self.alpha) / (total + self.alpha * len(feature_values))
                    self.feature_probs[cls][feature][value] = prob  # Guardar P(valor|clase)

    def predict(self, X):
        """
        Predice las clases para nuevas muestras.
        
        Args:
            X (np.array): Matriz de características a predecir (n_muestras, n_características)
            
        Returns:
            np.array: Vector de predicciones (n_muestras,)
        """
        predictions = []  # Lista para almacenar resultados
        
        for sample in X:  # Para cada muestra a predecir
            max_prob = -np.inf  # Inicializar con probabilidad muy baja
            best_class = None  # Clase más probable inicial
            
            for cls in self.classes:  # Evaluar cada clase posible
                # Iniciar con probabilidad a priori en escala logarítmica
                log_prob = log(self.class_probs[cls]) if self.class_probs[cls] > 0 else -np.inf
                
                # Calcular probabilidad conjunta (producto de P(atributo|clase))
                for feature, value in enumerate(sample):
                    if value in self.feature_probs[cls][feature]:
                        # Si el valor fue visto en entrenamiento, usar su probabilidad
                        log_prob += log(self.feature_probs[cls][feature][value])
                    else:
                        # Para valores no vistos: suavizado (alpha / (total + alpha * n_valores))
                        total = sum(self.feature_probs[cls][feature].values())
                        n_values = len(self.feature_probs[cls][feature])
                        log_prob += log(self.alpha / (total + self.alpha * n_values))
                
                # Actualizar mejor clase si encontramos mayor probabilidad
                if log_prob > max_prob:
                    max_prob = log_prob
                    best_class = cls
            
            predictions.append(best_class)  # Añadir predicción
        
        return np.array(predictions)  # Convertir a array numpy

    def score(self, X, y):
        """
        Calcula la precisión (accuracy) del modelo.
        
        Args:
            X (np.array): Matriz de características
            y (np.array): Etiquetas verdaderas
            
        Returns:
            float: Precisión del modelo (0 a 1)
        """
        predictions = self.predict(X)  # Obtener predicciones
        return np.mean(predictions == y)  # Calcular porcentaje de aciertos

# Ejemplo de uso con datos categóricos
if __name__ == "__main__":
    # Datos de ejemplo: Clima -> ¿Jugar tenis?
    # Atributos codificados numéricamente:
    # Outlook: 0=Sunny, 1=Overcast, 2=Rain
    # Temp: 0=Hot, 1=Mild, 2=Cool
    # Humidity: 0=High, 1=Normal
    # Wind: 0=Weak, 1=Strong
    # Clase: 0=No jugar, 1=Sí jugar
    
    # Datos de entrenamiento (14 muestras)
    X_train = np.array([
        [0, 0, 0, 0], [0, 0, 0, 1], [1, 0, 0, 0], [2, 1, 0, 0],
        [2, 2, 1, 0], [2, 2, 1, 1], [1, 2, 1, 1], [0, 1, 0, 0],
        [0, 2, 1, 0], [2, 1, 1, 0], [0, 1, 1, 1], [1, 1, 0, 1],
        [1, 0, 1, 0], [2, 1, 0, 1]
    ])
    
    y_train = np.array([0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0])  # Etiquetas

    # 1. Crear y entrenar el modelo
    nb = NaiveBayes(alpha=1)  # alpha=1 es suavizado Laplace estándar
    nb.fit(X_train, y_train)  # Ajustar modelo a datos

    # 2. Datos de prueba (3 muestras nuevas)
    X_test = np.array([
        [0, 0, 0, 1],  # Sunny, Hot, High, Strong
        [1, 2, 1, 0],   # Overcast, Cool, Normal, Weak
        [2, 1, 0, 1]    # Rain, Mild, High, Strong
    ])

    # 3. Realizar predicciones
    predictions = nb.predict(X_test)
    print("Predicciones para datos de prueba:", predictions)

    # 4. Evaluar precisión en datos de entrenamiento (como ejemplo)
    accuracy = nb.score(X_train, y_train)
    print(f"Precisión en datos de entrenamiento: {accuracy:.2f}")

    # 5. Mostrar las probabilidades aprendidas por el modelo
    print("\nProbabilidades aprendidas por el modelo:")
    for cls in nb.classes:
        print(f"\nPara la clase {cls} ('{'No' if cls == 0 else 'Sí'} jugar'):")
        print(f"- Probabilidad a priori P(clase): {nb.class_probs[cls]:.3f}")
        
        print("Probabilidades condicionales P(atributo|clase):")
        for feature_idx in range(X_train.shape[1]):
            feature_name = ["Outlook", "Temperature", "Humidity", "Wind"][feature_idx]
            print(f"  {feature_name}: {dict(nb.feature_probs[cls][feature_idx])}")