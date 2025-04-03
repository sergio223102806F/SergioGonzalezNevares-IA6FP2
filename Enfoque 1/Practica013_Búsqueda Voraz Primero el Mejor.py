# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 11:12:40 2025

@author: elvin
"""

import heapq                                     # Para colas de prioridad

class Nodo:                                     # Clase para nodos en el grafo
    def __init__(self, estado, padre=None):     # Constructor
        self.estado = estado                    # Identificador del nodo
        self.padre = padre                      # Nodo padre en el camino
        self.h = 0                              # Valor heurístico
        
    def __lt__(self, otro):                     # Comparador para heapq
        return self.h < otro.h                  # Ordena solo por heurística

def busqueda_voraz(grafo, inicio, meta, heuristica): # Algoritmo voraz
    abiertos = []                               # Lista de nodos por explorar
    cerrados = set()                            # Conjunto de nodos explorados
    
    nodo_inicio = Nodo(inicio)                  # Crea nodo inicial
    nodo_inicio.h = heuristica(inicio, meta)    # Calcula heurística
    heapq.heappush(abiertos, nodo_inicio)       # Añade a la cola de prioridad
    
    while abiertos:                             # Mientras haya nodos por explorar
        actual = heapq.heappop(abiertos)        # Extrae el nodo con mejor h
        cerrados.add(actual.estado)             # Marca como explorado
        
        if actual.estado == meta:               # Si llegamos a la meta
            camino = []                         # Reconstruye el camino
            while actual:
                camino.append(actual.estado)
                actual = actual.padre
            return camino[::-1]                 # Devuelve camino invertido
        
        for vecino in grafo[actual.estado]:     # Para cada vecino del nodo actual
            if vecino not in cerrados:          # Si no ha sido explorado
                nuevo_nodo = Nodo(vecino, actual) # Crea nuevo nodo
                nuevo_nodo.h = heuristica(vecino, meta) # Calcula heurística
                
                # Verifica si ya está en abiertos con mejor heurística
                en_abiertos = False
                for nodo in abiertos:
                    if nodo.estado == vecino and nodo.h <= nuevo_nodo.h:
                        en_abiertos = True
                        break
                
                if not en_abiertos:             # Si no está en abiertos o es mejor
                    heapq.heappush(abiertos, nuevo_nodo) # Añade a la cola
    
    return None                                # Si no hay camino

# --- Heurísticas de ejemplo ---
def distancia_lineal(a, b):                    # Heurística simple (ejemplo)
    return abs(ord(a) - ord(b))                 # Diferencia ASCII entre nodos

# --- Ejemplo de uso ---
if __name__ == "__main__":
    # Grafo de ejemplo (red de ciudades)
    grafo = {
        'A': ['B', 'C'],                       # A conecta con B y C
        'B': ['A', 'D', 'E'],                   # B conecta con A, D y E
        'C': ['A', 'F'],                        # C conecta con A y F
        'D': ['B', 'G'],                        # D conecta con B y G
        'E': ['B', 'G'],                        # E conecta con B y G
        'F': ['C', 'H'],                        # F conecta con C y H
        'G': ['D', 'E', 'I'],                   # G conecta con D, E e I
        'H': ['F', 'I'],                        # H conecta con F e I
        'I': ['G', 'H', 'J'],                   # I conecta con G, H y J
        'J': ['I']                              # J conecta con I
    }
    
    inicio = 'A'                                # Ciudad de origen
    meta = 'J'                                  # Ciudad destino
    
    print(f"Búsqueda Voraz de {inicio} a {meta}:")
    camino = busqueda_voraz(grafo, inicio, meta, distancia_lineal)
    
    if camino:
        print("Camino encontrado:", " -> ".join(camino))
    else:
        print("No se encontró camino válido")