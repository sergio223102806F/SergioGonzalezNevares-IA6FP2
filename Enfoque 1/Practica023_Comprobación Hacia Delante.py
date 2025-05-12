# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 13:33:01 2025

@author: elvin

Implementación de CSP con AC-3 y Backtracking para resolver Sudoku 9x9.
Incluye propagación de restricciones y heurísticas de selección de variables.
"""

from collections import deque  # Importa deque para cola eficiente

class CSP:
    def __init__(self, variables, dominios, restricciones):
        """
        Inicializa un problema CSP (Constraint Satisfaction Problem).
        
        Parámetros:
            variables:    Lista de variables del problema          (list)
            dominios:     Diccionario {variable: valores_posibles} (dict)
            restricciones: Lista de pares de variables restringidas (list)
        """
        self.variables     = variables       # Lista de variables del problema
        self.dominios      = dominios        # Dominios para cada variable
        self.restricciones = restricciones   # Restricciones entre variables
        self.vecinos       = {v: set() for v in variables}  # Grafo de vecindad
        
        for (v1, v2) in restricciones:      # Construye relación de vecindad
            self.vecinos[v1].add(v2)        # Agrega v2 como vecino de v1
            self.vecinos[v2].add(v1)        # Agrega v1 como vecino de v2

def ac3(csp, dominios=None):
    """
    Algoritmo AC-3 para propagación de restricciones arco-consistencia.
    
    Parámetros:
        csp:      Instancia del problema CSP        (CSP)
        dominios: Dominios actuales (opcional)      (dict)
    
    Retorna:
        Dominios reducidos o False si inconsistencia (dict/bool)
    """
    dominios = dominios or {v: list(csp.dominios[v]) for v in csp.variables}  # Copia dominios
    cola = deque((xi, xj) for xi in csp.variables for xj in csp.vecinos[xi])  # Todos los arcos
    
    while cola:                                # Mientras haya arcos por revisar
        xi, xj = cola.popleft()               # Extrae un arco (xi, xj)
        if revisar(xi, xj, dominios, csp):    # Si se modificó el dominio de xi
            if not dominios[xi]:               # Si dominio quedó vacío
                return False                   # Problema inconsistente
            for xk in csp.vecinos[xi]:        # Agrega arcos (xk, xi) a revisar
                if xk != xj:                  # Excepto el que ya revisamos
                    cola.append((xk, xi))
    return dominios                           # Retorna dominios consistentes

def revisar(xi, xj, dominios, csp):
    """
    Elimina valores inconsistentes de xi respecto a restricciones con xj.
    
    Parámetros:
        xi:       Variable a revisar                 (any)
        xj:       Variable vecina                    (any)
        dominios: Dominios actuales                  (dict)
        csp:      Instancia del problema CSP        (CSP)
    
    Retorna:
        True si se eliminó algún valor, False si no  (bool)
    """
    revisado = False                             # Bandera de modificación
    for x in list(dominios[xi]):                 # Para cada valor en xi
        if not any(cumple_restriccion(x, y)      # Si no hay valor en xj
                  for y in dominios[xj]):        # que cumpla restricción
            dominios[xi].remove(x)               # Elimina valor inconsistente
            revisado = True                      # Marca como modificado
    return revisado

def backtracking_ac3(asignacion, csp, dominios):
    """
    Backtracking con propagación AC-3 para CSP.
    
    Parámetros:
        asignacion: Asignación parcial actual          (dict)
        csp:        Instancia del problema CSP        (CSP)
        dominios:   Dominios actuales                 (dict)
    
    Retorna:
        Solución completa o None si no hay solución   (dict/None)
    """
    if len(asignacion) == len(csp.variables):  # Si asignación está completa
        return asignacion                      # Retorna solución
    
    var = seleccionar_variable(asignacion, dominios)  # Selecciona variable (MRV)
    
    for valor in orden_valores(var, asignacion, csp, dominios):  # Orden LCV
        if consistente(var, valor, asignacion, csp):             # Si es consistente
            asignacion[var] = valor                             # Realiza asignación
            nuevos_dominios = {v: list(dominios[v]) for v in dominios}  # Copia
            nuevos_dominios[var] = [valor]                      # Fija valor
            
            if ac3(csp, nuevos_dominios):                       # Si AC-3 exitoso
                resultado = backtracking_ac3(                   # Llamada recursiva
                    asignacion, csp, nuevos_dominios)
                if resultado is not None:                       # Si encontró solución
                    return resultado                            # Retórnala
            
            del asignacion[var]                                 # Backtrack (deshacer)
    
    return None                                                 # No hay solución

def seleccionar_variable(asignacion, dominios):
    """
    Selecciona variable no asignada usando heurística MRV.
    
    Parámetros:
        asignacion: Asignación parcial actual          (dict)
        dominios:   Dominios actuales de variables     (dict)
    
    Retorna:
        Variable no asignada con menor dominio         (any)
    """
    no_asignadas = [v for v in dominios if v not in asignacion]  # Variables libres
    return min(no_asignadas, key=lambda v: len(dominios[v]))     # Menor dominio

def orden_valores(var, asignacion, csp, dominios):
    """
    Ordena valores usando heurística LCV (Least Constraining Value).
    
    Parámetros:
        var:        Variable a ordenar valores         (any)
        asignacion: Asignación parcial actual          (dict)
        csp:        Instancia del problema CSP        (CSP)
        dominios:   Dominios actuales                 (dict)
    
    Retorna:
        Valores ordenados por menor restricción        (list)
    """
    return sorted(dominios[var],                      # Ordena valores
                key=lambda v: contar_conflictos(var, v, asignacion, csp))

def contar_conflictos(var, valor, asignacion, csp):
    """
    Cuenta conflictos potenciales para una asignación.
    
    Parámetros:
        var:        Variable a evaluar                 (any)
        valor:      Valor potencial a asignar          (any)
        asignacion: Asignación parcial actual          (dict)
        csp:        Instancia del problema CSP        (CSP)
    
    Retorna:
        Número de conflictos potenciales              (int)
    """
    return sum(1 for vecino in csp.vecinos[var]       # Cuenta vecinos
              if vecino in asignacion and              # asignados que
              not cumple_restriccion(valor, asignacion[vecino]))  # incumplen

def cumple_restriccion(valor1, valor2):
    """
    Función genérica de restricción (para Sudoku: valores diferentes).
    
    Parámetros:
        valor1: Primer valor a comparar               (any)
        valor2: Segundo valor a comparar              (any)
    
    Retorna:
        True si cumplen restricción, False si no      (bool)
    """
    return valor1 != valor2                           # Restricción básica

def consistente(var, valor, asignacion, csp):
    """
    Verifica si una asignación es consistente.
    
    Parámetros:
        var:        Variable a asignar                 (any)
        valor:      Valor a verificar                  (any)
        asignacion: Asignación parcial actual          (dict)
        csp:        Instancia del problema CSP        (CSP)
    
    Retorna:
        True si es consistente, False si no           (bool)
    """
    return all(cumple_restriccion(valor, asignacion[vecino])  # Todas las
              for vecino in csp.vecinos[var]                  # restricciones
              if vecino in asignacion)                        # deben cumplirse

def crear_sudoku_9x9():
    """
    Crea una instancia CSP para un Sudoku 9x9.
    
    Retorna:
        Problema CSP configurado para Sudoku 9x9      (CSP)
    """
    variables = [(i,j) for i in range(9) for j in range(9)]  # 81 celdas
    dominios  = {(i,j): list(range(1,10)) for i,j in variables}  # Valores 1-9
    
    restricciones = []                                # Lista de restricciones
    
    # Restricciones de filas y columnas
    for i in range(9):                                # Para cada celda
        for j in range(9):
            for k in range(9):
                if k != j: restricciones.append(((i,j), (i,k)))  # Misma fila
                if k != i: restricciones.append(((i,j), (k,j)))  # Misma columna
    
    # Restricciones de cajas 3x3
    for bi in range(0,9,3):                           # Para cada bloque 3x3
        for bj in range(0,9,3):
            caja = [(bi+i, bj+j) for i in range(3) for j in range(3)]
            for i, v1 in enumerate(caja):             # Todas combinaciones
                for v2 in caja[i+1:]:                # únicas en caja
                    restricciones.append((v1, v2))
    
    return CSP(variables, dominios, restricciones)    # Retorna CSP configurado

if __name__ == "__main__":
    # Configuración y resolución del Sudoku 9x9
    sudoku = crear_sudoku_9x9()                      # Crea instancia CSP
    
    # Asignar pistas iniciales (valores fijos)
    pistas = {                                       # Diccionario de pistas
        (0,0):5, (0,4):3, (0,8):7,                  # Valores iniciales
        (1,2):6, (2,5):9, (3,1):1,                  # para algunas celdas
        (4,4):7, (5,7):4, (6,3):5,
        (7,6):2, (8,0):3, (8,4):1
    }
    for (i,j), val in pistas.items():               # Fija valores en dominios
        sudoku.dominios[(i,j)] = [val]
    
    # Preprocesamiento con AC-3
    dominios_reducidos = ac3(sudoku)                # Reduce dominios
    
    if dominios_reducidos:                          # Si no hay inconsistencia
        print("\n" + "="*60)
        print(" PREPROCESAMIENTO AC-3 ".center(60, "="))
        print("="*60)
        print("Tamaño de dominios después de AC-3:")
        for i in range(9):                          # Muestra tamaño dominios
            print([len(dominios_reducidos[(i,j)]) for j in range(9)])
        
        # Resolver con Backtracking + AC-3
        solucion = backtracking_ac3({}, sudoku, dominios_reducidos)
        
        # Mostrar solución
        print("\n" + "="*60)
        print(" SOLUCIÓN SUDOKU 9x9 ".center(60, "="))
        print("="*60)
        if solucion:                                # Si encontró solución
            for i in range(9):                      # Imprime cada fila
                print(" ".join(str(solucion[(i,j)]) for j in range(9)))
        else:
            print("No se encontró solución")         # Mensaje de fallo
        print("="*60)
    else:
        print("El problema es inconsistente después de AC-3")  # Dominios vacíos