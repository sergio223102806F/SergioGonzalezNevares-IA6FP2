# -*- coding: utf-8 -*-


# Importaciones necesarias
from typing import Dict, List, Set, Optional, Tuple  # Tipos para anotaciones
from enum import Enum, auto  # Para enumeraciones
from dataclasses import dataclass, field  # Para clases de datos con menos boilerplate y valores por defecto
from collections import defaultdict  # Para diccionarios con valores por defecto

class TipoRelacion(Enum):
    """Tipos de relaciones semánticas posibles"""
    HIPERONIMO = auto()  # Relación "es-un" (ej: perro es-un animal)
    MERONIMO = auto()    # Relación "parte-de" (ej: pata es-parte-de perro)
    ATRIBUTO = auto()    # Relación de atributo (ej: perro tiene-propiedad color)
    INSTANCIA = auto()   # Relación de instancia (ej: Fido es-instancia-de perro)

class OperadorLogico(Enum):
    """Operadores para lógica descriptiva"""
    CONJUNCION = '∧'      # AND lógico
    DISYUNCION = '∨'      # OR lógico
    NEGACION = '¬'       # NOT lógico
    IMPLICACION = '→'    # Implicación
    EQUIVALENCIA = '≡'   # Equivalencia

@dataclass
class NodoSemantico:
    """Representa un concepto en la red semántica"""
    nombre: str,                                     # Identificador del concepto
    atributos: Dict[str, List[str]] = field(default_factory=dict),  # Propiedades del concepto (atributo -> lista de valores)
    relaciones: List[Tuple[TipoRelacion, str]] = field(default_factory=list)   # Relaciones con otros nodos (tipo de relación -> nombre del nodo destino)

@dataclass
class Regla:
    """Estructura para representar reglas de producción"""
    antecedente: List[str],        # Lista de condiciones (premisas)
    consecuente: str,              # Conclusión de la regla
    operador: OperadorLogico = OperadorLogico.IMPLICACION   # Operador lógico principal (por defecto es la implicación)

