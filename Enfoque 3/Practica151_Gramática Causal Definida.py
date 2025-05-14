"""
GRAMÁTICA CAUSAL DEFINIDA (DCG) EN PYTHON
------------------------------------------
Implementación de un sistema de DCG para análisis de relaciones causales en lenguaje natural
con capacidades de parsing y generación de oraciones.
"""

# ============ IMPORTACIONES ============
from typing import List, Dict, Tuple, Optional, Set  # Tipos para type hints
from enum import Enum                                # Para enumeraciones
import random                                       # Para generación aleatoria

# ============ DEFINICIÓN DE TIPOS ============
class TokenType(Enum):                              # Enumeración de tipos de tokens
    """Tipos de tokens para el análisis léxico"""
    NOUN = auto()         # Sustantivos             # Categoría gramatical
    VERB = auto()         # Verbos                  # Categoría gramatical
    CAUSAL_VERB = auto()  # Verbos causales (hacer, causar, provocar) # Verbos especiales
    ADJECTIVE = auto()    # Adjetivos               # Categoría gramatical
    PREPOSITION = auto()  # Preposiciones           # Categoría gramatical
    DETERMINER = auto()   # Artículos/determinantes # Categoría gramatical
    CONJUNCTION = auto()  # Conjunciones            # Categoría gramatical
    PRONOUN = auto()      # Pronombres              # Categoría gramatical
    ADVERB = auto()       # Adverbios               # Categoría gramatical
    PUNCTUATION = auto()  # Signos de puntuación    # Puntuación
    EOF = auto()          # Fin de entrada          # Marcador final

# Estructura para tokens (tipo, valor, posición)
Token = Tuple[TokenType, str, Tuple[int, int]]     # Tipo de dato para tokens

