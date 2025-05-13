# -*- coding: utf-8 -*-                                      # Especifica la codificación del archivo como UTF-8
"""
Created on Sun Apr 27 16:26:20 2025

@author: elvin
"""

"""
Implementación de Lógica Difusa y Conjuntos Difusos en Python

Este código incluye:
1. Definición de conjuntos difusos y funciones de pertenencia
2. Operaciones básicas entre conjuntos difusos
3. Sistema de inferencia difusa (Mamdani)
4. Ejemplos prácticos de aplicación
"""

from typing import Dict, List, Tuple, Callable                  # Importa tipos para type hints
import numpy as np                                             # Para operaciones numéricas
import matplotlib.pyplot as plt                                # Para graficar funciones

# =============================================================================
# 1. DEFINICIÓN DE CONJUNTOS DIFUSOS
# =============================================================================

class FuzzySet:
    """
    Representa un conjunto difuso con su función de pertenencia.
    """
    
    def __init__(self, name: str, membership_func: Callable[[float], float], domain: Tuple[float, float]):
        self.name = name                                       # Nombre descriptivo del conjunto
        self.membership_func = membership_func                 # Función que calcula pertenencia (0-1)
        self.domain = domain                                   # Rango de valores posibles (min, max)
    
    def __call__(self, x: float) -> float:
        """Calcula el grado de pertenencia de un valor x"""
        return self.membership_func(x)                         # Aplica la función de pertenencia
    
    def plot(self, ax=None, **kwargs):
        """Grafica la función de pertenencia"""
        x_vals = np.linspace(*self.domain, 100)               # Genera 100 puntos en el dominio
        y_vals = [self.membership_func(x) for x in x_vals]    # Calcula valores de pertenencia
        
        if ax is None:                                         # Si no se proporcionó eje
            fig, ax = plt.subplots()                           # Crea nueva figura
        
        ax.plot(x_vals, y_vals, label=self.name, **kwargs)    # Grafica la función
        ax.set_ylim(0, 1.1)                                   # Establece límites del eje Y
        ax.legend()                                            # Muestra leyenda
        return ax

# Funciones de pertenencia comunes
def triangular(a: float, b: float, c: float) -> Callable[[float], float]:
    """Crea una función de pertenencia triangular"""
    return lambda x: max(min((x-a)/(b-a), (c-x)/(c-b)), 0)    # Función triangular con vértices a,b,c

def trapezoidal(a: float, b: float, c: float, d: float) -> Callable[[float], float]:
    """Crea una función de pertenencia trapezoidal"""
    return lambda x: max(min((x-a)/(b-a), 1, (d-x)/(d-c)), 0) # Función trapezoidal con puntos a,b,c,d

def gaussian(mean: float, sigma: float) -> Callable[[float], float]:
    """Crea una función de pertenencia gaussiana"""
    return lambda x: np.exp(-((x - mean)**2) / (2 * sigma**2)) # Campana de Gauss con media y desviación

# =============================================================================
# 2. OPERACIONES DIFUSAS
# =============================================================================

def fuzzy_and(set1: FuzzySet, set2: FuzzySet) -> FuzzySet:
    """Intersección difusa (mínimo)"""
    return FuzzySet(
        f"{set1.name}_AND_{set2.name}",                        # Nombre combinado
        lambda x: min(set1(x), set2(x)),                       # Operador mínimo
        (min(set1.domain[0], set2.domain[0]), max(set1.domain[1], set2.domain[1]))  # Nuevo dominio
    )

def fuzzy_or(set1: FuzzySet, set2: FuzzySet) -> FuzzySet:
    """Unión difusa (máximo)"""
    return FuzzySet(
        f"{set1.name}_OR_{set2.name}",                         # Nombre combinado
        lambda x: max(set1(x), set2(x)),                       # Operador máximo
        (min(set1.domain[0], set2.domain[0]), max(set1.domain[1], set2.domain[1]))  # Nuevo dominio
    )

def fuzzy_not(set_: FuzzySet) -> FuzzySet:
    """Complemento difuso"""
    return FuzzySet(
        f"NOT_{set_.name}",                                    # Nombre con prefijo NOT
        lambda x: 1 - set_(x),                                # 1 - valor de pertenencia
        set_.domain                                           # Mismo dominio
    )

# =============================================================================
# 3. SISTEMA DE INFERENCIA DIFUSA (MAMDANI)
# =============================================================================

