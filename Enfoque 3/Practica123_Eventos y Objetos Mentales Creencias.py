# -*- coding: utf-8 -*-


# Importaciones necesarias para el código
from typing import Dict, List, Optional, Set  # Tipos para anotaciones
from enum import Enum, auto  # Para enumeraciones
from dataclasses import dataclass, field  # Para clases de datos con menos boilerplate

class TipoObjetoMental(Enum):
    """Enumeración de los tipos de objetos mentales posibles"""
    CREENCIA = auto()     # Representa una creencia sobre el mundo
    DESEO = auto()        # Representa un deseo o preferencia
    INTENCION = auto()    # Representa una intención de actuar

class GradoCertidumbre(Enum):
    """Escala de certidumbre para las creencias"""
    SEGURO = 3          # Máxima certeza
    PROBABLE = 2        # Creencia probable
    INCIERTO = 1        # Creencia con baja certeza
    DESCONOCIDO = 0     # Sin información

@dataclass
class ObjetoMental:
    """
    Clase base para representar objetos mentales (creencias, deseos, intenciones)
    """
    id: str                      # Identificador único
    tipo: TipoObjetoMental      # Tipo de objeto mental
    contenido: str              # Contenido proposicional
    fuente: str                  # Cómo se originó esta creencia
    grado: GradoCertidumbre      # Nivel de certidumbre
    soporte: Set[str] = field(default_factory=set)  # Evidencia que soporta esta creencia

@dataclass
class Evento:
    """
    Representa un evento que puede afectar o generar creencias
    """
    id: str                      # Identificador único
    tipo: str                    # Tipo de evento (ej. 'observación', 'comunicación')
    participantes: List[str]     # Agentes involucrados
    momento: float                # Marca temporal del evento
    datos: Dict[str, str]         # Información asociada al evento

class SistemaCreencias:
    """
    Sistema que maneja la red de creencias y eventos de un agente cognitivo
    """
    def __init__(self, agente_id: str):
        """
        Inicializa el sistema de creencias para un agente específico

        Args:
            agente_id (str): Identificador único del agente
        """
        self.agente_id = agente_id  # ID del agente dueño del sistema
        self.creencias: Dict[str, ObjetoMental] = {}  # Diccionario de creencias por ID
        self.eventos: Dict[str, Evento] = {}  # Registro de eventos conocidos
        self.contradicciones: Dict[str, List[str]] = {}  # Relación de creencias contradictorias

    def agregar_creencia(self, creencia: ObjetoMental) -> bool:
        """
        Añade una nueva creencia al sistema después de validarla

        Args:
            creencia (ObjetoMental): Creencia a añadir

        Returns:
            bool: True si se añadió exitosamente, False si ya existía
        """
        if creencia.id in self.creencias:  # Comprueba si la creencia ya existe en el diccionario de creencias
            return False  # Retorna False si la creencia ya existe
        self.creencias[creencia.id] = creencia  # Añade la creencia al diccionario de creencias usando su ID como clave
        self._verificar_contradicciones(creencia)  # Llama al método interno para verificar si la nueva creencia contradice alguna existente
        return True  # Retorna True si la creencia se añadió exitosamente

    def _verificar_contradicciones(self, nueva_creencia: ObjetoMental):
        """
        Método interno para detectar contradicciones con creencias existentes

        Args:
            nueva_creencia (ObjetoMental): Creencia recién añadida
        """
        for creencia_id, creencia_existente in self.creencias.items():  # Itera sobre todas las creencias existentes en el sistema
            if (creencia_existente.contenido == nueva_creencia.contenido and  # Comprueba si el contenido de la creencia existente es igual al de la nueva creencia
                    creencia_existente.tipo != nueva_creencia.tipo):  # Y si los tipos de objeto mental son diferentes
                # Registrar contradicción
                if creencia_id not in self.contradicciones:  # Si la creencia existente no tiene contradicciones registradas
                    self.contradicciones[creencia_id] = []  # Inicializa una lista para almacenar las IDs de las creencias contradictorias
                self.contradicciones[creencia_id].append(nueva_creencia.id)  # Añade la ID de la nueva creencia a la lista de contradicciones de la creencia existente

    def registrar_evento(self, evento: Evento) -> bool:
        """
        Registra un nuevo evento en el sistema y actualiza creencias relacionadas

        Args:
            evento (Evento): Evento a registrar

        Returns:
            bool: True si se registró exitosamente
        """
        if evento.id in self.eventos:  # Comprueba si el evento ya existe en el diccionario de eventos
            return False  # Retorna False si el evento ya existe
        self.eventos[evento.id] = evento  # Añade el evento al diccionario de eventos usando su ID como clave

        # Si el evento es una observación directa, crear creencia asociada
        if evento.tipo == 'observacion' and self.agente_id in evento.participantes:  # Comprueba si el evento es una observación realizada por el agente
            contenido = f"Observado({evento.datos.get('objeto')}, {evento.datos.get('propiedad')})"  # Crea el contenido de la nueva creencia basada en los datos del evento
            nueva_creencia = ObjetoMental(  # Crea un nuevo objeto mental de tipo CREENCIA
                id=f"creencia_{evento.id}",
                tipo=TipoObjetoMental.CREENCIA,
                contenido=contenido,
                fuente=evento.id,
                grado=GradoCertidumbre.SEGURO
            )
            self.agregar_creencia(nueva_creencia)  # Añade la nueva creencia al sistema de creencias

        return True  # Retorna True si el evento se registró exitosamente

    def actualizar_creencia(self, creencia_id: str, nuevo_grado: GradoCertidumbre) -> bool:
        """
        Actualiza el grado de certidumbre de una creencia existente

        Args:
            creencia_id (str): ID de la creencia a actualizar
            nuevo_grado (GradoCertidumbre): Nuevo nivel de certidumbre

        Returns:
            bool: True si se actualizó, False si no existe la creencia
        """
        if creencia_id not in self.creencias:  # Comprueba si la creencia con la ID dada existe
            return False  # Retorna False si la creencia no existe
        self.creencias[creencia_id].grado = nuevo_grado  # Actualiza el grado de certidumbre de la creencia
        return True  # Retorna True si la creencia se actualizó

    def obtener_creencias_por_tipo(self, tipo: TipoObjetoMental) -> List[ObjetoMental]:
        """
        Filtra y devuelve creencias por tipo específico

        Args:
            tipo (TipoObjetoMental): Tipo de creencias a filtrar

        Returns:
            List[ObjetoMental]: Lista de creencias del tipo solicitado
        """
        return [creencia for creencia in self.creencias.values() if creencia.tipo == tipo]  # Retorna una lista de objetos mentales cuyo tipo coincide con el tipo especificado

    def generar_informe(self) -> Dict:
        """
        Genera un informe resumido del estado del sistema de creencias

        Returns:
            Dict: Diccionario con estadísticas del sistema
        """
        return {  # Retorna un diccionario con estadísticas del sistema de creencias
            "total_creencias": len(self.creencias),  # Número total de creencias en el sistema
            "creencias_seguras": sum(1 for c in self.creencias.values() if c.grado == GradoCertidumbre.SEGURO),  # Número de creencias con grado de certidumbre SEGURO
            "total_eventos": len(self.eventos),  # Número total de eventos registrados
            "contradicciones_detectadas": sum(len(v) for v in self.contradicciones.values())  # Número total de contradicciones detectadas
        }

