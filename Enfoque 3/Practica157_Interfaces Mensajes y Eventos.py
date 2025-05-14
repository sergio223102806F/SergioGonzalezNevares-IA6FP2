"""
INTERFACES, MENSAJES Y EVENTOS -
---------------------------------------------------------
Este código demuestra los conceptos de:
1. Interfaces (clases abstractas)
2. Paso de mensajes entre objetos
3. Sistema de eventos (publicación/suscripción)
"""

# ============ IMPORTACIONES ============
from abc import ABC, abstractmethod # Importa ABC (Clase Base Abstracta) y abstractmethod para definir interfaces
from typing import List, Dict, Callable, Any # Importa tipos para anotaciones de tipo
from dataclasses import dataclass # Importa el decorador dataclass para crear clases de datos
from enum import Enum, auto # Importa Enum y auto para crear enumeraciones

import time # Importa el módulo time para manejar marcas de tiempo

# ============ INTERFACES (CLASES ABSTRACTAS) ============
class DispositivoElectronico(ABC):
    """Interfaz abstracta para dispositivos electrónicos"""
    
    @abstractmethod
    def encender(self) -> None:
        """Encender el dispositivo"""
        pass # Método abstracto: debe ser implementado por las subclases

    @abstractmethod
    def apagar(self) -> None:
        """Apagar el dispositivo"""
        pass # Método abstracto: debe ser implementado por las subclases
    
    @abstractmethod
    def estado(self) -> str:
        """Obtener estado actual"""
        pass # Método abstracto: debe ser implementado por las subclases

class DispositivoInteligente(DispositivoElectronico):
    """Interfaz extendida para dispositivos inteligentes"""
    
    @abstractmethod
    def conectar(self, red: str) -> bool:
        """Conectar a una red WiFi"""
        pass # Método abstracto: debe ser implementado por las subclases
    
    @abstractmethod
    def recibir_mensaje(self, mensaje: str) -> None:
        """Recibir un mensaje del sistema"""
        pass # Método abstracto: debe ser implementado por las subclases

# ============ MENSAJES ============
@dataclass
class Mensaje:
    """Estructura para mensajes entre objetos"""
    remitente: str # Atributo: nombre del remitente del mensaje
    destinatario: str # Atributo: nombre del destinatario del mensaje
    contenido: Any # Atributo: contenido del mensaje (puede ser de cualquier tipo)
    timestamp: float = time.time() # Atributo: marca de tiempo del mensaje, con valor por defecto la hora actual

# ============ SISTEMA DE EVENTOS ============
class TipoEvento(Enum):
    """Tipos de eventos en el sistema"""
    DISPOSITIVO_ENCENDIDO = auto() # Evento: dispositivo encendido
    DISPOSITIVO_APAGADO = auto() # Evento: dispositivo apagado
    MENSAJE_RECIBIDO = auto() # Evento: mensaje recibido
    ERROR = auto() # Evento: error

@dataclass
class Evento:
    """Estructura para eventos del sistema"""
    tipo: TipoEvento # Atributo: tipo del evento (de la enumeración TipoEvento)
    origen: str # Atributo: nombre del objeto que originó el evento
    datos: Dict[str, Any] = None # Atributo: datos adicionales del evento (diccionario), opcional
    timestamp: float = time.time() # Atributo: marca de tiempo del evento, con valor por defecto la hora actual

class PublicadorEventos:
    """Clase base para objetos que publican eventos"""
    
    def __init__(self):
        self._suscriptores: Dict[TipoEvento, List[Callable]] = {} # Diccionario: mapea tipos de evento a listas de funciones callback
    
    def suscribir(self, evento: TipoEvento, callback: Callable) -> None:
        """Suscribir una función a un tipo de evento"""
        if evento not in self._suscriptores: # Si el tipo de evento no está en el diccionario de suscriptores
            self._suscriptores[evento] = [] # Crea una lista vacía para ese tipo de evento
        self._suscriptores[evento].append(callback) # Agrega la función callback a la lista de suscriptores para ese evento
    
    def _notificar(self, evento: Evento) -> None:
        """Notificar a los suscriptores sobre un evento"""
        if evento.tipo in self._suscriptores: # Si hay suscriptores para el tipo de evento
            for callback in self._suscriptores[evento.tipo]: # Itera sobre las funciones callback suscritas a ese evento
                callback(evento) # Llama a cada función callback, pasándole el objeto Evento

