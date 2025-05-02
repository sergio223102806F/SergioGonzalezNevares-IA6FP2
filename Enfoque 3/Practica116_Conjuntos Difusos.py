# -*- coding: utf-8 -*-
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

from typing import Dict, List, Tuple, Callable
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# 1. DEFINICIÓN DE CONJUNTOS DIFUSOS
# =============================================================================

class FuzzySet:
    """
    Representa un conjunto difuso con su función de pertenencia.
    
    Atributos:
        name: Nombre del conjunto difuso
        membership_func: Función que calcula el grado de pertenencia (0 a 1)
        domain: Rango de valores posibles (min, max)
    """
    
    def __init__(self, name: str, membership_func: Callable[[float], float], domain: Tuple[float, float]):
        self.name = name
        self.membership_func = membership_func
        self.domain = domain
    
    def __call__(self, x: float) -> float:
        """Calcula el grado de pertenencia de un valor x"""
        return self.membership_func(x)
    
    def plot(self, ax=None, **kwargs):
        """Grafica la función de pertenencia"""
        x_vals = np.linspace(*self.domain, 100)
        y_vals = [self.membership_func(x) for x in x_vals]
        
        if ax is None:
            fig, ax = plt.subplots()
        
        ax.plot(x_vals, y_vals, label=self.name, **kwargs)
        ax.set_ylim(0, 1.1)
        ax.legend()
        return ax

# Funciones de pertenencia comunes
def triangular(a: float, b: float, c: float) -> Callable[[float], float]:
    """Crea una función de pertenencia triangular"""
    return lambda x: max(min((x-a)/(b-a), (c-x)/(c-b)), 0)

def trapezoidal(a: float, b: float, c: float, d: float) -> Callable[[float], float]:
    """Crea una función de pertenencia trapezoidal"""
    return lambda x: max(min((x-a)/(b-a), 1, (d-x)/(d-c)), 0)

def gaussian(mean: float, sigma: float) -> Callable[[float], float]:
    """Crea una función de pertenencia gaussiana"""
    return lambda x: np.exp(-((x - mean)**2) / (2 * sigma**2))

# =============================================================================
# 2. OPERACIONES DIFUSAS
# =============================================================================

def fuzzy_and(set1: FuzzySet, set2: FuzzySet) -> FuzzySet:
    """Intersección difusa (mínimo)"""
    return FuzzySet(
        f"{set1.name}_AND_{set2.name}",
        lambda x: min(set1(x), set2(x)),
        (min(set1.domain[0], set2.domain[0]), max(set1.domain[1], set2.domain[1]))
    )

def fuzzy_or(set1: FuzzySet, set2: FuzzySet) -> FuzzySet:
    """Unión difusa (máximo)"""
    return FuzzySet(
        f"{set1.name}_OR_{set2.name}",
        lambda x: max(set1(x), set2(x)),
        (min(set1.domain[0], set2.domain[0]), max(set1.domain[1], set2.domain[1]))
    )

def fuzzy_not(set_: FuzzySet) -> FuzzySet:
    """Complemento difuso"""
    return FuzzySet(
        f"NOT_{set_.name}",
        lambda x: 1 - set_(x),
        set_.domain
    )

# =============================================================================
# 3. SISTEMA DE INFERENCIA DIFUSA (MAMDANI)
# =============================================================================

class FuzzyInferenceSystem:
    """
    Sistema de inferencia difusa tipo Mamdani.
    
    Componentes:
        input_sets: Diccionario de conjuntos difusos de entrada
        output_sets: Diccionario de conjuntos difusos de salida
        rules: Lista de reglas difusas
    """
    
    def __init__(self):
        self.input_sets: Dict[str, Dict[str, FuzzySet]] = {}  # {variable: {conjunto: FuzzySet}}
        self.output_sets: Dict[str, Dict[str, FuzzySet]] = {}  # {variable: {conjunto: FuzzySet}}
        self.rules: List[str] = []  # Lista de reglas en formato "IF X THEN Y"
    
    def add_input_variable(self, name: str, sets: Dict[str, FuzzySet]):
        """Añade una variable de entrada con sus conjuntos difusos"""
        self.input_sets[name] = sets
    
    def add_output_variable(self, name: str, sets: Dict[str, FuzzySet]):
        """Añade una variable de salida con sus conjuntos difusos"""
        self.output_sets[name] = sets
    
    def add_rule(self, rule: str):
        """Añade una regla difusa"""
        self.rules.append(rule)
    
    def evaluate(self, inputs: Dict[str, float]) -> Dict[str, float]:
        """
        Evalúa el sistema con valores de entrada concretos.
        
        Pasos:
        1. Fuzzificación: Convertir entradas a grados de pertenencia
        2. Evaluación de reglas: Aplicar operadores difusos
        3. Agregación: Combinar resultados de todas las reglas
        4. Defuzzificación: Convertir a valor concreto (centroide)
        """
        # 1. Fuzzificación
        fuzzified = {}
        for var, value in inputs.items():
            fuzzified[var] = {}
            for set_name, set_ in self.input_sets[var].items():
                fuzzified[var][set_name] = set_(value)
        
        # 2. Evaluación de reglas
        rule_outputs = []
        for rule in self.rules:
            # Parsear regla (simplificado)
            if "AND" in rule:
                parts = rule.split(" AND ")
                # Evaluar condiciones
                activation = min(
                    fuzzified[parts[0].split()[1]][parts[0].split()[0]],
                    fuzzified[parts[1].split()[1]][parts[1].split()[0]]
                )
            else:
                part = rule.split("IF ")[1].split(" THEN")[0]
                var, set_name = part.split()
                activation = fuzzified[var][set_name]
            
            # Obtener conjunto de salida
            output_part = rule.split("THEN ")[1]
            output_var, output_set = output_part.split()
            rule_outputs.append((output_var, output_set, activation))
        
        # 3. Agregación y 4. Defuzzificación
        outputs = {}
        for var in self.output_sets:
            # Crear conjunto agregado
            x_vals = np.linspace(*self.output_sets[var][list(self.output_sets[var].keys())[0]].domain, 100)
            aggregated = np.zeros_like(x_vals)
            
            for output_var, output_set, activation in rule_outputs:
                if output_var == var:
                    y_vals = [min(activation, self.output_sets[var][output_set](x)) for x in x_vals]
                    aggregated = np.maximum(aggregated, y_vals)
            
            # Calcular centroide (defuzzificación)
            if np.sum(aggregated) > 0:
                centroid = np.sum(x_vals * aggregated) / np.sum(aggregated)
            else:
                centroid = np.mean(x_vals)
            
            outputs[var] = centroid
        
        return outputs

