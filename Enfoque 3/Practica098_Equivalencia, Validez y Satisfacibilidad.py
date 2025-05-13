# -*- coding: utf-8 -*-                                                     # Define la codificación de caracteres del archivo como UTF-8
"""
Created on Sun Apr 27 14:39:03 2025                                         # Indica la fecha y hora de creación del archivo
                                                                           #
@author: elvin                                                              # Define el autor del archivo
"""

# Definimos una clase MotorInferencia                                        # Define una clase llamada MotorInferencia
class MotorInferencia:                                                     # Define la clase MotorInferencia
    def __init__(self):                                                     # Define el constructor de la clase
        self.hechos = set()                                                 # Inicializa un conjunto vacío para almacenar los hechos conocidos
        self.reglas = []                                                  # Inicializa una lista vacía para almacenar las reglas

    def agregar_hecho(self, hecho):                                        # Define el método para agregar un hecho
        # Agrega un hecho al conjunto                                       # Comentario indicando la adición de un hecho
        self.hechos.add(hecho)                                              # Agrega el hecho al conjunto de hechos

    def agregar_regla(self, condiciones, conclusion):                      # Define el método para agregar una regla
        # Agrega una regla (condiciones => conclusion)                     # Comentario indicando la adición de una regla
        self.reglas.append((condiciones, conclusion))                      # Agrega la regla (tupla de condiciones y conclusión) a la lista de reglas

    def inferir(self):                                                      # Define el método para realizar la inferencia
        # Motor de inferencia: aplica reglas mientras se descubran nuevos hechos # Comentario explicando el motor de inferencia
        nuevos = True                                                      # Inicializa una bandera para rastrear si se infirieron nuevos hechos
        while nuevos:                                                      # Continúa mientras se infieran nuevos hechos
            nuevos = False                                                 # Restablece la bandera para cada iteración
            for condiciones, conclusion in self.reglas:                    # Itera sobre cada regla en la lista de reglas
                # Si las condiciones se cumplen y la conclusión aún no es un hecho # Comentario verificando las condiciones y la conclusión
                if self.evaluar(condiciones) and conclusion not in self.hechos: # Evalúa las condiciones y verifica si la conclusión no es un hecho conocido
                    print(f"Derivado: {conclusion}")                       # Imprime la conclusión derivada
                    self.hechos.add(conclusion)                           # Añade la conclusión al conjunto de hechos conocidos
                    nuevos = True                                          # Establece la bandera en True para continuar la inferencia

    def evaluar(self, condiciones):                                         # Define el método para evaluar las condiciones
        # Evalúa si unas condiciones son verdaderas                         # Comentario indicando la evaluación de las condiciones
        if isinstance(condiciones, str):                                  # Si las condiciones son una cadena (un hecho simple)
            return condiciones in self.hechos                             # Retorna True si el hecho está en el conjunto de hechos
        elif isinstance(condiciones, tuple):                                # Si las condiciones son una tupla (una expresión lógica)
            operador = condiciones[0]                                      # Obtiene el operador lógico (AND, OR, NOT)
            if operador == "AND":                                          # Si el operador es AND
                # Todas las condiciones deben cumplirse                     # Comentario indicando que todas las condiciones deben ser verdaderas
                return all(self.evaluar(c) for c in condiciones[1:])      # Retorna True si todas las sub-condiciones son verdaderas
            elif operador == "OR":                                           # Si el operador es OR
                # Al menos una condición debe cumplirse                    # Comentario indicando que al menos una condición debe ser verdadera
                return any(self.evaluar(c) for c in condiciones[1:])      # Retorna True si al menos una sub-condición es verdadera
            elif operador == "NOT":                                          # Si el operador es NOT
                # La condición NO debe cumplirse                          # Comentario indicando que la condición no debe ser verdadera
                return not self.evaluar(condiciones[1])                   # Retorna True si la sub-condición es falsa
        return False                                                       # Retorna False si las condiciones no se pueden evaluar

# Crear una instancia del motor                                          # Crea una instancia de la clase MotorInferencia
motor = MotorInferencia()                                                  # Crea un objeto llamado motor

# Agregar hechos iniciales                                               # Comentario indicando la adición de hechos iniciales
motor.agregar_hecho("tiene_agua")                                         # Agrega el hecho "tiene_agua"
motor.agregar_hecho("hay_sol")                                           # Agrega el hecho "hay_sol"

# Agregar reglas de inferencia                                            # Comentario indicando la adición de reglas de inferencia
motor.agregar_regla(("AND", "tiene_agua", "hay_sol"), "crece_planta")     # Agrega una regla: SI tiene_agua Y hay_sol ENTONCES crece_planta
motor.agregar_regla(("AND", "crece_planta", "hay_sol"), "produce_fruta")   # Agrega una regla: SI crece_planta Y hay_sol ENTONCES produce_fruta
motor.agregar_regla(("NOT", "tiene_agua"), "planta_muere")                 # Agrega una regla: SI NO tiene_agua ENTONCES planta_muere
motor.agregar_regla(("OR", "produce_fruta", "planta_muere"), "recolectar") # Agrega una regla: SI produce_fruta O planta_muere ENTONCES recolectar

# Ejecutar inferencia automática                                        # Comentario indicando la ejecución de la inferencia
motor.inferir()                                                          # Llama al método inferir para aplicar las reglas

# Mostrar todos los hechos obtenidos al final                             # Comentario indicando la muestra de los hechos finales
print("\nHechos finales:")                                               # Imprime un encabezado para los hechos finales
for hecho in motor.hechos:                                                # Itera sobre cada hecho en el conjunto de hechos
    print(hecho)                                                         # Imprime el hecho