class FuzzyInferenceSystem:
    """
    Sistema de inferencia difusa tipo Mamdani.
    """
    
    def __init__(self):
        self.input_sets: Dict[str, Dict[str, FuzzySet]] = {}   # Variables de entrada {var: {set: FuzzySet}}
        self.output_sets: Dict[str, Dict[str, FuzzySet]] = {}  # Variables de salida {var: {set: FuzzySet}}
        self.rules: List[str] = []                             # Lista de reglas en formato "IF X THEN Y"
    
    def add_input_variable(self, name: str, sets: Dict[str, FuzzySet]):
        """Añade una variable de entrada con sus conjuntos difusos"""
        self.input_sets[name] = sets                           # Almacena conjuntos por nombre de variable
    
    def add_output_variable(self, name: str, sets: Dict[str, FuzzySet]):
        """Añade una variable de salida con sus conjuntos difusos"""
        self.output_sets[name] = sets                          # Almacena conjuntos por nombre de variable
    
    def add_rule(self, rule: str):
        """Añade una regla difusa"""
        self.rules.append(rule)                                # Agrega regla a la lista
    
    def evaluate(self, inputs: Dict[str, float]) -> Dict[str, float]:
        """
        Evalúa el sistema con valores de entrada concretos.
        """
        # 1. Fuzzificación
        fuzzified = {}                                         # Diccionario para resultados
        for var, value in inputs.items():                      # Para cada variable de entrada
            fuzzified[var] = {}                                # Inicializa sub-diccionario
            for set_name, set_ in self.input_sets[var].items(): # Para cada conjunto difuso
                fuzzified[var][set_name] = set_(value)         # Calcula grado de pertenencia
        
        # 2. Evaluación de reglas
        rule_outputs = []                                      # Almacena salidas de reglas
        for rule in self.rules:                                # Para cada regla
            if "AND" in rule:                                  # Si es regla con AND
                parts = rule.split(" AND ")                    # Divide la regla
                # Evaluar condiciones
                activation = min(                             # Toma el mínimo (AND difuso)
                    fuzzified[parts[0].split()[1]][parts[0].split()[0]],  # Valor primer conjunto
                    fuzzified[parts[1].split()[1]][parts[1].split()[0]]   # Valor segundo conjunto
                )
            else:                                              # Si es regla simple
                part = rule.split("IF ")[1].split(" THEN")[0]  # Extrae parte de condición
                var, set_name = part.split()                   # Separa variable y conjunto
                activation = fuzzified[var][set_name]          # Obtiene grado de pertenencia
            
            # Obtener conjunto de salida
            output_part = rule.split("THEN ")[1]               # Extrae parte de conclusión
            output_var, output_set = output_part.split()       # Separa variable y conjunto de salida
            rule_outputs.append((output_var, output_set, activation))  # Guarda resultado
        
        # 3. Agregación y 4. Defuzzificación
        outputs = {}                                           # Diccionario para resultados finales
        for var in self.output_sets:                           # Para cada variable de salida
            # Crear conjunto agregado
            x_vals = np.linspace(*self.output_sets[var][list(self.output_sets[var].keys())[0]].domain, 100)
            aggregated = np.zeros_like(x_vals)                 # Inicializa array de ceros
            
            for output_var, output_set, activation in rule_outputs:  # Para cada salida de regla
                if output_var == var:                           # Si corresponde a esta variable
                    y_vals = [min(activation, self.output_sets[var][output_set](x)) for x in x_vals]
                    aggregated = np.maximum(aggregated, y_vals)  # Agrega con operador máximo
            
            # Calcular centroide (defuzzificación)
            if np.sum(aggregated) > 0:                         # Si hay área bajo la curva
                centroid = np.sum(x_vals * aggregated) / np.sum(aggregated)  # Calcula centro de masa
            else:
                centroid = np.mean(x_vals)                     # Valor medio como fallback
            
            outputs[var] = centroid                            # Almacena resultado
        
        return outputs                                         # Retorna valores defuzzificados

# =============================================================================
# 4. EJEMPLOS DE APLICACIÓN
# =============================================================================