# ============ CLASE LEXER ============
class DcgLexer:                                    # Analizador léxico
    """Analizador léxico para Gramáticas Causales Definidas"""
    
    # Diccionario de palabras clasificadas
    WORD_TYPES = {                                 # Palabras predefinidas
        'causar': TokenType.CAUSAL_VERB,          # Verbo causal
        'provocar': TokenType.CAUSAL_VERB,        # Verbo causal
        'hacer': TokenType.CAUSAL_VERB,           # Verbo causal
        'el': TokenType.DETERMINER,               # Determinante
        'la': TokenType.DETERMINER,               # Determinante
        'los': TokenType.DETERMINER,              # Determinante
        'las': TokenType.DETERMINER,              # Determinante
        'que': TokenType.CONJUNCTION,             # Conjunción
        'y': TokenType.CONJUNCTION,               # Conjunción
        'o': TokenType.CONJUNCTION,               # Conjunción
        'con': TokenType.PREPOSITION,             # Preposición
        'sin': TokenType.PREPOSITION,             # Preposición
        'por': TokenType.PREPOSITION,             # Preposición
        'rápidamente': TokenType.ADVERB,          # Adverbio
        'lentamente': TokenType.ADVERB,           # Adverbio
        '.': TokenType.PUNCTUATION,               # Puntuación
        ',': TokenType.PUNCTUATION,               # Puntuación
        ';': TokenType.PUNCTUATION                # Puntuación
    }
    
    def __init__(self, text: str):                # Constructor
        """
        Inicializa el lexer con texto a analizar
        
        Args:
            text: Cadena de texto a tokenizar      # Texto de entrada
        """
        self.text = text                          # Almacenar texto
        self.pos = 0                              # Posición actual
        self.line = 1                             # Línea actual
        self.column = 1                           # Columna actual
        self.tokens: List[Token] = []             # Lista de tokens
    
    def tokenize(self) -> List[Token]:            # Método principal
        """Convierte el texto en una lista de tokens"""
        while self.pos < len(self.text):          # Mientras haya texto
            current_char = self.text[self.pos]    # Carácter actual
            
            # Ignorar espacios en blanco
            if current_char.isspace():            # Si es espacio
                self._handle_whitespace(current_char) # Manejar espacio
                continue                          # Continuar
                
            # Manejar signos de puntuación
            if current_char in {'.', ',', ';'}:   # Si es puntuación
                self.tokens.append((TokenType.PUNCTUATION, current_char, (self.line, self.column))) # Añadir token
                self.pos += 1                     # Avanzar posición
                self.column += 1                  # Avanzar columna
                continue                         # Continuar
                
            # Extraer palabras completas
            word = self._extract_word()           # Obtener palabra
            
            # Clasificar la palabra
            token_type = self._classify_word(word) # Determinar tipo
            self.tokens.append((token_type, word, (self.line, self.column - len(word)))) # Añadir token
            
        # Añadir token EOF
        self.tokens.append((TokenType.EOF, "", (self.line, self.column))) # Añadir fin
        return self.tokens                        # Retornar tokens
    
    def _handle_whitespace(self, char: str) -> None: # Manejo de espacios
        """Maneja caracteres de espacio en blanco"""
        if char == '\n':                          # Si es salto de línea
            self.line += 1                        # Incrementar línea
            self.column = 1                       # Resetear columna
        else:                                     # Otro espacio
            self.column += 1                      # Incrementar columna
        self.pos += 1                             # Avanzar posición
    
    def _extract_word(self) -> str:               # Extracción de palabra
        """Extrae una palabra completa del texto"""
        start_pos = self.pos                      # Posición inicial
        while self.pos < len(self.text) and self.text[self.pos].isalpha(): # Mientras sea letra
            self.pos += 1                         # Avanzar posición
            self.column += 1                      # Avanzar columna
        return self.text[start_pos:self.pos].lower() # Retornar palabra en minúsculas
    
    def _classify_word(self, word: str) -> TokenType: # Clasificación
        """
        Clasifica una palabra según su tipo gramatical
        
        Args:
            word: Palabra a clasificar            # Palabra a clasificar
            
        Returns:
            TokenType: Tipo gramatical de la palabra # Tipo de token
        """
        # Verificar en el diccionario primero
        if word in self.WORD_TYPES:               # Si está predefinida
            return self.WORD_TYPES[word]           # Retornar tipo
            
        # Clasificación por sufijos (simplificada)
        if word.endswith(('ción', 'dad', 'ez')):  # Si termina como sustantivo
            return TokenType.NOUN                 # Retornar sustantivo
        elif word.endswith(('ar', 'er', 'ir')):   # Si termina como verbo
            return TokenType.VERB                 # Retornar verbo
        elif word.endswith(('oso', 'able')):      # Si termina como adjetivo
            return TokenType.ADJECTIVE            # Retornar adjetivo
            
        # Por defecto, considerar como sustantivo
        return TokenType.NOUN                     # Retornar sustantivo

