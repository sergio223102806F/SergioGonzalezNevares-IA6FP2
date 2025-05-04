"""
GRAMÁTICA CAUSAL DEFINIDA (DCG) EN PYTHON
------------------------------------------
Implementación de un sistema de DCG para análisis de relaciones causales en lenguaje natural
con capacidades de parsing y generación de oraciones.
"""

# ============ IMPORTACIONES ============
from typing import List, Dict, Tuple, Optional, Set
from enum import Enum
import random

# ============ DEFINICIÓN DE TIPOS ============
class TokenType(Enum):
    """Tipos de tokens para el análisis léxico"""
    NOUN = auto()         # Sustantivos
    VERB = auto()         # Verbos
    CAUSAL_VERB = auto()  # Verbos causales (hacer, causar, provocar)
    ADJECTIVE = auto()    # Adjetivos
    PREPOSITION = auto()  # Preposiciones
    DETERMINER = auto()   # Artículos/determinantes
    CONJUNCTION = auto()  # Conjunciones
    PRONOUN = auto()      # Pronombres
    ADVERB = auto()       # Adverbios
    PUNCTUATION = auto()  # Signos de puntuación
    EOF = auto()          # Fin de entrada

# Estructura para tokens (tipo, valor, posición)
Token = Tuple[TokenType, str, Tuple[int, int]]

# ============ CLASE LEXER ============
class DcgLexer:
    """Analizador léxico para Gramáticas Causales Definidas"""
    
    # Diccionario de palabras clasificadas
    WORD_TYPES = {
        'causar': TokenType.CAUSAL_VERB,
        'provocar': TokenType.CAUSAL_VERB,
        'hacer': TokenType.CAUSAL_VERB,
        'el': TokenType.DETERMINER,
        'la': TokenType.DETERMINER,
        'los': TokenType.DETERMINER,
        'las': TokenType.DETERMINER,
        'que': TokenType.CONJUNCTION,
        'y': TokenType.CONJUNCTION,
        'o': TokenType.CONJUNCTION,
        'con': TokenType.PREPOSITION,
        'sin': TokenType.PREPOSITION,
        'por': TokenType.PREPOSITION,
        'rápidamente': TokenType.ADVERB,
        'lentamente': TokenType.ADVERB,
        '.': TokenType.PUNCTUATION,
        ',': TokenType.PUNCTUATION,
        ';': TokenType.PUNCTUATION
    }
    
    def __init__(self, text: str):
        """
        Inicializa el lexer con texto a analizar
        
        Args:
            text: Cadena de texto a tokenizar
        """
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def tokenize(self) -> List[Token]:
        """Convierte el texto en una lista de tokens"""
        while self.pos < len(self.text):
            current_char = self.text[self.pos]
            
            # Ignorar espacios en blanco
            if current_char.isspace():
                self._handle_whitespace(current_char)
                continue
                
            # Manejar signos de puntuación
            if current_char in {'.', ',', ';'}:
                self.tokens.append((TokenType.PUNCTUATION, current_char, (self.line, self.column)))
                self.pos += 1
                self.column += 1
                continue
                
            # Extraer palabras completas
            word = self._extract_word()
            
            # Clasificar la palabra
            token_type = self._classify_word(word)
            self.tokens.append((token_type, word, (self.line, self.column - len(word))))
            
        # Añadir token EOF
        self.tokens.append((TokenType.EOF, "", (self.line, self.column)))
        return self.tokens
    
    def _handle_whitespace(self, char: str) -> None:
        """Maneja caracteres de espacio en blanco"""
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.pos += 1
    
    def _extract_word(self) -> str:
        """Extrae una palabra completa del texto"""
        start_pos = self.pos
        while self.pos < len(self.text) and self.text[self.pos].isalpha():
            self.pos += 1
            self.column += 1
        return self.text[start_pos:self.pos].lower()
    
    def _classify_word(self, word: str) -> TokenType:
        """
        Clasifica una palabra según su tipo gramatical
        
        Args:
            word: Palabra a clasificar
            
        Returns:
            TokenType: Tipo gramatical de la palabra
        """
        # Verificar en el diccionario primero
        if word in self.WORD_TYPES:
            return self.WORD_TYPES[word]
            
        # Clasificación por sufijos (simplificada)
        if word.endswith(('ción', 'dad', 'ez')):  # Sustantivos comunes
            return TokenType.NOUN
        elif word.endswith(('ar', 'er', 'ir')):   # Verbos
            return TokenType.VERB
        elif word.endswith(('oso', 'able')):      # Adjetivos
            return TokenType.ADJECTIVE
            
        # Por defecto, considerar como sustantivo
        return TokenType.NOUN

