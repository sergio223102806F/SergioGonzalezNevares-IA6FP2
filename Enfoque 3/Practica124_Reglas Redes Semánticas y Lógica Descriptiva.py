# -*- coding: utf-8 -*-


# Importaciones necesarias
from typing import Dict, List, Set, Optional, Tuple
from enum import Enum, auto
from dataclasses import dataclass
from collections import defaultdict

class TipoRelacion(Enum):
    """Tipos de relaciones semánticas posibles"""
    HIPERONIMO = auto()  # Relación "es-un" (ej: perro es-un animal)
    MERONIMO = auto()    # Relación "parte-de" (ej: pata es-parte-de perro)
    ATRIBUTO = auto()    # Relación de atributo (ej: perro tiene-propiedad color)
    INSTANCIA = auto()   # Relación de instancia (ej: Fido es-instancia-de perro)

class OperadorLogico(Enum):
    """Operadores para lógica descriptiva"""
    CONJUNCION = '∧'     # AND lógico
    DISYUNCION = '∨'     # OR lógico
    NEGACION = '¬'       # NOT lógico
    IMPLICACION = '→'    # Implicación
    EQUIVALENCIA = '≡'   # Equivalencia

@dataclass
class NodoSemantico:
    """Representa un concepto en la red semántica"""
    nombre: str           # Identificador del concepto
    atributos: Dict[str, List[str]] = field(default_factory=dict)  # Propiedades del concepto
    relaciones: List[Tuple[TipoRelacion, str]] = field(default_factory=list)  # Relaciones con otros nodos

@dataclass
class Regla:
    """Estructura para representar reglas de producción"""
    antecedente: List[str]  # Lista de condiciones (premisas)
    consecuente: str       # Conclusión de la regla
    operador: OperadorLogico = OperadorLogico.IMPLICACION  # Operador lógico principal

class SistemaConocimiento:
    """
    Sistema integrado que combina:
    - Redes semánticas
    - Reglas de producción
    - Lógica descriptiva
    """
    
    def __init__(self):
        """Inicializa las estructuras de conocimiento"""
        self.red_semantica: Dict[str, NodoSemantico] = {}  # Diccionario de nodos por nombre
        self.reglas: List[Regla] = []                     # Lista de reglas de producción
        self.ontologia: Dict[str, Set[str]] = defaultdict(set)  # Jerarquía de conceptos
        
    def agregar_nodo(self, nodo: NodoSemantico) -> bool:
        """
        Añade un nuevo nodo a la red semántica
        
        Args:
            nodo (NodoSemantico): Nodo a añadir
            
        Returns:
            bool: True si se añadió, False si ya existía
        """
        if nodo.nombre in self.red_semantica:
            return False
            
        self.red_semantica[nodo.nombre] = nodo
        return True
    
    def agregar_relacion(self, origen: str, tipo: TipoRelacion, destino: str) -> bool:
        """
        Establece una relación semántica entre nodos
        
        Args:
            origen (str): Nodo origen de la relación
            tipo (TipoRelacion): Tipo de relación semántica
            destino (str): Nodo destino de la relación
            
        Returns:
            bool: True si se estableció la relación, False si algún nodo no existe
        """
        if origen not in self.red_semantica or destino not in self.red_semantica:
            return False
            
        self.red_semantica[origen].relaciones.append((tipo, destino))
        
        # Actualizar ontología para relaciones jerárquicas
        if tipo == TipoRelacion.HIPERONIMO:
            self.ontologia[destino].add(origen)
        elif tipo == TipoRelacion.MERONIMO:
            self.ontologia[origen].add(destino)
            
        return True
    
    def agregar_regla(self, regla: Regla) -> None:
        """
        Añade una nueva regla de producción al sistema
        
        Args:
            regla (Regla): Regla a añadir
        """
        self.reglas.append(regla)
    
    def inferir_conocimiento(self, hechos: Set[str]) -> Set[str]:
        """
        Aplica el encadenamiento hacia adelante para inferir nuevos hechos
        
        Args:
            hechos (Set[str]): Conjunto inicial de hechos conocidos
            
        Returns:
            Set[str]: Conjunto ampliado de hechos después de aplicar reglas
        """
        nuevos_hechos = hechos.copy()
        cambio = True
        
        while cambio:
            cambio = False
            for regla in self.reglas:
                # Verificar si todas las premisas se cumplen
                if all(premisa in nuevos_hechos for premisa in regla.antecedente):
                    # Si la conclusión no estaba ya en los hechos
                    if regla.consecuente not in nuevos_hechos:
                        nuevos_hechos.add(regla.consecuente)
                        cambio = True
                        
        return nuevos_hechos
    
    def obtener_subclases(self, concepto: str) -> Set[str]:
        """
        Obtiene todas las subclases de un concepto en la jerarquía
        
        Args:
            concepto (str): Concepto del que obtener subclases
            
        Returns:
            Set[str]: Conjunto de subclases directas e indirectas
        """
        subclases = set()
        por_explorar = [concepto]
        
        while por_explorar:
            actual = por_explorar.pop()
            for subclase in self.ontologia.get(actual, set()):
                if subclase not in subclases:
                    subclases.add(subclase)
                    por_explorar.append(subclase)
                    
        return subclases
    
    def verificar_consistencia(self) -> List[str]:
        """
        Verifica consistencia básica del sistema de conocimiento
        
        Returns:
            List[str]: Lista de inconsistencias encontradas
        """
        inconsistencias = []
        
        # Verificar nodos sin relaciones
        for nombre, nodo in self.red_semantica.items():
            if not nodo.relaciones and nombre != "Thing":
                inconsistencias.append(f"Nodo aislado: {nombre}")
                
        # Verificar reglas con antecedentes vacíos
        for i, regla in enumerate(self.reglas):
            if not regla.antecedente:
                inconsistencias.append(f"Regla {i} sin antecedentes")
                
        return inconsistencias
    
    def consultar_red(self, concepto: str) -> Optional[Dict]:
        """
        Consulta toda la información sobre un concepto en la red
        
        Args:
            concepto (str): Concepto a consultar
            
        Returns:
            Optional[Dict]: Diccionario con la información o None si no existe
        """
        if concepto not in self.red_semantica:
            return None
            
        nodo = self.red_semantica[concepto]
        return {
            "atributos": nodo.atributos,
            "relaciones": [
                {"tipo": tipo.name, "destino": dest} 
                for tipo, dest in nodo.relaciones
            ],
            "subclases": list(self.obtener_subclases(concepto))
        }

