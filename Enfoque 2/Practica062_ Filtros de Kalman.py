# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 15:30:27 2025

@author: elvin
"""

import numpy as np
import matplotlib.pyplot as plt

class FiltroKalman:
    """
    Implementación de un Filtro de Kalman para sistemas lineales.
    
    Args:
        A (np.array): Matriz de transición del estado (n x n)
        B (np.array): Matriz de control (opcional) (n x m)
        H (np.array): Matriz de observación (k x n)
        Q (np.array): Matriz de covarianza del ruido del proceso (n x n)
        R (np.array): Matriz de covarianza del ruido de medición (k x k)
        x0 (np.array): Estado inicial (n x 1)
        P0 (np.array): Covarianza inicial del estado (n x n)
    """
    
    def __init__(self, A, H, Q, R, B=None, x0=None, P0=None):
        # Asignar matrices del modelo
        self.A = A  # Dinámica del sistema
        self.B = B  # Entradas de control (opcional)
        self.H = H  # Modelo de observación
        self.Q = Q  # Ruido del proceso
        self.R = R  # Ruido de medición
        
        # Dimensiones
        self.n = A.shape[0]  # Dimensión del estado
        self.k = H.shape[0]  # Dimensión de la observación
        
        # Estado inicial
        self.x = x0 if x0 is not None else np.zeros((self.n, 1))
        self.P = P0 if P0 is not None else np.eye(self.n)  # Incertidumbre inicial
        
        # Historial para trazado
        self.historial_estados = []
        self.historial_covarianzas = []
        self.historial_observaciones = []
    
    def predecir(self, u=None):
        """
        Predicción del siguiente estado usando el modelo del sistema.
        
        Args:
            u (np.array): Vector de control (opcional)
        """
        # Predicción del estado
        self.x = self.A @ self.x
        if self.B is not None and u is not None:
            self.x += self.B @ u
        
        # Predicción de la covarianza
        self.P = self.A @ self.P @ self.A.T + self.Q
        
        # Guardar historial
        self.historial_estados.append(self.x.copy())
        self.historial_covarianzas.append(self.P.copy())
        
        return self.x, self.P
    
    def actualizar(self, z):
        """
        Actualización del estado estimado usando una nueva observación.
        
        Args:
            z (np.array): Vector de observación
        """
        # Guardar observación
        self.historial_observaciones.append(z.copy())
        
        # Innovación (diferencia entre observación real y predicha)
        y = z - self.H @ self.x
        
        # Covarianza de la innovación
        S = self.H @ self.P @ self.H.T + self.R
        
        # Ganancia de Kalman (cuánto confiar en la nueva observación)
        K = self.P @ self.H.T @ np.linalg.inv(S)
        
        # Actualización del estado estimado
        self.x = self.x + K @ y
        
        # Actualización de la covarianza del estado
        I = np.eye(self.n)
        self.P = (I - K @ self.H) @ self.P
        
        # Guardar historial
        self.historial_estados.append(self.x.copy())
        self.historial_covarianzas.append(self.P.copy())
        
        return self.x, self.P
    
    def filtrar(self, observaciones, entradas=None):
        """
        Ejecuta el filtro completo para una secuencia de observaciones.
        
        Args:
            observaciones (list): Secuencia de vectores de observación
            entradas (list): Secuencia de vectores de control (opcional)
        """
        resultados = []
        for t, z in enumerate(observaciones):
            u = entradas[t] if entradas is not None else None
            self.predecir(u)
            self.actualizar(z)
            resultados.append((self.x.copy(), self.P.copy()))
        return resultados
    
    def graficar_resultados(self, estados_reales=None):
        """Visualiza los resultados del filtrado."""
        plt.figure(figsize=(12, 6))
        
        # Extraer estados estimados del historial
        estados_estimados = np.array([x.flatten() for x in self.historial_estados])
        
        # Graficar cada componente del estado
        for i in range(self.n):
            plt.subplot(self.n, 1, i+1)
            
            # Graficar estimaciones (predicciones + actualizaciones)
            plt.plot(estados_estimados[:, i], 'b-', label='Estimación Kalman')
            
            # Graficar observaciones (si aplica)
            if i < self.k and len(self.historial_observaciones) > 0:
                obs = np.array([z.flatten() for z in self.historial_observaciones])
                plt.plot(obs[:, i], 'ro', markersize=4, label='Observaciones')
            
            # Graficar estado real si está disponible
            if estados_reales is not None:
                reales = np.array([x.flatten() for x in estados_reales])
                plt.plot(reales[:, i], 'g--', label='Estado real')
            
            plt.ylabel(f'Componente {i+1}')
            plt.legend()
            plt.grid(True)
        
        plt.xlabel('Tiempo')
        plt.tight_layout()
        plt.show()

# Ejemplo de uso: Seguimiento de posición y velocidad
if __name__ == "__main__":
    # Parámetros del sistema
    dt = 0.1  # Paso de tiempo
    sigma_proceso = 0.1  # Ruido del proceso
    sigma_medicion = 0.5  # Ruido de medición
    
    # 1. Definir matrices del modelo
    
    # Matriz de transición (modelo de velocidad constante)
    A = np.array([
        [1, dt],  # Posición = posición anterior + velocidad*dt
        [0,  1]   # Velocidad se mantiene constante
    ])
    
    # Matriz de observación (solo observamos la posición)
    H = np.array([[1, 0]])
    
    # Matriz de covarianza del ruido del proceso
    Q = np.array([
        [dt**4/4, dt**3/2],
        [dt**3/2, dt**2]
    ]) * sigma_proceso**2
    
    # Covarianza del ruido de medición
    R = np.array([[sigma_medicion**2]])
    
    # 2. Crear filtro de Kalman
    x0 = np.array([[0], [1]])  # Posición 0, velocidad 1
    P0 = np.eye(2) * 10  # Alta incertidumbre inicial
    
    filtro = FiltroKalman(A, H, Q, R, x0=x0, P0=P0)
    
    # 3. Generar datos de simulación
    n_pasos = 50
    estados_reales = []
    observaciones = []
    
    # Estado real inicial
    x_real = x0.copy()
    
    for _ in range(n_pasos):
        # Evolución del estado real (con ruido del proceso)
        x_real = A @ x_real + np.random.multivariate_normal(
            mean=np.zeros(2), 
            cov=Q
        ).reshape(-1, 1)
        
        # Observación (con ruido de medición)
        z = H @ x_real + np.random.normal(0, sigma_medicion, size=(1, 1))
        
        estados_reales.append(x_real.copy())
        observaciones.append(z.copy())
    
    # 4. Ejecutar filtro de Kalman
    filtro.filtrar(observaciones)
    
    # 5. Visualizar resultados
    print("\nResultados del filtrado:")
    print(f"Estado final estimado:\n{filtro.x}")
    print(f"\nCovarianza final:\n{filtro.P}")
    
    filtro.graficar_resultados(estados_reales)