# ============ CLASE PARSER DCG ============
class DcgParser:
    """Implementación de un parser para Gramáticas Causales Definidas"""
    
    def __init__(self, tokens: List[Token]):
        """
        Inicializa el parser con tokens
        
        Args:
            tokens: Lista de tokens generados por el lexer
        """
        self.tokens = tokens
        self.current_token: Optional[Token] = None
        self.token_index = -1
        self.advance()
        
        # Estructuras para almacenar relaciones causales
        self.causal_relations: List[Dict] = []
        self.errors: List[str] = []
    
    def advance(self) -> None:
        """Avanza al siguiente token"""
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = (TokenType.EOF, "", (-1, -1))
    
    def parse(self) -> bool:
        """
        Realiza el análisis sintáctico-semántico
        
        Returns:
            bool: True si el análisis fue exitoso
        """
        try:
            self.sentence()
            return True
        except SyntaxError:
            return False
    
    def sentence(self) -> None:
        """Analiza una oración completa"""
        # Oración simple: Sujeto + Verbo + Objeto
        subject = self.noun_phrase()
        verb = self.verb_phrase()
        obj = self.noun_phrase()
        
        # Verificar si es relación causal
        if verb[0] == TokenType.CAUSAL_VERB:
            self.causal_relations.append({
                'cause': subject[1],
                'effect': obj[1],
                'verb': verb[1],
                'position': (subject[2], obj[2])
            })
        
        # Manejar puntuación final
        if self.current_token[0] == TokenType.PUNCTUATION:
            self.advance()
        else:
            self.error("Se esperaba signo de puntuación")
    
    def noun_phrase(self) -> Token:
        """Analiza una frase nominal"""
        # Posible determinante
        if self.current_token[0] == TokenType.DETERMINER:
            determiner = self.current_token
            self.advance()
        else:
            determiner = None
        
        # Sustantivo principal
        noun = self.current_token
        if noun[0] not in (TokenType.NOUN, TokenType.PRONOUN):
            self.error("Se esperaba un sustantivo o pronombre")
        self.advance()
        
        # Posible adjetivo
        if self.current_token[0] == TokenType.ADJECTIVE:
            adjective = self.current_token
            self.advance()
        else:
            adjective = None
        
        # Devolver el núcleo nominal (simplificado)
        return noun
    
    def verb_phrase(self) -> Token:
        """Analiza una frase verbal"""
        verb = self.current_token
        if verb[0] not in (TokenType.VERB, TokenType.CAUSAL_VERB):
            self.error("Se esperaba un verbo")
        self.advance()
        
        # Posible adverbio
        if self.current_token[0] == TokenType.ADVERB:
            adverb = self.current_token
            self.advance()
        else:
            adverb = None
        
        return verb
    
    def error(self, message: str) -> None:
        """Registra un error de parsing"""
        line, col = self.current_token[2]
        self.errors.append(f"Error en ({line}:{col}): {message}")
        raise SyntaxError(message)

# ============ GENERADOR DE ORACIONES ============
class DcgGenerator:
    """Genera oraciones usando Gramáticas Causales Definidas"""
    
    def __init__(self):
        # Bases de conocimiento para generación
        self.nouns = ["lluvia", "sol", "estudio", "ejercicio", "comida"]
        self.causal_verbs = ["causa", "provoca", "genera", "produce"]
        self.effects = ["crecimiento", "enfermedad", "felicidad", "problemas"]
        self.adjectives = ["fuerte", "excesivo", "regular", "insuficiente"]
        self.determiners = ["el", "la", "un", "una"]
    
    def generate_sentence(self) -> str:
        """Genera una oración causal aleatoria"""
        structure = random.choice([
            self._generate_simple_causal,
            self._generate_complex_causal,
            self._generate_multi_effect
        ])
        return structure()
    
    def _generate_simple_causal(self) -> str:
        """Genera una relación causal simple"""
        subject = f"{random.choice(self.determiners)} {random.choice(self.nouns)}"
        verb = random.choice(self.causal_verbs)
        obj = f"{random.choice(self.determiners)} {random.choice(self.effects)}"
        return f"{subject} {verb} {obj}."
    
    def _generate_complex_causal(self) -> str:
        """Genera una relación causal con adjetivos"""
        subject = f"{random.choice(self.determiners)} {random.choice(self.adjectives)} {random.choice(self.nouns)}"
        verb = random.choice(self.causal_verbs)
        obj = f"{random.choice(self.determiners)} {random.choice(self.adjectives)} {random.choice(self.effects)}"
        return f"{subject} {verb} {obj}."
    
    def _generate_multi_effect(self) -> str:
        """Genera una relación causal con múltiples efectos"""
        subject = f"{random.choice(self.determiners)} {random.choice(self.nouns)}"
        verb = random.choice(self.causal_verbs)
        effect1 = random.choice(self.effects)
        effect2 = random.choice([e for e in self.effects if e != effect1])
        return f"{subject} {verb} {random.choice(self.determiners)} {effect1} y {random.choice(self.determiners)} {effect2}."

# ============ EJEMPLO DE USO ============
if __name__ == "__main__":
    print("=== DEMOSTRACIÓN DE GRAMÁTICA CAUSAL DEFINIDA ===")
    
    # Ejemplo de análisis
    sample_text = "El sol provoca el crecimiento. La lluvia excesiva causa problemas."
    
    print("\nAnálisis de texto:")
    print(f"Texto: '{sample_text}'")
    
    # Tokenización
    lexer = DcgLexer(sample_text)
    tokens = lexer.tokenize()
    print("\nTokens generados:")
    for token in tokens:
        print(f"{token[0].name:<12}: '{token[1]}' (Línea {token[2][0]}, Col {token[2][1]})")
    
    # Parsing
    parser = DcgParser(tokens)
    if parser.parse():
        print("\nRelaciones causales encontradas:")
        for rel in parser.causal_relations:
            print(f"- {rel['cause']} {rel['verb']} {rel['effect']}")
    else:
        print("\nErrores encontrados:")
        for error in parser.errors:
            print(f"- {error}")
    
    # Generación de oraciones
    generator = DcgGenerator()
    print("\nOraciones generadas:")
    for _ in range(3):
        print(f"- {generator.generate_sentence()}")