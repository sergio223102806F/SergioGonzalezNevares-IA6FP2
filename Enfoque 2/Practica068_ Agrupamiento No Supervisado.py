# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 16:31:14 2025

@author: elvin
"""

# Importación de bibliotecas necesarias
import numpy as np  # Para operaciones numéricas eficientes
from sklearn.neighbors import NearestNeighbors  # Para búsqueda de vecinos en DBSCAN
import matplotlib.pyplot as plt  # Para visualización de resultados
from sklearn.datasets import make_blobs, make_moons  # Para generar datos de prueba
from scipy.spatial.distance import cdist  # Para cálculo de distancias

class KMeans:
    """
    Implementación completa del algoritmo K-Means para clustering particional.
    """
    
    def __init__(self, n_clusters=3, max_iter=100, tol=1e-4, random_state=None):
        """
        Inicializa los parámetros del algoritmo K-Means.
        
        Args:
            n_clusters (int): Número de grupos/clusters a formar
            max_iter (int): Límite máximo de iteraciones
            tol (float): Umbral de convergencia (cambio mínimo en centroides)
            random_state (int): Semilla para reproducibilidad
        """
        self.n_clusters = n_clusters  # El valor 'k' en k-means
        self.max_iter = max_iter  # Prevenir iteraciones infinitas
        self.tol = tol  # Tolerancia para declarar convergencia
        self.random_state = random_state  # Para resultados reproducibles
        self.centroids = None  # Almacenará los centroides finales
        self.labels = None  # Asignaciones de cluster para cada punto
        self.inertia_ = None  # Suma de distancias cuadradas intra-cluster
    
    def _initialize_centroids(self, X):
        """
        Inicialización inteligente de centroides usando el método k-means++.
        
        Args:
            X (np.array): Datos de entrada (n_muestras, n_características)
            
        Returns:
            np.array: Centroides iniciales (n_clusters, n_características)
        """
        np.random.seed(self.random_state)  # Fijar semilla
        centroids = [X[np.random.randint(X.shape[0])]]  # Primer centroide aleatorio
        
        for _ in range(1, self.n_clusters):
            # Calcular distancias al cuadrado a los centroides existentes
            distances = np.min(cdist(X, np.array(centroids), 'sqeuclidean'), axis=1)
            # Convertir distancias a probabilidades de selección
            probs = distances / distances.sum()
            # Selección probabilística del siguiente centroide
            cumulative_probs = probs.cumsum()
            r = np.random.rand()
            idx = np.where(cumulative_probs >= r)[0][0]
            centroids.append(X[idx])
        
        return np.array(centroids)
    
    def fit(self, X):
        """
        Ajusta el modelo k-means a los datos mediante iteraciones EM.
        
        Args:
            X (np.array): Datos de entrada (n_muestras, n_características)
        """
        # 1. Inicialización inteligente de centroides
        self.centroids = self._initialize_centroids(X)
        
        for iteration in range(self.max_iter):
            # 2. Paso Expectation: Asignar puntos al cluster más cercano
            distances = cdist(X, self.centroids, 'euclidean')
            self.labels = np.argmin(distances, axis=1)
            
            # 3. Paso Maximization: Recalcular centroides
            new_centroids = np.array([X[self.labels == k].mean(axis=0) 
                                    for k in range(self.n_clusters)])
            
            # 4. Verificar convergencia (cambio pequeño en centroides)
            centroid_shift = np.linalg.norm(new_centroids - self.centroids)
            if centroid_shift < self.tol:
                print(f"Convergencia alcanzada en iteración {iteration}")
                break
                
            self.centroids = new_centroids
        
        # Calcular métrica de inercia (suma de distancias cuadradas)
        self.inertia_ = np.sum(np.min(cdist(X, self.centroids, 'sqeuclidean'), axis=1))
    
    def predict(self, X):
        """
        Asigna nuevos puntos a los clusters aprendidos.
        
        Args:
            X (np.array): Nuevos datos a clasificar
            
        Returns:
            np.array: Etiquetas de cluster para cada punto
        """
        distances = cdist(X, self.centroids, 'euclidean')
        return np.argmin(distances, axis=1)

class DBSCAN:
    """
    Implementación del algoritmo DBSCAN para clustering basado en densidad.
    """
    
    def __init__(self, eps=0.5, min_samples=5):
        """
        Inicializa los parámetros de DBSCAN.
        
        Args:
            eps (float): Radio de la vecindad para considerar puntos cercanos
            min_samples (int): Mínimo de puntos para formar un cluster denso
        """
        self.eps = eps  # Radio de búsqueda de vecinos
        self.min_samples = min_samples  # Puntos mínimos para ser núcleo
        self.labels = None  # Resultados del clustering
    
    def _find_neighbors(self, X, point_idx):
        """
        Encuentra todos los puntos dentro del radio eps del punto dado.
        
        Args:
            X (np.array): Todos los puntos de datos
            point_idx (int): Índice del punto central
            
        Returns:
            np.array: Índices de los puntos vecinos
        """
        distances = np.linalg.norm(X - X[point_idx], axis=1)
        return np.where(distances <= self.eps)[0]
    
    def fit(self, X):
        """
        Ejecuta el algoritmo DBSCAN en los datos de entrada.
        
        Args:
            X (np.array): Datos a clusterizar (n_muestras, n_características)
        """
        n_samples = X.shape[0]
        self.labels = np.full(n_samples, -1)  # -1 indica ruido/no asignado
        cluster_id = 0  # Contador de clusters
        
        for i in range(n_samples):
            if self.labels[i] != -1:  # Punto ya procesado
                continue
                
            # Encontrar todos los vecinos en radio eps
            neighbors = self._find_neighbors(X, i)
            
            if len(neighbors) < self.min_samples:  # Punto es ruido
                self.labels[i] = -1
                continue
                
            # Comenzar nuevo cluster
            self.labels[i] = cluster_id
            seed_set = set(neighbors) - {i}  # Puntos por expandir
            
            # Expansión del cluster
            while seed_set:
                j = seed_set.pop()
                
                if self.labels[j] == -1:  # Cambiar ruido a punto frontera
                    self.labels[j] = cluster_id
                    
                if self.labels[j] != -1:  # Punto ya pertenece a un cluster
                    continue
                    
                self.labels[j] = cluster_id
                j_neighbors = self._find_neighbors(X, j)
                
                if len(j_neighbors) >= self.min_samples:  # Punto es núcleo
                    seed_set.update(j_neighbors)  # Expandir búsqueda
            
            cluster_id += 1  # Pasar al siguiente cluster
    
    def predict(self, X):
        """
        Para nuevos datos, asigna al cluster del vecino más cercano.
        
        Args:
            X (np.array): Nuevos datos a clasificar
            
        Returns:
            np.array: Etiquetas predichas
        """
        if not hasattr(self, 'X_train'):
            self.X_train = X
            return self.labels
            
        # Encontrar vecino más cercano en datos de entrenamiento
        knn = NearestNeighbors(n_neighbors=1)
        knn.fit(self.X_train)
        distances, indices = knn.kneighbors(X)
        return self.labels[indices.flatten()]

def evaluate_clustering(X, labels, algorithm_name, centroids=None):
    """
    Visualiza los resultados del clustering con matplotlib.
    
    Args:
        X (np.array): Datos originales
        labels (np.array): Asignaciones de cluster
        algorithm_name (str): Nombre del algoritmo para el título
        centroids (np.array): Centroides (opcional, para K-Means)
    """
    plt.figure(figsize=(10, 6))
    
    # Graficar centroides si están disponibles
    if centroids is not None:
        plt.scatter(centroids[:, 0], centroids[:, 1], marker='x', 
                   s=200, linewidths=3, color='r', label='Centroides')
    
    # Graficar puntos coloreados por cluster
    scatter = plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis', 
                         s=50, alpha=0.7, label='Datos')
    
    # Configuración del gráfico
    plt.title(f'Agrupamiento con {algorithm_name}')
    plt.xlabel('Característica 1')
    plt.ylabel('Característica 2')
    plt.grid(True)
    
    # Mostrar leyenda si hay elementos especiales
    if centroids is not None or -1 in labels:
        handles, _ = scatter.legend_elements()
        if -1 in labels:  # Para DBSCAN (ruido)
            handles.append(plt.Line2D([0], [0], marker='o', color='w', 
                          markerfacecolor='gray', markersize=10, label='Ruido'))
        plt.legend(handles=handles)
    
    plt.show()

# Bloque principal de ejecución
if __name__ == "__main__":
    np.random.seed(42)  # Para reproducibilidad
    
    # Generar datos de prueba
    X_blobs, y_blobs = make_blobs(n_samples=300, centers=3, 
                                 cluster_std=0.8, random_state=42)
    X_moons, y_moons = make_moons(n_samples=300, noise=0.05, random_state=42)
    
    # Demostración de K-Means (ideal para datos esféricos)
    print("=== Ejemplo 1: K-Means en datos esféricos ===")
    kmeans = KMeans(n_clusters=3, random_state=42)
    kmeans.fit(X_blobs)
    evaluate_clustering(X_blobs, kmeans.labels, "K-Means", kmeans.centroids)
    print(f"Inercia (suma de distancias cuadradas): {kmeans.inertia_:.2f}")
    
    # K-Means en datos no esféricos (resultados subóptimos)
    print("\n=== Ejemplo 2: K-Means en datos no esféricos ===")
    kmeans_moons = KMeans(n_clusters=2, random_state=42)
    kmeans_moons.fit(X_moons)
    evaluate_clustering(X_moons, kmeans_moons.labels, 
                       "K-Means en datos no esféricos", kmeans_moons.centroids)
    
    # Demostración de DBSCAN (ideal para datos complejos)
    print("\n=== Ejemplo 3: DBSCAN en datos complejos ===")
    dbscan = DBSCAN(eps=0.2, min_samples=5)
    dbscan.fit(X_moons)
    evaluate_clustering(X_moons, dbscan.labels, "DBSCAN")
    
    # DBSCAN en datos esféricos
    print("\n=== Ejemplo 4: DBSCAN en datos esféricos ===")
    dbscan_blobs = DBSCAN(eps=0.8, min_samples=10)
    dbscan_blobs.fit(X_blobs)
    evaluate_clustering(X_blobs, dbscan_blobs.labels, "DBSCAN en datos esféricos")