# -*- coding: utf-8 -*-
"""
Script para implementar y analizar cadenas de Markov discretas
Creado el Sábado 26 de Abril 2025
Autor: elvin
"""

# Importación de numpy para operaciones numéricas
import numpy as np

# Importación de matplotlib para visualización
import matplotlib.pyplot as plt

# Importación de defaultdict para diccionarios con valores por defecto
from collections import defaultdict

class ProcesoMarkov:
    """
    Clase para modelar y analizar procesos de Markov discretos
    
    Atributos:
        estados: Lista de estados posibles
        n_estados: Número de estados
        estado_actual: Estado actual del proceso
        matriz_transicion: Matriz de probabilidades de transición
    """
    
    def __init__(self, estados, matriz_transicion=None):
        """
        Inicializa el proceso de Markov con estados y matriz de transición
        
        Args:
            estados (list): Lista de nombres/identificadores de estados
            matriz_transicion (np.array): Matriz cuadrada de transición (opcional)
            
        Raises:
            ValueError: Si la matriz de transición no es válida
        """
        self.estados = estados  # Almacena los estados posibles
        self.n_estados = len(estados)  # Calcula número de estados
        self.estado_actual = None  # Inicialmente sin estado definido
        
        # Configuración de la matriz de transición
        if matriz_transicion is not None:
            # Convierte a array numpy si se proporciona
            self.matriz_transicion = np.array(matriz_transicion)
            # Verifica que cada fila sume 1 (probabilidades válidas)
            if not np.allclose(self.matriz_transicion.sum(axis=1), np.ones(self.n_estados)):
                raise ValueError("Las filas de la matriz de transición deben sumar 1")
        else:
            # Genera matriz aleatoria si no se proporciona
            self.matriz_transicion = self._generar_matriz_aleatoria()
    
    def _generar_matriz_aleatoria(self):
        """
        Genera una matriz de transición aleatoria válida
        
        Returns:
            np.array: Matriz de n_estados x n_estados con filas que suman 1
        """
        # Genera valores aleatorios entre 0 y 1
        matriz = np.random.rand(self.n_estados, self.n_estados)
        # Normaliza las filas para que sumen 1
        return matriz / matriz.sum(axis=1)[:, np.newaxis]
    
    def establecer_estado(self, estado):
        """
        Establece el estado actual del proceso
        
        Args:
            estado: Estado a establecer (debe estar en self.estados)
            
        Raises:
            ValueError: Si el estado no existe
        """
        if estado not in self.estados:
            raise ValueError(f"Estado {estado} no está en la lista de estados posibles")
        self.estado_actual = estado  # Actualiza el estado actual
    
    def transicion(self):
        """
        Realiza una transición de estado según las probabilidades definidas
        
        Returns:
            Nuevo estado después de la transición
            
        Raises:
            ValueError: Si no hay estado actual definido
        """
        if self.estado_actual is None:
            raise ValueError("No se ha establecido un estado actual")
            
        # Obtiene el índice del estado actual
        indice_actual = self.estados.index(self.estado_actual)
        # Probabilidades de transición desde el estado actual
        prob_transicion = self.matriz_transicion[indice_actual]
        # Selecciona nuevo estado aleatoriamente según probabilidades
        nuevo_indice = np.random.choice(self.n_estados, p=prob_transicion)
        # Actualiza y retorna el nuevo estado
        self.estado_actual = self.estados[nuevo_indice]
        return self.estado_actual
    
    def simular(self, n_pasos, estado_inicial=None):
        """
        Simula el proceso para un número determinado de pasos
        
        Args:
            n_pasos (int): Número de transiciones a simular
            estado_inicial: Estado inicial (opcional, aleatorio si es None)
            
        Returns:
            list: Secuencia de estados visitados
        """
        # Configura estado inicial
        if estado_inicial is not None:
            self.establecer_estado(estado_inicial)
        else:
            # Elige estado inicial aleatorio si no se especifica
            self.estado_actual = np.random.choice(self.estados)
        
        # Inicia la secuencia con el estado actual
        secuencia = [self.estado_actual]
        # Realiza n_pasos transiciones
        for _ in range(n_pasos):
            secuencia.append(self.transicion())
            
        return secuencia
    
    def distribucion_estacionaria(self, tol=1e-6, max_iter=1000):
        """
        Calcula la distribución estacionaria por iteración de la matriz
        
        Args:
            tol (float): Tolerancia para convergencia (default 1e-6)
            max_iter (int): Máximo de iteraciones (default 1000)
            
        Returns:
            dict: Distribución {estado: probabilidad}
            
        Raises:
            RuntimeError: Si no converge en max_iter iteraciones
        """
        # Inicia con distribución uniforme
        pi = np.ones(self.n_estados) / self.n_estados
        
        # Algoritmo iterativo
        for _ in range(max_iter):
            pi_nueva = pi @ self.matriz_transicion  # Multiplicación de matrices
            # Verifica convergencia
            if np.linalg.norm(pi_nueva - pi) < tol:
                # Formatea resultado como diccionario
                return {estado: prob for estado, prob in zip(self.estados, pi_nueva)}
            pi = pi_nueva  # Actualiza para siguiente iteración
        
        raise RuntimeError("No se alcanzó convergencia en el número máximo de iteraciones")
    
    def verificar_reversibilidad(self):
        """
        Verifica si la cadena satisface balance detallado (reversibilidad)
        
        Returns:
            bool: True si es reversible, False si no
        """
        # Obtiene distribución estacionaria
        pi = self.distribucion_estacionaria()
        # Convierte a vector numpy
        pi_vector = np.array([pi[estado] for estado in self.estados])
        
        # Verifica balance detallado para cada par de estados
        for i in range(self.n_estados):
            for j in range(self.n_estados):
                if not np.isclose(
                    pi_vector[i] * self.matriz_transicion[i, j],
                    pi_vector[j] * self.matriz_transicion[j, i]
                ):
                    return False  # No es reversible
        return True  # Es reversible
    
    def visualizar_matriz_transicion(self):
        """Visualiza la matriz de transición como heatmap con anotaciones"""
        plt.figure(figsize=(8, 6))  # Tamaño de figura
        # Muestra matriz como imagen
        plt.imshow(self.matriz_transicion, cmap='Blues')  # Mapa de color azul
        
        # Añade valores numéricos a cada celda
        for i in range(self.n_estados):
            for j in range(self.n_estados):
                plt.text(j, i, f"{self.matriz_transicion[i, j]:.2f}",
                         ha="center", va="center", color="black")
        
        # Configura ejes
        plt.xticks(np.arange(self.n_estados), self.estados)
        plt.yticks(np.arange(self.n_estados), self.estados)
        plt.title("Matriz de Transición")  # Título
        plt.colorbar(label="Probabilidad")  # Barra de color
        plt.show()  # Muestra gráfico

