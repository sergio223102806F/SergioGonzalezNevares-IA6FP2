"""
ANÁLISIS DE AMBIGÜEDAD EN PROCESAMIENTO DE LENGUAJE NATURAL
----------------------------------------------------------
Este sistema identifica y clasifica diferentes tipos de ambigüedad en oraciones,
proporcionando explicaciones y posibles interpretaciones.
"""

# ============ IMPORTACIONES ============
from typing import List, Dict, Tuple, Set, Optional
from enum import Enum, auto
import re
import nltk
from nltk import CFG, ChartParser
from nltk.tree import Tree

# Descargar recursos necesarios de NLTK
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# ============ DEFINICIÓN DE TIPOS ============
class AmbiguityType(Enum):
    """Tipos de ambigüedad lingüística"""
    LEXICAL = auto()      # Palabras con múltiples significados
    ESTRUCTURAL = auto()  # Múltiples estructuras sintácticas
    DE_REFERENCIA = auto() # Pronombres/referencias ambiguas
    DE_ALCANCE = auto()   # Ambigüedad en alcance de operadores
    FONETICA = auto()     # Sonidos similares, significados diferentes

# Estructura para ambigüedades detectadas
Ambiguity = Dict[str, Union[str, AmbiguityType, List[str]]]

# ============ CLASE ANALIZADOR DE AMBIGÜEDAD ============
class AmbiguityAnalyzer:
    """Identifica y analiza ambigüedades en texto natural"""
    
    def __init__(self):
        # Gramáticas para ambigüedad estructural
        self.grammars = {
            'pp_attachment': self._build_pp_attachment_grammar(),
            'coordination': self._build_coordination_grammar()
        }
        self.parser = ChartParser(self.grammars['pp_attachment'])
        
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
        sentences = self._split_sentences(text)
        ambiguities = []
        
        for sentence in sentences:
            ambiguities.extend(self._check_lexical_ambiguity(sentence))
            ambiguities.extend(self._check_structural_ambiguity(sentence))
            ambiguities.extend(self._check_reference_ambiguity(sentence))
        
        return ambiguities
    
    def _split_sentences(self, text: str) -> List[str]:
        """Divide el texto en oraciones"""
        return nltk.sent_tokenize(text)
    
    def _tokenize(self, sentence: str) -> List[Tuple[str, str]]:
        """Tokeniza y etiqueta una oración"""
        tokens = nltk.word_tokenize(sentence)
        return nltk.pos_tag(tokens)
    
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
        """)
    
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
        """)
    
    def _check_lexical_ambiguity(self, sentence: str) -> List[Ambiguity]:
        """
        Detecta ambigüedad léxica (palabras con múltiples significados)
        
        Args:
            sentence: Oración a analizar
            
        Returns:
            Lista de ambigüedades léxicas detectadas
        """
        tokens = [word.lower() for word, _ in self._tokenize(sentence)]
        ambiguities = []
        
        for word in tokens:
            if word in self.ambiguous_words:
                ambiguity = {
                    'type': AmbiguityType.LEXICAL,
                    'word': word,
                    'sentence': sentence,
                    'interpretations': self.ambiguous_words[word],
                    'position': self._find_word_position(sentence, word)
                }
                ambiguities.append(ambiguity)
        
        return ambiguities
    
    def _check_structural_ambiguity(self, sentence: str) -> List[Ambiguity]:
        """
        Detecta ambigüedad estructural (múltiples parseos posibles)
        
        Args:
            sentence: Oración a analizar
            
        Returns:
            Lista de ambigüedades estructurales detectadas
        """
        ambiguities = []
        
        # Verificar ambigüedad de adjunción de PP
        if ' con ' in sentence or ' en ' in sentence:
            trees = list(self.parser.parse(sentence.split()))
            if len(trees) > 1:
                ambiguity = {
                    'type': AmbiguityType.ESTRUCTURAL,
                    'subtype': 'adjunción de PP',
                    'sentence': sentence,
                    'interpretations': [str(tree) for tree in trees],
                    'position': 'global'
                }
                ambiguities.append(ambiguity)
        
        # Verificar ambigüedad de coordinación
        if ' y ' in sentence or ' o ' in sentence:
            self.parser = ChartParser(self.grammars['coordination'])
            trees = list(self.parser.parse(sentence.split()))
            if len(trees) > 1:
                ambiguity = {
                    'type': AmbiguityType.ESTRUCTURAL,
                    'subtype': 'coordinación',
                    'sentence': sentence,
                    'interpretations': [str(tree) for tree in trees],
                    'position': 'global'
                }
                ambiguities.append(ambiguity)
        
        return ambiguities
    
    def _check_reference_ambiguity(self, sentence: str) -> List[Ambiguity]:
        """
        Detecta ambigüedad referencial (pronombres con posibles referentes múltiples)
        
        Args:
            sentence: Oración a analizar
            
        Returns:
            Lista de ambigüedades referenciales detectadas
        """
        ambiguities = []
        tagged = self._tokenize(sentence)
        
        # Buscar pronombres personales
        pronouns = [word for word, pos in tagged if pos in ['PRP', 'PRP$']]
        
        if len(pronouns) > 0:
            # En un análisis real, buscaríamos los posibles referentes
            possible_referents = self._find_possible_referents(sentence)
            
            if len(possible_referents) > 1:
                for pronoun in pronouns:
                    ambiguity = {
                        'type': AmbiguityType.DE_REFERENCIA,
                        'word': pronoun,
                        'sentence': sentence,
                        'interpretations': possible_referents,
                        'position': self._find_word_position(sentence, pronoun)
                    }
                    ambiguities.append(ambiguity)
        
        return ambiguities
    
    def _find_word_position(self, sentence: str, word: str) -> str:
        """Encuentra la posición aproximada de una palabra en la oración"""
        words = sentence.lower().split()
        if word in words:
            index = words.index(word) + 1
            return f"palabra {index} de {len(words)}"
        return "desconocida"
    
    def _find_possible_referents(self, sentence: str) -> List[str]:
        """
        Encuentra posibles referentes para pronombres (simplificado)
        
        Args:
            sentence: Oración a analizar
            
        Returns:
            Lista de posibles referentes
        """
        # En una implementación real, usaríamos análisis más sofisticado
        tagged = self._tokenize(sentence)
        nouns = [word for word, pos in tagged if pos.startswith('NN')]
        return nouns or ['referente desconocido']

