# -*- coding: utf-8 -*-  # Especifica la codificación del archivo como UTF-8
"""
Created on Sun Apr 27 14:39:03 2025  # Fecha de creación del archivo

@author: elvin  # Autor del código
"""

"""
Implementación del Algoritmo de Resolución y Conversión a Forma Normal Conjuntiva  # Descripción general

Este código incluye:  # Lista de funcionalidades
1. Conversión de expresiones lógicas a FNC  # Transformación a FNC
2. Algoritmo de resolución para demostración automática  # Inferencia lógica
3. Simplificación de cláusulas  # Optimización
4. Detección de cláusulas vacías (contradicción)  # Identificación de contradicciones
5. Visualización de pasos de resolución  # Trazabilidad del proceso
"""

from typing import List, Dict, Set, Union, Optional  # Tipos para type hints
from collections import defaultdict  # Para diccionarios con valores por defecto
import itertools  # Para generar combinaciones

class Literal:
    """
    Representa un literal (proposición atómica o su negación).
    
    Atributos:
        simbolo (str): Símbolo proposicional (ej. 'p', 'q')  # Identificador
        negado (bool): Indica si el literal está negado  # Estado de negación
    """
    def __init__(self, simbolo: str, negado: bool = False):  # Constructor
        self.simbolo = simbolo  # Asigna símbolo proposicional
        self.negado = negado  # Asigna estado de negación
    
    def __repr__(self) -> str:  # Representación formal
        return f"¬{self.simbolo}" if self.negado else self.simbolo  # Muestra con negación si aplica
    
    def __eq__(self, other) -> bool:  # Comparación
        return self.simbolo == other.simbolo and self.negado == other.negado  # Compara símbolo y negación
    
    def __hash__(self) -> int:  # Hash para usar en conjuntos
        return hash((self.simbolo, self.negado))  # Hash basado en símbolo y negación
    
    def complemento(self) -> 'Literal':  # Negación del literal
        """Devuelve el complemento (negación) de este literal."""
        return Literal(self.simbolo, not self.negado)  # Invierte estado de negación

class Clausula:
    """
    Representa una cláusula (disyunción de literales) en FNC.
    
    Atributos:
        literales (Set[Literal]): Conjunto de literales en la cláusula  # Elementos de la cláusula
    """
    def __init__(self, literales: Set[Literal]):  # Constructor
        self.literales = literales  # Asigna conjunto de literales
    
    def __repr__(self) -> str:  # Representación formal
        return " ∨ ".join(map(str, sorted(self.literales, key=str)))  # Muestra como disyunción
    
    def __eq__(self, other) -> bool:  # Comparación
        return self.literales == other.literales  # Compara conjuntos de literales
    
    def __hash__(self) -> int:  # Hash para usar en conjuntos
        return hash(frozenset(self.literales))  # Hash basado en literales
    
    def es_vacia(self) -> bool:  # Verificación de cláusula vacía
        """Determina si la cláusula es vacía (contradicción)."""
        return len(self.literales) == 0  # True si no tiene literales
    
    def es_tautologia(self) -> bool:  # Verificación de tautología
        """Determina si la cláusula es una tautología (contiene p y ¬p)."""
        for lit in self.literales:  # Para cada literal
            if lit.complemento() in self.literales:  # Si encuentra su complemento
                return True  # Es tautología
        return False  # No es tautología
    
    def simplificar(self) -> Optional['Clausula']:  # Simplificación
        """
        Simplifica la cláusula eliminando literales redundantes.
        
        Returns:
            Clausula: Cláusula simplificada, o None si es tautología
        """
        # Eliminar literales duplicados
        literales_unicos = set(self.literales)  # Convierte a conjunto para eliminar duplicados
        
        # Verificar si es tautología
        for lit in literales_unicos:  # Para cada literal único
            if lit.complemento() in literales_unicos:  # Si tiene complemento
                return None  # Es tautología (descartar)
        
        return Clausula(literales_unicos)  # Retorna cláusula simplificada

