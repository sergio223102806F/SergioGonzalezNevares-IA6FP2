# -*- coding: utf-8 -*-


# Importación de módulos necesarios
from typing import Dict, List, Optional  # Para anotaciones de tipo
from dataclasses import dataclass  # Para crear clases de datos

@dataclass
class Entidad:
    """
    Clase base para cualquier entidad en el marco (frame).
    Representa los elementos fundamentales con nombre y atributos.
    """
    nombre: str  # Identificador único de la entidad
    atributos: Dict[str, str]  # Diccionario de propiedades clave-valor

@dataclass
class Accion(Entidad):
    """
    Representa una acción que puede ser realizada por un agente.
    Hereda de Entidad y añade propiedades específicas de acciones.
    """
    precondiciones: List[str]  # Situaciones requeridas antes de ejecutar
    efectos: List[str]  # Situaciones resultantes después de ejecutar

@dataclass
class Situacion(Entidad):
    """
    Representa un estado o condición en el marco.
    Hereda de Entidad con características específicas de situaciones.
    """
    persistente: bool = False  # Indica si la situación persiste en el tiempo

@dataclass
class Evento(Entidad):
    """
    Representa un acontecimiento que ocurre en un momento específico.
    Hereda de Entidad con propiedades temporales.
    """
    momento: int  # Marca temporal del evento
    participantes: List[str]  # Entidades involucradas en el evento

class Marco:
    """
    Clase principal que contiene y gestiona el sistema completo de marcos.
    Agrupa acciones, situaciones y eventos con métodos para manipularlos.
    """
    def __init__(self):
        """
        Inicializa el marco con estructuras vacías para cada tipo de entidad.
        """
        self.acciones: Dict[str, Accion] = {}  # Diccionario de acciones por nombre
        self.situaciones: Dict[str, Situacion] = {}  # Diccionario de situaciones
        self.eventos: Dict[str, Evento] = {}  # Diccionario de eventos
        self.historial_eventos: List[Evento] = []  # Lista temporal de eventos

    def agregar_accion(self, accion: Accion) -> bool:
        """
        Registra una nueva acción en el marco.
        
        Args:
            accion (Accion): Objeto Accion a agregar
            
        Returns:
            bool: True si se agregó correctamente, False si ya existía
        """
        if accion.nombre in self.acciones:
            return False
        self.acciones[accion.nombre] = accion
        return True

    def agregar_situacion(self, situacion: Situacion) -> bool:
        """
        Registra una nueva situación en el marco.
        
        Args:
            situacion (Situacion): Objeto Situacion a agregar
            
        Returns:
            bool: True si se agregó correctamente, False si ya existía
        """
        if situacion.nombre in self.situaciones:
            return False
        self.situaciones[situacion.nombre] = situacion
        return True

    def agregar_evento(self, evento: Evento) -> bool:
        """
        Registra un nuevo evento en el marco y lo añade al historial.
        
        Args:
            evento (Evento): Objeto Evento a agregar
            
        Returns:
            bool: True si se agregó correctamente, False si ya existía
        """
        if evento.nombre in self.eventos:
            return False
        self.eventos[evento.nombre] = evento
        self.historial_eventos.append(evento)
        return True

    def ejecutar_accion(self, nombre_accion: str) -> Optional[List[str]]:
        """
        Intenta ejecutar una acción verificando sus precondiciones.
        
        Args:
            nombre_accion (str): Nombre de la acción a ejecutar
            
        Returns:
            Optional[List[str]]: Lista de efectos si se ejecutó, None si falló
        """
        if nombre_accion not in self.acciones:
            return None
            
        accion = self.acciones[nombre_accion]
        
        # Verificar precondiciones
        for precond in accion.precondiciones:
            if precond not in self.situaciones:
                return None
                
        # Aplicar efectos
        nuevos_efectos = []
        for efecto in accion.efectos:
            if efecto not in self.situaciones:
                nueva_situacion = Situacion(efecto, {}, False)
                self.agregar_situacion(nueva_situacion)
                nuevos_efectos.append(efecto)
                
        return nuevos_efectos

    def obtener_estado_actual(self) -> Dict[str, bool]:
        """
        Devuelve un diccionario con el estado actual de todas las situaciones.
        
        Returns:
            Dict[str, bool]: Claves son nombres de situación, valores si están activas
        """
        return {nombre: True for nombre in self.situaciones}

    def simular_evento(self, nombre_evento: str) -> bool:
        """
        Simula la ocurrencia de un evento y actualiza el marco.
        
        Args:
            nombre_evento (str): Nombre del evento a simular
            
        Returns:
            bool: True si el evento se simuló correctamente
        """
        if nombre_evento not in self.eventos:
            return False
            
        evento = self.eventos[nombre_evento]
        
        # Actualizar situaciones basadas en el evento
        for participante in evento.participantes:
            if participante in self.situaciones:
                self.situaciones[participante].atributos["ultimo_evento"] = evento.nombre
                
        return True

    def visualizar_marco(self):
        """
        Muestra una representación gráfica del estado actual del marco.
        """
        print("\n=== ESTADO DEL MARCO ===")
        
        print("\nAcciones disponibles:")
        for accion in self.acciones.values():
            print(f"- {accion.nombre} (Pre: {accion.precondiciones}, Efectos: {accion.efectos})")
            
        print("\nSituaciones actuales:")
        for situacion in self.situaciones.values():
            print(f"- {situacion.nombre} {'(Persistente)' if situacion.persistente else ''}")
            
        print("\nÚltimos eventos:")
        for evento in self.historial_eventos[-3:]:  # Mostrar solo los 3 últimos
            print(f"- {evento.nombre} (T: {evento.momento})")

def ejemplo_uso():
    """
    Función de ejemplo que demuestra el uso del sistema de marcos.
    """
    # 1. Crear instancia del marco
    marco = Marco()
    
    # 2. Definir situaciones iniciales
    marco.agregar_situacion(Situacion("Dia_soleado", {"clima": "soleado"}, True))
    marco.agregar_situacion(Situacion("En_casa", {"ubicacion": "casa"}, False))
    
    # 3. Definir acciones posibles
    marco.agregar_accion(Accion(
        "Salir_a_pasear",
        ["Dia_soleado", "En_casa"],  # Precondiciones
        ["En_exterior", "Paseando"],  # Efectos
        {"intensidad": "moderada"}
    ))
    
    marco.agregar_accion(Accion(
        "Volver_a_casa",
        ["En_exterior"],  # Precondiciones
        ["En_casa"],  # Efectos
        {"duracion": "corta"}
    ))
    
    # 4. Definir eventos posibles
    marco.agregar_evento(Evento(
        "Llega_visita",
        10,  # Momento temporal
        ["En_casa"],  # Participantes
        {"tipo": "social"}
    ))
    
    # 5. Ejecutar algunas acciones
    print("Intentando salir a pasear...")
    efectos = marco.ejecutar_accion("Salir_a_pasear")
    if efectos:
        print(f"Acción ejecutada. Nuevas situaciones: {efectos}")
    else:
        print("No se pudo ejecutar la acción")
    
    # 6. Simular un evento
    print("\nSimulando llegada de visita...")
    if marco.simular_evento("Llega_visita"):
        print("Evento simulado correctamente")
    
    # 7. Mostrar estado final
    marco.visualizar_marco()

if __name__ == "__main__":
    ejemplo_uso()