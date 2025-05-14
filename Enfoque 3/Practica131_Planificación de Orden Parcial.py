# -*- coding: utf-8 -*-
# Importaciones necesarias
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass
from enum import Enum, auto
from collections import defaultdict
import heapq

class TipoOrden(Enum):
    """Tipos de relaciones de orden entre acciones"""
    ANTES = auto()      # La acción A debe ocurrir antes que la B
    DESPUES = auto()    # La acción A debe ocurrir después que la B
    SIMULTANEA = auto() # Las acciones deben ocurrir al mismo tiempo

class EstadoAccion(Enum):
    """Estado de una acción en el plan parcial"""
    PENDIENTE = auto()  # Aún no programada
    PROGRAMADA = auto() # Programada pero no ejecutada
    EJECUTADA = auto()  # Completada

@dataclass
class AccionParcial:
    """Representa una acción en un plan de orden parcial"""
    nombre: str
    precondiciones: Set[str]    # Qué debe ser verdad antes de ejecutar
    efectos: Set[str]           # Qué cambia después de ejecutar
    duracion: int = 1           # Duración de la acción
    estado: EstadoAccion = EstadoAccion.PENDIENTE
    tiempo_inicio: Optional[int] = None  # Cuando se programa

@dataclass
class RestriccionOrden:
    """Restricción de orden entre dos acciones"""
    accion_a: str
    accion_b: str
    tipo: TipoOrden
    diferencia: int = 0  # Mínima diferencia temporal requerida

@dataclass
class PlanParcial:
    """
    Representa un plan de orden parcial con:
    - Acciones a realizar
    - Restricciones de orden
    - Estado actual del mundo
    """
    acciones: Dict[str, AccionParcial]  # Todas las acciones disponibles
    restricciones: List[RestriccionOrden]  # Relaciones entre acciones
    estado_actual: Set[str]  # Hechos verdaderos en el estado actual
    objetivos: Set[str]      # Hechos que deben ser verdaderos al final
    tiempo_actual: int = 0   # Tiempo actual de ejecución

