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
    # Operadores (+, -, *, /, =, ==, !=, <=, >=, <, >)
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
        self.source_code = source_code  # Almacena el código fuente a analizar
        self.position = 0  # Inicializa la posición del cursor en el código fuente
        self.line = 1  # Inicializa el número de línea
        self.column = 1  # Inicializa el número de columna
        self.tokens: List[Token] = []  # Inicializa la lista donde se guardarán los tokens encontrados

    def tokenize(self) -> List[Token]:
        """
        Convierte el código fuente en una lista de tokens

        Returns:
            Lista de tokens reconocidos
        """
        while self.position < len(self.source_code):  # Itera sobre el código fuente hasta el final
            # Intenta hacer match con cada patrón de token
            matched = False  # Indica si se encontró un token para la posición actual

            for pattern, token_type in TOKEN_PATTERNS:  # Itera sobre los patrones de tokens definidos
                regex = re.compile(pattern)  # Compila la expresión regular del patrón
                match = regex.match(self.source_code, self.position)  # Intenta encontrar el patrón desde la posición actual

                if match:  # Si se encontró una coincidencia
                    value = match.group(0)  # Obtiene el valor del texto que coincide con el patrón
                    start_pos = (self.line, self.column)  # Guarda la posición inicial del token

                    # Actualiza la posición de línea y columna
                    lines = value.split('\n')  # Divide el valor del token por saltos de línea
                    if len(lines) > 1:  # Si el token contiene saltos de línea
                        self.line += len(lines) - 1  # Actualiza el número de línea
                        self.column = len(lines[-1]) + 1  # La columna es la longitud de la última línea + 1
                    else:
                        self.column += len(value)  # Si no hay saltos de línea, la columna se incrementa por la longitud del token

                    self.position = match.end()  # Avanza la posición del cursor al final del token encontrado

                    # Ignora comentarios y espacios en blanco
                    if token_type not in (TokenType.COMMENT, TokenType.WHITESPACE):  # Si el token no es un comentario o espacio
                        end_pos = (self.line, self.column - 1)  # Guarda la posición final del token
                        self.tokens.append((token_type, value, start_pos))  # Agrega el token a la lista de tokens

                    matched = True  # Marca que se encontró un token
                    break  # Sale del bucle interno (no necesita probar otros patrones)

            if not matched:  # Si no se encontró ningún token
                # Carácter no reconocido - error léxico
                error_char = self.source_code[self.position]  # Obtiene el carácter no reconocido
                error_pos = (self.line, self.column)  # Guarda la posición del error
                self.tokens.append((TokenType.ERROR, error_char, error_pos))  # Agrega un token de error a la lista
                self.position += 1  # Avanza el cursor una posición
                self.column += 1
        return self.tokens  # Devuelve la lista de tokens encontrados

    def print_tokens(self):
        """Muestra los tokens encontrados con formato"""
        print(f"{'TOKEN':<15} {'VALOR':<20} {'POSICIÓN':<10}")  # Imprime el encabezado de la tabla
        print("-" * 45)  # Imprime una línea separadora
        for token_type, value, (line, col) in self.tokens:  # Itera sobre la lista de tokens
            print(f"{token_type.name:<15} {repr(value):<20} ({line}:{col})")  # Imprime cada token con su tipo, valor y posición

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

    print("=== ANÁLISIS LÉXICO ===")  # Imprime un encabezado
    print("Código fuente:")  # Imprime una etiqueta
    print(SAMPLE_CODE)  # Imprime el código fuente a analizar

    # Crear lexer y analizar el código
    lexer = Lexer(SAMPLE_CODE)  # Crea una instancia del analizador léxico
    tokens = lexer.tokenize()  # Tokeniza el código fuente

    # Mostrar resultados
    print("\nTokens encontrados:")  # Imprime una etiqueta
    lexer.print_tokens()  # Imprime los tokens encontrados con formato

