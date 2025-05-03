# -*- coding: utf-8 -*-
"""
Created on Fri May  2 18:49:15 2025

@author: elvin
"""

# Importaciones necesarias
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass
from enum import Enum, auto
from collections import defaultdict, deque
import itertools

class TipoNodo(Enum):
    """Tipos de nodos en el grafo de planificación"""
    ACCION = auto()    # Nodo de acción
    PREDICADO = auto() # Nodo de predicado (precondición/efecto)

@dataclass
class NodoGrafo:
    """Estructura para representar nodos en el grafo de planificación"""
    id: str                 # Identificador único
    tipo: TipoNodo          # Tipo de nodo
    nivel: int              # Nivel en el grafo (0 para estado inicial)
    contenido: str          # Nombre de la acción o predicado
    mutex: Set[str]         # Conjunto de nodos mutuamente excluyentes

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
            acciones (Dict[str, Tuple[Set[str], Set[str]]]): 
                Diccionario de acciones con (precondiciones, efectos)
            estado_inicial (Set[str]): Conjunto de predicados iniciales
            objetivos (Set[str]): Conjunto de predicados objetivo
        """
        self.acciones = acciones
        self.estado_inicial = estado_inicial
        self.objetivos = objetivos
        self.grafo: Dict[int, Dict[TipoNodo, Dict[str, NodoGrafo]]] = {}  # Niveles del grafo
        self.mutex_acciones: Dict[int, Set[Tuple[str, str]]] = {}  # Pares de acciones mutex por nivel
        self.mutex_predicados: Dict[int, Set[Tuple[str, str]]] = {}  # Pares de predicados mutex por nivel
    
    def planificar(self) -> Optional[List[str]]:
        """
        Ejecuta el algoritmo GRAPHPLAN para encontrar un plan
        
        Returns:
            Optional[List[str]]: Lista de acciones del plan o None si no hay solución
        """
        # Paso 1: Expandir el grafo hasta que los objetivos sean alcanzables sin mutex
        nivel = self._expandir_grafo()
        
        # Paso 2: Buscar en el grafo expandido
        plan = self._buscar_plan(nivel)
        
        return plan
    
    def _expandir_grafo(self) -> int:
        """
        Expande el grafo de planificación nivel por nivel hasta que:
        - Todos los objetivos aparecen en un nivel sin mutex entre ellos
        - El grafo se estabiliza (no hay nuevos predicados o acciones)
        
        Returns:
            int: Nivel alcanzado
        """
        nivel = 0
        self._inicializar_nivel_0()
        
        while True:
            # Verificar si los objetivos están presentes sin mutex en el nivel actual
            if self._objetivos_alcanzables(nivel):
                return nivel
            
            # Expandir al siguiente nivel
            nivel += 1
            self._construir_nivel_acciones(nivel)
            self._construir_nivel_predicados(nivel)
            
            # Verificar si el grafo se ha estabilizado
            if self._grafo_estabilizado(nivel):
                if not self._objetivos_alcanzables(nivel):
                    raise Exception("El problema no tiene solución")
                return nivel
    
    def _inicializar_nivel_0(self):
        """Inicializa el nivel 0 del grafo con el estado inicial"""
        self.grafo[0] = {
            TipoNodo.PREDICADO: {},
            TipoNodo.ACCION: {}
        }
        
        # Crear nodos de predicado para el estado inicial
        for pred in self.estado_inicial:
            nodo_id = f"P0_{pred}"
            self.grafo[0][TipoNodo.PREDICADO][nodo_id] = NodoGrafo(
                id=nodo_id,
                tipo=TipoNodo.PREDICADO,
                nivel=0,
                contenido=pred,
                mutex=set()
            )
        
        # Inicializar mutex para nivel 0 (no hay acciones aún)
        self.mutex_predicados[0] = set()
    
    def _construir_nivel_acciones(self, nivel: int):
        """
        Construye la capa de acciones para un nivel dado
        
        Args:
            nivel (int): Nivel a construir (las acciones están en nivel i-1)
        """
        nivel_accion = nivel - 1
        self.grafo[nivel] = {
            TipoNodo.ACCION: {},
            TipoNodo.PREDICADO: {}
        }
        self.mutex_acciones[nivel_accion] = set()
        
        # Agregar acción de mantenimiento (no-op) para cada predicado existente
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
        
        # Agregar acciones aplicables
        for nombre_accion, (precondiciones, efectos) in self.acciones.items():
            # Verificar si todas las precondiciones están presentes sin mutex
            precond_presentes = all(
                any(p == nodo.contenido for nodo in self.grafo[nivel_accion][TipoNodo.PREDICADO].values())
                for p in precondiciones
            )
            
            if precond_presentes:
                # Verificar mutex entre precondiciones
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
        
        # Calcular mutex entre acciones en este nivel
        self._calcular_mutex_acciones(nivel_accion)
    
    def _construir_nivel_predicados(self, nivel: int):
        """
        Construye la capa de predicados para un nivel dado
        
        Args:
            nivel (int): Nivel a construir (los predicados están en nivel i)
        """
        nivel_accion = nivel - 1
        self.mutex_predicados[nivel] = set()
        
        # Los predicados son los efectos de las acciones del nivel anterior
        for accion_id, nodo_accion in self.grafo[nivel][TipoNodo.ACCION].items():
            if nodo_accion.contenido.startswith("no-op"):
                # Acción de mantenimiento, el predicado es el mismo
                pred = nodo_accion.contenido[6:-1]  # extraer de "no-op(pred)"
                pred_id = f"P{nivel}_{pred}"
                if pred_id not in self.grafo[nivel][TipoNodo.PREDICADO]:
                    self.grafo[nivel][TipoNodo.PREDICADO][pred_id] = NodoGrafo(
                        id=pred_id,
                        tipo=TipoNodo.PREDICADO,
                        nivel=nivel,
                        contenido=pred,
                        mutex=set()
                    )
            else:
                # Acción normal, agregar sus efectos
                efectos = self.acciones[nodo_accion.contenido][1]
                for efecto in efectos:
                    pred_id = f"P{nivel}_{efecto}"
                    if pred_id not in self.grafo[nivel][TipoNodo.PREDICADO]:
                        self.grafo[nivel][TipoNodo.PREDICADO][pred_id] = NodoGrafo(
                            id=pred_id,
                            tipo=TipoNodo.PREDICADO,
                            nivel=nivel,
                            contenido=efecto,
                            mutex=set()
                        )
        
        # Calcular mutex entre predicados en este nivel
        self._calcular_mutex_predicados(nivel)
    
    def _calcular_mutex_acciones(self, nivel: int):
        """
        Calcula relaciones de exclusión mutua (mutex) entre acciones en un nivel
        
        Args:
            nivel (int): Nivel de acciones a analizar
        """
        acciones_nivel = self.grafo[nivel+1][TipoNodo.ACCION]
        
        for a1, a2 in itertools.combinations(acciones_nivel.keys(), 2):
            nodo_a1 = acciones_nivel[a1]
            nodo_a2 = acciones_nivel[a2]
            
            # Dos acciones son mutex si:
            # 1. Una borra una precondición de la otra
            # 2. Una borra un efecto de la otra
            # 3. Sus efectos son mutex
            
            # Caso 1 y 2: Verificar interferencias
            nombre_a1 = nodo_a1.contenido
            nombre_a2 = nodo_a2.contenido
            
            preconds_a1 = self.acciones[nombre_a1][0] if not nombre_a1.startswith("no-op") else {nombre_a1[6:-1]}
            efectos_a1 = self.acciones[nombre_a1][1] if not nombre_a1.startswith("no-op") else {nombre_a1[6:-1]}
            
            preconds_a2 = self.acciones[nombre_a2][0] if not nombre_a2.startswith("no-op") else {nombre_a2[6:-1]}
            efectos_a2 = self.acciones[nombre_a2][1] if not nombre_a2.startswith("no-op") else {nombre_a2[6:-1]}
            
            # Verificar si a1 borra precondición o efecto de a2
            interferencia = any(
                (ef in preconds_a2 and f"¬{ef}" in efectos_a1) or 
                (ef in efectos_a2 and f"¬{ef}" in efectos_a1)
                for ef in efectos_a1 if ef.startswith("¬")
            )
            
            # Verificar si a2 borra precondición o efecto de a1
            interferencia = interferencia or any(
                (ef in preconds_a1 and f"¬{ef}" in efectos_a2) or 
                (ef in efectos_a1 and f"¬{ef}" in efectos_a2)
                for ef in efectos_a2 if ef.startswith("¬")
            )
            
            # Caso 3: Efectos mutex
            efectos_mutex = False
            for ef1 in efectos_a1:
                if ef1.startswith("¬"):
                    continue
                for ef2 in efectos_a2:
                    if ef2.startswith("¬"):
                        continue
                    if self._son_mutex(nivel, ef1, ef2):
                        efectos_mutex = True
                        break
                if efectos_mutex:
                    break
            
            if interferencia or efectos_mutex:
                self.mutex_acciones[nivel].add((a1, a2))
                nodo_a1.mutex.add(a2)
                nodo_a2.mutex.add(a1)
    
    def _calcular_mutex_predicados(self, nivel: int):
        """
        Calcula relaciones de exclusión mutua (mutex) entre predicados en un nivel
        
        Args:
            nivel (int): Nivel de predicados a analizar
        """
        if nivel == 0:
            return  # En nivel 0 solo está el estado inicial, no hay mutex
        
        acciones_nivel_anterior = self.grafo[nivel][TipoNodo.ACCION]
        predicados_nivel = self.grafo[nivel][TipoNodo.PREDICADO]
        
        for p1, p2 in itertools.combinations(predicados_nivel.keys(), 2):
            nodo_p1 = predicados_nivel[p1]
            nodo_p2 = predicados_nivel[p2]
            
            # Dos predicados son mutex si:
            # Todas las acciones que producen p1 son mutex con todas las que producen p2
            
            productores_p1 = [
                a for a in acciones_nivel_anterior.values() 
                if nodo_p1.contenido in self.acciones[a.contenido][1] or 
                   (a.contenido.startswith("no-op") and a.contenido[6:-1] == nodo_p1.contenido)
            ]
            
            productores_p2 = [
                a for a in acciones_nivel_anterior.values() 
                if nodo_p2.contenido in self.acciones[a.contenido][1] or 
                   (a.contenido.startswith("no-op") and a.contenido[6:-1] == nodo_p2.contenido)
            ]
            
            todos_mutex = True
            for prod_p1 in productores_p1:
                for prod_p2 in productores_p2:
                    if (prod_p1.id, prod_p2.id) not in self.mutex_acciones[nivel-1] and \
                       (prod_p2.id, prod_p1.id) not in self.mutex_acciones[nivel-1]:
                        todos_mutex = False
                        break
                if not todos_mutex:
                    break
            
            if todos_mutex and productores_p1 and productores_p2:
                self.mutex_predicados[nivel].add((p1, p2))
                nodo_p1.mutex.add(p2)
                nodo_p2.mutex.add(p1)
    
    def _son_mutex(self, nivel: int, p1: str, p2: str) -> bool:
        """
        Verifica si dos predicados son mutex en un nivel dado
        
        Args:
            nivel (int): Nivel a verificar
            p1 (str): Primer predicado
            p2 (str): Segundo predicado
            
        Returns:
            bool: True si los predicados son mutex
        """
        # Encontrar los IDs de nodo para estos predicados
        nodo_p1 = next(
            (n for n in self.grafo[nivel][TipoNodo.PREDICADO].values() if n.contenido == p1),
            None
        )
        nodo_p2 = next(
            (n for n in self.grafo[nivel][TipoNodo.PREDICADO].values() if n.contenido == p2),
            None
        )
        
        if nodo_p1 is None or nodo_p2 is None:
            return False
            
        return nodo_p2.id in nodo_p1.mutex
    
    def _objetivos_alcanzables(self, nivel: int) -> bool:
        """
        Verifica si todos los objetivos están presentes sin mutex en un nivel
        
        Args:
            nivel (int): Nivel a verificar
            
        Returns:
            bool: True si los objetivos son alcanzables en este nivel
        """
        # Verificar que todos los objetivos estén presentes
        for objetivo in self.objetivos:
            presente = any(
                nodo.contenido == objetivo 
                for nodo in self.grafo[nivel][TipoNodo.PREDICADO].values()
            )
            if not presente:
                return False
        
        # Verificar que no haya mutex entre objetivos
        for obj1, obj2 in itertools.combinations(self.objetivos, 2):
            if self._son_mutex(nivel, obj1, obj2):
                return False
        
        return True
    
    def _grafo_estabilizado(self, nivel: int) -> bool:
        """
        Verifica si el grafo se ha estabilizado (no hay cambios en predicados o mutex)
        
        Args:
            nivel (int): Nivel actual a comparar con el anterior
            
        Returns:
            bool: True si el grafo se ha estabilizado
        """
        if nivel < 2:
            return False
        
        # Comparar predicados y mutex con el nivel anterior
        preds_actual = {n.contenido for n in self.grafo[nivel][TipoNodo.PREDICADO].values()}
        preds_anterior = {n.contenido for n in self.grafo[nivel-1][TipoNodo.PREDICADO].values()}
        
        if preds_actual != preds_anterior:
            return False
        
        # Comparar mutex de predicados
        mutex_actual = {
            tuple(sorted((n1.contenido, n2.contenido)))
            for n1, n2 in self.mutex_predicados[nivel]
        }
        mutex_anterior = {
            tuple(sorted((n1.contenido, n2.contenido)))
            for n1, n2 in self.mutex_predicados[nivel-1]
        }
        
        return mutex_actual == mutex_anterior
    
    def _buscar_plan(self, nivel_objetivo: int) -> Optional[List[str]]:
        """
        Busca recursivamente un plan en el grafo expandido
        
        Args:
            nivel_objetivo (int): Nivel donde se alcanzan los objetivos
            
        Returns:
            Optional[List[str]]: Lista de acciones del plan o None
        """
        # Iniciar búsqueda desde los objetivos
        return self._buscar_plan_recursivo(
            nivel_objetivo, 
            self.objetivos, 
            set(), 
            set()
        )
    
    def _buscar_plan_recursivo(self, nivel: int, objetivos: Set[str], 
                              acciones_anteriores: Set[str], 
                              logros_anteriores: Set[str]) -> Optional[List[str]]:
        """
        Búsqueda recursiva del plan (algoritmo GP-SEARCH)
        
        Args:
            nivel (int): Nivel actual en el grafo
            objetivos (Set[str]): Predicados objetivo en este nivel
            acciones_anteriores (Set[str]): Acciones seleccionadas en el nivel superior
            logros_anteriores (Set[str]): Predicados logrados en el nivel superior
            
        Returns:
            Optional[List[str]]: Subplan encontrado o None
        """
        if nivel == 0:
            return []  # Plan vacío en nivel 0
        
        # Seleccionar acciones para lograr los objetivos
        seleccion_acciones = self._seleccionar_acciones(nivel, objetivos, acciones_anteriores)
        if not seleccion_acciones:
            return None
        
        # Precondiciones de las acciones seleccionadas se convierten en nuevos objetivos
        nuevas_precondiciones = set()
        for accion in seleccion_acciones:
            if accion.startswith("no-op"):
                continue
            precondiciones = self.acciones[accion][0]
            nuevas_precondiciones.update(precondiciones)
        
        # Buscar recursivamente en el nivel anterior
        subplan = self._buscar_plan_recursivo(
            nivel - 1,
            nuevas_precondiciones,
            {a for a in seleccion_acciones if not a.startswith("no-op")},
            objetivos
        )
        
        if subplan is None:
            return None
        
        # Combinar subplan con acciones actuales
        acciones_actuales = [a for a in seleccion_acciones if not a.startswith("no-op")]
        return subplan + acciones_actuales
    
    def _seleccionar_acciones(self, nivel: int, objetivos: Set[str], 
                             exclusiones: Set[str]) -> Optional[Set[str]]:
        """
        Selecciona un conjunto de acciones no mutex que cubran todos los objetivos
        
        Args:
            nivel (int): Nivel actual
            objetivos (Set[str]): Predicados a lograr
            exclusiones (Set[str]): Acciones a excluir (por conflictos con niveles superiores)
            
        Returns:
            Optional[Set[str]]: Conjunto de acciones seleccionadas o None
        """
        # Mapear cada objetivo a acciones que lo producen (no mutex con exclusiones)
        acciones_por_objetivo = {}
        for objetivo in objetivos:
            acciones = []
            for nodo_accion in self.grafo[nivel][TipoNodo.ACCION].values():
                if nodo_accion.contenido in exclusiones:
                    continue
                
                efectos = self.acciones[nodo_accion.contenido][1] if not nodo_accion.contenido.startswith("no-op") else {nodo_accion.contenido[6:-1]}
                
                if objetivo in efectos:
                    # Verificar si es mutex con alguna exclusión
                    conflictiva = False
                    for excl in exclusiones:
                        if (nodo_accion.id, excl) in self.mutex_acciones[nivel-1] or \
                           (excl, nodo_accion.id) in self.mutex_acciones[nivel-1]:
                            conflictiva = True
                            break
                    
                    if not conflictiva:
                        acciones.append(nodo_accion.id)
            
            if not acciones:
                return None  # No hay forma de lograr este objetivo
            
            acciones_por_objetivo[objetivo] = acciones
        
        # Intentar encontrar un conjunto de acciones que cubra todos los objetivos sin mutex
        from itertools import product
        for combinacion in product(*acciones_por_objetivo.values()):
            combinacion_unica = set(combinacion)
            
            # Verificar que no haya mutex entre las acciones seleccionadas
            mutex = False
            for a1, a2 in itertools.combinations(combinacion_unica, 2):
                if (a1, a2) in self.mutex_acciones[nivel-1] or \
                   (a2, a1) in self.mutex_acciones[nivel-1]:
                    mutex = True
                    break
            
            if not mutex:
                return combinacion_unica
        
        return None

def ejemplo_bloques_graphplan():
    """
    Ejemplo de planificación con GRAPHPLAN en el dominio de bloques
    """
    # Definir acciones (nombre: (precondiciones, efectos))
    acciones = {
        "mover_A_B": ({"libre(A)", "libre(B)", "en(A, Mesa)"}, 
                      {"en(A, B)", "¬en(A, Mesa)", "¬libre(B)"}),
        "mover_A_C": ({"libre(A)", "libre(C)", "en(A, Mesa)"}, 
                      {"en(A, C)", "¬en(A, Mesa)", "¬libre(C)"}),
        "mover_B_A": ({"libre(B)", "libre(A)", "en(B, Mesa)"}, 
                      {"en(B, A)", "¬en(B, Mesa)", "¬libre(A)"}),
        "mover_B_C": ({"libre(B)", "libre(C)", "en(B, Mesa)"}, 
                      {"en(B, C)", "¬en(B, Mesa)", "¬libre(C)"}),
        "mover_C_A": ({"libre(C)", "libre(A)", "en(C, Mesa)"}, 
                      {"en(C, A)", "¬en(C, Mesa)", "¬libre(A)"}),
        "mover_C_B": ({"libre(C)", "libre(B)", "en(C, Mesa)"}, 
                      {"en(C, B)", "¬en(C, Mesa)", "¬libre(B)"})
    }
    
    # Estado inicial
    estado_inicial = {
        "en(A, Mesa)", "en(B, Mesa)", "en(C, Mesa)",
        "libre(A)", "libre(B)", "libre(C)", "libre(Mesa)"
    }
    
    # Objetivo: A sobre B y B sobre C
    objetivos = {"en(A, B)", "en(B, C)"}
    
    # Crear y ejecutar planificador
    planificador = GraphPlan(acciones, estado_inicial, objetivos)
    plan = planificador.planificar()
    
    # Mostrar resultados
    print("\n=== PLANIFICACIÓN CON GRAPHPLAN ===")
    if plan:
        print("\nPlan encontrado:")
        for i, accion in enumerate(plan, 1):
            print(f"{i}. {accion}")
        
        # Mostrar estructura del grafo (resumido)
        print("\nResumen del grafo de planificación:")
        for nivel in sorted(planificador.grafo.keys()):
            print(f"\nNivel {nivel}:")
            print(f"  Predicados: {len(planificador.grafo[nivel][TipoNodo.PREDICADO])}")
            print(f"  Acciones: {len(planificador.grafo[nivel][TipoNodo.ACCION])}")
            if nivel in planificador.mutex_predicados:
                print(f"  Mutex predicados: {len(planificador.mutex_predicados[nivel])}")
            if nivel-1 in planificador.mutex_acciones:
                print(f"  Mutex acciones: {len(planificador.mutex_acciones[nivel-1])}")
    else:
        print("No se encontró plan solución")

if __name__ == "__main__":
    ejemplo_bloques_graphplan()