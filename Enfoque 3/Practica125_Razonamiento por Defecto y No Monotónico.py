# -*- coding: utf-8 -*-


# Importaciones necesarias
from typing import Dict, List, Set, Optional, Tuple  # Tipos para anotaciones
from enum import Enum, auto  # Para enumeraciones
from dataclasses import dataclass  # Para clases de datos con menos boilerplate
from collections import defaultdict  # Para diccionarios con valores por defecto

class EstadoCreencia(Enum):
    """Estados en los que puede estar una creencia"""
    ACTIVA = auto()        # Creencia actualmente aceptada
    DERROTADA = auto()     # Creencia invalidada por nueva información
    INCIERTA = auto()      # Creencia con soporte insuficiente

class TipoRegla(Enum):
    """Tipos de reglas no monotónicas"""
    DEFAULT = auto()       # Regla por defecto (razonamiento por defecto)
    DEFEASIBLE = auto()    # Regla anulable (derrotable)
    ESTRICTA = auto()      # Regla clásica (no anulable)

@dataclass
class Creencia:
    """Estructura para representar creencias con razonamiento no monotónico"""
    contenido: str              # Proposición de la creencia
    estado: EstadoCreencia      # Estado actual de la creencia
    soporte: Set[str]           # Conjunto de premisas que la apoyan
    reglas_afectadas: List[str]  # Reglas que pueden afectar esta creencia

@dataclass
class ReglaNoMonotonica:
    """Representación de reglas con excepciones"""
    nombre: str                  # Identificador de la regla
    tipo: TipoRegla              # Tipo de regla
    antecedente: List[str]       # Premisas requeridas
    consecuente: str            # Conclusión de la regla
    excepciones: List[str]       # Condiciones que invalidan la regla
    prioridad: int = 0           # Nivel de prioridad para resolver conflictos

