# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 15:30:28 2025

@author: elvin
"""

# Importación de bibliotecas necesarias
import numpy as np  # Para operaciones matriciales y numéricas
from scipy.stats import multivariate_normal  # Para cálculos de probabilidad gaussiana
import matplotlib.pyplot as plt  # Para visualización de resultados

class HMM_ReconocimientoVoz:
    """
    Clase principal que implementa el sistema de reconocimiento de voz usando HMM.
    Cada palabra se modela como un HMM donde los estados representan segmentos del sonido.
    """

    def __init__(self, n_estados=5, n_coeficientes=13):
        """
        Constructor que inicializa el reconocedor.
        
        Args:
            n_estados (int): Número de estados por modelo (típicamente 3-5 por fonema)
            n_coeficientes (int): Dimensión de los vectores MFCC (usualmente 13-39)
        """
        self.n_estados = n_estados  # Guarda número de estados por modelo
        self.n_coeficientes = n_coeficientes  # Guarda dimensión de características MFCC
        self.modelos = {}  # Diccionario para almacenar modelos HMM de cada palabra
        self.palabras = []  # Lista de palabras conocidas por el sistema

    def extraer_mfcc(self, señal_audio, tasa_muestreo=16000):
        """
        Simulador de extracción de coeficientes MFCC.
        En producción se usaría librosa o python_speech_features.
        
        Args:
            señal_audio (np.array): Señal de audio digital
            tasa_muestreo (int): Frecuencia de muestreo (Hz)
            
        Returns:
            np.array: Matriz de coeficientes MFCC (frames x coeficientes)
        """
        # Cálculo simplificado del número de frames (100 frames/segundo)
        duración = len(señal_audio) / tasa_muestreo
        n_frames = int(duración * 100)  
        
        # Generar MFCCs aleatorios (en realidad se calcularían del audio)
        return np.random.randn(n_frames, self.n_coeficientes)

    def entrenar_modelo(self, palabra, ejemplos_audio):
        """
        Entrena un HMM para una palabra específica usando algoritmo Baum-Welch simplificado.
        
        Args:
            palabra (str): Palabra a modelar
            ejemplos_audio (list): Lista de señales de audio de entrenamiento
        """
        # 1. Extraer características MFCC para todos los ejemplos de audio
        secuencias_mfcc = [self.extraer_mfcc(audio) for audio in ejemplos_audio]
        
        # 2. Inicializar matriz de transición con diagonal dominante
        A = np.ones((self.n_estados, self.n_estados)) * 0.1  # Valores bajos
        np.fill_diagonal(A, 0.8)  # Alta probabilidad de permanecer en mismo estado
        A /= A.sum(axis=1, keepdims=True)  # Normalizar filas para que sumen 1
        
        # 3. Inicializar parámetros de emisión (medias y covarianzas)
        means = np.zeros((self.n_estados, self.n_coeficientes))  # Medias
        covs = np.array([np.eye(self.n_coeficientes)] * self.n_estados)  # Covarianzas
        
        # 4. Entrenamiento simplificado (Baum-Welch real sería más complejo)
        for _ in range(10):  # 10 iteraciones EM (en realidad hasta convergencia)
            # Aquí iría el cálculo real de gamma y xi en Baum-Welch
            # Simplificación: ajuste aleatorio controlado
            means += np.random.randn(*means.shape) * 0.1  # Pequeño cambio en medias
            for i in range(self.n_estados):
                # Ajustar covarianzas (diagonal)
                covs[i] = np.diag(np.random.rand(self.n_coeficientes) * 2 + 0.5)
        
        # 5. Almacenar modelo entrenado
        self.modelos[palabra] = {'A': A, 'means': means, 'covs': covs}
        if palabra not in self.palabras:
            self.palabras.append(palabra)  # Registrar nueva palabra

    def calcular_log_verosimilitud(self, mfcc, modelo):
        """
        Calcula la verosimilitud logarítmica de una secuencia MFCC dado un modelo.
        
        Args:
            mfcc (np.array): Secuencia de vectores MFCC
            modelo (dict): Diccionario con parámetros del HMM
            
        Returns:
            float: Log-verosimilitud de la secuencia bajo el modelo
        """
        T = len(mfcc)  # Número de frames
        alpha = np.zeros((T, self.n_estados))  # Matriz alfa para algoritmo forward
        
        # Inicialización (t=0)
        for s in range(self.n_estados):
            # Probabilidad inicial usando distribución gaussiana
            alpha[0, s] = multivariate_normal.pdf(
                mfcc[0], 
                mean=modelo['means'][s], 
                cov=modelo['covs'][s]
            )
        
        # Paso forward (t=1 a T-1)
        for t in range(1, T):
            for s in range(self.n_estados):
                # Probabilidad de transición desde todos los estados
                trans_prob = alpha[t-1] @ modelo['A'][:, s]
                # Probabilidad de observación en estado s
                obs_prob = multivariate_normal.pdf(
                    mfcc[t],
                    mean=modelo['means'][s],
                    cov=modelo['covs'][s]
                )
                alpha[t, s] = obs_prob * trans_prob  # Combinación
        
        # Retornar log-verosimilitud (suma sobre estados finales)
        return np.log(alpha[-1].sum())

    def reconocer(self, señal_audio):
        """
        Identifica la palabra más probable en una señal de audio.
        
        Args:
            señal_audio (np.array): Señal de audio a reconocer
            
        Returns:
            str: Palabra reconocida (None si no hay modelos)
        """
        # Extraer características MFCC
        mfcc = self.extraer_mfcc(señal_audio)
        
        mejor_palabra = None
        mejor_score = -np.inf  # Inicializar con valor muy bajo
        
        # Evaluar contra todos los modelos entrenados
        for palabra in self.palabras:
            score = self.calcular_log_verosimilitud(mfcc, self.modelos[palabra])
            if score > mejor_score:
                mejor_score = score
                mejor_palabra = palabra
        
        return mejor_palabra

# Bloque principal de ejecución
if __name__ == "__main__":
    # 1. Instanciar reconocedor
    reconocedor = HMM_ReconocimientoVoz(n_estados=5)
    
    # 2. Simular datos de entrenamiento (en práctica serían audios reales)
    palabras = ["hola", "adiós", "computadora"]
    entrenamiento = {
        "hola": [np.random.randn(16000) for _ in range(10)],  # 10 ejemplos
        "adiós": [np.random.randn(15000) for _ in range(10)],
        "computadora": [np.random.randn(20000) for _ in range(10)]
    }
    
    # 3. Entrenar modelos para cada palabra
    for palabra in palabras:
        print(f"Entrenando modelo para: {palabra}")
        reconocedor.entrenar_modelo(palabra, entrenamiento[palabra])
    
    # 4. Probar reconocimiento con audio simulado
    prueba_audio = np.random.randn(17000)  # Señal de prueba
    palabra_reconocida = reconocedor.reconocer(prueba_audio)
    
    print(f"\nPalabra reconocida: {palabra_reconocida}")
    
    # 5. Visualización de parámetros de los modelos
    plt.figure(figsize=(10, 6))
    for palabra in palabras:
        # Graficar primer coeficiente MFCC por estado
        plt.plot(reconocedor.modelos[palabra]['means'][:, 0], label=palabra)
    
    plt.title("Evolución del primer coeficiente MFCC por estado")
    plt.xlabel("Estado HMM")
    plt.ylabel("Valor MFCC")
    plt.legend()
    plt.grid(True)
    plt.show()