# -*- coding: utf-8 -*-

# Importaciones necesarias
from typing import Dict, List, Set, Optional, Tuple, Callable  # Tipos para type hints
from dataclasses import dataclass                             # Para clases de datos
from enum import Enum, auto                                   # Para enumeraciones
import heapq                                                  # Para colas de prioridad
from collections import deque                                 # Para colas FIFO

class TipoBusqueda(Enum):                                     # Enumeración de algoritmos
    """Tipos de algoritmos de búsqueda en espacio de estados"""
    AMPLITUD = auto()      # BFS (Breadth-First Search)       # Búsqueda en amplitud
    PROFUNDIDAD = auto()   # DFS (Depth-First Search)         # Búsqueda en profundidad
    UNIFORME = auto()      # UCS (Uniform Cost Search)        # Búsqueda de costo uniforme
    AVARA = auto()         # Greedy Best-First Search         # Búsqueda avara
    A_ESTRELLA = auto()    # A* Search                        # Búsqueda A*

@dataclass
class Estado:                                                # Clase para estados
    """Estructura para representar un estado en el espacio de búsqueda"""
    id: str                   # Identificador único del estado # ID único
    datos: Dict               # Datos específicos del dominio  # Información del estado
    costo: float = 0          # Costo acumulado para llegar a este estado # Costo acumulado
    heuristica: float = 0     # Valor heurístico (para búsquedas informadas) # Estimación
    padre: Optional['Estado'] = None  # Estado padre en el camino # Estado anterior
    accion: Optional[str] = None      # Acción que llevó a este estado # Acción aplicada

class ProblemaEspacioEstados:                                # Clase base para problemas
    """
    Define un problema de búsqueda en espacio de estados con:
    - Estado inicial
    - Función de sucesores
    - Test de objetivo
    - Costo de acciones
    - Heurística (opcional)
    """
    
    def __init__(self, estado_inicial: Estado):              # Constructor
        """
        Inicializa el problema con un estado inicial
        
        Args:
            estado_inicial (Estado): Estado inicial de la búsqueda # Estado inicial
        """
        self.estado_inicial = estado_inicial                 # Guardar estado inicial
        self.estados_generados = 0  # Contador de estados generados # Contador
    
    def es_objetivo(self, estado: Estado) -> bool:           # Método abstracto
        """
        Determina si un estado es estado objetivo
        
        Args:
            estado (Estado): Estado a evaluar                # Estado a verificar
            
        Returns:
            bool: True si es estado objetivo                 # Resultado
        """
        raise NotImplementedError("Método abstracto")        # Debe implementarse
    
    def sucesores(self, estado: Estado) -> List[Tuple[str, Estado]]: # Método abstracto
        """
        Genera los estados sucesores de un estado dado
        
        Args:
            estado (Estado): Estado actual                   # Estado origen
            
        Returns:
            List[Tuple[str, Estado]]: Lista de (acción, estado sucesor) # Sucesores
        """
        raise NotImplementedError("Método abstracto")        # Debe implementarse
    
    def costo_accion(self, estado: Estado, accion: str, sucesor: Estado) -> float: # Costo
        """
        Calcula el costo de una acción (por defecto 1 para todos)
        
        Args:
            estado (Estado): Estado origen                  # Estado actual
            accion (str): Acción aplicada                   # Acción realizada
            sucesor (Estado): Estado resultante             # Estado siguiente
            
        Returns:
            float: Costo de la acción                       # Valor del costo
        """
        return 1.0                                          # Costo por defecto
    
    def heuristica(self, estado: Estado) -> float:          # Heurística
        """
        Estimación heurística del costo al objetivo (por defecto 0)
        
        Args:
            estado (Estado): Estado a evaluar               # Estado actual
            
        Returns:
            float: Valor heurístico                        # Estimación
        """
        return 0.0                                          # Heurística por defecto

