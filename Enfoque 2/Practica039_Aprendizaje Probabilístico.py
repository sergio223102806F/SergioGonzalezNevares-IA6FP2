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
        for i, obs in enumerate(observation_sequence):
            if i == 0:
                # Paso inicial
                evidence = {'O_0': obs}
                posterior = infer.query(variables=['S_0'], evidence=evidence)
            else:
                # Pasos siguientes
                evidence = {'O_0': obs, 'O_1': obs}
                posterior = infer.query(variables=['S_1'], evidence=evidence)
            
            # Obtener el fonema más probable
            most_probable = posterior.state_names['S_0' if i == 0 else 'S_1'][
                np.argmax(posterior.values)
            ]
            most_probable_sequence.append(most_probable)
            
            # Guardar distribuciones posteriores
            posterior_probs.append({
                state: prob for state, prob in zip(
                    posterior.state_names['S_0' if i == 0 else 'S_1'],
                    posterior.values
                )
            })
        
        # Reconstruir palabras a partir de fonemas
        recognized_words = self.reconstruct_words(most_probable_sequence)
        
        return {
            'phoneme_sequence': most_probable_sequence,
            'recognized_words': recognized_words,
            'posterior_probs': posterior_probs
        }
    
    def reconstruct_words(self, phoneme_sequence):
        """Reconstruye palabras a partir de secuencia de fonemas"""
        current_word = []
        recognized_words = []
        
        for phoneme in phoneme_sequence:
            current_word.append(phoneme)
            
            # Verificar si la secuencia actual coincide con alguna palabra
            for word, word_phonemes in self.words.items():
                if current_word == word_phonemes:
                    recognized_words.append(word)
                    current_word = []
                    break
        
        return recognized_words

# Ejemplo de configuración para un sistema simple de reconocimiento de habla
def setup_speech_example():
    # Fonemas básicos
    phonemes = ['p', 'a', 't', 'e', 'l', 'o', 'm']
    
    # Palabras conocidas y su composición fonética
    words = {
        'pat': ['p', 'a', 't'],
        'tel': ['t', 'e', 'l'],
        'mal': ['m', 'a', 'l'],
        'pato': ['p', 'a', 't', 'o']
    }
    
    # Probabilidades de transición entre fonemas
    transitions = {
        # Transiciones dentro de palabras
        ('p', 'a'): 0.8, ('a', 't'): 0.7, ('t', 'o'): 0.6,
        ('t', 'e'): 0.7, ('e', 'l'): 0.8,
        ('m', 'a'): 0.9, ('a', 'l'): 0.7,
        
        # Transiciones entre palabras
        ('l', 'p'): 0.3, ('o', 'p'): 0.2, ('l', 'm'): 0.4
    }
    
    # Probabilidades de observación (señales acústicas -> fonemas)
    observations = {
        'obs1': {'p': 0.7, 't': 0.1, 'm': 0.2},
        'obs2': {'a': 0.8, 'e': 0.1, 'o': 0.1},
        'obs3': {'t': 0.7, 'p': 0.1, 'l': 0.2},
        'obs4': {'e': 0.6, 'a': 0.3, 'o': 0.1},
        'obs5': {'l': 0.8, 'p': 0.1, 'm': 0.1},
        'obs6': {'o': 0.9, 'a': 0.05, 'e': 0.05},
        'obs7': {'m': 0.7, 'p': 0.2, 't': 0.1}
    }
    
    return phonemes, words, transitions, observations

if __name__ == "__main__":
    # Configurar el ejemplo
    phonemes, words, transitions, observations = setup_speech_example()
    
    # Crear el reconocedor
    recognizer = SpeechRecognitionCSP(phonemes, words, transitions, observations)
    
    # Secuencia de observaciones (señales acústicas)
    observation_sequence = ['obs1', 'obs2', 'obs3', 'obs6']  # Correspondería a "pato"
    
    # Realizar reconocimiento
    result = recognizer.recognize_speech(observation_sequence)
    
    # Mostrar resultados
    print("Secuencia de fonemas inferida:", result['phoneme_sequence'])
    print("Palabras reconocidas:", result['recognized_words'])
    
    # Visualizar probabilidades posteriores
    print("\nProbabilidades posteriores:")
    for i, probs in enumerate(result['posterior_probs']):
        print(f"Paso {i+1}:")
        for phoneme, prob in probs.items():
            print(f"  P({phoneme}) = {prob:.3f}")
    
    # Visualización de la red (opcional)
    plt.figure(figsize=(10, 6))
    pos = {'S_0': (0, 1), 'S_1': (2, 1), 'O_0': (0, 0), 'O_1': (2, 0)}
    nx.draw(recognizer.model, pos, with_labels=True, node_size=3000, 
           node_color='skyblue', font_size=12, font_weight='bold', arrowsize=20)
    plt.title("Modelo DBN para Reconocimiento del Habla")
    plt.show()