class SistemaConocimiento:
    """
    Sistema integrado que combina:
    - Redes semánticas
    - Reglas de producción
    - Lógica descriptiva
    """

    def __init__(self):
        """Inicializa las estructuras de conocimiento"""
        self.red_semantica: Dict[str, NodoSemantico] = {}   # Diccionario de nodos semánticos por su nombre
        self.reglas: List[Regla] = []                       # Lista de reglas de producción
        self.ontologia: Dict[str, Set[str]] = defaultdict(set)   # Jerarquía de conceptos (hiperónimo -> conjunto de hipónimos/merónimos)

    def agregar_nodo(self, nodo: NodoSemantico) -> bool:
        """
        Añade un nuevo nodo a la red semántica
        """
        if nodo.nombre in self.red_semantica:  # Comprueba si ya existe un nodo con el mismo nombre
            return False  # Retorna False si el nodo ya existe
        self.red_semantica[nodo.nombre] = nodo  # Añade el nuevo nodo al diccionario de la red semántica
        return True  # Retorna True si el nodo se añadió correctamente

    def agregar_relacion(self, origen: str, tipo: TipoRelacion, destino: str) -> bool:
        """
        Establece una relación semántica entre nodos
        """
        if origen not in self.red_semantica or destino not in self.red_semantica:  # Comprueba si ambos nodos existen en la red
            return False  # Retorna False si alguno de los nodos no existe
        self.red_semantica[origen].relaciones.append((tipo, destino))  # Añade la relación a la lista de relaciones del nodo origen
        if tipo == TipoRelacion.HIPERONIMO:  # Si la relación es de hiperónimo (es-un)
            self.ontologia[destino].add(origen)  # Añade el nodo origen como un tipo del nodo destino (ej: Animal -> Perro)
        elif tipo == TipoRelacion.MERONIMO:  # Si la relación es de merónimo (parte-de)
            self.ontologia[origen].add(destino)  # Añade el nodo destino como una parte del nodo origen (ej: Perro -> Pata)
        return True  # Retorna True si la relación se estableció correctamente

    def agregar_regla(self, regla: Regla) -> None:
        """
        Añade una nueva regla de producción al sistema
        """
        self.reglas.append(regla)  # Añade la regla a la lista de reglas de producción

    def inferir_conocimiento(self, hechos: Set[str]) -> Set[str]:
        """
        Aplica el encadenamiento hacia adelante para inferir nuevos hechos
        """
        nuevos_hechos = hechos.copy()  # Crea una copia del conjunto de hechos iniciales
        cambio = True  # Flag para controlar el bucle de inferencia
        while cambio:  # Continúa mientras se infieran nuevos hechos
            cambio = False  # Restablece el flag al inicio de cada iteración
            for regla in self.reglas:  # Itera sobre todas las reglas de producción
                if all(premisa in nuevos_hechos for premisa in regla.antecedente):  # Comprueba si todas las premisas de la regla están en el conjunto de hechos
                    if regla.consecuente not in nuevos_hechos:  # Comprueba si la conclusión de la regla ya es un hecho conocido
                        nuevos_hechos.add(regla.consecuente)  # Añade la conclusión al conjunto de hechos inferidos
                        cambio = True  # Marca que se ha inferido un nuevo hecho, por lo que se necesita otra iteración
        return nuevos_hechos  # Retorna el conjunto ampliado de hechos

    def obtener_subclases(self, concepto: str) -> Set[str]:
        """
        Obtiene todas las subclases de un concepto en la jerarquía
        """
        subclases = set()  # Conjunto para almacenar las subclases encontradas
        por_explorar = [concepto]  # Lista de conceptos a explorar (inicialmente el concepto dado)
        while por_explorar:  # Continúa mientras haya conceptos por explorar
            actual = por_explorar.pop(0)  # Obtiene el primer concepto de la lista
            for subclase in self.ontologia.get(actual, set()):  # Obtiene las subclases directas del concepto actual desde la ontología
                if subclase not in subclases:  # Si la subclase no ha sido visitada aún
                    subclases.add(subclase)  # Añade la subclase al conjunto de subclases
                    por_explorar.append(subclase)  # Añade la subclase a la lista de conceptos por explorar (para encontrar sus sub-subclases)
        return subclases  # Retorna el conjunto de todas las subclases encontradas

    def verificar_consistencia(self) -> List[str]:
        """
        Verifica consistencia básica del sistema de conocimiento
        """
        inconsistencias = []  # Lista para almacenar las inconsistencias encontradas
        for nombre, nodo in self.red_semantica.items():  # Itera sobre los nodos de la red semántica
            if not nodo.relaciones and nombre != "Thing":  # Comprueba si un nodo no tiene relaciones y no es "Thing"
                inconsistencias.append(f"Nodo aislado: {nombre}")  # Añade una inconsistencia si un nodo está aislado
        for i, regla in enumerate(self.reglas):  # Itera sobre las reglas de producción
            if not regla.antecedente:  # Comprueba si una regla no tiene antecedentes
                inconsistencias.append(f"Regla {i} sin antecedentes")  # Añade una inconsistencia si una regla no tiene premisas
        return inconsistencias  # Retorna la lista de inconsistencias encontradas

    def consultar_red(self, concepto: str) -> Optional[Dict]:
        """
        Consulta toda la información sobre un concepto en la red
        """
        if concepto not in self.red_semantica:  # Comprueba si el concepto existe en la red semántica
            return None  # Retorna None si el concepto no se encuentra
        nodo = self.red_semantica[concepto]  # Obtiene el nodo semántico del concepto
        return {  # Retorna un diccionario con la información del concepto
            "atributos": nodo.atributos,  # Atributos del concepto
            "relaciones": [  # Lista de relaciones del concepto
                {"tipo": tipo.name, "destino": dest}  # Formatea cada relación como un diccionario
                for tipo, dest in nodo.relaciones  # Itera sobre las relaciones del nodo
            ],
            "subclases": list(self.obtener_subclases(concepto))  # Lista de todas las subclases del concepto
        }