class BuscadorEspacioEstados:                               # Clase buscador
    """
    Implementa diversos algoritmos de búsqueda en espacio de estados
    """
    
    def __init__(self, problema: ProblemaEspacioEstados):   # Constructor
        """
        Inicializa el buscador con un problema concreto
        
        Args:
            problema (ProblemaEspacioEstados): Problema a resolver # Problema concreto
        """
        self.problema = problema                            # Guardar problema
    
    def buscar(self, tipo: TipoBusqueda, max_estados: int = 10000) -> Optional[Estado]: # Búsqueda
        """
        Realiza la búsqueda según el algoritmo especificado
        
        Args:
            tipo (TipoBusqueda): Tipo de algoritmo a usar   # Tipo de búsqueda
            max_estados (int): Límite de estados a generar # Límite de estados
            
        Returns:
            Optional[Estado]: Estado objetivo encontrado o None # Solución
        """
        self.problema.estados_generados = 0                 # Reiniciar contador
        
        if tipo == TipoBusqueda.AMPLITUD:                   # BFS
            return self._busqueda_amplitud(max_estados)
        elif tipo == TipoBusqueda.PROFUNDIDAD:              # DFS
            return self._busqueda_profundidad(max_estados)
        elif tipo == TipoBusqueda.UNIFORME:                 # UCS
            return self._busqueda_costo_uniforme(max_estados)
        elif tipo == TipoBusqueda.AVARA:                    # Avara
            return self._busqueda_avara(max_estados)
        elif tipo == TipoBusqueda.A_ESTRELLA:               # A*
            return self._busqueda_a_estrella(max_estados)
        else:
            raise ValueError("Tipo de búsqueda no válido")   # Error
    
    def _busqueda_amplitud(self, max_estados: int) -> Optional[Estado]: # BFS
        """
        Búsqueda en amplitud (BFS) - óptima para costos uniformes
        
        Args:
            max_estados (int): Límite de estados a generar # Límite
            
        Returns:
            Optional[Estado]: Estado objetivo o None        # Solución
        """
        frontera = deque()                                  # Cola FIFO
        frontera.append(self.problema.estado_inicial)       # Iniciar con estado inicial
        
        explorados = set()                                  # Conjunto de explorados
        explorados.add(self.problema.estado_inicial.id)     # Marcar inicial como explorado
        
        while frontera and self.problema.estados_generados < max_estados: # Mientras haya frontera
            estado_actual = frontera.popleft()              # Sacar primero
            
            if self.problema.es_objetivo(estado_actual):    # Si es objetivo
                return estado_actual                        # Retornar solución
            
            for accion, sucesor in self.problema.sucesores(estado_actual): # Generar sucesores
                if sucesor.id not in explorados:            # Si no explorado
                    explorados.add(sucesor.id)              # Marcar como explorado
                    frontera.append(sucesor)                # Añadir a frontera
                    self.problema.estados_generados += 1    # Incrementar contador
        
        return None                                         # No solución
    
    def _busqueda_profundidad(self, max_estados: int) -> Optional[Estado]: # DFS
        """
        Búsqueda en profundidad (DFS) - no óptima pero requiere poca memoria
        
        Args:
            max_estados (int): Límite de estados a generar # Límite
            
        Returns:
            Optional[Estado]: Estado objetivo o None      # Solución
        """
        frontera = []                                      # Pila LIFO
        frontera.append(self.problema.estado_inicial)       # Iniciar con estado inicial
        
        explorados = set()                                 # Conjunto de explorados
        explorados.add(self.problema.estado_inicial.id)     # Marcar inicial como explorado
        
        while frontera and self.problema.estados_generados < max_estados: # Mientras haya frontera
            estado_actual = frontera.pop()                  # Sacar último
            
            if self.problema.es_objetivo(estado_actual):    # Si es objetivo
                return estado_actual                        # Retornar solución
            
            for accion, sucesor in reversed(self.problema.sucesores(estado_actual)): # Sucesores en reversa
                if sucesor.id not in explorados:           # Si no explorado
                    explorados.add(sucesor.id)              # Marcar como explorado
                    frontera.append(sucesor)                # Añadir a frontera
                    self.problema.estados_generados += 1    # Incrementar contador
        
        return None                                         # No solución
    
    def _busqueda_costo_uniforme(self, max_estados: int) -> Optional[Estado]: # UCS
        """
        Búsqueda de costo uniforme (UCS) - óptima para costos variables
        
        Args:
            max_estados (int): Límite de estados a generar # Límite
            
        Returns:
            Optional[Estado]: Estado objetivo o None       # Solución
        """
        frontera = []                                      # Cola de prioridad
        heapq.heappush(frontera, (0, self.problema.estado_inicial)) # Iniciar con costo 0
        
        explorados = {}                                    # Diccionario de explorados
        explorados[self.problema.estado_inicial.id] = 0    # Guardar costo inicial
        
        while frontera and self.problema.estados_generados < max_estados: # Mientras haya frontera
            _, estado_actual = heapq.heappop(frontera)      # Sacar de menor costo
            
            if self.problema.es_objetivo(estado_actual):   # Si es objetivo
                return estado_actual                       # Retornar solución
            
            for accion, sucesor in self.problema.sucesores(estado_actual): # Sucesores
                nuevo_costo = estado_actual.costo + self.problema.costo_accion(estado_actual, accion, sucesor) # Calcular costo
                
                if sucesor.id not in explorados or nuevo_costo < explorados[sucesor.id]: # Si es mejor
                    explorados[sucesor.id] = nuevo_costo    # Actualizar costo
                    sucesor.costo = nuevo_costo             # Asignar costo
                    sucesor.padre = estado_actual           # Asignar padre
                    sucesor.accion = accion                 # Asignar acción
                    heapq.heappush(frontera, (nuevo_costo, sucesor)) # Añadir a frontera
                    self.problema.estados_generados += 1    # Incrementar contador
        
        return None                                         # No solución
    
    def _busqueda_avara(self, max_estados: int) -> Optional[Estado]: # Avara
        """
        Búsqueda avara (Greedy Best-First) - no óptima pero rápida
        
        Args:
            max_estados (int): Límite de estados a generar # Límite
            
        Returns:
            Optional[Estado]: Estado objetivo o None       # Solución
        """
        frontera = []                                      # Cola de prioridad
        heapq.heappush(frontera, (self.problema.heuristica(self.problema.estado_inicial), self.problema.estado_inicial)) # Iniciar con heurística
        
        explorados = set()                                 # Conjunto de explorados
        explorados.add(self.problema.estado_inicial.id)    # Marcar inicial como explorado
        
        while frontera and self.problema.estados_generados < max_estados: # Mientras haya frontera
            _, estado_actual = heapq.heappop(frontera)     # Sacar mejor heurística
            
            if self.problema.es_objetivo(estado_actual):   # Si es objetivo
                return estado_actual                       # Retornar solución
            
            for accion, sucesor in self.problema.sucesores(estado_actual): # Sucesores
                if sucesor.id not in explorados:           # Si no explorado
                    explorados.add(sucesor.id)              # Marcar como explorado
                    h = self.problema.heuristica(sucesor)   # Calcular heurística
                    heapq.heappush(frontera, (h, sucesor))  # Añadir a frontera
                    self.problema.estados_generados += 1    # Incrementar contador
        
        return None                                         # No solución
    
    def _busqueda_a_estrella(self, max_estados: int) -> Optional[Estado]: # A*
        """
        Búsqueda A* - óptima y eficiente con buena heurística
        
        Args:
            max_estados (int): Límite de estados a generar # Límite
            
        Returns:
            Optional[Estado]: Estado objetivo o None       # Solución
        """
        frontera = []                                      # Cola de prioridad
        f = self.problema.heuristica(self.problema.estado_inicial) # f = h (g=0 inicial)
        heapq.heappush(frontera, (f, self.problema.estado_inicial)) # Iniciar con f
        
        explorados = {}                                    # Diccionario de explorados
        explorados[self.problema.estado_inicial.id] = 0    # Guardar costo inicial
        
        while frontera and self.problema.estados_generados < max_estados: # Mientras haya frontera
            _, estado_actual = heapq.heappop(frontera)      # Sacar menor f
            
            if self.problema.es_objetivo(estado_actual):    # Si es objetivo
                return estado_actual                       # Retornar solución
            
            for accion, sucesor in self.problema.sucesores(estado_actual): # Sucesores
                nuevo_costo = estado_actual.costo + self.problema.costo_accion(estado_actual, accion, sucesor) # Calcular g
                
                if sucesor.id not in explorados or nuevo_costo < explorados[sucesor.id]: # Si es mejor
                    explorados[sucesor.id] = nuevo_costo    # Actualizar costo
                    sucesor.costo = nuevo_costo             # Asignar costo
                    sucesor.padre = estado_actual           # Asignar padre
                    sucesor.accion = accion                 # Asignar acción
                    f = nuevo_costo + self.problema.heuristica(sucesor) # f = g + h
                    heapq.heappush(frontera, (f, sucesor))  # Añadir a frontera
                    self.problema.estados_generados += 1    # Incrementar contador
        
        return None                                         # No solución
    
    def reconstruir_camino(self, estado: Estado) -> List[Tuple[str, Estado]]: # Reconstruir
        """
        Reconstruye el camino desde el estado inicial hasta el estado dado
        
        Args:
            estado (Estado): Estado final del camino       # Estado final
            
        Returns:
            List[Tuple[str, Estado]]: Lista de (acción, estado) del camino # Camino
        """
        camino = []                                        # Lista para camino
        actual = estado                                    # Comenzar desde final
        
        while actual.padre is not None:                    # Mientras tenga padre
            camino.append((actual.accion, actual))          # Añadir al camino
            actual = actual.padre                           # Mover al padre
        
        camino.reverse()                                   # Invertir orden
        return camino                                      # Retornar camino

