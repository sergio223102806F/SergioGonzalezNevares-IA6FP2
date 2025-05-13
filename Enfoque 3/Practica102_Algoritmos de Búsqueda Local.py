# -*- coding: utf-8 -*-  # Especifica la codificación del archivo como UTF-8
"""
Created on Sun Apr 27 14:39:05 2025  # Fecha de creación del archivo

@author: elvin  # Autor del código
"""

"""
Implementación de Algoritmos de Búsqueda Local para Optimización  # Descripción general

Este código incluye:  # Lista de funcionalidades
1. Hill Climbing (Ascenso de Colina)  # Algoritmo de ascenso de colina
2. Simulated Annealing (Recocido Simulado)  # Algoritmo de recocido simulado
3. Algoritmo Genético Simple  # Algoritmo genético básico
4. Funciones de evaluación y generación de vecinos  # Operaciones auxiliares
5. Visualización de progreso  # Gráficas de convergencia
"""

import random  # Para generación de números aleatorios
import math  # Para funciones matemáticas
import numpy as np  # Para operaciones numéricas (no usado directamente)
from typing import List, Tuple, Callable, Dict, Optional  # Para type hints
import matplotlib.pyplot as plt  # Para visualización

class ProblemaOptimizacion:
    """
    Clase base para problemas de optimización.
    
    Atributos:
        dominio (Tuple[float, float]): Rango de valores para las variables  # Límites del dominio
        dimension (int): Número de variables del problema  # Dimensionalidad
    """
    def __init__(self, dominio: Tuple[float, float] = (-10, 10), dimension: int = 2):  # Constructor
        self.dominio = dominio  # Asigna rango de valores
        self.dimension = dimension  # Asigna número de variables
    
    def evaluar(self, solucion: List[float]) -> float:  # Método abstracto
        """
        Evalúa una solución (a implementar por subclases).
        
        Args:
            solucion: Lista de valores de las variables  # Punto a evaluar
            
        Returns:
            float: Valor de la función objetivo  # Valor de fitness/costo
        """
        raise NotImplementedError("Método abstracto")  # Las subclases deben implementar
    
    def generar_vecino(self, solucion: List[float], paso: float = 0.1) -> List[float]:  # Generación de vecinos
        """
        Genera una solución vecina.
        
        Args:
            solucion: Solución actual  # Punto actual
            paso: Tamaño del paso para modificar la solución  # Magnitud de perturbación
            
        Returns:
            List[float]: Nueva solución vecina  # Punto cercano
        """
        vecino = solucion.copy()  # Copia la solución actual
        indice = random.randint(0, self.dimension - 1)  # Elige una dimensión al azar
        cambio = random.uniform(-paso, paso)  # Genera cambio aleatorio
        vecino[indice] += cambio  # Aplica el cambio
        
        # Asegurar que se mantenga dentro del dominio  # Restricción de límites
        vecino[indice] = max(self.dominio[0], min(self.dominio[1], vecino[indice]))
        return vecino
    
    def solucion_aleatoria(self) -> List[float]:  # Generación de solución inicial
        """Genera una solución aleatoria dentro del dominio."""
        return [random.uniform(self.dominio[0], self.dominio[1])  # Valor aleatorio en rango
                for _ in range(self.dimension)]  # Para cada dimensión

class ProblemaAckley(ProblemaOptimizacion):
    """
    Implementa la función de Ackley, común para probar algoritmos de optimización.
    Mínimo global en (0, 0) con valor 0.
    """
    def evaluar(self, solucion: List[float]) -> float:  # Implementación de Ackley
        a = 20  # Parámetro de la función
        b = 0.2  # Parámetro de la función
        c = 2 * math.pi  # Parámetro de la función
        sum1 = sum(x**2 for x in solucion)  # Suma de cuadrados
        sum2 = sum(math.cos(c * x) for x in solucion)  # Suma de cosenos
        n = len(solucion)  # Dimensionalidad
        
        term1 = -a * math.exp(-b * math.sqrt(sum1 / n))  # Primer término
        term2 = -math.exp(sum2 / n)  # Segundo término
        return term1 + term2 + a + math.exp(1)  # Combinación de términos