# ============ IMPLEMENTACIONES CONCRETAS ============
class BombillaInteligente(DispositivoInteligente, PublicadorEventos):
    """Implementación concreta de una bombilla inteligente"""
    
    def __init__(self, id: str):
        super().__init__() # Llama al constructor de la clase base (PublicadorEventos)
        self.id = id # Atributo: identificador único de la bombilla
        self._encendida = False # Atributo: estado de la bombilla (encendida o apagada)
        self._conectada = False # Atributo: estado de conexión de la bombilla
        self._red_wifi = "" # Atributo: nombre de la red WiFi a la que está conectada
    
    def encender(self) -> None:
        if not self._encendida: # Si la bombilla no está encendida
            self._encendida = True # Cambia el estado a encendida
            print(f"{self.id}: Bombilla encendida") # Imprime un mensaje
            self._notificar(Evento( # Notifica a los suscriptores que la bombilla se ha encendido
                TipoEvento.DISPOSITIVO_ENCENDIDO, # Tipo de evento: dispositivo encendido
                self.id, # Origen del evento: el ID de la bombilla
                {"nivel_luz": 100} # Datos adicionales: nivel de luz (100%)
            ))
    
    def apagar(self) -> None:
        if self._encendida: # Si la bombilla está encendida
            self._encendida = False # Cambia el estado a apagada
            print(f"{self.id}: Bombilla apagada") # Imprime un mensaje
            self._notificar(Evento( # Notifica a los suscriptores que la bombilla se ha apagado
                TipoEvento.DISPOSITIVO_APAGADO, # Tipo de evento: dispositivo apagado
                self.id # Origen del evento: el ID de la bombilla
            ))
    
    def estado(self) -> str:
        return (f"Bombilla {self.id}: " # Devuelve una cadena con el estado de la bombilla
                f"{'Encendida' if self._encendida else 'Apagada'}, " # Indica si está encendida o apagada
                f"{'Conectada' if self._conectada else 'Desconectada'}") # Indica si está conectada o desconectada
    
    def conectar(self, red: str) -> bool:
        self._conectada = True # Cambia el estado de conexión a conectada
        self._red_wifi = red # Guarda el nombre de la red WiFi
        print(f"{self.id}: Conectada a {red}") # Imprime un mensaje
        return True # Devuelve True para indicar éxito
    
    def recibir_mensaje(self, mensaje: str) -> None:
        print(f"{self.id}: Mensaje recibido - {mensaje}") # Imprime el mensaje recibido
        self._notificar(Evento( # Notifica a los suscriptores que se ha recibido un mensaje
            TipoEvento.MENSAJE_RECIBIDO, # Tipo de evento: mensaje recibido
            self.id, # Origen del evento: el ID de la bombilla
            {"mensaje": mensaje} # Datos adicionales: el mensaje recibido
        ))

