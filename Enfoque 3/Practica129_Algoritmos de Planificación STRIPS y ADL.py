# -*- coding: utf-8 -*-                                  # Encoding declaration for Python 2 compatibility

# Importaciones necesarias                               # Import section begins
from typing import Dict, List, Set, Optional, Tuple, Union  # Type hints for better code documentation
from dataclasses import dataclass                        # Decorator for creating classes with less boilerplate
from enum import Enum, auto                              # For creating enumerations
import re                                                # Regular expressions

class TipoPlaneador(Enum):                               # Enumeration for planner types
    """Tipos de algoritmos de planificación implementados"""  # Docstring for the enum
    STRIPS = auto()  # Stanford Research Institute Problem Solver  # Basic STRIPS planner
    ADL = auto()     # Action Description Language (extensión de STRIPS)  # More expressive ADL

class TipoExpresion(Enum):                               # Enumeration for expression types
    """Tipos de expresiones en precondiciones/efectos"""  # Docstring for the enum
    ATOMICA = auto()     # Expresión atómica (ej: "en(A, B)")  # Atomic expression
    NEGACION = auto()    # Negación (ej: "¬en(A, B)")  # Negation
    CONJUNCION = auto()  # AND lógico  # Logical AND
    DISYUNCION = auto()  # OR lógico  # Logical OR
    IMPLICACION = auto() # Implicación  # Implication
    UNIVERSAL = auto()   # Cuantificador universal  # Universal quantifier
    EXISTENCIAL = auto() # Cuantificador existencial  # Existential quantifier

