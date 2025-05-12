# -*- coding: utf-8 -*-  # Define la codificación del archivo (UTF-8)
"""
Created on Sat Apr 26 16:31:14 2025

@author: elvin
"""  # Comentario de encabezado del script

# Importación de módulos necesarios
import numpy as np  # Importa NumPy para operaciones numéricas
from sklearn.neighbors import NearestNeighbors  # Importa el algoritmo de vecinos más cercanos para predicciones
import matplotlib.pyplot as plt  # Importa Matplotlib para visualizar resultados
from sklearn.datasets import make_blobs, make_moons  # Importa generadores de conjuntos de datos artificiales
from scipy.spatial.distance import cdist  # Importa función para calcular distancias entre puntos

# Definición de la clase KMeans
class KMeans:
    """
    Implementación completa del algoritmo K-Means para agrupamiento.
    """
    
    def __init__(self, n_clusters=3, max_iter=100, tol=1e-4, random_state=None):
        """
        Inicializa los parámetros del algoritmo K-Means.
        """
        self.n_clusters = n_clusters  # Número de clusters a encontrar
        self.max_iter = max_iter  # Número máximo de iteraciones permitidas
        self.tol = tol  # Tolerancia para determinar convergencia
        self.random_state = random_state  # Semilla para reproducibilidad
        self.centroids = None  # Variable para almacenar los centroides calculados
        self.labels = None  # Etiquetas asignadas a cada punto
        self.inertia_ = None  # Suma de las distancias cuadradas mínimas (métrica de rendimiento)
    
    def _initialize_centroids(self, X):
        """
        Inicializa los centroides utilizando el método K-Means++.
        """
        np.random.seed(self.random_state)  # Fija la semilla aleatoria
        centroids = [X[np.random.randint(X.shape[0])]]  # Selecciona el primer centroide aleatoriamente

        for _ in range(1, self.n_clusters):  # Itera para seleccionar el resto de los centroides
            distances = np.min(cdist(X, np.array(centroids), 'sqeuclidean'), axis=1)  # Calcula la distancia al centroide más cercano
            probs = distances / distances.sum()  # Calcula la probabilidad proporcional a la distancia
            cumulative_probs = probs.cumsum()  # Suma acumulativa de probabilidades
            r = np.random.rand()  # Genera un número aleatorio entre 0 y 1
            idx = np.where(cumulative_probs >= r)[0][0]  # Encuentra el índice del nuevo centroide
            centroids.append(X[idx])  # Agrega el nuevo centroide a la lista

        return np.array(centroids)  # Devuelve los centroides inicializados como arreglo NumPy

    def fit(self, X):
        """
        Ejecuta el algoritmo K-Means sobre los datos X.
        """
        self.centroids = self._initialize_centroids(X)  # Inicializa los centroides

        for iteration in range(self.max_iter):  # Itera hasta alcanzar el número máximo de iteraciones
            distances = cdist(X, self.centroids, 'euclidean')  # Calcula distancias de cada punto a los centroides
            self.labels = np.argmin(distances, axis=1)  # Asigna cada punto al centroide más cercano

            new_centroids = np.array([X[self.labels == k].mean(axis=0) for k in range(self.n_clusters)])  # Recalcula los centroides

            centroid_shift = np.linalg.norm(new_centroids - self.centroids)  # Calcula el desplazamiento de los centroides

            if centroid_shift < self.tol:  # Verifica si el desplazamiento es menor a la tolerancia
                print(f"Convergencia alcanzada en iteración {iteration}")  # Imprime mensaje de convergencia
                break  # Termina el ciclo si hay convergencia

            self.centroids = new_centroids  # Actualiza los centroides con los nuevos valores

        self.inertia_ = np.sum(np.min(cdist(X, self.centroids, 'sqeuclidean'), axis=1))  # Calcula la inercia final

    def predict(self, X):
        """
        Asigna cada nuevo punto de X a su cluster más cercano.
        """
        distances = cdist(X, self.centroids, 'euclidean')  # Calcula distancias a los centroides
        return np.argmin(distances, axis=1)  # Devuelve el índice del centroide más cercano

