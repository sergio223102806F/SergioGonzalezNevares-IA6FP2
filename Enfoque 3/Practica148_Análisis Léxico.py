"""
Implementa un analizador léxico básico que:
1. Identifica tokens en código fuente
2. Clasifica tokens según su tipo
3. Maneja errores léxicos
"""

# ============ IMPORTACIONES ============
import re  # Para expresiones regulares
from enum import Enum, auto  # Para tipos de tokens
from typing import List, Tuple, Optional  # Para anotaciones de tipo

# ============ DEFINICIÓN DE TIPOS ============
class TokenType(Enum):
    """Enumeración de tipos de tokens"""
    # Palabras clave
    KEYWORD = auto()
    # Identificadores
    IDENTIFIER = auto()
    # Literales
    NUMBER = auto()
    STRING = auto()
    # Operadores
    OPERATOR = auto()
    # Delimitadores
    DELIMITER = auto()
    # Comentarios
    COMMENT = auto()
    # Espacios
    WHITESPACE = auto()
    # Errores
    ERROR = auto()

# Tipo para representar un token (tipo, valor, posición)
Token = Tuple[TokenType, str, Tuple[int, int]]

# ============ CONFIGURACIÓN DEL LEXER ============
# Expresiones regulares para cada tipo de token
TOKEN_PATTERNS = [
    # Comentarios (// o /* */)
    (r'//.*|/\*[\s\S]*?\*/', TokenType.COMMENT),
    # Palabras clave (if, else, while, etc.)
    (r'\b(if|else|while|for|return|function|var|let|const)\b', TokenType.KEYWORD),
    # Números (enteros y decimales)
    (r'\b\d+(\.\d+)?\b', TokenType.NUMBER),
    # Strings (comillas simples o dobles)
    (r'"[^"]*"|\'[^\']*\'', TokenType.STRING),
    # Operadores (+, -, *, /, =, ==, etc.)
    (r'[+\-*/%=]|==|!=|<=|>=|<|>', TokenType.OPERATOR),
    # Delimitadores (; , . ( ) { } [ ])
    (r'[;,\.\(\)\{\}\[\]]', TokenType.DELIMITER),
    # Identificadores (nombres de variables/funciones)
    (r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', TokenType.IDENTIFIER),
    # Espacios en blanco (ignorados)
    (r'\s+', TokenType.WHITESPACE),
]

# ============ CLASE LEXER ============
class Lexer:
    """Analizador léxico que convierte código fuente en tokens"""
    
    def __init__(self, source_code: str):
        """
        Inicializa el lexer con código fuente
        
        Args:
            source_code: Cadena con el código a analizar
        """
        self.source_code = source_code  # Almacena el código original
        self.position = 0  # Posición actual en el código
        self.line = 1  # Línea actual
        self.column = 1  # Columna actual
        self.tokens: List[Token] = []  # Lista de tokens encontrados
    
    def tokenize(self) -> List[Token]:
        """
        Convierte el código fuente en una lista de tokens
        
        Returns:
            Lista de tokens reconocidos
        """
        while self.position < len(self.source_code):
            # Intenta hacer match con cada patrón
            matched = False
            
            for pattern, token_type in TOKEN_PATTERNS:
                regex = re.compile(pattern)
                match = regex.match(self.source_code, self.position)
                
                if match:
                    value = match.group(0)
                    start_pos = (self.line, self.column)
                    
                    # Actualiza posición
                    lines = value.split('\n')
                    if len(lines) > 1:
                        self.line += len(lines) - 1
                        self.column = len(lines[-1]) + 1
                    else:
                        self.column += len(value)
                    
                    self.position = match.end()
                    
                    # Ignora comentarios y espacios
                    if token_type not in (TokenType.COMMENT, TokenType.WHITESPACE):
                        end_pos = (self.line, self.column - 1)
                        self.tokens.append((token_type, value, start_pos))
                    
                    matched = True
                    break
            
            if not matched:
                # Carácter no reconocido - error léxico
                error_char = self.source_code[self.position]
                error_pos = (self.line, self.column)
                self.tokens.append((TokenType.ERROR, error_char, error_pos))
                self.position += 1
                self.column += 1
        
        return self.tokens
    
    def print_tokens(self):
        """Muestra los tokens encontrados con formato"""
        print(f"{'TOKEN':<15} {'VALOR':<20} {'POSICIÓN':<10}")
        print("-" * 45)
        for token_type, value, (line, col) in self.tokens:
            print(f"{token_type.name:<15} {repr(value):<20} ({line}:{col})")

# ============ EJEMPLO DE USO ============
if __name__ == "__main__":
    # Código de ejemplo para analizar
    SAMPLE_CODE = """
    function factorial(n) {
        if (n <= 1) return 1;  // Caso base
        return n * factorial(n - 1);
    }
    
    /* Esto es un
       comentario multilínea */
    let num = 5;
    let result = factorial(num);
    """
    
    print("=== ANÁLISIS LÉXICO ===")
    print("Código fuente:")
    print(SAMPLE_CODE)
    
    # Crear lexer y analizar
    lexer = Lexer(SAMPLE_CODE)
    tokens = lexer.tokenize()
    
    # Mostrar resultados
    print("\nTokens encontrados:")
    lexer.print_tokens()
