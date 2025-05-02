# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 14:39:03 2025

@author: elvin
"""

"""
Implementación del Algoritmo de Resolución y Conversión a Forma Normal Conjuntiva

Este código incluye:
1. Conversión de expresiones lógicas a FNC
2. Algoritmo de resolución para demostración automática
3. Simplificación de cláusulas
4. Detección de cláusulas vacías (contradicción)
5. Visualización de pasos de resolución
"""

from typing import List, Dict, Set, Union, Optional
from collections import defaultdict
import itertools

class Literal:
    """
    Representa un literal (proposición atómica o su negación).
    
    Atributos:
        simbolo (str): Símbolo proposicional (ej. 'p', 'q')
        negado (bool): Indica si el literal está negado
    """
    def __init__(self, simbolo: str, negado: bool = False):
        self.simbolo = simbolo
        self.negado = negado
    
    def __repr__(self) -> str:
        return f"¬{self.simbolo}" if self.negado else self.simbolo
    
    def __eq__(self, other) -> bool:
        return self.simbolo == other.simbolo and self.negado == other.negado
    
    def __hash__(self) -> int:
        return hash((self.simbolo, self.negado))
    
    def complemento(self) -> 'Literal':
        """Devuelve el complemento (negación) de este literal."""
        return Literal(self.simbolo, not self.negado)

class Clausula:
    """
    Representa una cláusula (disyunción de literales) en FNC.
    
    Atributos:
        literales (Set[Literal]): Conjunto de literales en la cláusula
    """
    def __init__(self, literales: Set[Literal]):
        self.literales = literales
    
    def __repr__(self) -> str:
        return " ∨ ".join(map(str, sorted(self.literales, key=str)))
    
    def __eq__(self, other) -> bool:
        return self.literales == other.literales
    
    def __hash__(self) -> int:
        return hash(frozenset(self.literales))
    
    def es_vacia(self) -> bool:
        """Determina si la cláusula es vacía (contradicción)."""
        return len(self.literales) == 0
    
    def es_tautologia(self) -> bool:
        """Determina si la cláusula es una tautología (contiene p y ¬p)."""
        for lit in self.literales:
            if lit.complemento() in self.literales:
                return True
        return False
    
    def simplificar(self) -> Optional['Clausula']:
        """
        Simplifica la cláusula eliminando literales redundantes.
        
        Returns:
            Clausula: Cláusula simplificada, o None si es tautología
        """
        # Eliminar literales duplicados
        literales_unicos = set(self.literales)
        
        # Verificar si es tautología
        for lit in literales_unicos:
            if lit.complemento() in literales_unicos:
                return None
        
        return Clausula(literales_unicos)

class ExpresionLogica:
    """
    Clase para representar expresiones lógicas y convertirlas a FNC.
    
    Atributos:
        operador (str): Operador lógico ('and', 'or', 'not', 'implies', 'iff')
        izquierda: Subexpresión izquierda
        derecha: Subexpresión derecha
        simbolo (str): Para proposiciones atómicas
    """
    def __init__(self, operador: Optional[str] = None,
                 izquierda = None,
                 derecha = None,
                 simbolo: Optional[str] = None):
        self.operador = operador
        self.izquierda = izquierda
        self.derecha = derecha
        self.simbolo = simbolo
    
    def __repr__(self) -> str:
        if self.simbolo:
            return self.simbolo
        elif self.operador == 'not':
            return f"¬{self.izquierda}"
        else:
            return f"({self.izquierda} {self.operador} {self.derecha})"
    
    def a_fnc(self) -> List[Clausula]:
        """
        Convierte la expresión lógica a Forma Normal Conjuntiva (FNC).
        
        Returns:
            List[Clausula]: Lista de cláusulas en FNC
        """
        # Paso 1: Eliminar implicaciones y dobles implicaciones
        expr_sin_impl = self.eliminar_implicaciones()
        
        # Paso 2: Mover negaciones hacia adentro (Leyes de De Morgan)
        expr_neg_int = expr_sin_impl.mover_negaciones()
        
        # Paso 3: Aplicar distributividad para obtener FNC
        return expr_neg_int.aplicar_distributividad()
    
    def eliminar_implicaciones(self) -> 'ExpresionLogica':
        """Elimina → y ↔ usando equivalencias lógicas."""
        if self.simbolo:
            return self
        
        izquierda = self.izquierda.eliminar_implicaciones() if self.izquierda else None
        derecha = self.derecha.eliminar_implicaciones() if self.derecha else None
        
        if self.operador == 'implies':
            # A → B ≡ ¬A ∨ B
            return ExpresionLogica('or', 
                                  ExpresionLogica('not', izquierda),
                                  derecha)
        elif self.operador == 'iff':
            # A ↔ B ≡ (A → B) ∧ (B → A)
            impl1 = ExpresionLogica('implies', izquierda, derecha)
            impl2 = ExpresionLogica('implies', derecha, izquierda)
            return ExpresionLogica('and', 
                                  impl1.eliminar_implicaciones(),
                                  impl2.eliminar_implicaciones())
        else:
            return ExpresionLogica(self.operador, izquierda, derecha)
    
    def mover_negaciones(self) -> 'ExpresionLogica':
        """Aplica las leyes de De Morgan para mover negaciones hacia adentro."""
        if self.simbolo:
            return self
        
        if self.operador == 'not':
            subexpr = self.izquierda.mover_negaciones()
            
            # Doble negación: ¬¬A ≡ A
            if subexpr.operador == 'not':
                return subexpr.izquierda
            
            # Leyes de De Morgan
            if subexpr.operador == 'and':
                # ¬(A ∧ B) ≡ ¬A ∨ ¬B
                return ExpresionLogica('or',
                                      ExpresionLogica('not', subexpr.izquierda),
                                      ExpresionLogica('not', subexpr.derecha))
            elif subexpr.operador == 'or':
                # ¬(A ∨ B) ≡ ¬A ∧ ¬B
                return ExpresionLogica('and',
                                      ExpresionLogica('not', subexpr.izquierda),
                                      ExpresionLogica('not', subexpr.derecha))
        
        # Recursivamente aplicar a subexpresiones
        izquierda = self.izquierda.mover_negaciones() if self.izquierda else None
        derecha = self.derecha.mover_negaciones() if self.derecha else None
        return ExpresionLogica(self.operador, izquierda, derecha)
    
    def aplicar_distributividad(self) -> List[Clausula]:
        """Aplica la ley distributiva para convertir a FNC."""
        if self.simbolo:
            # Proposición atómica: cláusula con un literal positivo
            return [Clausula({Literal(self.simbolo)})]
        
        if self.operador == 'not' and self.izquierda.simbolo:
            # Negación de átomo: cláusula con un literal negativo
            return [Clausula({Literal(self.izquierda.simbolo, True)})]
        
        if self.operador == 'or':
            # Distribuir OR sobre AND: A ∨ (B ∧ C) ≡ (A ∨ B) ∧ (A ∨ C)
            izquierda = self.izquierda.aplicar_distributividad()
            derecha = self.derecha.aplicar_distributividad()
            
            # Producto cartesiano de cláusulas
            clausulas = []
            for claus_izq in izquierda:
                for claus_der in derecha:
                    nueva_clausula = Clausula(claus_izq.literales.union(claus_der.literales))
                    clausulas.append(nueva_clausula)
            return clausulas
        
        if self.operador == 'and':
            # AND de expresiones: concatenar cláusulas
            izquierda = self.izquierda.aplicar_distributividad()
            derecha = self.derecha.aplicar_distributividad()
            return izquierda + derecha
        
        raise ValueError(f"Operador no soportado en FNC: {self.operador}")

class ResolucionProposicional:
    """
    Implementa el algoritmo de resolución para lógica proposicional.
    """
    def __init__(self):
        self.pasos = []  # Registro de pasos de resolución
    
    def resolver(self, clausulas: List[Clausula], verbose: bool = False) -> bool:
        """
        Aplica el algoritmo de resolución para determinar insatisfacibilidad.
        
        Args:
            clausulas: Lista de cláusulas en FNC
            verbose: Si True, muestra los pasos intermedios
            
        Returns:
            bool: True si las cláusulas son insatisfacibles (contradicción), False en caso contrario
        """
        # Simplificar clausulas iniciales (eliminar tautologías y duplicados)
        clausulas_simpl = []
        for claus in clausulas:
            claus_simpl = claus.simplificar()
            if claus_simpl and claus_simpl not in clausulas_simpl:
                clausulas_simpl.append(claus_simpl)
        
        if verbose:
            print("Cláusulas iniciales simplificadas:")
            for i, claus in enumerate(clausulas_simpl, 1):
                print(f"{i}. {claus}")
            print()
        
        self.pasos = [("Inicio", clausulas_simpl.copy())]
        
        while True:
            nuevas_clausulas = []
            n = len(clausulas_simpl)
            
            # Intentar resolver cada par de cláusulas
            for i in range(n):
                for j in range(i + 1, n):
                    resolventes = self.aplicar_resolucion(clausulas_simpl[i], clausulas_simpl[j])
                    
                    for res in resolventes:
                        res_simpl = res.simplificar()
                        
                        # Si encontramos la cláusula vacía, las cláusulas son insatisfacibles
                        if res_simpl and res_simpl.es_vacia():
                            self.pasos.append(("Resolución", [res_simpl]))
                            if verbose:
                                print("¡Cláusula vacía encontrada! Las cláusulas son insatisfacibles.")
                            return True
                        
                        # Agregar resolventes no triviales
                        if res_simpl and res_simpl not in clausulas_simpl and res_simpl not in nuevas_clausulas:
                            nuevas_clausulas.append(res_simpl)
                            if verbose:
                                print(f"Resolvente: {res_simpl} (de {clausulas_simpl[i]} y {clausulas_simpl[j]})")
            
            # Si no se generaron nuevas cláusulas, no hay contradicción
            if not nuevas_clausulas:
                if verbose:
                    print("No se pueden generar más resolventes. Las cláusulas son satisfacibles.")
                return False
            
            # Agregar nuevas cláusulas y registrar paso
            clausulas_simpl.extend(nuevas_clausulas)
            self.pasos.append(("Resolución", nuevas_clausulas.copy()))
    
    def aplicar_resolucion(self, claus1: Clausula, claus2: Clausula) -> List[Clausula]:
        """
        Aplica la regla de resolución a dos cláusulas.
        
        Args:
            claus1: Primera cláusula
            claus2: Segunda cláusula
            
        Returns:
            List[Clausula]: Lista de cláusulas resolventes
        """
        resolventes = []
        
        # Buscar pares de literales complementarios
        for lit1 in claus1.literales:
            for lit2 in claus2.literales:
                if lit1.complemento() == lit2:
                    # Crear nueva cláusula combinando las dos, eliminando los literales complementarios
                    nuevos_literales = set()
                    
                    # Agregar literales de claus1 excepto lit1
                    for lit in claus1.literales:
                        if lit != lit1:
                            nuevos_literales.add(lit)
                    
                    # Agregar literales de claus2 excepto lit2
                    for lit in claus2.literales:
                        if lit != lit2:
                            nuevos_literales.add(lit)
                    
                    resolventes.append(Clausula(nuevos_literales))
        
        return resolventes
    
    def mostrar_pasos(self):
        """Muestra los pasos de resolución realizados."""
        print("\nPasos de Resolución:")
        for i, (accion, clausulas) in enumerate(self.pasos):
            print(f"\nPaso {i + 1}: {accion}")
            for j, claus in enumerate(clausulas, 1):
                print(f"  {j}. {claus}")

# Ejemplo de uso
if __name__ == "__main__":
    print("DEMOSTRACIÓN POR RESOLUCIÓN EN LÓGICA PROPOSICIONAL")
    print("=" * 60)
    
    # Crear expresiones lógicas de ejemplo
    p = ExpresionLogica(simbolo='p')
    q = ExpresionLogica(simbolo='q')
    r = ExpresionLogica(simbolo='r')
    
    # Ejemplo 1: Demostrar que (p ∨ q) ∧ (¬p ∨ r) ∧ (¬q ∨ ¬r) es insatisfacible
    print("\nEjemplo 1: Demostrar insatisfacibilidad de (p ∨ q) ∧ (¬p ∨ r) ∧ (¬q ∨ ¬r)")
    
    # Convertir a FNC (ya está en FNC en este caso)
    expr1 = ExpresionLogica('and',
                           ExpresionLogica('or', p, q),
                           ExpresionLogica('and',
                                          ExpresionLogica('or', ExpresionLogica('not', p), r),
                                          ExpresionLogica('or', ExpresionLogica('not', q), ExpresionLogica('not', r))))
    
    clausulas1 = expr1.a_fnc()
    
    # Aplicar resolución
    resolutor = ResolucionProposicional()
    resultado = resolutor.resolver(clausulas1, verbose=True)
    resolutor.mostrar_pasos()
    
    print(f"\nResultado: Las cláusulas son {'insatisfacibles' if resultado else 'satisfacibles'}")
    
    # Ejemplo 2: Demostrar que p ∧ ¬p es una contradicción
    print("\nEjemplo 2: Demostrar que p ∧ ¬p es una contradicción")
    expr2 = ExpresionLogica('and', p, ExpresionLogica('not', p))
    clausulas2 = expr2.a_fnc()
    
    resolutor = ResolucionProposicional()
    resultado = resolutor.resolver(clausulas2, verbose=True)
    resolutor.mostrar_pasos()
    
    print(f"\nResultado: p ∧ ¬p es {'insatisfacible' if resultado else 'satisfacible'} (contradicción)")
    
    # Ejemplo 3: Demostrar que (p → q) ∧ p → q es una tautología (usando refutación)
    print("\nEjemplo 3: Demostrar que (p → q) ∧ p → q es una tautología")
    # Para demostrar que es tautología, negamos la expresión y mostramos que es insatisfacible
    expr_original = ExpresionLogica('implies',
                                   ExpresionLogica('and',
                                                  ExpresionLogica('implies', p, q),
                                                  p),
                                   q)
    
    # Negamos la expresión para refutación
    expr_refutacion = ExpresionLogica('not', expr_original)
    
    # Convertir a FNC
    clausulas3 = expr_refutacion.a_fnc()
    
    resolutor = ResolucionProposicional()
    resultado = resolutor.resolver(clausulas3, verbose=True)
    resolutor.mostrar_pasos()
    
    print(f"\nResultado: La expresión original es {'tautología' if resultado else 'no tautología'}")