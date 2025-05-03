# -*- coding: utf-8 -*-


# Importaciones necesarias para el código
from typing import Dict, List, Optional, Set  # Tipos para anotaciones
from enum import Enum, auto  # Para enumeraciones
from dataclasses import dataclass, field  # Para clases de datos con menos boilerplate

class TipoObjetoMental(Enum):
    """Enumeración de los tipos de objetos mentales posibles"""
    CREENCIA = auto()      # Representa una creencia sobre el mundo
    DESEO = auto()         # Representa un deseo o preferencia
    INTENCION = auto()     # Representa una intención de actuar

class GradoCertidumbre(Enum):
    """Escala de certidumbre para las creencias"""
    SEGURO = 3            # Máxima certeza
    PROBABLE = 2          # Creencia probable
    INCIERTO = 1          # Creencia con baja certeza
    DESCONOCIDO = 0       # Sin información

@dataclass
class ObjetoMental:
    """
    Clase base para representar objetos mentales (creencias, deseos, intenciones)
    """
    id: str                       # Identificador único
    tipo: TipoObjetoMental        # Tipo de objeto mental
    contenido: str                # Contenido proposicional
    fuente: str                   # Cómo se originó esta creencia
    grado: GradoCertidumbre       # Nivel de certidumbre
    soporte: Set[str] = field(default_factory=set)  # Evidencia que soporta esta creencia

@dataclass
class Evento:
    """
    Representa un evento que puede afectar o generar creencias
    """
    id: str                       # Identificador único
    tipo: str                     # Tipo de evento (ej. 'observación', 'comunicación')
    participantes: List[str]      # Agentes involucrados
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
        if creencia.id in self.creencias:
            return False
            
        self.creencias[creencia.id] = creencia
        self._verificar_contradicciones(creencia)
        return True

    def _verificar_contradicciones(self, nueva_creencia: ObjetoMental):
        """
        Método interno para detectar contradicciones con creencias existentes
        
        Args:
            nueva_creencia (ObjetoMental): Creencia recién añadida
        """
        for creencia_id, creencia_existente in self.creencias.items():
            if (creencia_existente.contenido == nueva_creencia.contenido and 
                creencia_existente.tipo != nueva_creencia.tipo):
                # Registrar contradicción
                if creencia_id not in self.contradicciones:
                    self.contradicciones[creencia_id] = []
                self.contradicciones[creencia_id].append(nueva_creencia.id)

    def registrar_evento(self, evento: Evento) -> bool:
        """
        Registra un nuevo evento en el sistema y actualiza creencias relacionadas
        
        Args:
            evento (Evento): Evento a registrar
            
        Returns:
            bool: True si se registró exitosamente
        """
        if evento.id in self.eventos:
            return False
            
        self.eventos[evento.id] = evento
        
        # Si el evento es una observación directa, crear creencia asociada
        if evento.tipo == 'observacion' and self.agente_id in evento.participantes:
            contenido = f"Observado({evento.datos.get('objeto')}, {evento.datos.get('propiedad')})"
            nueva_creencia = ObjetoMental(
                id=f"creencia_{evento.id}",
                tipo=TipoObjetoMental.CREENCIA,
                contenido=contenido,
                fuente=evento.id,
                grado=GradoCertidumbre.SEGURO
            )
            self.agregar_creencia(nueva_creencia)
            
        return True

    def actualizar_creencia(self, creencia_id: str, nuevo_grado: GradoCertidumbre) -> bool:
        """
        Actualiza el grado de certidumbre de una creencia existente
        
        Args:
            creencia_id (str): ID de la creencia a actualizar
            nuevo_grado (GradoCertidumbre): Nuevo nivel de certidumbre
            
        Returns:
            bool: True si se actualizó, False si no existe la creencia
        """
        if creencia_id not in self.creencias:
            return False
            
        self.creencias[creencia_id].grado = nuevo_grado
        return True

    def obtener_creencias_por_tipo(self, tipo: TipoObjetoMental) -> List[ObjetoMental]:
        """
        Filtra y devuelve creencias por tipo específico
        
        Args:
            tipo (TipoObjetoMental): Tipo de creencias a filtrar
            
        Returns:
            List[ObjetoMental]: Lista de creencias del tipo solicitado
        """
        return [creencia for creencia in self.creencias.values() if creencia.tipo == tipo]

    def generar_informe(self) -> Dict:
        """
        Genera un informe resumido del estado del sistema de creencias
        
        Returns:
            Dict: Diccionario con estadísticas del sistema
        """
        return {
            "total_creencias": len(self.creencias),
            "creencias_seguras": sum(1 for c in self.creencias.values() if c.grado == GradoCertidumbre.SEGURO),
            "total_eventos": len(self.eventos),
            "contradicciones_detectadas": sum(len(v) for v in self.contradicciones.values())
        }

def demostracion_sistema():
    """
    Función de demostración que muestra el uso del sistema de creencias
    """
    # 1. Crear sistema de creencias para un agente
    sistema = SistemaCreencias(agente_id="agente_1")
    
    # 2. Registrar algunos eventos iniciales
    sistema.registrar_evento(Evento(
        id="evento_1",
        tipo="observacion",
        participantes=["agente_1"],
        momento=1.0,
        datos={"objeto": "mesa", "propiedad": "color_rojo"}
    ))
    
    sistema.registrar_evento(Evento(
        id="evento_2",
        tipo="comunicacion",
        participantes=["agente_1", "agente_2"],
        momento=2.0,
        datos={"emisor": "agente_2", "mensaje": "La mesa es azul"}
    ))
    
    # 3. Añadir algunas creencias manualmente
    sistema.agregar_creencia(ObjetoMental(
        id="creencia_1",
        tipo=TipoObjetoMental.DESEO,
        contenido="Prefiero ambientes tranquilos",
        fuente="interna",
        grado=GradoCertidumbre.SEGURO
    ))
    
    # 4. Mostrar estado del sistema
    print("\n=== INFORME DEL SISTEMA ===")
    informe = sistema.generar_informe()
    for k, v in informe.items():
        print(f"{k.replace('_', ' ').title()}: {v}")
    
    print("\nCreencias de tipo CREENCIA:")
    for creencia in sistema.obtener_creencias_por_tipo(TipoObjetoMental.CREENCIA):
        print(f"- {creencia.contenido} (Certidumbre: {creencia.grado.name})")
    
    print("\nEventos registrados:")
    for evento in sistema.eventos.values():
        print(f"- {evento.tipo} en t={evento.momento}: {evento.datos}")

if __name__ == "__main__":
    demostracion_sistema()