# Definición de la clase DBSCAN
class DBSCAN:
    """
    Implementación del algoritmo DBSCAN desde cero.
    """
    
    def __init__(self, eps=0.5, min_samples=5):
        """
        Inicializa los parámetros de DBSCAN.
        """
        self.eps = eps  # Radio máximo para considerar vecinos
        self.min_samples = min_samples  # Mínimo de puntos para formar un núcleo
        self.labels = None  # Etiquetas asignadas a cada punto

    def _find_neighbors(self, X, point_idx):
        """
        Encuentra los vecinos dentro del radio eps del punto dado.
        """
        distances = np.linalg.norm(X - X[point_idx], axis=1)  # Calcula distancias euclidianas
        return np.where(distances <= self.eps)[0]  # Retorna índices de los vecinos dentro del radio

    def fit(self, X):
        """
        Ejecuta el algoritmo DBSCAN sobre los datos X.
        """
        n_samples = X.shape[0]  # Obtiene el número de muestras
        self.labels = np.full(n_samples, -1)  # Inicializa todas las etiquetas como ruido (-1)
        cluster_id = 0  # Inicializa el ID del primer cluster

        for i in range(n_samples):  # Itera sobre cada punto
            if self.labels[i] != -1:  # Si ya fue etiquetado, lo salta
                continue

            neighbors = self._find_neighbors(X, i)  # Encuentra vecinos del punto i

            if len(neighbors) < self.min_samples:  # Si no es un punto núcleo
                self.labels[i] = -1  # Se considera ruido
                continue

            self.labels[i] = cluster_id  # Asigna el cluster actual al punto
            seed_set = set(neighbors) - {i}  # Conjunto de puntos para expandir el cluster

            while seed_set:  # Mientras haya puntos por expandir
                j = seed_set.pop()  # Extrae un punto del conjunto

                if self.labels[j] == -1:
                    self.labels[j] = cluster_id  # Cambia de ruido a frontera

                if self.labels[j] != -1:
                    continue  # Ya fue etiquetado

                self.labels[j] = cluster_id  # Asigna el punto al cluster
                j_neighbors = self._find_neighbors(X, j)  # Busca vecinos del nuevo punto

                if len(j_neighbors) >= self.min_samples:
                    seed_set.update(j_neighbors)  # Agrega nuevos vecinos al conjunto

            cluster_id += 1  # Aumenta el ID del cluster

    def predict(self, X):
        """
        Predice etiquetas para nuevos puntos según su vecino más cercano del entrenamiento.
        """
        if not hasattr(self, 'X_train'):  # Si no se ha guardado X
            self.X_train = X  # Almacena los datos de entrenamiento
            return self.labels  # Devuelve las etiquetas actuales

        knn = NearestNeighbors(n_neighbors=1)  # Inicializa búsqueda de 1 vecino más cercano
        knn.fit(self.X_train)  # Ajusta con los datos de entrenamiento
        distances, indices = knn.kneighbors(X)  # Encuentra el vecino más cercano para cada punto
        return self.labels[indices.flatten()]  # Devuelve etiquetas de los vecinos más cercanos

# Función para visualizar los resultados de clustering
def evaluate_clustering(X, labels, algorithm_name, centroids=None):
    """
    Visualiza el resultado del clustering con etiquetas de color.
    """
    plt.figure(figsize=(10, 6))  # Crea una nueva figura con tamaño 10x6

    if centroids is not None:  # Si se proporcionaron centroides
        plt.scatter(centroids[:, 0], centroids[:, 1], marker='x', 
                   s=200, linewidths=3, color='r', label='Centroides')  # Dibuja los centroides

    scatter = plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis', 
                         s=50, alpha=0.7, label='Datos')  # Dibuja los puntos con colores por cluster

    plt.title(f'Agrupamiento con {algorithm_name}')  # Título del gráfico
    plt.xlabel('Característica 1')  # Etiqueta eje X
    plt.ylabel('Característica 2')  # Etiqueta eje Y
    plt.grid(True)  # Muestra la rejilla

    if centroids is not None or -1 in labels:  # Si hay centroides o puntos de ruido
        handles, _ = scatter.legend_elements()  # Obtiene los elementos para la leyenda
        if -1 in labels:  # Si hay puntos de ruido
            handles.append(plt.Line2D([0], [0], marker='o', color='w', 
                          markerfacecolor='gray', markersize=10, label='Ruido'))  # Añade ícono de ruido
        plt.legend(handles=handles)  # Muestra la leyenda

    plt.show()  # Muestra el gráfico

# Bloque principal de ejecución
if __name__ == "__main__":  # Se ejecuta solo si este archivo es el principal
    np.random.seed(42)  # Fija la semilla para resultados reproducibles

    # Genera datos artificiales con estructura esférica
    X_blobs, y_blobs = make_blobs(n_samples=300, centers=3, 
                                 cluster_std=0.8, random_state=42)

    # Genera datos artificiales con forma de lunas
    X_moons, y_moons = make_moons(n_samples=300, noise=0.05, random_state=42)

    # Prueba 1: K-Means sobre datos esféricos
    print("=== Ejemplo 1: K-Means en datos esféricos ===")  # Imprime título del ejemplo
    kmeans = KMeans(n_clusters=3, random_state=42)  # Instancia KMeans
    kmeans.fit(X_blobs)  # Ajusta el modelo a los datos
    evaluate_clustering(X_blobs, kmeans.labels, "K-Means", kmeans.centroids)  # Visualiza resultado
    print(f"Inercia (suma de distancias cuadradas): {kmeans.inertia_:.2f}")  # Muestra la inercia

    # Prueba 2: K-Means sobre datos no esféricos
    print("\n=== Ejemplo 2: K-Means en datos no esféricos ===")  # Título
    kmeans_moons = KMeans(n_clusters=2, random_state=42)  # Instancia KMeans con 2 clusters
    kmeans_moons.fit(X_moons)  # Ajusta a datos lunares
    evaluate_clustering(X_moons, kmeans_moons.labels, 
                       "K-Means en datos no esféricos", kmeans_moons.centroids)  # Visualiza

    # Prueba 3: DBSCAN sobre datos no esféricos
    print("\n=== Ejemplo 3: DBSCAN en datos complejos ===")  # Título
    dbscan = DBSCAN(eps=0.2, min_samples=5)  # Instancia DBSCAN
    dbscan.fit(X_moons)  # Ajusta a datos lunares
    evaluate_clustering(X_moons, dbscan.labels, "DBSCAN")  # Visualiza

    # Prueba 4: DBSCAN sobre datos esféricos
    print("\n=== Ejemplo 4: DBSCAN en datos esféricos ===")  # Título
    dbscan_blobs = DBSCAN(eps=0.8, min_samples=10)  # Instancia DBSCAN con parámetros diferentes
    dbscan_blobs.fit(X_blobs)  # Ajusta a blobs
    evaluate_clustering(X_blobs, dbscan_blobs.labels, "DBSCAN en datos esféricos")  # Visualiza
