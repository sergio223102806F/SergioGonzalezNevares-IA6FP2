# -*- coding: utf-8 -*-
"""
Implementación de Modelos Ocultos de Markov (HMM)
Creado el Sábado 26 de Abril 2025
Autor: elvin
"""

# Importación de numpy para operaciones matriciales
import numpy as np

# Importación de scipy.stats para distribuciones estadísticas (no usado directamente aquí)
from scipy.stats import norm

# Importación de matplotlib para visualización
import matplotlib.pyplot as plt

class HMM:
    """
    Implementación completa de un Modelo Oculto de Markov con:
    - Filtrado (forward algorithm)
    - Predicción de estados futuros
    - Suavizado (forward-backward algorithm)
    - Decodificación de secuencia (Viterbi algorithm)
    """
    
    def __init__(self, A, B, pi):
        """
        Inicializa el HMM con sus parámetros fundamentales
        
        Args:
            A (np.array): Matriz de transición entre estados (NxN)
            B (np.array): Matriz de emisión/observación (NxM)
            pi (np.array): Distribución inicial de probabilidades (1xN)
        """
        self.A = A  # Matriz de transición de estados (N estados)
        self.B = B  # Matriz de emisión (M observables posibles)
        self.pi = pi  # Distribución inicial de estados
        self.N = A.shape[0]  # Número de estados ocultos
        self.M = B.shape[1]  # Número de observaciones posibles
        
        # Validación de que los parámetros son consistentes
        self._validar_parametros()
    
    def _validar_parametros(self):
        """Verifica que las matrices sean válidas (sumas de probabilidades)"""
        # Verifica que cada fila de A sume 1 (probabilidades de transición)
        assert np.allclose(self.A.sum(axis=1), np.ones(self.N)), "Filas de A deben sumar 1"
        # Verifica que cada fila de B sume 1 (probabilidades de emisión)
        assert np.allclose(self.B.sum(axis=1), np.ones(self.N)), "Filas de B deben sumar 1"
        # Verifica que la distribución inicial sume 1
        assert np.allclose(self.pi.sum(), 1), "pi debe sumar 1"
    
    def filtrado(self, observaciones):
        """
        Algoritmo de filtrado (forward) para estimar el estado actual
        
        Args:
            observaciones (list): Secuencia de índices de observaciones
            
        Returns:
            tuple: (alpha, log_verosimilitud)
                   alpha: Probabilidades de estado en cada tiempo
                   log_verosimilitud: Log-verosimilitud de la secuencia
        """
        T = len(observaciones)  # Longitud de la secuencia
        alpha = np.zeros((T, self.N))  # Matriz para probabilidades forward
        c = np.zeros(T)  # Factores de normalización
        
        # Paso inicial (t=0)
        alpha[0] = self.pi * self.B[:, observaciones[0]]  # Combinación inicial
        c[0] = alpha[0].sum()  # Factor de normalización
        alpha[0] /= c[0]  # Normalización
        
        # Pasos recursivos (t=1 a T-1)
        for t in range(1, T):
            # Calcula probabilidades no normalizadas
            alpha[t] = self.B[:, observaciones[t]] * (alpha[t-1] @ self.A)
            # Calcula factor de normalización
            c[t] = alpha[t].sum()
            # Normaliza las probabilidades
            alpha[t] /= c[t]
        
        # Calcula log-verosimilitud sumando los logs de los factores de normalización
        log_verosimilitud = np.sum(np.log(c))
        return alpha, log_verosimilitud
    
    def prediccion(self, alpha, k=1):
        """
        Predice estados k pasos adelante usando las probabilidades filtradas
        
        Args:
            alpha (np.array): Probabilidades filtradas actuales
            k (int): Número de pasos a predecir
            
        Returns:
            np.array: Probabilidades predichas para cada paso futuro
        """
        alpha_pred = alpha.copy()  # Copia para no modificar el original
        predicciones = []  # Almacenará los resultados
        
        # Calcula predicciones para cada paso
        for _ in range(k):
            alpha_pred = alpha_pred @ self.A  # Multiplica por matriz de transición
            predicciones.append(alpha_pred)
        
        return np.array(predicciones)
    
    def suavizado(self, observaciones):
        """
        Algoritmo de suavizado (forward-backward) para estimar estados pasados
        
        Args:
            observaciones (list): Secuencia completa de observaciones
            
        Returns:
            np.array: Probabilidades suavizadas gamma
        """
        T = len(observaciones)  # Longitud de la secuencia
        
        # Paso forward (usa el algoritmo de filtrado)
        alpha, _ = self.filtrado(observaciones)
        
        # Paso backward
        beta = np.zeros((T, self.N))  # Matriz para probabilidades backward
        beta[-1] = 1.0  # Inicialización en t=T
        
        # Recorrido hacia atrás (t=T-2 a t=0)
        for t in range(T-2, -1, -1):
            # Calcula probabilidades backward
            beta[t] = (self.A * self.B[:, observaciones[t+1]] * beta[t+1]).sum(axis=1)
            # Normalización numérica
            beta[t] /= beta[t].sum()
        
        # Combinación de forward y backward
        gamma = alpha * beta
        # Normalización para obtener probabilidades válidas
        gamma /= gamma.sum(axis=1, keepdims=True)
        
        return gamma
    
    def algoritmo_viterbi(self, observaciones):
        """
        Algoritmo de Viterbi para encontrar la secuencia de estados más probable
        
        Args:
            observaciones (list): Secuencia de observaciones
            
        Returns:
            tuple: (secuencia_estados, probabilidad)
                   secuencia_estados: Índices de la secuencia más probable
                   probabilidad: Probabilidad de dicha secuencia
        """
        T = len(observaciones)  # Longitud de la secuencia
        delta = np.zeros((T, self.N))  # Matriz para maximización
        psi = np.zeros((T, self.N), dtype=int)  # Matriz para backtracking
        
        # Inicialización (t=0)
        delta[0] = self.pi * self.B[:, observaciones[0]]
        delta[0] /= delta[0].sum()  # Normalización
        
        # Recursión (t=1 a T-1)
        for t in range(1, T):
            for j in range(self.N):
                # Calcula probabilidades de transición
                trans_prob = delta[t-1] * self.A[:, j]
                # Guarda el estado más probable que lleva a j
                psi[t, j] = np.argmax(trans_prob)
                # Actualiza probabilidad máxima
                delta[t, j] = trans_prob[psi[t, j]] * self.B[j, observaciones[t]]
            # Normalización
            delta[t] /= delta[t].sum()
        
        # Backtracking para encontrar la secuencia
        estados = np.zeros(T, dtype=int)  # Almacenará la secuencia óptima
        estados[-1] = np.argmax(delta[-1])  # Comienza por el último estado
        
        # Reconstruye la secuencia hacia atrás
        for t in range(T-2, -1, -1):
            estados[t] = psi[t+1, estados[t+1]]
        
        return estados, np.max(delta[-1])

