# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 14:39:03 2025

@author: elvin
"""

# Definimos una clase MotorInferencia
class MotorInferencia:
    def __init__(self):
        self.hechos = set()       # Conjunto de hechos conocidos
        self.reglas = []          # Lista de reglas (cada regla es (condiciones, conclusion))

    def agregar_hecho(self, hecho):
        # Agrega un hecho al conjunto
        self.hechos.add(hecho)

    def agregar_regla(self, condiciones, conclusion):
        # Agrega una regla (condiciones => conclusion)
        self.reglas.append((condiciones, conclusion))

    def inferir(self):
        # Motor de inferencia: aplica reglas mientras se descubran nuevos hechos
        nuevos = True
        while nuevos:
            nuevos = False
            for condiciones, conclusion in self.reglas:
                # Si las condiciones se cumplen y la conclusión aún no es un hecho
                if self.evaluar(condiciones) and conclusion not in self.hechos:
                    print(f"Derivado: {conclusion}")
                    self.hechos.add(conclusion)  # Añadir nuevo hecho
                    nuevos = True  # Seguimos buscando inferencias

    def evaluar(self, condiciones):
        # Evalúa si unas condiciones son verdaderas
        if isinstance(condiciones, str):
            return condiciones in self.hechos  # Si es un hecho simple
        elif isinstance(condiciones, tuple):
            operador = condiciones[0]
            if operador == "AND":
                # Todas las condiciones deben cumplirse
                return all(self.evaluar(c) for c in condiciones[1:])
            elif operador == "OR":
                # Al menos una condición debe cumplirse
                return any(self.evaluar(c) for c in condiciones[1:])
            elif operador == "NOT":
                # La condición NO debe cumplirse
                return not self.evaluar(condiciones[1])
        return False

# Crear una instancia del motor
motor = MotorInferencia()

# Agregar hechos iniciales
motor.agregar_hecho("tiene_agua")
motor.agregar_hecho("hay_sol")

# Agregar reglas de inferencia
motor.agregar_regla(("AND", "tiene_agua", "hay_sol"), "crece_planta")
motor.agregar_regla(("AND", "crece_planta", "hay_sol"), "produce_fruta")
motor.agregar_regla(("NOT", "tiene_agua"), "planta_muere")
motor.agregar_regla(("OR", "produce_fruta", "planta_muere"), "recolectar")

# Ejecutar inferencia automática
motor.inferir()

# Mostrar todos los hechos obtenidos al final
print("\nHechos finales:")
for hecho in motor.hechos:
    print(f"- {hecho}")