class ExpresionLogica:
    """
    Clase para representar expresiones lógicas y convertirlas a FNC.
    
    Atributos:
        operador (str): Operador lógico ('and', 'or', 'not', 'implies', 'iff')  # Operación principal
        izquierda: Subexpresión izquierda  # Operando izquierdo
        derecha: Subexpresión derecha  # Operando derecho
        simbolo (str): Para proposiciones atómicas  # Símbolo proposicional
    """
    def __init__(self, operador: Optional[str] = None,
                 izquierda = None,
                 derecha = None,
                 simbolo: Optional[str] = None):  # Constructor
        self.operador = operador  # Asigna operador
        self.izquierda = izquierda  # Asigna subexpresión izquierda
        self.derecha = derecha  # Asigna subexpresión derecha
        self.simbolo = simbolo  # Asigna símbolo proposicional
    
    def __repr__(self) -> str:  # Representación formal
        if self.simbolo:  # Si es proposición atómica
            return self.simbolo  # Retorna símbolo
        elif self.operador == 'not':  # Si es negación
            return f"¬{self.izquierda}"  # Muestra con ¬
        else:  # Otros operadores binarios
            return f"({self.izquierda} {self.operador} {self.derecha})"  # Formato parentizado
    
    def a_fnc(self) -> List[Clausula]:  # Conversión a FNC
        """
        Convierte la expresión lógica a Forma Normal Conjuntiva (FNC).
        
        Returns:
            List[Clausula]: Lista de cláusulas en FNC
        """
        # Paso 1: Eliminar implicaciones y dobles implicaciones
        expr_sin_impl = self.eliminar_implicaciones()  # Elimina → y ↔
        
        # Paso 2: Mover negaciones hacia adentro (Leyes de De Morgan)
        expr_neg_int = expr_sin_impl.mover_negaciones()  # Aplica De Morgan
        
        # Paso 3: Aplicar distributividad para obtener FNC
        return expr_neg_int.aplicar_distributividad()  # Convierte a FNC
    
    def eliminar_implicaciones(self) -> 'ExpresionLogica':  # Eliminación de implicaciones
        """Elimina → y ↔ usando equivalencias lógicas."""
        if self.simbolo:  # Si es proposición atómica
            return self  # No hay nada que eliminar
        
        # Procesar recursivamente subexpresiones
        izquierda = self.izquierda.eliminar_implicaciones() if self.izquierda else None
        derecha = self.derecha.eliminar_implicaciones() if self.derecha else None
        
        if self.operador == 'implies':  # Implicación
            # A → B ≡ ¬A ∨ B
            return ExpresionLogica('or', 
                                  ExpresionLogica('not', izquierda),
                                  derecha)
        elif self.operador == 'iff':  # Doble implicación
            # A ↔ B ≡ (A → B) ∧ (B → A)
            impl1 = ExpresionLogica('implies', izquierda, derecha)
            impl2 = ExpresionLogica('implies', derecha, izquierda)
            return ExpresionLogica('and', 
                                  impl1.eliminar_implicaciones(),
                                  impl2.eliminar_implicaciones())
        else:  # Otros operadores
            return ExpresionLogica(self.operador, izquierda, derecha)
    
    def mover_negaciones(self) -> 'ExpresionLogica':  # Movimiento de negaciones
        """Aplica las leyes de De Morgan para mover negaciones hacia adentro."""
        if self.simbolo:  # Si es proposición atómica
            return self  # No hay negaciones que mover
        
        if self.operador == 'not':  # Si es negación
            subexpr = self.izquierda.mover_negaciones()  # Procesar subexpresión
            
            # Doble negación: ¬¬A ≡ A
            if subexpr.operador == 'not':  # Si es doble negación
                return subexpr.izquierda  # Elimina ambas negaciones
            
            # Leyes de De Morgan
            if subexpr.operador == 'and':  # Negación de conjunción
                # ¬(A ∧ B) ≡ ¬A ∨ ¬B
                return ExpresionLogica('or',
                                      ExpresionLogica('not', subexpr.izquierda),
                                      ExpresionLogica('not', subexpr.derecha))
            elif subexpr.operador == 'or':  # Negación de disyunción
                # ¬(A ∨ B) ≡ ¬A ∧ ¬B
                return ExpresionLogica('and',
                                      ExpresionLogica('not', subexpr.izquierda),
                                      ExpresionLogica('not', subexpr.derecha))
        
        # Recursivamente aplicar a subexpresiones
        izquierda = self.izquierda.mover_negaciones() if self.izquierda else None
        derecha = self.derecha.mover_negaciones() if self.derecha else None
        return ExpresionLogica(self.operador, izquierda, derecha)
    
    def aplicar_distributividad(self) -> List[Clausula]:  # Aplicación de distributividad
        """Aplica la ley distributiva para convertir a FNC."""
        if self.simbolo:  # Proposición atómica
            # Cláusula con un literal positivo
            return [Clausula({Literal(self.simbolo)})]
        
        if self.operador == 'not' and self.izquierda.simbolo:  # Negación de átomo
            # Cláusula con un literal negativo
            return [Clausula({Literal(self.izquierda.simbolo, True)})]
        
        if self.operador == 'or':  # Disyunción
            # Distribuir OR sobre AND: A ∨ (B ∧ C) ≡ (A ∨ B) ∧ (A ∨ C)
            izquierda = self.izquierda.aplicar_distributividad()  # Subexpresión izquierda
            derecha = self.derecha.aplicar_distributividad()  # Subexpresión derecha
            
            # Producto cartesiano de cláusulas
            clausulas = []
            for claus_izq in izquierda:  # Para cada cláusula izquierda
                for claus_der in derecha:  # Y cada cláusula derecha
                    # Unir literales de ambas cláusulas
                    nueva_clausula = Clausula(claus_izq.literales.union(claus_der.literales))
                    clausulas.append(nueva_clausula)
            return clausulas
        
        if self.operador == 'and':  # Conjunción
            # Concatenar cláusulas de ambas subexpresiones
            izquierda = self.izquierda.aplicar_distributividad()
            derecha = self.derecha.aplicar_distributividad()
            return izquierda + derecha
        
        raise ValueError(f"Operador no soportado en FNC: {self.operador}")  # Error

