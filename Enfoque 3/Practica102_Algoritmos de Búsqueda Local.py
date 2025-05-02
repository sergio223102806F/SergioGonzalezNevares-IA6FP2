# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 14:39:05 2025

@author: elvin
"""

"""
Implementación de Algoritmos de Búsqueda Local para Optimización

Este código incluye:
1. Hill Climbing (Ascenso de Colina)
2. Simulated Annealing (Recocido Simulado)
3. Algoritmo Genético Simple
4. Funciones de evaluación y generación de vecinos
5. Visualización de progreso
"""

import random
import math
import numpy as np
from typing import List, Tuple, Callable, Dict, Optional
import matplotlib.pyplot as plt

class ProblemaOptimizacion:
    """
    Clase base para problemas de optimización.
    
    Atributos:
        dominio (Tuple[float, float]): Rango de valores para las variables
        dimension (int): Número de variables del problema
    """
    def __init__(self, dominio: Tuple[float, float] = (-10, 10), dimension: int = 2):
        self.dominio = dominio
        self.dimension = dimension
    
    def evaluar(self, solucion: List[float]) -> float:
        """
        Evalúa una solución (a implementar por subclases).
        
        Args:
            solucion: Lista de valores de las variables
            
        Returns:
            float: Valor de la función objetivo
        """
        raise NotImplementedError("Método abstracto")
    
    def generar_vecino(self, solucion: List[float], paso: float = 0.1) -> List[float]:
        """
        Genera una solución vecina.
        
        Args:
            solucion: Solución actual
            paso: Tamaño del paso para modificar la solución
            
        Returns:
            List[float]: Nueva solución vecina
        """
        vecino = solucion.copy()
        indice = random.randint(0, self.dimension - 1)
        cambio = random.uniform(-paso, paso)
        vecino[indice] += cambio
        
        # Asegurar que se mantenga dentro del dominio
        vecino[indice] = max(self.dominio[0], min(self.dominio[1], vecino[indice]))
        return vecino
    
    def solucion_aleatoria(self) -> List[float]:
        """Genera una solución aleatoria dentro del dominio."""
        return [random.uniform(self.dominio[0], self.dominio[1]) 
                for _ in range(self.dimension)]

class ProblemaAckley(ProblemaOptimizacion):
    """
    Implementa la función de Ackley, común para probar algoritmos de optimización.
    Mínimo global en (0, 0) con valor 0.
    """
    def evaluar(self, solucion: List[float]) -> float:
        a = 20
        b = 0.2
        c = 2 * math.pi
        sum1 = sum(x**2 for x in solucion)
        sum2 = sum(math.cos(c * x) for x in solucion)
        n = len(solucion)
        
        term1 = -a * math.exp(-b * math.sqrt(sum1 / n))
        term2 = -math.exp(sum2 / n)
        return term1 + term2 + a + math.exp(1)

class BusquedaLocal:
    """
    Clase base para algoritmos de búsqueda local.
    
    Atributos:
        problema: Instancia del problema de optimización
        max_iter (int): Máximo número de iteraciones
        historial (List[float]): Registro de mejores valores por iteración
    """
    def __init__(self, problema: ProblemaOptimizacion, max_iter: int = 1000):
        self.problema = problema
        self.max_iter = max_iter
        self.historial = []
    
    def resolver(self) -> List[float]:
        """
        Método principal para resolver el problema (a implementar por subclases).
        
        Returns:
            List[float]: Mejor solución encontrada
        """
        raise NotImplementedError("Método abstracto")
    
    def graficar_progreso(self, titulo: str = "Progreso de la Búsqueda") -> None:
        """Muestra una gráfica del progreso del algoritmo."""
        plt.figure(figsize=(10, 6))
        plt.plot(self.historial, 'b-', linewidth=1)
        plt.title(titulo)
        plt.xlabel("Iteración")
        plt.ylabel("Valor de la Función Objetivo")
        plt.grid(True)
        plt.show()

class HillClimbing(BusquedaLocal):
    """
    Implementa el algoritmo de Hill Climbing (Ascenso de Colina).
    
    Atributos adicionales:
        paso_inicial (float): Tamaño inicial del paso para generar vecinos
        reduccion_paso (float): Factor para reducir el paso en cada iteración
    """
    def __init__(self, problema: ProblemaOptimizacion, max_iter: int = 1000,
                 paso_inicial: float = 0.5, reduccion_paso: float = 0.99):
        super().__init__(problema, max_iter)
        self.paso_inicial = paso_inicial
        self.reduccion_paso = reduccion_paso
    
    def resolver(self) -> List[float]:
        """Implementación del algoritmo Hill Climbing."""
        # Generar solución inicial aleatoria
        solucion_actual = self.problema.solucion_aleatoria()
        valor_actual = self.problema.evaluar(solucion_actual)
        self.historial.append(valor_actual)
        
        paso = self.paso_inicial
        
        for iteracion in range(self.max_iter):
            # Generar vecino y evaluarlo
            vecino = self.problema.generar_vecino(solucion_actual, paso)
            valor_vecino = self.problema.evaluar(vecino)
            
            # Si el vecino es mejor, movernos a él
            if valor_vecino < valor_actual:  # Minimización
                solucion_actual = vecino
                valor_actual = valor_vecino
            
            # Reducir el tamaño del paso
            paso *= self.reduccion_paso
            
            # Registrar el mejor valor
            self.historial.append(valor_actual)
        
        return solucion_actual

class SimulatedAnnealing(BusquedaLocal):
    """
    Implementa el algoritmo de Simulated Annealing (Recocido Simulado).
    
    Atributos adicionales:
        temperatura_inicial (float): Temperatura inicial
        enfriamiento (float): Tasa de enfriamiento
        paso_inicial (float): Tamaño inicial del paso
    """
    def __init__(self, problema: ProblemaOptimizacion, max_iter: int = 1000,
                 temperatura_inicial: float = 100.0, enfriamiento: float = 0.95,
                 paso_inicial: float = 0.5):
        super().__init__(problema, max_iter)
        self.temperatura_inicial = temperatura_inicial
        self.enfriamiento = enfriamiento
        self.paso_inicial = paso_inicial
    
    def resolver(self) -> List[float]:
        """Implementación del algoritmo Simulated Annealing."""
        # Generar solución inicial aleatoria
        solucion_actual = self.problema.solucion_aleatoria()
        valor_actual = self.problema.evaluar(solucion_actual)
        self.historial.append(valor_actual)
        
        mejor_solucion = solucion_actual.copy()
        mejor_valor = valor_actual
        
        temperatura = self.temperatura_inicial
        paso = self.paso_inicial
        
        for iteracion in range(self.max_iter):
            # Generar vecino y evaluarlo
            vecino = self.problema.generar_vecino(solucion_actual, paso)
            valor_vecino = self.problema.evaluar(vecino)
            
            # Calcular diferencia y probabilidad de aceptación
            delta = valor_vecino - valor_actual
            probabilidad = math.exp(-delta / temperatura) if temperatura > 0 else 0
            
            # Aceptar el vecino si es mejor o con cierta probabilidad si es peor
            if delta < 0 or random.random() < probabilidad:
                solucion_actual = vecino
                valor_actual = valor_vecino
                
                # Actualizar la mejor solución encontrada
                if valor_actual < mejor_valor:
                    mejor_solucion = solucion_actual.copy()
                    mejor_valor = valor_actual
            
            # Enfriar el sistema
            temperatura *= self.enfriamiento
            paso *= self.enfriamiento  # También reducimos el paso
            
            # Registrar el mejor valor
            self.historial.append(mejor_valor)
        
        return mejor_solucion

class AlgoritmoGenetico(BusquedaLocal):
    """
    Implementa un algoritmo genético simple.
    
    Atributos adicionales:
        tam_poblacion (int): Tamaño de la población
        prob_mutacion (float): Probabilidad de mutación
        prob_cruce (float): Probabilidad de cruce
    """
    def __init__(self, problema: ProblemaOptimizacion, max_iter: int = 100,
                 tam_poblacion: int = 50, prob_mutacion: float = 0.1,
                 prob_cruce: float = 0.7):
        super().__init__(problema, max_iter)
        self.tam_poblacion = tam_poblacion
        self.prob_mutacion = prob_mutacion
        self.prob_cruce = prob_cruce
    
    def inicializar_poblacion(self) -> List[List[float]]:
        """Genera una población inicial aleatoria."""
        return [self.problema.solucion_aleatoria() 
                for _ in range(self.tam_poblacion)]
    
    def seleccionar(self, poblacion: List[List[float]], valores: List[float]) -> List[List[float]]:
        """Selección por torneo binario."""
        seleccionados = []
        for _ in range(self.tam_poblacion):
            # Escoger dos individuos al azar
            i, j = random.sample(range(self.tam_poblacion), 2)
            
            # Seleccionar el mejor (minimización)
            ganador = poblacion[i] if valores[i] < valores[j] else poblacion[j]
            seleccionados.append(ganador)
        
        return seleccionados
    
    def cruzar(self, padre1: List[float], padre2: List[float]) -> Tuple[List[float], List[float]]:
        """Cruce por recombinación aritmética."""
        if random.random() > self.prob_cruce:
            return padre1.copy(), padre2.copy()
        
        alpha = random.random()
        hijo1 = [alpha * x + (1 - alpha) * y for x, y in zip(padre1, padre2)]
        hijo2 = [(1 - alpha) * x + alpha * y for x, y in zip(padre1, padre2)]
        return hijo1, hijo2
    
    def mutar(self, individuo: List[float]) -> List[float]:
        """Mutación gaussiana."""
        if random.random() > self.prob_mutacion:
            return individuo.copy()
        
        mutado = individuo.copy()
        indice = random.randint(0, self.problema.dimension - 1)
        mutado[indice] += random.gauss(0, 0.1)
        
        # Asegurar que se mantenga dentro del dominio
        mutado[indice] = max(self.problema.dominio[0], 
                            min(self.problema.dominio[1], mutado[indice]))
        return mutado
    
    def resolver(self) -> List[float]:
        """Implementación del algoritmo genético."""
        # Inicializar población
        poblacion = self.inicializar_poblacion()
        valores = [self.problema.evaluar(ind) for ind in poblacion]
        mejor_valor = min(valores)
        self.historial.append(mejor_valor)
        
        for iteracion in range(self.max_iter):
            # Selección
            seleccionados = self.seleccionar(poblacion, valores)
            
            # Cruce
            nueva_poblacion = []
            for i in range(0, self.tam_poblacion, 2):
                hijo1, hijo2 = self.cruzar(seleccionados[i], seleccionados[i+1])
                nueva_poblacion.extend([hijo1, hijo2])
            
            # Mutación
            poblacion = [self.mutar(ind) for ind in nueva_poblacion]
            
            # Evaluación
            valores = [self.problema.evaluar(ind) for ind in poblacion]
            mejor_valor = min(valores)
            self.historial.append(mejor_valor)
        
        # Devolver el mejor individuo encontrado
        mejor_indice = valores.index(min(valores))
        return poblacion[mejor_indice]

def comparar_algoritmos(problema: ProblemaOptimizacion, n_ejecuciones: int = 10) -> Dict[str, float]:
    """
    Compara el rendimiento de diferentes algoritmos de búsqueda local.
    
    Args:
        problema: Problema de optimización a resolver
        n_ejecuciones: Número de ejecuciones para promediar resultados
        
    Returns:
        Dict[str, float]: Diccionario con los mejores valores encontrados por cada algoritmo
    """
    resultados = {
        'Hill Climbing': [],
        'Simulated Annealing': [],
        'Algoritmo Genético': []
    }
    
    for _ in range(n_ejecuciones):
        # Hill Climbing
        hc = HillClimbing(problema)
        sol_hc = hc.resolver()
        resultados['Hill Climbing'].append(problema.evaluar(sol_hc))
        
        # Simulated Annealing
        sa = SimulatedAnnealing(problema)
        sol_sa = sa.resolver()
        resultados['Simulated Annealing'].append(problema.evaluar(sol_sa))
        
        # Algoritmo Genético
        ag = AlgoritmoGenetico(problema)
        sol_ag = ag.resolver()
        resultados['Algoritmo Genético'].append(problema.evaluar(sol_ag))
    
    # Calcular promedios
    return {algo: sum(vals)/n_ejecuciones for algo, vals in resultados.items()}

# Ejemplo de uso
if __name__ == "__main__":
    print("COMPARACIÓN DE ALGORITMOS DE BÚSQUEDA LOCAL")
    print("=" * 50)
    
    # Crear problema de optimización (Ackley en 2D)
    problema = ProblemaAckley(dominio=(-5, 5), dimension=2)
    
    # 1. Ejemplo individual con Hill Climbing
    print("\nEjecutando Hill Climbing...")
    hc = HillClimbing(problema, max_iter=1000)
    sol_hc = hc.resolver()
    print(f"Mejor solución encontrada: {sol_hc}")
    print(f"Valor de la función: {problema.evaluar(sol_hc):.4f}")
    hc.graficar_progreso("Progreso de Hill Climbing")
    
    # 2. Ejemplo individual con Simulated Annealing
    print("\nEjecutando Simulated Annealing...")
    sa = SimulatedAnnealing(problema, max_iter=1000)
    sol_sa = sa.resolver()
    print(f"Mejor solución encontrada: {sol_sa}")
    print(f"Valor de la función: {problema.evaluar(sol_sa):.4f}")
    sa.graficar_progreso("Progreso de Simulated Annealing")
    
    # 3. Ejemplo individual con Algoritmo Genético
    print("\nEjecutando Algoritmo Genético...")
    ag = AlgoritmoGenetico(problema, max_iter=100)
    sol_ag = ag.resolver()
    print(f"Mejor solución encontrada: {sol_ag}")
    print(f"Valor de la función: {problema.evaluar(sol_ag):.4f}")
    ag.graficar_progreso("Progreso del Algoritmo Genético")
    
    # 4. Comparación estadística
    print("\nComparando algoritmos...")
    resultados = comparar_algoritmos(problema, n_ejecuciones=5)
    
    print("\nResultados promedio (minimización):")
    for algoritmo, valor in resultados.items():
        print(f"{algoritmo}: {valor:.4f}")
    
    # Visualización comparativa
    plt.figure(figsize=(10, 6))
    plt.bar(resultados.keys(), resultados.values(), color=['blue', 'green', 'red'])
    plt.title("Comparación de Algoritmos de Búsqueda Local")
    plt.ylabel("Valor promedio de la función objetivo")
    plt.grid(True, axis='y')
    plt.show()