class BusquedaLocal:
    """
    Clase base para algoritmos de búsqueda local.
    
    Atributos:
        problema: Instancia del problema de optimización  # Problema a resolver
        max_iter (int): Máximo número de iteraciones  # Límite de iteraciones
        historial (List[float]): Registro de mejores valores por iteración  # Traza de ejecución
    """
    def __init__(self, problema: ProblemaOptimizacion, max_iter: int = 1000):  # Constructor
        self.problema = problema  # Asigna problema
        self.max_iter = max_iter  # Asigna máximo de iteraciones
        self.historial = []  # Inicializa historial vacío
    
    def resolver(self) -> List[float]:  # Método abstracto
        """
        Método principal para resolver el problema (a implementar por subclases).
        
        Returns:
            List[float]: Mejor solución encontrada  # Mejor punto encontrado
        """
        raise NotImplementedError("Método abstracto")  # Subclases deben implementar
    
    def graficar_progreso(self, titulo: str = "Progreso de la Búsqueda") -> None:  # Visualización
        """Muestra una gráfica del progreso del algoritmo."""
        plt.figure(figsize=(10, 6))  # Crea figura
        plt.plot(self.historial, 'b-', linewidth=1)  # Grafica historial
        plt.title(titulo)  # Añade título
        plt.xlabel("Iteración")  # Etiqueta eje X
        plt.ylabel("Valor de la Función Objetivo")  # Etiqueta eje Y
        plt.grid(True)  # Añade cuadrícula
        plt.show()  # Muestra gráfica

class HillClimbing(BusquedaLocal):
    """
    Implementa el algoritmo de Hill Climbing (Ascenso de Colina).
    
    Atributos adicionales:
        paso_inicial (float): Tamaño inicial del paso para generar vecinos  # Tamaño de paso inicial
        reduccion_paso (float): Factor para reducir el paso en cada iteración  # Tasa de reducción
    """
    def __init__(self, problema: ProblemaOptimizacion, max_iter: int = 1000,
                 paso_inicial: float = 0.5, reduccion_paso: float = 0.99):  # Constructor
        super().__init__(problema, max_iter)  # Llama al constructor padre
        self.paso_inicial = paso_inicial  # Asigna paso inicial
        self.reduccion_paso = reduccion_paso  # Asigna tasa de reducción
    
    def resolver(self) -> List[float]:  # Implementación de Hill Climbing
        """Implementación del algoritmo Hill Climbing."""
        # Generar solución inicial aleatoria
        solucion_actual = self.problema.solucion_aleatoria()  # Solución inicial
        valor_actual = self.problema.evaluar(solucion_actual)  # Evalúa solución
        self.historial.append(valor_actual)  # Registra valor inicial
        
        paso = self.paso_inicial  # Inicializa tamaño de paso
        
        for iteracion in range(self.max_iter):  # Bucle principal
            # Generar vecino y evaluarlo
            vecino = self.problema.generar_vecino(solucion_actual, paso)  # Genera vecino
            valor_vecino = self.problema.evaluar(vecino)  # Evalúa vecino
            
            # Si el vecino es mejor, movernos a él (minimización)
            if valor_vecino < valor_actual:  # Comparación
                solucion_actual = vecino  # Actualiza solución
                valor_actual = valor_vecino  # Actualiza valor
            
            # Reducir el tamaño del paso (enfriamiento adaptativo)
            paso *= self.reduccion_paso  # Reduce paso
            
            # Registrar el mejor valor
            self.historial.append(valor_actual)  # Añade a historial
        
        return solucion_actual  # Devuelve mejor solución encontrada

