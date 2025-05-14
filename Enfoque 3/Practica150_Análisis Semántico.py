# ============ IMPORTACIONES ============
from typing import Dict, List, Tuple, Optional, Union  # Tipos de datos para anotaciones
from enum import Enum  # Para definir enumeraciones

# ============ DEFINICIÓN DE TOKENS ============
class TokenType(Enum):  # Enumeración de tipos de tokens
    """Tipos de tokens para nuestro lenguaje"""
    KEYWORD = auto()       # Palabras clave como var, if, while
    IDENTIFIER = auto()    # Identificadores de variables o funciones
    NUMBER = auto()        # Literales numéricos
    STRING = auto()        # Literales de texto
    BOOL = auto()          # Literales booleanos
    OPERATOR = auto()      # Operadores matemáticos o lógicos
    DELIMITER = auto()     # Delimitadores como ; , ( ) { }
    EOF = auto()           # Fin de archivo
    ERROR = auto()         # Token inválido

# ============ DEFINICIÓN DE TIPOS DE DATOS ============
class DataType(Enum):  # Enumeración de tipos de datos
    """Tipos de datos soportados"""
    INT = auto()        # Entero
    FLOAT = auto()      # Flotante
    STR = auto()        # Cadena de texto
    BOOL = auto()       # Booleano
    VOID = auto()       # Sin valor (funciones)
    ERROR = auto()      # Tipo no válido

# ============ TABLA DE SÍMBOLOS ============
class SymbolTable:  # Representa la tabla de símbolos
    """Mantiene registro de variables y sus tipos"""
    
    def __init__(self):  # Constructor
        self.table: Dict[str, Dict[str, Union[DataType, str]]] = {}  # Tabla de símbolos por ámbito
        self.scope_stack: List[str] = ["global"]  # Pila de ámbitos iniciando en global
        
    def enter_scope(self, scope_name: str) -> None:  # Entrar a nuevo ámbito
        """Entra en un nuevo ámbito"""
        self.scope_stack.append(scope_name)  # Agrega a la pila
        
    def exit_scope(self) -> None:  # Salir del ámbito actual
        """Sale del ámbito actual"""
        if len(self.scope_stack) > 1:  # Evita eliminar el global
            self.scope_stack.pop()
        
    def current_scope(self) -> str:  # Obtener ámbito actual
        """Obtiene el ámbito actual"""
        return self.scope_stack[-1]  # Último en la pila
        
    def add_symbol(self, name: str, symbol_type: DataType) -> bool:  # Añadir símbolo
        """
        Añade un símbolo a la tabla actual
        """
        current = self.current_scope()  # Ámbito actual
        if name in self.table.get(current, {}):  # Ya existe
            return False  # No se puede añadir
            
        if current not in self.table:  # Crear entrada si no existe
            self.table[current] = {}
            
        self.table[current][name] = {"type": symbol_type, "scope": current}  # Añadir símbolo
        return True
        
    def lookup(self, name: str) -> Optional[Dict[str, Union[DataType, str]]]:  # Buscar símbolo
        """
        Busca un símbolo en los ámbitos actuales
        """
        for scope in reversed(self.scope_stack):  # Busca desde el más interno
            if scope in self.table and name in self.table[scope]:  # Si lo encuentra
                return self.table[scope][name]
        return None  # No encontrado