class PlanificadorParcial:
    """
    Implementa algoritmos de planificación de orden parcial:
    - Planificación como satisfacción de restricciones (CSP)
    - Algoritmo de planificación parcialmente ordenada
    """
    
    def __init__(self, problema: PlanParcial):
        """
        Inicializa el planificador con un problema concreto
        
        Args:
            problema (PlanParcial): Problema de planificación a resolver
        """
        self.problema = problema
        self.plan: List[Tuple[int, str]] = []  # (tiempo, acción)
        self.causal_links: List[Tuple[str, str, str]] = []  # (A, B, p) donde A establece p para B
    
    def planificar(self) -> Optional[List[Tuple[int, str]]]:
        """
        Encuentra un plan parcialmente ordenado que resuelva el problema
        
        Returns:
            Optional[List[Tuple[int, str]]]: Plan con (tiempo, acción) o None
        """
        # Inicialización
        acciones_relevantes = self._identificar_acciones_relevantes()
        if not acciones_relevantes:
            return None  # No hay acciones que satisfagan los objetivos
        
        # Paso 1: Establecer orden parcial inicial
        self._establecer_orden_inicial(acciones_relevantes)
        
        # Paso 2: Resolver conflictos y amenazas
        while not self._es_plan_valido():
            resolvio = self._resolver_conflictos()
            if not resolvio:
                return None  # No se pudo resolver conflictos
            
        # Paso 3: Ordenar temporalmente (opcional)
        self._ordenar_temporalmente()
        
        return self.plan
    
    def _identificar_acciones_relevantes(self) -> List[AccionParcial]:
        """
        Identifica acciones cuyos efectos pueden satisfacer los objetivos
        
        Returns:
            List[AccionParcial]: Acciones relevantes para los objetivos
        """
        relevantes = []
        for objetivo in self.problema.objetivos:
            for accion in self.problema.acciones.values():
                if objetivo in accion.efectos:
                    relevantes.append(accion)
        return relevantes
    
    def _establecer_orden_inicial(self, acciones_relevantes: List[AccionParcial]):
        """
        Establece un orden parcial inicial entre acciones
        
        Args:
            acciones_relevantes (List[AccionParcial]): Acciones a ordenar
        """
        # Acción inicial implícita (estado inicial)
        accion_inicial = AccionParcial(
            nombre="INICIO",
            precondiciones=set(),
            efectos=self.problema.estado_actual,
            duracion=0,
            estado=EstadoAccion.EJECUTADA,
            tiempo_inicio=0
        )
        
        # Acción final implícita (objetivos)
        accion_final = AccionParcial(
            nombre="FIN",
            precondiciones=self.problema.objetivos,
            efectos=set(),
            duracion=0,
            estado=EstadoAccion.PENDIENTE
        )
        
        # Agregar al problema
        self.problema.acciones["INICIO"] = accion_inicial
        self.problema.acciones["FIN"] = accion_final
        
        # Establecer orden: INICIO antes que todas las relevantes, que están antes que FIN
        for accion in acciones_relevantes:
            self.problema.restricciones.append(
                RestriccionOrden("INICIO", accion.nombre, TipoOrden.ANTES)
            )
            self.problema.restricciones.append(
                RestriccionOrden(accion.nombre, "FIN", TipoOrden.ANTES)
            )
            
            # Registrar enlaces causales
            for efecto in accion.efectos:
                if efecto in self.problema.objetivos:
                    self.causal_links.append((accion.nombre, "FIN", efecto))
    
    def _es_plan_valido(self) -> bool:
        """
        Verifica si el plan actual es válido (sin conflictos)
        
        Returns:
            bool: True si el plan es válido
        """
        # Verificar que todas las precondiciones estén satisfechas
        for accion in self.problema.acciones.values():
            if accion.estado == EstadoAccion.PENDIENTE:
                continue
                
            for precond in accion.precondiciones:
                if not self._esta_satisfecha(precond, accion.tiempo_inicio):
                    return False
        
        # Verificar que no haya amenazas a los enlaces causales
        for (a, b, p) in self.causal_links:
            for accion in self.problema.acciones.values():
                if accion.nombre == a or accion.nombre == b:
                    continue
                    
                if p in accion.efectos and self._puede_interferir(accion, a, b):
                    return False
        
        return True
    
    def _esta_satisfecha(self, hecho: str, tiempo: int) -> bool:
        """
        Verifica si un hecho está satisfecho en un momento dado
        
        Args:
            hecho (str): Hecho a verificar
            tiempo (int): Tiempo en el que se necesita
            
        Returns:
            bool: True si el hecho es verdad en ese momento
        """
        # Verificar en el estado inicial
        if hecho in self.problema.estado_actual:
            return True
            
        # Verificar en acciones ya ejecutadas
        for accion in self.problema.acciones.values():
            if accion.estado == EstadoAccion.EJECUTADA and \
               accion.tiempo_inicio is not None and \
               accion.tiempo_inicio + accion.duracion <= tiempo and \
               hecho in accion.efectos:
                return True
                
        return False
    
    def _puede_interferir(self, accion: AccionParcial, a: str, b: str) -> bool:
        """
        Determina si una acción puede interferir con un enlace causal
        
        Args:
            accion (AccionParcial): Acción potencialmente interferente
            a (str): Acción que establece el hecho
            b (str): Acción que necesita el hecho
            
        Returns:
            bool: True si hay interferencia potencial
        """
        # Obtener tiempos de las acciones
        t_a = self.problema.acciones[a].tiempo_inicio
        t_b = self.problema.acciones[b].tiempo_inicio
        t_c = accion.tiempo_inicio
        
        if t_a is None or t_b is None or t_c is None:
            return False
            
        # Verificar si la acción C puede ejecutarse entre A y B
        fin_a = t_a + self.problema.acciones[a].duracion
        inicio_b = t_b
        
        return fin_a <= t_c < inicio_b
    
    def _resolver_conflictos(self) -> bool:
        """
        Intenta resolver conflictos en el plan actual
        
        Returns:
            bool: True si se resolvió al menos un conflicto
        """
        # Identificar amenazas a enlaces causales
        for (a, b, p) in self.causal_links:
            for c in self.problema.acciones.values():
                if c.nombre == a or c.nombre == b:
                    continue
                    
                if p in c.efectos and self._puede_interferir(c, a, b):
                    # Intentar resolver la amenaza
                    if self._promocion_orden(c.nombre, a, b) or \
                       self._demora_orden(c.nombre, a, b):
                        return True
        
        # Identificar precondiciones no satisfechas
        for accion in self.problema.acciones.values():
            if accion.estado != EstadoAccion.PENDIENTE:
                continue
                
            for precond in accion.precondiciones:
                if not self._esta_satisfecha(precond, self.problema.tiempo_actual):
                    # Buscar acción que pueda establecer la precondición
                    for a in self.problema.acciones.values():
                        if precond in a.efectos and a.estado == EstadoAccion.EJECUTADA:
                            # Establecer enlace causal y orden
                            self.causal_links.append((a.nombre, accion.nombre, precond))
                            self.problema.restricciones.append(
                                RestriccionOrden(a.nombre, accion.nombre, TipoOrden.ANTES)
                            )
                            return True
        
        return False
    
    def _promocion_orden(self, c: str, a: str, b: str) -> bool:
        """
        Resuelve conflicto ordenando C antes de A (promoción)
        
        Args:
            c (str): Acción interferente
            a (str): Acción que establece el hecho
            b (str): Acción que necesita el hecho
            
        Returns:
            bool: True si se pudo establecer el orden
        """
        # Verificar si C puede ordenarse antes de A sin conflictos
        if not self._es_orden_posible(c, a, TipoOrden.ANTES):
            return False
            
        self.problema.restricciones.append(
            RestriccionOrden(c, a, TipoOrden.ANTES)
        )
        return True
    
    def _demora_orden(self, c: str, a: str, b: str) -> bool:
        """
        Resuelve conflicto ordenando C después de B (demora)
        
        Args:
            c (str): Acción interferente
            a (str): Acción que establece el hecho
            b (str): Acción que necesita el hecho
            
        Returns:
            bool: True si se pudo establecer el orden
        """
        # Verificar si C puede ordenarse después de B sin conflictos
        if not self._es_orden_posible(b, c, TipoOrden.ANTES):
            return False
            
        self.problema.restricciones.append(
            RestriccionOrden(b, c, TipoOrden.ANTES)
        )
        return True
    
    def _es_orden_posible(self, x: str, y: str, tipo: TipoOrden) -> bool:
        """
        Verifica si es posible ordenar X e Y sin crear ciclos
        
        Args:
            x (str): Nombre de la primera acción
            y (str): Nombre de la segunda acción
            tipo (TipoOrden): Tipo de orden a establecer
            
        Returns:
            bool: True si el orden es posible
        """
 
