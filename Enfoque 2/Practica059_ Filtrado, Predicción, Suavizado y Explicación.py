# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 15:26:36 2025

@author: elvin
"""

import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

class HMM:
    """
    Implementación de un Modelo Oculto de Markov (HMM) con funciones para:
    - Filtrado: estimar el estado actual dado observaciones hasta el presente
    - Predicción: estimar estados futuros
    - Suavizado: estimar estados pasados dado todo el historial de observaciones
    """
    
    def __init__(self, A, B, pi):
        """
        Inicializa el HMM con parámetros del modelo.
        
        Args:
            A (np.array): Matriz de transición de estados NxN
            B (np.array): Matriz de emisión (probabilidades de observación) NxM
            pi (np.array): Distribución inicial de estados 1xN
        """
        self.A = A  # Matriz de transición (N estados)
        self.B = B  # Matriz de emisión (M observables)
        self.pi = pi  # Distribución inicial
        self.N = A.shape[0]  # Número de estados
        self.M = B.shape[1]  # Número de observables
        
        # Validación de parámetros
        self._validar_parametros()
    
    def _validar_parametros(self):
        """Verifica que los parámetros sean válidos."""
        assert np.allclose(self.A.sum(axis=1), np.ones(self.N)), "Filas de A deben sumar 1"
        assert np.allclose(self.B.sum(axis=1), np.ones(self.N)), "Filas de B deben sumar 1"
        assert np.allclose(self.pi.sum(), 1), "pi debe sumar 1"
    
    def filtrado(self, observaciones):
        """
        Algoritmo de filtrado (forward) para estimar el estado actual.
        
        Args:
            observaciones (list): Secuencia de observaciones
            
        Returns:
            tuple: (probabilidades filtradas, log-verosimilitud)
        """
        T = len(observaciones)
        alpha = np.zeros((T, self.N))
        c = np.zeros(T)  # Factores de normalización
        
        # Paso inicial
        alpha[0] = self.pi * self.B[:, observaciones[0]]
        c[0] = alpha[0].sum()
        alpha[0] /= c[0]
        
        # Pasos recursivos
        for t in range(1, T):
            alpha[t] = self.B[:, observaciones[t]] * (alpha[t-1] @ self.A)
            c[t] = alpha[t].sum()
            alpha[t] /= c[t]
        
        log_verosimilitud = np.sum(np.log(c))
        return alpha, log_verosimilitud
    
    def prediccion(self, alpha, k=1):
        """
        Predice estados futuros dado el estado filtrado actual.
        
        Args:
            alpha (np.array): Probabilidades filtradas actuales
            k (int): Número de pasos a predecir
            
        Returns:
            np.array: Probabilidades predichas para k pasos adelante
        """
        alpha_pred = alpha.copy()
        predicciones = []
        
        for _ in range(k):
            alpha_pred = alpha_pred @ self.A
            predicciones.append(alpha_pred)
        
        return np.array(predicciones)
    
    def suavizado(self, observaciones):
        """
        Algoritmo de suavizado (forward-backward) para estimar estados pasados.
        
        Args:
            observaciones (list): Secuencia completa de observaciones
            
        Returns:
            np.array: Probabilidades suavizadas para cada estado
        """
        T = len(observaciones)
        
        # Paso forward (filtrado)
        alpha, _ = self.filtrado(observaciones)
        
        # Paso backward
        beta = np.zeros((T, self.N))
        beta[-1] = 1.0
        
        for t in range(T-2, -1, -1):
            beta[t] = (self.A * self.B[:, observaciones[t+1]] * beta[t+1]).sum(axis=1)
            beta[t] /= beta[t].sum()  # Normalización
        
        # Combinar forward y backward
        gamma = alpha * beta
        gamma /= gamma.sum(axis=1, keepdims=True)
        
        return gamma
    
    def algoritmo_viterbi(self, observaciones):
        """
        Algoritmo de Viterbi para encontrar la secuencia de estados más probable.
        
        Args:
            observaciones (list): Secuencia de observaciones
            
        Returns:
            tuple: (secuencia de estados, probabilidad)
        """
        T = len(observaciones)
        delta = np.zeros((T, self.N))
        psi = np.zeros((T, self.N), dtype=int)
        
        # Inicialización
        delta[0] = self.pi * self.B[:, observaciones[0]]
        delta[0] /= delta[0].sum()
        
        # Recursión
        for t in range(1, T):
            for j in range(self.N):
                trans_prob = delta[t-1] * self.A[:, j]
                psi[t, j] = np.argmax(trans_prob)
                delta[t, j] = trans_prob[psi[t, j]] * self.B[j, observaciones[t]]
            delta[t] /= delta[t].sum()  # Normalización
        
        # Backtracking
        estados = np.zeros(T, dtype=int)
        estados[-1] = np.argmax(delta[-1])
        
        for t in range(T-2, -1, -1):
            estados[t] = psi[t+1, estados[t+1]]
        
        return estados, np.max(delta[-1])

# Ejemplo de uso con modelo de clima y observaciones discretas
if __name__ == "__main__":
    print("=== Ejemplo HMM: Modelo de Clima ===")
    
    # Definir estados ocultos (clima real no observable)
    estados = ["Soleado", "Nublado", "Lluvioso"]
    N = len(estados)
    
    # Definir observaciones (acciones de personas)
    observables = ["Pasea", "Shopping", "Netflix"]
    M = len(observables)
    
    # Matriz de transición (A)
    A = np.array([
        [0.7, 0.2, 0.1],  # Desde Soleado
        [0.3, 0.4, 0.3],  # Desde Nublado
        [0.2, 0.3, 0.5]   # Desde Lluvioso
    ])
    
    # Matriz de emisión (B)
    B = np.array([
        [0.6, 0.3, 0.1],  # Soleado
        [0.3, 0.4, 0.3],  # Nublado
        [0.1, 0.2, 0.7]   # Lluvioso
    ])
    
    # Distribución inicial (pi)
    pi = np.array([0.6, 0.3, 0.1])
    
    # Crear modelo HMM
    modelo = HMM(A, B, pi)
    
    # Secuencia de observaciones (ejemplo)
    obs_map = {v:k for k,v in enumerate(observables)}
    observaciones = ["Pasea", "Shopping", "Netflix", "Netflix", "Pasea"]
    obs_seq = [obs_map[o] for o in observaciones]
    
    # 1. Filtrado: estimar estado actual
    print("\n1. Filtrado (estimación estado actual):")
    alpha, _ = modelo.filtrado(obs_seq)
    print("Probabilidades filtradas:")
    for t in range(len(observaciones)):
        print(f"t={t}: {dict(zip(estados, alpha[t].round(3))}")
    
    # 2. Predicción: estados futuros
    print("\n2. Predicción (1 paso adelante):")
    pred = modelo.prediccion(alpha[-1], k=1)
    print("Probabilidades predichas:")
    print(dict(zip(estados, pred[0].round(3))))
    
    # 3. Suavizado: estimación estados pasados
    print("\n3. Suavizado (estimación estados pasados):")
    gamma = modelo.suavizado(obs_seq)
    print("Probabilidades suavizadas:")
    for t in range(len(observaciones)):
        print(f"t={t}: {dict(zip(estados, gamma[t].round(3))}")
    
    # 4. Secuencia más probable (Viterbi)
    print("\n4. Secuencia más probable de estados (Viterbi):")
    secuencia, prob = modelo.algoritmo_viterbi(obs_seq)
    print("Secuencia:", " -> ".join([estados[s] for s in secuencia]))
    print(f"Probabilidad: {prob:.6f}")
    
    # Visualización
    plt.figure(figsize=(10, 6))
    
    # Filtrado
    plt.subplot(2, 2, 1)
    for i in range(N):
        plt.plot(alpha[:, i], label=estados[i])
    plt.title("Probabilidades de Filtrado")
    plt.xlabel("Tiempo")
    plt.ylabel("Probabilidad")
    plt.legend()
    
    # Suavizado
    plt.subplot(2, 2, 2)
    for i in range(N):
        plt.plot(gamma[:, i], label=estados[i])
    plt.title("Probabilidades Suavizadas")
    plt.xlabel("Tiempo")
    plt.ylabel("Probabilidad")
    plt.legend()
    
    # Predicción
    pred_3 = modelo.prediccion(alpha[-1], k=3)
    plt.subplot(2, 2, 3)
    for i in range(N):
        plt.plot(range(3), pred_3[:, i], 'o-', label=estados[i])
    plt.title("Predicción a 3 pasos")
    plt.xlabel("Pasos adelante")
    plt.ylabel("Probabilidad")
    plt.xticks(range(3))
    plt.legend()
    
    # Viterbi
    plt.subplot(2, 2, 4)
    plt.plot(secuencia, 'ro-')
    plt.yticks(range(N), estados)
    plt.title("Secuencia Viterbi")
    plt.xlabel("Tiempo")
    plt.ylabel("Estado")
    
    plt.tight_layout()
    plt.show()