def demostracion_sistema():
    """
    Función de demostración que muestra el uso del sistema de creencias
    """
    # 1. Crear sistema de creencias para un agente
    sistema = SistemaCreencias(agente_id="agente_1")  # Crea una instancia del sistema de creencias para un agente con ID "agente_1"

    # 2. Registrar algunos eventos iniciales
    sistema.registrar_evento(Evento(  # Registra un evento de tipo "observacion"
        id="evento_1",
        tipo="observacion",
        participantes=["agente_1"],
        momento=1.0,
        datos={"objeto": "mesa", "propiedad": "color_rojo"}
    ))

    sistema.registrar_evento(Evento(  # Registra un evento de tipo "comunicacion"
        id="evento_2",
        tipo="comunicacion",
        participantes=["agente_1", "agente_2"],
        momento=2.0,
        datos={"emisor": "agente_2", "mensaje": "La mesa es azul"}
    ))

    # 3. Añadir algunas creencias manualmente
    sistema.agregar_creencia(ObjetoMental(  # Añade una creencia de tipo DESEO
        id="creencia_1",
        tipo=TipoObjetoMental.DESEO,
        contenido="Prefiero ambientes tranquilos",
        fuente="interna",
        grado=GradoCertidumbre.SEGURO
    ))

    # 4. Mostrar estado del sistema
    print("\n=== INFORME DEL SISTEMA ===")  # Imprime un encabezado para el informe del sistema
    informe = sistema.generar_informe()  # Genera un informe del estado del sistema
    for k, v in informe.items():  # Itera sobre los elementos del informe
        print(f"{k.replace('_', ' ').title()}: {v}")  # Imprime cada clave del informe con formato de título y su valor

    print("\nCreencias de tipo CREENCIA:")  # Imprime un encabezado para las creencias de tipo CREENCIA
    for creencia in sistema.obtener_creencias_por_tipo(TipoObjetoMental.CREENCIA):  # Obtiene y itera sobre las creencias de tipo CREENCIA
        print(f"- {creencia.contenido} (Certidumbre: {creencia.grado.name})")  # Imprime el contenido y el grado de certidumbre de cada creencia

    print("\nEventos registrados:")  # Imprime un encabezado para los eventos registrados
    for evento in sistema.eventos.values():  # Itera sobre todos los eventos registrados
        print(f"- {evento.tipo} en t={evento.momento}: {evento.datos}")  # Imprime el tipo, momento y datos de cada evento

if __name__ == "__main__":
    demostracion_sistema()  # Llama a la función de demostración cuando el script se ejecuta directamente