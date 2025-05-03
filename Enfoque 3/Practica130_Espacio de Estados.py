# -*- coding: utf-8 -*-


# Importaciones necesarias
from typing import Dict, List, Set, Optional, Tuple, Callable
from dataclasses import dataclass
from enum import Enum, auto
import heapq
from collections import deque

class TipoBusqueda(Enum):
    """Tipos de algoritmos de búsqueda en espacio de estados"""
    AMPLITUD = auto()      # BFS (Breadth-First Search)
    PROFUNDIDAD = auto()   # DFS (Depth-First Search)
    UNIFORME = auto()      # UCS (Uniform Cost Search)
    AVARA = auto()         # Greedy Best-First Search
    A_ESTRELLA = auto()    # A* Search

@dataclass
class Estado:
    """Estructura para representar un estado en el espacio de búsqueda"""
    id: str                   # Identificador único del estado
    datos: Dict               # Datos específicos del dominio
    costo: float = 0          # Costo acumulado para llegar a este estado
    heuristica: float = 0     # Valor heurístico (para búsquedas informadas)
    padre: Optional['Estado'] = None  # Estado padre en el camino
    accion: Optional[str] = None      # Acción que llevó a este estado

class ProblemaEspacioEstados:
    """
    Define un problema de búsqueda en espacio de estados con:
    - Estado inicial
    - Función de sucesores
    - Test de objetivo
    - Costo de acciones
    - Heurística (opcional)
    """
    
    def __init__(self, estado_inicial: Estado):
        """
        Inicializa el problema con un estado inicial
        
        Args:
            estado_inicial (Estado): Estado inicial de la búsqueda
        """
        self.estado_inicial = estado_inicial
        self.estados_generados = 0  # Contador de estados generados
    
    def es_objetivo(self, estado: Estado) -> bool:
        """
        Determina si un estado es estado objetivo
        
        Args:
            estado (Estado): Estado a evaluar
            
        Returns:
            bool: True si es estado objetivo
        """
        raise NotImplementedError("Método abstracto")
    
    def sucesores(self, estado: Estado) -> List[Tuple[str, Estado]]:
        """
        Genera los estados sucesores de un estado dado
        
        Args:
            estado (Estado): Estado actual
            
        Returns:
            List[Tuple[str, Estado]]: Lista de (acción, estado sucesor)
        """
        raise NotImplementedError("Método abstracto")
    
    def costo_accion(self, estado: Estado, accion: str, sucesor: Estado) -> float:
        """
        Calcula el costo de una acción (por defecto 1 para todos)
        
        Args:
            estado (Estado): Estado origen
            accion (str): Acción aplicada
            sucesor (Estado): Estado resultante
            
        Returns:
            float: Costo de la acción
        """
        return 1.0
    
    def heuristica(self, estado: Estado) -> float:
        """
        Estimación heurística del costo al objetivo (por defecto 0)
        
        Args:
            estado (Estado): Estado a evaluar
            
        Returns:
            float: Valor heurístico
        """
        return 0.0

