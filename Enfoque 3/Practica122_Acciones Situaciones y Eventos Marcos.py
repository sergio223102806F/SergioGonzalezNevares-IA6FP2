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
        if accion.nombre in self.acciones:  # Verifica si la acción ya existe en el diccionario de acciones
            return False  # Retorna False si la acción ya existe
        self.acciones[accion.nombre] = accion  # Agrega la acción al diccionario de acciones usando su nombre como clave
        return True  # Retorna True si la acción se agregó correctamente

    def agregar_situacion(self, situacion: Situacion) -> bool:
        """
        Registra una nueva situación en el marco.

        Args:
            situacion (Situacion): Objeto Situacion a agregar

        Returns:
            bool: True si se agregó correctamente, False si ya existía
        """
        if situacion.nombre in self.situaciones:  # Verifica si la situación ya existe en el diccionario de situaciones
            return False  # Retorna False si la situación ya existe
        self.situaciones[situacion.nombre] = situacion  # Agrega la situación al diccionario de situaciones usando su nombre como clave
        return True  # Retorna True si la situación se agregó correctamente

    def agregar_evento(self, evento: Evento) -> bool:
        """
        Registra un nuevo evento en el marco y lo añade al historial.

        Args:
            evento (Evento): Objeto Evento a agregar

        Returns:
            bool: True si se agregó correctamente, False si ya existía
        """
        if evento.nombre in self.eventos:  # Verifica si el evento ya existe en el diccionario de eventos
            return False  # Retorna False si el evento ya existe
        self.eventos[evento.nombre] = evento  # Agrega el evento al diccionario de eventos usando su nombre como clave
        self.historial_eventos.append(evento)  # Añade el evento a la lista del historial de eventos
        return True  # Retorna True si el evento se agregó correctamente

    def ejecutar_accion(self, nombre_accion: str) -> Optional[List[str]]:
        """
        Intenta ejecutar una acción verificando sus precondiciones.

        Args:
            nombre_accion (str): Nombre de la acción a ejecutar

        Returns:
            Optional[List[str]]: Lista de efectos si se ejecutó, None si falló
        """
        if nombre_accion not in self.acciones:  # Verifica si la acción existe en el diccionario de acciones
            return None  # Retorna None si la acción no se encuentra

        accion = self.acciones[nombre_accion]  # Obtiene el objeto Accion correspondiente al nombre

        # Verificar precondiciones
        for precond in accion.precondiciones:  # Itera sobre las precondiciones de la acción
            if precond not in self.situaciones:  # Verifica si cada precondición existe como una situación en el marco
                return None  # Retorna None si alguna precondición no se cumple

        # Aplicar efectos
        nuevos_efectos = []  # Inicializa una lista para almacenar los nuevos efectos
        for efecto in accion.efectos:  # Itera sobre los efectos de la acción
            if efecto not in self.situaciones:  # Verifica si el efecto ya existe como una situación
                nueva_situacion = Situacion(efecto, {}, False)  # Crea una nueva situación para el efecto
                self.agregar_situacion(nueva_situacion)  # Agrega la nueva situación al marco
                nuevos_efectos.append(efecto)  # Añade el nombre del efecto a la lista de nuevos efectos

        return nuevos_efectos  # Retorna la lista de los nuevos efectos resultantes de la acción

    def obtener_estado_actual(self) -> Dict[str, bool]:
        """
        Devuelve un diccionario con el estado actual de todas las situaciones.

        Returns:
            Dict[str, bool]: Claves son nombres de situación, valores si están activas
        """
        return {nombre: True for nombre in self.situaciones}  # Retorna un diccionario donde las claves son los nombres de las situaciones y los valores son True (indicando que existen)

    def simular_evento(self, nombre_evento: str) -> bool:
        """
        Simula la ocurrencia de un evento y actualiza el marco.

        Args:
            nombre_evento (str): Nombre del evento a simular

        Returns:
            bool: True si el evento se simuló correctamente
        """
        if nombre_evento not in self.eventos:  # Verifica si el evento existe en el diccionario de eventos
            return False  # Retorna False si el evento no se encuentra

        evento = self.eventos[nombre_evento]  # Obtiene el objeto Evento correspondiente al nombre

        # Actualizar situaciones basadas en el evento
        for participante in evento.participantes:  # Itera sobre los participantes del evento
            if participante in self.situaciones:  # Verifica si el participante es también una situación en el marco
                self.situaciones[participante].atributos["ultimo_evento"] = evento.nombre  # Actualiza un atributo de la situación con el nombre del último evento

        return True  # Retorna True si el evento se simuló correctamente

    def visualizar_marco(self):
        """
        Muestra una representación gráfica del estado actual del marco.
        """
        print("\n=== ESTADO DEL MARCO ===")  # Imprime un encabezado para el estado del marco

        print("\nAcciones disponibles:")  # Imprime un encabezado para las acciones disponibles
        for accion in self.acciones.values():  # Itera sobre los valores (objetos Accion) en el diccionario de acciones
            print(f"- {accion.nombre} (Pre: {accion.precondiciones}, Efectos: {accion.efectos})")  # Imprime el nombre, precondiciones y efectos de cada acción

        print("\nSituaciones actuales:")  # Imprime un encabezado para las situaciones actuales
        for situacion in self.situaciones.values():  # Itera sobre los valores (objetos Situacion) en el diccionario de situaciones
            print(f"- {situacion.nombre} {'(Persistente)' if situacion.persistente else ''}")  # Imprime el nombre de cada situación y si es persistente

        print("\nÚltimos eventos:")  # Imprime un encabezado para los últimos eventos
        for evento in self.historial_eventos[-3:]:  # Itera sobre los últimos 3 eventos en la lista del historial de eventos
            print(f"- {evento.nombre} (T: {evento.momento})")  # Imprime el nombre y el momento temporal de cada evento

