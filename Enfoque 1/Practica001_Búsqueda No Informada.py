# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 09:54:51 2025

@author: elvin
"""

from collections import deque          # Importa deque para operaciones eficientes

class Grafo:                          # Clase para representar un grafo no dirigido
    def __init__(self):               # Constructor que inicializa el grafo
        self.grafo = {}               # Diccionario: {nodo: [vecinos]}
    
    def agregar_nodo(self, nodo):     # Método para añadir un nodo al grafo
        if nodo not in self.grafo:    # Verifica si el nodo no existe
            self.grafo[nodo] = []     # Inicializa lista de vecinos vacía
    
    def agregar_arista(self, nodo1,   # Método para añadir arista entre nodos
                       nodo2):        
        self.agregar_nodo(nodo1)      # Asegura que nodo1 exista
        self.agregar_nodo(nodo2)      # Asegura que nodo2 exista
        self.grafo[nodo1].append(nodo2)# Añade nodo2 como vecino de nodo1
        self.grafo[nodo2].append(nodo1)# Añade nodo1 como vecino de nodo2 (no dirigido)

    def dfs(self, inicio):            # Búsqueda en Profundidad (iterativa)
        visitados = set()             # Conjunto para nodos visitados
        pila = [inicio]              # Pila para nodos por explorar (LIFO)
        recorrido = []                # Lista para almacenar el orden
        
        while pila:                   # Mientras haya nodos en la pila
            nodo = pila.pop()         # Extrae el último nodo añadido
            if nodo not in visitados:  # Procesa si no está visitado
                visitados.add(nodo)    # Marca como visitado
                recorrido.append(nodo)# Añade al recorrido
                for vecino in reversed(# Añade vecinos en orden inverso
                    self.grafo.get(nodo, [])):
                    if vecino not in visitados:
                        pila.append(vecino)
        return recorrido              # Devuelve el orden de recorrido

    def bfs(self, inicio):            # Búsqueda en Anchura (iterativa)
        visitados = set()             # Conjunto para nodos visitados
        cola = deque([inicio])       # Cola para nodos por explorar (FIFO)
        recorrido = []                # Lista para almacenar el orden
        
        while cola:                   # Mientras haya nodos en la cola
            nodo = cola.popleft()     # Extrae el primer nodo añadido
            if nodo not in visitados:  # Procesa si no está visitado
                visitados.add(nodo)    # Marca como visitado
                recorrido.append(nodo)# Añade al recorrido
                for vecino in self.grafo.get(nodo, []):
                    if vecino not in visitados:
                        cola.append(vecino)
        return recorrido              # Devuelve el orden de recorrido

if __name__ == "__main__":            # Bloque principal de ejecución
    g = Grafo()                       # Crea instancia del grafo
    
    # Construye el grafo de ejemplo
    g.agregar_arista("A", "B")        # Conexión A-B
    g.agregar_arista("A", "C")        # Conexión A-C
    g.agregar_arista("B", "D")        # Conexión B-D
    g.agregar_arista("C", "E")        # Conexión C-E
    g.agregar_arista("D", "E")        # Conexión D-E
    
    print("Grafo:", g.grafo)           # Muestra la estructura del grafo
    print("\nDFS desde 'A':",          # Muestra DFS desde A
          g.dfs("A"))                 
    print("BFS desde 'A':",            # Muestra BFS desde A
          g.bfs("A"))                 