class SistemaNoMonotonico:
    """
    Sistema de razonamiento no monotónico que implementa:
    - Razonamiento por defecto
    - Reglas derrotables
    - Actualización de creencias
    """

    def __init__(self):
        """Inicializa el sistema con estructuras básicas"""
        self.creencias: Dict[str, Creencia] = {}      # Diccionario de creencias
        self.reglas: Dict[str, ReglaNoMonotonica] = {}  # Reglas del sistema
        self.hechos_observados: Set[str] = set()      # Hechos conocidos
        self.historial: List[Tuple[str, str]] = []    # Historial de cambios

    def agregar_regla(self, regla: ReglaNoMonotonica) -> None:
        """
        Añade una nueva regla al sistema

        Args:
            regla (ReglaNoMonotonica): Regla a añadir
        """
        self.reglas[regla.nombre] = regla  # Agrega la regla al diccionario de reglas usando su nombre como clave

    def observar_hecho(self, hecho: str) -> None:
        """
        Añade un hecho observado al sistema y actualiza las creencias

        Args:
            hecho (str): Hecho observado que puede afectar el sistema
        """
        self.hechos_observados.add(hecho)  # Añade el hecho observado al conjunto de hechos observados
        self.actualizar_creencias()  # Llama al método para actualizar las creencias basadas en el nuevo hecho

    def actualizar_creencias(self) -> None:
        """
        Re-evalúa todas las creencias basadas en la información actual
        y aplica el razonamiento no monotónico
        """
        # Primero desactivar todas las creencias derivadas
        for nombre, creencia in self.creencias.items():  # Itera sobre todas las creencias en el sistema
            if not creencia.soporte:  # No cambiar hechos observados
                continue  # Si la creencia no tiene soporte (es un hecho observado), se omite
            creencia.estado = EstadoCreencia.INCIERTA  # Establece el estado de la creencia como INCIERTA (para re-evaluar)

        # Aplicar todas las reglas para generar nuevas creencias
        for regla in self.reglas.values():  # Itera sobre todas las reglas en el sistema
            self.aplicar_regla(regla)  # Intenta aplicar cada regla

        # Verificar conflictos y derrotar creencias si es necesario
        self.resolver_conflictos()  # Llama al método para resolver conflictos entre creencias

    def aplicar_regla(self, regla: ReglaNoMonotonica) -> bool:
        """
        Intenta aplicar una regla para generar nuevas creencias

        Args:
            regla (ReglaNoMonotonica): Regla a aplicar

        Returns:
            bool: True si la regla pudo aplicarse, False si no
        """
        # Verificar si todas las premisas se cumplen
        premisas_cumplidas = all(  # Comprueba si todas las premisas de la regla se cumplen
            prem in self.hechos_observados or  # Una premisa se cumple si es un hecho observado
            (prem in self.creencias and self.creencias[prem].estado == EstadoCreencia.ACTIVA)  # o si es una creencia activa
            for prem in regla.antecedente  # Itera sobre las premisas de la regla
        )

        # Verificar si alguna excepción se cumple
        excepcion_cumplida = any(  # Comprueba si alguna de las excepciones de la regla se cumple
            exc in self.hechos_observados or  # Una excepción se cumple si es un hecho observado
            (exc in self.creencias and self.creencias[exc].estado == EstadoCreencia.ACTIVA)  # o si es una creencia activa
            for exc in regla.excepciones  # Itera sobre las excepciones de la regla
        )

        if premisas_cumplidas and not excepcion_cumplida:  # Si todas las premisas se cumplen y ninguna excepción se cumple
            # Crear o actualizar la creencia resultante
            if regla.consecuente not in self.creencias:  # Si la creencia consecuente no existe aún
                self.creencias[regla.consecuente] = Creencia(  # Crea una nueva creencia
                    contenido=regla.consecuente,
                    estado=EstadoCreencia.ACTIVA,
                    soporte=set(regla.antecedente),
                    reglas_afectadas=[regla.nombre]
                )
            else:  # Si la creencia consecuente ya existe
                creencia = self.creencias[regla.consecuente]  # Obtiene la creencia existente
                creencia.soporte.update(regla.antecedente)  # Actualiza el soporte de la creencia con las premisas de la regla
                creencia.reglas_afectadas.append(regla.nombre)  # Añade el nombre de la regla a las reglas que afectan esta creencia
                creencia.estado = EstadoCreencia.ACTIVA  # Establece el estado de la creencia como ACTIVA

            # Registrar en el historial
            self.historial.append((f"Aplicada regla {regla.nombre}", regla.consecuente))  # Añade un registro al historial
            return True  # Retorna True si la regla se aplicó

        return False  # Retorna False si la regla no se pudo aplicar

    def resolver_conflictos(self) -> None:
        """
        Resuelve conflictos entre creencias basadas en prioridades de reglas
        """
        # Buscar creencias conflictivas
        conflictos: Dict[str, List[str]] = defaultdict(list)  # Diccionario para almacenar conflictos (creencia -> lista de creencias derrotadas)

        for nombre, creencia in self.creencias.items():  # Itera sobre todas las creencias activas
            if creencia.estado == EstadoCreencia.ACTIVA:
                for regla_nombre in creencia.reglas_afectadas:  # Itera sobre las reglas que llevaron a esta creencia
                    regla = self.reglas[regla_nombre]  # Obtiene la regla
                    # Verificar si esta regla derrota otras
                    for otra_creencia in self.creencias.values():  # Itera sobre todas las creencias
                        if otra_creencia.contenido in regla.excepciones:  # Si otra creencia coincide con una excepción de la regla actual
                            conflictos[nombre].append(otra_creencia.contenido)  # Registra un conflicto potencial

        # Resolver conflictos basados en prioridad
        for creencia, derrotadas in conflictos.items():  # Itera sobre los conflictos encontrados
            for derrotada in derrotadas:  # Itera sobre las creencias que podrían ser derrotadas
                if derrotada in self.creencias:  # Asegura que la creencia derrotada aún existe
                    # Comparar prioridades de reglas
                    max_prioridad_creencia = max(  # Obtiene la máxima prioridad de las reglas que soportan la creencia actual
                        self.reglas[r].prioridad
                        for r in self.creencias[creencia].reglas_afectadas
                    )
                    max_prioridad_derrotada = max(  # Obtiene la máxima prioridad de las reglas que soportan la creencia derrotada
                        self.reglas[r].prioridad
                        for r in self.creencias[derrotada].reglas_afectadas
                    )

                    if max_prioridad_creencia > max_prioridad_derrotada:  # Si la prioridad de la regla de la creencia actual es mayor
                        self.creencias[derrotada].estado = EstadoCreencia.DERROTADA  # Marca la otra creencia como DERROTADA
                        self.historial.append((f"Derrotada {derrotada}", f"por {creencia}"))  # Registra la derrota en el historial

    def consultar_creencia(self, proposicion: str) -> Optional[EstadoCreencia]:
        """
        Consulta el estado actual de una creencia

        Args:
            proposicion (str): Proposición a consultar

        Returns:
            Optional[EstadoCreencia]: Estado de la creencia o None si no existe
        """
        if proposicion in self.creencias:  # Comprueba si la proposición existe como una creencia
            return self.creencias[proposicion].estado  # Retorna el estado de la creencia
        return None  # Retorna None si la creencia no existe

    def generar_informe(self) -> Dict:
        """
        Genera un informe del estado actual del sistema

        Returns:
            Dict: Diccionario con estadísticas del sistema
        """
        return {  # Retorna un diccionario con estadísticas del sistema
            "total_creencias": len(self.creencias),  # Número total de creencias en el sistema
            "creencias_activas": sum(1 for c in self.creencias.values()
                                    if c.estado == EstadoCreencia.ACTIVA),  # Número de creencias activas
            "creencias_derrotadas": sum(1 for c in self.creencias.values()
                                       if c.estado == EstadoCreencia.DERROTADA),  # Número de creencias derrotadas
            "total_reglas": len(self.reglas),  # Número total de reglas en el sistema
            "hechos_observados": len(self.hechos_observados)  # Número de hechos observados
        }

