# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 18:14:49 2025

@author: elvin
"""

# Importación de numpy para operaciones matriciales
import numpy as np  

class BoltzmannMachine:
    def __init__(self, n_neurons):
        """
        Constructor - Inicializa la máquina con:
        Args:
            n_neurons: Número de neuronas en la red
        """
        # Matriz de pesos (simétrica) inicializada en ceros
        # Shape: (n_neurons, n_neurons)
        self.weights = np.zeros((n_neurons, n_neurons))
        
        # Vector de sesgos (bias) para cada neurona
        self.biases = np.zeros(n_neurons)  

    def energy(self, state):
        """
        Calcula la energía de un estado específico
        Fórmula: E = -0.5*sᵀWs - bᵀs
        Args:
            state: Vector de estados de las neuronas (1 activado, 0 desactivado)
        Returns:
            Valor de energía (float)
        """
        return -0.5 * state @ self.weights @ state - self.biases @ state

    def update_rule(self, visible_data, lr=0.1):
        """
        Actualiza pesos usando Contrastive Divergence (CD-1)
        Args:
            visible_data: Vector de datos observados
            lr: Tasa de aprendizaje (learning rate)
        """
        # Fase positiva (producto exterior de datos reales)
        positive_phase = np.outer(visible_data, visible_data)
        
        # Fase negativa (muestreo del modelo)
        hidden_state = self.sample_hidden(visible_data)
        negative_phase = np.outer(hidden_state, hidden_state)
        
        # Actualización de pesos: ΔW = η(<vvᵀ>data - <vvᵀ>model)
        self.weights += lr * (positive_phase - negative_phase)

    def sample_hidden(self, visible_state, steps=100):
        """
        Muestreo de Gibbs para generar estados ocultos
        Args:
            visible_state: Estado visible inicial
            steps: Pasos de muestreo
        Returns:
            Vector de estados muestreados
        """
        state = visible_state.copy()  # Copia del estado inicial
        
        for _ in range(steps):  # Iteraciones de muestreo
            for i in range(len(state)):  # Actualización por neurona
                # Calcula probabilidad de activación (sigmoide)
                prob = 1 / (1 + np.exp(-(self.weights[i] @ state + self.biases[i])))
                # Muestrea estado binario
                state[i] = 1 if np.random.rand() < prob else 0
                
        return state

# Ejemplo de uso mínimo
if __name__ == "__main__":
    # 1. Configuración inicial
    n_neurons = 4  # Neuronas en la red
    data = [np.array([1, 0, 1, 0]),  # Datos de entrenamiento
            np.array([0, 1, 0, 1])]  # (2 patrones binarios)

    # 2. Crear máquina
    bm = BoltzmannMachine(n_neurons)

    # 3. Entrenamiento (100 épocas)
    for epoch in range(100):
        for sample in data:
            bm.update_rule(sample, lr=0.05)  # Tasa de aprendizaje 0.05

    # 4. Evaluación
    test_state = np.array([1, 0, 1, 0])
    print("Energía del estado [1,0,1,0]:", bm.energy(test_state))