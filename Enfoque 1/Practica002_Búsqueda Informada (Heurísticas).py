# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 10:31:43 2025

@author: elvin
"""

import heapq                                     # Para usar colas de prioridad

class Nodo:                                     # Clase para nodos en el grafo
    def __init__(self, estado, padre=None):     # Constructor del nodo
        self.estado = estado                    # Identificador del nodo (ej: coordenadas)
        self.padre = padre                      # Nodo padre en el camino
        self.g = 0                              # Costo acumulado desde inicio
        self.h = 0                              # Heurística (estimado a meta)
        self.f = 0                              # Costo total (g + h)
    
    def __lt__(self, otro):                     # Comparador para heapq
        return self.f < otro.f                  # Ordena por costo total (f)

def a_estrella(grafo, inicio, meta, heuristica):# Algoritmo A*
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
        
        for vecino in grafo[actual.estado]:     # Para cada vecino del nodo actual
            if vecino in cerrados:              # Si ya fue explorado, lo salta
                continue
            
            nuevo_g = actual.g + 1              # Costo acumulado (aquí: 1 por paso)
            nuevo_nodo = Nodo(vecino, actual)   # Crea nodo vecino
            nuevo_nodo.g = nuevo_g
            nuevo_nodo.h = heuristica(vecino, meta)
            nuevo_nodo.f = nuevo_nodo.g + nuevo_nodo.h
            
            if any(nodo.estado == vecino and    # Si ya está en abiertos con mejor g
                   nodo.f <= nuevo_nodo.f 
                   for nodo in abiertos):
                continue
            
            heapq.heappush(abiertos, nuevo_nodo)# Añade vecino a la cola
    
    return None                                # Si no hay camino

# Ejemplo de heurística (distancia Manhattan para grid)
def heuristica_manhattan(a, b):                # Para coordenadas (x,y)
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

if __name__ == "__main__":                     # Ejemplo de uso
    # Grafo representado como diccionario (grid 3x3)
    grafo = {
        (0, 0): [(0, 1), (1, 0)],              # Esquinas
        (0, 1): [(0, 0), (0, 2), (1, 1)],
        (0, 2): [(0, 1), (1, 2)],
        (1, 0): [(0, 0), (1, 1), (2, 0)],
        (1, 1): [(0, 1), (1, 0), (1, 2), (2, 1)],
        (1, 2): [(0, 2), (1, 1), (2, 2)],
        (2, 0): [(1, 0), (2, 1)],
        (2, 1): [(1, 1), (2, 0), (2, 2)],
        (2, 2): [(1, 2), (2, 1)]
    }
    
    inicio = (0, 0)                            # Punto de inicio
    meta = (2, 2)                              # Punto de destino
    
    camino = a_estrella(grafo, inicio, meta,    # Ejecuta A*
                        heuristica_manhattan)
    print("Camino encontrado:", camino)         # Muestra resultado