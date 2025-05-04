"""
INTERFACES, MENSAJES Y EVENTOS - 
---------------------------------------------------------
Este código demuestra los conceptos de:
1. Interfaces (clases abstractas)
2. Paso de mensajes entre objetos
3. Sistema de eventos (publicación/suscripción)
"""

# ============ IMPORTACIONES ============
from abc import ABC, abstractmethod
from typing import List, Dict, Callable, Any
from dataclasses import dataclass
from enum import Enum
import time

# ============ INTERFACES (CLASES ABSTRACTAS) ============
class DispositivoElectronico(ABC):
    """Interfaz abstracta para dispositivos electrónicos"""
    
    @abstractmethod
    def encender(self) -> None:
        """Encender el dispositivo"""
        pass
    
    @abstractmethod
    def apagar(self) -> None:
        """Apagar el dispositivo"""
        pass
    
    @abstractmethod
    def estado(self) -> str:
        """Obtener estado actual"""
        pass

class DispositivoInteligente(DispositivoElectronico):
    """Interfaz extendida para dispositivos inteligentes"""
    
    @abstractmethod
    def conectar(self, red: str) -> bool:
        """Conectar a una red WiFi"""
        pass
    
    @abstractmethod
    def recibir_mensaje(self, mensaje: str) -> None:
        """Recibir un mensaje del sistema"""
        pass

# ============ MENSAJES ============
@dataclass
class Mensaje:
    """Estructura para mensajes entre objetos"""
    remitente: str
    destinatario: str
    contenido: Any
    timestamp: float = time.time()

# ============ SISTEMA DE EVENTOS ============
class TipoEvento(Enum):
    """Tipos de eventos en el sistema"""
    DISPOSITIVO_ENCENDIDO = auto()
    DISPOSITIVO_APAGADO = auto()
    MENSAJE_RECIBIDO = auto()
    ERROR = auto()

@dataclass
class Evento:
    """Estructura para eventos del sistema"""
    tipo: TipoEvento
    origen: str
    datos: Dict[str, Any] = None
    timestamp: float = time.time()

class PublicadorEventos:
    """Clase base para objetos que publican eventos"""
    
    def __init__(self):
        self._suscriptores: Dict[TipoEvento, List[Callable]] = {}
    
    def suscribir(self, evento: TipoEvento, callback: Callable) -> None:
        """Suscribir una función a un tipo de evento"""
        if evento not in self._suscriptores:
            self._suscriptores[evento] = []
        self._suscriptores[evento].append(callback)
    
    def _notificar(self, evento: Evento) -> None:
        """Notificar a los suscriptores sobre un evento"""
        if evento.tipo in self._suscriptores:
            for callback in self._suscriptores[evento.tipo]:
                callback(evento)

# ============ IMPLEMENTACIONES CONCRETAS ============
class BombillaInteligente(DispositivoInteligente, PublicadorEventos):
    """Implementación concreta de una bombilla inteligente"""
    
    def __init__(self, id: str):
        super().__init__()
        self.id = id
        self._encendida = False
        self._conectada = False
        self._red_wifi = ""
    
    def encender(self) -> None:
        if not self._encendida:
            self._encendida = True
            print(f"{self.id}: Bombilla encendida")
            self._notificar(Evento(
                TipoEvento.DISPOSITIVO_ENCENDIDO,
                self.id,
                {"nivel_luz": 100}
            ))
    
    def apagar(self) -> None:
        if self._encendida:
            self._encendida = False
            print(f"{self.id}: Bombilla apagada")
            self._notificar(Evento(
                TipoEvento.DISPOSITIVO_APAGADO,
                self.id
            ))
    
    def estado(self) -> str:
        return (f"Bombilla {self.id}: "
                f"{'Encendida' if self._encendida else 'Apagada'}, "
                f"{'Conectada' if self._conectada else 'Desconectada'}")
    
    def conectar(self, red: str) -> bool:
        self._conectada = True
        self._red_wifi = red
        print(f"{self.id}: Conectada a {red}")
        return True
    
    def recibir_mensaje(self, mensaje: str) -> None:
        print(f"{self.id}: Mensaje recibido - {mensaje}")
        self._notificar(Evento(
            TipoEvento.MENSAJE_RECIBIDO,
            self.id,
            {"mensaje": mensaje}
        ))