class ResolucionProposicional:
    """
    Implementa el algoritmo de resolución para lógica proposicional.
    """
    def __init__(self):  # Constructor
        self.pasos = []  # Registro de pasos de resolución
    
    def resolver(self, clausulas: List[Clausula], verbose: bool = False) -> bool:  # Algoritmo principal
        """
        Aplica el algoritmo de resolución para determinar insatisfacibilidad.
        
        Args:
            clausulas: Lista de cláusulas en FNC  # Premisas
            verbose: Si True, muestra los pasos intermedios  # Modo detallado
            
        Returns:
            bool: True si las cláusulas son insatisfacibles (contradicción), False en caso contrario
        """
        # Simplificar clausulas iniciales (eliminar tautologías y duplicados)
        clausulas_simpl = []
        for claus in clausulas:  # Para cada cláusula
            claus_simpl = claus.simplificar()  # Simplificar
            if claus_simpl and claus_simpl not in clausulas_simpl:  # Si no es tautología y no está duplicada
                clausulas_simpl.append(claus_simpl)  # Añadir a lista simplificada
        
        if verbose:  # Si modo detallado
            print("Cláusulas iniciales simplificadas:")
            for i, claus in enumerate(clausulas_simpl, 1):  # Enumerar cláusulas
                print(f"{i}. {claus}")
            print()
        
        self.pasos = [("Inicio", clausulas_simpl.copy())]  # Registrar paso inicial
        
        while True:  # Bucle principal
            nuevas_clausulas = []  # Para nuevas cláusulas generadas
            n = len(clausulas_simpl)  # Cantidad actual de cláusulas
            
            # Intentar resolver cada par de cláusulas
            for i in range(n):  # Para cada cláusula
                for j in range(i + 1, n):  # Y cada cláusula siguiente
                    resolventes = self.aplicar_resolucion(clausulas_simpl[i], clausulas_simpl[j])  # Resolver
                    
                    for res in resolventes:  # Para cada resolvente
                        res_simpl = res.simplificar()  # Simplificar resolvente
                        
                        # Si encontramos la cláusula vacía, las cláusulas son insatisfacibles
                        if res_simpl and res_simpl.es_vacia():  # Cláusula vacía
                            self.pasos.append(("Resolución", [res_simpl]))  # Registrar paso
                            if verbose:
                                print("¡Cláusula vacía encontrada! Las cláusulas son insatisfacibles.")
                            return True  # Insatisfacible
                        
                        # Agregar resolventes no triviales
                        if res_simpl and res_simpl not in clausulas_simpl and res_simpl not in nuevas_clausulas:
                            nuevas_clausulas.append(res_simpl)  # Añadir resolvente
                            if verbose:  # Mostrar detalle
                                print(f"Resolvente: {res_simpl} (de {clausulas_simpl[i]} y {clausulas_simpl[j]})")
            
            # Si no se generaron nuevas cláusulas, no hay contradicción
            if not nuevas_clausulas:  # Sin nuevos resolventes
                if verbose:
                    print("No se pueden generar más resolventes. Las cláusulas son satisfacibles.")
                return False  # Satisfacible
            
            # Agregar nuevas cláusulas y registrar paso
            clausulas_simpl.extend(nuevas_clausulas)  # Extender lista
            self.pasos.append(("Resolución", nuevas_clausulas.copy()))  # Registrar paso
    
    def aplicar_resolucion(self, claus1: Clausula, claus2: Clausula) -> List[Clausula]:  # Regla de resolución
        """
        Aplica la regla de resolución a dos cláusulas.
        
        Args:
            claus1: Primera cláusula  # Clausula 1
            claus2: Segunda cláusula  # Clausula 2
            
        Returns:
            List[Clausula]: Lista de cláusulas resolventes  # Resultados
        """
        resolventes = []  # Lista para resolventes
        
        # Buscar pares de literales complementarios
        for lit1 in claus1.literales:  # Para cada literal en claus1
            for lit2 in claus2.literales:  # Para cada literal en claus2
                if lit1.complemento() == lit2:  # Si son complementarios
                    # Crear nueva cláusula combinando las dos, eliminando los literales complementarios
                    nuevos_literales = set()  # Conjunto para nuevos literales
                    
                    # Agregar literales de claus1 excepto lit1
                    for lit in claus1.literales:
                        if lit != lit1:
                            nuevos_literales.add(lit)
                    
                    # Agregar literales de claus2 excepto lit2
                    for lit in claus2.literales:
                        if lit != lit2:
                            nuevos_literales.add(lit)
                    
                    resolventes.append(Clausula(nuevos_literales))  # Añadir resolvente
        
        return resolventes  # Retornar resolventes
    
    def mostrar_pasos(self):  # Visualización de pasos
        """Muestra los pasos de resolución realizados."""
        print("\nPasos de Resolución:")
        for i, (accion, clausulas) in enumerate(self.pasos):  # Para cada paso
            print(f"\nPaso {i + 1}: {accion}")  # Mostrar acción
            for j, claus in enumerate(clausulas, 1):  # Mostrar cláusulas
                print(f"  {j}. {claus}")

