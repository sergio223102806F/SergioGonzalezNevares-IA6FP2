# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 11:12:40 2025

@author: elvin

Implementación de los algoritmos A* y AO* para búsqueda de caminos óptimos.
Incluye clases para nodos y funciones de búsqueda con heurísticas.
"""

import heapq  # Importa módulo para colas de prioridad

class NodoAEstrella:
    """
    Clase que representa un nodo en el algoritmo A*.
    Almacena información del estado, costos y heurísticas.
    """
    def __init__(self, estado, padre=None):
        self.estado = estado        # Identificador único del nodo (ej: coordenadas)
        self.padre  = padre         # Referencia al nodo padre en el camino
        self.g      = 0             # Costo acumulado desde el nodo inicial
        self.h      = 0             # Valor heurístico (estimación a meta)
        self.f      = 0             # Costo total (g + h)
    
    def __lt__(self, otro):         # Método para comparación de nodos
        return self.f < otro.f      # Ordena por costo total (para heapq)

def a_estrella(grafo, inicio, meta, heuristica):
    """
    Implementación del algoritmo A* para búsqueda de caminos óptimos.
    
    Parámetros:
        grafo:      Diccionario de adyacencia del grafo         (dict)
        inicio:     Estado inicial de la búsqueda               (any)
        meta:       Estado objetivo                             (any)
        heuristica: Función de estimación heurística           (callable)
    
    Retorna:
        Lista con el camino óptimo o None si no hay solución    (list/None)
    """
    abiertos  = []                  # Cola de prioridad (nodos por explorar)
    cerrados  = set()               # Conjunto de nodos ya explorados
    
    nodo_inicio       = NodoAEstrella(inicio)          # Crea nodo inicial
    nodo_inicio.h     = heuristica(inicio, meta)       # Calcula heurística
    nodo_inicio.f     = nodo_inicio.g + nodo_inicio.h  # Costo total inicial
    heapq.heappush(abiertos, nodo_inicio)              # Agrega a abiertos
    
    while abiertos:                                     # Mientras haya nodos
        actual = heapq.heappop(abiertos)                # Extrae el mejor nodo
        
        if actual.estado == meta:                       # Si es solución
            camino = []                                 # Reconstruye camino
            while actual:
                camino.append(actual.estado)
                actual = actual.padre
            return camino[::-1]                         # Devuelve camino invertido
        
        cerrados.add(actual.estado)                    # Marca como explorado
        
        for vecino, costo in grafo[actual.estado]:     # Expande vecinos
            if vecino in cerrados:                     # Si ya fue explorado
                continue                               # Lo ignora
            
            nuevo_g       = actual.g + costo           # Calcula nuevo costo
            nuevo_nodo    = NodoAEstrella(vecino, actual)  # Crea nodo vecino
            nuevo_nodo.g  = nuevo_g                    # Asigna costo acumulado
            nuevo_nodo.h  = heuristica(vecino, meta)   # Calcula heurística
            nuevo_nodo.f  = nuevo_nodo.g + nuevo_nodo.h  # Costo total
            
            # Verifica si ya está en abiertos con menor costo
            en_abiertos = False
            for nodo in abiertos:
                if nodo.estado == vecino and nodo.f <= nuevo_nodo.f:
                    en_abiertos = True
                    break
            
            if not en_abiertos:                        # Si es nuevo o mejor
                heapq.heappush(abiertos, nuevo_nodo)   # Agrega a abiertos
    
    return None                                        # No encontró solución

class NodoAOEstrella:
    """
    Clase que representa un nodo en el algoritmo AO*.
    Extiende la funcionalidad de A* con marca de resolución.
    """
    def __init__(self, estado, padre=None):
        self.estado   = estado        # Identificador único del nodo
        self.padre    = padre         # Referencia al nodo padre
        self.g        = 0             # Costo acumulado desde inicio
        self.h        = 0             # Valor heurístico (estimación)
        self.f        = 0             # Costo total (g + h)
        self.resuelto = False         # Indica si el nodo lleva a solución
    
    def __lt__(self, otro):           # Método para comparación de nodos
        return self.f < otro.f        # Ordena por costo total (para heapq)

def ao_estrella(grafo, inicio, meta, heuristica):
    """
    Implementación del algoritmo AO* para búsqueda de caminos óptimos.
    Versión adaptativa que reevalúa caminos durante la búsqueda.
    
    Parámetros:
        grafo:      Diccionario de adyacencia del grafo         (dict)
        inicio:     Estado inicial de la búsqueda               (any)
        meta:       Estado objetivo                             (any)
        heuristica: Función de estimación heurística           (callable)
    
    Retorna:
        Lista con el camino óptimo o None si no hay solución    (list/None)
    """
    abiertos  = []                  # Cola de prioridad (nodos por explorar)
    cerrados  = set()               # Conjunto de nodos ya explorados
    
    nodo_inicio       = NodoAOEstrella(inicio)        # Crea nodo inicial
    nodo_inicio.h     = heuristica(inicio, meta)      # Calcula heurística
    nodo_inicio.f     = nodo_inicio.g + nodo_inicio.h # Costo total inicial
    heapq.heappush(abiertos, nodo_inicio)             # Agrega a abiertos
    
    while abiertos:                                   # Mientras haya nodos
        actual = heapq.heappop(abiertos)             # Extrae el mejor nodo
        
        if actual.estado == meta:                    # Si es solución
            actual.resuelto = True                   # Marca como resuelto
            camino = []                              # Reconstruye camino
            while actual:
                camino.append(actual.estado)
                actual = actual.padre
            return camino[::-1]                      # Devuelve camino invertido
        
        cerrados.add(actual.estado)                 # Marca como explorado
        
        for vecino, costo in grafo[actual.estado]:  # Expande vecinos
            if vecino in cerrados:                  # Si ya fue explorado
                continue                            # Lo ignora
            
            nuevo_g       = actual.g + costo        # Calcula nuevo costo
            nuevo_nodo    = NodoAOEstrella(vecino, actual)  # Crea nodo
            nuevo_nodo.g  = nuevo_g                 # Asigna costo acumulado
            nuevo_nodo.h  = heuristica(vecino, meta)# Calcula heurística
            nuevo_nodo.f  = nuevo_nodo.g + nuevo_nodo.h  # Costo total
            
            if nuevo_nodo.estado == meta:           # Si es solución
                nuevo_nodo.resuelto = True          # Marca como resuelto
            
            # Actualiza costos si encontramos un camino mejor
            actualizado = False
            for nodo in abiertos:
                if nodo.estado == vecino and nodo.f > nuevo_nodo.f:
                    nodo.f      = nuevo_nodo.f      # Actualiza costo total
                    nodo.g      = nuevo_nodo.g      # Actualiza costo acumulado
                    nodo.padre  = actual            # Actualiza padre
                    actualizado = True
                    heapq.heapify(abiertos)         # Reordena la cola
                    break
            
            if not actualizado:                     # Si es nuevo o mejor
                heapq.heappush(abiertos, nuevo_nodo)# Agrega a abiertos
    
    return None                                    # No encontró solución

def distancia_manhattan(a, b):
    """
    Función heurística de distancia Manhattan para coordenadas.
    
    Parámetros:
        a: Coordenada (x1, y1)                    (tuple)
        b: Coordenada (x2, y2)                    (tuple)
    
    Retorna:
        Distancia Manhattan entre puntos           (float)
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