def demostracion_sistema():
    """
    Función de demostración del sistema integrado de conocimiento
    """
    sistema = SistemaConocimiento()  # Crea una instancia del sistema de conocimiento
    sistema.agregar_nodo(NodoSemantico("Animal", {"movimiento": ["voluntario"]}))  # Crea y añade el nodo "Animal" con un atributo
    sistema.agregar_nodo(NodoSemantico("Perro", {"patas": ["4"], "sonido": ["ladrido"]}))  # Crea y añade el nodo "Perro" con atributos
    sistema.agregar_nodo(NodoSemantico("Gato", {"patas": ["4"], "sonido": ["maullido"]}))  # Crea y añade el nodo "Gato" con atributos
    sistema.agregar_nodo(NodoSemantico("Pata", {"funcion": ["caminar"]}))  # Crea y añade el nodo "Pata" con un atributo
    sistema.agregar_relacion("Perro", TipoRelacion.HIPERONIMO, "Animal")  # Establece que "Perro" es un tipo de "Animal"
    sistema.agregar_relacion("Gato", TipoRelacion.HIPERONIMO, "Animal")  # Establece que "Gato" es un tipo de "Animal"
    sistema.agregar_relacion("Pata", TipoRelacion.MERONIMO, "Perro")  # Establece que "Pata" es parte de "Perro"
    sistema.agregar_relacion("Pata", TipoRelacion.MERONIMO, "Gato")  # Establece que "Pata" es parte de "Gato"
    sistema.agregar_regla(Regla(antecedente=["Perro(x)"], consecuente="Tiene_patas(x)", operador=OperadorLogico.IMPLICACION))  # Añade una regla: Si es un perro, entonces tiene patas
    sistema.agregar_regla(Regla(antecedente=["Gato(x)"], consecuente="Tiene_patas(x)", operador=OperadorLogico.IMPLICACION))  # Añade una regla: Si es un gato, entonces tiene patas
    sistema.agregar_regla(Regla(antecedente=["Animal(x)", "Tiene_patas(x)"], consecuente="Puede_caminar(x)", operador=OperadorLogico.IMPLICACION))  # Añade una regla: Si es un animal y tiene patas, entonces puede caminar
    hechos_iniciales = {"Perro(Fido)", "Gato(Garfiel)"}  # Define un conjunto de hechos iniciales
    hechos_inferidos = sistema.inferir_conocimiento(hechos_iniciales)  # Realiza la inferencia basada en los hechos y las reglas
    consulta_perro = sistema.consultar_red("Perro")  # Consulta la información sobre el concepto "Perro" en la red semántica
    subclases_animal = sistema.obtener_subclases("Animal")  # Obtiene todas las subclases del concepto "Animal"
    print("=== DEMOSTRACIÓN SISTEMA DE CONOCIMIENTO ===")  # Imprime un encabezado
    print("\nHechos iniciales:", hechos_iniciales)  # Imprime los hechos iniciales
    print("Hechos inferidos:", hechos_inferidos)  # Imprime los hechos que se pudieron inferir
    print("\nConsulta 'Perro':")  # Imprime un encabezado para la consulta de "Perro"
    if consulta_perro:  # Comprueba si se encontró información sobre "Perro"
        for k, v in consulta_perro.items():  # Itera sobre la información encontrada
            print(f"{k}: {v}")  # Imprime la clave y el valor de la información
    else:  # Si no se encontró información
        print("No se encontró información sobre 'Perro'.")  # Imprime un mensaje indicando que no se encontró información
    print("\nSubclases de 'Animal':", subclases_animal)  # Imprime las subclases encontradas para "Animal"
    print("\nInconsistencias detectadas:", sistema.verificar_consistencia())  # Imprime cualquier inconsistencia básica detectada en el sistema

if __name__ == "__main__":
    demostracion_sistema()  # Llama a la función de demostración cuando el script se ejecuta directamente