class ProblemaLaberinto(ProblemaEspacioEstados):           # Problema concreto
    """
    Problema concreto: encontrar camino en un laberinto
    Ejemplo de implementación de un problema de espacio de estados
    """
    
    def __init__(self, laberinto: List[List[str]], inicio: Tuple[int, int], objetivo: Tuple[int, int]): # Constructor
        """
        Inicializa el problema del laberinto
        
        Args:
            laberinto (List[List[str]]): Matriz representando el laberinto # Laberinto
            inicio (Tuple[int, int]): Coordenadas (fila, columna) de inicio # Inicio
            objetivo (Tuple[int, int]): Coordenadas del objetivo           # Objetivo
        """
        self.laberinto = laberinto                         # Guardar laberinto
        self.filas = len(laberinto)                        # Número de filas
        self.columnas = len(laberinto[0]) if self.filas > 0 else 0 # Número de columnas
        self.objetivo = objetivo                           # Guardar objetivo
        
        # Crear estado inicial
        estado_inicial = Estado(                           # Estado inicial
            id=f"{inicio[0]},{inicio[1]}",                 # ID como coordenadas
            datos={'posicion': inicio},                    # Datos con posición
            costo=0,                                       # Costo inicial 0
            heuristica=self._distancia_manhattan(inicio)   # Calcular heurística
        )
        
        super().__init__(estado_inicial)                   # Llamar constructor padre
    
    def es_objetivo(self, estado: Estado) -> bool:         # Verificar objetivo
        """Verifica si la posición actual es la objetivo"""
        pos = estado.datos['posicion']                     # Obtener posición
        return pos == self.objetivo                        # Comparar con objetivo
    
    def sucesores(self, estado: Estado) -> List[Tuple[str, Estado]]: # Generar sucesores
        """Genera movimientos válidos (arriba, abajo, izquierda, derecha)"""
        movimientos = [                                    # Posibles movimientos
            ('arriba', (-1, 0)),                           # Arriba
            ('abajo', (1, 0)),                             # Abajo
            ('izquierda', (0, -1)),                        # Izquierda
            ('derecha', (0, 1))                            # Derecha
        ]
        
        pos_actual = estado.datos['posicion']              # Posición actual
        sucesores = []                                     # Lista de sucesores
        
        for nombre, (df, dc) in movimientos:               # Para cada movimiento
            nueva_f = pos_actual[0] + df                   # Nueva fila
            nueva_c = pos_actual[1] + dc                   # Nueva columna
            
            if 0 <= nueva_f < self.filas and 0 <= nueva_c < self.columnas: # Si está dentro
                if self.laberinto[nueva_f][nueva_c] != '#':  # Si no es pared
                    nueva_pos = (nueva_f, nueva_c)          # Nueva posición
                    nuevo_estado = Estado(                  # Crear estado
                        id=f"{nueva_f},{nueva_c}",          # ID como coordenadas
                        datos={'posicion': nueva_pos},      # Datos con posición
                        costo=estado.costo + 1,            # Incrementar costo
                        heuristica=self._distancia_manhattan(nueva_pos), # Calcular heurística
                        padre=estado,                       # Asignar padre
                        accion=nombre                       # Asignar acción
                    )
                    sucesores.append((nombre, nuevo_estado)) # Añadir a sucesores
        
        return sucesores                                    # Retornar sucesores
    
    def _distancia_manhattan(self, pos: Tuple[int, int]) -> float: # Heurística
        """Calcula la heurística (distancia Manhattan al objetivo)"""
        return abs(pos[0] - self.objetivo[0]) + abs(pos[1] - self.objetivo[1]) # Suma de diferencias