class TermostatoInteligente(DispositivoInteligente, PublicadorEventos):
    """Implementación concreta de un termostato inteligente"""
    
    def __init__(self, id: str):
        super().__init__()
        self.id = id
        self._encendido = False
        self._temperatura = 20.0
        self._conectado = False
    
    def encender(self) -> None:
        if not self._encendido:
            self._encendido = True
            print(f"{self.id}: Termostato encendido")
            self._notificar(Evento(
                TipoEvento.DISPOSITIVO_ENCENDIDO,
                self.id,
                {"temperatura": self._temperatura}
            ))
    
    def apagar(self) -> None:
        if self._encendido:
            self._encendido = False
            print(f"{self.id}: Termostato apagado")
            self._notificar(Evento(
                TipoEvento.DISPOSITIVO_APAGADO,
                self.id
            ))
    
    def estado(self) -> str:
        return (f"Termostato {self.id}: "
                f"{'Encendido' if self._encendido else 'Apagado'}, "
                f"Temp: {self._temperatura}°C")
    
    def conectar(self, red: str) -> bool:
        self._conectado = True
        print(f"{self.id}: Conectado a {red}")
        return True
    
    def recibir_mensaje(self, mensaje: str) -> None:
        print(f"{self.id}: Mensaje recibido - {mensaje}")
        if "set_temp:" in mensaje:
            nueva_temp = float(mensaje.split(":")[1])
            self._temperatura = nueva_temp
            print(f"{self.id}: Temperatura cambiada a {nueva_temp}°C")
        
        self._notificar(Evento(
            TipoEvento.MENSAJE_RECIBIDO,
            self.id,
            {"mensaje": mensaje, "temperatura": self._temperatura}
        ))

# ============ CENTRALITA INTELIGENTE ============
class CentralitaInteligente:
    """Sistema central que gestiona dispositivos y mensajes"""
    
    def __init__(self):
        self.dispositivos: Dict[str, DispositivoInteligente] = {}
        self._registro_eventos: List[Evento] = []
    
    def agregar_dispositivo(self, dispositivo: DispositivoInteligente) -> None:
        """Agregar un dispositivo a la centralita"""
        self.dispositivos[dispositivo.id] = dispositivo
        # Suscribir a los eventos del dispositivo
        dispositivo.suscribir(TipoEvento.DISPOSITIVO_ENCENDIDO, self._manejar_evento)
        dispositivo.suscribir(TipoEvento.DISPOSITIVO_APAGADO, self._manejar_evento)
        dispositivo.suscribir(TipoEvento.MENSAJE_RECIBIDO, self._manejar_evento)
        dispositivo.suscribir(TipoEvento.ERROR, self._manejar_evento)
    
    def enviar_mensaje(self, destino_id: str, mensaje: str) -> bool:
        """Enviar un mensaje a un dispositivo específico"""
        if destino_id in self.dispositivos:
            self.dispositivos[destino_id].recibir_mensaje(mensaje)
            return True
        return False
    
    def broadcast(self, mensaje: str) -> None:
        """Enviar un mensaje a todos los dispositivos"""
        for dispositivo in self.dispositivos.values():
            dispositivo.recibir_mensaje(mensaje)
    
    def _manejar_evento(self, evento: Evento) -> None:
        """Manejador de eventos registrados"""
        self._registro_eventos.append(evento)
        print(f"\n[Centralita] Evento registrado: "
              f"{evento.tipo.name} de {evento.origen}")
        
        # Ejemplo de reacción a eventos
        if evento.tipo == TipoEvento.DISPOSITIVO_ENCENDIDO:
            if "bombilla" in evento.origen:
                self.enviar_mensaje(evento.origen, "Bienvenida bombilla!")
    
    def mostrar_estados(self) -> None:
        """Mostrar estado de todos los dispositivos"""
        print("\n=== ESTADO DE DISPOSITIVOS ===")
        for dispositivo in self.dispositivos.values():
            print(dispositivo.estado())
    
    def mostrar_eventos(self) -> None:
        """Mostrar eventos registrados"""
        print("\n=== HISTORIAL DE EVENTOS ===")
        for evento in self._registro_eventos:
            print(f"[{evento.timestamp:.2f}] {evento.tipo.name} de {evento.origen}")

# ============ EJEMPLO DE USO ============
def demo_sistema_hogar_inteligente():
    """Demuestra el sistema completo de hogar inteligente"""
    print("\n=== SISTEMA DE HOGAR INTELIGENTE ===")
    
    # 1. Crear centralita
    centralita = CentralitaInteligente()
    
    # 2. Crear y agregar dispositivos
    bombilla = BombillaInteligente("bombilla_sala")
    termostato = TermostatoInteligente("termostato_principal")
    
    centralita.agregar_dispositivo(bombilla)
    centralita.agregar_dispositivo(termostato)
    
    # 3. Conectar dispositivos
    bombilla.conectar("WifiHogar")
    termostato.conectar("WifiHogar")
    
    # 4. Operar dispositivos
    bombilla.encender()
    termostato.encender()
    
    # 5. Enviar mensajes
    centralita.enviar_mensaje("termostato_principal", "set_temp:22.5")
    centralita.broadcast("Buenos días!")
    
    # 6. Mostrar estados y eventos
    centralita.mostrar_estados()
    centralita.mostrar_eventos()

if __name__ == "__main__":
    demo_sistema_hogar_inteligente()