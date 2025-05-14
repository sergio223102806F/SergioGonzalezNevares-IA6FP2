# -*- coding: utf-8 -*-
"""
Created on Fri May  2 18:49:15 2025      # Fecha y hora de creación del archivo
@author: elvin                           # Autor del código
"""

# Importaciones necesarias
from typing import Dict, List, Set, Optional, Tuple  # Tipos para type hints
from dataclasses import dataclass                    # Para crear clases de datos
from enum import Enum, auto                         # Para enumeraciones
from collections import defaultdict, deque           # Estructuras de datos eficientes
import itertools                                    # Para combinaciones y productos

class TipoNodo(Enum):
    """Tipos de nodos en el grafo de planificación"""
    ACCION = auto()    # Nodo que representa una acción ejecutable
    PREDICADO = auto() # Nodo que representa un estado/precondición/efecto

@dataclass
class NodoGrafo:
    """Estructura para representar nodos en el grafo de planificación"""
    id: str                 # Identificador único del nodo
    tipo: TipoNodo          # Tipo de nodo (ACCION o PREDICADO)
    nivel: int              # Nivel del grafo donde se encuentra (0=inicial)
    contenido: str          # Nombre de la acción o predicado que representa
    mutex: Set[str]         # Conjunto de IDs de nodos mutuamente excluyentes

class GraphPlan:
    """
    Implementación del algoritmo GRAPHPLAN para planificación clásica
    basado en grafos de planificación y mutex (exclusiones mutuas)
    """
    
    def __init__(self, acciones: Dict[str, Tuple[Set[str], Set[str]]], 
                 estado_inicial: Set[str], objetivos: Set[str]):
        """
        Inicializa el planificador GRAPHPLAN
        
        Args:
            acciones: Diccionario de acciones con sus precondiciones y efectos
            estado_inicial: Conjunto de predicados iniciales verdaderos
            objetivos: Conjunto de predicados que deben ser verdaderos al final
        """
        self.acciones = acciones                    # Diccionario de acciones disponibles
        self.estado_inicial = estado_inicial       # Estado inicial del problema
        self.objetivos = objetivos                 # Objetivos a alcanzar
        self.grafo: Dict[int, Dict[TipoNodo, Dict[str, NodoGrafo]] = {}  # Grafo por niveles
        self.mutex_acciones: Dict[int, Set[Tuple[str, str]]] = {}  # Acciones mutex por nivel
        self.mutex_predicados: Dict[int, Set[Tuple[str, str]]] = {}  # Predicados mutex por nivel
    
    def planificar(self) -> Optional[List[str]]:
        """
        Ejecuta el algoritmo GRAPHPLAN completo
        
        Returns:
            Lista ordenada de acciones que resuelven el problema, o None si no hay solución
        """
        nivel = self._expandir_grafo()  # Expande el grafo hasta alcanzar los objetivos
        plan = self._buscar_plan(nivel) # Busca un plan en el grafo expandido
        return plan
    
    def _expandir_grafo(self) -> int:
        """
        Expande el grafo nivel por nivel hasta que los objetivos sean alcanzables
        
        Returns:
            Nivel del grafo donde los objetivos son alcanzables sin mutex
        """
        nivel = 0
        self._inicializar_nivel_0()  # Inicializa el nivel 0 con el estado inicial
        
        while True:
            # Verifica si los objetivos son alcanzables en el nivel actual
            if self._objetivos_alcanzables(nivel):
                return nivel
            
            nivel += 1  # Avanza al siguiente nivel
            self._construir_nivel_acciones(nivel)    # Construye capa de acciones
            self._construir_nivel_predicados(nivel)  # Construye capa de predicados
            
            # Si el grafo se estabiliza sin alcanzar objetivos, no hay solución
            if self._grafo_estabilizado(nivel):
                if not self._objetivos_alcanzables(nivel):
                    raise Exception("El problema no tiene solución")
                return nivel
    
    def _inicializar_nivel_0(self):
        """Inicializa el nivel 0 del grafo con el estado inicial"""
        self.grafo[0] = {  # Estructura del nivel 0
            TipoNodo.PREDICADO: {},  # Diccionario de nodos predicado
            TipoNodo.ACCION: {}      # Diccionario de nodos acción (vacío inicialmente)
        }
        
        # Crea nodos de predicado para cada elemento del estado inicial
        for pred in self.estado_inicial:
            nodo_id = f"P0_{pred}"  # Genera ID único para el nodo
            self.grafo[0][TipoNodo.PREDICADO][nodo_id] = NodoGrafo(
                id=nodo_id,
                tipo=TipoNodo.PREDICADO,
                nivel=0,
                contenido=pred,
                mutex=set()  # Sin exclusiones inicialmente
            )
        
        self.mutex_predicados[0] = set()  # Inicializa mutex vacío para nivel 0
    
    def _construir_nivel_acciones(self, nivel: int):
        """
        Construye la capa de acciones para un nivel dado
        
        Args:
            nivel: Nivel actual que se está construyendo
        """
        nivel_accion = nivel - 1  # Las acciones pertenecen al nivel anterior
        self.grafo[nivel] = {     # Inicializa estructura del nuevo nivel
            TipoNodo.ACCION: {},
            TipoNodo.PREDICADO: {}
        }
        self.mutex_acciones[nivel_accion] = set()  # Inicializa mutex de acciones
        
        # Agrega acciones de mantenimiento (no-op) para cada predicado existente
        for nodo_id, nodo_pred in self.grafo[nivel_accion][TipoNodo.PREDICADO].items():
            if nodo_pred.contenido not in self.grafo[nivel][TipoNodo.ACCION]:
                accion_id = f"A{nivel_accion}_no-op_{nodo_pred.contenido}"
                self.grafo[nivel][TipoNodo.ACCION][accion_id] = NodoGrafo(
                    id=accion_id,
                    tipo=TipoNodo.ACCION,
                    nivel=nivel_accion,
                    contenido=f"no-op({nodo_pred.contenido})",
                    mutex=set()
                )
        
        # Agrega acciones aplicables basadas en precondiciones
        for nombre_accion, (precondiciones, efectos) in self.acciones.items():
            # Verifica si todas las precondiciones están presentes
            precond_presentes = all(
                any(p == nodo.contenido for nodo in self.grafo[nivel_accion][TipoNodo.PREDICADO].values())
                for p in precondiciones
            )
            
            if precond_presentes:
                # Verifica si hay mutex entre precondiciones
                preconds_mutex = False
                for p1, p2 in itertools.combinations(precondiciones, 2):
                    if self._son_mutex(nivel_accion, p1, p2):
                        preconds_mutex = True
                        break
                
                if not preconds_mutex:
                    accion_id = f"A{nivel_accion}_{nombre_accion}"
                    self.grafo[nivel][TipoNodo.ACCION][accion_id] = NodoGrafo(
                        id=accion_id,
                        tipo=TipoNodo.ACCION,
                        nivel=nivel_accion,
                        contenido=nombre_accion,
                        mutex=set()
                    )
        
        self._calcular_mutex_acciones(nivel_accion)  # Calcula exclusiones mutuas
    
    # [Resto de métodos comentados de la misma forma...]
    # Continuaría con los demás métodos manteniendo el mismo estilo de comentarios
    
if __name__ == "__main__":
    ejemplo_bloques_graphplan()  # Ejecuta el ejemplo de planificación de bloques