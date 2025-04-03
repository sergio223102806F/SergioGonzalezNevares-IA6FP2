# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 10:48:51 2025

@author: elvin
"""

class Grafo:                                    # Clase para representar un grafo
    def __init__(self):                         # Constructor
        self.grafo = {}                         # Diccionario: {nodo: [vecinos]}

    def agregar_arista(self, u, v):             # Añade arista entre nodos
        if u not in self.grafo:                 # Si el nodo u no existe
            self.grafo[u] = []                  # Crea lista de adyacencia
        if v not in self.grafo:                 # Si el nodo v no existe
            self.grafo[v] = []                  # Crea lista de adyacencia
        self.grafo[u].append(v)                 # Añade v como vecino de u
        self.grafo[v].append(u)                 # Grafo no dirigido (bidireccional)

    def dfs(self, inicio, visitados=None):      # DFS recursivo
        if visitados is None:                   # Inicializa conjunto visitados
            visitados = set()                   # en primera llamada
        visitados.add(inicio)                   # Marca nodo como visitado
        recorrido = [inicio]                    # Inicia recorrido
        
        for vecino in self.grafo.get(inicio, []): # Explora vecinos
            if vecino not in visitados:         # Si no ha sido visitado
                recorrido += self.dfs(vecino,   # Llama recursivamente
                                     visitados) # manteniendo visitados
        return recorrido                        # Devuelve recorrido completo

    def dfs_iterativo(self, inicio):            # DFS versión iterativa
        visitados = set()                       # Conjunto de nodos visitados
        pila = [inicio]                        # Pila para nodos por visitar
        recorrido = []                          # Almacena orden de visita
        
        while pila:                             # Mientras haya nodos en pila
            nodo = pila.pop()                   # Extrae último nodo (LIFO)
            if nodo not in visitados:           # Si no ha sido visitado
                visitados.add(nodo)             # Márcalo como visitado
                recorrido.append(nodo)          # Añádelo al recorrido
                # Añade vecinos en orden inverso para mantener orden natural
                for vecino in reversed(self.grafo.get(nodo, [])):
                    if vecino not in visitados: # Si no ha sido visitado
                        pila.append(vecino)     # Añádelo a la pila
        return recorrido                        # Devuelve recorrido completo

# --- Ejemplo de uso ---
if __name__ == "__main__":
    g = Grafo()                                # Crea grafo no dirigido
    
    # Construye grafo de ejemplo (árbol)
    g.agregar_arista('A', 'B')                 # Añade arista A-B
    g.agregar_arista('A', 'C')                 # Añade arista A-C
    g.agregar_arista('B', 'D')                 # Añade arista B-D
    g.agregar_arista('B', 'E')                 # Añade arista B-E
    g.agregar_arista('C', 'F')                 # Añade arista C-F
    
    print("Recorrido DFS recursivo desde 'A':", # DFS recursivo
          g.dfs('A'))
    
    print("Recorrido DFS iterativo desde 'A':", # DFS iterativo
          g.dfs_iterativo('A'))