def ejemplo_laberinto():                                   # Ejemplo de uso
    """
    Crea y resuelve un problema de laberinto con diferentes algoritmos
    """
    # Definir laberinto ('.' = camino libre, '#' = pared)
    laberinto = [                                         # Laberinto
        ['.', '.', '.', '.', '#', '.', '.', '.', '.', '.'], # Fila 0
        ['.', '#', '#', '.', '#', '.', '#', '#', '#', '.'], # Fila 1
        ['.', '#', '.', '.', '#', '.', '.', '.', '#', '.'], # Fila 2
        ['.', '#', '.', '#', '#', '#', '#', '.', '#', '.'], # Fila 3
        ['.', '#', '.', '.', '.', '.', '#', '.', '#', '.'], # Fila 4
        ['.', '#', '#', '#', '#', '.', '#', '.', '#', '.'], # Fila 5
        ['.', '.', '.', '.', '.', '.', '#', '.', '.', '.'], # Fila 6
        ['.', '#', '#', '#', '#', '#', '#', '#', '#', '.'], # Fila 7
        ['.', '.', '.', '.', '.', '.', '.', '.', '#', '.'], # Fila 8
        ['.', '#', '#', '#', '#', '#', '#', '#', '#', '.']  # Fila 9
    ]
    
    inicio = (0, 0)                                       # Posición inicial
    objetivo = (9, 9)                                     # Posición objetivo
    
    problema = ProblemaLaberinto(laberinto, inicio, objetivo) # Crear problema
    buscador = BuscadorEspacioEstados(problema)           # Crear buscador
    
    # Probar diferentes algoritmos de búsqueda
    algoritmos = [                                        # Algoritmos a probar
        (TipoBusqueda.AMPLITUD, "Búsqueda en Amplitud (BFS)"), # BFS
        (TipoBusqueda.PROFUNDIDAD, "Búsqueda en Profundidad (DFS)"), # DFS
        (TipoBusqueda.UNIFORME, "Costo Uniforme (UCS)"),  # UCS
        (TipoBusqueda.AVARA, "Búsqueda Avara"),           # Avara
        (TipoBusqueda.A_ESTRELLA, "A*")                   # A*
    ]
    
    for tipo, nombre in algoritmos:                        # Para cada algoritmo
        print(f"\n=== {nombre} ===")                       # Mostrar nombre
        solucion = buscador.buscar(tipo)                   # Buscar solución
        
        if solucion:                                       # Si hay solución
            camino = buscador.reconstruir_camino(solucion) # Reconstruir camino
            print(f"Camino encontrado ({len(camino)} pasos):") # Mostrar longitud
            for i, (accion, estado) in enumerate(camino, 1): # Mostrar pasos
                print(f"{i}. {accion} -> {estado.datos['posicion']}")
            print(f"Estados generados: {problema.estados_generados}") # Mostrar contador
        else:
            print("No se encontró solución")                # Mensaje de no solución
            print(f"Estados generados: {problema.estados_generados}") # Mostrar contador

if __name__ == "__main__":                                 # Punto de entrada
    ejemplo_laberinto()                                    # Ejecutar ejemplo