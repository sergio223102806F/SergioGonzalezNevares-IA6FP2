"""
ANALIZADOR SEMÁNTICO 
-------------------------------------------
Implementa un analizador semántico para un lenguaje simple que:
1. Verifica tipos de variables
2. Comprueba declaraciones antes de uso
3. Valida ámbito de variables
4. Detecta errores semánticos
"""

# ============ IMPORTACIONES ============
from typing import Dict, List, Tuple, Optional, Union
from enum import Enum

# ============ DEFINICIÓN DE TOKENS ============
class TokenType(Enum):
    """Tipos de tokens para nuestro lenguaje"""
    KEYWORD = auto()       # var, if, while, etc.
    IDENTIFIER = auto()    # Nombres de variables
    NUMBER = auto()        # Literales numéricos
    STRING = auto()        # Literales de cadena
    BOOL = auto()         # true, false
    OPERATOR = auto()      # +, -, *, /, ==, etc.
    DELIMITER = auto()     ; , ( ) { } 
    EOF = auto()           # Fin de archivo
    ERROR = auto()         # Token inválido

# ============ DEFINICIÓN DE TIPOS DE DATOS ============
class DataType(Enum):
    """Tipos de datos soportados"""
    INT = auto()        # Tipo entero
    FLOAT = auto()      # Tipo flotante
    STR = auto()        # Tipo cadena
    BOOL = auto()       # Tipo booleano
    VOID = auto()       # Sin tipo (para funciones)
    ERROR = auto()      # Tipo inválido

