# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 10:35:56 2025

@author: elvin
"""

class CSP:                                      # Clase para Problemas de Satisfacción de Restricciones
    def __init__(self, variables, dominios,     # Constructor con parámetros básicos
                 restricciones):
        self.variables = variables              # Lista de variables del problema
        self.dominios = dominios                # Diccionario {variable: [valores_posibles]}
        self.restricciones = restricciones      # Diccionario {(var1, var2): [funciones_restricción]}
        self.asignacion = {}                    # Almacena la asignación actual {variable: valor}

    def consistente(self, variable, valor,      # Verifica si una asignación es válida
                    asignacion):
        for (v1, v2), restricciones in self.restricciones.items():
            if v1 == variable and v2 in asignacion:
                for restriccion in restricciones:
                    if not restriccion(valor, asignacion[v2]):
                        return False
            elif v2 == variable and v1 in asignacion:
                for restriccion in restricciones:
                    if not restriccion(asignacion[v1], valor):
                        return False
        return True

    def backtracking(self, asignacion={}):       # Algoritmo principal de backtracking
        if len(asignacion) == len(self.variables):  # Si todas las variables tienen valor
            return asignacion                    

        var_no_asignada = [v for v in self.variables  # Selecciona próxima variable sin asignar
                           if v not in asignacion][0]
        
        for valor in self.dominios[var_no_asignada]:  # Prueba cada valor posible
            if self.consistente(var_no_asignada,      # Verifica restricciones
                                valor, asignacion):
                nueva_asignacion = asignacion.copy()
                nueva_asignacion[var_no_asignada] = valor
                resultado = self.backtracking(nueva_asignacion)  # Llamada recursiva
                if resultado is not None:
                    return resultado
        return None                                # No se encontró solución

# --- Ejemplo: Problema de las 4 Reinas ---
if __name__ == "__main__":
    variables = ['R1', 'R2', 'R3', 'R4']        # 4 reinas (una por columna)
    dominios = {v: [1, 2, 3, 4] for v in variables}  # Posiciones en filas (1-4)

    # Restricciones: No se ataquen entre sí
    def no_se_ataquen(fila1, fila2):            # Función de restricción
        return fila1 != fila2 and abs(fila1 - fila2) != abs(variables.index('R1') - variables.index('R2'))

    # Pares de variables que tienen restricciones
    restricciones = {
        ('R1', 'R2'): [no_se_ataquen],
        ('R1', 'R3'): [no_se_ataquen],
        ('R1', 'R4'): [no_se_ataquen],
        ('R2', 'R3'): [no_se_ataquen],
        ('R2', 'R4'): [no_se_ataquen],
        ('R3', 'R4'): [no_se_ataquen]
    }

    problema = CSP(variables, dominios,         # Crea instancia del problema
                   restricciones)
    
    solucion = problema.backtracking()           # Ejecuta el algoritmo
    print("Solución encontrada:", solucion)      # Muestra resultado