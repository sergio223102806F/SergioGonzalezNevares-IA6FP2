# -*- coding: utf-8 -*-


# Importaciones necesarias
from typing import Dict, List, Set, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum, auto
import re

class TipoPlaneador(Enum):
    """Tipos de algoritmos de planificación implementados"""
    STRIPS = auto()  # Stanford Research Institute Problem Solver
    ADL = auto()     # Action Description Language (extensión de STRIPS)

class TipoExpresion(Enum):
    """Tipos de expresiones en precondiciones/efectos"""
    ATOMICA = auto()     # Expresión atómica (ej: "en(A, B)")
    NEGACION = auto()    # Negación (ej: "¬en(A, B)")
    CONJUNCION = auto()  # AND lógico
    DISYUNCION = auto()  # OR lógico
    IMPLICACION = auto() # Implicación
    UNIVERSAL = auto()   # Cuantificador universal
    EXISTENCIAL = auto() # Cuantificador existencial

@dataclass
class Expresion:
    """Estructura para representar expresiones lógicas"""
    tipo: TipoExpresion
    contenido: Union[str, List['Expresion']  # String para atómicas/negaciones, lista para otras
    parametros: List[str] = field(default_factory=list)  # Para cuantificadores

@dataclass
class Accion:
    """Estructura para representar acciones en STRIPS/ADL"""
    nombre: str
    parametros: List[str]  # Variables de la acción
    precondiciones: Expresion  # Expresión que debe ser verdadera para ejecutar
    efectos: Expresion        # Cambios que produce la acción
    tipo: TipoPlaneador       # Tipo de planificador (STRIPS o ADL)

@dataclass
class ProblemaPlanificacion:
    """Define un problema completo de planificación"""
    nombre: str
    objetos: Dict[str, List[str]]  # Tipos y sus instancias
    predicados: Dict[str, List[str]]  # Tipos de los parámetros
    estado_inicial: Set[str]  # Hechos iniciales (como strings)
    metas: Expresion          # Objetivo a alcanzar
    acciones: List[Accion]    # Acciones disponibles
    tipo: TipoPlaneador       # Tipo de planificación (STRIPS o ADL)

class Planeador:
    """
    Implementación de algoritmos de planificación STRIPS y ADL
    con búsqueda hacia adelante y hacia atrás
    """
    
    def __init__(self, problema: ProblemaPlanificacion):
        """Inicializa el planeador con un problema específico"""
        self.problema = problema
        self.plan: List[str] = []  # Secuencia de acciones del plan
        self.estados_visitados: Set[frozenset] = set()  # Estados ya explorados
    
    def planificar(self) -> Optional[List[str]]:
        """
        Encuentra un plan que resuelva el problema
        
        Returns:
            Optional[List[str]]: Lista de acciones del plan, o None si no hay solución
        """
        if self.problema.tipo == TipoPlaneador.STRIPS:
            return self._busqueda_hacia_adelante()
        else:
            return self._busqueda_adelante_adl()
    
    def _busqueda_hacia_adelante(self) -> Optional[List[str]]:
        """
        Búsqueda hacia adelante para STRIPS (sin variables)
        
        Returns:
            Optional[List[str]]: Plan encontrado o None
        """
        estado_actual = self.problema.estado_inicial.copy()
        self.estados_visitados.add(frozenset(estado_actual))
        
        for _ in range(100):  # Límite de pasos para evitar bucles infinitos
            if self._satisface(estado_actual, self.problema.metas):
                return self.plan
            
            # Encontrar acciones aplicables
            acciones_aplicables = []
            for accion in self.problema.acciones:
                if accion.tipo != TipoPlaneador.STRIPS:
                    continue
                    
                # Instanciar parámetros para STRIPS (todas las combinaciones posibles)
                instancias = self._instanciar_parametros(accion)
                for instancia in instancias:
                    accion_instanciada = self._instanciar_accion(accion, instancia)
                    if self._es_aplicable(estado_actual, accion_instanciada.precondiciones):
                        acciones_aplicables.append(accion_instanciada)
            
            if not acciones_aplicables:
                return None  # No hay solución
            
            # Seleccionar una acción (estrategia simple: primera disponible)
            accion_elegida = acciones_aplicables[0]
            self.plan.append(accion_elegida.nombre)
            
            # Aplicar efectos
            estado_actual = self._aplicar_efectos(estado_actual, accion_elegida.efectos)
            
            # Verificar si ya visitamos este estado
            estado_frozen = frozenset(estado_actual)
            if estado_frozen in self.estados_visitados:
                return None  # Ciclo detectado
            self.estados_visitados.add(estado_frozen)
        
        return None  # Límite de pasos alcanzado
    
    def _busqueda_adelante_adl(self) -> Optional[List[str]]:
        """
        Búsqueda hacia adelante para ADL (maneja expresiones complejas)
        
        Returns:
            Optional[List[str]]: Plan encontrado o None
        """
        estado_actual = self.problema.estado_inicial.copy()
        self.estados_visitados.add(frozenset(estado_actual))
        
        for _ in range(100):  # Límite de pasos
            if self._satisface(estado_actual, self.problema.metas):
                return self.plan
            
            # Encontrar acciones aplicables (con unificación para ADL)
            acciones_aplicables = []
            for accion in self.problema.acciones:
                # Para ADL, encontramos sustituciones que satisfagan precondiciones
                sustituciones = self._encontrar_sustituciones(estado_actual, accion.precondiciones, {})
                for sustitucion in sustituciones:
                    accion_instanciada = self._instanciar_accion(accion, sustitucion)
                    acciones_aplicables.append(accion_instanciada)
            
            if not acciones_aplicables:
                return None  # No hay solución
            
            # Seleccionar una acción (estrategia simple: primera disponible)
            accion_elegida = acciones_aplicables[0]
            self.plan.append(accion_elegida.nombre)
            
            # Aplicar efectos
            estado_actual = self._aplicar_efectos_adl(estado_actual, accion_elegida.efectos)
            
            # Verificar si ya visitamos este estado
            estado_frozen = frozenset(estado_actual)
            if estado_frozen in self.estados_visitados:
                return None  # Ciclo detectado
            self.estados_visitados.add(estado_frozen)
        
        return None  # Límite de pasos alcanzado
    
    def _instanciar_parametros(self, accion: Accion) -> List[Dict[str, str]]:
        """
        Genera todas las posibles instanciaciones de parámetros para STRIPS
        
        Args:
            accion (Accion): Acción a instanciar
            
        Returns:
            List[Dict[str, str]]: Lista de sustituciones posibles
        """
        from itertools import product
        
        # Para STRIPS, asumimos que los parámetros tienen tipos definidos en el problema
        valores_por_parametro = []
        for param in accion.parametros:
            # Asumimos que el nombre del tipo es el mismo que el del parámetro (simplificación)
            tipo = param.split(':')[-1] if ':' in param else param
            if tipo in self.problema.objetos:
                valores_por_parametro.append(self.problema.objetos[tipo])
            else:
                # Si no se especifica tipo, usar todos los objetos
                valores_por_parametro.append([obj for lista in self.problema.objetos.values() for obj in lista])
        
        # Producto cartesiano de todas las combinaciones posibles
        combinaciones = product(*valores_por_parametro)
        
        # Convertir a diccionarios de sustituciones
        sustituciones = []
        for combo in combinaciones:
            sustitucion = {}
            for i, param in enumerate(accion.parametros):
                nombre_var = param.split(':')[0] if ':' in param else param
                sustitucion[nombre_var] = combo[i]
            sustituciones.append(sustitucion)
        
        return sustituciones
    
    def _encontrar_sustituciones(self, estado: Set[str], expr: Expresion, sustitucion: Dict[str, str]) -> List[Dict[str, str]]:
        """
        Encuentra sustituciones que satisfagan una expresión (para ADL)
        
        Args:
            estado (Set[str]): Estado actual
            expr (Expresion): Expresión a satisfacer
            sustitucion (Dict[str, str]): Sustitución acumulada
            
        Returns:
            List[Dict[str, str]]: Lista de sustituciones válidas
        """
        if expr.tipo == TipoExpresion.ATOMICA:
            # Sustituir variables en la expresión atómica
            atomo = self._aplicar_sustitucion(expr.contenido, sustitucion)
            if atomo in estado:
                return [sustitucion]
            else:
                return []
            
        elif expr.tipo == TipoExpresion.NEGACION:
            atomo = self._aplicar_sustitucion(expr.contenido, sustitucion)
            if atomo not in estado:
                return [sustitucion]
            else:
                return []
            
        elif expr.tipo == TipoExpresion.CONJUNCION:
            sustituciones_actuales = [sustitucion]
            for subexpr in expr.contenido:
                nuevas_sustituciones = []
                for sust in sustituciones_actuales:
                    nuevas_sustituciones.extend(self._encontrar_sustituciones(estado, subexpr, sust))
                sustituciones_actuales = nuevas_sustituciones
                if not sustituciones_actuales:
                    break
            return sustituciones_actuales
            
        elif expr.tipo == TipoExpresion.UNIVERSAL:
            # Para cuantificador universal, todas las instancias deben satisfacer
            variable = expr.parametros[0]
            tipo = expr.parametros[1] if len(expr.parametros) > 1 else None
            
            objetos = self.problema.objetos.get(tipo, []) if tipo else \
                     [obj for lista in self.problema.objetos.values() for obj in lista]
            
            sustituciones_actuales = []
            for obj in objetos:
                nueva_sust = sustitucion.copy()
                nueva_sust[variable] = obj
                subs = self._encontrar_sustituciones(estado, expr.contenido, nueva_sust)
                if not subs:
                    return []
                sustituciones_actuales.extend(subs)
            
            return sustituciones_actuales
            
        else:
            # Implementación simplificada - no maneja todos los casos de ADL
            return []
    
    def _aplicar_sustitucion(self, expresion: str, sustitucion: Dict[str, str]) -> str:
        """
        Aplica una sustitución a una expresión
        
        Args:
            expresion (str): Expresión con variables
            sustitucion (Dict[str, str]): Sustitución a aplicar
            
        Returns:
            str: Expresión con variables sustituidas
        """
        for var, valor in sustitucion.items():
            expresion = expresion.replace(f"?{var}", valor)
        return expresion
    
    def _instanciar_accion(self, accion: Accion, sustitucion: Dict[str, str]) -> Accion:
        """
        Crea una instancia concreta de una acción aplicando una sustitución
        
        Args:
            accion (Accion): Acción a instanciar
            sustitucion (Dict[str, str]): Sustitución a aplicar
            
        Returns:
            Accion: Acción instanciada
        """
        nombre_instanciado = self._aplicar_sustitucion(accion.nombre, sustitucion)
        
        def instanciar_expresion(expr: Expresion) -> Expresion:
            if expr.tipo in [TipoExpresion.ATOMICA, TipoExpresion.NEGACION]:
                contenido = self._aplicar_sustitucion(expr.contenido, sustitucion)
                return Expresion(expr.tipo, contenido)
            else:
                contenido = [instanciar_expresion(sub) for sub in expr.contenido]
                return Expresion(expr.tipo, contenido, expr.parametros)
        
        precond_instanciada = instanciar_expresion(accion.precondiciones)
        efectos_instanciados = instanciar_expresion(accion.efectos)
        
        return Accion(
            nombre=nombre_instanciado,
            parametros=[],
            precondiciones=precond_instanciada,
            efectos=efectos_instanciados,
            tipo=accion.tipo
        )
    
    def _es_aplicable(self, estado: Set[str], precondiciones: Expresion) -> bool:
        """
        Verifica si las precondiciones se satisfacen en un estado (STRIPS)
        
        Args:
            estado (Set[str]): Estado actual
            precondiciones (Expresion): Precondiciones a verificar
            
        Returns:
            bool: True si todas las precondiciones se satisfacen
        """
        if precondiciones.tipo == TipoExpresion.ATOMICA:
            return precondiciones.contenido in estado
        elif precondiciones.tipo == TipoExpresion.NEGACION:
            return precondiciones.contenido not in estado
        elif precondiciones.tipo == TipoExpresion.CONJUNCION:
            return all(self._es_aplicable(estado, sub) for sub in precondiciones.contenido)
        else:
            # STRIPS solo maneja conjunciones de literales
            return False
    
    def _satisface(self, estado: Set[str], metas: Expresion) -> bool:
        """
        Verifica si un estado satisface las metas
        
        Args:
            estado (Set[str]): Estado a verificar
            metas (Expresion): Metas a satisfacer
            
        Returns:
            bool: True si el estado satisface las metas
        """
        if metas.tipo == TipoExpresion.ATOMICA:
            return metas.contenido in estado
        elif metas.tipo == TipoExpresion.NEGACION:
            return metas.contenido not in estado
        elif metas.tipo == TipoExpresion.CONJUNCION:
            return all(self._satisface(estado, sub) for sub in metas.contenido)
        elif metas.tipo == TipoExpresion.DISYUNCION:
            return any(self._satisface(estado, sub) for sub in metas.contenido)
        else:
            # Implementación simplificada
            return False
    
    def _aplicar_efectos(self, estado: Set[str], efectos: Expresion) -> Set[str]:
        """
        Aplica efectos a un estado (STRIPS)
        
        Args:
            estado (Set[str]): Estado actual
            efectos (Expresion): Efectos a aplicar
            
        Returns:
            Set[str]: Nuevo estado después de aplicar efectos
        """
        nuevo_estado = estado.copy()
        
        if efectos.tipo == TipoExpresion.ATOMICA:
            nuevo_estado.add(efectos.contenido)
        elif efectos.tipo == TipoExpresion.NEGACION:
            nuevo_estado.discard(efectos.contenido[1:])  # Elimina el ¬
        elif efectos.tipo == TipoExpresion.CONJUNCION:
            for efecto in efectos.contenido:
                nuevo_estado = self._aplicar_efectos(nuevo_estado, efecto)
        
        return nuevo_estado
    
    def _aplicar_efectos_adl(self, estado: Set[str], efectos: Expresion) -> Set[str]:
        """
        Aplica efectos ADL (más complejos que STRIPS)
        
        Args:
            estado (Set[str]): Estado actual
            efectos (Expresion): Efectos a aplicar
            
        Returns:
            Set[str]: Nuevo estado después de aplicar efectos
        """
        nuevo_estado = estado.copy()
        
        if efectos.tipo == TipoExpresion.ATOMICA:
            nuevo_estado.add(efectos.contenido)
        elif efectos.tipo == TipoExpresion.NEGACION:
            nuevo_estado.discard(efectos.contenido[1:])  # Elimina el ¬
        elif efectos.tipo == TipoExpresion.CONJUNCION:
            for efecto in efectos.contenido:
                nuevo_estado = self._aplicar_efectos_adl(nuevo_estado, efecto)
        elif efectos.tipo == TipoExpresion.UNIVERSAL:
            # Efecto universal: aplicar para todos los objetos del tipo
            variable = efectos.parametros[0]
            tipo = efectos.parametros[1] if len(efectos.parametros) > 1 else None
            
            objetos = self.problema.objetos.get(tipo, []) if tipo else \
                     [obj for lista in self.problema.objetos.values() for obj in lista]
            
            for obj in objetos:
                sustitucion = {variable: obj}
                efecto_instanciado = self._instanciar_expresion(efectos.contenido, sustitucion)
                nuevo_estado = self._aplicar_efectos_adl(nuevo_estado, efecto_instanciado)
        
        return nuevo_estado
    
    def _instanciar_expresion(self, expr: Expresion, sustitucion: Dict[str, str]) -> Expresion:
        """
        Instancia una expresión aplicando una sustitución
        
        Args:
            expr (Expresion): Expresión a instanciar
            sustitucion (Dict[str, str]): Sustitución a aplicar
            
        Returns:
            Expresion: Expresión instanciada
        """
        if expr.tipo in [TipoExpresion.ATOMICA, TipoExpresion.NEGACION]:
            contenido = self._aplicar_sustitucion(expr.contenido, sustitucion)
            return Expresion(expr.tipo, contenido)
        else:
            contenido = [self._instanciar_expresion(sub, sustitucion) for sub in expr.contenido]
            return Expresion(expr.tipo, contenido, expr.parametros)

def ejemplo_bloques_strips():
    """
    Crea y devuelve un problema de planificación STRIPS clásico:
    el mundo de bloques (apilar, desapilar, mover)
    """
    # Definir objetos
    objetos = {
        'bloque': ['A', 'B', 'C', 'D'],
        'ubicacion': ['Mesa', 'A', 'B', 'C', 'D']  # Los bloques también pueden ser ubicaciones
    }
    
    # Definir predicados
    predicados = {
        'en': ['bloque', 'ubicacion'],  # en(bloque, ubicación)
        'sobre': ['bloque', 'bloque'],  # sobre(bloque, bloque)
        'libre': ['bloque'],            # libre(bloque)
        'agarrado': ['bloque']          # agarrado(bloque)
    }
    
    # Estado inicial
    estado_inicial = {
        'en(A, Mesa)', 'en(B, Mesa)', 'en(C, Mesa)', 'en(D, Mesa)',
        'libre(A)', 'libre(B)', 'libre(C)', 'libre(D)',
        'libre(Mesa)'
    }
    
    # Metas: A sobre B, B sobre C
    metas = Expresion(
        tipo=TipoExpresion.CONJUNCION,
        contenido=[
            Expresion(TipoExpresion.ATOMICA, 'sobre(A, B)'),
            Expresion(TipoExpresion.ATOMICA, 'sobre(B, C)')
        ]
    )
    
    # Acciones STRIPS
    acciones = [
        # Agarrar un bloque: precondiciones y efectos
        Accion(
            nombre='agarrar(?X:bloque)',
            parametros=['?X:bloque'],
            precondiciones=Expresion(
                tipo=TipoExpresion.CONJUNCION,
                contenido=[
                    Expresion(TipoExpresion.ATOMICA, 'libre(?X)'),
                    Expresion(TipoExpresion.ATOMICA, 'en(?X, ?Y)'),
                    Expresion(TipoExpresion.ATOMICA, 'libre(?Y)')
                ]
            ),
            efectos=Expresion(
                tipo=TipoExpresion.CONJUNCION,
                contenido=[
                    Expresion(TipoExpresion.ATOMICA, 'agarrado(?X)'),
                    Expresion(TipoExpresion.NEGACION, '¬libre(?X)'),
                    Expresion(TipoExpresion.NEGACION, '¬en(?X, ?Y)'),
                    Expresion(TipoExpresion.ATOMICA, 'libre(?Y)')
                ]
            ),
            tipo=TipoPlaneador.STRIPS
        ),
        
        # Soltar un bloque en una ubicación
        Accion(
            nombre='soltar(?X:bloque, ?Y:ubicacion)',
            parametros=['?X:bloque', '?Y:ubicacion'],
            precondiciones=Expresion(
                tipo=TipoExpresion.CONJUNCION,
                contenido=[
                    Expresion(TipoExpresion.ATOMICA, 'agarrado(?X)'),
                    Expresion(TipoExpresion.ATOMICA, 'libre(?Y)')
                ]
            ),
            efectos=Expresion(
                tipo=TipoExpresion.CONJUNCION,
                contenido=[
                    Expresion(TipoExpresion.NEGACION, '¬agarrado(?X)'),
                    Expresion(TipoExpresion.ATOMICA, 'en(?X, ?Y)'),
                    Expresion(TipoExpresion.ATOMICA, 'libre(?X)'),
                    Expresion(TipoExpresion.NEGACION, '¬libre(?Y)')
                ]
            ),
            tipo=TipoPlaneador.STRIPS
        )
    ]
    
    return ProblemaPlanificacion(
        nombre='Mundo de bloques (STRIPS)',
        objetos=objetos,
        predicados=predicados,
        estado_inicial=estado_inicial,
        metas=metas,
        acciones=acciones,
        tipo=TipoPlaneador.STRIPS
    )

def ejemplo_bloques_adl():
    """
    Crea y devuelve un problema de planificación ADL más complejo
    con condiciones universales en el mundo de bloques
    """
    problema_strips = ejemplo_bloques_strips()
    
    # Convertir a ADL y añadir acciones más complejas
    acciones_adl = problema_strips.acciones.copy()
    
    # Añadir acción para mover un bloque encima de otro solo si no tiene nada encima
    acciones_adl.append(
        Accion(
            nombre='mover_seguro(?X:bloque, ?Y:bloque)',
            parametros=['?X:bloque', '?Y:bloque'],
            precondiciones=Expresion(
                tipo=TipoExpresion.CONJUNCION,
                contenido=[
                    Expresion(TipoExpresion.ATOMICA, 'libre(?X)'),
                    Expresion(TipoExpresion.ATOMICA, 'en(?X, ?Z)'),
                    Expresion(TipoExpresion.ATOMICA, 'libre(?Y)'),
                    # Condición ADL: no existe un bloque ?W sobre ?X (usando negación existencial)
                    Expresion(
                        tipo=TipoExpresion.NEGACION,
                        contenido=Expresion(
                            tipo=TipoExpresion.EXISTENCIAL,
                            contenido=[
                                Expresion(TipoExpresion.ATOMICA, 'sobre(?W, ?X)')
                            ],
                            parametros=['?W:bloque']
                        )
                    )
                ]
            ),
            efectos=Expresion(
                tipo=TipoExpresion.CONJUNCION,
                contenido=[
                    Expresion(TipoExpresion.NEGACION, '¬en(?X, ?Z)'),
                    Expresion(TipoExpresion.ATOMICA, 'en(?X, ?Y)'),
                    Expresion(TipoExpresion.NEGACION, '¬libre(?Y)'),
                    Expresion(TipoExpresion.ATOMICA, 'libre(?Z)')
                ]
            ),
            tipo=TipoPlaneador.ADL
        )
    )
    
    return ProblemaPlanificacion(
        nombre='Mundo de bloques (ADL)',
        objetos=problema_strips.objetos,
        predicados=problema_strips.predicados,
        estado_inicial=problema_strips.estado_inicial,
        metas=problema_strips.metas,
        acciones=acciones_adl,
        tipo=TipoPlaneador.ADL
    )

if __name__ == "__main__":
    print("\n=== PLANIFICACIÓN STRIPS ===")
    problema_strips = ejemplo_bloques_strips()
    planeador_strips = Planeador(problema_strips)
    plan_strips = planeador_strips.planificar()
    
    print("\nPlan encontrado (STRIPS):")
    if plan_strips:
        for i, accion in enumerate(plan_strips, 1):
            print(f"{i}. {accion}")
    else:
        print("No se encontró plan solución")
    
    print("\n=== PLANIFICACIÓN ADL ===")
    problema_adl = ejemplo_bloques_adl()
    planeador_adl = Planeador(problema_adl)
    plan_adl = planeador_adl.planificar()
    
    print("\nPlan encontrado (ADL):")
    if plan_adl:
        for i, accion in enumerate(plan_adl, 1):
            print(f"{i}. {accion}")
    else:
        print("No se encontró plan solución")