# ============ VISUALIZACIÓN DE RESULTADOS ============
def print_ambiguities(ambiguities: List[Ambiguity]) -> None:
    """Muestra las ambigüedades detectadas de forma legible"""
    if not ambiguities:
        print("No se encontraron ambigüedades.")
        return
    
    print(f"\nSe encontraron {len(ambiguities)} ambigüedades:")
    for i, amb in enumerate(ambiguities, 1):
        print(f"\nAMBIGÜEDAD {i}:")
        print(f"Tipo: {amb['type'].name}")
        if 'subtype' in amb:
            print(f"Subtipo: {amb['subtype']}")
        print(f"Oración: {amb['sentence']}")
        if 'word' in amb:
            print(f"Palabra/frase ambigua: '{amb['word']}' (posición: {amb['position']})")
        print("Interpretaciones posibles:")
        for j, interp in enumerate(amb['interpretations'], 1):
            print(f"  {j}. {interp}")

# ============ EJEMPLO DE USO ============
if __name__ == "__main__":
    print("=== DEMOSTRACIÓN DE ANÁLISIS DE AMBIGÜEDAD ===")
    
    # Oraciones de ejemplo con diferentes tipos de ambigüedad
    sample_sentences = [
        "Vi al hombre con el telescopio",       # Ambigüedad estructural
        "El perro persiguió al gato y al ratón", # Ambigüedad de coordinación
        "Fui al banco a pedir un préstamo",      # Ambigüedad léxica
        "Juan le dijo a Pedro que él ganó",      # Ambigüedad referencial
        "Los cazadores cazaron osos con rifles"  # Ambigüedad de adjunción
    ]
    
    analyzer = AmbiguityAnalyzer()
    
    for sentence in sample_sentences:
        print(f"\nAnalizando oración: '{sentence}'")
        ambiguities = analyzer.analyze(sentence)
        print_ambiguities(ambiguities)