"""
```python
ENSAMBLADOR DIDÁCTICO 
-----------------------------------------------
Un ensamblador básico que traduce código ensamblador a código máquina,
con emulación de ejecución paso a paso.
"""

# ============ IMPORTACIONES ============
from typing import Dict, List, Tuple, Optional  # Importa tipos de datos para type hints
from dataclasses import dataclass              # Para crear clases de datos fácilmente
from enum import Enum, auto                     # Para crear enumeraciones

# ============ DEFINICIÓN DE INSTRUCCIONES ============
class OpCode(Enum):                             # Enumeración de códigos de operación
    """Códigos de operación soportados"""
    MOV = auto()    # Mover datos               # Instrucción para mover valores
    ADD = auto()    # Sumar                     # Instrucción para sumar
    SUB = auto()    # Restar                    # Instrucción para restar
    JMP = auto()    # Salto incondicional       # Instrucción para saltar
    JZ = auto()     # Salto si cero             # Salto condicional si cero
    HLT = auto()    # Detener ejecución         # Detiene la ejecución
    NOP = auto()    # No operación              # No hace nada

class OperandType(Enum):                        # Enumeración de tipos de operandos
    """Tipos de operandos"""
    REGISTER = auto()  # Registro (AX, BX, etc.) # Operando que es un registro
    IMMEDIATE = auto() # Valor inmediato (número) # Operando con valor directo
    MEMORY = auto()    # Dirección de memoria    # Operando que accede a memoria
    LABEL = auto()     # Etiqueta para saltos    # Operando que es una etiqueta

@dataclass
class Instruction:                              # Clase para representar instrucciones
    """Estructura para instrucciones ensambladoras"""
    opcode: OpCode                              # Código de operación de la instrucción
    operands: List[Tuple[OperandType, str]]     # Lista de operandos con sus tipos
    line: int          # Línea original en código # Número de línea en el código fuente
    address: int = 0   # Dirección en memoria    # Dirección donde se almacena

