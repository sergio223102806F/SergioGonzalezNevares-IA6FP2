# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 13:33:01 2025

@author: elvin

Implementación de Backjumping (salto atrás dirigido por conflictos) para CSP.
Algoritmo que mejora el backtracking tradicional evitando explorar ramas conflictivas.
"""

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

def backjumping(asignacion, csp, nivel=0, conflictos=None):
    """
    Algoritmo de Backjumping con seguimiento de conflictos.
    
    Parámetros:
        asignacion: Asignación parcial actual          (dict)
        csp:        Instancia del problema CSP        (CSP)
        nivel:      Profundidad actual en la búsqueda (int)
        conflictos: Diccionario de conflictos         (dict)
    
    Retorna:
        Solución completa o None si no hay solución   (dict/None)
    """
    if len(asignacion) == len(csp.variables):  # Si asignación está completa
        return asignacion                      # Retorna solución
    
    conflictos = conflictos or {v: set() for v in csp.variables}  # Inicializa
    var = seleccionar_variable(asignacion, csp)                   # Selecciona var
    
    for valor in orden_valores(var, asignacion, csp):              # Orden LCV
        if consistente(var, valor, asignacion, csp):               # Si es consistente
            asignacion[var] = valor                               # Realiza asignación
            resultado = backjumping(                              # Llamada recursiva
                asignacion, csp, nivel+1, conflictos)
            if resultado is not None:                             # Si encontró solución
                return resultado                                  # Retórnala
            del asignacion[var]                                   # Backtrack (deshacer)
        else:
            # Registrar conflictos con variables asignadas
            for vecino in csp.vecinos[var]:                       # Para cada vecino
                if vecino in asignacion:                          # Si está asignado
                    conflictos[var].add(nivel_dict[vecino])       # Agrega nivel conflicto
    
    # Determinar nivel de salto (máximo nivel de conflicto)
    if conflictos[var]:                                           # Si hay conflictos
        nivel_salto = max(conflictos[var])                        # Nivel máximo
        # Propagación de conflictos a variables anteriores
        for v in conflictos:                                      # Para cada variable
            if nivel_dict[v] < nivel_dict[var]:                   # Si es anterior
                conflictos[v].update(conflictos[var])             # Propaga conflictos
        return backjumping(asignacion, csp, nivel_salto, conflictos)  # Salta
    else:
        return None                                               # No hay solución

def seleccionar_variable(asignacion, csp):
    """
    Selecciona variable no asignada usando heurística MRV.
    
    Parámetros:
        asignacion: Asignación parcial actual          (dict)
        csp:        Instancia del problema CSP        (CSP)
    
    Retorna:
        Variable no asignada con menor dominio        (any)
    """
    no_asignadas = [v for v in csp.variables if v not in asignacion]  # Variables libres
    return min(no_asignadas, key=lambda v: len(csp.dominios[v]))      # Menor dominio

def orden_valores(var, asignacion, csp):
    """
    Ordena valores usando heurística LCV (Least Constraining Value).
    
    Parámetros:
        var:        Variable a ordenar valores         (any)
        asignacion: Asignación parcial actual          (dict)
        csp:        Instancia del problema CSP        (CSP)
    
    Retorna:
        Valores ordenados por menor restricción        (list)
    """
    return sorted(csp.dominios[var],                  # Ordena valores
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

# Mapeo de variables a niveles (para seguimiento de conflictos)
nivel_dict = {}                                      # Diccionario global

def crear_sudoku_4x4():
    """
    Crea una instancia CSP para un Sudoku 4x4.
    
    Retorna:
        Problema CSP configurado para Sudoku 4x4      (CSP)
    """
    variables = [(i,j) for i in range(4) for j in range(4)]  # 16 celdas
    dominios  = {(i,j): list(range(1,5)) for i,j in variables}  # Valores 1-4
    
    restricciones = []                                # Lista de restricciones
    
    # Restricciones de filas y columnas
    for i in range(4):                                # Para cada celda
        for j in range(4):
            nivel_dict[(i,j)] = i*4 + j               # Asigna nivel único
            for k in range(4):
                if k != j: restricciones.append(((i,j), (i,k)))  # Misma fila
                if k != i: restricciones.append(((i,j), (k,j)))  # Misma columna
    
    # Restricciones de cajas 2x2
    for bi in [0,2]:                                 # Para cada bloque 2x2
        for bj in [0,2]:
            caja = [(bi+i, bj+j) for i in range(2) for j in range(2)]
            for i, v1 in enumerate(caja):            # Todas combinaciones
                for v2 in caja[i+1:]:                # únicas en caja
                    restricciones.append((v1, v2))
    
    return CSP(variables, dominios, restricciones)   # Retorna CSP configurado

if __name__ == "__main__":
    # Configuración y resolución del Sudoku 4x4
    sudoku = crear_sudoku_4x4()                     # Crea instancia CSP
    
    # Asignar pistas iniciales (valores fijos)
    pistas = {                                      # Diccionario de pistas
        (0,0):1, (0,2):3,                          # Valores iniciales
        (1,1):4, (3,3):2                           # para algunas celdas
    }
    for (i,j), val in pistas.items():              # Fija valores en dominios
        sudoku.dominios[(i,j)] = [val]
    
    # Resolver con Backjumping
    solucion = backjumping({}, sudoku)             # Ejecuta algoritmo
    
    # Mostrar solución
    print("\n" + "="*40)
    print(" SOLUCIÓN SUDOKU 4x4 ".center(40, "="))
    print("="*40)
    if solucion:                                   # Si encontró solución
        for i in range(4):                        # Imprime cada fila
            print([solucion[(i,j)] for j in range(4)])
    else:
        print("No se encontró solución")           # Mensaje de fallo
    print("="*40)