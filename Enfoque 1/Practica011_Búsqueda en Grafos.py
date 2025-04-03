# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 11:10:48 2025

@author: elvin
"""

from collections import deque, defaultdict       # Estructuras de datos eficientes

class Grafo:                                    # Clase para representar un grafo
    def __init__(self, dirigido=False):         # Constructor con parámetro dirigido
        self.grafo = defaultdict(list)          # Diccionario de listas de adyacencia
        self.dirigido = dirigido                # Bool: grafo dirigido o no

    def agregar_arista(self, u, v, peso=1):     # Añade arista con peso opcional
        self.grafo[u].append((v, peso))         # Añade arista u -> v
        if not self.dirigido:                   # Si no es dirigido
            self.grafo[v].append((u, peso))     # Añade arista v -> u

    def bfs(self, inicio, meta=None):           # Búsqueda en Anchura
        visitados = set()                       # Conjunto de nodos visitados
        cola = deque([(inicio, [inicio])])      # Cola de tuplas (nodo, camino)
        while cola:
            nodo, camino = cola.popleft()       # Extrae el primer elemento
            if nodo == meta:                    # Si encontramos la meta
                return camino                   # Retorna el camino
            if nodo not in visitados:
                visitados.add(nodo)             # Marca como visitado
                for vecino, _ in self.grafo[nodo]: # Explora vecinos
                    if vecino not in visitados:
                        cola.append((vecino, camino + [vecino])) # Añade a cola
        return list(visitados) if meta is None else None # Retorna todos visitados o None

    def dfs(self, inicio, meta=None, iterativo=True): # Búsqueda en Profundidad
        if iterativo:                           # Versión iterativa (por defecto)
            return self._dfs_iterativo(inicio, meta)
        else:
            return self._dfs_recursivo(inicio, meta, set(), [])

    def _dfs_iterativo(self, inicio, meta):     # DFS iterativo
        pila = [(inicio, [inicio])]            # Pila de tuplas (nodo, camino)
        visitados = set()                       # Conjunto de nodos visitados
        while pila:
            nodo, camino = pila.pop()          # Extrae último elemento
            if nodo == meta:                    # Si encontramos la meta
                return camino                   # Retorna el camino
            if nodo not in visitados:
                visitados.add(nodo)             # Marca como visitado
                for vecino, _ in reversed(self.grafo[nodo]): # Vecinos en orden inverso
                    if vecino not in visitados:
                        pila.append((vecino, camino + [vecino])) # Añade a pila
        return list(visitados) if meta is None else None # Retorna todos visitados o None

    def _dfs_recursivo(self, nodo, meta, visitados, camino): # DFS recursivo
        visitados.add(nodo)                     # Marca nodo como visitado
        camino.append(nodo)                     # Añade al camino actual
        if nodo == meta:                        # Si encontramos la meta
            return camino.copy()                # Retorna copia del camino
        for vecino, _ in self.grafo[nodo]:      # Explora vecinos
            if vecino not in visitados:         # Si no ha sido visitado
                resultado = self._dfs_recursivo(vecino, meta, visitados, camino)
                if resultado is not None:       # Si encontró solución
                    return resultado            # Retórnala
                camino.pop()                    # Retrocede (backtracking)
        return None                             # No encontró solución

    def mostrar_grafo(self):                    # Muestra la estructura del grafo
        for nodo in self.grafo:
            print(f"{nodo}: {self.grafo[nodo]}")

# --- Ejemplo de uso ---
if __name__ == "__main__":
    # Crea grafo no dirigido (ejemplo laberinto)
    g = Grafo(dirigido=False)
    g.agregar_arista('A', 'B')
    g.agregar_arista('A', 'C')
    g.agregar_arista('B', 'D')
    g.agregar_arista('C', 'E')
    g.agregar_arista('D', 'F')
    g.agregar_arista('E', 'F')
    g.agregar_arista('F', 'G')

    print("Estructura del grafo:")
    g.mostrar_grafo()

    inicio = 'A'
    meta = 'G'

    # Prueba BFS
    print(f"\nBFS de {inicio} a {meta}:")
    camino_bfs = g.bfs(inicio, meta)
    print(" -> ".join(camino_bfs) if camino_bfs else "No encontrado")

    # Prueba DFS iterativo
    print(f"\nDFS iterativo de {inicio} a {meta}:")
    camino_dfs_iter = g.dfs(inicio, meta, iterativo=True)
    print(" -> ".join(camino_dfs_iter) if camino_dfs_iter else "No encontrado")

    # Prueba DFS recursivo
    print(f"\nDFS recursivo de {inicio} a {meta}:")
    camino_dfs_rec = g.dfs(inicio, meta, iterativo=False)
    print(" -> ".join(camino_dfs_rec) if camino_dfs_rec else "No encontrado")