# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 14:24:39 2025

@author: elvin
"""

import numpy as np                              # Importa NumPy para operaciones numéricas
from pgmpy.models import DynamicBayesianNetwork as DBN       # Importa modelo de Red Bayesiana Dinámica de pgmpy
from pgmpy.factors.discrete import TabularCPD              # Importa CPD para variables discretas
from pgmpy.inference import DBNInference                   # Importa clase para inferencia en DBNs
from collections import defaultdict                        # Importa defaultdict para estructuras de datos por defecto
import matplotlib.pyplot as plt                            # Importa matplotlib para visualización

class SpeechRecognitionCSP:                                # Clase para el sistema de reconocimiento de habla
    def __init__(self, phonemes, words, transitions, observations):
        """
        Constructor del reconocedor de voz
        phonemes: Lista de fonemas posibles
        words: Diccionario {palabra: [secuencia de fonemas]}
        transitions: Probabilidades de transición entre fonemas
        observations: Probabilidades de emisión (fonema -> señal acústica)
        """
        self.phonemes = phonemes                           # Guarda fonemas posibles
        self.words = words                                 # Guarda diccionario de palabras
        self.transitions = transitions                     # Guarda matriz de transición
        self.observations = observations                   # Guarda probabilidades de observación

        self.state_map = {p:i for i,p in enumerate(phonemes)}      # Mapeo fonema -> índice
        self.obs_map = {o:i for i,o in enumerate(observations.keys())} # Mapeo observación -> índice

        self.model = self.build_dbn_model()                # Construye el modelo DBN

    def build_dbn_model(self):                             # Método para construir el modelo DBN
        dbn = DBN()                                        # Crea una instancia del modelo DBN

        dbn.add_nodes_from(['S_0', 'S_1', 'O_0', 'O_1'])    # Añade nodos para dos pasos de tiempo (estados y observaciones)

        dbn.add_edge('S_0', 'S_1')                         # Conecta estado actual con siguiente
        dbn.add_edge('S_0', 'O_0')                         # Conecta estado con observación correspondiente
        dbn.add_edge('S_1', 'O_1')                         # Conecta siguiente estado con su observación

        start_cpd = TabularCPD(                            # CPD para estado inicial
            variable='S_0',
            variable_card=len(self.phonemes),              # Cantidad de fonemas posibles
            values=[[1.0/len(self.phonemes)] for _ in self.phonemes],  # Distribución uniforme inicial
            state_names={'S_0': self.phonemes}             # Nombres de estado legibles
        )

        trans_cpd = TabularCPD(                            # CPD para transición entre estados
            variable='S_1',
            variable_card=len(self.phonemes),              # Cantidad de fonemas
            values=self.get_transition_matrix(),           # Matriz de transición
            evidence=['S_0'],                              # Condicionado por estado anterior
            evidence_card=[len(self.phonemes)],            # Cardinalidad del estado anterior
            state_names={'S_1': self.phonemes, 'S_0': self.phonemes}
        )

        obs_cpd = TabularCPD(                              # CPD para observaciones (emisiones)
            variable='O_0',
            variable_card=len(self.observations),          # Cantidad de observaciones posibles
            values=self.get_observation_matrix(),          # Matriz de observación
            evidence=['S_0'],                              # Condicionado por estado
            evidence_card=[len(self.phonemes)],
            state_names={'O_0': list(self.observations.keys()), 
                         'S_0': self.phonemes}
        )

        dbn.add_cpds(start_cpd, trans_cpd, obs_cpd)        # Añade todas las CPDs al modelo

        assert dbn.check_model(), "El modelo DBN no es válido"  # Verifica consistencia del modelo

        return dbn                                         # Devuelve el modelo construido

    def get_transition_matrix(self):                       # Método para generar la matriz de transición
        trans_matrix = []                                  # Lista de filas de probabilidades
        for p1 in self.phonemes:                           # Para cada fonema origen
            row = []                                       # Fila de probabilidades hacia cada fonema destino
            for p2 in self.phonemes:                       # Para cada fonema destino
                prob = self.transitions.get((p1, p2), 0.01)  # Obtiene probabilidad o usa valor bajo por defecto
                row.append(prob)                           # Añade probabilidad a la fila
            row_sum = sum(row)                             # Suma para normalización
            trans_matrix.append([p/row_sum for p in row])  # Normaliza fila y añade a la matriz
        return np.array(trans_matrix).T.tolist()           # Transpone para formato de pgmpy y retorna

    def get_observation_matrix(self):                      # Método para generar la matriz de observación
        obs_matrix = []                                    # Lista de filas de probabilidades
        for p in self.phonemes:                            # Para cada fonema
            row = []                                       # Fila para observaciones
            for o in self.observations:                    # Para cada observación
                prob = self.observations[o].get(p, 0.01)   # Obtiene probabilidad o usa suavizado
                row.append(prob)                           # Añade a fila
            row_sum = sum(row)                             # Suma para normalizar
            obs_matrix.append([p/row_sum for p in row])    # Normaliza y añade fila
        return np.array(obs_matrix).T.tolist()             # Transpone y retorna matriz

    def recognize_speech(self, observation_sequence):      # Método para realizar reconocimiento de habla
        infer = DBNInference(self.model)                   # Crea objeto para inferencia en DBN

        most_probable_sequence = []                        # Lista para almacenar fonemas inferidos
        posterior_probs = []                               # Lista para almacenar distribuciones posteriores

        for i, obs in enumerate(observation_sequence):     # Itera sobre la secuencia de observaciones
            if i == 0:                                     # Paso inicial
                evidence = {'O_0': obs}                    # Evidencia en tiempo 0
                posterior = infer.query(variables=['S_0'], evidence=evidence)  # Inferencia sobre S_0
            else:                                          # Pasos siguientes
                evidence = {'O_0': obs, 'O_1': obs}        # Evidencia en ambos tiempos
                posterior = infer.query(variables=['S_1'], evidence=evidence)  # Inferencia sobre S_1

            most_probable = posterior.state_names['S_0' if i == 0 else 'S_1'][  # Encuentra fonema más probable
                np.argmax(posterior.values)
            ]
            most_probable_sequence.append(most_probable)   # Añade fonema a la secuencia

            posterior_probs.append({                       # Guarda la distribución posterior
                state: prob for state, prob in zip(
                    posterior.state_names['S_0' if i == 0 else 'S_1'],
                    posterior.values
                )
            })

        recognized_words = self.reconstruct_words(most_probable_sequence)  # Reconstruye palabras

        return {                                            # Devuelve resultados
            'phoneme_sequence': most_probable_sequence,
            'recognized_words': recognized_words,
            'posterior_probs': posterior_probs
        }

    def reconstruct_words(self, phoneme_sequence):          # Método para reconstruir palabras desde fonemas
        current_word = []                                   # Almacena fonemas actuales
        recognized_words = []                               # Lista de palabras reconocidas

        for phoneme in phoneme_sequence:                    # Itera sobre fonemas inferidos
            current_word.append(phoneme)                    # Añade fonema actual

            for word, word_phonemes in self.words.items():  # Verifica coincidencia con palabras conocidas
                if current_word == word_phonemes:
                    recognized_words.append(word)           # Si coincide, añade palabra reconocida
                    current_word = []                       # Reinicia palabra actual
                    break

        return recognized_words                             # Devuelve lista de palabras reconocidas

def setup_speech_example():                                # Función para configurar un ejemplo de prueba
    phonemes = ['p', 'a', 't', 'e', 'l', 'o', 'm']          # Lista de fonemas disponibles

    words = {                                               # Diccionario de palabras y sus fonemas
        'pat': ['p', 'a', 't'],
        'tel': ['t', 'e', 'l'],
        'mal': ['m', 'a', 'l'],
        'pato': ['p', 'a', 't', 'o']
    }

    transitions = {                                         # Probabilidades de transición entre fonemas
        ('p', 'a'): 0.8, ('a', 't'): 0.7, ('t', 'o'): 0.6,
        ('t', 'e'): 0.7, ('e', 'l'): 0.8,
        ('m', 'a'): 0.9, ('a', 'l'): 0.7,
        ('l', 'p'): 0.3, ('o', 'p'): 0.2, ('l', 'm'): 0.4
    }

    observations = {                                        # Probabilidades de observación (emisión)
        'obs1': {'p': 0.7, 't': 0.1, 'm': 0.2},
        'obs2': {'a': 0.8, 'e': 0.1, 'o': 0.1},
        'obs3': {'t': 0.7, 'p': 0.1, 'l': 0.2},
        'obs4': {'e': 0.6, 'a': 0.3, 'o': 0.1},
        'obs5': {'l': 0.8, 'p': 0.1, 'm': 0.1},
        'obs6': {'o': 0.9, 'a': 0.05, 'e': 0.05},
        'obs7': {'m': 0.7, 'p': 0.2, 't': 0.1}
    }

    return phonemes, words, transitions, observations       # Devuelve la configuración

if __name__ == "__main__":                                 # Bloque principal de ejecución
    phonemes, words, transitions, observations = setup_speech_example()  # Carga la configuración

    recognizer = SpeechRecognitionCSP(phonemes, words, transitions, observations)  # Instancia el reconocedor

    observation_sequence = ['obs1', 'obs2', 'obs3', 'obs6']  # Secuencia de observaciones acústicas (simulada)

    result = recognizer.recognize_speech(observation_sequence)  # Realiza inferencia sobre la secuencia

    print("Secuencia de fonemas inferida:", result['phoneme_sequence'])  # Muestra fonemas inferidos
    print("Palabras reconocidas:", result['recognized_words'])           # Muestra palabras reconocidas

    print("\nProbabilidades posteriores:")                                # Muestra probabilidades para cada paso
    for i, probs in enumerate(result['posterior_probs']):
        print(f"Paso {i+1}:")
        for phoneme, prob in probs.items():
            print(f"  P({phoneme}) = {prob:.3f}")

    plt.figure(figsize=(10, 6))                                           # Inicializa figura para graficar DBN
    pos = {'S_0': (0, 1), 'S_1': (2, 1), 'O_0': (0, 0), 'O_1': (2, 0)}     # Posiciones de nodos
    nx.draw(recognizer.model, pos, with_labels=True, node_size=3000,     # Dibuja el grafo DBN
           node_color='skyblue', font_size=12, font_weight='bold', arrowsize=20)
    plt.title("Modelo DBN para Reconocimiento del Habla")                # Título del gráfico
    plt.show()                                                           # Muestra la visualización
