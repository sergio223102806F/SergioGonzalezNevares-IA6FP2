# -*- coding: utf-8 -*-
"""
Implementación de un Filtro de Kalman para estimación de estados
Creado el Sábado 26 de Abril 2025
Autor: elvin
"""

# Importación de numpy para operaciones matriciales
import numpy as np

# Importación de matplotlib para visualización
import matplotlib.pyplot as plt

class FiltroKalman:
    """
    Implementación completa de un Filtro de Kalman para sistemas lineales
    
    Atributos:
        A: Matriz de transición del estado
        B: Matriz de control (opcional)
        H: Matriz de observación
        Q: Matriz de covarianza del ruido del proceso  
        R: Matriz de covarianza del ruido de medición
        x: Vector de estado actual
        P: Matriz de covarianza del estado actual
        n: Dimensión del estado
        k: Dimensión de la observación
    """
    
    def __init__(self, A, H, Q, R, B=None, x0=None, P0=None):
        """
        Inicializa el filtro de Kalman con las matrices del modelo
        
        Args:
            A (np.array): Matriz de transición del estado (n x n)
            H (np.array): Matriz de observación (k x n)
            Q (np.array): Matriz de covarianza del ruido del proceso (n x n)
            R (np.array): Matriz de covarianza del ruido de medición (k x k)
            B (np.array): Matriz de control opcional (n x m)
            x0 (np.array): Estado inicial (n x 1)
            P0 (np.array): Covarianza inicial del estado (n x n)
        """
        # Asignación de matrices del modelo
        self.A = A  # Matriz de dinámica del sistema
        self.B = B  # Matriz de control (opcional)
        self.H = H  # Matriz de modelo de observación
        self.Q = Q  # Matriz de covarianza del ruido del proceso
        self.R = R  # Matriz de covarianza del ruido de medición
        
        # Dimensiones del sistema
        self.n = A.shape[0]  # Dimensión del vector de estado
        self.k = H.shape[0]  # Dimensión del vector de observación
        
        # Inicialización del estado
        self.x = x0 if x0 is not None else np.zeros((self.n, 1))  # Estado inicial
        self.P = P0 if P0 is not None else np.eye(self.n)  # Covarianza inicial
        
        # Historial para registro y visualización
        self.historial_estados = []  # Almacena todos los estados estimados
        self.historial_covarianzas = []  # Almacena todas las covarianzas
        self.historial_observaciones = []  # Almacena todas las observaciones
    
    def predecir(self, u=None):
        """
        Realiza la etapa de predicción del filtro de Kalman
        
        Args:
            u (np.array): Vector de control opcional
            
        Returns:
            tuple: (x_predicho, P_predicho)
        """
        # Predicción del estado usando el modelo dinámico
        self.x = self.A @ self.x
        # Si hay matriz de control y entrada, aplicarla
        if self.B is not None and u is not None:
            self.x += self.B @ u
        
        # Predicción de la covarianza del estado
        self.P = self.A @ self.P @ self.A.T + self.Q
        
        # Guardar en el historial
        self.historial_estados.append(self.x.copy())
        self.historial_covarianzas.append(self.P.copy())
        
        return self.x, self.P
    
    def actualizar(self, z):
        """
        Realiza la etapa de actualización del filtro con una nueva observación
        
        Args:
            z (np.array): Vector de observación
            
        Returns:
            tuple: (x_actualizado, P_actualizado)
        """
        # Registrar la nueva observación
        self.historial_observaciones.append(z.copy())
        
        # Calcular la innovación (error entre observación y predicción)
        y = z - self.H @ self.x
        
        # Calcular la covarianza de la innovación
        S = self.H @ self.P @ self.H.T + self.R
        
        # Calcular la ganancia óptima de Kalman
        K = self.P @ self.H.T @ np.linalg.inv(S)
        
        # Actualizar la estimación del estado
        self.x = self.x + K @ y
        
        # Actualizar la covarianza del estado
        I = np.eye(self.n)
        self.P = (I - K @ self.H) @ self.P
        
        # Guardar en el historial
        self.historial_estados.append(self.x.copy())
        self.historial_covarianzas.append(self.P.copy())
        
        return self.x, self.P
    
    def filtrar(self, observaciones, entradas=None):
        """
        Ejecuta el filtro completo para una secuencia de observaciones
        
        Args:
            observaciones (list): Lista de vectores de observación
            entradas (list): Lista opcional de vectores de control
            
        Returns:
            list: Lista de tuplas (estado, covarianza) en cada paso
        """
        resultados = []
        for t, z in enumerate(observaciones):
            # Obtener entrada de control si existe
            u = entradas[t] if entradas is not None else None
            # Etapa de predicción
            self.predecir(u)
            # Etapa de actualización
            self.actualizar(z)
            # Guardar resultados
            resultados.append((self.x.copy(), self.P.copy()))
        return resultados
    
    def graficar_resultados(self, estados_reales=None):
        """
        Visualiza los resultados del filtrado comparando con valores reales
        
        Args:
            estados_reales (list): Lista opcional de estados reales para comparación
        """
        plt.figure(figsize=(12, 6))  # Crear figura
        
        # Convertir historial de estados a array numpy
        estados_estimados = np.array([x.flatten() for x in self.historial_estados])
        
        # Graficar cada componente del estado por separado
        for i in range(self.n):
            plt.subplot(self.n, 1, i+1)  # Crear subplot para cada componente
            
            # Graficar estimaciones del filtro
            plt.plot(estados_estimados[:, i], 'b-', label='Estimación Kalman')
            
            # Graficar observaciones si están disponibles para esta componente
            if i < self.k and len(self.historial_observaciones) > 0:
                obs = np.array([z.flatten() for z in self.historial_observaciones])
                plt.plot(obs[:, i], 'ro', markersize=4, label='Observaciones')
            
            # Graficar estados reales si se proporcionan
            if estados_reales is not None:
                reales = np.array([x.flatten() for x in estados_reales])
                plt.plot(reales[:, i], 'g--', label='Estado real')
            
            plt.ylabel(f'Componente {i+1}')  # Etiqueta del eje Y
            plt.legend()  # Mostrar leyenda
            plt.grid(True)  # Activar cuadrícula
        
        plt.xlabel('Tiempo')  # Etiqueta común del eje X
        plt.tight_layout()  # Ajustar layout
        plt.show()  # Mostrar gráfico

