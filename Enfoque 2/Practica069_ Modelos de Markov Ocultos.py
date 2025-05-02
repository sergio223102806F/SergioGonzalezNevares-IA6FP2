# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 16:31:14 2025

@author: elvin
"""

import numpy as np  # Importa la librería NumPy para operaciones matriciales eficientes

class HMM:
    def __init__(self, A, B, pi):
        """
        Constructor de la clase HMM (Modelo Oculto de Markov)
        
        Parámetros:
        A : Matriz de transición entre estados ocultos (N x N)
        B : Matriz de emisión de observaciones (N x M)
        pi : Distribución inicial de probabilidades de estados (1 x N)
        """
        self.A = A  # Almacena la matriz de transición de estados
        self.B = B  # Almacena la matriz de probabilidades de observación
        self.pi = pi  # Almacena las probabilidades iniciales de estado
        
        self.N = A.shape[0]  # Número de estados ocultos (dimension de A)
        self.M = B.shape[1]  # Número de símbolos observables (dimension de B)

    def forward(self, obs):
        """
        Algoritmo Forward: Calcula la probabilidad de una secuencia observada
        
        Parámetros:
        obs : Lista de índices que representan la secuencia de observaciones
        
        Retorna:
        Probabilidad total de la secuencia observada bajo el modelo
        """
        T = len(obs)  # Longitud de la secuencia observada
        alpha = np.zeros((T, self.N))  # Matriz para almacenar las probabilidades forward
        
        # Paso inicial: alpha_1(i) = pi_i * b_i(o1)
        alpha[0, :] = self.pi * self.B[:, obs[0]]  # Multiplica pi por la columna de B correspondiente a la primera observación
        
        # Paso de inducción: alpha_t(j) = [sum_i alpha_{t-1}(i)*a_ij] * b_j(o_t)
        for t in range(1, T):  # Para cada paso de tiempo desde el segundo hasta el final
            for j in range(self.N):  # Para cada estado oculto j
                # Suma sobre todos los estados anteriores i
                alpha[t, j] = np.sum(alpha[t-1, :] * self.A[:, j]) * self.B[j, obs[t]]
        
        # Paso de terminación: P(O|modelo) = sum_i alpha_T(i)
        return np.sum(alpha[T-1, :])  # Suma las probabilidades en el último paso de tiempo

    def viterbi(self, obs):
        """
        Algoritmo de Viterbi: Encuentra la secuencia de estados más probable
        
        Parámetros:
        obs : Lista de índices que representan la secuencia de observaciones
        
        Retorna:
        Lista con la secuencia de estados más probable que genera las observaciones
        """
        T = len(obs)  # Longitud de la secuencia observada
        delta = np.zeros((T, self.N))  # Matriz para almacenar las máximas probabilidades
        psi = np.zeros((T, self.N), dtype=int)  # Matriz para almacenar los índices de los mejores estados anteriores
        
        # Inicialización: delta_1(i) = pi_i * b_i(o1)
        delta[0, :] = self.pi * self.B[:, obs[0]]  # Mismo cálculo que en forward
        
        # Recursión: delta_t(j) = max_i [delta_{t-1}(i)*a_ij] * b_j(o_t)
        for t in range(1, T):  # Para cada paso de tiempo desde el segundo hasta el final
            for j in range(self.N):  # Para cada estado oculto j
                # Encuentra el máximo sobre todos los estados anteriores i
                delta[t, j] = np.max(delta[t-1, :] * self.A[:, j]) * self.B[j, obs[t]]
                # Guarda el índice del estado que maximiza la probabilidad
                psi[t, j] = np.argmax(delta[t-1, :] * self.A[:, j])
        
        # Backtracking: Reconstruye la secuencia de estados más probable
        path = np.zeros(T, dtype=int)  # Array para almacenar el camino óptimo
        path[T-1] = np.argmax(delta[T-1, :])  # Comienza por el estado con máxima probabilidad al final
        
        # Recorre hacia atrás para encontrar el camino completo
        for t in range(T-2, -1, -1):
            path[t] = psi[t+1, path[t+1]]  # Usa psi para encontrar el mejor estado anterior
        
        return path  # Retorna la secuencia de estados óptima

    def baum_welch(self, obs, max_iter=100, tol=1e-6):
        """
        Algoritmo Baum-Welch: Entrena el modelo HMM con datos observados
        
        Parámetros:
        obs : Secuencia de observaciones para entrenamiento
        max_iter : Máximo número de iteraciones permitidas
        tol : Tolerancia para determinar convergencia
        
        Retorna:
        Tupla con las matrices A, B y pi actualizadas
        """
        T = len(obs)  # Longitud de la secuencia de entrenamiento
        old_log_prob = -np.inf  # Inicializa la probabilidad logarítmica anterior
        
        for _ in range(max_iter):  # Realiza hasta max_iter iteraciones
            # Paso Forward con escalamiento para evitar underflow
            alpha, c = self._forward_with_scaling(obs)
            
            # Paso Backward con escalamiento
            beta = self._backward_with_scaling(obs, c)
            
            # Inicializa matrices para gamma y xi
            gamma = np.zeros((T, self.N))  # gamma_t(i) = P(q_t=i|O,λ)
            xi = np.zeros((T-1, self.N, self.N))  # xi_t(i,j) = P(q_t=i,q_{t+1}=j|O,λ)
            
            # Calcula xi y gamma
            for t in range(T-1):
                # Denominador para normalizar xi
                denom = np.dot(np.dot(alpha[t, :], self.A) * self.B[:, obs[t+1]], beta[t+1, :])
                for i in range(self.N):
                    # Numerador para xi
                    numer = alpha[t, i] * self.A[i, :] * self.B[:, obs[t+1]] * beta[t+1, :]
                    xi[t, i, :] = numer / denom
            
            # Calcula gamma a partir de alpha y beta
            gamma = alpha * beta / c.reshape(-1, 1)
            
            # Reestimación de parámetros
            
            # Distribución inicial: gamma en t=0
            self.pi = gamma[0, :]
            
            # Matriz de transición A
            for i in range(self.N):
                denom = np.sum(gamma[:-1, i])  # Suma de gamma sobre todos los tiempos excepto el último
                for j in range(self.N):
                    self.A[i, j] = np.sum(xi[:, i, j]) / denom  # Suma xi sobre todos los tiempos
            
            # Matriz de emisión B
            for j in range(self.N):
                denom = np.sum(gamma[:, j])  # Suma de gamma sobre todos los tiempos
                for k in range(self.M):
                    # Suma gamma solo cuando la observación es k
                    mask = np.array(obs) == k
                    self.B[j, k] = np.sum(gamma[mask, j]) / denom
            
            # Verifica convergencia
            log_prob = -np.sum(np.log(c))  # Calcula la probabilidad logarítmica
            if log_prob - old_log_prob < tol:  # Si el cambio es menor que la tolerancia
                break  # Termina el entrenamiento
            old_log_prob = log_prob  # Actualiza la probabilidad anterior
        
        return self.A, self.B, self.pi  # Retorna las matrices entrenadas

    def _forward_with_scaling(self, obs):
        """Implementación del forward con escalamiento para evitar underflow"""
        T = len(obs)
        alpha = np.zeros((T, self.N))  # Matriz alpha escalada
        c = np.zeros(T)  # Factores de escalamiento
        
        # Paso inicial con escalamiento
        alpha[0, :] = self.pi * self.B[:, obs[0]]
        c[0] = 1.0 / np.sum(alpha[0, :])  # Factor de escalamiento
        alpha[0, :] *= c[0]  # Aplica escalamiento
        
        # Paso de inducción con escalamiento
        for t in range(1, T):
            alpha[t, :] = np.dot(alpha[t-1, :], self.A) * self.B[:, obs[t]]
            c[t] = 1.0 / np.sum(alpha[t, :])  # Calcula nuevo factor
            alpha[t, :] *= c[t]  # Aplica escalamiento
        
        return alpha, c  # Retorna alpha escalada y factores

    def _backward_with_scaling(self, obs, c):
        """Implementación del backward con escalamiento"""
        T = len(obs)
        beta = np.zeros((T, self.N))  # Matriz beta escalada
        
        # Inicialización
        beta[T-1, :] = c[T-1]  # Usa el último factor de escalamiento
        
        # Paso de inducción hacia atrás con escalamiento
        for t in range(T-2, -1, -1):
            beta[t, :] = np.dot(self.A, self.B[:, obs[t+1]] * beta[t+1, :])
            beta[t, :] *= c[t]  # Aplica el factor de escalamiento
        
        return beta  # Retorna beta escalada


# Ejemplo de uso
if __name__ == "__main__":
    # Configuración del ejemplo: Modelo del clima y actividades
    
    # Estados ocultos: Clima
    # 0 = Soleado, 1 = Nublado, 2 = Lluvioso
    
    # Observaciones: Actividades
    # 0 = Paseo, 1 = Compras, 2 = Limpieza
    
    # Matriz de transición entre estados climáticos
    A = np.array([[0.6, 0.3, 0.1],  # De soleado a [soleado, nublado, lluvioso]
                  [0.2, 0.5, 0.3],  # De nublado a ...
                  [0.1, 0.4, 0.5]]) # De lluvioso a ...
    
    # Matriz de emisión: Probabilidad de actividad dado el clima
    B = np.array([[0.6, 0.3, 0.1],  # Si es soleado
                  [0.3, 0.4, 0.3],  # Si es nublado
                  [0.1, 0.5, 0.4]]) # Si es lluvioso
    
    # Distribución inicial del clima
    pi = np.array([0.5, 0.3, 0.2])  # [soleado, nublado, lluvioso]
    
    # Crea una instancia del modelo HMM
    model = HMM(A, B, pi)
    
    # Secuencia de observaciones: [Paseo, Compras, Limpieza, Paseo]
    obs = [0, 1, 2, 0]
    
    # 1. Calcula la probabilidad de la secuencia observada
    prob = model.forward(obs)
    print(f"Probabilidad de la secuencia observada: {prob:.6f}")
    
    # 2. Encuentra la secuencia de estados climáticos más probable
    path = model.viterbi(obs)
    state_names = ["Soleado", "Nublado", "Lluvioso"]
    print("\nSecuencia de estados más probable:")
    for t, state in enumerate(path):
        print(f"Tiempo {t+1}: {state_names[state]}")
    
    # 3. Entrena el modelo con nuevas observaciones
    print("\nEntrenando el modelo...")
    new_obs = [0, 1, 2, 0, 1, 2, 0, 1, 0, 2]  # Nueva secuencia de actividades observadas
    trained_A, trained_B, trained_pi = model.baum_welch(new_obs)
    
    # Muestra los resultados del entrenamiento
    print("\nMatriz de transición entrenada:")
    print(trained_A)
    print("\nMatriz de emisión entrenada:")
    print(trained_B)
    print("\nDistribución inicial entrenada:")
    print(trained_pi)