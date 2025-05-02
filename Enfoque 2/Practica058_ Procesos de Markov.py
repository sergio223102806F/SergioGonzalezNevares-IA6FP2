# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 15:17:31 2025

@author: elvin
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

class ProcesoMarkov:
    """
    Clase para modelar y analizar procesos de Markov discretos en tiempo y estados.
    Implementa cadenas de Markov con estados discretos y probabilidades de transición.
    """
    
    def __init__(self, estados, matriz_transicion=None):
        """
        Inicializa el proceso de Markov.
        
        Args:
            estados (list): Lista de estados posibles del proceso.
            matriz_transicion (np.array, optional): Matriz de transición entre estados.
                            Si es None, se inicializa aleatoriamente. Default es None.
        """
        self.estados = estados
        self.n_estados = len(estados)
        self.estado_actual = None
        
        # Inicializar matriz de transición
        if matriz_transicion is not None:
            self.matriz_transicion = np.array(matriz_transicion)
            # Verificar que las filas sumen 1 (probabilidades válidas)
            if not np.allclose(self.matriz_transicion.sum(axis=1), np.ones(self.n_estados)):
                raise ValueError("Las filas de la matriz de transición deben sumar 1")
        else:
            # Crear matriz aleatoria si no se proporciona
            self.matriz_transicion = self._generar_matriz_aleatoria()
    
    def _generar_matriz_aleatoria(self):
        """Genera una matriz de transición válida aleatoria."""
        matriz = np.random.rand(self.n_estados, self.n_estados)
        # Normalizar las filas para que sumen 1
        return matriz / matriz.sum(axis=1)[:, np.newaxis]
    
    def establecer_estado(self, estado):
        """
        Establece el estado actual del proceso.
        
        Args:
            estado: Estado inicial del proceso. Debe estar en self.estados.
            
        Raises:
            ValueError: Si el estado no es válido.
        """
        if estado not in self.estados:
            raise ValueError(f"Estado {estado} no está en la lista de estados posibles")
        self.estado_actual = estado
    
    def transicion(self):
        """
        Realiza una transición de estado según las probabilidades definidas.
        
        Returns:
            El nuevo estado después de la transición.
            
        Raises:
            ValueError: Si no se ha establecido un estado actual.
        """
        if self.estado_actual is None:
            raise ValueError("No se ha establecido un estado actual")
            
        indice_actual = self.estados.index(self.estado_actual)
        # Obtener probabilidades de transición desde el estado actual
        prob_transicion = self.matriz_transicion[indice_actual]
        # Elegir nuevo estado aleatoriamente según las probabilidades
        nuevo_indice = np.random.choice(self.n_estados, p=prob_transicion)
        self.estado_actual = self.estados[nuevo_indice]
        
        return self.estado_actual
    
    def simular(self, n_pasos, estado_inicial=None):
        """
        Simula el proceso de Markov para un número dado de pasos.
        
        Args:
            n_pasos (int): Número de pasos a simular.
            estado_inicial: Estado inicial de la simulación. Si es None, se elige aleatorio.
            
        Returns:
            list: Secuencia de estados visitados.
        """
        if estado_inicial is not None:
            self.establecer_estado(estado_inicial)
        else:
            # Establecer estado inicial aleatorio si no se especifica
            self.estado_actual = np.random.choice(self.estados)
        
        secuencia = [self.estado_actual]
        for _ in range(n_pasos):
            secuencia.append(self.transicion())
            
        return secuencia
    
    def distribucion_estacionaria(self, tol=1e-6, max_iter=1000):
        """
        Calcula la distribución estacionaria del proceso de Markov.
        
        Args:
            tol (float): Tolerancia para la convergencia. Default 1e-6.
            max_iter (int): Máximo número de iteraciones. Default 1000.
            
        Returns:
            dict: Distribución estacionaria {estado: probabilidad}.
            
        Raises:
            RuntimeError: Si no converge después de max_iter iteraciones.
        """
        # Comenzar con distribución uniforme
        pi = np.ones(self.n_estados) / self.n_estados
        
        for _ in range(max_iter):
            pi_nueva = pi @ self.matriz_transicion
            # Verificar convergencia
            if np.linalg.norm(pi_nueva - pi) < tol:
                # Crear diccionario con los resultados
                return {estado: prob for estado, prob in zip(self.estados, pi_nueva)}
            pi = pi_nueva
        
        raise RuntimeError("No se alcanzó convergencia en el número máximo de iteraciones")
    
    def verificar_reversibilidad(self):
        """
        Verifica si la cadena de Markov es reversible (satisface balance detallado).
        
        Returns:
            bool: True si la cadena es reversible, False en caso contrario.
        """
        pi = self.distribucion_estacionaria()
        pi_vector = np.array([pi[estado] for estado in self.estados])
        
        # Verificar balance detallado: π_i * P_ij = π_j * P_ji para todo i,j
        for i in range(self.n_estados):
            for j in range(self.n_estados):
                if not np.isclose(
                    pi_vector[i] * self.matriz_transicion[i, j],
                    pi_vector[j] * self.matriz_transicion[j, i]
                ):
                    return False
        return True
    
    def visualizar_matriz_transicion(self):
        """Visualiza la matriz de transición como un heatmap."""
        plt.figure(figsize=(8, 6))
        plt.imshow(self.matriz_transicion, cmap='Blues')
        
        # Añadir anotaciones con los valores
        for i in range(self.n_estados):
            for j in range(self.n_estados):
                plt.text(j, i, f"{self.matriz_transicion[i, j]:.2f}",
                         ha="center", va="center", color="black")
        
        plt.xticks(np.arange(self.n_estados), self.estados)
        plt.yticks(np.arange(self.n_estados), self.estados)
        plt.title("Matriz de Transición")
        plt.colorbar(label="Probabilidad")
        plt.show()

