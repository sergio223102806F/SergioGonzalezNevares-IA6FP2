# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 16:26:20 2025

@author: elvin
"""

"""
Implementación de un Sistema de Inferencia Difusa (FIS) tipo Mamdani

Este código implementa:
1. Conjuntos difusos y funciones de pertenencia
2. Un motor de inferencia difusa completo
3. Mecanismo de fuzzificación, evaluación de reglas y defuzzificación
4. Ejemplo práctico de control difuso
"""

from typing import Dict, List, Tuple, Callable
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# 1. DEFINICIÓN DE CONJUNTOS DIFUSOS
# =============================================================================

class ConjuntoDifuso:
    """
    Representa un conjunto difuso con su función de pertenencia.
    
    Atributos:
        nombre: Identificador del conjunto
        funcion_pertenencia: Función que calcula el grado de pertenencia (0-1)
        dominio: Tupla con los límites del dominio (min, max)
    """
    
    def __init__(self, nombre: str, funcion_pertenencia: Callable[[float], float], dominio: Tuple[float, float]):
        self.nombre = nombre
        self.funcion = funcion_pertenencia
        self.dominio = dominio
    
    def calcular_pertenencia(self, x: float) -> float:
        """Evalúa el grado de pertenencia para un valor x"""
        return self.funcion(x)
    
    def graficar(self, ax=None, **kwargs):
        """Visualiza la función de pertenencia"""
        x = np.linspace(*self.dominio, 100)
        y = [self.calcular_pertenencia(xi) for xi in x]
        
        if ax is None:
            _, ax = plt.subplots()
        
        ax.plot(x, y, label=self.nombre, **kwargs)
        ax.set_ylim(0, 1.1)
        ax.legend()
        return ax

# Funciones de pertenencia predefinidas
def triangular(a: float, b: float, c: float) -> Callable[[float], float]:
    """Genera función de pertenencia triangular"""
    return lambda x: max(min((x-a)/(b-a), (c-x)/(c-b)), 0)

def trapezoidal(a: float, b: float, c: float, d: float) -> Callable[[float], float]:
    """Genera función de pertenencia trapezoidal"""
    return lambda x: max(min((x-a)/(b-a), 1, (d-x)/(d-c)), 0)

# =============================================================================
# 2. MOTOR DE INFERENCIA DIFUSA
# =============================================================================

class SistemaInferenciaDifusa:
    """
    Implementa un sistema de inferencia difusa tipo Mamdani.
    
    Componentes:
        - Variables de entrada/salida con sus conjuntos difusos
        - Base de reglas difusas
        - Métodos para fuzzificación, inferencia y defuzzificación
    """
    
    def __init__(self):
        self.entradas: Dict[str, Dict[str, ConjuntoDifuso]] = {}
        self.salidas: Dict[str, Dict[str, ConjuntoDifuso]] = {}
        self.reglas: List[str] = []
    
    def agregar_variable_entrada(self, nombre: str, conjuntos: Dict[str, ConjuntoDifuso]):
        """Registra una variable de entrada con sus conjuntos difusos"""
        self.entradas[nombre] = conjuntos
    
    def agregar_variable_salida(self, nombre: str, conjuntos: Dict[str, ConjuntoDifuso]):
        """Registra una variable de salida con sus conjuntos difusos"""
        self.salidas[nombre] = conjuntos
    
    def agregar_regla(self, regla: str):
        """Añade una regla difusa al sistema"""
        self.reglas.append(regla)
    
    def evaluar(self, valores_entrada: Dict[str, float]) -> Dict[str, float]:
        """
        Ejecuta el proceso completo de inferencia difusa:
        1. Fuzzificación
        2. Evaluación de reglas
        3. Agregación de resultados
        4. Defuzzificación
        """
        # Paso 1: Fuzzificación
        valores_difusos = {}
        for var, valor in valores_entrada.items():
            valores_difusos[var] = {}
            for nombre, conjunto in self.entradas[var].items():
                valores_difusos[var][nombre] = conjunto.calcular_pertenencia(valor)
        
        # Paso 2: Evaluación de reglas
        activaciones = []
        for regla in self.reglas:
            # Parseo simplificado de reglas
            partes = regla.split()
            var_entrada = partes[1]
            conjunto_entrada = partes[2]
            var_salida = partes[5]
            conjunto_salida = partes[6]
            
            # Obtener grado de activación
            grado = valores_difusos[var_entrada][conjunto_entrada]
            activaciones.append((var_salida, conjunto_salida, grado))
        
        # Paso 3: Agregación y 4: Defuzzificación (centroide)
        resultados = {}
        for var in self.salidas:
            # Generar universo de discurso
            dominio = next(iter(self.salidas[var].values())).dominio
            x = np.linspace(*dominio, 100)
            
            # Inicializar superficie de salida agregada
            superficie_salida = np.zeros_like(x)
            
            # Aplicar todas las reglas relevantes
            for var_salida, conjunto_salida, grado in activaciones:
                if var_salida == var:
                    conjunto = self.salidas[var][conjunto_salida]
                    y = np.array([min(grado, conjunto.calcular_pertenencia(xi)) for xi in x])
                    superficie_salida = np.maximum(superficie_salida, y)
            
            # Calcular centroide (defuzzificación)
            if np.sum(superficie_salida) > 0:
                centroide = np.sum(x * superficie_salida) / np.sum(superficie_salida)
            else:
                centroide = np.mean(dominio)
            
            resultados[var] = centroide
        
        return resultados

# =============================================================================
# 3. EJEMPLO PRÁCTICO: CONTROL DE TEMPERATURA
# =============================================================================

def configurar_sistema_temperatura() -> SistemaInferenciaDifusa:
    """Configura un sistema de control difuso para temperatura"""
    fis = SistemaInferenciaDifusa()
    
    # Variable de entrada: Temperatura
    temp_conjuntos = {
        "fria": ConjuntoDifuso("fria", triangular(0, 10, 20), (0, 40)),
        "templada": ConjuntoDifuso("templada", triangular(10, 20, 30), (0, 40)),
        "caliente": ConjuntoDifuso("caliente", triangular(20, 30, 40), (0, 40))
    }
    fis.agregar_variable_entrada("temperatura", temp_conjuntos)
    
    # Variable de salida: Velocidad del ventilador
    fan_conjuntos = {
        "baja": ConjuntoDifuso("baja", triangular(0, 25, 50), (0, 100)),
        "media": ConjuntoDifuso("media", triangular(25, 50, 75), (0, 100)),
        "alta": ConjuntoDifuso("alta", triangular(50, 75, 100), (0, 100))
    }
    fis.agregar_variable_salida("ventilador", fan_conjuntos)
    
    # Base de reglas
    fis.agregar_regla("SI temperatura ES fria ENTONCES ventilador ES baja")
    fis.agregar_regla("SI temperatura ES templada ENTONCES ventilador ES media")
    fis.agregar_regla("SI temperatura ES caliente ENTONCES ventilador ES alta")
    
    return fis

def demostrar_control_temperatura():
    """Muestra el funcionamiento del sistema de control"""
    fis = configurar_sistema_temperatura()
    
    # Casos de prueba
    pruebas = [5, 15, 25, 35]
    print("\nResultados del control difuso de temperatura:")
    for temp in pruebas:
        resultado = fis.evaluar({"temperatura": temp})
        print(f"Temperatura: {temp}°C -> Velocidad ventilador: {resultado['ventilador']:.1f}%")
    
    # Visualización de conjuntos
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    for nombre, conjunto in fis.entradas["temperatura"].items():
        conjunto.graficar(ax1)
    ax1.set_title("Conjuntos difusos de temperatura")
    
    for nombre, conjunto in fis.salidas["ventilador"].items():
        conjunto.graficar(ax2)
    ax2.set_title("Conjuntos difusos de velocidad")
    plt.show()

# =============================================================================
# 4. EJEMPLO AVANZADO: SISTEMA DE PROPINAS
# =============================================================================

def configurar_sistema_propinas() -> SistemaInferenciaDifusa:
    """Configura un sistema para calcular propinas basado en servicio y comida"""
    fis = SistemaInferenciaDifusa()
    
    # Variable de entrada: Calidad del servicio (0-10)
    servicio_conjuntos = {
        "pobre": ConjuntoDifuso("pobre", triangular(0, 0, 5), (0, 10)),
        "bueno": ConjuntoDifuso("bueno", triangular(0, 5, 10), (0, 10)),
        "excelente": ConjuntoDifuso("excelente", triangular(5, 10, 10), (0, 10))
    }
    fis.agregar_variable_entrada("servicio", servicio_conjuntos)
    
    # Variable de entrada: Calidad de la comida (0-10)
    comida_conjuntos = {
        "mala": ConjuntoDifuso("mala", triangular(0, 0, 5), (0, 10)),
        "decente": ConjuntoDifuso("decente", triangular(0, 5, 10), (0, 10)),
        "deliciosa": ConjuntoDifuso("deliciosa", triangular(5, 10, 10), (0, 10))
    }
    fis.agregar_variable_entrada("comida", comida_conjuntos)
    
    # Variable de salida: Porcentaje de propina (0-25%)
    propina_conjuntos = {
        "baja": ConjuntoDifuso("baja", triangular(0, 5, 10), (0, 25)),
        "media": ConjuntoDifuso("media", triangular(5, 12.5, 20), (0, 25)),
        "alta": ConjuntoDifuso("alta", triangular(15, 25, 25), (0, 25))
    }
    fis.agregar_variable_salida("propina", propina_conjuntos)
    
    # Base de reglas más compleja
    fis.agregar_regla("SI servicio ES pobre ENTONCES propina ES baja")
    fis.agregar_regla("SI servicio ES bueno ENTONCES propina ES media")
    fis.agregar_regla("SI servicio ES excelente ENTONCES propina ES alta")
    fis.agregar_regla("SI comida ES deliciosa ENTONCES propina ES alta")
    fis.agregar_regla("SI comida ES mala ENTONCES propina ES baja")
    
    return fis

def demostrar_sistema_propinas():
    """Muestra el funcionamiento del sistema de propinas"""
    fis = configurar_sistema_propinas()
    
    # Casos de prueba
    pruebas = [
        {"servicio": 3, "comida": 8},  # Servicio pobre, comida deliciosa
        {"servicio": 7, "comida": 5},  # Servicio bueno, comida decente
        {"servicio": 9, "comida": 2},  # Servicio excelente, comida mala
        {"servicio": 10, "comida": 10}  # Máximas puntuaciones
    ]
    
    print("\nResultados del sistema de propinas:")
    for caso in pruebas:
        resultado = fis.evaluar(caso)
        print(f"Servicio: {caso['servicio']}, Comida: {caso['comida']} -> Propina: {resultado['propina']:.1f}%")

if __name__ == "__main__":
    print("=== SISTEMA DE INFERENCIA DIFUSA ===")
    demostrar_control_temperatura()
    demostrar_sistema_propinas()