# ============ CLASE ENSAMBLADOR ============
class Assembler:                                # Clase principal del ensamblador
    """Traduce código ensamblador a código máquina"""
    
    # Tamaños en bytes
    OPCODE_SIZE = 1                             # Tamaño en bytes del opcode
    OPERAND_SIZE = 2                            # Tamaño en bytes de cada operando
    INSTRUCTION_SIZE = OPCODE_SIZE + 2 * OPERAND_SIZE # Tamaño total por instrucción
    
    # Registros disponibles
    REGISTERS = {                               # Diccionario de registros
        'AX': 0, 'BX': 1, 'CX': 2, 'DX': 3,    # Registros de propósito general
        'SP': 4, 'BP': 5, 'SI': 6, 'DI': 7      # Registros especiales
    }
    
    def __init__(self):                         # Constructor del ensamblador
        self.symbol_table: Dict[str, int] = {}  # Para etiquetas # Tabla de símbolos
        self.memory: bytearray = bytearray(1024) # Memoria de 1KB # Memoria simulada
        self.pc = 0                             # Contador de programa # Program Counter
        
    def assemble(self, source: str) -> bool:    # Método principal
        """
        Ensambla código fuente a código máquina
        
        Args:
            source: Código fuente en ensamblador # Cadena con código ensamblador
            
        Returns:
            True si el ensamblado fue exitoso   # Booleano indicando éxito
        """
        lines = self._preprocess(source)        # Preprocesa el código fuente
        instructions = self._parse_lines(lines) # Convierte líneas a instrucciones
        
        # Primer paso: construir tabla de símbolos
        if not self._build_symbol_table(instructions): # Construye tabla de símbolos
            return False                           # Retorna False si hay error
            
        # Segundo paso: generar código máquina
        return self._generate_machine_code(instructions) # Genera código máquina
    
    def _preprocess(self, source: str) -> List[str]: # Limpia el código fuente
        """Limpia y divide el código fuente en líneas"""
        lines = []                                # Lista para líneas procesadas
        for line in source.split('\n'):           # Divide por saltos de línea
            # Eliminar comentarios y espacios extras
            line = line.split(';')[0].strip()     # Elimina comentarios y espacios
            if line:                             # Si la línea no está vacía
                lines.append(line)               # Añade a la lista
        return lines                              # Retorna líneas limpias
    
    def _parse_lines(self, lines: List[str]) -> List[Instruction]: # Parsea líneas
        """Convierte líneas de texto en estructuras Instruction"""
        instructions = []                         # Lista de instrucciones
        
        for i, line in enumerate(lines):         # Recorre cada línea
            parts = line.split()                 # Divide la línea en partes
            if not parts:                        # Si no hay partes
                continue                        # Salta a siguiente línea
                
            # Manejar etiquetas (palabra terminada en :)
            if parts[0].endswith(':'):           # Si es una etiqueta
                label = parts[0][:-1]            # Extrae nombre de etiqueta
                self.symbol_table[label] = len(instructions) * self.INSTRUCTION_SIZE # Guarda posición
                parts = parts[1:] if len(parts) > 1 else [] # Quita etiqueta de partes
                if not parts:                    # Si solo quedaba etiqueta
                    continue                    # Salta a siguiente línea
                    
            # Obtener opcode
            try:                                # Intenta obtener opcode
                opcode = OpCode[parts[0].upper()] # Convierte a enum OpCode
            except KeyError:                    # Si no existe el opcode
                print(f"Error: Opcode desconocido '{parts[0]}' en línea {i+1}") # Muestra error
                continue                        # Continua con siguiente línea
                
            # Parsear operandos
            operands = []                       # Lista para operandos
            for op in parts[1:]:                 # Recorre los operandos
                if op in self.REGISTERS:        # Si es un registro
                    operands.append((OperandType.REGISTER, op)) # Añade como registro
                elif op.startswith('[') and op.endswith(']'): # Si es acceso a memoria
                    operands.append((OperandType.MEMORY, op[1:-1])) # Añade como memoria
                elif op.isdigit() or (op[0] == '-' and op[1:].isdigit()): # Si es número
                    operands.append((OperandType.IMMEDIATE, op)) # Añade como inmediato
                else:  # Asumir que es etiqueta # Si no coincide con nada anterior
                    operands.append((OperandType.LABEL, op)) # Añade como etiqueta
            
            instructions.append(Instruction(opcode, operands, i+1)) # Crea instrucción
        
        return instructions                      # Retorna lista de instrucciones
    
    def _build_symbol_table(self, instructions: List[Instruction]) -> bool: # Construye tabla
        """Primer paso: construir tabla de símbolos (etiquetas)"""
        # Las etiquetas ya se procesaron en _parse_lines
        return True  # En una implementación real, verificaríamos errores # Simplificado
    
    def _generate_machine_code(self, instructions: List[Instruction]) -> bool: # Genera código
        """Segundo paso: generar código máquina"""
        self.pc = 0  # Resetear contador de programa # Inicializa PC
        
        for instr in instructions:               # Recorre cada instrucción
            # Codificar opcode
            self.memory[self.pc] = instr.opcode.value # Almacena valor del opcode
            self.pc += 1                        # Incrementa contador
            
            # Codificar operandos (max 2)
            for i in range(2):                  # Para cada posible operando
                if i < len(instr.operands):     # Si existe el operando
                    op_type, op_value = instr.operands[i] # Obtiene tipo y valor
                    self._encode_operand(op_type, op_value, instr.line) # Codifica
                else:                           # Si no existe operando
                    # Operando vacío
                    self.memory[self.pc] = 0    # Escribe 0 en byte bajo
                    self.memory[self.pc + 1] = 0 # Escribe 0 en byte alto
                    self.pc += 2                # Avanza contador
                    
            # Guardar dirección de la instrucción
            instr.address = self.pc - self.INSTRUCTION_SIZE # Guarda dirección
        
        return True                             # Retorna éxito
    
    def _encode_operand(self, op_type: OperandType, op_value: str, line: int) -> None: # Codifica
        """Codifica un operando en memoria"""
        if op_type == OperandType.REGISTER:     # Si es un registro
            reg_num = self.REGISTERS.get(op_value, 0) # Obtiene número de registro
            self.memory[self.pc] = reg_num      # Escribe número de registro
            self.memory[self.pc + 1] = 0xFF     # Marca de registro (0xFF)
        elif op_type == OperandType.IMMEDIATE:  # Si es valor inmediato
            num = int(op_value)                 # Convierte a entero
            self.memory[self.pc] = num & 0xFF   # Byte bajo del valor
            self.memory[self.pc + 1] = (num >> 8) & 0xFF # Byte alto del valor
        elif op_type == OperandType.LABEL:      # Si es una etiqueta
            # En una implementación real, calcularíamos el offset
            self.memory[self.pc] = 0            # Byte bajo a 0 (simplificado)
            self.memory[self.pc + 1] = 0        # Byte alto a 0 (simplificado)
        elif op_type == OperandType.MEMORY:     # Si es acceso a memoria
            # Simplificación: asumimos dirección directa
            if op_value.isdigit():              # Si es número directo
                addr = int(op_value)            # Convierte a entero
                self.memory[self.pc] = addr & 0xFF # Byte bajo de dirección
                self.memory[self.pc + 1] = (addr >> 8) & 0xFF # Byte alto
            else:                               # Si no es número directo
                print(f"Error: Dirección de memoria compleja no soportada en línea {line}") # Error
                self.memory[self.pc] = 0        # Byte bajo a 0
                self.memory[self.pc + 1] = 0     # Byte alto a 0
        
        self.pc += 2                            # Avanza 2 bytes
    
    def get_machine_code(self) -> bytearray:    # Obtiene código máquina
        """Obtiene el código máquina generado"""
        return self.memory[:self.pc]  # Solo la parte usada # Retorna solo memoria usada

