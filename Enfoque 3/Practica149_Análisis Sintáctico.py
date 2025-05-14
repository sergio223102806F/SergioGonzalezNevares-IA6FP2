"""
ANALIZADOR SINTÁCTICO (PARSER) DESCENDENTE RECURSIVO
---------------------------------------------------
Omoimplementa peteĩ parser gramática simple de expresiones matemáticas-pe guarã,
ojekuaa hag̃ua umi mba'e oĩ vaiha sintaxis-pe.
"""

# ============ IMPORTACIONES ============
from typing import List, Tuple, Optional, Union  # Oimporta umi tipo oñeikotevẽva anotaciones de tipo-pe guarã
from enum import Enum, auto  # Oimporta Enum odefine hag̃ua umi token type

# ============ DEFINICIÓN DE TOKENS ============
class TokenType(Enum):
    """Umi token type-kuéra lexer ohechakuaáva"""
    NUMBER = auto()      # Pukukuekuehína
    PLUS = auto()        # Operador +
    MINUS = auto()       # Operador -
    MULT = auto()        # Operador *
    DIV = auto()         # Operador /
    LPAREN = auto()      # Paréntesis izquierdo (
    RPAREN = auto()      # Paréntesis derecho )
    EOF = auto()         # Pahaite entrada-pegua
    ERROR = auto()       # Token naiporãiva

# Estructura token-kuérape guarã (tipo, valor, posición)
Token = Tuple[TokenType, str, Tuple[int, int]]  # Odefine Token como peteĩ tupla orekóva TokenType, peteĩ cadena ha peteĩ tupla orekóva int

# ============ CLASE PARSER ============
class Parser:
    """Omoimplementa peteĩ parser descendente recursivo expresiones aritméticas-pe guarã"""

    def __init__(self, tokens: List[Token]):
        """
        Oinicializa parser umi token lista ndive

        Args:
            tokens: Token lista ojapo va'ekue lexer
        """
        self.tokens = tokens  # Oñongatu token lista
        self.current_token: Optional[Token] = None  # Oñongatu ko'ag̃agua token
        self.token_index = -1  # Oñepyrũ índice token -1-pe
        self.advance()  # Ocarga peteĩha token

        # Registro de errores
        self.errors: List[str] = []  # Oñongatu error kuéra ojejuhúva

    def advance(self) -> None:
        """Ohasa siguiente token-pe"""
        self.token_index += 1  # Ombohetave índice
        if self.token_index < len(self.tokens):  # Ohecha oĩpa token
            self.current_token = self.tokens[self.token_index]  # Omoassign siguiente token
        else:
            # Token EOF otermina vove umi token
            self.current_token = (TokenType.EOF, '', (-1, -1))  # Omoassign EOF token

    def eat(self, token_type: TokenType) -> None:
        """
        Overifica ha okonsumi peteĩ token oesperáva

        Args:
            token_type: Token tipo oesperáva

        Raises:
            SyntaxError: Ocurre ramo token ko'ag̃agua ndojoajúi upe oesperáva ndive
        """
        if self.current_token[0] == token_type:  # Ohecha token ko'ag̃agua ha'eha tipo oesperáva
            self.advance()  # Ohasa siguiente token-pe
        else:
            expected = token_type.name  # Oñongatu oesperáva token réra
            found = self.current_token[0].name  # Oñongatu token ojejuhu va'ekue réra
            line, col = self.current_token[2]  # Oñongatu línea ha columna ojejuhu haguépe error
            error_msg = f"Error sintáctico ({line}:{col})-pe: Oespera {expected}, ojejuhu {found}"  # Omoarma mensaje de error
            self.errors.append(error_msg)  # Oñeagrega error lista de errores-pe
            raise SyntaxError(error_msg)  # Olanza excepción SyntaxError

    def parse(self) -> Union[float, None]:
        """
        Oinicia análisis sintáctico

        Returns:
            Resultado expresión ramo ha'e válido, None oĩramo error
        """
        try:
            result = self.expr()  # Ocalcula resultado expresión
            
            # Ohecha ndopytái hague token oprocesa'ỹre
            if self.current_token[0] != TokenType.EOF:  # Ohecha opaite token oprocesapa
                self.errors.append(f"Error: Oĩ token adiciónal expresión rire")  # Oñeagrega error lista de errores-pe
                return None  # Odevuelve None oĩramo error
                
            return result  # Odevuelve resultado
        except SyntaxError:
            return None  # Odevuelve None oĩramo error

    def expr(self) -> float:
        """
        Omaneja expresión suma ha resta rehegua

        Regla gramatical:
            expr : term ((PLUS | MINUS) term)*
        """
        result = self.term()  # Ocalcula peteĩha término
        
        while self.current_token[0] in (TokenType.PLUS, TokenType.MINUS):  # Oitera mientra oĩ + o -
            op = self.current_token  # Oñongatu operador
            if op[0] == TokenType.PLUS:
                self.eat(TokenType.PLUS)  # Okonsumi + token
                result += self.term()  # Osuma siguiente término
            elif op[0] == TokenType.MINUS:
                self.eat(TokenType.MINUS)  # Okonsumi - token
                result -= self.term()  # Oresta siguiente término
                
        return result  # Odevuelve resultado

    def term(self) -> float:
        """
        Omaneja término multiplicación ha división rehegua

        Regla gramatical:
            term : factor ((MULT | DIV) factor)*
        """
        result = self.factor()  # Ocalcula peteĩha factor
        
        while self.current_token[0] in (TokenType.MULT, TokenType.DIV):  # Oitera mientra oĩ * o /
            op = self.current_token  # Oñongatu operador
            if op[0] == TokenType.MULT:
                self.eat(TokenType.MULT)  # Okonsumi * token
                result *= self.factor()  # Omultiplica siguiente factor
            elif op[0] == TokenType.DIV:
                self.eat(TokenType.DIV)  # Okonsumi / token
                divisor = self.factor()  # Ocalcula divisor
                if divisor == 0:  # Ohecha divisor ha'eha 0
                    line, col = self.current_token[2]  # Oñongatu línea ha columna
                    self.errors.append(f"Error ({line}:{col})-pe: Oñedividi 0 rupive")  # Oñeagrega error
                    raise SyntaxError("División por cero")  # Olanza error
                result /= divisor  # Odivide resultado divisor rupive
                
        return result  # Odevuelve resultado

    def factor(self) -> float:
        """
        Omaneha factor kuéra (número ha expresión paréntesis mbytépe)

        Regla gramatical:
            factor : NUMBER | LPAREN expr RPAREN
        """
        token = self.current_token  # Oñongatu ko'ag̃agua token
        
        if token[0] == TokenType.NUMBER:  # Ohecha token ha'eha NUMBER
            self.eat(TokenType.NUMBER)  # Okonsumi NUMBER token
            return float(token[1])  # Oconvierte valor token pukukuehupépe ha odevuelve
        elif token[0] == TokenType.LPAREN:  # Ohecha token ha'eha LPAREN
            self.eat(TokenType.LPAREN)  # Okonsumi LPAREN token
            result = self.expr()  # Ocalcula expresión paréntesis mbytépe
            self.eat(TokenType.RPAREN)  # Okonsumi RPAREN token
            return result  # Odevuelve resultado
        else:
            line, col = token[2]  # Oñongatu línea ha columna
            self.errors.append(f"Error ({line}:{col})-pe: Oespera número térã '('")  # Omoarma mensaje de error
            raise SyntaxError("Factor inválido")  # Olanza excepción

