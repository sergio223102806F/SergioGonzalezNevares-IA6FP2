"""
ENSAMBLADOR DIDÁCTICO 
-----------------------------------------------
Un ensamblador básico que traduce código ensamblador a código máquina,
con emulación de ejecución paso a paso.
"""

# ============ IMPORTACIONES ============
from typing import Dict, List, Tuple, Optional  # Tipos para type hints
from dataclasses import dataclass              # Para clases de datos
from enum import Enum, auto                    # Para enumeraciones

# ============ DEFINICIÓN DE INSTRUCCIONES ============
class OpCode(Enum):                            # Enumeración de códigos de operación
    """Códigos de operación soportados"""
    MOV = auto()    # Mover datos              # Instrucción de movimiento
    ADD = auto()    # Sumar                    # Instrucción de suma
    SUB = auto()    # Restar                   # Instrucción de resta
    JMP = auto()    # Salto incondicional      # Instrucción de salto
    JZ = auto()     # Salto si cero            # Salto condicional
    HLT = auto()    # Detener ejecución        # Detener CPU
    NOP = auto()    # No operación             # Instrucción nula

class OperandType(Enum):                       # Enumeración de tipos de operandos
    """Tipos de operandos"""
    REGISTER = auto()  # Registro (AX, BX, etc.) # Operando de registro
    IMMEDIATE = auto() # Valor inmediato (número) # Valor directo
    MEMORY = auto()    # Dirección de memoria     # Acceso a memoria
    LABEL = auto()     # Etiqueta para saltos     # Referencia a etiqueta

@dataclass
class Instruction:                             # Clase para instrucciones
    """Estructura para instrucciones ensambladoras"""
    opcode: OpCode                             # Código de operación
    operands: List[Tuple[OperandType, str]]    # Lista de operandos
    line: int          # Línea original en código # Número de línea fuente
    address: int = 0   # Dirección en memoria    # Dirección en memoria

