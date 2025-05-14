"""
ANÁLISIS DE AMBIGÜEDAD EN PROCESAMIENTO DE LENGUAJE NATURAL
----------------------------------------------------------
Este sistema identifica y clasifica diferentes tipos de ambigüedad en oraciones,
proporcionando explicaciones y posibles interpretaciones.
"""

# ============ IMPORTACIONES ============
from typing import List, Dict, Tuple, Set, Optional # Importa tipos para anotación de tipos
from enum import Enum, auto # Importa Enum para definir tipos de ambigüedad
import re # Importa el módulo re para expresiones regulares (no se usa directamente en el código proporcionado pero puede ser útil para tareas relacionadas)
import nltk # Importa la biblioteca NLTK para procesamiento de lenguaje natural
from nltk import CFG, ChartParser # Importa CFG para gramáticas de contexto libre y ChartParser para el análisis sintáctico
from nltk.tree import Tree # Importa la clase Tree para representar árboles sintácticos

# Descargar recursos necesarios de NLTK
nltk.download('punkt') # Descarga el modelo Punkt para la tokenización de oraciones
nltk.download('averaged_perceptron_tagger') # Descarga el tagger Perceptron Promediado para el etiquetado de partes del habla

# ============ DEFINICIÓN DE TIPOS ============
class AmbiguityType(Enum):
    """Tipos de ambigüedad lingüística"""
    LEXICAL = auto()      # Palabras con múltiples significados
    STRUCTURAL = auto()    # Múltiples estructuras sintácticas
    DE_REFERENCIA = auto() # Pronombres/referencias ambiguas
    DE_ALCANCE = auto()    # Ambigüedad en alcance de operadores
    FONETICA = auto()      # Sonidos similares, significados diferentes

# Estructura para ambigüedades detectadas
Ambiguity = Dict[str, Union[str, AmbiguityType, List[str]]] # Define el tipo Ambiguity como un diccionario