# ============ FUNCIÓN DE PRUEBA ============
def test_parser(expression: str):
    """Oprueba parser peteĩ expresión ome'ẽva ndive"""
    # Osimula peteĩ lexer simple ohupyty hag̃ua token kuéra
    tokens = []
    i = 0
    line = 1
    col = 1
    
    while i < len(expression):
        c = expression[i]
        
        # Oignora espacio kuéra
        if c.isspace():
            if c == '\n':
                line += 1
                col = 1
            else:
                col += 1
            i += 1
            continue
        
        # Oidentifica token kuéra
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
            # Ocaptura pukukuekuehupaite
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
    
    # Oñeagrega token EOF
    tokens.append((TokenType.EOF, '', (line, col)))
    
    # Ocrea ha oejecuta parser
    parser = Parser(tokens)
    result = parser.parse()
    
    # Ohechauka resultado kuéra
    print(f"\nExpresión: {expression}")
    if parser.errors:
        print("Ojejuhu error kuéra:")
        for error in parser.errors:
            print(f"  {error}")
    else:
        print(f"Resultado: {result}")

# ============ EJECUCIÓN ============
if __name__ == "__main__":
    print("=== PRUEBA KUÉRA PARSER-PEGUA ===")
    
    # Expresión prueba rehegua
    test_cases = [
        "2 + 3 * 4",        # Correcta
        "(2 + 3) * 4",      # Correcta paréntesis ndive
        "10 / (5 - 5)",     # División 0 rupive
        "3 + * 4",          # Error sintáctico
        "5 + 2)",            # Paréntesis desbalanceado
        "2 + 3 4",          # Token adicional
    ]
    
    for expr in test_cases:
        test_parser(expr)


