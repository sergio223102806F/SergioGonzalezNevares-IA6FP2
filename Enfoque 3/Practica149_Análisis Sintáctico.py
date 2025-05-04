"""
ANALIZADOR SINTÁCTICO (PARSER) DESCENDENTE RECURSIVO
---------------------------------------------------
Implementa un parser para una gramática simple de expresiones matemáticas
con detección de errores sintácticos.
"""

# ============ IMPORTACIONES ============
from typing import List, Tuple, Optional, Union
from enum import Enum

# ============ DEFINICIÓN DE TOKENS ============
class TokenType(Enum):
    """Tipos de tokens que reconoce el lexer"""
    NUMBER = auto()      # Números enteros
    PLUS = auto()        # Operador +
    MINUS = auto()       # Operador -
    MULT = auto()        # Operador *
    DIV = auto()         # Operador /
    LPAREN = auto()      # Paréntesis izquierdo (
    RPAREN = auto()      # Paréntesis derecho )
    EOF = auto()         # Fin de entrada
    ERROR = auto()       # Token inválido

# Estructura para tokens (tipo, valor, posición)
Token = Tuple[TokenType, str, Tuple[int, int]]

# ============ CLASE PARSER ============
class Parser:
    """Implementa un parser descendente recursivo para expresiones aritméticas"""
    
    def __init__(self, tokens: List[Token]):
        """
        Inicializa el parser con la lista de tokens
        
        Args:
            tokens: Lista de tokens generados por el lexer
        """
        self.tokens = tokens
        self.current_token: Optional[Token] = None
        self.token_index = -1
        self.advance()  # Carga el primer token
        
        # Registro de errores
        self.errors: List[str] = []
    
    def advance(self) -> None:
        """Avanza al siguiente token"""
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            # Token EOF cuando se acaban los tokens
            self.current_token = (TokenType.EOF, '', (-1, -1))
    
    def eat(self, token_type: TokenType) -> None:
        """
        Verifica y consume un token esperado
        
        Args:
            token_type: Tipo de token que se espera
            
        Raises:
            SyntaxError: Si el token actual no coincide con el esperado
        """
        if self.current_token[0] == token_type:
            self.advance()
        else:
            expected = token_type.name
            found = self.current_token[0].name
            line, col = self.current_token[2]
            error_msg = f"Error sintáctico en ({line}:{col}): Se esperaba {expected}, se encontró {found}"
            self.errors.append(error_msg)
            raise SyntaxError(error_msg)
    
    def parse(self) -> Union[float, None]:
        """
        Inicia el análisis sintáctico
        
        Returns:
            Resultado de la expresión si es válida, None si hay errores
        """
        try:
            result = self.expr()
            
            # Verifica que no queden tokens sin procesar
            if self.current_token[0] != TokenType.EOF:
                self.errors.append(f"Error: Tokens adicionales después de la expresión")
                return None
                
            return result
        except SyntaxError:
            return None
    
    def expr(self) -> float:
        """
        Maneja expresiones con suma y resta
        
        Grammar rule:
            expr : term ((PLUS | MINUS) term)*
        """
        result = self.term()
        
        while self.current_token[0] in (TokenType.PLUS, TokenType.MINUS):
            op = self.current_token
            if op[0] == TokenType.PLUS:
                self.eat(TokenType.PLUS)
                result += self.term()
            elif op[0] == TokenType.MINUS:
                self.eat(TokenType.MINUS)
                result -= self.term()
        
        return result
    
    def term(self) -> float:
        """
        Maneja términos con multiplicación y división
        
        Grammar rule:
            term : factor ((MULT | DIV) factor)*
        """
        result = self.factor()
        
        while self.current_token[0] in (TokenType.MULT, TokenType.DIV):
            op = self.current_token
            if op[0] == TokenType.MULT:
                self.eat(TokenType.MULT)
                result *= self.factor()
            elif op[0] == TokenType.DIV:
                self.eat(TokenType.DIV)
                divisor = self.factor()
                if divisor == 0:
                    line, col = self.current_token[2]
                    self.errors.append(f"Error en ({line}:{col}): División por cero")
                    raise SyntaxError("División por cero")
                result /= divisor
        
        return result
    
    def factor(self) -> float:
        """
        Maneja factores (números y expresiones entre paréntesis)
        
        Grammar rule:
            factor : NUMBER | LPAREN expr RPAREN
        """
        token = self.current_token
        
        if token[0] == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return float(token[1])
        elif token[0] == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            result = self.expr()
            self.eat(TokenType.RPAREN)
            return result
        else:
            line, col = token[2]
            self.errors.append(f"Error en ({line}:{col}): Se esperaba número o '('")
            raise SyntaxError("Factor inválido")

# ============ FUNCIÓN DE PRUEBA ============
def test_parser(expression: str):
    """Prueba el parser con una expresión dada"""
    # Simulamos un lexer simple para obtener tokens
    tokens = []
    i = 0
    line = 1
    col = 1
    
    while i < len(expression):
        c = expression[i]
        
        # Ignorar espacios
        if c.isspace():
            if c == '\n':
                line += 1
                col = 1
            else:
                col += 1
            i += 1
            continue
        
        # Identificar tokens
        if c == '+':
            tokens.append((TokenType.PLUS, c, (line, col)))
        elif c == '-':
            tokens.append((TokenType.MINUS, c, (line, col)))
        elif c == '*':
            tokens.append((TokenType.MULT, c, (line, col)))
        elif c == '/':
            tokens.append((TokenType.DIV, c, (line, col)))
        elif c == '(':
            tokens.append((TokenType.LPAREN, c, (line, col)))
        elif c == ')':
            tokens.append((TokenType.RPAREN, c, (line, col)))
        elif c.isdigit():
            # Capturar número completo
            num_str = ''
            start_col = col
            while i < len(expression) and expression[i].isdigit():
                num_str += expression[i]
                i += 1
                col += 1
            tokens.append((TokenType.NUMBER, num_str, (line, start_col)))
            continue
        else:
            tokens.append((TokenType.ERROR, c, (line, col)))
        
        i += 1
        col += 1
    
    # Añadir token EOF
    tokens.append((TokenType.EOF, '', (line, col)))
    
    # Crear y ejecutar parser
    parser = Parser(tokens)
    result = parser.parse()
    
    # Mostrar resultados
    print(f"\nExpresión: {expression}")
    if parser.errors:
        print("Errores encontrados:")
        for error in parser.errors:
            print(f"  {error}")
    else:
        print(f"Resultado: {result}")

# ============ EJECUCIÓN ============
if __name__ == "__main__":
    print("=== PRUEBAS DEL PARSER ===")
    
    # Expresiones de prueba
    test_cases = [
        "2 + 3 * 4",        # Correcta
        "(2 + 3) * 4",      # Correcta con paréntesis
        "10 / (5 - 5)",     # División por cero
        "3 + * 4",          # Error sintáctico
        "5 + 2)",           # Paréntesis desbalanceado
        "2 + 3 4",          # Tokens adicionales
    ]
    
    for expr in test_cases:
        test_parser(expr)

