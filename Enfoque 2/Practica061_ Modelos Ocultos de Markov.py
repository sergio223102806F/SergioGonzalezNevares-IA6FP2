# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 15:30:27 2025

@author: elvin
"""

import numpy as np

class HMM:
    def __init__(self, estados, observaciones):
        """
        Inicializa un HMM básico
        
        Args:
            estados (list): Lista de estados ocultos (ej: ['Soleado', 'Lluvioso'])
            observaciones (list): Lista de observaciones posibles (ej: ['Pasea', 'Queda_casa'])
        """
        self.estados = estados
        self.observaciones = observaciones
        self.N = len(estados)  # Número de estados
        self.M = len(observaciones)  # Número de observaciones
        
        # Inicializar parámetros aleatoriamente (normalizados)
        self.A = np.random.rand(self.N, self.N)  # Matriz de transición
        self.A = self.A / self.A.sum(axis=1, keepdims=True)
        
        self.B = np.random.rand(self.N, self.M)  # Matriz de emisión
        self.B = self.B / self.B.sum(axis=1, keepdims=True)
        
        self.pi = np.random.rand(self.N)  # Distribución inicial
        self.pi = self.pi / self.pi.sum()

    def forward(self, obs_seq):
        """Algoritmo hacia adelante (filtrado)"""
        T = len(obs_seq)
        alpha = np.zeros((T, self.N))
        
        # Paso inicial
        obs_idx = self.observaciones.index(obs_seq[0])
        alpha[0] = self.pi * self.B[:, obs_idx]
        alpha[0] /= alpha[0].sum()  # Normalizar
        
        # Pasos recursivos
        for t in range(1, T):
            obs_idx = self.observaciones.index(obs_seq[t])
            alpha[t] = self.B[:, obs_idx] * np.dot(alpha[t-1], self.A)
            alpha[t] /= alpha[t].sum()
            
        return alpha

    def viterbi(self, obs_seq):
        """Algoritmo de Viterbi para decodificación"""
        T = len(obs_seq)
        delta = np.zeros((T, self.N))
        psi = np.zeros((T, self.N), dtype=int)
        
        # Inicialización
        obs_idx = self.observaciones.index(obs_seq[0])
        delta[0] = self.pi * self.B[:, obs_idx]
        delta[0] /= delta[0].sum()
        
        # Recursión
        for t in range(1, T):
            obs_idx = self.observaciones.index(obs_seq[t])
            for j in range(self.N):
                trans_probs = delta[t-1] * self.A[:, j]
                psi[t, j] = np.argmax(trans_probs)
                delta[t, j] = trans_probs[psi[t, j]] * self.B[j, obs_idx]
            delta[t] /= delta[t].sum()
        
        # Backtracking
        path = np.zeros(T, dtype=int)
        path[-1] = np.argmax(delta[-1])
        for t in range(T-2, -1, -1):
            path[t] = psi[t+1, path[t+1]]
            
        return [self.estados[i] for i in path]

    def train(self, obs_seqs, max_iter=10):
        """Entrenamiento básico con algoritmo Baum-Welch (EM)"""
        for _ in range(max_iter):
            # Aquí iría la implementación completa de Baum-Welch
            # Por simplicidad, solo mostramos un esqueleto
            new_A = np.zeros((self.N, self.N))
            new_B = np.zeros((self.N, self.M))
            new_pi = np.zeros(self.N)
            
            # En la práctica, aquí se calcularían nuevas estimaciones
            # usando todas las secuencias de entrenamiento
            
            # Actualizamos parámetros (simulado)
            self.A = 0.9*self.A + 0.1*new_A
            self.B = 0.9*self.B + 0.1*new_B
            self.pi = 0.9*self.pi + 0.1*new_pi

# Ejemplo de uso
if __name__ == "__main__":
    # 1. Definimos estados y observaciones
    estados = ['Soleado', 'Lluvioso']
    observaciones = ['Pasea', 'Queda_casa', 'Usa_paraguas']
    
    # 2. Creamos modelo
    modelo = HMM(estados, observaciones)
    
    # 3. Secuencia de observaciones de ejemplo
    secuencia = ['Pasea', 'Queda_casa', 'Usa_paraguas', 'Queda_casa']
    
    # 4. Filtrado: estimar estado actual
    print("\nProbabilidades filtradas:")
    alpha = modelo.forward(secuencia)
    for t, probs in enumerate(alpha):
        print(f"Tiempo {t}:")
        for i, estado in enumerate(estados):
            print(f"  P({estado}) = {probs[i]:.3f}")
    
    # 5. Decodificación: secuencia más probable
    print("\nSecuencia más probable de estados:")
    secuencia_estados = modelo.viterbi(secuencia)
    print(" -> ".join(secuencia_estados))
    
    # 6. Entrenamiento (simulado)
    print("\nEntrenando modelo...")
    modelo.train([secuencia])  # Normalmente con múltiples secuencias