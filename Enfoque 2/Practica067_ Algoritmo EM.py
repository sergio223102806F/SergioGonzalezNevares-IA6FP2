# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 16:20:26 2025

@author: elvin
"""

# Importación de bibliotecas necesarias
import numpy as np  # Para operaciones numéricas y manejo de arrays
from scipy.stats import multivariate_normal  # Para cálculos de distribuciones normales multivariadas
import matplotlib.pyplot as plt  # Para visualización de resultados

class GaussianMixtureEM:
    """
    Implementación completa del algoritmo Expectation-Maximization (EM)
    para estimación de Mezclas Gaussianas (Gaussian Mixture Models - GMM).
    """
    
    def __init__(self, n_components=3, max_iter=100, tol=1e-6):
        """
        Inicializa el modelo de mezcla gaussiana.
        
        Args:
            n_components (int): Número de distribuciones gaussianas en la mezcla
            max_iter (int): Máximo número de iteraciones permitidas
            tol (float): Tolerancia para determinar convergencia (cambio mínimo en log-verosimilitud)
        """
        self.n_components = n_components  # K en el modelo
        self.max_iter = max_iter  # Límite de iteraciones
        self.tol = tol  # Umbral de convergencia
        self.weights = None  # Pesos de mezcla (π_k)
        self.means = None  # Medias de cada componente (μ_k)
        self.covariances = None  # Matrices de covarianza (Σ_k)
        self.responsibilities = None  # Matriz de responsabilidades (γ_nk)
        self.log_likelihood_history = []  # Historial de verosimilitud para monitorear convergencia
    
    def initialize_parameters(self, X):
        """
        Inicializa los parámetros del modelo de manera aleatoria pero inteligente.
        
        Args:
            X (np.array): Datos de entrada con forma (n_muestras, n_características)
        """
        n_samples, n_features = X.shape
        
        # 1. Inicializar pesos: distribución uniforme al inicio
        self.weights = np.ones(self.n_components) / self.n_components
        
        # 2. Seleccionar muestras aleatorias como centros iniciales (más estable que puramente aleatorio)
        random_idx = np.random.choice(n_samples, self.n_components, replace=False)
        self.means = X[random_idx]  # Medias iniciales
        
        # 3. Inicializar covarianzas como matrices de identidad (evita matrices singulares)
        self.covariances = np.array([np.eye(n_features) for _ in range(self.n_components)])
    
    def e_step(self, X):
        """
        Paso Expectation (E): Calcula las responsabilidades (probabilidades posteriores)
        de cada componente para cada punto de datos.
        
        Args:
            X (np.array): Datos de entrada (n_muestras, n_características)
            
        Returns:
            float: Log-verosimilitud actual del modelo
        """
        n_samples = X.shape[0]
        self.responsibilities = np.zeros((n_samples, self.n_components))
        
        # Calcular la densidad de probabilidad para cada componente k
        for k in range(self.n_components):
            self.responsibilities[:, k] = self.weights[k] * \
                multivariate_normal.pdf(X, mean=self.means[k], cov=self.covariances[k])
        
        # Normalizar las responsabilidades para que sumen 1 por fila (por muestra)
        sum_resp = self.responsibilities.sum(axis=1, keepdims=True)
        self.responsibilities = np.where(sum_resp > 0, self.responsibilities / sum_resp, 0)
        
        # Calcular la log-verosimilitud marginal (para monitorear convergencia)
        log_likelihood = np.log(sum_resp).sum()
        self.log_likelihood_history.append(log_likelihood)
        
        return log_likelihood
    
    def m_step(self, X):
        """
        Paso Maximization (M): Actualiza los parámetros del modelo maximizando
        la verosimilitud esperada calculada en el E-step.
        
        Args:
            X (np.array): Datos de entrada (n_muestras, n_características)
        """
        n_samples = X.shape[0]
        
        # 1. Actualizar pesos de mezcla (proporción de puntos asignados a cada componente)
        self.weights = self.responsibilities.mean(axis=0)
        
        # 2. Actualizar medias (centroides ponderados por responsabilidad)
        self.means = np.zeros_like(self.means)  # Reiniciar medias
        for k in range(self.n_components):
            # Suma ponderada de los puntos (responsabilidad como peso)
            weighted_sum = (self.responsibilities[:, k, np.newaxis] * X).sum(axis=0)
            # Normalizar por la suma total de responsabilidades
            sum_resp_k = self.responsibilities[:, k].sum()
            self.means[k] = weighted_sum / sum_resp_k if sum_resp_k > 0 else self.means[k]
        
        # 3. Actualizar matrices de covarianza
        self.covariances = np.zeros_like(self.covariances)  # Reiniciar covarianzas
        for k in range(self.n_components):
            diff = X - self.means[k]  # Diferencias respecto a la media
            # Cálculo eficiente de la covarianza ponderada usando einsum
            weighted_cov = (self.responsibilities[:, k, np.newaxis, np.newaxis] * 
                          np.einsum('ij,ik->ijk', diff, diff)).sum(axis=0)
            sum_resp_k = self.responsibilities[:, k].sum()
            self.covariances[k] = weighted_cov / sum_resp_k if sum_resp_k > 0 else self.covariances[k]
            
            # Añadir pequeña constante a la diagonal para evitar matrices singulares
            self.covariances[k] += 1e-6 * np.eye(X.shape[1])
    
    def fit(self, X):
        """
        Ajusta el modelo a los datos mediante el algoritmo EM iterativo.
        
        Args:
            X (np.array): Datos de entrada (n_muestras, n_características)
        """
        # 1. Inicialización de parámetros
        self.initialize_parameters(X)
        
        # 2. Iteración EM hasta convergencia o máximo de iteraciones
        for i in range(self.max_iter):
            # a. Paso Expectation (E)
            log_likelihood = self.e_step(X)
            
            # b. Paso Maximization (M)
            self.m_step(X)
            
            # c. Verificar convergencia (cambio pequeño en log-verosimilitud)
            if i > 0 and abs(log_likelihood - self.log_likelihood_history[-2]) < self.tol:
                print(f"Convergencia alcanzada en iteración {i+1}")
                break
    
    def predict(self, X):
        """
        Asigna cada punto al componente más probable (hard clustering).
        
        Args:
            X (np.array): Datos a clasificar (n_muestras, n_características)
            
        Returns:
            np.array: Etiquetas de componente predichas (n_muestras,)
        """
        # Primero calcular responsabilidades
        self.e_step(X)
        # Seleccionar componente con mayor responsabilidad para cada punto
        return np.argmax(self.responsibilities, axis=1)
    
    def plot_results(self, X, true_labels=None):
        """
        Visualización de los resultados (solo para datos 2D).
        
        Args:
            X (np.array): Datos de entrada (n_muestras, 2)
            true_labels (np.array): Etiquetas reales (opcional, para comparación)
        """
        if X.shape[1] != 2:
            print("Visualización solo disponible para datos 2D")
            return
        
        plt.figure(figsize=(10, 6))
        
        # Graficar los puntos de datos
        if true_labels is not None:
            plt.scatter(X[:, 0], X[:, 1], c=true_labels, s=20, cmap='viridis', alpha=0.6, label='Datos reales')
        else:
            plt.scatter(X[:, 0], X[:, 1], s=20, alpha=0.6, label='Datos')
        
        # Crear grid para visualizar las distribuciones estimadas
        x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
        y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
        xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100),
                             np.linspace(y_min, y_max, 100))
        
        # Graficar contornos de cada componente gaussiana
        for k in range(self.n_components):
            # Calcular PDF en el grid
            zz = multivariate_normal.pdf(np.c_[xx.ravel(), yy.ravel()], 
                                       mean=self.means[k], 
                                       cov=self.covariances[k])
            zz = zz.reshape(xx.shape)
            # Dibujar contornos en 3 niveles de densidad
            plt.contour(xx, yy, zz, levels=3, colors=f'C{k}', linewidths=2, 
                        linestyles=['--', '-', '--'], alpha=0.8)
            # Marcar el centro de la gaussiana
            plt.scatter(self.means[k, 0], self.means[k, 1], marker='x', 
                        color=f'C{k}', s=100, linewidths=2, label=f'Componente {k+1}')
        
        plt.title('Mezcla de Gaussianas - Resultado del EM')
        plt.xlabel('Característica 1')
        plt.ylabel('Característica 2')
        plt.legend()
        plt.grid(True)
        plt.show()
        
        # Graficar la evolución de la log-verosimilitud
        plt.figure(figsize=(10, 4))
        plt.plot(self.log_likelihood_history, 'o-')
        plt.title('Convergencia del Algoritmo EM')
        plt.xlabel('Iteración')
        plt.ylabel('Log-Verisimilitud')
        plt.grid(True)
        plt.show()

# Ejemplo de uso completo
if __name__ == "__main__":
    # 1. Generar datos sintéticos de una mezcla de 3 gaussianas 2D
    np.random.seed(42)  # Para reproducibilidad
    n_samples = 500
    
    # Parámetros reales de la mezcla (desconocidos para el modelo)
    true_means = np.array([[0, 0], [4, 4], [-3, 5]])  # Medias reales
    true_covs = np.array([[[1, 0.5], [0.5, 1]],  # Covarianzas reales
                         [[1, -0.4], [-0.4, 1]],
                         [[0.7, 0], [0, 0.7]]])
    true_weights = np.array([0.3, 0.5, 0.2])  # Pesos reales
    
    # Generar muestras de cada componente
    X_components = [
        np.random.multivariate_normal(true_means[i], true_covs[i], 
        int(n_samples * true_weights[i]))
        for i in range(3)
    ]
    
    # Concatenar todos los componentes
    X = np.vstack(X_components)
    true_labels = np.concatenate([np.full(int(n_samples * true_weights[i]), i) 
                                for i in range(3)])
    
    # Mezclar los datos (aleatorizar el orden)
    shuffle_idx = np.random.permutation(n_samples)
    X = X[shuffle_idx]
    true_labels = true_labels[shuffle_idx]
    
    # 2. Crear e instanciar el modelo GMM
    print("Inicializando modelo GMM con EM...")
    gmm = GaussianMixtureEM(n_components=3, max_iter=50, tol=1e-4)
    
    # 3. Ajustar el modelo a los datos
    gmm.fit(X)
    
    # 4. Predecir las etiquetas de componente
    pred_labels = gmm.predict(X)
    
    # 5. Mostrar resultados
    print("\nResultados del ajuste:")
    print("Pesos estimados:", np.round(gmm.weights, 3))
    print("Medias estimadas:\n", np.round(gmm.means, 2))
    
    print("\nComparación con valores reales:")
    print("Pesos reales:", true_weights)
    print("Medias reales:\n", true_means)
    
    # 6. Visualizar resultados
    gmm.plot_results(X, true_labels)