# Bloque principal de ejecución (ejemplo de uso)
if __name__ == "__main__":
    print("=== Ejemplo HMM: Modelo de Clima ===")
    
    # 1. Definición del modelo
    
    # Estados ocultos (el clima real)
    estados = ["Soleado", "Nublado", "Lluvioso"]
    N = len(estados)  # Número de estados
    
    # Observaciones (comportamiento de las personas)
    observables = ["Pasea", "Shopping", "Netflix"]
    M = len(observables)  # Número de observaciones
    
    # Matriz de transición (A) - Probabilidades entre estados ocultos
    A = np.array([
        [0.7, 0.2, 0.1],  # Desde Soleado
        [0.3, 0.4, 0.3],  # Desde Nublado
        [0.2, 0.3, 0.5]   # Desde Lluvioso
    ])
    
    # Matriz de emisión (B) - Probabilidades de observación dado el estado
    B = np.array([
        [0.6, 0.3, 0.1],  # Si está Soleado
        [0.3, 0.4, 0.3],  # Si está Nublado
        [0.1, 0.2, 0.7]   # Si está Lluvioso
    ])
    
    # Distribución inicial (pi) - Probabilidades iniciales del estado
    pi = np.array([0.6, 0.3, 0.1])
    
    # 2. Creación del modelo HMM
    modelo = HMM(A, B, pi)
    
    # 3. Secuencia de observaciones de ejemplo
    # Mapeo de observaciones a índices
    obs_map = {v:k for k,v in enumerate(observables)}
    # Secuencia de observaciones (convertida a índices)
    observaciones = ["Pasea", "Shopping", "Netflix", "Netflix", "Pasea"]
    obs_seq = [obs_map[o] for o in observaciones]
    
    # 4. Demostración de las capacidades del modelo
    
    # 4.1 Filtrado: estimación del estado actual
    print("\n1. Filtrado (estimación estado actual):")
    alpha, _ = modelo.filtrado(obs_seq)
    print("Probabilidades filtradas:")
    for t in range(len(observaciones)):
        print(f"t={t}: {dict(zip(estados, alpha[t].round(3)))}")
    
    # 4.2 Predicción: estados futuros
    print("\n2. Predicción (1 paso adelante):")
    pred = modelo.prediccion(alpha[-1], k=1)
    print("Probabilidades predichas:")
    print(dict(zip(estados, pred[0].round(3))))
    
    # 4.3 Suavizado: estimación mejorada de estados pasados
    print("\n3. Suavizado (estimación estados pasados):")
    gamma = modelo.suavizado(obs_seq)
    print("Probabilidades suavizadas:")
    for t in range(len(observaciones)):
        print(f"t={t}: {dict(zip(estados, gamma[t].round(3)))}")
    
    # 4.4 Secuencia más probable (Viterbi)
    print("\n4. Secuencia más probable de estados (Viterbi):")
    secuencia, prob = modelo.algoritmo_viterbi(obs_seq)
    print("Secuencia:", " -> ".join([estados[s] for s in secuencia]))
    print(f"Probabilidad: {prob:.6f}")
    
    # 5. Visualización gráfica de los resultados
    plt.figure(figsize=(10, 6))  # Tamaño de la figura
    
    # 5.1 Gráfico de filtrado
    plt.subplot(2, 2, 1)
    for i in range(N):
        plt.plot(alpha[:, i], label=estados[i])
    plt.title("Probabilidades de Filtrado")
    plt.xlabel("Tiempo")
    plt.ylabel("Probabilidad")
    plt.legend()
    
    # 5.2 Gráfico de suavizado
    plt.subplot(2, 2, 2)
    for i in range(N):
        plt.plot(gamma[:, i], label=estados[i])
    plt.title("Probabilidades Suavizadas")
    plt.xlabel("Tiempo")
    plt.ylabel("Probabilidad")
    plt.legend()
    
    # 5.3 Gráfico de predicción
    pred_3 = modelo.prediccion(alpha[-1], k=3)
    plt.subplot(2, 2, 3)
    for i in range(N):
        plt.plot(range(3), pred_3[:, i], 'o-', label=estados[i])
    plt.title("Predicción a 3 pasos")
    plt.xlabel("Pasos adelante")
    plt.ylabel("Probabilidad")
    plt.xticks(range(3))
    plt.legend()
    
    # 5.4 Gráfico de secuencia Viterbi
    plt.subplot(2, 2, 4)
    plt.plot(secuencia, 'ro-')
    plt.yticks(range(N), estados)
    plt.title("Secuencia Viterbi")
    plt.xlabel("Tiempo")
    plt.ylabel("Estado")
    
    plt.tight_layout()  # Ajuste de layout
    plt.show()  # Mostrar gráficos