class SimulatedAnnealing(BusquedaLocal):
    """
    Implementa el algoritmo de Simulated Annealing (Recocido Simulado).
    
    Atributos adicionales:
        temperatura_inicial (float): Temperatura inicial  # Temp. inicial del sistema
        enfriamiento (float): Tasa de enfriamiento  # Factor de enfriamiento
        paso_inicial (float): Tamaño inicial del paso  # Tamaño de paso inicial
    """
    def __init__(self, problema: ProblemaOptimizacion, max_iter: int = 1000,
                 temperatura_inicial: float = 100.0, enfriamiento: float = 0.95,
                 paso_inicial: float = 0.5):  # Constructor
        super().__init__(problema, max_iter)  # Llama al constructor padre
        self.temperatura_inicial = temperatura_inicial  # Asigna temperatura inicial
        self.enfriamiento = enfriamiento  # Asigna tasa de enfriamiento
        self.paso_inicial = paso_inicial  # Asigna paso inicial
    
    def resolver(self) -> List[float]:  # Implementación de Simulated Annealing
        """Implementación del algoritmo Simulated Annealing."""
        # Generar solución inicial aleatoria
        solucion_actual = self.problema.solucion_aleatoria()  # Solución inicial
        valor_actual = self.problema.evaluar(solucion_actual)  # Evalúa solución
        self.historial.append(valor_actual)  # Registra valor inicial
        
        mejor_solucion = solucion_actual.copy()  # Inicializa mejor solución
        mejor_valor = valor_actual  # Inicializa mejor valor
        
        temperatura = self.temperatura_inicial  # Inicializa temperatura
        paso = self.paso_inicial  # Inicializa paso
        
        for iteracion in range(self.max_iter):  # Bucle principal
            # Generar vecino y evaluarlo
            vecino = self.problema.generar_vecino(solucion_actual, paso)  # Genera vecino
            valor_vecino = self.problema.evaluar(vecino)  # Evalúa vecino
            
            # Calcular diferencia y probabilidad de aceptación
            delta = valor_vecino - valor_actual  # Calcula diferencia
            probabilidad = math.exp(-delta / temperatura) if temperatura > 0 else 0  # Prob. de aceptación
            
            # Aceptar el vecino si es mejor o con cierta probabilidad si es peor
            if delta < 0 or random.random() < probabilidad:  # Criterio de aceptación
                solucion_actual = vecino  # Actualiza solución
                valor_actual = valor_vecino  # Actualiza valor
                
                # Actualizar la mejor solución encontrada
                if valor_actual < mejor_valor:  # Comparación
                    mejor_solucion = solucion_actual.copy()  # Copia mejor solución
                    mejor_valor = valor_actual  # Actualiza mejor valor
            
            # Enfriar el sistema (reducir temperatura y paso)
            temperatura *= self.enfriamiento  # Reduce temperatura
            paso *= self.enfriamiento  # Reduce paso
            
            # Registrar el mejor valor
            self.historial.append(mejor_valor)  # Añade a historial
        
        return mejor_solucion  # Devuelve mejor solución encontrada

