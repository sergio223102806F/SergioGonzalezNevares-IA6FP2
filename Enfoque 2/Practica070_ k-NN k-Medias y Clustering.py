# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 16:31:15 2025

@author: elvin
"""

from collections import Counter
import numpy as np

class KNN:
    def __init__(self, k=3):
        self.k = k  # Número de vecinos a considerar
        
    def fit(self, X, y):
        self.X = X  # Guarda datos de entrenamiento
        self.y = y  # Guarda etiquetas
        
    def predict(self, X_new):
        preds = []
        for x in X_new:
            # Calcula distancias a todos los puntos
            dists = np.sqrt(np.sum((self.X - x)**2, axis=1))
            # Encuentra los k más cercanos
            k_indices = np.argsort(dists)[:self.k]
            # Toma la etiqueta más común
            pred = Counter(self.y[k_indices]).most_common(1)[0][0]
            preds.append(pred)
        return np.array(preds)