# ============ CLASE ENSAMBLADOR ============
class Assembler:                               # Clase principal del ensamblador
    """Traduce código ensamblador a código máquina"""
    
    # Tamaños en bytes
    OPCODE_SIZE = 1                            # Bytes para opcode
    OPERAND_SIZE = 2                           # Bytes por operando
    INSTRUCTION_SIZE = OPCODE_SIZE + 2 * OPERAND_SIZE # Bytes por instrucción
    
    # Registros disponibles
    REGISTERS = {                              # Diccionario de registros
        'AX': 0, 'BX': 1, 'CX': 2, 'DX': 3,   # Registros de propósito general
        'SP': 4, 'BP': 5, 'SI': 6, 'DI': 7    # Registros especiales
    }
    
    def __init__(self):                        # Constructor
        self.symbol_table: Dict[str, int] = {}  # Para etiquetas # Tabla de símbolos
        self.memory: bytearray = bytearray(1024) # Memoria de 1KB # Memoria simulada
        self.pc = 0                             # Contador de programa # Program Counter
        
    def assemble(self, source: str) -> bool:   # Método principal
        """
        Ensambla código fuente a código máquina
        
        Args:
            source: Código fuente en ensamblador # Texto con código fuente
            
        Returns:
            True si el ensamblado fue exitoso   # Booleano de éxito
        """
        lines = self._preprocess(source)       # Preprocesar código
        instructions = self._parse_lines(lines) # Convertir a instrucciones
        
        # Primer paso: construir tabla de símbolos
        if not self._build_symbol_table(instructions): # Construir tabla
            return False                        # Retornar si hay error
            
        # Segundo paso: generar código máquina
        return self._generate_machine_code(instructions) # Generar código
    
    def _preprocess(self, source: str) -> List[str]: # Limpieza de código
        """Limpia y divide el código fuente en líneas"""
        lines = []                              # Lista para líneas limpias
        for line in source.split('\n'):         # Dividir por saltos
            # Eliminar comentarios y espacios extras
            line = line.split(';')[0].strip()   # Quitar comentarios
            if line:                            # Si hay contenido
                lines.append(line)              # Añadir a lista
        return lines                            # Retornar líneas limpias
    
    def _parse_lines(self, lines: List[str]) -> List[Instruction]: # Parser
        """Convierte líneas de texto en estructuras Instruction"""
        instructions = []                      # Lista de instrucciones
        
        for i, line in enumerate(lines):       # Procesar cada línea
            parts = line.split()               # Dividir línea
            if not parts:                      # Si está vacía
                continue                       # Saltar
                
            # Manejar etiquetas (palabra terminada en :)
            if parts[0].endswith(':'):         # Si es etiqueta
                label = parts[0][:-1]          # Extraer nombre
                self.symbol_table[label] = len(instructions) * self.INSTRUCTION_SIZE # Guardar posición
                parts = parts[1:] if len(parts) > 1 else [] # Quitar etiqueta
                if not parts:                  # Si solo era etiqueta
                    continue                  # Saltar
                    
            # Obtener opcode
            try:                              # Intentar obtener opcode
                opcode = OpCode[parts[0].upper()] # Convertir a enum
            except KeyError:                   # Si no existe
                print(f"Error: Opcode desconocido '{parts[0]}' en línea {i+1}") # Mostrar error
                continue                      # Continuar
                
            # Parsear operandos
            operands = []                     # Lista de operandos
            for op in parts[1:]:              # Procesar cada operando
                if op in self.REGISTERS:      # Si es registro
                    operands.append((OperandType.REGISTER, op)) # Añadir como registro
                elif op.startswith('[') and op.endswith(']'): # Si es memoria
                    operands.append((OperandType.MEMORY, op[1:-1])) # Añadir como memoria
                elif op.isdigit() or (op[0] == '-' and op[1:].isdigit()): # Si es número
                    operands.append((OperandType.IMMEDIATE, op)) # Añadir como inmediato
                else:  # Asumir que es etiqueta # Si no coincide
                    operands.append((OperandType.LABEL, op)) # Añadir como etiqueta
            
            instructions.append(Instruction(opcode, operands, i+1)) # Crear instrucción
        
        return instructions                    # Retornar instrucciones
    
    def _build_symbol_table(self, instructions: List[Instruction]) -> bool: # Tabla símbolos
        """Primer paso: construir tabla de símbolos (etiquetas)"""
        # Las etiquetas ya se procesaron en _parse_lines
        return True  # En una implementación real, verificaríamos errores # Simplificado
    
    def _generate_machine_code(self, instructions: List[Instruction]) -> bool: # Generar código
        """Segundo paso: generar código máquina"""
        self.pc = 0  # Resetear contador de programa # Inicializar PC
        
        for instr in instructions:             # Procesar cada instrucción
            # Codificar opcode
            self.memory[self.pc] = instr.opcode.value # Guardar opcode
            self.pc += 1                      # Incrementar PC
            
            # Codificar operandos (max 2)
            for i in range(2):                # Para cada posible operando
                if i < len(instr.operands):   # Si existe operando
                    op_type, op_value = instr.operands[i] # Obtener tipo y valor
                    self._encode_operand(op_type, op_value, instr.line) # Codificar
                else:                         # Si no existe
                    # Operando vacío
                    self.memory[self.pc] = 0  # Escribir 0
                    self.memory[self.pc + 1] = 0 # Escribir 0
                    self.pc += 2              # Avanzar
                    
            # Guardar dirección de la instrucción
            instr.address = self.pc - self.INSTRUCTION_SIZE # Guardar dirección
        
        return True                          # Retornar éxito
    
    def _encode_operand(self, op_type: OperandType, op_value: str, line: int) -> None: # Codificar
        """Codifica un operando en memoria"""
        if op_type == OperandType.REGISTER:  # Si es registro
            reg_num = self.REGISTERS.get(op_value, 0) # Obtener número
            self.memory[self.pc] = reg_num   # Guardar número
            self.memory[self.pc + 1] = 0xFF  # Marca de registro
        elif op_type == OperandType.IMMEDIATE: # Si es inmediato
            num = int(op_value)              # Convertir a entero
            self.memory[self.pc] = num & 0xFF # Byte bajo
            self.memory[self.pc + 1] = (num >> 8) & 0xFF # Byte alto
        elif op_type == OperandType.LABEL:   # Si es etiqueta
            # En una implementación real, calcularíamos el offset
            self.memory[self.pc] = 0         # Byte bajo 0
            self.memory[self.pc + 1] = 0      # Byte alto 0
        elif op_type == OperandType.MEMORY:  # Si es memoria
            # Simplificación: asumimos dirección directa
            if op_value.isdigit():           # Si es número
                addr = int(op_value)         # Convertir a entero
                self.memory[self.pc] = addr & 0xFF # Byte bajo
                self.memory[self.pc + 1] = (addr >> 8) & 0xFF # Byte alto
            else:                            # Si no es número
                print(f"Error: Dirección de memoria compleja no soportada en línea {line}") # Error
                self.memory[self.pc] = 0     # Byte bajo 0
                self.memory[self.pc + 1] = 0  # Byte alto 0
        
        self.pc += 2                         # Avanzar 2 bytes
    
    def get_machine_code(self) -> bytearray:  # Obtener código
        """Obtiene el código máquina generado"""
        return self.memory[:self.pc]  # Solo la parte usada # Retornar memoria usada

