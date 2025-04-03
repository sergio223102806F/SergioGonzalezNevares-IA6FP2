# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 09:51:42 2025

@author: elvin
"""

# Importa la clase TopologicalSorter y la excepción CycleError del módulo graphlib
from graphlib import TopologicalSorter, CycleError

# Función principal que encapsula toda la lógica del programa
def main():
    # --- Definición del grafo de ejemplo ---
    # Diccionario donde las llaves son nodos y los valores son sus dependencias
    # Representa un grafo dirigido acíclico (DAG)
    graph = {
        "B": {"A"},  # El nodo B depende del nodo A
        "C": {"A"},  # El nodo C depende del nodo A
        "D": {"B", "C"},  # El nodo D depende de B y C
    }

    # Crea una instancia de TopologicalSorter con el grafo definido
    ts = TopologicalSorter(graph)

    # --- Agregar nodos dinámicamente ---
    # Añade el nodo E sin dependencias
    ts.add("E")
    # Establece que el nodo D ahora también depende de E
    ts.add("D", "E")  # D -> E

    # Bloque try-except para manejar posibles ciclos en el grafo
    try:
        # --- Ordenamiento topológico (versión simple) ---
        # static_order() devuelve un iterable con el orden topológico
        print("Orden topológico (static_order):", tuple(ts.static_order()))

        # --- Procesamiento paso a paso (para paralelismo) ---
        print("\nProcesamiento paso a paso:")
        # Prepara el grafo para el procesamiento (verifica ciclos)
        ts.prepare()  # Bloquea el grafo para modificaciones

        # Mientras haya nodos por procesar
        while ts.is_active():
            # Obtiene los nodos listos para procesar (sin dependencias pendientes)
            ready_nodes = ts.get_ready()
            print("Nodos listos para procesar:", ready_nodes)
            # Simula el procesamiento de los nodos (en un caso real, se enviarían a workers)
            ts.done(*ready_nodes)

    # Captura la excepción si se detecta un ciclo en el grafo
    except CycleError as e:
        # e.args[1] contiene la lista de nodos que forman el ciclo
        print(f"¡Error! Hay un ciclo: {e.args[1]}")

# Punto de entrada del programa
if __name__ == "__main__":
    # Llama a la función principal
    main()