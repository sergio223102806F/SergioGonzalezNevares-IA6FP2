# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 14:24:39 2025

@author: elvin
"""

import numpy as np
from pgmpy.models import DynamicBayesianNetwork as DBN
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import DBNInference
from collections import defaultdict
import matplotlib.pyplot as plt

class SpeechRecognitionCSP:
    def __init__(self, phonemes, words, transitions, observations):
        """
        phonemes: Lista de fonemas posibles
        words: Diccionario {palabra: [secuencia de fonemas]}
        transitions: Probabilidades de transición entre fonemas
        observations: Probabilidades de emisión (fonema -> señal acústica)
        """
        self.phonemes = phonemes
        self.words = words
        self.transitions = transitions
        self.observations = observations
        
        # Crear mapeos de estado
        self.state_map = {p:i for i,p in enumerate(phonemes)}
        self.obs_map = {o:i for i,o in enumerate(observations.keys())}
        
        # Construir el modelo DBN
        self.model = self.build_dbn_model()
    
    def build_dbn_model(self):
        """Construye el modelo DBN para reconocimiento del habla"""
        dbn = DBN()
        
        # Añadir nodos para cada paso de tiempo
        dbn.add_nodes_from(['S_0', 'S_1', 'O_0', 'O_1'])
        
        # Conexiones temporales
        dbn.add_edge('S_0', 'S_1')
        dbn.add_edge('S_0', 'O_0')
        dbn.add_edge('S_1', 'O_1')
        
        # Definir CPDs (Distribuciones de Probabilidad Condicional)
        # CPD para el estado inicial
        start_cpd = TabularCPD(
            variable='S_0',
            variable_card=len(self.phonemes),
            values=[[1.0/len(self.phonemes)] for _ in self.phonemes],
            state_names={'S_0': self.phonemes}
        )
        
        # CPD para transiciones entre estados
        trans_cpd = TabularCPD(
            variable='S_1',
            variable_card=len(self.phonemes),
            values=self.get_transition_matrix(),
            evidence=['S_0'],
            evidence_card=[len(self.phonemes)],
            state_names={'S_1': self.phonemes, 'S_0': self.phonemes}
        )
        
        # CPD para observaciones
        obs_cpd = TabularCPD(
            variable='O_0',
            variable_card=len(self.observations),
            values=self.get_observation_matrix(),
            evidence=['S_0'],
            evidence_card=[len(self.phonemes)],
            state_names={'O_0': list(self.observations.keys()), 
                        'S_0': self.phonemes}
        )
        
        # Añadir CPDs al modelo
        dbn.add_cpds(start_cpd, trans_cpd, obs_cpd)
        
        # Verificar modelo
        assert dbn.check_model(), "El modelo DBN no es válido"
        
        return dbn
    
    def get_transition_matrix(self):
        """Genera matriz de transición entre fonemas"""
        trans_matrix = []
        for p1 in self.phonemes:
            row = []
            for p2 in self.phonemes:
                # Probabilidad de transición p1 -> p2
                prob = self.transitions.get((p1, p2), 0.01)  # Suavizado
                row.append(prob)
            # Normalizar fila
            row_sum = sum(row)
            trans_matrix.append([p/row_sum for p in row])
        return np.array(trans_matrix).T.tolist()
    
    def get_observation_matrix(self):
        """Genera matriz de emisión de observaciones"""
        obs_matrix = []
        for p in self.phonemes:
            row = []
            for o in self.observations:
                # Probabilidad de observar o dado el fonema p
                prob = self.observations[o].get(p, 0.01)  # Suavizado
                row.append(prob)
            # Normalizar fila
            row_sum = sum(row)
            obs_matrix.append([p/row_sum for p in row])
        return np.array(obs_matrix).T.tolist()
    
    def recognize_speech(self, observation_sequence):
        """Realiza reconocimiento del habla usando inferencia en el DBN"""
        infer = DBNInference(self.model)
        
        # Almacenar resultados
        most_probable_sequence = []
        posterior_probs = []
        
        # Manejar cada observación en la secuencia
        for i, obs in enumerate(