# ============ CLASE CPU (EMULADOR) ============
class CPU:                                   # Clase para emular CPU
    """Emula una CPU simple para ejecutar código máquina"""
    
    def __init__(self):                      # Constructor
        self.registers = {name: 0 for name in Assembler.REGISTERS} # Inicializar registros
        self.memory = bytearray(1024)  # 1KB de memoria # Memoria de CPU
        self.pc = 0                   # Contador de programa # Program Counter
        self.flags = {'Z': False}     # Flags de estado # Flag Zero
        self.running = False          # Estado de ejecución # Control ejecución
    
    def load_program(self, program: bytearray) -> None: # Cargar programa
        """Carga un programa en memoria"""
        self.memory[:len(program)] = program # Copiar programa
        self.pc = 0                         # Resetear PC
        self.running = True                 # Activar ejecución
    
    def step(self) -> bool:                 # Ejecutar paso
        """Ejecuta una instrucción"""
        if not self.running or self.pc >= len(self.memory): # Verificar estado
            return False                   # Retornar si no se puede ejecutar
            
        # Decodificar instrucción
        opcode = self.memory[self.pc]     # Leer opcode
        op1 = self._decode_operand(self.pc + 1) # Decodificar op1
        op2 = self._decode_operand(self.pc + 3) # Decodificar op2
        
        # Ejecutar
        self.pc += Assembler.INSTRUCTION_SIZE # Avanzar PC
        
        try:                               # Intentar ejecutar
            opcode_enum = OpCode(opcode)   # Convertir a enum
            if opcode_enum == OpCode.MOV:  # MOV
                self._execute_mov(op1, op2) # Ejecutar MOV
            elif opcode_enum == OpCode.ADD: # ADD
                self._execute_add(op1, op2) # Ejecutar ADD
            elif opcode_enum == OpCode.SUB: # SUB
                self._execute_sub(op1, op2) # Ejecutar SUB
            elif opcode_enum == OpCode.JMP: # JMP
                self.pc = op1['value']     # Saltar
            elif opcode_enum == OpCode.JZ: # JZ
                if self.flags['Z']:        # Si flag Z
                    self.pc = op1['value'] # Saltar
            elif opcode_enum == OpCode.HLT: # HLT
                self.running = False       # Detener
            elif opcode_enum == OpCode.NOP: # NOP
                pass                      # No hacer nada
        except ValueError:                 # Si opcode inválido
            print(f"Error: Opcode inválido {opcode} en PC={self.pc - Assembler.INSTRUCTION_SIZE}") # Error
            self.running = False           # Detener
        
        return self.running                # Retornar estado
    
    def _decode_operand(self, addr: int) -> Dict: # Decodificar operando
        """Decodifica un operando de 2 bytes"""
        byte1 = self.memory[addr]         # Leer byte bajo
        byte2 = self.memory[addr + 1]     # Leer byte alto
        
        if byte2 == 0xFF:  # Es un registro # Si es registro
            reg_name = list(Assembler.REGISTERS.keys())[byte1] # Obtener nombre
            return {'type': 'register', 'name': reg_name, 'value': self.registers[reg_name]} # Retornar info
        else:  # Valor inmediato o dirección # Si no es registro
            value = byte1 | (byte2 << 8)  # Combinar bytes
            return {'type': 'immediate', 'value': value} # Retornar valor
    
    def _execute_mov(self, op1: Dict, op2: Dict) -> None: # Ejecutar MOV
        """Ejecuta instrucción MOV"""
        if op1['type'] == 'register':      # Si destino es registro
            self.registers[op1['name']] = op2['value'] # Mover valor
    
    def _execute_add(self, op1: Dict, op2: Dict) -> None: # Ejecutar ADD
        """Ejecuta instrucción ADD"""
        if op1['type'] == 'register':      # Si destino es registro
            result = self.registers[op1['name']] + op2['value'] # Sumar
            self.registers[op1['name']] = result & 0xFFFF # Guardar (16 bits)
            self.flags['Z'] = (result == 0) # Actualizar flag Z
    
    def _execute_sub(self, op1: Dict, op2: Dict) -> None: # Ejecutar SUB
        """Ejecuta instrucción SUB"""
        if op1['type'] == 'register':      # Si destino es registro
            result = self.registers[op1['name']] - op2['value'] # Restar
            self.registers[op1['name']] = result & 0xFFFF # Guardar (16 bits)
            self.flags['Z'] = (result == 0) # Actualizar flag Z

