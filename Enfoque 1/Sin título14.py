# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 11:12:40 2025

@author: elvin
"""

import heapq
class NodoAEstrella:
    def __init__(self, estado, padre=None):
        self.estado = estado        # Identificador del nodo (ej: coordenadas)
        self.padre = padre          # Nodo padre en el camino
        self.g = 0                  # Costo acumulado desde inicio
        self.h = 0                  # Heurística (estimado a meta)
        self.f = 0                  # Costo total (g + h)
    
    def __lt__(self, otro):         # Comparador para heapq
        return self.f < otro.f      # Ordena por costo total

def a_estrella(grafo, inicio, meta, heuristica):
    abiertos = []                   # Cola de prioridad para nodos por explorar
    cerrados = set()                # Conjunto de nodos ya explorados
    
    nodo_inicio = NodoAEstrella(inicio)
    nodo_inicio.h = heuristica(inicio, meta)
    nodo_inicio.f = nodo_inicio.g + nodo_inicio.h
    heapq.heappush(abiertos, nodo_inicio)
    
    while abiertos:
        actual = heapq.heappop(abiertos)
        
        if actual.estado == meta:
            camino = []
            while actual:
                camino.append(actual.estado)
                actual = actual.padre
            return camino[::-1]      # Devuelve camino invertido
        
        cerrados.add(actual.estado)
        
        for vecino, costo in grafo[actual.estado]:
            if vecino in cerrados:
                continue
            
            nuevo_g = actual.g + costo
            nuevo_nodo = NodoAEstrella(vecino, actual)
            nuevo_nodo.g = nuevo_g
            nuevo_nodo.h = heuristica(vecino, meta)
            nuevo_nodo.f = nuevo_nodo.g + nuevo_nodo.h
            
            # Verifica si ya está en abiertos con menor costo
            en_abiertos = False
            for nodo in abiertos:
                if nodo.estado == vecino and nodo.f <= nuevo_nodo.f:
                    en_abiertos = True
                    break
            
            if not en_abiertos:
                heapq.heappush(abiertos, nuevo_nodo)
    
    return None  # No se encontró camino

class NodoAOEstrella:
    def __init__(self, estado, padre=None):
        self.estado = estado        # Identificador del nodo
        self.padre = padre          # Nodo padre en el camino
        self.g = 0                  # Costo acumulado
        self.h = 0                  # Heurística
        self.f = 0                  # Costo total (g + h)
        self.resuelto = False       # Marca si el nodo está resuelto
    
    def __lt__(self, otro):
        return self.f < otro.f      # Ordena por costo total

def ao_estrella(grafo, inicio, meta, heuristica):
    abiertos = []                   # Cola de prioridad para nodos por explorar
    cerrados = set()                # Nodos ya explorados
    
    nodo_inicio = NodoAOEstrella(inicio)
    nodo_inicio.h = heuristica(inicio, meta)
    nodo_inicio.f = nodo_inicio.g + nodo_inicio.h
    heapq.heappush(abiertos, nodo_inicio)
    
    while abiertos:
        actual = heapq.heappop(abiertos)
        
        if actual.estado == meta:
            actual.resuelto = True
            camino = []
            while actual:
                camino.append(actual.estado)
                actual = actual.padre
            return camino[::-1]      # Devuelve camino óptimo
        
        cerrados.add(actual.estado)
        
        # Expande el nodo actual
        for vecino, costo in grafo[actual.estado]:
            if vecino in cerrados:
                continue
            
            nuevo_g = actual.g + costo
            nuevo_nodo = NodoAOEstrella(vecino, actual)
            nuevo_nodo.g = nuevo_g
            nuevo_nodo.h = heuristica(vecino, meta)
            nuevo_nodo.f = nuevo_nodo.g + nuevo_nodo.h
            
            # Verifica si el vecino conduce a una solución
            if nuevo_nodo.estado == meta:
                nuevo_nodo.resuelto = True
            
            # Actualiza costos si encontramos un camino mejor
            actualizado = False
            for nodo in abiertos:
                if nodo.estado == vecino and nodo.f > nuevo_nodo.f:
                    nodo.f = nuevo_nodo.f
                    nodo.g = nuevo_nodo.g
                    nodo.padre = actual
                    actualizado = True
                    heapq.heapify(abiertos)  # Reordena la cola
                    break
            
            if not actualizado:
                heapq.heappush(abiertos, nuevo_nodo)
    
    return None  # No se encontró solución

# --- Heurísticas de ejemplo ---
def distancia_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# --- Ejemplo de uso ---
if __name__ == "__main__":
    # Grafo de ejemplo (grid 3x3)
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
    
    inicio = (0, 0)
    meta = (2, 2)
    
    print("=== A* ===")
    camino_a_estrella = a_estrella(grafo_grid, inicio, meta, distancia_manhattan)
    print("Camino encontrado:", " -> ".join(f"({x},{y})" for x, y in camino_a_estrella))
    
    print("\n=== AO* ===")
    camino_ao_estrella = ao_estrella(grafo_grid, inicio, meta, distancia_manhattan)
    print("Camino óptimo encontrado:", " -> ".join(f"({x},{y})" for x, y in camino_ao_estrella))