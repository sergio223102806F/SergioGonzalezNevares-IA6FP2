# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 18:14:49 2025

@author: elvin
"""

# Importación de bibliotecas necesarias
import numpy as np  # Operaciones numéricas eficientes
import matplotlib.pyplot as plt  # Visualización gráfica
from matplotlib.gridspec import GridSpec  # Diseño de subgráficos

class SOM:
    def __init__(self, grid_size=(10, 10), input_dim=3, learning_rate=0.5, sigma=None):
        """
        Constructor de la clase SOM (Self-Organizing Map)
        
        Args:
            grid_size: Tupla (filas, columnas) que define el tamaño del mapa
            input_dim: Dimensión de los vectores de entrada
            learning_rate: Tasa de aprendizaje inicial (0-1)
            sigma: Radio inicial del vecindario (si None, se calcula automáticamente)
        """
        self.grid_size = grid_size  # Tamaño de la cuadrícula 2D
        self.input_dim = input_dim  # Dimensión de los datos de entrada
        self.learning_rate = learning_rate  # Tasa de aprendizaje inicial
        
        # Radio de influencia inicial (default: mitad del tamaño mayor del grid)
        self.sigma = sigma if sigma is not None else max(grid_size) / 2
        
        # Inicialización aleatoria de los pesos (matriz 3D: filas x columnas x dimens_entrada)
        self.weights = np.random.rand(grid_size[0], grid_size[1], input_dim)
        
        # Crear matriz de coordenadas de los nodos para cálculo de distancias
        self.node_coords = np.array([[[x, y] for y in range(grid_size[1])] 
                                     for x in range(grid_size[0])])
    
    def find_bmu(self, sample):
        """
        Encuentra la Best Matching Unit (BMU) - Neurona más cercana al sample
        
        Args:
            sample: Vector de entrada (dimensión = input_dim)
            
        Returns:
            Tupla (i,j) con las coordenadas de la BMU en el grid
        """
        # Calcula la distancia euclidiana al cuadrado entre el sample y todos los pesos
        distances = np.sum((self.weights - sample) ** 2, axis=2)
        # Encuentra el índice del valor mínimo en la matriz de distancias
        bmu_idx = np.unravel_index(np.argmin(distances), distances.shape)
        return bmu_idx
    
    def get_neighborhood(self, bmu_coords, current_sigma):
        """
        Calcula la función de vecindario gaussiana alrededor de la BMU
        
        Args:
            bmu_coords: Coordenadas (x,y) de la BMU
            current_sigma: Radio actual del vecindario
            
        Returns:
            Matriz 2D con valores de influencia (0-1) para cada neurona
        """
        # Calcula distancia euclidiana al cuadrado desde cada nodo a la BMU
        distances = np.sum((self.node_coords - bmu_coords) ** 2, axis=2)
        # Aplica función gaussiana para suavizar la influencia
        neighborhood = np.exp(-distances / (2 * current_sigma ** 2))
        return neighborhood
    
    def train(self, data, num_epochs=100):
        """
        Algoritmo de entrenamiento del SOM
        
        Args:
            data: Matriz de datos (n_samples x input_dim)
            num_epochs: Número total de iteraciones de entrenamiento
        """
        for epoch in range(num_epochs):
            # Ajuste progresivo de parámetros (decaimiento lineal)
            current_lr = self.learning_rate * (1 - epoch / num_epochs)  # Tasa de aprendizaje actual
            current_sigma = self.sigma * (1 - epoch / num_epochs)  # Radio actual
            
            # Barajar los datos en cada época para mejor aprendizaje
            np.random.shuffle(data)
            
            for sample in data:
                # 1. Encontrar la BMU para este sample
                bmu_x, bmu_y = self.find_bmu(sample)
                bmu_coords = np.array([bmu_x, bmu_y])
                
                # 2. Calcular función de vecindario gaussiana
                neighborhood = self.get_neighborhood(bmu_coords, current_sigma)
                
                # 3. Actualizar pesos: 
                # influence es una matriz 3D (para broadcasting)
                influence = neighborhood[:, :, np.newaxis]
                # Regla de actualización de Kohonen
                self.weights += current_lr * influence * (sample - self.weights)
    
    def plot_results(self, data=None, labels=None):
        """
        Visualiza los resultados del SOM
        
        Args:
            data: Datos de entrada para proyectar (opcional)
            labels: Etiquetas para visualización por color (opcional)
        """
        fig = plt.figure(figsize=(15, 6))  # Crear figura
        gs = GridSpec(1, 2, figure=fig)  # Dividir en 2 subgráficos
        
        # --- Subgráfico 1: Mapa de pesos ---
        ax1 = fig.add_subplot(gs[0, 0])
        
        if self.input_dim == 3:
            # Visualización directa para datos RGB (3 dimensiones)
            ax1.imshow(self.weights, interpolation='none')
        else:
            # Calcular U-Matrix para otras dimensiones
            umatrix = np.zeros(self.grid_size)
            for i in range(self.grid_size[0]):
                for j in range(self.grid_size[1]):
                    # Vecinos inmediatos (arriba, abajo, izquierda, derecha)
                    neighbors = []
                    if i > 0: neighbors.append(self.weights[i-1, j])
                    if i < self.grid_size[0]-1: neighbors.append(self.weights[i+1, j])
                    if j > 0: neighbors.append(self.weights[i, j-1])
                    if j < self.grid_size[1]-1: neighbors.append(self.weights[i, j+1])
                    
                    if neighbors:
                        # Distancia promedio a los vecinos
                        umatrix[i, j] = np.mean([np.linalg.norm(self.weights[i,j] - n) 
                                               for n in neighbors])
            
            # Visualizar U-Matrix (escala de grises)
            ax1.imshow(umatrix, cmap='gray_r', interpolation='none')
            plt.colorbar(ax1.imshow(umatrix, cmap='gray_r'), ax=ax1)
        
        ax1.set_title('Mapa Autoorganizado (Pesos)')
        
        # --- Subgráfico 2: Proyección de datos ---
        if data is not None:
            ax2 = fig.add_subplot(gs[0, 1])
            
            # Encontrar BMU para cada muestra
            bmu_indices = np.array([self.find_bmu(sample) for sample in data])
            
            # Visualizar con o sin etiquetas de color
            if labels is None:
                ax2.scatter(bmu_indices[:, 1], bmu_indices[:, 0], alpha=0.5)
            else:
                unique_labels = np.unique(labels)
                for label in unique_labels:
                    mask = labels == label
                    ax2.scatter(bmu_indices[mask, 1], bmu_indices[mask, 0], 
                               label=f'Clase {label}', alpha=0.7)
                ax2.legend()
            
            # Configuración del gráfico
            ax2.set_xlim([-0.5, self.grid_size[1]-0.5])
            ax2.set_ylim([-0.5, self.grid_size[0]-0.5])
            ax2.invert_yaxis()  # Para que (0,0) esté arriba a la izquierda
            ax2.set_title('Proyección de Datos en el SOM')
            ax2.set_aspect('equal')  # Misma escala en ambos ejes
        
        plt.tight_layout()
        plt.show()


# --- Ejemplo de uso con datos RGB ---
if __name__ == "__main__":
    print("Ejemplo 1: Entrenando SOM con colores RGB aleatorios")
    
    # 1. Generar 100 colores RGB aleatorios
    np.random.seed(42)  # Para reproducibilidad
    colors = np.random.rand(100, 3)  # Matriz 100x3
    
    # 2. Crear y entrenar SOM
    som = SOM(grid_size=(15, 15), input_dim=3, learning_rate=0.5)
    print("Entrenamiento en progreso...")
    som.train(colors, num_epochs=100)
    
    # 3. Visualizar mapa de pesos (organización automática de colores)
    som.plot_results(colors)
    
    # --- Ejemplo con datos etiquetados ---
    print("\nEjemplo 2: SOM con datos de clustering")
    from sklearn.datasets import make_blobs
    
    # Generar datos sintéticos (4 clusters)
    X, y = make_blobs(n_samples=200, centers=4, random_state=42)
    
    # Normalizar datos al rango [0,1]
    X = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
    
    # Crear y entrenar SOM 2D
    som2 = SOM(grid_size=(10, 10), input_dim=2, learning_rate=0.5)
    som2.train(X, num_epochs=50)
    
    # Visualizar proyección de los datos manteniendo las etiquetas
    som2.plot_results(X, y)