# ============ EJEMPLO DE USO ============
def print_state(cpu: CPU) -> None:         # Mostrar estado
    """Muestra el estado actual de la CPU"""
    print(f"\nPC: {cpu.pc}  FLAGS: Z={cpu.flags['Z']}") # Mostrar PC y flag
    print("Registros:")                    # Encabezado
    for reg, val in cpu.registers.items(): # Recorrer registros
        print(f"  {reg}: {val}")           # Mostrar cada registro
    
    # Mostrar próxima instrucción
    if cpu.pc < len(cpu.memory):           # Si hay más código
        opcode = cpu.memory[cpu.pc]        # Leer opcode
        try:                               # Intentar mostrar nombre
            print(f"\nPróxima instrucción: {OpCode(opcode).name}") # Mostrar nombre
        except ValueError:                 # Si no se reconoce
            print(f"\nPróxima instrucción: Desconocida ({opcode})") # Mostrar código

if __name__ == "__main__":                 # Punto de entrada
    print("=== DEMOSTRACIÓN DE ENSAMBLADOR Y CPU ===") # Mensaje inicial
    
    # Programa de ejemplo en ensamblador
    source_code = """
        MOV AX, 5       ; Cargar 5 en AX
        MOV BX, 3       ; Cargar 3 en BX
        ADD AX, BX      ; Sumar BX a AX
        SUB AX, 1       ; Restar 1
        JZ end          ; Saltar si cero
        MOV CX, AX      ; Copiar AX a CX
    end:
        HLT             ; Detener
    """
    
    # Ensamblar el programa
    print("\nEnsamblando código...")       # Mensaje
    assembler = Assembler()               # Crear ensamblador
    if assembler.assemble(source_code):   # Si ensamblado exitoso
        machine_code = assembler.get_machine_code() # Obtener código
        print("\nCódigo máquina generado (primeras 20 bytes):") # Mensaje
        print(' '.join(f"{b:02X}" for b in machine_code[:20])) # Mostrar bytes
        
        # Ejecutar en la CPU
        print("\nEjecutando programa paso a paso:") # Mensaje
        cpu = CPU()                       # Crear CPU
        cpu.load_program(machine_code)    # Cargar programa
        
        step = 1                         # Contador pasos
        while cpu.step():                 # Ejecutar pasos
            print(f"\n--- Paso {step} ---") # Mostrar paso
            print_state(cpu)              # Mostrar estado
            step += 1                    # Incrementar
            if step > 10:  # Límite para la demostración # Límite
                print("\nDemostración limitada a 10 pasos") # Mensaje
                break                     # Terminar
    else:
        print("\nError durante el ensamblado") # Mensaje error