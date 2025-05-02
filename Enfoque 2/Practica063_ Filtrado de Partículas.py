# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 15:30:28 2025

@author: elvin
"""

# Importación de bibliotecas necesarias
import numpy as np  # Para operaciones numéricas y matrices
import matplotlib.pyplot as plt  # Para visualización
from scipy.stats import norm, multivariate_normal  # Para distribuciones probabilísticas

class FiltroParticulas:
    """
    Implementación del Filtro de Partículas (Sequential Monte Carlo)
    para estimación de estado en sistemas dinámicos.
    """

    def __init__(self, n_particulas, dim_estado, transicion_estado, modelo_observacion,
                 ruido_proceso, ruido_observacion, x_inicial):
        # Inicialización de parámetros del filtro
        self.n = n_particulas  # Número de partículas
        self.dim = dim_estado  # Dimensión del espacio de estados
        self.f = transicion_estado  # Función de transición de estado
        self.h = modelo_observacion  # Función de observación
        self.Q = ruido_proceso  # Covarianza del ruido del proceso
        self.R = ruido_observacion  # Covarianza del ruido de observación
        
        # Inicialización de partículas (distribución inicial)
        self.particulas = np.random.multivariate_normal(
            mean=x_inicial,  # Centrado en el estado inicial
            cov=np.eye(dim_estado),  # Con cierta dispersión inicial
            size=n_particulas  # Número de partículas
        )
        # Inicialización de pesos (iguales al inicio)
        self.pesos = np.ones(n_particulas) / n_particulas  # Normalizados a sumar 1
        
        # Historial para guardar resultados
        self.historial_estimaciones = []  # Guarda las estimaciones de estado
        self.historial_particulas = []  # Guarda las partículas en cada paso

    def predecir(self, u=None, dt=1.0):
        """
        Fase de predicción: propaga las partículas según el modelo dinámico.
        """
        # Para cada partícula en el conjunto
        for i in range(self.n):
            # Aplicar modelo dinámico (transición de estado)
            self.particulas[i] = self.f(self.particulas[i], u, dt)
            # Añadir ruido del proceso (exploración)
            self.particulas[i] += multivariate_normal.rvs(
                mean=np.zeros(self.dim),  # Ruido con media cero
                cov=self.Q  # Covarianza del ruido del proceso
            )
        
        # Guardar estado actual de las partículas para historial
        self.historial_particulas.append(self.particulas.copy())

    def actualizar(self, z):
        """
        Fase de actualización: ajusta pesos según la observación actual.
        """
        # Calcular nuevos pesos basados en la observación
        for i in range(self.n):
            # Calcular residuo (diferencia entre observación real y predicha)
            residuo = z - self.h(self.particulas[i])
            # Calcular verosimilitud (probabilidad de la observación dado el estado)
            self.pesos[i] = multivariate_normal.pdf(
                residuo, 
                mean=np.zeros_like(z),  # Media cero (error)
                cov=self.R  # Covarianza del ruido de observación
            )
        
        # Evitar pesos cero para estabilidad numérica
        self.pesos += 1e-300  # Pequeño valor epsilon
        # Normalizar pesos para que sumen 1 (distribución de probabilidad)
        self.pesos /= np.sum(self.pesos)
        
        # Calcular estimación actual como promedio ponderado
        estimacion = np.average(self.particulas, weights=self.pesos, axis=0)
        # Guardar estimación en historial
        self.historial_estimaciones.append(estimacion)
        
        # Realizar remuestreo para evitar degeneración
        self._resample()
        
        return estimacion  # Devolver la estimación actual

    def _resample(self):
        """
        Remuestreo sistemático para evitar degeneración de partículas.
        """
        # Generar posiciones estratificadas para remuestreo
        posiciones = (np.arange(self.n) + np.random.random()) / self.n
        # Inicializar índices de nuevas partículas
        indices = np.zeros(self.n, dtype=int)
        # Calcular suma acumulativa de pesos
        cumsum = np.cumsum(self.pesos)
        
        # Algoritmo de remuestreo sistemático
        i, j = 0, 0
        while i < self.n:
            if posiciones[i] < cumsum[j]:
                indices[i] = j  # Seleccionar partícula j
                i += 1
            else:
                j += 1
        
        # Reemplazar partículas según índices calculados
        self.particulas = self.particulas[indices]
        # Resetear pesos a uniformes
        self.pesos = np.ones(self.n) / self.n

    def filtrar(self, observaciones, entradas=None, dt=1.0):
        """
        Ejecuta el filtro completo para una secuencia de observaciones.
        """
        estimaciones = []  # Lista para guardar estimaciones
        # Procesar cada observación en secuencia
        for t, z in enumerate(observaciones):
            u = entradas[t] if entradas is not None else None  # Entrada de control opcional
            self.predecir(u, dt)  # Fase de predicción
            estimacion = self.actualizar(z)  # Fase de actualización
            estimaciones.append(estimacion)  # Guardar estimación
        return estimaciones  # Devolver todas las estimaciones

    def graficar_resultados(self, estados_reales=None):
        """
        Visualización de los resultados del filtrado.
        """
        plt.figure(figsize=(12, 6))  # Crear figura
        
        # Convertir historial a array numpy
        estimaciones = np.array(self.historial_estimaciones)
        
        # Graficar cada dimensión del estado por separado
        for d in range(self.dim):
            plt.subplot(self.dim, 1, d+1)  # Crear subplot
            
            # Graficar estimaciones del filtro
            plt.plot(estimaciones[:, d], 'b-', label='Estimación')
            
            # Graficar estado real si está disponible (para comparación)
            if estados_reales is not None:
                reales = np.array(estados_reales)
                plt.plot(reales[:, d], 'g--', label='Estado real')
            
            # Graficar partículas en tiempos clave para visualizar dispersión
            for t in [0, len(self.historial_particulas)//2, -1]:
                if t < len(self.historial_particulas):
                    particulas_t = self.historial_particulas[t]
                    plt.scatter([t]*self.n, particulas_t[:, d], 
                                color='red', alpha=0.1, s=10)
            
            plt.ylabel(f'Dimensión {d+1}')  # Etiqueta eje Y
            plt.legend()  # Mostrar leyenda
            plt.grid(True)  # Activar grid
        
        plt.xlabel('Tiempo')  # Etiqueta eje X común
        plt.tight_layout()  # Ajustar layout
        plt.show()  # Mostrar gráfico

# Ejemplo de uso: Seguimiento de posición y velocidad
if __name__ == "__main__":
    # Configuración de semilla aleatoria para reproducibilidad
    np.random.seed(42)
    
    # Parámetros de simulación
    n_pasos = 50  # Número de pasos de tiempo
    dt = 0.1  # Tamaño del paso de tiempo
    
    # 1. Definir funciones del modelo dinámico
    
    # Función de transición de estado (modelo de velocidad constante)
    def transicion_estado(x, u, dt):
        F = np.array([[1, dt],  # Matriz de transición
                     [0, 1]])
        return F @ x  # Multiplicación matriz-vector
    
    # Función de observación (solo observamos la posición)
    def modelo_observacion(x):
        H = np.array([[1, 0]])  # Matriz de observación
        return H @ x  # Multiplicación matriz-vector
    
    # 2. Configurar filtro de partículas
    
    n_particulas = 1000  # Número de partículas
    dim_estado = 2  # Dimensión del estado [posición, velocidad]
    
    # Matrices de covarianza de ruidos
    ruido_proceso = np.array([[0.1, 0],  # Ruido en el modelo dinámico
                             [0, 0.3]])
    ruido_observacion = np.array([[0.5]])  # Ruido en las observaciones
    
    # Estado inicial verdadero
    x_inicial = np.array([0, 1])  # Posición 0, velocidad 1
    
    # Crear instancia del filtro
    filtro = FiltroParticulas(
        n_particulas=n_particulas,
        dim_estado=dim_estado,
        transicion_estado=transicion_estado,
        modelo_observacion=modelo_observacion,
        ruido_proceso=ruido_proceso,
        ruido_observacion=ruido_observacion,
        x_inicial=x_inicial
    )
    
    # 3. Generar datos de simulación
    
    estados_reales = []  # Para guardar estados reales
    observaciones = []  # Para guardar observaciones
    
    x_real = x_inicial.copy()  # Estado real inicial
    
    # Simulación del sistema real
    for _ in range(n_pasos):
        # Evolución del estado real según modelo dinámico
        x_real = transicion_estado(x_real, None, dt)
        # Añadir ruido del proceso
        x_real += multivariate_normal.rvs(
            mean=np.zeros(dim_estado), 
            cov=ruido_proceso
        )
        
        # Generar observación con ruido
        z = modelo_observacion(x_real) + np.random.normal(0, ruido_observacion[0,0])
        
        # Guardar estados y observaciones
        estados_reales.append(x_real.copy())
        observaciones.append(z)
    
    # 4. Ejecutar filtro de partículas sobre las observaciones
    estimaciones = filtro.filtrar(observaciones, dt=dt)
    
    # 5. Mostrar resultados finales
    print("\nResultados del filtrado de partículas:")
    print(f"Estimación final: {estimaciones[-1]}")
    print(f"Estado real final: {estados_reales[-1]}")
    
    # 6. Visualizar resultados
    filtro.graficar_resultados(estados_reales)