# ============ CLASE CPU (EMULADOR) ============
class CPU:                                      # Clase que emula una CPU simple
    """Emula una CPU simple para ejecutar código máquina"""
    
    def __init__(self):                         # Constructor de la CPU
        self.registers = {name: 0 for name in Assembler.REGISTERS} # Inicializa registros
        self.memory = bytearray(1024)  # 1KB de memoria # Memoria de la CPU
        self.pc = 0                   # Contador de programa # Program Counter
        self.flags = {'Z': False}     # Flags de estado # Flag Zero
        self.running = False          # Estado de ejecución # Control de ejecución
    
    def load_program(self, program: bytearray) -> None: # Carga programa
        """Carga un programa en memoria"""
        self.memory[:len(program)] = program    # Copia programa a memoria
        self.pc = 0                            # Reinicia contador
        self.running = True                     # Marca como ejecutando
    
    def step(self) -> bool:                    # Ejecuta un paso
        """Ejecuta una instrucción"""
        if not self.running or self.pc >= len(self.memory): # Verifica si puede ejecutar
            return False                        # Retorna False si no
            
        # Decodificar instrucción
        opcode = self.memory[self.pc]          # Lee opcode
        op1 = self._decode_operand(self.pc + 1) # Decodifica operando 1
        op2 = self._decode_operand(self.pc + 3) # Decodifica operando 2
        
        # Ejecutar
        self.pc += Assembler.INSTRUCTION_SIZE  # Avanza contador
        
        try:                                   # Intenta ejecutar
            opcode_enum = OpCode(opcode)       # Convierte a enum
            if opcode_enum == OpCode.MOV:      # Si es MOV
                self._execute_mov(op1, op2)    # Ejecuta MOV
            elif opcode_enum == OpCode.ADD:    # Si es ADD
                self._execute_add(op1, op2)    # Ejecuta ADD
            elif opcode_enum == OpCode.SUB:    # Si es SUB
                self._execute_sub(op1, op2)    # Ejecuta SUB
            elif opcode_enum == OpCode.JMP:    # Si es JMP
                self.pc = op1['value']         # Salta a dirección
            elif opcode_enum == OpCode.JZ:     # Si es JZ
                if self.flags['Z']:            # Si flag Z está activo
                    self.pc = op1['value']    # Salta a dirección
            elif opcode_enum == OpCode.HLT:    # Si es HLT
                self.running = False           # Detiene ejecución
            elif opcode_enum == OpCode.NOP:    # Si es NOP
                pass                          # No hace nada
        except ValueError:                     # Si opcode no válido
            print(f"Error: Opcode inválido {opcode} en PC={self.pc - Assembler.INSTRUCTION_SIZE}") # Error
            self.running = False               # Detiene ejecución
        
        return self.running                    # Retorna estado
    
    def _decode_operand(self, addr: int) -> Dict: # Decodifica operando
        """Decodifica un operando de 2 bytes"""
        byte1 = self.memory[addr]              # Lee primer byte
        byte2 = self.memory[addr + 1]          # Lee segundo byte
        
        if byte2 == 0xFF:  # Es un registro    # Si es registro (marca 0xFF)
            reg_name = list(Assembler.REGISTERS.keys())[byte1] # Obtiene nombre
            return {'type': 'register', 'name': reg_name, 'value': self.registers[reg_name]} # Retorna info
        else:  # Valor inmediato o dirección    # Si no es registro
            value = byte1 | (byte2 << 8)       # Combina los bytes
            return {'type': 'immediate', 'value': value} # Retorna valor
    
    def _execute_mov(self, op1: Dict, op2: Dict) -> None: # Ejecuta MOV
        """Ejecuta instrucción MOV"""
        if op1['type'] == 'register':          # Si destino es registro
            self.registers[op1['name']] = op2['value'] # Mueve valor a registro
    
    def _execute_add(self, op1: Dict, op2: Dict) -> None: # Ejecuta ADD
        """Ejecuta instrucción ADD"""
        if op1['type'] == 'register':          # Si destino es registro
            result = self.registers[op1['name']] + op2['value'] # Suma valores
            self.registers[op1['name']] = result & 0xFFFF # Guarda resultado (16 bits)
            self.flags['Z'] = (result == 0)    # Actualiza flag Z
    
    def _execute_sub(self, op1: Dict, op2: Dict) -> None: # Ejecuta SUB
        """Ejecuta instrucción SUB"""
        if op1['type'] == 'register':          # Si destino es registro
            result = self.registers[op1['name']] - op2['value'] # Resta valores
            self.registers[op1['name']] = result & 0xFFFF # Guarda resultado (16 bits)
            self.flags['Z'] = (result == 0)    # Actualiza flag Z