# =============================================================================
# 4. EJEMPLOS DE APLICACIÓN
# =============================================================================

def ejemplo_temperatura():
    """Sistema de control difuso para temperatura"""
    fis = FuzzyInferenceSystem()
    
    # 1. Definir variables de entrada y salida
    # Temperatura (entrada)
    temp_sets = {
        "fria": FuzzySet("fria", triangular(0, 10, 20), (0, 40)),
        "templada": FuzzySet("templada", triangular(10, 20, 30), (0, 40)),
        "caliente": FuzzySet("caliente", triangular(20, 30, 40), (0, 40))
    }
    fis.add_input_variable("temperatura", temp_sets)
    
    # Velocidad ventilador (salida)
    fan_sets = {
        "baja": FuzzySet("baja", triangular(0, 25, 50), (0, 100)),
        "media": FuzzySet("media", triangular(25, 50, 75), (0, 100)),
        "alta": FuzzySet("alta", triangular(50, 75, 100), (0, 100))
    }
    fis.add_output_variable("ventilador", fan_sets)
    
    # 2. Añadir reglas
    fis.add_rule("IF temperatura IS fria THEN ventilador IS baja")
    fis.add_rule("IF temperatura IS templada THEN ventilador IS media")
    fis.add_rule("IF temperatura IS caliente THEN ventilador IS alta")
    
    # 3. Evaluar el sistema
    test_temps = [5, 15, 25, 35]
    print("\nResultados del sistema de control de temperatura:")
    for temp in test_temps:
        result = fis.evaluate({"temperatura": temp})
        print(f"Temperatura: {temp}°C -> Velocidad ventilador: {result['ventilador']:.1f}%")
    
    # Graficar conjuntos
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    for name, set_ in temp_sets.items():
        set_.plot(ax1)
    ax1.set_title("Conjuntos difusos de temperatura")
    
    for name, set_ in fan_sets.items():
        set_.plot(ax2)
    ax2.set_title("Conjuntos difusos de velocidad")
    plt.show()

def ejemplo_propina():
    """Sistema para calcular propina basado en servicio y comida"""
    fis = FuzzyInferenceSystem()
    
    # 1. Definir variables
    # Calidad del servicio (entrada)
    service_sets = {
        "pobre": FuzzySet("pobre", triangular(0, 0, 5), (0, 10)),
        "bueno": FuzzySet("bueno", triangular(0, 5, 10), (0, 10)),
        "excelente": FuzzySet("excelente", triangular(5, 10, 10), (0, 10))
    }
    fis.add_input_variable("servicio", service_sets)
    
    # Calidad de la comida (entrada)
    food_sets = {
        "mala": FuzzySet("mala", triangular(0, 0, 5), (0, 10)),
        "decente": FuzzySet("decente", triangular(0, 5, 10), (0, 10)),
        "deliciosa": FuzzySet("deliciosa", triangular(5, 10, 10), (0, 10))
    }
    fis.add_input_variable("comida", food_sets)
    
    # Propina (salida)
    tip_sets = {
        "baja": FuzzySet("baja", triangular(0, 5, 10), (0, 25)),
        "media": FuzzySet("media", triangular(5, 12.5, 20), (0, 25)),
        "alta": FuzzySet("alta", triangular(15, 25, 25), (0, 25))
    }
    fis.add_output_variable("propina", tip_sets)
    
    # 2. Añadir reglas
    fis.add_rule("IF servicio IS pobre OR comida IS mala THEN propina IS baja")
    fis.add_rule("IF servicio IS bueno THEN propina IS media")
    fis.add_rule("IF servicio IS excelente OR comida IS deliciosa THEN propina IS alta")
    fis.add_rule("IF comida IS decente AND servicio IS bueno THEN propina IS media")
    
    # 3. Evaluar el sistema
    test_cases = [
        {"servicio": 3, "comida": 8},
        {"servicio": 7, "comida": 5},
        {"servicio": 9, "comida": 9}
    ]
    
    print("\nResultados del sistema de propinas:")
    for case in test_cases:
        result = fis.evaluate(case)
        print(f"Servicio: {case['servicio']}, Comida: {case['comida']} -> Propina: {result['propina']:.1f}%")

if __name__ == "__main__":
    print("=== SISTEMAS DIFUSOS DEMOSTRACIÓN ===")
    ejemplo_temperatura()
    ejemplo_propina()