if __name__ == "__main__":
    # Grafo de ejemplo (grid 3x3 con costos)
    grafo_grid = {
        (0, 0): [((0, 1), 1), ((1, 0), 1)],
        (0, 1): [((0, 0), 1), ((0, 2), 1), ((1, 1), 1.5)],
        (0, 2): [((0, 1), 1), ((1, 2), 1)],
        (1, 0): [((0, 0), 1), ((1, 1), 1), ((2, 0), 1)],
        (1, 1): [((0, 1), 1.5), ((1, 0), 1), ((1, 2), 1), ((2, 1), 1)],
        (1, 2): [((0, 2), 1), ((1, 1), 1), ((2, 2), 1)],
        (2, 0): [((1, 0), 1), ((2, 1), 1)],
        (2, 1): [((1, 1), 1), ((2, 0), 1), ((2, 2), 1)],
        (2, 2): [((1, 2), 1), ((2, 1), 1)]
    }
    
    inicio = (0, 0)                                # Punto de inicio
    meta   = (2, 2)                                # Punto objetivo
    
    # Presentación de resultados para A*
print("\n" + "="*50)                                  # Línea decorativa superior
print(" RESULTADOS DE BÚSQUEDA A* ".center(50, "="))  # Título centrado
print("="*50)                                         # Línea decorativa inferior

# Ejecuta algoritmo A* y muestra resultados
camino_a_estrella = a_estrella(                       # Busca camino con A*
    grafo_grid,                                       # Grafo de búsqueda
    inicio,                                           # Punto de partida
    meta,                                             # Destino final
    distancia_manhattan                               # Función heurística
)
print("Camino encontrado:",                           # Muestra etiqueta
      " → ".join(f"({x},{y})" for x, y in camino_a_estrella))  # Formato coordenadas

# Presentación de resultados para AO*
print("\n" + "="*50)                                  # Línea decorativa superior
print(" RESULTADOS DE BÚSQUEDA AO* ".center(50, "=")) # Título centrado
print("="*50)                                         # Línea decorativa inferior

# Ejecuta algoritmo AO* y muestra resultados
camino_ao_estrella = ao_estrella(                     # Busca camino con AO*
    grafo_grid,                                       # Grafo de búsqueda
    inicio,                                           # Punto de partida
    meta,                                             # Destino final
    distancia_manhattan                               # Función heurística
)
print("Camino óptimo encontrado:",                    # Muestra etiqueta 
      " → ".join(f"({x},{y})" for x, y in camino_ao_estrella))  # Formato coordenadas
print("="*50)                                         # Línea decorativa final