# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 10:48:51 2025

@author: elvin
"""

from collections import deque                     # Importa deque para colas eficientes

class Grafo:                                     # Clase para representar un grafo
    def __init__(self):                          # Constructor
        self.grafo = {}                          # Diccionario: {nodo: [vecinos]}

    def agregar_arista(self, u, v):              # Añade arista entre nodos
        if u not in self.grafo:                 # Si el nodo u no existe
            self.grafo[u] = []                   # Crea lista de adyacencia
        if v not in self.grafo:                 # Si el nodo v no existe
            self.grafo[v] = []                   # Crea lista de adyacencia
        self.grafo[u].append(v)                  # Añade v como vecino de u
        self.grafo[v].append(u)                  # Grafo no dirigido (bidireccional)

    def busqueda_bidireccional(self, inicio, meta): # Algoritmo bidireccional
        if inicio == meta:                       # Caso trivial: inicio es meta
            return [inicio]

        # Estructuras para búsqueda desde inicio
        cola_inicio = deque([inicio])           # Cola para BFS desde inicio
        visitado_inicio = {inicio: None}        # Diccionario {nodo: padre}

        # Estructuras para búsqueda desde meta
        cola_meta = deque([meta])               # Cola para BFS desde meta
        visitado_meta = {meta: None}            # Diccionario {nodo: padre}

        intersect_node = None                   # Nodo de intersección

        while cola_inicio and cola_meta:        # Mientras ambas colas tengan nodos
            # BFS desde inicio
            nodo_actual = cola_inicio.popleft() # Extrae primer nodo
            for vecino in self.grafo.get(nodo_actual, []):
                if vecino not in visitado_inicio:
                    visitado_inicio[vecino] = nodo_actual
                    cola_inicio.append(vecino)
                    if vecino in visitado_meta:  # Si hay intersección
                        intersect_node = vecino
                        break

            # BFS desde meta
            nodo_actual = cola_meta.popleft()   # Extrae primer nodo
            for vecino in self.grafo.get(nodo_actual, []):
                if vecino not in visitado_meta:
                    visitado_meta[vecino] = nodo_actual
                    cola_meta.append(vecino)
                    if vecino in visitado_inicio: # Si hay intersección
                        intersect_node = vecino
                        break

            if intersect_node is not None:      # Si encontró intersección
                break                          # Termina búsqueda

        # Reconstruye camino si hay intersección
        if intersect_node is None:              # Si no hay camino
            return None

        # Reconstruye camino desde inicio hasta intersección
        camino = []
        nodo = intersect_node
        while nodo is not None:
            camino.append(nodo)
            nodo = visitado_inicio[nodo]
        camino = camino[::-1]                   # Invierte el camino

        # Reconstruye camino desde intersección hasta meta
        nodo = visitado_meta[intersect_node]
        while nodo is not None:
            camino.append(nodo)
            nodo = visitado_meta[nodo]

        return camino                           # Devuelve camino completo

# --- Ejemplo de uso ---
if __name__ == "__main__":
    g = Grafo()                                 # Crea grafo no dirigido
    
    # Construye grafo de ejemplo (laberinto)
    g.agregar_arista('A', 'B')                  # Añade arista A-B
    g.agregar_arista('A', 'C')                  # Añade arista A-C
    g.agregar_arista('B', 'D')                  # Añade arista B-D
    g.agregar_arista('C', 'E')                  # Añade arista C-E
    g.agregar_arista('D', 'F')                  # Añade arista D-F
    g.agregar_arista('E', 'F')                  # Añade arista E-F
    g.agregar_arista('F', 'G')                  # Añade arista F-G
    
    inicio = 'A'                                # Nodo inicial
    meta = 'G'                                  # Nodo objetivo
    
    print(f"Búsqueda bidireccional de {inicio} a {meta}:")
    camino = g.busqueda_bidireccional(inicio, meta)
    
    if camino:                                   # Si encontró solución
        print("Camino encontrado:", " -> ".join(camino))
    else:
        print("No se encontró camino válido")