class AlgoritmoGenetico(BusquedaLocal):
    """
    Implementa un algoritmo genético simple.
    
    Atributos adicionales:
        tam_poblacion (int): Tamaño de la población  # Número de individuos
        prob_mutacion (float): Probabilidad de mutación  # Tasa de mutación
        prob_cruce (float): Probabilidad de cruce  # Tasa de cruce
    """
    def __init__(self, problema: ProblemaOptimizacion, max_iter: int = 100,
                 tam_poblacion: int = 50, prob_mutacion: float = 0.1,
                 prob_cruce: float = 0.7):  # Constructor
        super().__init__(problema, max_iter)  # Llama al constructor padre
        self.tam_poblacion = tam_poblacion  # Asigna tamaño de población
        self.prob_mutacion = prob_mutacion  # Asigna probabilidad de mutación
        self.prob_cruce = prob_cruce  # Asigna probabilidad de cruce
    
    def inicializar_poblacion(self) -> List[List[float]]:  # Inicialización
        """Genera una población inicial aleatoria."""
        return [self.problema.solucion_aleatoria()  # Solución aleatoria
                for _ in range(self.tam_poblacion)]  # Para cada individuo
    
    def seleccionar(self, poblacion: List[List[float]], valores: List[float]) -> List[List[float]]:  # Selección
        """Selección por torneo binario."""
        seleccionados = []  # Lista para padres seleccionados
        for _ in range(self.tam_poblacion):  # Para cada individuo a seleccionar
            # Escoger dos individuos al azar
            i, j = random.sample(range(self.tam_poblacion), 2)  # Dos índices aleatorios
            
            # Seleccionar el mejor (minimización)
            ganador = poblacion[i] if valores[i] < valores[j] else poblacion[j]  # Torneo
            seleccionados.append(ganador)  # Añade a seleccionados
        
        return seleccionados  # Devuelve padres seleccionados
    
    def cruzar(self, padre1: List[float], padre2: List[float]) -> Tuple[List[float], List[float]]:  # Cruce
        """Cruce por recombinación aritmética."""
        if random.random() > self.prob_cruce:  # Si no hay cruce
            return padre1.copy(), padre2.copy()  # Devuelve copias de padres
        
        alpha = random.random()  # Factor de mezcla aleatorio
        hijo1 = [alpha * x + (1 - alpha) * y for x, y in zip(padre1, padre2)]  # Combinación lineal
        hijo2 = [(1 - alpha) * x + alpha * y for x, y in zip(padre1, padre2)]  # Combinación lineal inversa
        return hijo1, hijo2  # Devuelve descendientes
    
    def mutar(self, individuo: List[float]) -> List[float]:  # Mutación
        """Mutación gaussiana."""
        if random.random() > self.prob_mutacion:  # Si no hay mutación
            return individuo.copy()  # Devuelve copia
        
        mutado = individuo.copy()  # Copia el individuo
        indice = random.randint(0, self.problema.dimension - 1)  # Elige gen a mutar
        mutado[indice] += random.gauss(0, 0.1)  # Aplica mutación gaussiana
        
        # Asegurar que se mantenga dentro del dominio  # Restricción de límites
        mutado[indice] = max(self.problema.dominio[0], 
                            min(self.problema.dominio[1], mutado[indice]))
        return mutado  # Devuelve individuo mutado
    
    def resolver(self) -> List[float]:  # Implementación de Algoritmo Genético
        """Implementación del algoritmo genético."""
        # Inicializar población
        poblacion = self.inicializar_poblacion()  # Genera población inicial
        valores = [self.problema.evaluar(ind) for ind in poblacion]  # Evalúa población
        mejor_valor = min(valores)  # Encuentra mejor valor
        self.historial.append(mejor_valor)  # Registra valor inicial
        
        for iteracion in range(self.max_iter):  # Bucle principal
            # Selección
            seleccionados = self.seleccionar(poblacion, valores)  # Selecciona padres
            
            # Cruce
            nueva_poblacion = []  # Lista para nueva generación
            for i in range(0, self.tam_poblacion, 2):  # Por pares
                hijo1, hijo2 = self.cruzar(seleccionados[i], seleccionados[i+1])  # Cruza
                nueva_poblacion.extend([hijo1, hijo2])  # Añade descendientes
            
            # Mutación
            poblacion = [self.mutar(ind) for ind in nueva_poblacion]  # Aplica mutaciones
            
            # Evaluación
            valores = [self.problema.evaluar(ind) for ind in poblacion]  # Evalúa nueva población
            mejor_valor = min(valores)  # Encuentra mejor valor
            self.historial.append(mejor_valor)  # Registra mejor valor
        
        # Devolver el mejor individuo encontrado
        mejor_indice = valores.index(min(valores))  # Índice del mejor
        return poblacion[mejor_indice]  # Devuelve mejor solución