# Importaciones necesarias
from typing import Dict, List, Set, Optional, Tuple  # Tipos para type hints
from dataclasses import dataclass                        # Para clases de datos
from enum import Enum, auto                            # Para enumeraciones
from collections import defaultdict                    # Diccionario con valores por defecto
import heapq                                         # Para colas de prioridad

class TipoOrden(Enum):
    """Tipos de relaciones de orden entre acciones"""
    ANTES = auto()      # La acción A debe ocurrir antes que la B
    DESPUES = auto()    # La acción A debe ocurrir después que la B
    SIMULTANEA = auto() # Las acciones deben ocurrir al mismo tiempo

class EstadoAccion(Enum):
    """Estado de una acción en el plan parcial"""
    PENDIENTE = auto()  # Aún no programada
    PROGRAMADA = auto() # Programada pero no ejecutada
    EJECUTADA = auto()  # Completada

@dataclass
class AccionParcial:
    """Representa una acción en un plan de orden parcial"""
    nombre: str                  # Identificador único de la acción
    precondiciones: Set[str]    # Qué debe ser verdad antes de ejecutar
    efectos: Set[str]            # Qué cambia después de ejecutar
    duracion: int = 1            # Duración de la acción (por defecto 1)
    estado: EstadoAccion = EstadoAccion.PENDIENTE  # Estado inicial
    tiempo_inicio: Optional[int] = None  # Cuándo se programa (inicialmente None)

