# -*- coding: utf-8 -*-  # Codificación de caracteres UTF-8

"""
Created on Wed Apr  9 14:24:39 2025

@author: elvin
"""

import numpy as np  # Importa NumPy para manejo de arreglos y cálculos numéricos
from pgmpy.models import DynamicBayesianNetwork as DBN  # Importa el modelo de Red Bayesiana Dinámica de pgmpy
from pgmpy.factors.discrete import TabularCPD  # Importa las distribuciones de probabilidad condicional tabulares
from pgmpy.inference import DBNInference  # Importa el motor de inferencia para DBNs
from collections import defaultdict  # Importa defaultdict para estructuras de datos con valores por defecto
import matplotlib.pyplot as plt  # Importa matplotlib para graficar y visualizar

class SpeechRecognitionCSP:  # Clase principal para el sistema de reconocimiento del habla
    def __init__(self, phonemes, words, transitions, observations):
        """
        Constructor de la clase:
        phonemes: Lista de fonemas posibles
        words: Diccionario {palabra: [secuencia de fonemas]}
        transitions: Probabilidades de transición entre fonemas
        observations: Probabilidades de emisión (fonema -> señal acústica)
        """
        self.phonemes = phonemes  # Guarda lista de fonemas
        self.words = words  # Guarda diccionario de palabras y fonemas
        self.transitions = transitions  # Guarda matriz de transiciones entre fonemas
        self.observations = observations  # Guarda probabilidades de observación

        # Crear mapeo de fonemas a índices para facilitar manejo en matrices
        self.state_map = {p:i for i,p in enumerate(phonemes)}
        # Crear mapeo de observaciones a índices
        self.obs_map = {o:i for i,o in enumerate(observations.keys())}

        # Construir el modelo DBN usando los datos proporcionados
        self.model = self.build_dbn_model()

    def build_dbn_model(self):
        """Construye el modelo DBN para reconocimiento del habla"""
        dbn = DBN()  # Crea instancia del modelo de red bayesiana dinámica

        # Añade nodos para dos pasos de tiempo: estados (S) y observaciones (O)
        dbn.add_nodes_from(['S_0', 'S_1', 'O_0', 'O_1'])

        # Añade las conexiones entre nodos según la estructura del DBN
        dbn.add_edge('S_0', 'S_1')  # Conexión entre estados consecutivos
        dbn.add_edge('S_0', 'O_0')  # Conexión entre estado y observación en t=0
        dbn.add_edge('S_1', 'O_1')  # Conexión entre estado y observación en t=1

        # Definir CPDs (Distribuciones de Probabilidad Condicional)

        # CPD para el estado inicial (distribución uniforme sobre todos los fonemas)
        start_cpd = TabularCPD(
            variable='S_0',
            variable_card=len(self.phonemes),
            values=[[1.0/len(self.phonemes)] for _ in self.phonemes],
            state_names={'S_0': self.phonemes}
        )

        # CPD para transiciones entre estados fonéticos
        trans_cpd = TabularCPD(
            variable='S_1',
            variable_card=len(self.phonemes),
            values=self.get_transition_matrix(),  # Matriz de transición generada dinámicamente
            evidence=['S_0'],  # Condicionado por el estado anterior
            evidence_card=[len(self.phonemes)],
            state_names={'S_1': self.phonemes, 'S_0': self.phonemes}
        )

        # CPD para las observaciones (emisiones acústicas)
        obs_cpd = TabularCPD(
            variable='O_0',
            variable_card=len(self.observations),  # Cantidad de observaciones posibles
            values=self.get_observation_matrix(),  # Matriz de observaciones generada dinámicamente
            evidence=['S_0'],  # Condicionado por el estado S_0
            evidence_card=[len(self.phonemes)],
            state_names={'O_0': list(self.observations.keys()), 
                         'S_0': self.phonemes}
        )

        # Añadir las CPDs al modelo DBN
        dbn.add_cpds(start_cpd, trans_cpd, obs_cpd)

        # Verifica que el modelo esté bien definido y consistente
        assert dbn.check_model(), "El modelo DBN no es válido"

        return dbn  # Devuelve el modelo construido

    def get_transition_matrix(self):
        """Genera matriz de transición entre fonemas"""
        trans_matrix = []  # Lista para contener las filas de la matriz

        for p1 in self.phonemes:  # Itera sobre cada fonema de origen
            row = []  # Fila de probabilidades de transición desde p1
            for p2 in self.phonemes:  # Itera sobre cada fonema de destino
                prob = self.transitions.get((p1, p2), 0.01)  # Busca la probabilidad o usa 0.01 (suavizado)
                row.append(prob)  # Añade la probabilidad a la fila
            row_sum = sum(row)  # Suma total para normalizar la fila
            trans_matrix.append([p/row_sum for p in row])  # Normaliza fila y añade a la matriz

        return np.array(trans_matrix).T.tolist()  # Transpone para pgmpy y convierte a lista

    def get_observation_matrix(self):
        """Genera matriz de emisión de observaciones"""
        obs_matrix = []  # Lista para almacenar filas de la matriz

        for p in self.phonemes:  # Itera sobre cada fonema
            row = []  # Fila para observaciones desde fonema p
            for o in self.observations:  # Itera sobre cada observación
                prob = self.observations[o].get(p, 0.01)  # Busca la probabilidad o usa 0.01 (suavizado)
                row.append(prob)  # Añade la probabilidad a la fila
            row_sum = sum(row)  # Suma total para normalizar
            obs_matrix.append([p/row_sum for p in row])  # Normaliza la fila y la añade

        return np.array(obs_matrix).T.tolist()  # Transpone para pgmpy y convierte a lista

    def recognize_speech(self, observation_sequence):
        """Realiza reconocimiento del habla usando inferencia en el DBN"""
        infer = DBNInference(self.model)  # Crea el objeto de inferencia para DBNs

        most_probable_sequence = []  # Almacena la secuencia más probable de fonemas
        posterior_probs = []  # Almacena las distribuciones de probabilidad posterior

        # Itera sobre la secuencia de observaciones acústicas
        for i, obs in enumerate(observation_sequence):
            ...
            # (el resto del código fue truncado en tu mensaje anterior)