# ============ EJEMPLO DE USO ============
def print_state(cpu: CPU) -> None:             # Muestra estado de la CPU
    """Muestra el estado actual de la CPU"""
    print(f"\nPC: {cpu.pc}  FLAGS: Z={cpu.flags['Z']}") # Muestra PC y flag Z
    print("Registros:")                        # Encabezado para registros
    for reg, val in cpu.registers.items():     # Recorre registros
        print(f"  {reg}: {val}")               # Muestra cada registro
    
    # Mostrar próxima instrucción
    if cpu.pc < len(cpu.memory):               # Si hay más instrucciones
        opcode = cpu.memory[cpu.pc]            # Lee opcode
        try:                                   # Intenta mostrar nombre
            print(f"\nPróxima instrucción: {OpCode(opcode).name}") # Muestra nombre
        except ValueError:                     # Si no reconoce
            print(f"\nPróxima instrucción: Desconocida ({opcode})") # Muestra código

if __name__ == "__main__":                     # Punto de entrada principal
    print("=== DEMOSTRACIÓN DE ENSAMBLADOR Y CPU ===") # Mensaje inicial
    
    # Programa de ejemplo en ensamblador
    source_code = """
        MOV AX, 5       ; Cargar 5 en AX      # Comentario
        MOV BX, 3       ; Cargar 3 en BX      # Comentario
        ADD AX, BX      ; Sumar BX a AX       # Comentario
        SUB AX, 1       ; Restar 1            # Comentario
        JZ end          ; Saltar si cero      # Comentario
        MOV CX, AX      ; Copiar AX a CX      # Comentario
    end:
        HLT             ; Detener             # Comentario
    """
    
    # Ensamblar el programa
    print("\nEnsamblando código...")           # Mensaje de ensamblado
    assembler = Assembler()                   # Crea instancia de ensamblador
    if assembler.assemble(source_code):       # Si ensamblado exitoso
        machine_code = assembler.get_machine_code() # Obtiene código máquina
        print("\nCódigo máquina generado (primeras 20 bytes):") # Muestra mensaje
        print(' '.join(f"{b:02X}" for b in machine_code[:20])) # Muestra bytes en hex
        
        # Ejecutar en la CPU
        print("\nEjecutando programa paso a paso:") # Mensaje de ejecución
        cpu = CPU()                           # Crea instancia de CPU
        cpu.load_program(machine_code)        # Carga el programa
        
        step = 1                              # Contador de pasos
        while cpu.step():                     # Mientras pueda ejecutar
            print(f"\n--- Paso {step} ---")   # Muestra número de paso
            print_state(cpu)                  # Muestra estado
            step += 1                         # Incrementa contador
            if step > 10:  # Límite para la demostración # Limita pasos
                print("\nDemostración limitada a 10 pasos") # Mensaje
                break                         # Termina ejecución
    else:
        print("\nError durante el ensamblado") # Mensaje de error
```