@dataclass
class RestriccionOrden:
    """Restricción de orden entre dos acciones"""
    accion_a: str            # Nombre de la primera acción
    accion_b: str            # Nombre de la segunda acción
    tipo: TipoOrden          # Tipo de relación de orden
    diferencia: int = 0      # Mínima diferencia temporal requerida

@dataclass
class PlanParcial:
    """
    Representa un plan de orden parcial con:
    - Acciones a realizar
    - Restricciones de orden
    - Estado actual del mundo
    """
    acciones: Dict[str, AccionParcial]  # Diccionario de acciones disponibles
    restricciones: List[RestriccionOrden]  # Lista de relaciones de orden
    estado_actual: Set[str]            # Hechos verdaderos en el estado actual
    objetivos: Set[str]              # Hechos que deben ser verdaderos al final
    tiempo_actual: int = 0          # Tiempo actual de ejecución

class PlanificadorParcial:
    """
    Implementa algoritmos de planificación de orden parcial:
    - Planificación como satisfacción de restricciones (CSP)
    - Algoritmo de planificación parcialmente ordenada
    """

    def __init__(self, problema: PlanParcial):
        """
        Inicializa el planificador con un problema concreto

        Args:
            problema: Definición del problema de planificación
        """
        self.problema = problema            # Almacena el problema a resolver
        self.plan: List[Tuple[int, str]] = []    # Plan final (tiempo, acción)
        self.causal_links: List[Tuple[str, str, str]] = []  # Enlaces causales

    def planificar(self) -> Optional[List[Tuple[int, str]]]:
        """
        Encuentra un plan parcialmente ordenado que resuelva el problema

        Returns:
            Lista de tuplas (tiempo, acción) ordenadas, o None si no hay solución
        """
        # Paso 1: Identificar acciones relevantes para los objetivos
        acciones_relevantes = self._identificar_acciones_relevantes()
        if not acciones_relevantes:
            return None  # No hay solución posible

        # Paso 2: Establecer orden inicial entre acciones
        self._establecer_orden_inicial(acciones_relevantes)

        # Paso 3: Resolver conflictos iterativamente
        while not self._es_plan_valido():
            if not self._resolver_conflictos():
                return None  # No se pudieron resolver los conflictos

        # Paso 4: Ordenar temporalmente las acciones
        self._ordenar_temporalmente()

        return self.plan

    def _identificar_acciones_relevantes(self) -> List[AccionParcial]:
        """
        Identifica acciones cuyos efectos pueden satisfacer los objetivos

        Returns:
            Lista de acciones relevantes para alcanzar los objetivos
        """
        relevantes = []
        for objetivo in self.problema.objetivos:
            for accion in self.problema.acciones.values():
                if objetivo in accion.efectos:
                    relevantes.append(accion)
        return relevantes

    def _establecer_orden_inicial(self, acciones_relevantes: List[AccionParcial]):
        """
        Establece un orden parcial inicial entre acciones

        Args:
            acciones_relevantes: Lista de acciones que pueden contribuir a los objetivos
        """
        # Crear acción inicial implícita (estado inicial)
        accion_inicial = AccionParcial(
            nombre="INICIO",
            precondiciones=set(),
            efectos=self.problema.estado_actual,
            duracion=0,
            estado=EstadoAccion.EJECUTADA,
            tiempo_inicio=0
        )

        # Crear acción final implícita (objetivos)
        accion_final = AccionParcial(
            nombre="FIN",
            precondiciones=self.problema.objetivos,
            efectos=set(),
            duracion=0,
            estado=EstadoAccion.PENDIENTE
        )

        # Agregar acciones especiales al problema
        self.problema.acciones["INICIO"] = accion_inicial
        self.problema.acciones["FIN"] = accion_final

        # Establecer orden básico: INICIO < acciones_relevantes < FIN
        for accion in acciones_relevantes:
            self.problema.restricciones.append(
                RestriccionOrden("INICIO", accion.nombre, TipoOrden.ANTES)
            )
            self.problema.restricciones.append(
                RestriccionOrden(accion.nombre, "FIN", TipoOrden.ANTES)
            )

            # Registrar enlaces causales (qué acción provee cada objetivo)
            for efecto in accion.efectos:
                if efecto in self.problema.objetivos:
                    self.causal_links.append((accion.nombre, "FIN", efecto))

    def _es_plan_valido(self) -> bool:
        """
        Verifica si el plan actual es válido (sin conflictos)

        Returns:
            True si el plan es válido, False si hay conflictos
        """
        # Verificar precondiciones de todas las acciones
        for accion in self.problema.acciones.values():
            if accion.estado == EstadoAccion.PENDIENTE:
                continue

            for precond in accion.precondiciones:
                if not self._esta_satisfecha(precond, accion.tiempo_inicio):
                    return False

        # Verificar amenazas a enlaces causales
        for (a, b, p) in self.causal_links:
            for accion in self.problema.acciones.values():
                if accion.nombre == a or accion.nombre == b:
                    continue

                if p in accion.efectos and self._puede_interferir(accion, a, b):
                    return False

        return True

    def _esta_satisfecha(self, hecho: str, tiempo: int) -> bool:
        """
        Verifica si un hecho está satisfecho en un momento dado

        Args:
            hecho: El hecho a verificar
            tiempo: Momento temporal a comprobar

        Returns:
            True si el hecho es verdadero en ese momento
        """
        # Verificar en estado inicial
        if hecho in self.problema.estado_actual:
            return True

        # Verificar en acciones ejecutadas
        for accion in self.problema.acciones.values():
            if (accion.estado == EstadoAccion.EJECUTADA and
                    accion.tiempo_inicio is not None and
                    accion.tiempo_inicio + accion.duracion <= tiempo and
                    hecho in accion.efectos):
                return True

        return False

    def _puede_interferir(self, accion: AccionParcial, a: str, b: str) -> bool:
        """
        Determina si una acción puede interferir con un enlace causal

        Args:
            accion: Acción potencialmente interferente
            a: Acción que establece el hecho
            b: Acción que necesita el hecho

        Returns:
            True si hay posibilidad de interferencia
        """
        t_a = self.problema.acciones[a].tiempo_inicio
        t_b = self.problema.acciones[b].tiempo_inicio
        t_c = accion.tiempo_inicio

        if t_a is None or t_b is None or t_c is None:
            return False

        # La acción C interfiere si se ejecuta entre el fin de A y el inicio de B
        fin_a = t_a + self.problema.acciones[a].duracion
        inicio_b = t_b

        return fin_a <= t_c < inicio_b

    def _resolver_conflictos(self) -> bool:
        """
        Intenta resolver conflictos en el plan actual

        Returns:
            True si se resolvió al menos un conflicto
        """
        # Resolver amenazas a enlaces causales
        for (a, b, p) in self.causal_links:
            for c in self.problema.acciones.values():
                if c.nombre == a or c.nombre == b:
                    continue

                if p in c.efectos and self._puede_interferir(c, a, b):
                    # Intentar promoción (ordenar C antes de A)
                    if self._promocion_orden(c.nombre, a, b):
                        return True
                    # Intentar demora (ordenar C después de B)
                    if self._demora_orden(c.nombre, a, b):
                        return True

        # Resolver precondiciones no satisfechas
        for accion in self.problema.acciones.values():
            if accion.estado != EstadoAccion.PENDIENTE:
                continue

            for precond in accion.precondiciones:
                if not self._esta_satisfecha(precond, self.problema.tiempo_actual):
                    # Buscar acción que establezca la precondición
                    for a in self.problema.acciones.values():
                        if precond in a.efectos and a.estado == EstadoAccion.EJECUTADA:
                            # Establecer nuevo enlace causal y orden
                            self.causal_links.append((a.nombre, accion.nombre, precond))
                            self.problema.restricciones.append(
                                RestriccionOrden(a.nombre, accion.nombre, TipoOrden.ANTES)
                            )
                            return True

        return False

    def _promocion_orden(self, c: str, a: str, b: str) -> bool:
        """
        Resuelve conflicto ordenando C antes de A (promoción)

        Args:
            c: Acción interferente
            a: Acción que establece el hecho
            b: Acción que necesita el hecho

        Returns:
            True si se pudo establecer el orden
        """
        if not self._es_orden_posible(c, a, TipoOrden.ANTES):
            return False

        self.problema.restricciones.append(
            RestriccionOrden(c, a, TipoOrden.ANTES)
        )
        return True

    def _demora_orden(self, c: str, a: str, b: str) -> bool:
        """
        Resuelve conflicto ordenando C después de B (demora)

        Args:
            c: Acción interferente
            a: Acción que establece el hecho
            b: Acción que necesita el hecho

        Returns:
            True si se pudo establecer el orden
        """
        if not self._es_orden_posible(b, c, TipoOrden.ANTES):
            return False

        self.problema.restricciones.append(
            RestriccionOrden(b, c, TipoOrden.ANTES)
        )
        return True

    def _es_orden_posible(self, x: str, y: str, tipo: TipoOrden) -> bool:
        """
        Verifica si es posible ordenar X e Y sin crear ciclos

        Args:
            x: Primera acción
            y: Segunda acción
            tipo: Tipo de relación de orden

        Returns:
            True si el orden es posible sin ciclos
        """
        # Construir grafo de orden actual
        grafo = defaultdict(set)
        for restriccion in self.problema.restricciones:
            if restriccion.tipo == TipoOrden.ANTES:
                grafo[restriccion.accion_a].add(restriccion.accion_b)
            elif restriccion.tipo == TipoOrden.DESPUES:
                grafo[restriccion.accion_b].add(restriccion.accion_a)

        # Verificar si agregar X -> Y crearía un ciclo
        if tipo == TipoOrden.ANTES:
            # Verificar si Y puede llegar a X (crearía ciclo X->Y->...->X)
            if self._hay_camino(grafo, y, x):
                return False
        else:
            # Verificar si X puede llegar a Y (crearía ciclo Y->X->...->Y)
            if self._hay_camino(grafo, x, y):
                return False

        return True

    def _hay_camino(self, grafo: Dict[str, Set[str]], inicio: str, fin: str) -> bool:
        """
        Búsqueda en profundidad para detectar caminos en el grafo de orden

        Args:
            grafo (Dict[str, Set[str]]): Grafo de relaciones de orden
            inicio (str): Nodo inicial
            fin (str): Nodo objetivo

        Returns:
            bool: True si existe un camino de inicio a fin
        """
        visitados = set()
        pila = [inicio]

        while pila:
            nodo = pila.pop()
            if nodo == fin:
                return True

            if nodo not in visitados:
                visitados.add(nodo)
                for vecino in grafo.get(nodo, set()):
                    pila.append(vecino)

        return False

    def _ordenar_temporalmente(self):
        """
        Asigna tiempos de inicio a las acciones basado en el orden parcial
        """
        # Construir grafo de precedencia
        precedencia = defaultdict(set)
        for restriccion in self.problema.restricciones:
            if restriccion.tipo == TipoOrden.ANTES:
                precedencia[restriccion.accion_a].add(restriccion.accion_b)

        # Orden topológico
        orden_topologico = self._orden_topologico(precedencia)

        # Asignar tiempos de inicio más tempranos
        tiempos_inicio = {}
        for accion in orden_topologico:
            max_tiempo = 0
            for pred in precedencia:
                if accion in precedencia[pred]:
                    fin_pred = tiempos_inicio[pred] + self.problema.acciones[pred].duracion
                    max_tiempo = max(max_tiempo, fin_pred)
            tiempos_inicio[accion] = max_tiempo
            self.problema.acciones[accion].tiempo_inicio = max_tiempo
            self.problema.acciones[accion].estado = EstadoAccion.PROGRAMADA

            # Agregar al plan final
            if accion not in ["INICIO", "FIN"]:
                self.plan.append((max_tiempo, accion))

        # Ordenar el plan por tiempo
        self.plan.sort()

    def _orden_topologico(self, grafo: Dict[str, Set[str]]) -> List[str]:
        """
        Orden topológico de un grafo dirigido acíclico

        Args:
            grafo (Dict[str, Set[str]]): Grafo de precedencia

        Returns:
            List[str]: Orden topológico de los nodos
        """
        visitados = set()
        orden = []

        def visitar(nodo):
            if nodo not in visitados:
                visitados.add(nodo)
                for vecino in grafo.get(nodo, set()):
                    visitar(vecino)
                orden.append(nodo)

        for nodo in list(grafo.keys()):
            visitar(nodo)

        return orden[::-1]  # Invertir para obtener el orden correcto