# ============ TABLA DE SÍMBOLOS ============
class SymbolTable:
    """Mantiene registro de variables y sus tipos"""
    
    def __init__(self):
        self.table: Dict[str, Dict[str, Union[DataType, str]] = {}
        self.scope_stack: List[str] = ["global"]  # Pila de ámbitos
        
    def enter_scope(self, scope_name: str) -> None:
        """Entra en un nuevo ámbito"""
        self.scope_stack.append(scope_name)
        
    def exit_scope(self) -> None:
        """Sale del ámbito actual"""
        if len(self.scope_stack) > 1:  # No podemos salir del ámbito global
            self.scope_stack.pop()
        
    def current_scope(self) -> str:
        """Obtiene el ámbito actual"""
        return self.scope_stack[-1]
        
    def add_symbol(self, name: str, symbol_type: DataType) -> bool:
        """
        Añade un símbolo a la tabla actual
        
        Args:
            name: Nombre del símbolo
            symbol_type: Tipo de dato
            
        Returns:
            True si se añadió, False si ya existía
        """
        current = self.current_scope()
        if name in self.table.get(current, {}):
            return False  # Símbolo ya existe
            
        if current not in self.table:
            self.table[current] = {}
            
        self.table[current][name] = {"type": symbol_type, "scope": current}
        return True
        
    def lookup(self, name: str) -> Optional[Dict[str, Union[DataType, str]]]:
        """
        Busca un símbolo en los ámbitos actuales
        
        Args:
            name: Nombre del símbolo a buscar
            
        Returns:
            Información del símbolo o None si no existe
        """
        # Busca desde el ámbito más interno al global
        for scope in reversed(self.scope_stack):
            if scope in self.table and name in self.table[scope]:
                return self.table[scope][name]
        return None

# ============ ANALIZADOR SEMÁNTICO ============
class SemanticAnalyzer:
    """Realiza análisis semántico del código"""
    
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors: List[str] = []
        self.current_function: Optional[str] = None
        
    def analyze(self, node: Dict) -> DataType:
        """
        Función principal que inicia el análisis
        
        Args:
            node: Nodo raíz del AST
            
        Returns:
            Tipo de dato del nodo analizado
        """
        node_type = node.get("type")
        
        if node_type == "program":
            return self.analyze_program(node)
        elif node_type == "variable_declaration":
            return self.analyze_variable_declaration(node)
        elif node_type == "assignment":
            return self.analyze_assignment(node)
        elif node_type == "binary_operation":
            return self.analyze_binary_operation(node)
        elif node_type == "function_call":
            return self.analyze_function_call(node)
        elif node_type == "if_statement":
            return self.analyze_if_statement(node)
        elif node_type == "while_loop":
            return self.analyze_while_loop(node)
        elif node_type == "literal":
            return self.analyze_literal(node)
        elif node_type == "identifier":
            return self.analyze_identifier(node)
        else:
            self.error(f"Nodo desconocido: {node_type}", node)
            return DataType.ERROR
            
    def analyze_program(self, node: Dict) -> DataType:
        """Analiza un nodo de programa"""
        for statement in node["body"]:
            self.analyze(statement)
        return DataType.VOID
        
    def analyze_variable_declaration(self, node: Dict) -> DataType:
        """Analiza declaración de variables"""
        var_name = node["identifier"]
        var_type = self.get_type_from_string(node["data_type"])
        
        # Verifica si la variable ya existe
        if self.symbol_table.lookup(var_name):
            self.error(f"Variable '{var_name}' ya declarada", node)
            return DataType.ERROR
            
        # Añade a la tabla de símbolos
        if not self.symbol_table.add_symbol(var_name, var_type):
            self.error(f"No se pudo añadir variable '{var_name}'", node)
            return DataType.ERROR
            
        # Analiza la expresión de asignación si existe
        if "assignment" in node:
            expr_type = self.analyze(node["assignment"])
            if expr_type != var_type:
                self.error(f"Tipo incompatible para '{var_name}'. Esperaba {var_type}, obtuvo {expr_type}", node)
                
        return var_type
        
    def analyze_assignment(self, node: Dict) -> DataType:
        """Analiza asignación de variables"""
        var_name = node["left"]
        symbol = self.symbol_table.lookup(var_name)
        
        if not symbol:
            self.error(f"Variable '{var_name}' no declarada", node)
            return DataType.ERROR
            
        var_type = symbol["type"]
        expr_type = self.analyze(node["right"])
        
        if var_type != expr_type:
            self.error(f"Tipo incompatible en asignación. Esperaba {var_type}, obtuvo {expr_type}", node)
            return DataType.ERROR
            
        return var_type
        
    def analyze_binary_operation(self, node: Dict) -> DataType:
        """Analiza operaciones binarias"""
        left_type = self.analyze(node["left"])
        right_type = self.analyze(node["right"])
        op = node["operator"]
        
        # Comprobación de tipos
        if left_type != right_type:
            self.error(f"Tipos incompatibles en operación {op}: {left_type} y {right_type}", node)
            return DataType.ERROR
            
        # Comprobación de operadores válidos
        if op in ["+", "-", "*", "/"] and left_type not in [DataType.INT, DataType.FLOAT]:
            self.error(f"Operador {op} no válido para tipo {left_type}", node)
            return DataType.ERROR
        elif op in ["==", "!=", "<", ">"] and left_type == DataType.STR:
            self.error(f"Operador {op} no válido para cadenas", node)
            return DataType.ERROR
            
        # Tipo de retorno (bool para comparaciones, mismo tipo para aritméticas)
        return DataType.BOOL if op in ["==", "!=", "<", ">", "<=", ">="] else left_type
        
    def analyze_identifier(self, node: Dict) -> DataType:
        """Analiza referencias a variables"""
        var_name = node["name"]
        symbol = self.symbol_table.lookup(var_name)
        
        if not symbol:
            self.error(f"Variable '{var_name}' no declarada", node)
            return DataType.ERROR
            
        return symbol["type"]
        
    def get_type_from_string(self, type_str: str) -> DataType:
        """Convierte string a tipo de dato"""
        return {
            "int": DataType.INT,
            "float": DataType.FLOAT,
            "str": DataType.STR,
            "bool": DataType.BOOL,
            "void": DataType.VOID
        }.get(type_str, DataType.ERROR)
        
    def error(self, message: str, node: Dict) -> None:
        """Registra un error semántico"""
        line = node.get("line", "?")
        col = node.get("column", "?")
        self.errors.append(f"Error semántico en línea {line}, columna {col}: {message}")

# ============ EJEMPLO DE USO ============
if __name__ == "__main__":
    # AST de ejemplo (simplificado)
    sample_ast = {
        "type": "program",
        "body": [
            {
                "type": "variable_declaration",
                "identifier": "x",
                "data_type": "int",
                "assignment": {
                    "type": "literal",
                    "value": "5",
                    "data_type": "int",
                    "line": 1,
                    "column": 10
                },
                "line": 1,
                "column": 5
            },
            {
                "type": "variable_declaration",
                "identifier": "y",
                "data_type": "float",
                "line": 2,
                "column": 5
            },
            {
                "type": "assignment",
                "left": "y",
                "right": {
                    "type": "binary_operation",
                    "left": {
                        "type": "identifier",
                        "name": "x",
                        "line": 3,
                        "column": 9
                    },
                    "operator": "+",
                    "right": {
                        "type": "literal",
                        "value": "3.2",
                        "data_type": "float",
                        "line": 3,
                        "column": 13
                    },
                    "line": 3,
                    "column": 11
                },
                "line": 3,
                "column": 5
            },
            {
                "type": "if_statement",
                "condition": {
                    "type": "binary_operation",
                    "left": {
                        "type": "identifier",
                        "name": "x",
                        "line": 5,
                        "column": 9
                    },
                    "operator": ">",
                    "right": {
                        "type": "literal",
                        "value": "10",
                        "data_type": "int",
                        "line": 5,
                        "column": 13
                    },
                    "line": 5,
                    "column": 11
                },
                "body": [
                    {
                        "type": "assignment",
                        "left": "y",
                        "right": {
                            "type": "literal",
                            "value": "20.5",
                            "data_type": "float",
                            "line": 6,
                            "column": 15
                        },
                        "line": 6,
                        "column": 9
                    }
                ],
                "line": 5,
                "column": 5
            }
        ]
    }

    # Crear y ejecutar analizador semántico
    analyzer = SemanticAnalyzer()
    analyzer.analyze(sample_ast)
    
    # Mostrar resultados
    print("=== RESULTADOS DEL ANÁLISIS SEMÁNTICO ===")
    if analyzer.errors:
        print("\nErrores encontrados:")
        for error in analyzer.errors:
            print(f"- {error}")
    else:
        print("\nEl código es semánticamente válido")
    
    print("\nTabla de símbolos final:")
    for scope, symbols in analyzer.symbol_table.table.items():
        print(f"\nÁmbito: {scope}")
        for name, info in symbols.items():
            print(f"  {name}: {info['type'].name}")