def demostracion_sistema():
    """
    Función de demostración del sistema integrado de conocimiento
    """
    sistema = SistemaConocimiento()
    
    # 1. Construcción de la red semántica
    # Crear nodos conceptuales
    sistema.agregar_nodo(NodoSemantico("Animal", {"movimiento": ["voluntario"]}))
    sistema.agregar_nodo(NodoSemantico("Perro", {"patas": ["4"], "sonido": ["ladrido"]}))
    sistema.agregar_nodo(NodoSemantico("Gato", {"patas": ["4"], "sonido": ["maullido"]}))
    sistema.agregar_nodo(NodoSemantico("Pata", {"funcion": ["caminar"]}))
    
    # Establecer relaciones semánticas
    sistema.agregar_relacion("Perro", TipoRelacion.HIPERONIMO, "Animal")
    sistema.agregar_relacion("Gato", TipoRelacion.HIPERONIMO, "Animal")
    sistema.agregar_relacion("Pata", TipoRelacion.MERONIMO, "Perro")
    sistema.agregar_relacion("Pata", TipoRelacion.MERONIMO, "Gato")
    
    # 2. Añadir reglas de producción
    sistema.agregar_regla(Regla(
        antecedente=["Perro(x)"],
        consecuente="Tiene_patas(x)",
        operador=OperadorLogico.IMPLICACION
    ))
    
    sistema.agregar_regla(Regla(
        antecedente=["Gato(x)"],
        consecuente="Tiene_patas(x)",
        operador=OperadorLogico.IMPLICACION
    ))
    
    sistema.agregar_regla(Regla(
        antecedente=["Animal(x)", "Tiene_patas(x)"],
        consecuente="Puede_caminar(x)",
        operador=OperadorLogico.IMPLICACION
    ))
    
    # 3. Demostración de inferencia
    hechos_iniciales = {"Perro(Fido)", "Gato(Garfiel)"}
    hechos_inferidos = sistema.inferir_conocimiento(hechos_iniciales)
    
    # 4. Consultas a la red semántica
    consulta_perro = sistema.consultar_red("Perro")
    subclases_animal = sistema.obtener_subclases("Animal")
    
    # 5. Mostrar resultados
    print("=== DEMOSTRACIÓN SISTEMA DE CONOCIMIENTO ===")
    print("\nHechos iniciales:", hechos_iniciales)
    print("Hechos inferidos:", hechos_inferidos)
    
    print("\nConsulta 'Perro':")
    for k, v in consulta_perro.items():
        print(f"{k}: {v}")
    
    print("\nSubclases de 'Animal':", subclases_animal)
    
    print("\nInconsistencias detectadas:", sistema.verificar_consistencia())

if __name__ == "__main__":
    demostracion_sistema()