# ============ CLASE ANALIZADOR DE AMBIGÜEDAD ============
class AmbiguityAnalyzer:
    """Identifica y analiza ambigüedades en texto natural"""
    
    def __init__(self):
        # Gramáticas para ambigüedad estructural
        self.grammars = {
            'pp_attachment': self._build_pp_attachment_grammar(), # Gramática para ambigüedad de adjunción de PP
            'coordination': self._build_coordination_grammar() # Gramática para ambigüedad de coordinación
        }
        self.parser = ChartParser(self.grammars['pp_attachment']) # Inicializa el parser con la gramática de adjunción de PP
        
        # Diccionario de palabras léxicamente ambiguas
        self.ambiguous_words = {
            'banco': ['entidad financiera', 'asiento', 'establecimiento'],
            'cura': ['sacerdote', 'tratamiento médico'],
            'llave': ['instrumento para abrir', 'llave de paso', 'llave mecánica']
        }
    
    def analyze(self, text: str) -> List[Ambiguity]:
        """
        Analiza un texto buscando diferentes tipos de ambigüedad
        
        Args:
            text: Texto a analizar
            
        Returns:
            Lista de ambigüedades detectadas
        """
        sentences = self._split_sentences(text) # Divide el texto en oraciones
        ambiguities = [] # Inicializa la lista de ambigüedades
        
        for sentence in sentences:
            ambiguities.extend(self._check_lexical_ambiguity(sentence)) # Busca ambigüedad léxica en la oración
            ambiguities.extend(self._check_structural_ambiguity(sentence)) # Busca ambigüedad estructural en la oración
            ambiguities.extend(self._check_reference_ambiguity(sentence)) # Busca ambigüedad de referencia en la oración
            
        return ambiguities # Devuelve la lista de ambigüedades
    
    def _split_sentences(self, text: str) -> List[str]:
        """Divide el texto en oraciones"""
        return nltk.sent_tokenize(text) # Usa el tokenizador de oraciones de NLTK
    
    def _tokenize(self, sentence: str) -> List[Tuple[str, str]]:
        """Tokeniza y etiqueta una oración"""
        tokens = nltk.word_tokenize(sentence) # Tokeniza la oración
        return nltk.pos_tag(tokens) # Etiqueta las partes del habla de los tokens
    
    def _build_pp_attachment_grammar(self) -> CFG:
        """Gramática para ambigüedad de adjunción de PP"""
        return CFG.fromstring("""
            S -> NP VP
            VP -> V NP | V NP PP
            PP -> P NP
            NP -> Det N | Det N PP
            Det -> 'el' | 'la' | 'un' | 'una'
            N -> 'hombre' | 'mujer' | 'telescopio' | 'perro'
            V -> 'vio' | 'observó' | 'pateó'
            P -> 'con' | 'en'
        """) # Define la gramática de contexto libre como una cadena
    
    def _build_coordination_grammar(self) -> CFG:
        """Gramática para ambigüedad de coordinación"""
        return CFG.fromstring("""
            S -> NP VP | S Conj S
            NP -> Det N | NP Conj NP
            VP -> V NP | VP Conj VP
            Det -> 'el' | 'la'
            N -> 'perro' | 'gato' | 'hueso'
            V -> 'persiguió' | 'comió'
            Conj -> 'y' | 'o'
        """) # Define la gramática de contexto libre para la coordinación
    
    def _check_lexical_ambiguity(self, sentence: str) -> List[Ambiguity]:
        """
        Detecta ambigüedad léxica (palabras con múltiples significados)
        
        Args:
            sentence: Oración a analizar
            
        Returns:
            Lista de ambigüedades léxicas detectadas
        """
        tokens = [word.lower() for word, _ in self._tokenize(sentence)] # Tokeniza la oración y convierte las palabras a minúsculas
        ambiguities = [] # Inicializa la lista de ambigüedades
        
        for word in tokens:
            if word in self.ambiguous_words: # Si la palabra está en el diccionario de palabras ambiguas
                ambiguity = {
                    'type': AmbiguityType.LEXICAL, # Tipo de ambigüedad: léxica
                    'word': word, # Palabra ambigua
                    'sentence': sentence, # Oración en la que aparece
                    'interpretations': self.ambiguous_words[word], # Posibles interpretaciones
                    'position': self._find_word_position(sentence, word) # Posición de la palabra en la oración
                }
                ambiguities.append(ambiguity) # Agrega la ambigüedad a la lista
                
        return ambiguities # Devuelve la lista de ambigüedades
    
    def _check_structural_ambiguity(self, sentence: str) -> List[Ambiguity]:
        """
        Detecta ambigüedad estructural (múltiples parseos posibles)
        
        Args:
            sentence: Oración a analizar
            
        Returns:
            Lista de ambigüedades estructurales detectadas
        """
        ambiguities = [] # Inicializa la lista de ambigüedades
        
        # Verificar ambigüedad de adjunción de PP
        if ' con ' in sentence or ' en ' in sentence: # Busca preposiciones comunes que causan ambigüedad de adjunción de PP
            trees = list(self.parser.parse(sentence.split())) # Parsea la oración usando la gramática de adjunción de PP
            if len(trees) > 1: # Si hay más de un árbol de análisis
                ambiguity = {
                    'type': AmbiguityType.STRUCTURAL, # Tipo de ambigüedad: estructural
                    'subtype': 'adjunción de PP', # Subtipo: adjunción de PP
                    'sentence': sentence, # Oración ambigua
                    'interpretations': [str(tree) for tree in trees], # Representaciones en cadena de los árboles de análisis
                    'position': 'global' # La ambigüedad afecta a toda la oración
                }
                ambiguities.append(ambiguity) # Agrega la ambigüedad a la lista
        
        # Verificar ambigüedad de coordinación
        if ' y ' in sentence or ' o ' in sentence: # Busca conjunciones comunes que causan ambigüedad de coordinación
            self.parser = ChartParser(self.grammars['coordination']) # Cambia el parser a la gramática de coordinación
            trees = list(self.parser.parse(sentence.split())) # Parsea la oración usando la gramática de coordinación
            if len(trees) > 1: # Si hay más de un árbol de análisis
                ambiguity = {
                    'type': AmbiguityType.STRUCTURAL, # Tipo de ambigüedad: estructural
                    'subtype': 'coordinación', # Subtipo: coordinación
                    'sentence': sentence, # Oración ambigua
                    'interpretations': [str(tree) for tree in trees], # Representaciones de los árboles
                    'position': 'global' # La ambigüedad es global
                }
                ambiguities.append(ambiguity) # Agrega la ambigüedad a la lista
                
        return ambiguities # Devuelve la lista de ambigüedades
    
    def _check_reference_ambiguity(self, sentence: str) -> List[Ambiguity]:
        """
        Detecta ambigüedad referencial (pronombres con posibles referentes múltiples)
        
        Args:
            sentence: Oración a analizar
            
        Returns:
            Lista de ambigüedades referenciales detectadas
        """
        ambiguities = [] # Inicializa la lista de ambigüedades
        tagged = self._tokenize(sentence) # Tokeniza y etiqueta la oración
        
        # Buscar pronombres personales
        pronouns = [word for word, pos in tagged if pos in ['PRP', 'PRP$']] # Encuentra pronombres personales y posesivos
        
        if len(pronouns) > 0: # Si se encuentran pronombres
            # En un análisis real, buscaríamos los posibles referentes
            possible_referents = self._find_possible_referents(sentence) # Encuentra los posibles referentes de los pronombres
            
            if len(possible_referents) > 1: # Si hay más de un referente posible
                for pronoun in pronouns: # Itera sobre los pronombres
                    ambiguity = {
                        'type': AmbiguityType.DE_REFERENCIA, # Tipo de ambigüedad: de referencia
                        'word': pronoun, # Pronombre ambiguo
                        'sentence': sentence, # Oración ambigua
                        'interpretations': possible_referents, # Posibles referentes
                        'position': self._find_word_position(sentence, pronoun) # Posición del pronombre
                    }
                    ambiguities.append(ambiguity) # Agrega la ambigüedad a la lista
                    
        return ambiguities # Devuelve la lista de ambigüedades
    
    def _find_word_position(self, sentence: str, word: str) -> str:
        """Encuentra la posición aproximada de una palabra en la oración"""
        words = sentence.lower().split() # Divide la oración en palabras y las convierte a minúsculas
        if word in words:
            index = words.index(word) + 1 # Encuentra el índice de la palabra
            return f"palabra {index} de {len(words)}" # Devuelve la posición de la palabra
        return "desconocida" # Si la palabra no se encuentra, devuelve "desconocida"
    
    def _find_possible_referents(self, sentence: str) -> List[str]:
        """
        Encuentra posibles referentes para pronombres (simplificado)
        
        Args:
            sentence: Oración a analizar
            
        Returns:
            Lista de posibles referentes
        """
        # En una implementación real, usaríamos análisis más sofisticado
        tagged = self._tokenize(sentence) # Tokeniza y etiqueta la oración
        nouns = [word for word, pos in tagged if pos.startswith('NN')] # Encuentra sustantivos
        return nouns or ['referente desconocido'] # Devuelve los sustantivos o "referente desconocido" si no hay sustantivos