# ============ CLASE PARSER DCG ============
class DcgParser:                                  # Analizador sintáctico
    """Implementación de un parser para Gramáticas Causales Definidas"""
    
    def __init__(self, tokens: List[Token]):      # Constructor
        """
        Inicializa el parser con tokens
        
        Args:
            tokens: Lista de tokens generados por el lexer # Tokens de entrada
        """
        self.tokens = tokens                      # Almacenar tokens
        self.current_token: Optional[Token] = None # Token actual
        self.token_index = -1                     # Índice actual
        self.advance()                            # Avanzar al primer token
        
        # Estructuras para almacenar relaciones causales
        self.causal_relations: List[Dict] = []    # Relaciones encontradas
        self.errors: List[str] = []               # Errores encontrados
    
    def advance(self) -> None:                    # Avanzar al siguiente token
        """Avanza al siguiente token"""
        self.token_index += 1                     # Incrementar índice
        if self.token_index < len(self.tokens):   # Si hay más tokens
            self.current_token = self.tokens[self.token_index] # Obtener token
        else:                                     # Si no hay más
            self.current_token = (TokenType.EOF, "", (-1, -1)) # Token EOF
    
    def parse(self) -> bool:                      # Método principal
        """
        Realiza el análisis sintáctico-semántico
        
        Returns:
            bool: True si el análisis fue exitoso # Resultado del análisis
        """
        try:                                     # Manejar errores
            self.sentence()                       # Analizar oración
            return True                           # Retornar éxito
        except SyntaxError:                       # Si hay error
            return False                          # Retornar fallo
    
    def sentence(self) -> None:                   # Análisis de oración
        """Analiza una oración completa"""
        # Oración simple: Sujeto + Verbo + Objeto
        subject = self.noun_phrase()              # Analizar sujeto
        verb = self.verb_phrase()                 # Analizar verbo
        obj = self.noun_phrase()                  # Analizar objeto
        
        # Verificar si es relación causal
        if verb[0] == TokenType.CAUSAL_VERB:      # Si es verbo causal
            self.causal_relations.append({        # Añadir relación
                'cause': subject[1],              # Causa
                'effect': obj[1],                # Efecto
                'verb': verb[1],                 # Verbo
                'position': (subject[2], obj[2])  # Posiciones
            })
        
        # Manejar puntuación final
        if self.current_token[0] == TokenType.PUNCTUATION: # Si hay puntuación
            self.advance()                         # Avanzar
        else:                                      # Si no hay
            self.error("Se esperaba signo de puntuación") # Error
    
    def noun_phrase(self) -> Token:                # Análisis de frase nominal
        """Analiza una frase nominal"""
        # Posible determinante
        if self.current_token[0] == TokenType.DETERMINER: # Si hay determinante
            determiner = self.current_token        # Obtener determinante
            self.advance()                        # Avanzar
        else:                                     # Si no hay
            determiner = None                     # Ningún determinante
        
        # Sustantivo principal
        noun = self.current_token                 # Obtener sustantivo
        if noun[0] not in (TokenType.NOUN, TokenType.PRONOUN): # Validar tipo
            self.error("Se esperaba un sustantivo o pronombre") # Error
        self.advance()                            # Avanzar
        
        # Posible adjetivo
        if self.current_token[0] == TokenType.ADJECTIVE: # Si hay adjetivo
            adjective = self.current_token        # Obtener adjetivo
            self.advance()                       # Avanzar
        else:                                    # Si no hay
            adjective = None                     # Ningún adjetivo
        
        # Devolver el núcleo nominal (simplificado)
        return noun                              # Retornar sustantivo
    
    def verb_phrase(self) -> Token:               # Análisis de frase verbal
        """Analiza una frase verbal"""
        verb = self.current_token                 # Obtener verbo
        if verb[0] not in (TokenType.VERB, TokenType.CAUSAL_VERB): # Validar tipo
            self.error("Se esperaba un verbo")     # Error
        self.advance()                            # Avanzar
        
        # Posible adverbio
        if self.current_token[0] == TokenType.ADVERB: # Si hay adverbio
            adverb = self.current_token           # Obtener adverbio
            self.advance()                        # Avanzar
        else:                                     # Si no hay
            adverb = None                        # Ningún adverbio
        
        return verb                               # Retornar verbo
    
    def error(self, message: str) -> None:        # Manejo de errores
        """Registra un error de parsing"""
        line, col = self.current_token[2]         # Obtener posición
        self.errors.append(f"Error en ({line}:{col}): {message}") # Añadir error
        raise SyntaxError(message)                # Lanzar excepción

