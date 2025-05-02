# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 15:30:27 2025

@author: elvin
"""

import numpy as np

class HMM_Simple:
    def __init__(self, A, B, pi):
        """Inicializa el modelo HMM con matrices de transición (A), emisión (B) y distribución inicial (pi)"""
        self.A = A  # Matriz de transición entre estados
        self.B = B  # Matriz de emisión de observaciones
        self.pi = pi  # Distribución inicial de estados
        self.N = A.shape[0]  # Número de estados
        
    def forward(self, obs):
        """Paso hacia delante: calcula probabilidades de estado dado observaciones hasta el momento"""
        T = len(obs)
        alpha = np.zeros((T, self.N))
        alpha[0] = self.pi * self.B[:, obs[0]]
        
        for t in range(1, T):
            alpha[t] = self.B[:, obs[t]] * (alpha[t-1] @ self.A)
            alpha[t] /= alpha[t].sum()  # Normalización
            
        return alpha
    
    def backward(self, obs):
        """Paso hacia atrás: calcula probabilidades de observaciones futuras dado el estado actual"""
        T = len(obs)
        beta = np.ones((T, self.N))
        
        for t in range(T-2, -1, -1):
            beta[t] = (self.A * self.B[:, obs[t+1]] * beta[t+1]).sum(axis=1)
            beta[t] /= beta[t].sum()  # Normalización
            
        return beta
    
    def smooth(self, obs):
        """Algoritmo completo hacia delante-atrás para suavizado de estados"""
        alpha = self.forward(obs)
        beta = self.backward(obs)
        
        gamma = alpha * beta
        gamma /= gamma.sum(axis=1, keepdims=True)  # Probabilidades suavizadas
        
        return gamma

# Ejemplo de uso simplificado
if __name__ == "__main__":
    # Definimos un modelo de clima simple
    estados = ["Soleado", "Lluvioso"]
    obs = ["Pasea", "Queda_casa"]  # Observaciones
    
    # Matrices del modelo
    A = np.array([[0.7, 0.3],  # Transición entre estados
                 [0.4, 0.6]])
    
    B = np.array([[0.8, 0.2],  # Emisión de observaciones
                 [0.1, 0.9]])
    
    pi = np.array([0.6, 0.4])  # Distribución inicial
    
    # Creamos y usamos el modelo
    modelo = HMM_Simple(A, B, pi)
    secuencia_obs = [0, 1, 0]  # Pasea, Queda_casa, Pasea
    
    # Calculamos probabilidades suavizadas
    gamma = modelo.smooth(secuencia_obs)
    
    print("Probabilidades suavizadas de estados:")
    for t, probs in enumerate(gamma):
        print(f"Tiempo {t}: Soleado={probs[0]:.3f}, Lluvioso={probs[1]:.3f}")