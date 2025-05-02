# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 16:26:20 2025

@author: elvin
"""

"""
Implementación de un sistema híbrido que combina:
- Reglas difusas estilo CLIPS
- Motor de inferencia difusa
- Base de hechos tradicional y difusa
"""

from typing import Dict, List, Tuple, Set, Callable, Union
import numpy as np

# =============================================================================
# 1. DEFINICIÓN DE LOS COMPONENTES BÁSICOS
# =============================================================================

class Hecho:
    """Representa un hecho en la base de conocimiento"""
    def __init__(self, nombre: str, valor: Union[float, str, bool]):
        self.nombre = nombre
        self.valor = valor
    
    def __repr__(self):
        return f"({self.nombre} {self.valor})"

class ConjuntoDifuso:
    """Define un conjunto difuso con su función de pertenencia"""
    def __init__(self, nombre: str, funcion: Callable[[float], float]):
        self.nombre = nombre
        self.funcion = funcion
    
    def pertenencia(self, x: float) -> float:
        """Calcula el grado de pertenencia para un valor x"""
        return self.funcion(x)

# Funciones de pertenencia predefinidas
def triangular(a: float, b: float, c: float) -> Callable[[float], float]:
    """Crea una función de pertenencia triangular"""
    return lambda x: max(min((x-a)/(b-a), (c-x)/(c-b)), 0)

def trapezoidal(a: float, b: float, c: float, d: float) -> Callable[[float], float]:
    """Crea una función de pertenencia trapezoidal"""
    return lambda x: max(min((x-a)/(b-a), 1, (d-x)/(d-c)), 0)

# =============================================================================
# 2. MOTOR DE INFERENCIA HÍBRIDO
# =============================================================================

class FuzzyCLIPS:
    """
    Sistema híbrido que combina:
    - Base de hechos tradicional (como CLIPS)
    - Variables difusas con conjuntos difusos
    - Motor de reglas que maneja tanto lógica clásica como difusa
    """
    
    def __init__(self):
        # Base de hechos tradicional
        self.hechos: Set[Hecho] = set()
        
        # Variables difusas y sus conjuntos
        self.variables_difusas: Dict[str, Dict[str, ConjuntoDifuso]] = {}
        
        # Reglas del sistema (parte izquierda y derecha)
        self.reglas: List[Tuple[List[str], List[str]]] = []
        
        # Parámetros del sistema
        self.umbral_activacion: float = 0.5
    
    def agregar_hecho(self, hecho: Hecho):
        """Añade un hecho a la base de conocimiento"""
        self.hechos.add(hecho)
    
    def definir_variable_difusa(self, nombre: str, conjuntos: Dict[str, ConjuntoDifuso]):
        """Registra una variable difusa con sus conjuntos"""
        self.variables_difusas[nombre] = conjuntos
    
    def agregar_regla(self, antecedente: List[str], consecuente: List[str]):
        """
        Añade una regla al sistema
        
        Args:
            antecedente: Lista de condiciones (pueden ser difusas o booleanas)
            consecuente: Lista de acciones/conclusiones
        """
        self.reglas.append((antecedente, consecuente))
    
    def fuzzificar(self, variable: str, valor: float) -> Dict[str, float]:
        """
        Convierte un valor nítido en grados de pertenencia para cada conjunto
        
        Args:
            variable: Nombre de la variable difusa
            valor: Valor nítido a fuzzificar
            
        Returns:
            Diccionario {conjunto: grado_pertenencia}
        """
        if variable not in self.variables_difusas:
            raise ValueError(f"Variable difusa no definida: {variable}")
        
        return {
            nombre: conjunto.pertenencia(valor)
            for nombre, conjunto in self.variables_difusas[variable].items()
        }
    
    def evaluar_condicion(self, condicion: str) -> float:
        """
        Evalúa una condición individual, puede ser:
        - Hecho booleano tradicional
        - Condición difusa
        - Comparación numérica
        """
        # Caso 1: Hecho booleano tradicional (ej. "(hecho verdadero)")
        if condicion.startswith("(") and condicion.endswith(")"):
            nombre, valor = condicion[1:-1].split()
            for hecho in self.hechos:
                if hecho.nombre == nombre and str(hecho.valor) == valor:
                    return 1.0
            return 0.0
        
        # Caso 2: Condición difusa (ej. "temperatura ES caliente")
        elif " ES " in condicion:
            variable, _, conjunto = condicion.partition(" ES ")
            if variable in self.variables_difusas and conjunto in self.variables_difusas[variable]:
                # Esto sería reemplazado por el valor actual de la variable
                # En una implementación real necesitaríamos el valor actual
                return 0.5  # Valor de ejemplo
            else:
                return 0.0
        
        # Caso 3: Comparación numérica (ej. "valor > 10")
        elif ">" in condicion:
            var, val = condicion.split(">")
            # Implementación simplificada
            return 1.0 if float(var) > float(val) else 0.0
        elif "<" in condicion:
            var, val = condicion.split("<")
            return 1.0 if float(var) < float(val) else 0.0
        
        return 0.0
    
    def ejecutar(self):
        """Ejecuta el ciclo de inferencia del sistema"""
        for antecedente, consecuente in self.reglas:
            # Evaluar todas las condiciones del antecedente
            activacion = 1.0
            for cond in antecedente:
                grado = self.evaluar_condicion(cond)
                activacion = min(activacion, grado)
                if activacion == 0:
                    break  # No point continuing if any condition fails
            
            # Si la activación supera el umbral, ejecutar consecuente
            if activacion >= self.umbral_activacion:
                self.ejecutar_consecuente(consecuente, activacion)
    
    def ejecutar_consecuente(self, acciones: List[str], grado_activacion: float):
        """
        Ejecuta las acciones de la parte derecha de una regla
        
        Args:
            acciones: Lista de acciones a ejecutar
            grado_activacion: Grado con el que se activó la regla
        """
        for accion in acciones:
            # Caso 1: Añadir hecho tradicional
            if accion.startswith("(assert ") and accion.endswith(")"):
                hecho_str = accion[8:-1]
                nombre, valor = hecho_str.split()
                self.agregar_hecho(Hecho(nombre, valor))
            
            # Caso 2: Modificar variable difusa (simplificado)
            elif " ES " in accion:
                variable, _, conjunto = accion.partition(" ES ")
                print(f"Establecer {variable} a {conjunto} con grado {grado_activacion}")
            
            # Otros casos podrían incluir acciones de salida, etc.
            else:
                print(f"Ejecutando acción: {accion}")

# =============================================================================
# 3. EJEMPLOS DE USO
# =============================================================================

def ejemplo_control_clima():
    """Sistema de control climático híbrido"""
    sistema = FuzzyCLIPS()
    
    # 1. Definir variables difusas
    temperatura_conjuntos = {
        "fria": ConjuntoDifuso("fria", triangular(0, 10, 20)),
        "templada": ConjuntoDifuso("templada", triangular(10, 20, 30)),
        "caliente": ConjuntoDifuso("caliente", triangular(20, 30, 40))
    }
    sistema.definir_variable_difusa("temperatura", temperatura_conjuntos)
    
    humedad_conjuntos = {
        "baja": ConjuntoDifuso("baja", triangular(0, 30, 60)),
        "media": ConjuntoDifuso("media", triangular(30, 60, 90)),
        "alta": ConjuntoDifuso("alta", triangular(60, 90, 100))
    }
    sistema.definir_variable_difusa("humedad", humedad_conjuntos)
    
    # 2. Añadir hechos tradicionales
    sistema.agregar_hecho(Hecho("modo", "verano"))
    sistema.agregar_hecho(Hecho("ventanas", "cerradas"))
    
    # 3. Definir reglas híbridas
    sistema.agregar_regla(
        ["(modo verano)", "temperatura ES caliente", "humedad ES alta"],
        ["(assert ventanas abiertas)", "activar ventilador"]
    )
    
    sistema.agregar_regla(
        ["(modo invierno)", "temperatura ES fria"],
        ["(assert ventanas cerradas)", "activar calefaccion"]
    )
    
    # 4. Ejecutar el sistema (simulación)
    print("\nEjecutando sistema de control climático...")
    sistema.ejecutar()

def ejemplo_diagnostico_medico():
    """Sistema de diagnóstico médico con componentes difusos y booleanos"""
    sistema = FuzzyCLIPS()
    
    # 1. Definir variables difusas para síntomas
    fiebre_conjuntos = {
        "leve": ConjuntoDifuso("leve", triangular(36, 37, 38)),
        "moderada": ConjuntoDifuso("moderada", triangular(37, 38, 39)),
        "alta": ConjuntoDifuso("alta", triangular(38, 39, 42))
    }
    sistema.definir_variable_difusa("fiebre", fiebre_conjuntos)
    
    # 2. Hechos tradicionales
    sistema.agregar_hecho(Hecho("vacunado", True))
    sistema.agregar_hecho(Hecho("contacto_con_infectado", False))
    
    # 3. Reglas de diagnóstico
    sistema.agregar_regla(
        ["(contacto_con_infectado verdadero)", "fiebre ES alta"],
        ["(assert posible_covid verdadero)", "recomendar prueba PCR"]
    )
    
    sistema.agregar_regla(
        ["(vacunado verdadero)", "fiebre ES moderada"],
        ["(assert posible_covid falso)", "recomendar observacion"]
    )
    
    # 4. Ejecutar el sistema
    print("\nEjecutando sistema de diagnóstico médico...")
    sistema.ejecutar()

if __name__ == "__main__":
    print("=== SISTEMA FUZZY CLIPS DEMOSTRACIÓN ===")
    ejemplo_control_clima()
    ejemplo_diagnostico_medico()