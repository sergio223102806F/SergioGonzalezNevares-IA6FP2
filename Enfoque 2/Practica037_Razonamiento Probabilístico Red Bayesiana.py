# -*- coding: utf-8 -*-  # Define la codificación del archivo en UTF-8 para permitir caracteres especiales

"""
Created on Wed Apr  9 14:24:39 2025  # Fecha y hora de creación del archivo

@author: elvin  # Autor del código
"""

# ============================== IMPORTACIONES ==============================

import numpy as np  # Importa NumPy para operaciones matemáticas y vectores
from collections import defaultdict  # Importa defaultdict para crear diccionarios con valores por defecto
from pgmpy.models import BayesianNetwork  # Importa la clase BayesianNetwork del módulo pgmpy
from pgmpy.factors.discrete import TabularCPD  # Importa TabularCPD para definir distribuciones condicionales
from pgmpy.inference import VariableElimination  # Importa algoritmo de inferencia basado en eliminación de variables
import networkx as nx  # Importa NetworkX para representar y visualizar grafos
import matplotlib.pyplot as plt  # Importa Matplotlib para graficar estructuras

# ============================== DEFINICIÓN DE LA CLASE ==============================

class BayesianCSP:  # Define una clase para representar un problema CSP usando una red bayesiana
    def __init__(self, variables, dominios, restricciones):  # Constructor de la clase
        self.variables = variables  # Almacena la lista de variables
        self.dominios = dominios  # Almacena el dominio de cada variable
        self.restricciones = restricciones  # Almacena las restricciones binarias entre variables

        self.vecinos = {v: set() for v in variables}  # Inicializa el diccionario de vecinos
        for (v1, v2) in restricciones:  # Itera sobre cada par de variables relacionadas por una restricción
            self.vecinos[v1].add(v2)  # Añade v2 como vecino de v1
            self.vecinos[v2].add(v1)  # Añade v1 como vecino de v2

        self.model = self.build_bayesian_network()  # Construye la red bayesiana y la guarda

    def build_bayesian_network(self):  # Función que construye la red bayesiana
        """Construye la red bayesiana para el CSP"""  # Comentario tipo docstring
        model = BayesianNetwork()  # Crea un nuevo modelo de red bayesiana

        model.add_nodes_from(self.variables)  # Añade todas las variables como nodos al modelo

        for (v1, v2) in self.restricciones:  # Itera sobre las restricciones
            model.add_edge(v1, v2)  # Añade un arco dirigido entre variables relacionadas

        cpds = []  # Lista que almacenará las CPDs
        for var in self.variables:  # Itera sobre cada variable del modelo
            if len(model.get_parents(var)) == 0:  # Si la variable no tiene padres
                cpd = TabularCPD(  # Crea una CPD uniforme
                    variable=var,  # Nombre de la variable
                    variable_card=len(self.dominios[var]),  # Número de valores posibles
                    values=[[1.0/len(self.dominios[var]) for _ in self.dominios[var]]],  # Probabilidades uniformes
                    state_names={var: list(map(str, self.dominios[var]))}  # Nombres de los estados como strings
                )
            else:  # Si la variable tiene padres
                parents = list(model.get_parents(var))  # Obtiene la lista de padres
                parent_cards = [len(self.dominios[p]) for p in parents]  # Cardinalidades de los padres

                prob_table = []  # Matriz que contendrá las probabilidades condicionales
                for val in self.dominios[var]:  # Itera sobre cada valor del dominio de la variable
                    row = []  # Inicializa fila para ese valor
                    from itertools import product  # Importa product para combinaciones cartesianas
                    for parent_vals in product(*[self.dominios[p] for p in parents]):  # Itera sobre combinaciones de valores de padres
                        satisfies = all(  # Verifica si se cumplen todas las restricciones entre padres y la variable
                            cumple_restriccion(val, parent_vals[i])  # Llama a la función de restricción
                            for i, p in enumerate(parents)  # Para cada padre
                            if (p, var) in self.restricciones or (var, p) in self.restricciones  # Solo si hay una restricción explícita
                        )
                        prob = 0.9 if satisfies else 0.1  # Asigna alta probabilidad si cumple, baja si no
                        row.append(prob)  # Añade el valor a la fila

                    row_sum = sum(row)  # Suma de la fila (para normalizar)
                    normalized_row = [p/row_sum for p in row]  # Normaliza la fila
                    prob_table.append(normalized_row)  # Añade la fila normalizada a la tabla

                cpd = TabularCPD(  # Crea una CPD condicional
                    variable=var,  # Variable objetivo
                    variable_card=len(self.dominios[var]),  # Cardinalidad
                    values=prob_table,  # Tabla de valores condicionales
                    evidence=parents,  # Lista de variables de evidencia (padres)
                    evidence_card=parent_cards,  # Cardinalidad de los padres
                    state_names={var: list(map(str, self.dominios[var]))} |  # Estados de la variable
                                {p: list(map(str, self.dominios[p])) for p in parents}  # Estados de los padres
                )
            cpds.append(cpd)  # Añade la CPD a la lista

        model.add_cpds(*cpds)  # Añade todas las CPDs al modelo

        assert model.check_model(), "La red bayesiana no es válida"  # Verifica que el modelo sea válido

        return model  # Retorna el modelo construido

    def solve(self, evidence=None):  # Método para resolver el CSP usando inferencia
        """Resuelve el CSP usando inferencia probabilística"""  # Docstring explicativo
        if evidence is None:  # Si no se proporciona evidencia
            evidence = {}  # Se inicializa como diccionario vacío

        formatted_evidence = {k: str(v) for k, v in evidence.items()}  # Convierte valores a string para pgmpy

        infer = VariableElimination(self.model)  # Crea objeto de inferencia

        solution = {}  # Diccionario para guardar la solución
        for var in self.variables:  # Para cada variable del CSP
            if var in evidence:  # Si ya está en la evidencia
                solution[var] = evidence[var]  # Asigna directamente su valor
            else:
                posterior = infer.query(variables=[var], evidence=formatted_evidence)  # Calcula la distribución posterior
                solution[var] = int(posterior.state_names[var][np.argmax(posterior.values)])  # Toma el valor más probable

        return solution  # Retorna la solución completa

    def visualize_network(self):  # Método para visualizar la estructura de la red bayesiana
        """Visualiza la estructura de la red bayesiana"""  # Docstring explicativo
        nx.draw(self.model, with_labels=True, node_size=2000, node_color='skyblue',
                font_size=10, font_weight='bold', arrowsize=20)  # Dibuja el grafo
        plt.title("Red Bayesiana del CSP")  # Título de la figura
        plt.show()  # Muestra la visualización