class TermostatoInteligente(DispositivoInteligente, PublicadorEventos):
    """Implementación concreta de un termostato inteligente"""
    
    def __init__(self, id: str):
        super().__init__() # Llama al constructor de la clase base (PublicadorEventos)
        self.id = id # Atributo: identificador único del termostato
        self._encendido = False # Atributo: estado del termostato (encendido o apagado)
        self._temperatura = 20.0 # Atributo: temperatura actual del termostato
        self._conectado = False # Atributo: estado de conexión del termostato
    
    def encender(self) -> None:
        if not self._encendido: # Si el termostato no está encendido
            self._encendido = True # Cambia el estado a encendido
            print(f"{self.id}: Termostato encendido") # Imprime un mensaje
            self._notificar(Evento( # Notifica a los suscriptores que el termostato se ha encendido
                TipoEvento.DISPOSITIVO_ENCENDIDO, # Tipo de evento: dispositivo encendido
                self.id, # Origen del evento: el ID del termostato
                {"temperatura": self._temperatura} # Datos adicionales: la temperatura actual
            ))
    
    def apagar(self) -> None:
        if self._encendido: # Si el termostato está encendido
            self._encendido = False # Cambia el estado a apagado
            print(f"{self.id}: Termostato apagado") # Imprime un mensaje
            self._notificar(Evento( # Notifica a los suscriptores que el termostato se ha apagado
                TipoEvento.DISPOSITIVO_APAGADO, # Tipo de evento: dispositivo apagado
                self.id # Origen del evento: el ID del termostato
            ))
    
    def estado(self) -> str:
        return (f"Termostato {self.id}: " # Devuelve una cadena con el estado del termostato
                f"{'Encendido' if self._encendido else 'Apagado'}, " # Indica si está encendido o apagado
                f"Temp: {self._temperatura}°C") # Indica la temperatura actual
    
    def conectar(self, red: str) -> bool:
        self._conectado = True # Cambia el estado de conexión a conectado
        print(f"{self.id}: Conectado a {red}") # Imprime un mensaje
        return True
    
    def recibir_mensaje(self, mensaje: str) -> None:
        print(f"{self.id}: Mensaje recibido - {mensaje}") # Imprime el mensaje recibido
        if "set_temp:" in mensaje: # Si el mensaje es para cambiar la temperatura
            nueva_temp = float(mensaje.split(":")[1]) # Extrae la nueva temperatura del mensaje
            self._temperatura = nueva_temp # Actualiza la temperatura
            print(f"{self.id}: Temperatura cambiada a {nueva_temp}°C") # Imprime un mensaje
        
        self._notificar(Evento( # Notifica a los suscriptores que se ha recibido un mensaje
            TipoEvento.MENSAJE_RECIBIDO, # Tipo de evento: mensaje recibido
            self.id, # Origen del evento: el ID del termostato
            {"mensaje": mensaje, "temperatura": self._temperatura} # Datos del mensaje y la temperatura
        ))