class BuscadorEspacioEstados:
    """
    Implementa diversos algoritmos de búsqueda en espacio de estados
    """
    
    def __init__(self, problema: ProblemaEspacioEstados):
        """
        Inicializa el buscador con un problema concreto
        
        Args:
            problema (ProblemaEspacioEstados): Problema a resolver
        """
        self.problema = problema
    
    def buscar(self, tipo: TipoBusqueda, max_estados: int = 10000) -> Optional[Estado]:
        """
        Realiza la búsqueda según el algoritmo especificado
        
        Args:
            tipo (TipoBusqueda): Tipo de algoritmo a usar
            max_estados (int): Límite de estados a generar
            
        Returns:
            Optional[Estado]: Estado objetivo encontrado o None
        """
        self.problema.estados_generados = 0
        
        if tipo == TipoBusqueda.AMPLITUD:
            return self._busqueda_amplitud(max_estados)
        elif tipo == TipoBusqueda.PROFUNDIDAD:
            return self._busqueda_profundidad(max_estados)
        elif tipo == TipoBusqueda.UNIFORME:
            return self._busqueda_costo_uniforme(max_estados)
        elif tipo == TipoBusqueda.AVARA:
            return self._busqueda_avara(max_estados)
        elif tipo == TipoBusqueda.A_ESTRELLA:
            return self._busqueda_a_estrella(max_estados)
        else:
            raise ValueError("Tipo de búsqueda no válido")
    
    def _busqueda_amplitud(self, max_estados: int) -> Optional[Estado]:
        """
        Búsqueda en amplitud (BFS) - óptima para costos uniformes
        
        Args:
            max_estados (int): Límite de estados a generar
            
        Returns:
            Optional[Estado]: Estado objetivo o None
        """
        frontera = deque()
        frontera.append(self.problema.estado_inicial)
        
        explorados = set()
        explorados.add(self.problema.estado_inicial.id)
        
        while frontera and self.problema.estados_generados < max_estados:
            estado_actual = frontera.popleft()
            
            if self.problema.es_objetivo(estado_actual):
                return estado_actual
            
            for accion, sucesor in self.problema.sucesores(estado_actual):
                if sucesor.id not in explorados:
                    explorados.add(sucesor.id)
                    frontera.append(sucesor)
                    self.problema.estados_generados += 1
        
        return None
    
    def _busqueda_profundidad(self, max_estados: int) -> Optional[Estado]:
        """
        Búsqueda en profundidad (DFS) - no óptima pero requiere poca memoria
        
        Args:
            max_estados (int): Límite de estados a generar
            
        Returns:
            Optional[Estado]: Estado objetivo o None
        """
        frontera = []
        frontera.append(self.problema.estado_inicial)
        
        explorados = set()
        explorados.add(self.problema.estado_inicial.id)
        
        while frontera and self.problema.estados_generados < max_estados:
            estado_actual = frontera.pop()
            
            if self.problema.es_objetivo(estado_actual):
                return estado_actual
            
            for accion, sucesor in reversed(self.problema.sucesores(estado_actual)):
                if sucesor.id not in explorados:
                    explorados.add(sucesor.id)
                    frontera.append(sucesor)
                    self.problema.estados_generados += 1
        
        return None
    
    def _busqueda_costo_uniforme(self, max_estados: int) -> Optional[Estado]:
        """
        Búsqueda de costo uniforme (UCS) - óptima para costos variables
        
        Args:
            max_estados (int): Límite de estados a generar
            
        Returns:
            Optional[Estado]: Estado objetivo o None
        """
        frontera = []
        heapq.heappush(frontera, (0, self.problema.estado_inicial))
        
        explorados = {}
        explorados[self.problema.estado_inicial.id] = 0
        
        while frontera and self.problema.estados_generados < max_estados:
            _, estado_actual = heapq.heappop(frontera)
            
            if self.problema.es_objetivo(estado_actual):
                return estado_actual
            
            for accion, sucesor in self.problema.sucesores(estado_actual):
                nuevo_costo = estado_actual.costo + self.problema.costo_accion(estado_actual, accion, sucesor)
                
                if sucesor.id not in explorados or nuevo_costo < explorados[sucesor.id]:
                    explorados[sucesor.id] = nuevo_costo
                    sucesor.costo = nuevo_costo
                    sucesor.padre = estado_actual
                    sucesor.accion = accion
                    heapq.heappush(frontera, (nuevo_costo, sucesor))
                    self.problema.estados_generados += 1
        
        return None
    
    def _busqueda_avara(self, max_estados: int) -> Optional[Estado]:
        """
        Búsqueda avara (Greedy Best-First) - no óptima pero rápida
        
        Args:
            max_estados (int): Límite de estados a generar
            
        Returns:
            Optional[Estado]: Estado objetivo o None
        """
        frontera = []
        heapq.heappush(frontera, (self.problema.heuristica(self.problema.estado_inicial), self.problema.estado_inicial))
        
        explorados = set()
        explorados.add(self.problema.estado_inicial.id)
        
        while frontera and self.problema.estados_generados < max_estados:
            _, estado_actual = heapq.heappop(frontera)
            
            if self.problema.es_objetivo(estado_actual):
                return estado_actual
            
            for accion, sucesor in self.problema.sucesores(estado_actual):
                if sucesor.id not in explorados:
                    explorados.add(sucesor.id)
                    h = self.problema.heuristica(sucesor)
                    heapq.heappush(frontera, (h, sucesor))
                    self.problema.estados_generados += 1
        
        return None
    
    def _busqueda_a_estrella(self, max_estados: int) -> Optional[Estado]:
        """
        Búsqueda A* - óptima y eficiente con buena heurística
        
        Args:
            max_estados (int): Límite de estados a generar
            
        Returns:
            Optional[Estado]: Estado objetivo o None
        """
        frontera = []
        f = self.problema.heuristica(self.problema.estado_inicial)
        heapq.heappush(frontera, (f, self.problema.estado_inicial))
        
        explorados = {}
        explorados[self.problema.estado_inicial.id] = 0
        
        while frontera and self.problema.estados_generados < max_estados:
            _, estado_actual = heapq.heappop(frontera)
            
            if self.problema.es_objetivo(estado_actual):
                return estado_actual
            
            for accion, sucesor in self.problema.sucesores(estado_actual):
                nuevo_costo = estado_actual.costo + self.problema.costo_accion(estado_actual, accion, sucesor)
                
                if sucesor.id not in explorados or nuevo_costo < explorados[sucesor.id]:
                    explorados[sucesor.id] = nuevo_costo
                    sucesor.costo = nuevo_costo
                    sucesor.padre = estado_actual
                    sucesor.accion = accion
                    f = nuevo_costo + self.problema.heuristica(sucesor)
                    heapq.heappush(frontera, (f, sucesor))
                    self.problema.estados_generados += 1
        
        return None
    
    def reconstruir_camino(self, estado: Estado) -> List[Tuple[str, Estado]]:
        """
        Reconstruye el camino desde el estado inicial hasta el estado dado
        
        Args:
            estado (Estado): Estado final del camino
            
        Returns:
            List[Tuple[str, Estado]]: Lista de (acción, estado) del camino
        """
        camino = []
        actual = estado
        
        while actual.padre is not None:
            camino.append((actual.accion, actual))
            actual = actual.padre
        
        camino.reverse()
        return camino

