# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 10:48:51 2025

@author: elvin
"""

import heapq                                     # Para la cola de prioridad

class Grafo:                                    # Clase para representar un grafo ponderado
    def __init__(self):                         # Constructor
        self.adyacencia = {}                    # Diccionario: {nodo: [(vecino, costo)]}

    def agregar_arista(self, u, v, costo=1):    # Añade arista con costo opcional
        if u not in self.adyacencia:            # Si el nodo u no existe
            self.adyacencia[u] = []             # Inicializa su lista de adyacencia
        if v not in self.adyacencia:            # Si el nodo v no existe
            self.adyacencia[v] = []             # Inicializa su lista de adyacencia
        self.adyacencia[u].append((v, costo))   # Añade arista dirigida u->v con costo
        self.adyacencia[v].append((u, costo))   # Para grafo no dirigido (comentar si es dirigido)

    def ucs(self, inicio, meta):                # Algoritmo de Costo Uniforme
        cola = [(0, inicio, [])]                # Cola de prioridad: (costo_acumulado, nodo, camino)
        visitados = set()                       # Conjunto para nodos visitados

        while cola:                             # Mientras haya nodos por explorar
            costo, nodo, camino = heapq.heappop(cola)  # Extrae el nodo con menor costo
            if nodo == meta:                     # Si llegamos a la meta
                return camino + [nodo], costo    # Devuelve camino y costo total

            if nodo not in visitados:            # Si no ha sido visitado
                visitados.add(nodo)              # Márcalo como visitado
                for vecino, costo_arista in self.adyacencia.get(nodo, []):
                    if vecino not in visitados:  # Para cada vecino no visitado
                        heapq.heappush(cola, (costo + costo_arista,  # Añade a la cola con
                                             vecino,                 # nuevo costo acumulado
                                             camino + [nodo]))       # y actualiza camino

        return None, float('inf')               # Si no hay camino, devuelve infinito

# --- Ejemplo de uso ---
if __name__ == "__main__":
    g = Grafo()                                 # Crea grafo ponderado
    
    # Construye grafo de ejemplo (red de ciudades)
    g.agregar_arista('A', 'B', 4)               # A-B con costo 4
    g.agregar_arista('A', 'C', 2)               # A-C con costo 2
    g.agregar_arista('B', 'D', 5)               # B-D con costo 5
    g.agregar_arista('C', 'D', 8)               # C-D con costo 8
    g.agregar_arista('C', 'E', 3)               # C-E con costo 3
    g.agregar_arista('D', 'E', 1)               # D-E con costo 1
    g.agregar_arista('D', 'F', 6)               # D-F con costo 6
    g.agregar_arista('E', 'F', 7)               # E-F con costo 7

    inicio = 'A'                                # Ciudad de origen
    meta = 'F'                                  # Ciudad destino

    camino, costo_total = g.ucs(inicio, meta)    # Ejecuta UCS

    if camino:                                   # Si encontró camino
        print(f"Camino óptimo de {inicio} a {meta}: {' -> '.join(camino)}")
        print(f"Costo total: {costo_total}")
    else:
        print("No se encontró camino válido")