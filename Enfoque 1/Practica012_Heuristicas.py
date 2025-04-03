# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 11:12:40 2025

@author: elvin
"""

import heapq                                     # Para colas de prioridad

class Nodo:                                     # Clase para nodos en el grafo
    def __init__(self, estado, padre=None):     # Constructor
        self.estado = estado                    # Identificador del nodo (ej: coordenadas)
        self.padre = padre                      # Nodo padre en el camino
        self.g = 0                              # Costo acumulado desde inicio
        self.h = 0                              # Heurística (estimado a meta)
        self.f = 0                              # Costo total (g + h)
    
    def __lt__(self, otro):                     # Comparador para heapq
        return self.f < otro.f                  # Ordena por costo total

def a_estrella(grafo, inicio, meta, heuristica): # Algoritmo A*
    abiertos = []                               # Lista de nodos por explorar
    cerrados = set()                            # Conjunto de nodos explorados
    
    nodo_inicio = Nodo(inicio)                  # Crea nodo inicial
    nodo_inicio.h = heuristica(inicio, meta)    # Calcula heurística inicial
    nodo_inicio.f = nodo_inicio.g + nodo_inicio.h
    heapq.heappush(abiertos, nodo_inicio)       # Añade a la cola de prioridad
    
    while abiertos:                             # Mientras haya nodos por explorar
        actual = heapq.heappop(abiertos)        # Extrae el nodo con menor f
        cerrados.add(actual.estado)             # Marca como explorado
        
        if actual.estado == meta:               # Si llegamos a la meta
            camino = []                         # Reconstruye el camino óptimo
            while actual:
                camino.append(actual.estado)
                actual = actual.padre
            return camino[::-1]                 # Devuelve camino invertido
        
        for vecino, costo in grafo[actual.estado]: # Para cada vecino del nodo actual
            if vecino in cerrados:              # Si ya fue explorado, lo salta
                continue
            
            nuevo_g = actual.g + costo          # Costo acumulado real
            nuevo_nodo = Nodo(vecino, actual)   # Crea nodo vecino
            nuevo_nodo.g = nuevo_g
            nuevo_nodo.h = heuristica(vecino, meta)
            nuevo_nodo.f = nuevo_nodo.g + nuevo_nodo.h
            
            # Si ya está en abiertos con mejor g, lo ignora
            if any(nodo.estado == vecino and nodo.f <= nuevo_nodo.f 
                   for nodo in abiertos):
                continue
            
            heapq.heappush(abiertos, nuevo_nodo)# Añade vecino a la cola
    
    return None                                # Si no hay camino

# --- Heurísticas comunes ---
def manhattan(a, b):                           # Distancia Manhattan (para grids)
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def euclidiana(a, b):                          # Distancia Euclidiana
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5

def cero(a, b):                                # Heurística nula (equivale a Dijkstra)
    return 0

# --- Ejemplo de uso ---
if __name__ == "__main__":
    # Grafo representado como diccionario (grid 4x4)
    grafo = {
        (0, 0): [((0, 1), 1), ((1, 0), 1)],    # Esquina superior izquierda
        (0, 1): [((0, 0), 1), ((0, 2), 1), ((1, 1), 1.5)],
        (0, 2): [((0, 1), 1), ((0, 3), 1), ((1, 2), 1)],
        (0, 3): [((0, 2), 1), ((1, 3), 1)],    # Esquina superior derecha
        (1, 0): [((0, 0), 1), ((1, 1), 1), ((2, 0), 1)],
        (1, 1): [((0, 1), 1.5), ((1, 0), 1), ((1, 2), 1), ((2, 1), 1)],
        (1, 2): [((0, 2), 1), ((1, 1), 1), ((1, 3), 1), ((2, 2), 1)],
        (1, 3): [((0, 3), 1), ((1, 2), 1), ((2, 3), 1)],
        (2, 0): [((1, 0), 1), ((2, 1), 1), ((3, 0), 1)],
        (2, 1): [((1, 1), 1), ((2, 0), 1), ((2, 2), 1), ((3, 1), 1)],
        (2, 2): [((1, 2), 1), ((2, 1), 1), ((2, 3), 1), ((3, 2), 1)],
        (2, 3): [((1, 3), 1), ((2, 2), 1), ((3, 3), 1)],
        (3, 0): [((2, 0), 1), ((3, 1), 1)],    # Esquina inferior izquierda
        (3, 1): [((2, 1), 1), ((3, 0), 1), ((3, 2), 1)],
        (3, 2): [((2, 2), 1), ((3, 1), 1), ((3, 3), 1)],
        (3, 3): [((2, 3), 1), ((3, 2), 1)]     # Esquina inferior derecha
    }
    
    inicio = (0, 0)                            # Punto de inicio
    meta = (3, 3)                              # Punto destino
    
    print("Camino con heurística Manhattan:")
    camino_manhattan = a_estrella(grafo, inicio, meta, manhattan)
    print(" -> ".join(f"({x},{y})" for x, y in camino_manhattan))
    
    print("\nCamino con heurística Euclidiana:")
    camino_euclid = a_estrella(grafo, inicio, meta, euclidiana)
    print(" -> ".join(f"({x},{y})" for x, y in camino_euclid))
    
    print("\nCamino con heurística cero (Dijkstra):")
    camino_dijkstra = a_estrella(grafo, inicio, meta, cero)
    print(" -> ".join(f"({x},{y})" for x, y in camino_dijkstra))