# ============================== FUNCIÓN DE RESTRICCIÓN ==============================

def cumple_restriccion(valor1, valor2):  # Define si dos valores satisfacen la restricción del CSP
    """Función de restricción para el sudoku (valores diferentes)"""  # Docstring
    return valor1 != valor2  # Retorna True si los valores son distintos

# ============================== CREACIÓN DEL SUDOKU ==============================

def crear_sudoku_4x4():  # Función que construye un CSP para un sudoku 4x4
    variables = [(i, j) for i in range(4) for j in range(4)]  # Crea todas las posiciones del tablero
    dominios = {(i, j): list(range(1, 5)) for i, j in variables}  # Asigna dominio [1,2,3,4] a cada celda

    restricciones = []  # Lista de restricciones
    for i in range(4):  # Recorre filas
        for j in range(4):  # Recorre columnas
            for k in range(4):  # Otro índice para comparación
                if k != j:
                    restricciones.append(((i, j), (i, k)))  # Restricción fila
                if k != i:
                    restricciones.append(((i, j), (k, j)))  # Restricción columna

    for bi in [0, 2]:  # Índices de bloques 2x2 en filas
        for bj in [0, 2]:  # Índices de bloques 2x2 en columnas
            caja = [(bi+i, bj+j) for i in range(2) for j in range(2)]  # Crea lista de posiciones de la caja
            for i, v1 in enumerate(caja):  # Recorre cada par de celdas en la caja
                for v2 in caja[i+1:]:
                    restricciones.append((v1, v2))  # Añade restricción entre celdas de la misma caja

    return BayesianCSP(variables, dominios, restricciones)  # Retorna la instancia del CSP

# ============================== PROGRAMA PRINCIPAL ==============================

if __name__ == "__main__":  # Punto de entrada del programa
    sudoku = crear_sudoku_4x4()  # Crea el modelo CSP para el sudoku

    # sudoku.visualize_network()  # Línea comentada para visualizar la red (opcional)

    pistas = {(0,0):1, (0,2):3, (1,1):4, (3,3):2}  # Evidencia inicial (pistas del sudoku)

    solucion = sudoku.solve(evidence=pistas)  # Resuelve el sudoku usando inferencia

    print("Solución encontrada:")  # Muestra la solución obtenida
    for i in range(4):  # Imprime cada fila del tablero
        print([solucion.get((i,j), 0) for j in range(4)])

    conflictos = 0  # Contador de restricciones violadas
    for (v1, v2) in sudoku.restricciones:  # Verifica cada restricción
        if not cumple_restriccion(solucion[v1], solucion[v2]):
            conflictos += 1  # Incrementa si hay conflicto

    print("\nRestricciones violadas:", conflictos)  # Muestra cantidad de conflictos
    print("Tasa de satisfacción: {:.1f}%".format(  # Calcula porcentaje de satisfacción
        (1 - conflictos/len(sudoku.restricciones)) * 100))

    infer = VariableElimination(sudoku.model)  # Crea objeto para inferencia posterior
    posterior = infer.query(variables=[(1,0)], evidence={k: str(v) for k, v in pistas.items()})  # Consulta distribución para celda (1,0)

    print("\nDistribución posterior para celda (1,0):")  # Muestra distribución
    for val, prob in zip(posterior.state_names[(1,0)], posterior.values):  # Recorre los valores y probabilidades
        print(f"Valor {val}: {prob:.3f}")  # Imprime cada valor con su probabilidad