def comparar_algoritmos(problema: ProblemaOptimizacion, n_ejecuciones: int = 10) -> Dict[str, float]:  # Comparación
    """
    Compara el rendimiento de diferentes algoritmos de búsqueda local.
    
    Args:
        problema: Problema de optimización a resolver  # Problema a evaluar
        n_ejecuciones: Número de ejecuciones para promediar resultados  # Repeticiones
        
    Returns:
        Dict[str, float]: Diccionario con los mejores valores encontrados por cada algoritmo  # Resultados
    """
    resultados = {  # Diccionario para resultados
        'Hill Climbing': [],
        'Simulated Annealing': [],
        'Algoritmo Genético': []
    }
    
    for _ in range(n_ejecuciones):  # Para cada ejecución
        # Hill Climbing
        hc = HillClimbing(problema)  # Crea instancia
        sol_hc = hc.resolver()  # Ejecuta algoritmo
        resultados['Hill Climbing'].append(problema.evaluar(sol_hc))  # Almacena resultado
        
        # Simulated Annealing
        sa = SimulatedAnnealing(problema)  # Crea instancia
        sol_sa = sa.resolver()  # Ejecuta algoritmo
        resultados['Simulated Annealing'].append(problema.evaluar(sol_sa))  # Almacena resultado
        
        # Algoritmo Genético
        ag = AlgoritmoGenetico(problema)  # Crea instancia
        sol_ag = ag.resolver()  # Ejecuta algoritmo
        resultados['Algoritmo Genético'].append(problema.evaluar(sol_ag))  # Almacena resultado
    
    # Calcular promedios
    return {algo: sum(vals)/n_ejecuciones for algo, vals in resultados.items()}  # Devuelve promedios

# Ejemplo de uso  # Bloque principal
if __name__ == "__main__":
    print("COMPARACIÓN DE ALGORITMOS DE BÚSQUEDA LOCAL")  # Título
    print("=" * 50)  # Separador
    
    # Crear problema de optimización (Ackley en 2D)  # Paso 1: Definir problema
    problema = ProblemaAckley(dominio=(-5, 5), dimension=2)  # Instancia problema Ackley
    
    # 1. Ejemplo individual con Hill Climbing  # Caso 1: Hill Climbing
    print("\nEjecutando Hill Climbing...")
    hc = HillClimbing(problema, max_iter=1000)  # Crea instancia
    sol_hc = hc.resolver()  # Ejecuta algoritmo
    print(f"Mejor solución encontrada: {sol_hc}")  # Muestra solución
    print(f"Valor de la función: {problema.evaluar(sol_hc):.4f}")  # Muestra valor
    hc.graficar_progreso("Progreso de Hill Climbing")  # Muestra gráfica
    
    # 2. Ejemplo individual con Simulated Annealing  # Caso 2: Simulated Annealing
    print("\nEjecutando Simulated Annealing...")
    sa = SimulatedAnnealing(problema, max_iter=1000)  # Crea instancia
    sol_sa = sa.resolver()  # Ejecuta algoritmo
    print(f"Mejor solución encontrada: {sol_sa}")  # Muestra solución
    print(f"Valor de la función: {problema.evaluar(sol_sa):.4f}")  # Muestra valor
    sa.graficar_progreso("Progreso de Simulated Annealing")  # Muestra gráfica
    
    # 3. Ejemplo individual con Algoritmo Genético  # Caso 3: Algoritmo Genético
    print("\nEjecutando Algoritmo Genético...")
    ag = AlgoritmoGenetico(problema, max_iter=100)  # Crea instancia
    sol_ag = ag.resolver()  # Ejecuta algoritmo
    print(f"Mejor solución encontrada: {sol_ag}")  # Muestra solución
    print(f"Valor de la función: {problema.evaluar(sol_ag):.4f}")  # Muestra valor
    ag.graficar_progreso("Progreso del Algoritmo Genético")  # Muestra gráfica
    
    # 4. Comparación estadística  # Comparación exhaustiva
    print("\nComparando algoritmos...")
    resultados = comparar_algoritmos(problema, n_ejecuciones=5)  # Ejecuta comparación
    
    print("\nResultados promedio (minimización):")  # Muestra resultados
    for algoritmo, valor in resultados.items():  # Para cada algoritmo
        print(f"{algoritmo}: {valor:.4f}")  # Muestra promedio
    
    # Visualización comparativa  # Gráfica de comparación
    plt.figure(figsize=(10, 6))  # Crea figura
    plt.bar(resultados.keys(), resultados.values(), color=['blue', 'green', 'red'])  # Gráfica de barras
    plt.title("Comparación de Algoritmos de Búsqueda Local")  # Título
    plt.ylabel("Valor promedio de la función objetivo")  # Etiqueta eje Y
    plt.grid(True, axis='y')  # Cuadrícula
    plt.show()  # Muestra gráfica