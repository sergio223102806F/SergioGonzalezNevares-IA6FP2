# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 13:28:16 2025

@author: elvin
"""

class CSP:
    def __init__(self, variables, dominios, restricciones):
        self.variables = variables      # Lista de variables del problema
        self.dominios = dominios        # Diccionario {variable: [valores_posibles]}
        self.restricciones = restricciones  # Lista de pares (var1, var2) con restricciones
        self.vecinos = {v: set() for v in variables}
        for (v1, v2) in restricciones:  # Estructura para acceder rápido a vecinos
            self.vecinos[v1].add(v2)
            self.vecinos[v2].add(v1)

def backtracking(asignacion, csp):
    """Algoritmo de vuelta atrás recursivo"""
    # Si todas las variables están asignadas, retornar solución
    if len(asignacion) == len(csp.variables):
        return asignacion.copy()  # Copia para evitar modificaciones
    
    # Seleccionar variable no asignada (heurística: MRV - Mínimos Valores Restantes)
    var = min([v for v in csp.variables if v not in asignacion],
              key=lambda v: len(csp.dominios[v]))
    
    # Probar valores en orden (heurística: LCV - Valores Menos Restrictivos primero)
    for valor in sorted(csp.dominios[var],
                       key=lambda v: contar_conflictos(var, v, asignacion, csp)):
        
        # Verificar consistencia con asignación actual
        if consistente(var, valor, asignacion, csp):
            asignacion[var] = valor  # Hacer asignación
            
            # Llamada recursiva
            resultado = backtracking(asignacion, csp)
            if resultado is not None:  # Si encontró solución
                return resultado
            
            del asignacion[var]  # Deshacer asignación (backtrack)
    
    return None  # No se encontró solución

# Funciones auxiliares
def contar_conflictos(var, valor, asignacion, csp):
    """Cuántas restricciones violaría asignar este valor"""
    return sum(1 for vecino in csp.vecinos[var] 
              if vecino in asignacion and not cumple_restriccion(valor, asignacion[vecino]))

def consistente(var, valor, asignacion, csp):
    """Verifica si una asignación es consistente"""
    return all(cumple_restriccion(valor, asignacion[vecino])
              for vecino in csp.vecinos[var] if vecino in asignacion)

def cumple_restriccion(valor1, valor2):
    """Función genérica de restricción (ejemplo: valores diferentes)"""
    return valor1 != valor2

# Ejemplo práctico: Sudoku 4x4
def crear_sudoku_4x4():
    """Crea un CSP para Sudoku 4x4"""
    variables = [(i, j) for i in range(4) for j in range(4)]
    dominios = {(i, j): list(range(1, 5)) for i, j in variables}
    
    # Restricciones: filas, columnas y cajas 2x2
    restricciones = []
    
    # Misma fila y misma columna
    for i in range(4):
        for j in range(4):
            for k in range(4):
                if k != j: restricciones.append(((i, j), (i, k)))  # Misma fila
                if k != i: restricciones.append(((i, j), (k, j)))  # Misma columna
    
    # Cajas 2x2
    for bi in [0, 2]:
        for bj in [0, 2]:
            caja = [(bi + i, bj + j) for i in range(2) for j in range(2)]
            for i, v1 in enumerate(caja):
                for v2 in caja[i + 1:]:
                    restricciones.append((v1, v2))
    
    return CSP(variables, dominios, restricciones)

# ----------------------------------
# Ejemplo de uso con Sudoku 4x4
# ----------------------------------
if __name__ == "__main__":
    # Crear CSP
    sudoku = crear_sudoku_4x4()
    
    # Añadir pistas (valores fijos)
    pistas = {
        (0, 0): 1, (0, 2): 3,
        (1, 1): 4, (3, 3): 2
    }
    for (i, j), val in pistas.items():
        sudoku.dominios[(i, j)] = [val]
    
    # Resolver
    solucion = backtracking({}, sudoku)
    
    # Mostrar solución
    if solucion:
        print("Solución encontrada:")
        for i in range(4):
            print([solucion[(i, j)] for j in range(4)])
    else:
        print("No se encontró solución")