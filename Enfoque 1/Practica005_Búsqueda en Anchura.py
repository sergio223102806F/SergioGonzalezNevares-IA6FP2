# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 10:41:27 2025

@author: elvin
"""

from collections import deque                     # Importa deque para colas eficientes

class Grafo:                                     # Clase para representar un grafo
    def __init__(self):                          # Constructor
        self.adyacencia = {}                     # Diccionario de adyacencia {nodo: [vecinos]}

    def agregar_arista(self, u, v):              # Añade arista entre nodos u y v
        if u not in self.adyacencia:             # Si u no existe en el grafo
            self.adyacencia[u] = []              # Crea lista de adyacencia para u
        if v not in self.adyacencia:             # Si v no existe en el grafo
            self.adyacencia[v] = []              # Crea lista de adyacencia para v
        self.adyacencia[u].append(v)             # Añade v como vecino de u
        self.adyacencia[v].append(u)             # Grafo no dirigido: añade u como vecino de v

    def bfs(self, inicio):                       # Algoritmo Búsqueda en Anchura
        visitados = set()                        # Conjunto para nodos visitados
        cola = deque([inicio])                   # Cola para nodos por visitar
        recorrido = []                           # Lista para almacenar el orden de visita

        while cola:                              # Mientras haya nodos en la cola
            nodo = cola.popleft()               # Extrae el primer nodo (FIFO)
            if nodo not in visitados:            # Si no ha sido visitado
                visitados.add(nodo)              # Márcalo como visitado
                recorrido.append(nodo)          # Añádelo al recorrido
                for vecino in self.adyacencia.get(nodo, []):  # Para cada vecino
                    if vecino not in visitados:  # Si no ha sido visitado
                        cola.append(vecino)      # Añádelo a la cola
        return recorrido                        # Devuelve el recorrido completo

# --- Ejemplo de uso ---
if __name__ == "__main__":
    g = Grafo()                                 # Crea un grafo no dirigido
    
    # Construye el grafo de ejemplo
    g.agregar_arista('A', 'B')                  # Añade arista A-B
    g.agregar_arista('A', 'C')                  # Añade arista A-C
    g.agregar_arista('B', 'D')                  # Añade arista B-D
    g.agregar_arista('C', 'E')                  # Añade arista C-E
    g.agregar_arista('D', 'E')                  # Añade arista D-E
    
    print("Recorrido BFS desde 'A':",            # Ejecuta BFS desde el nodo A
          g.bfs('A'))