# Bloque principal de ejecución (ejemplo de seguimiento de posición)
if __name__ == "__main__":
    # 1. Configuración de parámetros del sistema
    dt = 0.1  # Intervalo de tiempo entre mediciones
    sigma_proceso = 0.1  # Desviación estándar del ruido del proceso
    sigma_medicion = 0.5  # Desviación estándar del ruido de medición
    
    # 2. Definición de matrices del modelo
    
    # Matriz de transición (modelo de velocidad constante)
    A = np.array([
        [1, dt],  # Ecuación de posición: x = x_prev + v*dt
        [0,  1]   # Ecuación de velocidad: v = v_prev (constante)
    ])
    
    # Matriz de observación (solo observamos la posición)
    H = np.array([[1, 0]])
    
    # Matriz de covarianza del ruido del proceso
    Q = np.array([
        [dt**4/4, dt**3/2],  # Covarianza para modelo de aceleración constante
        [dt**3/2, dt**2]
    ]) * sigma_proceso**2  # Escalar por varianza del ruido
    
    # Matriz de covarianza del ruido de medición
    R = np.array([[sigma_medicion**2]])  # Varianza de la medición
    
    # 3. Creación del filtro de Kalman
    x0 = np.array([[0], [1]])  # Estado inicial: posición 0, velocidad 1
    P0 = np.eye(2) * 10  # Covarianza inicial (alta incertidumbre)
    
    filtro = FiltroKalman(A, H, Q, R, x0=x0, P0=P0)
    
    # 4. Generación de datos de simulación
    n_pasos = 50  # Número de pasos de tiempo
    estados_reales = []  # Almacenará los estados reales
    observaciones = []  # Almacenará las observaciones con ruido
    
    # Estado real inicial
    x_real = x0.copy()
    
    for _ in range(n_pasos):
        # Simular evolución del estado real (con ruido del proceso)
        x_real = A @ x_real + np.random.multivariate_normal(
            mean=np.zeros(2), 
            cov=Q
        ).reshape(-1, 1)
        
        # Simular observación con ruido
        z = H @ x_real + np.random.normal(0, sigma_medicion, size=(1, 1))
        
        # Guardar estados y observaciones
        estados_reales.append(x_real.copy())
        observaciones.append(z.copy())
    
    # 5. Ejecución del filtro de Kalman
    filtro.filtrar(observaciones)
    
    # 6. Mostrar resultados
    print("\nResultados del filtrado:")
    print(f"Estado final estimado:\n{filtro.x}")
    print(f"\nCovarianza final:\n{filtro.P}")
    
    # 7. Visualización gráfica
    filtro.graficar_resultados(estados_reales)