# ============ VISUALIZACIÓN DE RESULTADOS ============
def print_ambiguities(ambiguities: List[Ambiguity]) -> None:
    """Muestra las ambigüedades detectadas de forma legible"""
    if not ambiguities: # Si no hay ambigüedades
        print("No se encontraron ambigüedades.") # Imprime un mensaje
        return
    
    print(f"\nSe encontraron {len(ambiguities)} ambigüedades:") # Imprime el número de ambigüedades encontradas
    for i, amb in enumerate(ambiguities, 1): # Itera sobre las ambigüedades
        print(f"\nAMBIGÜEDAD {i}:") # Imprime el número de la ambigüedad
        print(f"Tipo: {amb['type'].name}") # Imprime el tipo de ambigüedad
        if 'subtype' in amb: # Si hay un subtipo
            print(f"Subtipo: {amb['subtype']}") # Imprime el subtipo
        print(f"Oración: {amb['sentence']}") # Imprime la oración
        if 'word' in amb: # Si hay una palabra ambigua
            print(f"Palabra/frase ambigua: '{amb['word']}' (posición: {amb['position']})") # Imprime la palabra y su posición
        print("Interpretaciones posibles:") # Imprime las posibles interpretaciones
        for j, interp in enumerate(amb['interpretations'], 1): # Itera sobre las interpretaciones
            print(f"  {j}. {interp}") # Imprime cada interpretación

# ============ EJEMPLO DE USO ============
if __name__ == "__main__":
    print("=== DEMOSTRACIÓN DE ANÁLISIS DE AMBIGÜEDAD ===")
    
    # Oraciones de ejemplo con diferentes tipos de ambigüedad
    sample_sentences = [
        "Vi al hombre con el telescopio",        # Ambigüedad estructural
        "El perro persiguió al gato y al ratón", # Ambigüedad de coordinación
        "Fui al banco a pedir un préstamo",      # Ambigüedad léxica
        "Juan le dijo a Pedro que él ganó",      # Ambigüedad referencial
        "Los cazadores cazaron osos con rifles"  # Ambigüedad de adjunción
    ]
    
    analyzer = AmbiguityAnalyzer() # Crea una instancia del analizador de ambigüedad
    
    for sentence in sample_sentences: # Itera sobre las oraciones de ejemplo
        print(f"\nAnalizando oración: '{sentence}'") # Imprime la oración que se está analizando
        ambiguities = analyzer.analyze(sentence) # Analiza la oración
        print_ambiguities(ambiguities) # Imprime las ambigüedades encontradas
