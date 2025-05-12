# -*- coding: utf-8 -*-                                                     # Define la codificación de caracteres del archivo como UTF-8
"""
Created on Sat Apr 26 18:14:49 2025                                         # Indica la fecha y hora de creación del archivo
                                                                           #
@author: elvin                                                              # Define el autor del archivo
"""

# Import required libraries                                               # Comentario general sobre las importaciones
from collections import defaultdict  # For dictionary with default values   # Importa defaultdict para diccionarios con valores predeterminados
import numpy as np  # For probability calculations and random sampling    # Importa NumPy para cálculos de probabilidad y muestreo aleatorio
import math  # For logarithmic operations                               # Importa la biblioteca math para operaciones logarítmicas

class LanguageModel:                                                      # Define una nueva clase llamada LanguageModel
    def __init__(self, n_gram=2):                                         # Define el constructor de la clase LanguageModel con un valor predeterminado
        """
        Initialize the language model with n-gram structure.              # Documentación del constructor
        Args:                                                               # Inicio de la sección de argumentos
            n_gram (int): The context window size (2 for bigrams, 3 for trigrams, etc.) # Descripción del argumento n_gram
        """
        self.n_gram = n_gram  # Store the n-gram size                       # Almacena el tamaño del n-gram
        # Dictionary to store counts of each n-gram (e.g., ('el', 'gato') -> 2) # Comentario sobre el diccionario de conteos de n-gramas
        self.counts = defaultdict(int)                                     # Inicializa un diccionario con valores predeterminados de 0 para los conteos de n-gramas
        # Dictionary to store counts of each context (n-1 words)          # Comentario sobre el diccionario de conteos de contexto
        self.context_counts = defaultdict(int)                              # Inicializa un diccionario con valores predeterminados de 0 para los conteos de contexto
        # Set to store unique vocabulary words                             # Comentario sobre el conjunto de vocabulario
        self.vocab = set()                                                  # Inicializa un conjunto vacío para almacenar las palabras únicas del vocabulario
        # Counter for total words processed (including start/end markers)  # Comentario sobre el contador de palabras totales
        self.total_words = 0                                              # Inicializa el contador de palabras totales en 0

    def preprocess(self, text):                                           # Define el método para preprocesar el texto
        """
        Process raw text into tokens with start/end markers.              # Documentación del método preprocess
        Args:                                                               # Inicio de la sección de argumentos
            text (str): Input sentence/phrase                             # Descripción del argumento text
        Returns:                                                            # Inicio de la sección de retorno
            list: Processed tokens with markers                            # Descripción del valor de retorno
        """
        # Convert to lowercase and split into words                      # Comentario sobre la conversión a minúsculas y división
        tokens = text.lower().split()                                      # Convierte el texto a minúsculas y lo divide en palabras
        # Add start markers (<s>) at beginning and end marker (</s>) at end # Comentario sobre la adición de marcadores de inicio y fin
        # Number of start markers depends on n-gram size (n-1 markers needed) # Comentario sobre el número de marcadores de inicio
        return ['<s>']*(self.n_gram-1) + tokens + ['</s>']                 # Agrega marcadores de inicio, los tokens y el marcador de fin

    def train(self, corpus):                                               # Define el método para entrenar el modelo
        """
        Train the model on a text corpus by counting n-gram frequencies.  # Documentación del método train
        Args:                                                               # Inicio de la sección de argumentos
            corpus (list): List of sentences/phrases                      # Descripción del argumento corpus
        """
        for text in corpus:  # Process each text in corpus                 # Itera sobre cada texto en el corpus
            tokens = self.preprocess(text)  # Tokenize with markers        # Preprocesa el texto para obtener los tokens con marcadores
            self.total_words += len(tokens)  # Update total word count    # Actualiza el contador total de palabras

            # Add all words to vocabulary                                # Comentario sobre la adición de palabras al vocabulario
            self.vocab.update(tokens)                                      # Agrega todas las palabras únicas de los tokens al vocabulario

            # Slide n-gram window through text                           # Comentario sobre el deslizamiento de la ventana n-grama
            for i in range(len(tokens) - self.n_gram + 1):                # Itera sobre los tokens con una ventana de tamaño n_gram
                # Extract n-word sequence                                # Comentario sobre la extracción de la secuencia de n palabras
                n_gram = tuple(tokens[i:i+self.n_gram])                     # Extrae una tupla de n palabras
                # Context is first n-1 words of n-gram                    # Comentario sobre la definición del contexto
                context = tuple(n_gram[:-1])                              # El contexto son las primeras n-1 palabras del n-grama

                # Increment count for this specific n-gram                # Comentario sobre el incremento del conteo del n-grama
                self.counts[n_gram] += 1                                  # Incrementa el conteo para este n-grama específico
                # Increment count for this context                        # Comentario sobre el incremento del conteo del contexto
                self.context_counts[context] += 1                         # Incrementa el conteo para este contexto

    def probability(self, word, context):                                # Define el método para calcular la probabilidad
        """
        Calculate P(word|context) with Laplace (add-1) smoothing.        # Documentación del método probability
        Args:                                                               # Inicio de la sección de argumentos
            word (str): Word to predict                                  # Descripción del argumento word
            context (tuple): Context words (n-1 words)                    # Descripción del argumento context
        Returns:                                                            # Inicio de la sección de retorno
            float: Probability estimate                                  # Descripción del valor de retorno
        """
        context = tuple(context)  # Ensure context is tuple               # Asegura que el contexto sea una tupla
        # Numerator: count of (context + word) + 1 for smoothing        # Comentario sobre el numerador con suavizado Laplace
        numerator = self.counts[context + (word,)] + 1                   # Calcula el numerador con suavizado Laplace (add-1)
        # Denominator: count of context + vocabulary size               # Comentario sobre el denominador
        denominator = self.context_counts[context] + len(self.vocab)     # Calcula el denominador (conteo del contexto + tamaño del vocabulario)
        return numerator / denominator                                   # Devuelve la probabilidad estimada

    def perplexity(self, test_corpus):                                   # Define el método para calcular la perplejidad
        """
        Evaluate model on test corpus using perplexity metric.          # Documentación del método perplexity
        Lower perplexity = better model performance.                      # Información sobre la interpretación de la perplejidad
        Args:                                                               # Inicio de la sección de argumentos
            test_corpus (list): List of test sentences                    # Descripción del argumento test_corpus
        Returns:                                                            # Inicio de la sección de retorno
            float: Perplexity score                                      # Descripción del valor de retorno
        """
        total_log_prob = 0  # Accumulator for log probabilities           # Inicializa el acumulador de log probabilidades
        test_word_count = 0  # Counter for words in test set              # Inicializa el contador de palabras en el conjunto de prueba

        for text in test_corpus:                                         # Itera sobre cada texto en el corpus de prueba
            tokens = self.preprocess(text)                               # Preprocesa el texto para obtener los tokens
            test_word_count += len(tokens)                               # Actualiza el contador de palabras del conjunto de prueba

            # Start predicting from nth word (after context)             # Comentario sobre el inicio de la predicción
            for i in range(self.n_gram-1, len(tokens)):                   # Itera sobre los tokens comenzando después del contexto inicial
                context = tokens[i-self.n_gram+1:i]                      # Obtiene la lista de palabras del contexto
                word = tokens[i]                                         # Obtiene la palabra actual a predecir
                # Add log probability to accumulator                     # Comentario sobre la adición de la log probabilidad
                total_log_prob += math.log(self.probability(word, context)) # Agrega la log probabilidad de la palabra dado el contexto al acumulador

        # Calculate perplexity: e^(-average log probability)             # Comentario sobre el cálculo de la perplejidad
        return math.exp(-total_log_prob / test_word_count)                 # Calcula y devuelve la perplejidad

    def generate_text(self, max_length=20):                              # Define el método para generar texto
        """
        Generate new text by sampling from the model's probability distribution. # Documentación del método generate_text
        Args:                                                               # Inicio de la sección de argumentos
            max_length (int): Maximum words to generate                   # Descripción del argumento max_length
        Returns:                                                            # Inicio de la sección de retorno
            str: Generated text                                          # Descripción del valor de retorno
        """
                                     # Comentario sobre la inicialización con marcadores de inicio
        text = ['<s>']*(self.n_gram-1)                                  # Inicializa la lista de texto con marcadores de inicio

        while len(text) < max_length + self.n_gram - 1:                 # Continúa hasta alcanzar la longitud máxima
            # Get last n-1 words as current context                      # Comentario sobre la obtención del contexto actual
            context = tuple(text[-(self.n_gram-1):])                     # Obtiene las últimas n-1 palabras como contexto

                   
            candidates = []                                              # Inicializa una lista para almacenar candidatos (palabra, probabilidad)
            for word in self.vocab:                                      # Itera sobre cada palabra en el vocabulario
                if context + (word,) in self.counts:                    # Verifica si el n-grama (contexto + palabra) existe en los conteos
                    prob = self.probability(word, context)              # Calcula la probabilidad de la palabra dado el contexto
                    candidates.append((word, prob))                      # Agrega la palabra y su probabilidad a la lista de candidatos

                                    # Comentario sobre la detención si no hay candidatos
            if not candidates:                                           # Si no hay candidatos para la siguiente palabra
                break                                                    # Detiene la generación

                                 # Comentario sobre la separación de palabras y probabilidades
            words, probs = zip(*candidates)                              # Separa las palabras y las probabilidades de la lista de candidatos
                              # Comentario sobre la normalización de las probabilidades
            probs = np.array(probs) / sum(probs)                         # Normaliza las probabilidades para que sumen 1

                           # Comentario sobre la selección aleatoria de la palabra
            word = np.random.choice(words, p=probs)                      # Selecciona aleatoriamente una palabra basada en su probabilidad

            text.append(word)                                            # Agrega la palabra generada al texto
                                   # Comentario sobre la detención si se genera el marcador de fin
            if word == '</s>':                                            # Si la palabra generada es el marcador de fin
                break                                                    # Detiene la generación

                               # Comentario sobre el retorno del texto generado sin marcadores
        if text[-1] == '</s>':                                            # Si el último token es el marcador de fin
            return ' '.join(text[self.n_gram-1:-1])                      # Devuelve el texto generado sin los marcadores de inicio y fin
        else:                                                            # Si no se generó el marcador de fin
            return ' '.join(text[self.n_gram-1:])                       # Devuelve el texto generado sin los marcadores de inicio

                                                      # Comentario sobre la demostración
if __name__ == "__main__":                                               # Asegura que el código dentro solo se ejecute si el script es el principal
                  # Comentario sobre los datos de entrenamiento de ejemplo
    corpus = [                                                           # Lista de frases en español sobre mascotas
        "el gato come pescado",
        "el perro come carne",
        "el gato bebe leche",
        "el perro bebe agua"
    ]

                                      # Comentario sobre la creación y entrenamiento del modelo bigrama
    print("Training bigram model...")                                  # Imprime un mensaje indicando el inicio del entrenamiento
    lm = LanguageModel(n_gram=2)                                      # Crea una instancia de la clase LanguageModel con n_gram=2 (bigrama)
    lm.train(corpus)                                                 # Entrena el modelo con el corpus de ejemplo

                                         # Comentario sobre la evaluación en una oración de prueba
    test_text = ["el gato bebe agua"]                                  # Oración de prueba
    print(f"Perplexity on test text: {lm.perplexity(test_text):.2f}") # Calcula e imprime la perplejidad en el texto de prueba

                                                 # Comentario sobre la generación de texto nuevo
    print("Generated example:", lm.generate_text())                   # Genera e imprime un ejemplo de texto generado por el modelo