# Ejemplo de uso  # Bloque principal
if __name__ == "__main__":
    print("DEMOSTRACIÓN POR RESOLUCIÓN EN LÓGICA PROPOSICIONAL")  # Título
    print("=" * 60)  # Separador
    
    # Crear expresiones lógicas de ejemplo  # Paso 1: Definir proposiciones
    p = ExpresionLogica(simbolo='p')  # Proposición p
    q = ExpresionLogica(simbolo='q')  # Proposición q
    r = ExpresionLogica(simbolo='r')  # Proposición r
    
    # Ejemplo 1: Demostrar que (p ∨ q) ∧ (¬p ∨ r) ∧ (¬q ∨ ¬r) es insatisfacible  # Caso 1
    print("\nEjemplo 1: Demostrar insatisfacibilidad de (p ∨ q) ∧ (¬p ∨ r) ∧ (¬q ∨ ¬r)")
    
    # Convertir a FNC (ya está en FNC en este caso)  # Expresión en FNC
    expr1 = ExpresionLogica('and',
                           ExpresionLogica('or', p, q),
                           ExpresionLogica('and',
                                          ExpresionLogica('or', ExpresionLogica('not', p), r),
                                          ExpresionLogica('or', ExpresionLogica('not', q), ExpresionLogica('not', r))))
    
    clausulas1 = expr1.a_fnc()  # Obtener cláusulas
    
    # Aplicar resolución  # Paso 2: Resolver
    resolutor = ResolucionProposicional()  # Instanciar resolutor
    resultado = resolutor.resolver(clausulas1, verbose=True)  # Ejecutar con modo detallado
    resolutor.mostrar_pasos()  # Mostrar pasos
    
    print(f"\nResultado: Las cláusulas son {'insatisfacibles' if resultado else 'satisfacibles'}")  # Mostrar resultado
    
    # Ejemplo 2: Demostrar que p ∧ ¬p es una contradicción  # Caso 2
    print("\nEjemplo 2: Demostrar que p ∧ ¬p es una contradicción")
    expr2 = ExpresionLogica('and', p, ExpresionLogica('not', p))  # Expresión
    clausulas2 = expr2.a_fnc()  # Convertir a FNC
    
    resolutor = ResolucionProposicional()  # Nuevo resolutor
    resultado = resolutor.resolver(clausulas2, verbose=True)  # Resolver
    resolutor.mostrar_pasos()  # Mostrar pasos
    
    print(f"\nResultado: p ∧ ¬p es {'insatisfacible' if resultado else 'satisfacible'} (contradicción)")  # Resultado
    
    # Ejemplo 3: Demostrar que (p → q) ∧ p → q es una tautología (usando refutación)  # Caso 3
    print("\nEjemplo 3: Demostrar que (p → q) ∧ p → q es una tautología")
    # Para demostrar que es tautología, negamos la expresión y mostramos que es insatisfacible
    expr_original = ExpresionLogica('implies',
                                   ExpresionLogica('and',
                                                  ExpresionLogica('implies', p, q),
                                                  p),
                                   q)
    
    # Negamos la expresión para refutación  # Paso 1: Negar
    expr_refutacion = ExpresionLogica('not', expr_original)
    
    # Convertir a FNC  # Paso 2: Convertir
    clausulas3 = expr_refutacion.a_fnc()
    
    resolutor = ResolucionProposicional()  # Paso 3: Resolver
    resultado = resolutor.resolver(clausulas3, verbose=True)
    resolutor.mostrar_pasos()
    
    print(f"\nResultado: La expresión original es {'tautología' if resultado else 'no tautología'}")  # Conclus