def ejemplo_uso():
    """
    Función de ejemplo que demuestra el uso del sistema de marcos.
    """
    # 1. Crear instancia del marco
    marco = Marco()  # Crea una instancia de la clase Marco

    # 2. Definir situaciones iniciales
    marco.agregar_situacion(Situacion("Dia_soleado", {"clima": "soleado"}, True))  # Agrega una situación inicial "Dia_soleado" con un atributo y marcada como persistente
    marco.agregar_situacion(Situacion("En_casa", {"ubicacion": "casa"}, False))  # Agrega una situación inicial "En_casa" con un atributo y no persistente

    # 3. Definir acciones posibles
    marco.agregar_accion(Accion(  # Agrega una acción "Salir_a_pasear"
        "Salir_a_pasear",
        ["Dia_soleado", "En_casa"],  # Precondiciones para la acción
        ["En_exterior", "Paseando"],  # Efectos de la acción
        {"intensidad": "moderada"}  # Atributos de la acción
    ))

    marco.agregar_accion(Accion(  # Agrega una acción "Volver_a_casa"
        "Volver_a_casa",
        ["En_exterior"],  # Precondiciones para la acción
        ["En_casa"],  # Efectos de la acción
        {"duracion": "corta"}  # Atributos de la acción
    ))

    # 4. Definir eventos posibles
    marco.agregar_evento(Evento(  # Agrega un evento "Llega_visita"
        "Llega_visita",
        10,  # Momento temporal del evento
        ["En_casa"],  # Participantes del evento
        {"tipo": "social"}  # Atributos del evento
    ))

    # 5. Ejecutar algunas acciones
    print("Intentando salir a pasear...")  # Imprime un mensaje indicando la intención de ejecutar una acción
    efectos = marco.ejecutar_accion("Salir_a_pasear")  # Intenta ejecutar la acción "Salir_a_pasear"
    if efectos:  # Verifica si la acción se ejecutó con éxito (retornó una lista de efectos)
        print(f"Acción ejecutada. Nuevas situaciones: {efectos}")  # Imprime un mensaje indicando que la acción se ejecutó y los nuevos efectos
    else:  # Si la acción no se pudo ejecutar (retornó None)
        print("No se pudo ejecutar la acción")  # Imprime un mensaje indicando que la acción falló

    # 6. Simular un evento
    print("\nSimulando llegada de visita...")  # Imprime un mensaje indicando la simulación de un evento
    if marco.simular_evento("Llega_visita"):  # Simula el evento "Llega_visita"
        print("Evento simulado correctamente")  # Imprime un mensaje si el evento se simuló correctamente

    # 7. Mostrar estado final
    marco.visualizar_marco()  # Llama a la función para mostrar el estado actual del marco

if __name__ == "__main__":
    ejemplo_uso()  # Llama a la función de ejemplo cuando el script se ejecuta directamente