# ============ CENTRALITA INTELIGENTE ============
class CentralitaInteligente:
    """Sistema central que gestiona dispositivos y mensajes"""
    
    def __init__(self):
        self.dispositivos: Dict[str, DispositivoInteligente] = {} # Diccionario: mapea IDs de dispositivo a objetos DispositivoInteligente
        self._registro_eventos: List[Evento] = [] # Lista: almacena todos los eventos que han ocurrido en el sistema
    
    def agregar_dispositivo(self, dispositivo: DispositivoInteligente) -> None:
        """Agregar un dispositivo a la centralita"""
        self.dispositivos[dispositivo.id] = dispositivo # Agrega el dispositivo al diccionario, usando su ID como clave
        # Suscribir a los eventos del dispositivo
        dispositivo.suscribir(TipoEvento.DISPOSITIVO_ENCENDIDO, self._manejar_evento) # Suscribe al método _manejar_evento a los eventos de encendido del dispositivo
        dispositivo.suscribir(TipoEvento.DISPOSITIVO_APAGADO, self._manejar_evento) # Suscribe al método _manejar_evento a los eventos de apagado del dispositivo
        dispositivo.suscribir(TipoEvento.MENSAJE_RECIBIDO, self._manejar_evento) # Suscribe al método _manejar_evento a los eventos de recepción de mensajes del dispositivo
        dispositivo.suscribir(TipoEvento.ERROR, self._manejar_evento) # Suscribe al método _manejar_evento a los eventos de error del dispositivo
    
    def enviar_mensaje(self, destino_id: str, mensaje: str) -> bool:
        """Enviar un mensaje a un dispositivo específico"""
        if destino_id in self.dispositivos: # Si el ID de destino existe en el diccionario de dispositivos
            self.dispositivos[destino_id].recibir_mensaje(mensaje) # Llama al método recibir_mensaje del dispositivo destinatario
            return True # Devuelve True para indicar éxito
        return False # Devuelve False si el dispositivo de destino no existe
    
    def broadcast(self, mensaje: str) -> None:
        """Enviar un mensaje a todos los dispositivos"""
        for dispositivo in self.dispositivos.values(): # Itera sobre todos los dispositivos en el diccionario
            dispositivo.recibir_mensaje(mensaje) # Llama al método recibir_mensaje de cada dispositivo
    
    def _manejar_evento(self, evento: Evento) -> None:
        """Manejador de eventos registrados"""
        self._registro_eventos.append(evento) # Agrega el evento a la lista de eventos registrados
        print(f"\n[Centralita] Evento registrado: " # Imprime un mensaje indicando que el evento ha sido registrado
              f"{evento.tipo.name} de {evento.origen}") # Imprime el tipo de evento y el origen
        
        # Ejemplo de reacción a eventos
        if evento.tipo == TipoEvento.DISPOSITIVO_ENCENDIDO: # Si el evento es de tipo DISPOSITIVO_ENCENDIDO
            if "bombilla" in evento.origen: # Y el origen del evento contiene "bombilla"
                self.enviar_mensaje(evento.origen, "Bienvenida bombilla!") # Envía un mensaje de bienvenida a la bombilla
    
    def mostrar_estados(self) -> None:
        """Mostrar estado de todos los dispositivos"""
        print("\n=== ESTADO DE DISPOSITIVOS ===") # Imprime un encabezado
        for dispositivo in self.dispositivos.values(): # Itera sobre todos los dispositivos
            print(dispositivo.estado()) # Imprime el estado de cada dispositivo
    
    def mostrar_eventos(self) -> None:
        """Mostrar eventos registrados"""
        print("\n=== HISTORIAL DE EVENTOS ===") # Imprime un encabezado
        for evento in self._registro_eventos: # Itera sobre la lista de eventos registrados
            print(f"[{evento.timestamp:.2f}] {evento.tipo.name} de {evento.origen}") # Imprime la marca de tiempo, el tipo y el origen de cada evento

# ============ EJEMPLO DE USO ============
def demo_sistema_hogar_inteligente():
    """Demuestra el sistema completo de hogar inteligente"""
    print("\n=== SISTEMA DE HOGAR INTELIGENTE ===")
    
    # 1. Crear centralita
    centralita = CentralitaInteligente() # Crea una instancia de la clase CentralitaInteligente
    
    # 2. Crear y agregar dispositivos
    bombilla = BombillaInteligente("bombilla_sala") # Crea una bombilla inteligente
    termostato = TermostatoInteligente("termostato_principal") # Crea un termostato inteligente
    
    centralita.agregar_dispositivo(bombilla) # Agrega la bombilla a la centralita
    centralita.agregar_dispositivo(termostato) # Agrega el termostato a la centralita
    
    # 3. Conectar dispositivos
    bombilla.conectar("WifiHogar") # Conecta la bombilla a la red WiFi
    termostato.conectar("WifiHogar") # Conecta el termostato a la red WiFi
    
    # 4. Operar dispositivos
    bombilla.encender() # Enciende la bombilla
    termostato.encender() # Enciende el termostato
    
    # 5. Enviar mensajes
    centralita.enviar_mensaje("termostato_principal", "set_temp:22.5") # Envía un mensaje al termostato para cambiar la temperatura
    centralita.broadcast("Buenos días!") # Envía un mensaje a todos los dispositivos
    
    # 6. Mostrar estados y eventos
    centralita.mostrar_estados() # Muestra el estado de todos los dispositivos
    centralita.mostrar_eventos() # Muestra el historial de eventos

if __name__ == "__main__":
    demo_sistema_hogar_inteligente() # Llama a la función principal para ejecutar la demostración