def demostracion_razonamiento_default():
    """
    Demuestra el razonamiento por defecto con el clásico ejemplo de los pájaros
    """
    sistema = SistemaNoMonotonico()  # Crea una instancia del sistema de razonamiento no monotónico

    # 1. Definir reglas
    sistema.agregar_regla(ReglaNoMonotonica(  # Define una regla por defecto: los pájaros vuelan
        nombre="default_pajaro_vuela",
        tipo=TipoRegla.DEFAULT,
        antecedente=["Pájaro(x)"],
        consecuente="Vuela(x)",
        excepciones=["Pingüino(x)", "Herido(x)"],
        prioridad=1
    ))

    sistema.agregar_regla(ReglaNoMonotonica(  # Define una regla derrotable: los pingüinos no vuelan (con mayor prioridad)
        nombre="pinguino_no_vuela",
        tipo=TipoRegla.DEFEASIBLE,
        antecedente=["Pingüino(x)"],
        consecuente="¬Vuela(x)",
        excepciones=[],
        prioridad=2  # Mayor prioridad que la regla por defecto
    ))

    # 2. Observar hechos iniciales
    sistema.observar_hecho("Pájaro(Tweety)")  # Se observa que Tweety es un pájaro

    print("\nEstado inicial:")
    print("Tweety vuela?", sistema.consultar_creencia("Vuela(Tweety)"))  # Consulta si se cree que Tweety vuela (debería ser ACTIVA por la regla por defecto)

    # 3. Añadir nueva información (Tweety es un pingüino)
    sistema.observar_hecho("Pingüino(Tweety)")  # Se observa que Tweety es un pingüino

    print("\nDespués de saber que Tweety es un pingüino:")
    print("Tweety vuela?", sistema.consultar_creencia("Vuela(Tweety)"))  # Consulta si se cree ahora que Tweety vuela (debería ser DERROTADA por la regla del pingüino)

    # 4. Mostrar informe final
    print("\nInforme del sistema:")
    for k, v in sistema.generar_informe().items():  # Genera e imprime el informe del estado del sistema
        print(f"{k}: {v}")

if __name__ == "__main__":
    demostracion_razonamiento_default()  # Llama a la función de demostración cuando el script se ejecuta directamente