class ProblemaLaberinto(ProblemaEspacioEstados):
    """
    Problema concreto: encontrar camino en un laberinto
    Ejemplo de implementación de un problema de espacio de estados
    """
    
    def __init__(self, laberinto: List[List[str]], inicio: Tuple[int, int], objetivo: Tuple[int, int]):
        """
        Inicializa el problema del laberinto
        
        Args:
            laberinto (List[List[str]]): Matriz representando el laberinto
            inicio (Tuple[int, int]): Coordenadas (fila, columna) de inicio
            objetivo (Tuple[int, int]): Coordenadas del objetivo
        """
        self.laberinto = laberinto
        self.filas = len(laberinto)
        self.columnas = len(laberinto[0]) if self.filas > 0 else 0
        self.objetivo = objetivo
        
        # Crear estado inicial
        estado_inicial = Estado(
            id=f"{inicio[0]},{inicio[1]}",
            datos={'posicion': inicio},
            costo=0,
            heuristica=self._distancia_manhattan(inicio)
        )
        
        super().__init__(estado_inicial)
    
    def es_objetivo(self, estado: Estado) -> bool:
        """Verifica si la posición actual es la objetivo"""
        pos = estado.datos['posicion']
        return pos == self.objetivo
    
    def sucesores(self, estado: Estado) -> List[Tuple[str, Estado]]:
        """Genera movimientos válidos (arriba, abajo, izquierda, derecha)"""
        movimientos = [
            ('arriba', (-1, 0)),
            ('abajo', (1, 0)),
            ('izquierda', (0, -1)),
            ('derecha', (0, 1))
        ]
        
        pos_actual = estado.datos['posicion']
        sucesores = []
        
        for nombre, (df, dc) in movimientos:
            nueva_f = pos_actual[0] + df
            nueva_c = pos_actual[1] + dc
            
            if 0 <= nueva_f < self.filas and 0 <= nueva_c < self.columnas:
                if self.laberinto[nueva_f][nueva_c] != '#':  # No es pared
                    nueva_pos = (nueva_f, nueva_c)
                    nuevo_estado = Estado(
                        id=f"{nueva_f},{nueva_c}",
                        datos={'posicion': nueva_pos},
                        costo=estado.costo + 1,
                        heuristica=self._distancia_manhattan(nueva_pos),
                        padre=estado,
                        accion=nombre
                    )
                    sucesores.append((nombre, nuevo_estado))
        
        return sucesores
    
    def _distancia_manhattan(self, pos: Tuple[int, int]) -> float:
        """Calcula la heurística (distancia Manhattan al objetivo)"""
        return abs(pos[0] - self.objetivo[0]) + abs(pos[1] - self.objetivo[1])