# ============ ANALIZADOR SEMÁNTICO ============
class SemanticAnalyzer:  # Clase para analizar semántica
    """Realiza análisis semántico del código"""
    
    def __init__(self):  # Constructor
        self.symbol_table = SymbolTable()  # Instancia de tabla de símbolos
        self.errors: List[str] = []  # Lista de errores encontrados
        self.current_function: Optional[str] = None  # Función actual (si aplica)
        
    def analyze(self, node: Dict) -> DataType:  # Analiza un nodo del AST
        """
        Función principal que inicia el análisis
        """
        node_type = node.get("type")  # Tipo de nodo
        
        if node_type == "program":  # Nodo raíz
            return self.analyze_program(node)
        elif node_type == "variable_declaration":  # Declaración de variable
            return self.analyze_variable_declaration(node)
        elif node_type == "assignment":  # Asignación
            return self.analyze_assignment(node)
        elif node_type == "binary_operation":  # Operación binaria
            return self.analyze_binary_operation(node)
        elif node_type == "function_call":  # Llamada a función
            return self.analyze_function_call(node)
        elif node_type == "if_statement":  # Sentencia if
            return self.analyze_if_statement(node)
        elif node_type == "while_loop":  # Bucle while
            return self.analyze_while_loop(node)
        elif node_type == "literal":  # Valor literal
            return self.analyze_literal(node)
        elif node_type == "identifier":  # Referencia a variable
            return self.analyze_identifier(node)
        else:  # Nodo no reconocido
            self.error(f"Nodo desconocido: {node_type}", node)
            return DataType.ERROR
            
    def analyze_program(self, node: Dict) -> DataType:  # Análisis del nodo program
        """Analiza un nodo de programa"""
        for statement in node["body"]:  # Analiza cada instrucción
            self.analyze(statement)
        return DataType.VOID  # No devuelve valor
        
    def analyze_variable_declaration(self, node: Dict) -> DataType:  # Declaración de variable
        """Analiza declaración de variables"""
        var_name = node["identifier"]  # Nombre de variable
        var_type = self.get_type_from_string(node["data_type"])  # Tipo de variable
        
        if self.symbol_table.lookup(var_name):  # Ya existe
            self.error(f"Variable '{var_name}' ya declarada", node)
            return DataType.ERROR
            
        if not self.symbol_table.add_symbol(var_name, var_type):  # Fallo al añadir
            self.error(f"No se pudo añadir variable '{var_name}'", node)
            return DataType.ERROR
            
        if "assignment" in node:  # Tiene asignación inicial
            expr_type = self.analyze(node["assignment"])  # Tipo de expresión
            if expr_type != var_type:  # Tipos incompatibles
                self.error(f"Tipo incompatible para '{var_name}'. Esperaba {var_type}, obtuvo {expr_type}", node)
                
        return var_type  # Retorna tipo declarado
        
    def analyze_assignment(self, node: Dict) -> DataType:  # Análisis de asignación
        """Analiza asignación de variables"""
        var_name = node["left"]  # Variable a asignar
        symbol = self.symbol_table.lookup(var_name)  # Buscar en tabla
        
        if not symbol:  # Variable no declarada
            self.error(f"Variable '{var_name}' no declarada", node)
            return DataType.ERROR
            
        var_type = symbol["type"]  # Tipo esperado
        expr_type = self.analyze(node["right"])  # Tipo asignado
        
        if var_type != expr_type:  # Comparar tipos
            self.error(f"Tipo incompatible en asignación. Esperaba {var_type}, obtuvo {expr_type}", node)
            return DataType.ERROR
            
        return var_type  # Asignación válida
        
    def analyze_binary_operation(self, node: Dict) -> DataType:  # Operación binaria
        """Analiza operaciones binarias"""
        left_type = self.analyze(node["left"])  # Tipo del operando izquierdo
        right_type = self.analyze(node["right"])  # Tipo del operando derecho
        op = node["operator"]  # Operador usado
        
        if left_type != right_type:  # Tipos deben coincidir
            self.error(f"Tipos incompatibles en operación {op}: {left_type} y {right_type}", node)
            return DataType.ERROR
            
        if op in ["+", "-", "*", "/"] and left_type not in [DataType.INT, DataType.FLOAT]:  # Solo numéricos
            self.error(f"Operador {op} no válido para tipo {left_type}", node)
            return DataType.ERROR
        elif op in ["==", "!=", "<", ">"] and left_type == DataType.STR:  # Comparación inválida
            self.error(f"Operador {op} no válido para cadenas", node)
            return DataType.ERROR
            
        return DataType.BOOL if op in ["==", "!=", "<", ">", "<=", ">="] else left_type  # Tipo de retorno
        
    def analyze_identifier(self, node: Dict) -> DataType:  # Identificador
        """Analiza referencias a variables"""
        var_name = node["name"]  # Nombre de variable
        symbol = self.symbol_table.lookup(var_name)  # Buscar en tabla
        
        if not symbol:  # No existe
            self.error(f"Variable '{var_name}' no declarada", node)
            return DataType.ERROR
            
        return symbol["type"]  # Retorna tipo de variable
        
    def get_type_from_string(self, type_str: str) -> DataType:  # Convertir cadena a tipo
        """Convierte string a tipo de dato"""
        return {
            "int": DataType.INT,
            "float": DataType.FLOAT,
            "str": DataType.STR,
            "bool": DataType.BOOL,
            "void": DataType.VOID
        }.get(type_str, DataType.ERROR)  # Valor por defecto es ERROR
        
    def error(self, message: str, node: Dict) -> None:  # Registrar error
        """Registra un error semántico"""
        line = node.get("line", "?")  # Línea del error
        col = node.get("column", "?")  # Columna del error
        self.errors.append(f"Error semántico en línea {line}, columna {col}: {message}")  # Guardar error

# ============ EJEMPLO DE USO ============
if __name__ == "__main__":  # Punto de entrada del script
    sample_ast = {  # AST de ejemplo
        "type": "program",
        "body": [ ... ]  # Omitido por brevedad
    }

    analyzer = SemanticAnalyzer()  # Crear analizador
    analyzer.analyze(sample_ast)  # Ejecutar análisis
    
    print("=== RESULTADOS DEL ANÁLISIS SEMÁNTICO ===")  # Imprimir encabezado
    if analyzer.errors:  # Si hubo errores
        print("\nErrores encontrados:")
        for error in analyzer.errors:  # Imprimir cada error
            print(f"- {error}")
    else:
        print("\nEl código es semánticamente válido")  # Sin errores
        
    print("\nTabla de símbolos final:")  # Mostrar tabla
    for scope, symbols in analyzer.symbol_table.table.items():  # Por cada ámbito
        print(f"\nÁmbito: {scope}")
        for name, info in symbols.items():  # Por cada símbolo
            print(f"  {name}: {info['type'].name}")  # Nombre y tipo