# Ejemplo de uso
if __name__ == "__main__":
    print("=== Ejemplo de Proceso de Markov ===")
    
    # 1. Definir estados y matriz de transición
    estados = ["Soleado", "Nublado", "Lluvioso"]
    
    # Matriz de transición del clima (filas suman 1)
    matriz_trans = np.array([
        [0.7, 0.2, 0.1],  # Desde Soleado
        [0.3, 0.4, 0.3],  # Desde Nublado
        [0.2, 0.3, 0.5]   # Desde Lluvioso
    ])
    
    # 2. Crear proceso de Markov
    clima = ProcesoMarkov(estados, matriz_trans)
    
    # 3. Visualizar matriz de transición
    print("\nMatriz de transición del clima:")
    clima.visualizar_matriz_transicion()
    
    # 4. Simular el proceso
    print("\nSimulando 10 días de clima:")
    secuencia_clima = clima.simular(n_pasos=10, estado_inicial="Soleado")
    print(" -> ".join(secuencia_clima))
    
    # 5. Calcular distribución estacionaria
    print("\nCalculando distribución estacionaria:")
    dist_estacionaria = clima.distribucion_estacionaria()
    for estado, prob in dist_estacionaria.items():
        print(f"{estado}: {prob:.4f}")
    
    # 6. Verificar reversibilidad
    print("\nVerificando reversibilidad:")
    es_reversible = clima.verificar_reversibilidad()
    print(f"La cadena {'es' if es_reversible else 'no es'} reversible")
    
    # 7. Visualizar simulación más larga
    print("\nVisualizando simulación de 100 días:")
    secuencia_larga = clima.simular(100, "Soleado")
    
    plt.figure(figsize=(10, 4))
    plt.plot(secuencia_larga, marker='o', linestyle='-')
    plt.title("Simulación del Clima (100 días)")
    plt.xlabel("Día")
    plt.ylabel("Estado")
    plt.grid(True)
    plt.show()