# ============ GENERADOR DE ORACIONES ============
class DcgGenerator:                               # Generador de oraciones
    """Genera oraciones usando Gramáticas Causales Definidas"""
    
    def __init__(self):                           # Constructor
        # Bases de conocimiento para generación
        self.nouns = ["lluvia", "sol", "estudio", "ejercicio", "comida"] # Sustantivos
        self.causal_verbs = ["causa", "provoca", "genera", "produce"]    # Verbos causales
        self.effects = ["crecimiento", "enfermedad", "felicidad", "problemas"] # Efectos
        self.adjectives = ["fuerte", "excesivo", "regular", "insuficiente"] # Adjetivos
        self.determiners = ["el", "la", "un", "una"]                      # Determinantes
    
    def generate_sentence(self) -> str:           # Generación de oración
        """Genera una oración causal aleatoria"""
        structure = random.choice([               # Elegir estructura aleatoria
            self._generate_simple_causal,         # Estructura simple
            self._generate_complex_causal,        # Estructura compleja
            self._generate_multi_effect           # Múltiples efectos
        ])
        return structure()                        # Retornar oración generada
    
    def _generate_simple_causal(self) -> str:     # Generación simple
        """Genera una relación causal simple"""
        subject = f"{random.choice(self.determiners)} {random.choice(self.nouns)}" # Sujeto
        verb = random.choice(self.causal_verbs)   # Verbo
        obj = f"{random.choice(self.determiners)} {random.choice(self.effects)}" # Objeto
        return f"{subject} {verb} {obj}."         # Retornar oración
    
    def _generate_complex_causal(self) -> str:    # Generación compleja
        """Genera una relación causal con adjetivos"""
        subject = f"{random.choice(self.determiners)} {random.choice(self.adjectives)} {random.choice(self.nouns)}" # Sujeto con adjetivo
        verb = random.choice(self.causal_verbs)   # Verbo
        obj = f"{random.choice(self.determiners)} {random.choice(self.adjectives)} {random.choice(self.effects)}" # Objeto con adjetivo
        return f"{subject} {verb} {obj}."         # Retornar oración
    
    def _generate_multi_effect(self) -> str:      # Generación múltiple
        """Genera una relación causal con múltiples efectos"""
        subject = f"{random.choice(self.determiners)} {random.choice(self.nouns)}" # Sujeto
        verb = random.choice(self.causal_verbs)   # Verbo
        effect1 = random.choice(self.effects)     # Efecto 1
        effect2 = random.choice([e for e in self.effects if e != effect1]) # Efecto 2 diferente
        return f"{subject} {verb} {random.choice(self.determiners)} {effect1} y {random.choice(self.determiners)} {effect2}." # Retornar oración

# ============ EJEMPLO DE USO ============
if __name__ == "__main__":                       # Punto de entrada
    print("=== DEMOSTRACIÓN DE GRAMÁTICA CAUSAL DEFINIDA ===") # Título
    
    # Ejemplo de análisis
    sample_text = "El sol provoca el crecimiento. La lluvia excesiva causa problemas." # Texto de ejemplo
    
    print("\nAnálisis de texto:")                # Encabezado
    print(f"Texto: '{sample_text}'")             # Mostrar texto
    
    # Tokenización
    lexer = DcgLexer(sample_text)                # Crear lexer
    tokens = lexer.tokenize()                    # Tokenizar texto
    print("\nTokens generados:")                 # Encabezado
    for token in tokens:                         # Para cada token
        print(f"{token[0].name:<12}: '{token[1]}' (Línea {token[2][0]}, Col {token[2][1]})") # Mostrar token
    
    # Parsing
    parser = DcgParser(tokens)                   # Crear parser
    if parser.parse():                           # Si análisis exitoso
        print("\nRelaciones causales encontradas:") # Encabezado
        for rel in parser.causal_relations:      # Para cada relación
            print(f"- {rel['cause']} {rel['verb']} {rel['effect']}") # Mostrar relación
    else:                                        # Si hay errores
        print("\nErrores encontrados:")          # Encabezado
        for error in parser.errors:              # Para cada error
            print(f"- {error}")                  # Mostrar error
    
    # Generación de oraciones
    generator = DcgGenerator()                   # Crear generador
    print("\nOraciones generadas:")              # Encabezado
    for _ in range(3):                           # Generar 3 oraciones
        print(f"- {generator.generate_sentence()}") # Mostrar oración generada