"""
ENSAMBLADOR DIDÁCTICO 
-----------------------------------------------
Un ensamblador básico que traduce código ensamblador a código máquina,
con emulación de ejecución paso a paso.
"""

# ============ IMPORTACIONES ============
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum, auto

# ============ DEFINICIÓN DE INSTRUCCIONES ============
class OpCode(Enum):
    """Códigos de operación soportados"""
    MOV = auto()    # Mover datos
    ADD = auto()    # Sumar
    SUB = auto()    # Restar
    JMP = auto()    # Salto incondicional
    JZ = auto()     # Salto si cero
    HLT = auto()    # Detener ejecución
    NOP = auto()    # No operación

class OperandType(Enum):
    """Tipos de operandos"""
    REGISTER = auto()  # Registro (AX, BX, etc.)
    IMMEDIATE = auto() # Valor inmediato (número)
    MEMORY = auto()    # Dirección de memoria
    LABEL = auto()     # Etiqueta para saltos

@dataclass
class Instruction:
    """Estructura para instrucciones ensambladoras"""
    opcode: OpCode
    operands: List[Tuple[OperandType, str]]
    line: int          # Línea original en código
    address: int = 0   # Dirección en memoria

# ============ CLASE ENSAMBLADOR ============
class Assembler:
    """Traduce código ensamblador a código máquina"""
    
    # Tamaños en bytes
    OPCODE_SIZE = 1
    OPERAND_SIZE = 2
    INSTRUCTION_SIZE = OPCODE_SIZE + 2 * OPERAND_SIZE
    
    # Registros disponibles
    REGISTERS = {
        'AX': 0, 'BX': 1, 'CX': 2, 'DX': 3,
        'SP': 4, 'BP': 5, 'SI': 6, 'DI': 7
    }
    
    def __init__(self):
        self.symbol_table: Dict[str, int] = {}  # Para etiquetas
        self.memory: bytearray = bytearray(1024) # Memoria de 1KB
        self.pc = 0                             # Contador de programa
        
    def assemble(self, source: str) -> bool:
        """
        Ensambla código fuente a código máquina
        
        Args:
            source: Código fuente en ensamblador
            
        Returns:
            True si el ensamblado fue exitoso
        """
        lines = self._preprocess(source)
        instructions = self._parse_lines(lines)
        
        # Primer paso: construir tabla de símbolos
        if not self._build_symbol_table(instructions):
            return False
            
        # Segundo paso: generar código máquina
        return self._generate_machine_code(instructions)
    
    def _preprocess(self, source: str) -> List[str]:
        """Limpia y divide el código fuente en líneas"""
        lines = []
        for line in source.split('\n'):
            # Eliminar comentarios y espacios extras
            line = line.split(';')[0].strip()
            if line:
                lines.append(line)
        return lines
    
    def _parse_lines(self, lines: List[str]) -> List[Instruction]:
        """Convierte líneas de texto en estructuras Instruction"""
        instructions = []
        
        for i, line in enumerate(lines):
            parts = line.split()
            if not parts:
                continue
                
            # Manejar etiquetas (palabra terminada en :)
            if parts[0].endswith(':'):
                label = parts[0][:-1]
                self.symbol_table[label] = len(instructions) * self.INSTRUCTION_SIZE
                parts = parts[1:] if len(parts) > 1 else []
                if not parts:
                    continue
                    
            # Obtener opcode
            try:
                opcode = OpCode[parts[0].upper()]
            except KeyError:
                print(f"Error: Opcode desconocido '{parts[0]}' en línea {i+1}")
                continue
                
            # Parsear operandos
            operands = []
            for op in parts[1:]:
                if op in self.REGISTERS:
                    operands.append((OperandType.REGISTER, op))
                elif op.startswith('[') and op.endswith(']'):
                    operands.append((OperandType.MEMORY, op[1:-1]))
                elif op.isdigit() or (op[0] == '-' and op[1:].isdigit()):
                    operands.append((OperandType.IMMEDIATE, op))
                else:  # Asumir que es etiqueta
                    operands.append((OperandType.LABEL, op))
            
            instructions.append(Instruction(opcode, operands, i+1))
        
        return instructions
    
    def _build_symbol_table(self, instructions: List[Instruction]) -> bool:
        """Primer paso: construir tabla de símbolos (etiquetas)"""
        # Las etiquetas ya se procesaron en _parse_lines
        return True  # En una implementación real, verificaríamos errores
    
    def _generate_machine_code(self, instructions: List[Instruction]) -> bool:
        """Segundo paso: generar código máquina"""
        self.pc = 0  # Resetear contador de programa
        
        for instr in instructions:
            # Codificar opcode
            self.memory[self.pc] = instr.opcode.value
            self.pc += 1
            
            # Codificar operandos (max 2)
            for i in range(2):
                if i < len(instr.operands):
                    op_type, op_value = instr.operands[i]
                    self._encode_operand(op_type, op_value, instr.line)
                else:
                    # Operando vacío
                    self.memory[self.pc] = 0
                    self.memory[self.pc + 1] = 0
                    self.pc += 2
                    
            # Guardar dirección de la instrucción
            instr.address = self.pc - self.INSTRUCTION_SIZE
        
        return True
    
    def _encode_operand(self, op_type: OperandType, op_value: str, line: int) -> None:
        """Codifica un operando en memoria"""
        if op_type == OperandType.REGISTER:
            reg_num = self.REGISTERS.get(op_value, 0)
            self.memory[self.pc] = reg_num
            self.memory[self.pc + 1] = 0xFF  # Marca de registro
        elif op_type == OperandType.IMMEDIATE:
            num = int(op_value)
            self.memory[self.pc] = num & 0xFF          # Byte bajo
            self.memory[self.pc + 1] = (num >> 8) & 0xFF # Byte alto
        elif op_type == OperandType.LABEL:
            # En una implementación real, calcularíamos el offset
            self.memory[self.pc] = 0
            self.memory[self.pc + 1] = 0
        elif op_type == OperandType.MEMORY:
            # Simplificación: asumimos dirección directa
            if op_value.isdigit():
                addr = int(op_value)
                self.memory[self.pc] = addr & 0xFF
                self.memory[self.pc + 1] = (addr >> 8) & 0xFF
            else:
                print(f"Error: Dirección de memoria compleja no soportada en línea {line}")
                self.memory[self.pc] = 0
                self.memory[self.pc + 1] = 0
        
        self.pc += 2
    
    def get_machine_code(self) -> bytearray:
        """Obtiene el código máquina generado"""
        return self.memory[:self.pc]  # Solo la parte usada