@dataclass                                               # Data class for expressions
class Expresion:
    """Estructura para representar expresiones lógicas"""  # Class docstring
    tipo: TipoExpresion                                   # Expression type from enum
    contenido: Union[str, List['Expresion']               # String for atomics/negations, list for others
    parametros: List[str] = field(default_factory=list)   # For quantifiers

@dataclass                                               # Data class for actions
class Accion:
    """Estructura para representar acciones en STRIPS/ADL"""  # Class docstring
    nombre: str                                          # Action name
    parametros: List[str]                                # Action parameters
    precondiciones: Expresion                            # Preconditions expression
    efectos: Expresion                                   # Effects expression
    tipo: TipoPlaneador                                  # Planner type (STRIPS or ADL)

@dataclass                                               # Data class for planning problems
class ProblemaPlanificacion:
    """Define un problema completo de planificación"""    # Class docstring
    nombre: str                                          # Problem name
    objetos: Dict[str, List[str]]                        # Types and their instances
    predicados: Dict[str, List[str]]                     # Parameter types for predicates
    estado_inicial: Set[str]                             # Initial state facts
    metas: Expresion                                     # Goal expression
    acciones: List[Accion]                               # Available actions
    tipo: TipoPlaneador                                  # Planning type (STRIPS or ADL)

class Planeador:                                         # Main planner class
    """
    Implementación de algoritmos de planificación STRIPS y ADL  # Class docstring
    con búsqueda hacia adelante y hacia atrás
    """
    
    def __init__(self, problema: ProblemaPlanificacion):  # Constructor method
        """Inicializa el planeador con un problema específico"""  # Method docstring
        self.problema = problema                         # Store the planning problem
        self.plan: List[str] = []                        # Plan sequence
        self.estados_visitados: Set[frozenset] = set()   # Visited states
    
    def planificar(self) -> Optional[List[str]]:          # Main planning method
        """
        Encuentra un plan que resuelva el problema      # Method docstring
        
        Returns:
            Optional[List[str]]: Lista de acciones del plan, o None si no hay solución
        """
        if self.problema.tipo == TipoPlaneador.STRIPS:    # Check planner type
            return self._busqueda_hacia_adelante()        # Use forward search for STRIPS
        else:
            return self._busqueda_adelante_adl()         # Use ADL forward search
    
    def _busqueda_hacia_adelante(self) -> Optional[List[str]]:  # Forward search for STRIPS
        """
        Búsqueda hacia adelante para STRIPS (sin variables)  # Method docstring
        
        Returns:
            Optional[List[str]]: Plan encontrado o None
        """
        estado_actual = self.problema.estado_inicial.copy()  # Copy initial state
        self.estados_visitados.add(frozenset(estado_actual))  # Mark as visited
        
        for _ in range(100):                          # Limit steps to avoid infinite loops
            if self._satisface(estado_actual, self.problema.metas):  # Check if goal is satisfied
                return self.plan                      # Return plan if goal reached
            
            acciones_aplicables = []                  # Find applicable actions
            for accion in self.problema.acciones:     # Check each action
                if accion.tipo != TipoPlaneador.STRIPS:  # Skip non-STRIPS actions
                    continue
                    
                instancias = self._instanciar_parametros(accion)  # Instantiate parameters
                for instancia in instancias:          # For each parameter instantiation
                    accion_instanciada = self._instanciar_accion(accion, instancia)  # Instantiate action
                    if self._es_aplicable(estado_actual, accion_instanciada.precondiciones):  # Check preconditions
                        acciones_aplicables.append(accion_instanciada)  # Add to applicable
            
            if not acciones_aplicables:               # If no applicable actions
                return None                          # No solution found
            
            accion_elegida = acciones_aplicables[0]   # Simple strategy: pick first
            self.plan.append(accion_elegida.nombre)   # Add to plan
            
            estado_actual = self._aplicar_efectos(estado_actual, accion_elegida.efectos)  # Apply effects
            
            estado_frozen = frozenset(estado_actual)  # Check for cycles
            if estado_frozen in self.estados_visitados:
                return None                          # Cycle detected
            self.estados_visitados.add(estado_frozen)  # Mark state as visited
        
        return None                                  # Step limit reached
    
    def _busqueda_adelante_adl(self) -> Optional[List[str]]:  # Forward search for ADL
        """
        Búsqueda hacia adelante para ADL (maneja expresiones complejas)  # Method docstring
        
        Returns:
            Optional[List[str]]: Plan encontrado o None
        """
        estado_actual = self.problema.estado_inicial.copy()  # Copy initial state
        self.estados_visitados.add(frozenset(estado_actual))  # Mark as visited
        
        for _ in range(100):                          # Limit steps
            if self._satisface(estado_actual, self.problema.metas):  # Check goal
                return self.plan                      # Return plan if goal reached
            
            acciones_aplicables = []                  # Find applicable actions
            for accion in self.problema.acciones:     # For each action
                sustituciones = self._encontrar_sustituciones(estado_actual, accion.precondiciones, {})  # Find substitutions
                for sustitucion in sustituciones:      # For each valid substitution
                    accion_instanciada = self._instanciar_accion(accion, sustitucion)  # Instantiate action
                    acciones_aplicables.append(accion_instanciada)  # Add to applicable
            
            if not acciones_aplicables:               # If no applicable actions
                return None                          # No solution found
            
            accion_elegida = acciones_aplicables[0]   # Simple strategy: pick first
            self.plan.append(accion_elegida.nombre)   # Add to plan
            
            estado_actual = self._aplicar_efectos_adl(estado_actual, accion_elegida.efectos)  # Apply effects
            
            estado_frozen = frozenset(estado_actual)  # Check for cycles
            if estado_frozen in self.estados_visitados:
                return None                          # Cycle detected
            self.estados_visitados.add(estado_frozen)  # Mark state as visited
        
        return None                                  # Step limit reached
    
    def _instanciar_parametros(self, accion: Accion) -> List[Dict[str, str]]:  # Parameter instantiation
        """
        Genera todas las posibles instanciaciones de parámetros para STRIPS  # Method docstring
        
        Args:
            accion (Accion): Acción a instanciar
            
        Returns:
            List[Dict[str, str]]: Lista de sustituciones posibles
        """
        from itertools import product                # Import for Cartesian product
        
        valores_por_parametro = []                  # Possible values for each parameter
        for param in accion.parametros:             # For each parameter
            tipo = param.split(':')[-1] if ':' in param else param  # Get type
            if tipo in self.problema.objetos:       # If type defined
                valores_por_parametro.append(self.problema.objetos[tipo])  # Add objects of type
            else:                                   # If no type
                valores_por_parametro.append([obj for lista in self.problema.objetos.values() for obj in lista])  # All objects
        
        combinaciones = product(*valores_por_parametro)  # All possible combinations
        
        sustituciones = []                          # Convert to substitution dictionaries
        for combo in combinaciones:                 # For each combination
            sustitucion = {}                       # Create substitution
            for i, param in enumerate(accion.parametros):  # For each parameter
                nombre_var = param.split(':')[0] if ':' in param else param  # Get variable name
                sustitucion[nombre_var] = combo[i]  # Add to substitution
            sustituciones.append(sustitucion)       # Add to list
        
        return sustituciones                        # Return all substitutions
    
    def _encontrar_sustituciones(self, estado: Set[str], expr: Expresion, sustitucion: Dict[str, str]) -> List[Dict[str, str]]:  # Find substitutions
        """
        Encuentra sustituciones que satisfagan una expresión (para ADL)  # Method docstring
        
        Args:
            estado (Set[str]): Estado actual
            expr (Expresion): Expresión a satisfacer
            sustitucion (Dict[str, str]): Sustitución acumulada
            
        Returns:
            List[Dict[str, str]]: Lista de sustituciones válidas
        """
        if expr.tipo == TipoExpresion.ATOMICA:      # Atomic expression
            atomo = self._aplicar_sustitucion(expr.contenido, sustitucion)  # Apply substitution
            if atomo in estado:                     # If satisfied
                return [sustitucion]                # Return current substitution
            else:
                return []                          # No valid substitution
            
        elif expr.tipo == TipoExpresion.NEGACION:   # Negation
            atomo = self._aplicar_sustitucion(expr.contenido, sustitucion)  # Apply substitution
            if atomo not in estado:                # If satisfied
                return [sustitucion]                # Return current substitution
            else:
                return []                          # No valid substitution
            
        elif expr.tipo == TipoExpresion.CONJUNCION:  # Conjunction
            sustituciones_actuales = [sustitucion]  # Current substitutions
            for subexpr in expr.contenido:          # For each subexpression
                nuevas_sustituciones = []          # New valid substitutions
                for sust in sustituciones_actuales:  # For each current substitution
                    nuevas_sustituciones.extend(self._encontrar_sustituciones(estado, subexpr, sust))  # Find valid
                sustituciones_actuales = nuevas_sustituciones  # Update current
                if not sustituciones_actuales:      # If none valid
                    break                          # Stop early
            return sustituciones_actuales           # Return valid substitutions
            
        elif expr.tipo == TipoExpresion.UNIVERSAL:  # Universal quantifier
            variable = expr.parametros[0]          # Get variable name
            tipo = expr.parametros[1] if len(expr.parametros) > 1 else None  # Get type if specified
            
            objetos = self.problema.objetos.get(tipo, []) if tipo else \  # Get objects of type
                     [obj for lista in self.problema.objetos.values() for obj in lista]  # Or all objects
            
            sustituciones_actuales = []            # Valid substitutions
            for obj in objetos:                    # For each object
                nueva_sust = sustitucion.copy()    # Copy current substitution
                nueva_sust[variable] = obj         # Add object substitution
                subs = self._encontrar_sustituciones(estado, expr.contenido, nueva_sust)  # Find valid
                if not subs:                       # If none valid for this object
                    return []                      # Universal fails
                sustituciones_actuales.extend(subs)  # Add to valid
            
            return sustituciones_actuales          # Return valid substitutions
            
        else:                                     # Simplified implementation
            return []                             # Doesn't handle all ADL cases
    
    def _aplicar_sustitucion(self, expresion: str, sustitucion: Dict[str, str]) -> str:  # Apply substitution
        """
        Aplica una sustitución a una expresión      # Method docstring
        
        Args:
            expresion (str): Expresión con variables
            sustitucion (Dict[str, str]): Sustitución a aplicar
            
        Returns:
            str: Expresión con variables sustituidas
        """
        for var, valor in sustitucion.items():      # For each variable substitution
            expresion = expresion.replace(f"?{var}", valor)  # Replace variable
        return expresion                            # Return substituted expression
    
    def _instanciar_accion(self, accion: Accion, sustitucion: Dict[str, str]) -> Accion:  # Instantiate action
        """
        Crea una instancia concreta de una acción aplicando una sustitución  # Method docstring
        
        Args:
            accion (Accion): Acción a instanciar
            sustitucion (Dict[str, str]): Sustitución a aplicar
            
        Returns:
            Accion: Acción instanciada
        """
        nombre_instanciado = self._aplicar_sustitucion(accion.nombre, sustitucion)  # Instantiate name
        
        def instanciar_expresion(expr: Expresion) -> Expresion:  # Helper function
            if expr.tipo in [TipoExpresion.ATOMICA, TipoExpresion.NEGACION]:  # Atomic/negation
                contenido = self._aplicar_sustitucion(expr.contenido, sustitucion)  # Substitute
                return Expresion(expr.tipo, contenido)  # Return new expression
            else:                                   # Compound expression
                contenido = [instanciar_expresion(sub) for sub in expr.contenido]  # Recursively instantiate
                return Expresion(expr.tipo, contenido, expr.parametros)  # Return new expression
        
        precond_instanciada = instanciar_expresion(accion.precondiciones)  # Instantiate preconditions
        efectos_instanciados = instanciar_expresion(accion.efectos)  # Instantiate effects
        
        return Accion(                             # Return instantiated action
            nombre=nombre_instanciado,
            parametros=[],
            precondiciones=precond_instanciada,
            efectos=efectos_instanciados,
            tipo=accion.tipo
        )
    
    def _es_aplicable(self, estado: Set[str], precondiciones: Expresion) -> bool:  # Check applicability
        """
        Verifica si las precondiciones se satisfacen en un estado (STRIPS)  # Method docstring
        
        Args:
            estado (Set[str]): Estado actual
            precondiciones (Expresion): Precondiciones a verificar
            
        Returns:
            bool: True si todas las precondiciones se satisfacen
        """
        if precondiciones.tipo == TipoExpresion.ATOMICA:  # Atomic
            return precondiciones.contenido in estado  # Check if in state
        elif precondiciones.tipo == TipoExpresion.NEGACION:  # Negation
            return precondiciones.contenido not in estado  # Check if not in state
        elif precondiciones.tipo == TipoExpresion.CONJUNCION:  # Conjunction
            return all(self._es_aplicable(estado, sub) for sub in precondiciones.contenido)  # Check all
        else:                                   # STRIPS only handles conjunctions
            return False                        # Not applicable
    
    def _satisface(self, estado: Set[str], metas: Expresion) -> bool:  # Check goal satisfaction
        """
        Verifica si un estado satisface las metas  # Method docstring
        
        Args:
            estado (Set[str]): Estado a verificar
            metas (Expresion): Metas a satisfacer
            
        Returns:
            bool: True si el estado satisface las metas
        """
        if metas.tipo == TipoExpresion.ATOMICA:   # Atomic goal
            return metas.contenido in estado      # Check if in state
        elif metas.tipo == TipoExpresion.NEGACION:  # Negation
            return metas.contenido not in estado  # Check if not in state
        elif metas.tipo == TipoExpresion.CONJUNCION:  # Conjunction
            return all(self._satisface(estado, sub) for sub in metas.contenido)  # Check all
        elif metas.tipo == TipoExpresion.DISYUNCION:  # Disjunction
            return any(self._satisface(estado, sub) for sub in metas.contenido)  # Check any
        else:                                   # Simplified implementation
            return False                        # Doesn't handle all cases
    
    def _aplicar_efectos(self, estado: Set[str], efectos: Expresion) -> Set[str]:  # Apply STRIPS effects
        """
        Aplica efectos a un estado (STRIPS)       # Method docstring
        
        Args:
            estado (Set[str]): Estado actual
            efectos (Expresion): Efectos a aplicar
            
        Returns:
            Set[str]: Nuevo estado después de aplicar efectos
        """
        nuevo_estado = estado.copy()             # Copy current state
        
        if efectos.tipo == TipoExpresion.ATOMICA:  # Atomic effect
            nuevo_estado.add(efectos.contenido)   # Add to state
        elif efectos.tipo == TipoExpresion.NEGACION:  # Negation
            nuevo_estado.discard(efectos.contenido[1:])  # Remove from state (without ¬)
        elif efectos.tipo == TipoExpresion.CONJUNCION:  # Conjunction
            for efecto in efectos.contenido:      # Apply each effect
                nuevo_estado = self._aplicar_efectos(nuevo_estado, efecto)  # Recursively apply
        
        return nuevo_estado                       # Return new state
    
    def _aplicar_efectos_adl(self, estado: Set[str], efectos: Expresion) -> Set[str]:  # Apply ADL effects
        """
        Aplica efectos ADL (más complejos que STRIPS)  # Method docstring
        
        Args:
            estado (Set[str]): Estado actual
            efectos (Expresion): Efectos a aplicar
            
        Returns:
            Set[str]: Nuevo estado después de aplicar efectos
        """
        nuevo_estado = estado.copy()             # Copy current state
        
        if efectos.tipo == TipoExpresion.ATOMICA:  # Atomic effect
            nuevo_estado.add(efectos.contenido)   # Add to state
        elif efectos.tipo == TipoExpresion.NEGACION:  # Negation
            nuevo_estado.discard(efectos.contenido[1:])  # Remove from state
        elif efectos.tipo == TipoExpresion.CONJUNCION:  # Conjunction
            for efecto in efectos.contenido:      # Apply each effect
                nuevo_estado = self._aplicar_efectos_adl(nuevo_estado, efecto)  # Recursively apply
        elif efectos.tipo == TipoExpresion.UNIVERSAL:  # Universal quantifier
            variable = efectos.parametros[0]     # Get variable
            tipo = efectos.parametros[1] if len(efectos.parametros) > 1 else None  # Get type
            
            objetos = self.problema.objetos.get(tipo, []) if tipo else \  # Get objects of type
                     [obj for lista in self.problema.objetos.values() for obj in lista]  # Or all objects
            
            for obj in objetos:                  # For each object
                sustitucion = {variable: obj}    # Create substitution
                efecto_instanciado = self._instanciar_expresion(efectos.contenido, sustitucion)  # Instantiate
                nuevo_estado = self._aplicar_efectos_adl(nuevo_estado, efecto_instanciado)  # Apply
        
        return nuevo_estado                       # Return new state
    
    def _instanciar_expresion(self, expr: Expresion, sustitucion: Dict[str, str]) -> Expresion:  # Instantiate expression
        """
        Instancia una expresión aplicando una sustitución  # Method docstring
        
        Args:
            expr (Expresion): Expresión a instanciar
            sustitucion (Dict[str, str]): Sustitución a aplicar
            
        Returns:
            Expresion: Expresión instanciada
        """
        if expr.tipo in [TipoExpresion.ATOMICA, TipoExpresion.NEGACION]:  # Atomic/negation
            contenido = self._aplicar_sustitucion(expr.contenido, sustitucion)  # Substitute
            return Expresion(expr.tipo, contenido)  # Return new expression
        else:                                   # Compound expression
            contenido = [self._instanciar_expresion(sub, sustitucion) for sub in expr.contenido]  # Recursively instantiate
            return Expresion(expr.tipo, contenido, expr.parametros)  # Return new expression

def ejemplo_bloques_strips():                    # STRIPS blocks world example
    """
    Crea y devuelve un problema de planificación STRIPS clásico:  # Function docstring
    el mundo de bloques (apilar, desapilar, mover)
    """
    objetos = {                                 # Define objects
        'bloque': ['A', 'B', 'C', 'D'],        # Blocks
        'ubicacion': ['Mesa', 'A', 'B', 'C', 'D']  # Locations (blocks can be locations)
    }
    
    predicados = {                              # Define predicates
        'en': ['bloque', 'ubicacion'],         # on(block, location)
        'sobre': ['bloque', 'bloque'],         # on(block, block)
        'libre': ['bloque'],                   # clear(block)
        'agarrado': ['bloque']                 # holding(block)
    }
    
    estado_inicial = {                          # Initial state
        'en(A, Mesa)', 'en(B, Mesa)', 'en(C, Mesa)', 'en(D, Mesa)',
        'libre(A)', 'libre(B)', 'libre(C)', 'libre(D)',
        'libre(Mesa)'
    }
    
    metas = Expresion(                         # Goal: A on B, B on C
        tipo=TipoExpresion.CONJUNCION,
        contenido=[
            Expresion(TipoExpresion.ATOMICA, 'sobre(A, B)'),
            Expresion(TipoExpresion.ATOMICA, 'sobre(B, C)')
        ]
    )
    
    acciones = [                               # Define STRIPS actions
        # Pick up a block
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
        
        # Put down a block
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
    
    return ProblemaPlanificacion(               # Return planning problem
        nombre='Mundo de bloques (STRIPS)',
        objetos=objetos,
        predicados=predicados,
        estado_inicial=estado_inicial,
        metas=metas,
        acciones=acciones,
        tipo=TipoPlaneador.STRIPS
    )

if __name__ == "__main__":                     # Main execution
    print("\n=== PLANIFICACIÓN STRIPS ===")     # STRIPS example
    problema_strips = ejemplo_bloques_strips()  # Create problem
    planeador_strips = Planeador(problema_strips)  # Create planner
    plan_strips = planeador_strips.planificar()  # Find plan
    
    print("\nPlan encontrado (STRIPS):")       # Print plan
    if plan_strips:
        for i, accion in enumerate(plan_strips, 1):
            print(f"{i}. {accion}")
    else:
        print("No se encontró plan solución")