def ejemplo_temperatura():
    """Sistema de control difuso para temperatura"""
    fis = FuzzyInferenceSystem()                               # Crea nuevo sistema
    
    # 1. Definir variables de entrada y salida
    # Temperatura (entrada)
    temp_sets = {                                             # Conjuntos para temperatura
        "fria": FuzzySet("fria", triangular(0, 10, 20), (0, 40)),
        "templada": FuzzySet("templada", triangular(10, 20, 30), (0, 40)),
        "caliente": FuzzySet("caliente", triangular(20, 30, 40), (0, 40))
    }
    fis.add_input_variable("temperatura", temp_sets)           # Añade variable de entrada
    
    # Velocidad ventilador (salida)
    fan_sets = {                                              # Conjuntos para velocidad
        "baja": FuzzySet("baja", triangular(0, 25, 50), (0, 100)),
        "media": FuzzySet("media", triangular(25, 50, 75), (0, 100)),
        "alta": FuzzySet("alta", triangular(50, 75, 100), (0, 100))
    }
    fis.add_output_variable("ventilador", fan_sets)            # Añade variable de salida
    
    # 2. Añadir reglas
    fis.add_rule("IF temperatura IS fria THEN ventilador IS baja")  # Regla 1
    fis.add_rule("IF temperatura IS templada THEN ventilador IS media")  # Regla 2
    fis.add_rule("IF temperatura IS caliente THEN ventilador IS alta")  # Regla 3
    
    # 3. Evaluar el sistema
    test_temps = [5, 15, 25, 35]                              # Valores de prueba
    print("\nResultados del sistema de control de temperatura:")
    for temp in test_temps:                                    # Para cada temperatura
        result = fis.evaluate({"temperatura": temp})           # Evalúa el sistema
        print(f"Temperatura: {temp}°C -> Velocidad ventilador: {result['ventilador']:.1f}%")
    
    # Graficar conjuntos
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))      # Crea figura con 2 subplots
    for name, set_ in temp_sets.items():                       # Grafica conjuntos de temperatura
        set_.plot(ax1)
    ax1.set_title("Conjuntos difusos de temperatura")
    
    for name, set_ in fan_sets.items():                        # Grafica conjuntos de velocidad
        set_.plot(ax2)
    ax2.set_title("Conjuntos difusos de velocidad")
    plt.show()                                                 # Muestra gráficos

def ejemplo_propina():
    """Sistema para calcular propina basado en servicio y comida"""
    fis = FuzzyInferenceSystem()                               # Crea nuevo sistema
    
    # 1. Definir variables
    # Calidad del servicio (entrada)
    service_sets = {                                          # Conjuntos para servicio
        "pobre": FuzzySet("pobre", triangular(0, 0, 5), (0, 10)),
        "bueno": FuzzySet("bueno", triangular(0, 5, 10), (0, 10)),
        "excelente": FuzzySet("excelente", triangular(5, 10, 10), (0, 10))
    }
    fis.add_input_variable("servicio", service_sets)           # Añade variable de entrada
    
    # Calidad de la comida (entrada)
    food_sets = {                                             # Conjuntos para comida
        "mala": FuzzySet("mala", triangular(0, 0, 5), (0, 10)),
        "decente": FuzzySet("decente", triangular(0, 5, 10), (0, 10)),
        "deliciosa": FuzzySet("deliciosa", triangular(5, 10, 10), (0, 10))
    }
    fis.add_input_variable("comida", food_sets)                # Añade variable de entrada
    
    # Propina (salida)
    tip_sets = {                                              # Conjuntos para propina
        "baja": FuzzySet("baja", triangular(0, 5, 10), (0, 25)),
        "media": FuzzySet("media", triangular(5, 12.5, 20), (0, 25)),
        "alta": FuzzySet("alta", triangular(15, 25, 25), (0, 25))
    }
    fis.add_output_variable("propina", tip_sets)               # Añade variable de salida
    
    # 2. Añadir reglas
    fis.add_rule("IF servicio IS pobre OR comida IS mala THEN propina IS baja")  # Regla 1
    fis.add_rule("IF servicio IS bueno THEN propina IS media")  # Regla 2
    fis.add_rule("IF servicio IS excelente OR comida IS deliciosa THEN propina IS alta")  # Regla 3
    fis.add_rule("IF comida IS decente AND servicio IS bueno THEN propina IS media")  # Regla 4
    
    # 3. Evaluar el sistema
    test_cases = [                                            # Casos de prueba
        {"servicio": 3, "comida": 8},
        {"servicio": 7, "comida": 5},
        {"servicio": 9, "comida": 9}
    ]
    
    print("\nResultados del sistema de propinas:")
    for case in test_cases:                                    # Para cada caso
        result = fis.evaluate(case)                            # Evalúa el sistema
        print(f"Servicio: {case['servicio']}, Comida: {case['comida']} -> Propina: {result['propina']:.1f}%")

if __name__ == "__main__":
    print("=== SISTEMAS DIFUSOS DEMOSTRACIÓN ===")            # Mensaje inicial
    ejemplo_temperatura()                                      # Ejecuta ejemplo de temperatura
    ejemplo_propina()                                          # Ejecuta ejemplo de propinas