def ejemplo_laberinto():
    """
    Crea y resuelve un problema de laberinto con diferentes algoritmos
    """
    # Definir laberinto ('.' = camino libre, '#' = pared)
    laberinto = [
        ['.', '.', '.', '.', '#', '.', '.', '.', '.', '.'],
        ['.', '#', '#', '.', '#', '.', '#', '#', '#', '.'],
        ['.', '#', '.', '.', '#', '.', '.', '.', '#', '.'],
        ['.', '#', '.', '#', '#', '#', '#', '.', '#', '.'],
        ['.', '#', '.', '.', '.', '.', '#', '.', '#', '.'],
        ['.', '#', '#', '#', '#', '.', '#', '.', '#', '.'],
        ['.', '.', '.', '.', '.', '.', '#', '.', '.', '.'],
        ['.', '#', '#', '#', '#', '#', '#', '#', '#', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '#', '.'],
        ['.', '#', '#', '#', '#', '#', '#', '#', '#', '.']
    ]
    
    inicio = (0, 0)
    objetivo = (9, 9)
    
    problema = ProblemaLaberinto(laberinto, inicio, objetivo)
    buscador = BuscadorEspacioEstados(problema)
    
    # Probar diferentes algoritmos de búsqueda
    algoritmos = [
        (TipoBusqueda.AMPLITUD, "Búsqueda en Amplitud (BFS)"),
        (TipoBusqueda.PROFUNDIDAD, "Búsqueda en Profundidad (DFS)"),
        (TipoBusqueda.UNIFORME, "Costo Uniforme (UCS)"),
        (TipoBusqueda.AVARA, "Búsqueda Avara"),
        (TipoBusqueda.A_ESTRELLA, "A*")
    ]
    
    for tipo, nombre in algoritmos:
        print(f"\n=== {nombre} ===")
        solucion = buscador.buscar(tipo)
        
        if solucion:
            camino = buscador.reconstruir_camino(solucion)
            print(f"Camino encontrado ({len(camino)} pasos):")
            for i, (accion, estado) in enumerate(camino, 1):
                print(f"{i}. {accion} -> {estado.datos['posicion']}")
            print(f"Estados generados: {problema.estados_generados}")
        else:
            print("No se encontró solución")
            print(f"Estados generados: {problema.estados_generados}")

if __name__ == "__main__":
    ejemplo_laberinto()