def ejemplo_bloques_parcial():
    """
    Ejemplo de planificación parcialmente ordenada en el dominio de bloques
    """
    # Definir acciones
    acciones = {
        "mover_A_B": AccionParcial(
            nombre="mover_A_B",
            precondiciones={"libre(A)", "libre(B)", "en(A, Mesa)"},
            efectos={"en(A, B)", "¬en(A, Mesa)", "¬libre(B)"},
            duracion=1
        ),
        "mover_A_C": AccionParcial(
            nombre="mover_A_C",
            precondiciones={"libre(A)", "libre(C)", "en(A, Mesa)"},
            efectos={"en(A, C)", "¬en(A, Mesa)", "¬libre(C)"},
            duracion=1
        ),
        "mover_B_C": AccionParcial(
            nombre="mover_B_C",
            precondiciones={"libre(B)", "libre(C)", "en(B, Mesa)"},
            efectos={"en(B, C)", "¬en(B, Mesa)", "¬libre(C)"},
            duracion=1
        ),
        "mover_C_A": AccionParcial(
            nombre="mover_C_A",
            precondiciones={"libre(C)", "libre(A)", "en(C, Mesa)"},
            efectos={"en(C, A)", "¬en(C, Mesa)", "¬libre(A)"},
            duracion=1
        )
    }

    # Estado inicial
    estado_inicial = {
        "en(A, Mesa)", "en(B, Mesa)", "en(C, Mesa)",
        "libre(A)", "libre(B)", "libre(C)", "libre(Mesa)"
    }

    # Objetivo: A sobre B y B sobre C
    objetivos = {"en(A, B)", "en(B, C)"}

    # Crear problema de planificación parcial
    problema = PlanParcial(
        acciones=acciones,
        restricciones=[],
        estado_actual=estado_inicial,
        objetivos=objetivos
    )

    # Planificar
    planificador = PlanificadorParcial(problema)
    plan = planificador.planificar()

    # Mostrar resultados
    print("\n=== PLANIFICACIÓN PARCIALMENTE ORDENADA ===")
    if plan:
        print("\nPlan encontrado:")
        for tiempo, accion in plan:
            print(f"Tiempo {tiempo}: {accion}")

        print("\nRestricciones de orden:")
        for restriccion in problema.restricciones:
            print(f"{restriccion.accion_a} {restriccion.tipo.name.lower()} {restriccion.accion_b}")

        print("\nEnlaces causales:")
        for (a, b, p) in planificador.causal_links:
            print(f"{a} provee {p} para {b}")
    else:
        print("No se encontró plan solución")

if __name__ == "__main__":
    ejemplo_bloques_parcial()