# Bloque principal de ejecución (ejemplo de uso)
if __name__ == "__main__":
    print("=== Ejemplo de Proceso de Markov ===")
    
    # 1. Definición del sistema climático
    estados = ["Soleado", "Nublado", "Lluvioso"]
    
    # Matriz de transición (filas suman 1)
    matriz_trans = np.array([
        [0.7, 0.2, 0.1],  # Transiciones desde Soleado
        [0.3, 0.4, 0.3],  # Transiciones desde Nublado
        [0.2, 0.3, 0.5]   # Transiciones desde Lluvioso
    ])
    
    # 2. Creación del modelo
    clima = ProcesoMarkov(estados, matriz_trans)
    
    # 3. Visualización de la matriz de transición
    print("\nMatriz de transición del clima:")
    clima.visualizar_matriz_transicion()
    
    # 4. Simulación a corto plazo
    print("\nSimulando 10 días de clima:")
    secuencia_clima = clima.simular(n_pasos=10, estado_inicial="Soleado")
    print(" -> ".join(secuencia_clima))
    
    # 5. Cálculo de distribución estacionaria
    print("\nCalculando distribución estacionaria:")
    dist_estacionaria = clima.distribucion_estacionaria()
    for estado, prob in dist_estacionaria.items():
        print(f"{estado}: {prob:.4f}")  # Probabilidad a 4 decimales
    
    # 6. Verificación de reversibilidad
    print("\nVerificando reversibilidad:")
    es_reversible = clima.verificar_reversibilidad()
    print(f"La cadena {'es' if es_reversible else 'no es'} reversible")
    
    # 7. Visualización de simulación extendida
    print("\nVisualizando simulación de 100 días:")
    secuencia_larga = clima.simular(100, "Soleado")
    
    # Configuración del gráfico de la simulación
    plt.figure(figsize=(10, 4))
    plt.plot(secuencia_larga, marker='o', linestyle='-')  # Línea con marcadores
    plt.title("Simulación del Clima (100 días)")  # Título
    plt.xlabel("Día")  # Etiqueta eje X
    plt.ylabel("Estado")  # Etiqueta eje Y
    plt.grid(True)  # Activar cuadrícula
    plt.show()  # Mostrar gráfico