# ============ CLASE CPU (EMULADOR) ============
class CPU:
    """Emula una CPU simple para ejecutar código máquina"""
    
    def __init__(self):
        self.registers = {name: 0 for name in Assembler.REGISTERS}
        self.memory = bytearray(1024)  # 1KB de memoria
        self.pc = 0                   # Contador de programa
        self.flags = {'Z': False}     # Flags de estado
        self.running = False          # Estado de ejecución
    
    def load_program(self, program: bytearray) -> None:
        """Carga un programa en memoria"""
        self.memory[:len(program)] = program
        self.pc = 0
        self.running = True
    
    def step(self) -> bool:
        """Ejecuta una instrucción"""
        if not self.running or self.pc >= len(self.memory):
            return False
            
        # Decodificar instrucción
        opcode = self.memory[self.pc]
        op1 = self._decode_operand(self.pc + 1)
        op2 = self._decode_operand(self.pc + 3)
        
        # Ejecutar
        self.pc += Assembler.INSTRUCTION_SIZE
        
        try:
            opcode_enum = OpCode(opcode)
            if opcode_enum == OpCode.MOV:
                self._execute_mov(op1, op2)
            elif opcode_enum == OpCode.ADD:
                self._execute_add(op1, op2)
            elif opcode_enum == OpCode.SUB:
                self._execute_sub(op1, op2)
            elif opcode_enum == OpCode.JMP:
                self.pc = op1['value']
            elif opcode_enum == OpCode.JZ:
                if self.flags['Z']:
                    self.pc = op1['value']
            elif opcode_enum == OpCode.HLT:
                self.running = False
            elif opcode_enum == OpCode.NOP:
                pass
        except ValueError:
            print(f"Error: Opcode inválido {opcode} en PC={self.pc - Assembler.INSTRUCTION_SIZE}")
            self.running = False
        
        return self.running
    
    def _decode_operand(self, addr: int) -> Dict:
        """Decodifica un operando de 2 bytes"""
        byte1 = self.memory[addr]
        byte2 = self.memory[addr + 1]
        
        if byte2 == 0xFF:  # Es un registro
            reg_name = list(Assembler.REGISTERS.keys())[byte1]
            return {'type': 'register', 'name': reg_name, 'value': self.registers[reg_name]}
        else:  # Valor inmediato o dirección
            value = byte1 | (byte2 << 8)
            return {'type': 'immediate', 'value': value}
    
    def _execute_mov(self, op1: Dict, op2: Dict) -> None:
        """Ejecuta instrucción MOV"""
        if op1['type'] == 'register':
            self.registers[op1['name']] = op2['value']
    
    def _execute_add(self, op1: Dict, op2: Dict) -> None:
        """Ejecuta instrucción ADD"""
        if op1['type'] == 'register':
            result = self.registers[op1['name']] + op2['value']
            self.registers[op1['name']] = result & 0xFFFF
            self.flags['Z'] = (result == 0)
    
    def _execute_sub(self, op1: Dict, op2: Dict) -> None:
        """Ejecuta instrucción SUB"""
        if op1['type'] == 'register':
            result = self.registers[op1['name']] - op2['value']
            self.registers[op1['name']] = result & 0xFFFF
            self.flags['Z'] = (result == 0)

# ============ EJEMPLO DE USO ============
def print_state(cpu: CPU) -> None:
    """Muestra el estado actual de la CPU"""
    print(f"\nPC: {cpu.pc}  FLAGS: Z={cpu.flags['Z']}")
    print("Registros:")
    for reg, val in cpu.registers.items():
        print(f"  {reg}: {val}")
    
    # Mostrar próxima instrucción
    if cpu.pc < len(cpu.memory):
        opcode = cpu.memory[cpu.pc]
        try:
            print(f"\nPróxima instrucción: {OpCode(opcode).name}")
        except ValueError:
            print(f"\nPróxima instrucción: Desconocida ({opcode})")

if __name__ == "__main__":
    print("=== DEMOSTRACIÓN DE ENSAMBLADOR Y CPU ===")
    
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
    print("\nEnsamblando código...")
    assembler = Assembler()
    if assembler.assemble(source_code):
        machine_code = assembler.get_machine_code()
        print("\nCódigo máquina generado (primeras 20 bytes):")
        print(' '.join(f"{b:02X}" for b in machine_code[:20]))
        
        # Ejecutar en la CPU
        print("\nEjecutando programa paso a paso:")
        cpu = CPU()
        cpu.load_program(machine_code)
        
        step = 1
        while cpu.step():
            print(f"\n--- Paso {step} ---")
            print_state(cpu)
            step += 1
            if step > 10:  # Límite para la demostración
                print("\nDemostración limitada a 10 pasos")
                break
    else:
        print("\nError durante el ensamblado")