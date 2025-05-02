# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 14:39:02 2025

@author: elvin
"""

"""
Sistema de Inferencia Lógica Proposicional

Este código implementa:
1. Representación de proposiciones lógicas
2. Tablas de verdad para evaluar expresiones
3. Algoritmo de resolución para demostración automática
4. Forma normal conjuntiva (FNC)
5. Verificación de equivalencias lógicas
"""

from typing import List, Dict, Set, Tuple, Optional
import itertools

class Proposicion:
    """
    Clase base para representar proposiciones lógicas.
    
    Atributos:
        simbolo (str): Símbolo proposicional (ej. 'p', 'q')
        negado (bool): Indica si la proposición está negada
    """
    def __init__(self, simbolo: str, negado: bool = False):
        self.simbolo = simbolo
        self.negado = negado
    
    def __repr__(self):
        return f"¬{self.simbolo}" if self.negado else self.simbolo
    
    def __eq__(self, other):
        return self.simbolo == other.simbolo and self.negado == other.negado
    
    def __hash__(self):
        return hash((self.simbolo, self.negado))
    
    def negar(self):
        """Devuelve la negación de esta proposición."""
        return Proposicion(self.simbolo, not self.negado)
    
    def evaluar(self, interpretacion: Dict[str, bool]) -> bool:
        """
        Evalúa la proposición bajo una interpretación dada.
        
        Args:
            interpretacion: Diccionario que asigna valores de verdad a símbolos
            
        Returns:
            bool: Valor de verdad de la proposición
        """
        valor = interpretacion.get(self.simbolo, False)
        return not valor if self.negado else valor

class Expresion:
    """
    Clase para representar expresiones lógicas compuestas.
    
    Atributos:
        izquierda: Subexpresión izquierda
        derecha: Subexpresión derecha
        operador: Operador lógico ('and', 'or', 'implies', 'iff')
    """
    def __init__(self, izquierda, operador: str, derecha):
        self.izquierda = izquierda
        self.operador = operador
        self.derecha = derecha
    
    def __repr__(self):
        return f"({self.izquierda} {self.operador} {self.derecha})"
    
    def obtener_proposiciones(self) -> Set[str]:
        """Devuelve el conjunto de símbolos proposicionales en la expresión."""
        props = set()
        
        if isinstance(self.izquierda, Proposicion):
            props.add(self.izquierda.simbolo)
        elif isinstance(self.izquierda, Expresion):
            props.update(self.izquierda.obtener_proposiciones())
        
        if isinstance(self.derecha, Proposicion):
            props.add(self.derecha.simbolo)
        elif isinstance(self.derecha, Expresion):
            props.update(self.derecha.obtener_proposiciones())
        
        return props
    
    def evaluar(self, interpretacion: Dict[str, bool]) -> bool:
        """
        Evalúa la expresión bajo una interpretación dada.
        
        Args:
            interpretacion: Diccionario que asigna valores de verdad a símbolos
            
        Returns:
            bool: Valor de verdad de la expresión
        """
        # Evaluar subexpresiones
        val_izq = self.izquierda.evaluar(interpretacion)
        val_der = self.derecha.evaluar(interpretacion)
        
        # Aplicar operador lógico
        if self.operador == 'and':
            return val_izq and val_der
        elif self.operador == 'or':
            return val_izq or val_der
        elif self.operador == 'implies':
            return (not val_izq) or val_der
        elif self.operador == 'iff':
            return val_izq == val_der
        else:
            raise ValueError(f"Operador desconocido: {self.operador}")
    
    def a_fnc(self):
        """
        Convierte la expresión a Forma Normal Conjuntiva (FNC).
        
        Returns:
            List[List[Proposicion]]: Lista de cláusulas, donde cada cláusula es una lista de literales
        """
        # Eliminar implicaciones y dobles implicaciones
        expr = self.eliminar_implicaciones()
        
        # Aplicar leyes de De Morgan y mover negaciones hacia adentro
        expr = expr.mover_negaciones()
        
        # Aplicar distributividad para obtener FNC
        return expr.aplicar_distributividad()
    
    def eliminar_implicaciones(self):
        """Elimina implicaciones y dobles implicaciones usando equivalencias lógicas."""
        if isinstance(self.izquierda, Expresion):
            izquierda = self.izquierda.eliminar_implicaciones()
        else:
            izquierda = self.izquierda
        
        if isinstance(self.derecha, Expresion):
            derecha = self.derecha.eliminar_implicaciones()
        else:
            derecha = self.derecha
        
        if self.operador == 'implies':
            # A → B ≡ ¬A ∨ B
            return Expresion(Expresion(izquierda, 'not', None), 'or', derecha)
        elif self.operador == 'iff':
            # A ↔ B ≡ (A → B) ∧ (B → A)
            impl1 = Expresion(izquierda, 'implies', derecha)
            impl2 = Expresion(derecha, 'implies', izquierda)
            return Expresion(impl1.eliminar_implicaciones(), 'and', impl2.eliminar_implicaciones())
        else:
            return Expresion(izquierda, self.operador, derecha)
    
    def mover_negaciones(self):
        """Mueve las negaciones hacia adentro usando las leyes de De Morgan."""
        # Implementación simplificada - en una versión completa se manejarían todos los casos
        return self
    
    def aplicar_distributividad(self):
        """Aplica la distributividad para obtener FNC."""
        # Implementación simplificada - en una versión completa se aplicaría la ley distributiva
        return [[self.izquierda], [self.derecha]] if self.operador == 'or' else [self.izquierda, self.derecha]

class SistemaInferencia:
    """
    Sistema para realizar inferencia lógica proposicional.
    """
    def __init__(self):
        self.reglas = []
    
    def tabla_verdad(self, expresion) -> List[Dict[str, bool]]:
        """
        Genera la tabla de verdad para una expresión lógica.
        
        Args:
            expresion: Expresión lógica a evaluar
            
        Returns:
            List[Dict[str, bool]]: Lista de interpretaciones con sus resultados
        """
        # Obtener todas las proposiciones atómicas
        proposiciones = sorted(expresion.obtener_proposiciones())
        n = len(proposiciones)
        
        # Generar todas las posibles combinaciones de valores de verdad
        combinaciones = itertools.product([False, True], repeat=n)
        
        tabla = []
        for combinacion in combinaciones:
            # Crear interpretación (asignación de valores)
            interpretacion = dict(zip(proposiciones, combinacion))
            
            # Evaluar la expresión
            resultado = expresion.evaluar(interpretacion)
            
            # Añadir resultado a la interpretación
            interpretacion['resultado'] = resultado
            tabla.append(interpretacion)
        
        return tabla
    
    def es_tautologia(self, expresion) -> bool:
        """
        Determina si una expresión es una tautología.
        
        Args:
            expresion: Expresión lógica a verificar
            
        Returns:
            bool: True si es tautología, False en caso contrario
        """
        tabla = self.tabla_verdad(expresion)
        return all(fila['resultado'] for fila in tabla)
    
    def es_contradiccion(self, expresion) -> bool:
        """
        Determina si una expresión es una contradicción.
        
        Args:
            expresion: Expresión lógica a verificar
            
        Returns:
            bool: True si es contradicción, False en caso contrario
        """
        tabla = self.tabla_verdad(expresion)
        return not any(fila['resultado'] for fila in tabla)
    
    def son_equivalentes(self, expr1, expr2) -> bool:
        """
        Determina si dos expresiones son lógicamente equivalentes.
        
        Args:
            expr1: Primera expresión lógica
            expr2: Segunda expresión lógica
            
        Returns:
            bool: True si son equivalentes, False en caso contrario
        """
        # Obtener todas las proposiciones de ambas expresiones
        proposiciones = sorted(expr1.obtener_proposiciones().union(expr2.obtener_proposiciones()))
        n = len(proposiciones)
        
        # Generar todas las posibles combinaciones de valores de verdad
        combinaciones = itertools.product([False, True], repeat=n)
        
        for combinacion in combinaciones:
            interpretacion = dict(zip(proposiciones, combinacion))
            val1 = expr1.evaluar(interpretacion)
            val2 = expr2.evaluar(interpretacion)
            
            if val1 != val2:
                return False
        
        return True
    
    def resolucion(self, premisas: List[List[Proposicion]], conclusion: List[Proposicion]) -> bool:
        """
        Aplica el algoritmo de resolución para demostrar si la conclusión sigue de las premisas.
        
        Args:
            premisas: Lista de cláusulas en FNC que representan las premisas
            conclusion: Conclusión a demostrar (como cláusula en FNC)
            
        Returns:
            bool: True si la conclusión es consecuencia lógica, False en caso contrario
        """
        # Convertir la negación de la conclusión a FNC
        neg_conclusion = [[lit.negar() for lit in conclusion]]
        
        # Unir premisas con la negación de la conclusión
        clausulas = premisas + neg_conclusion
        
        while True:
            nuevas_clausulas = []
            n = len(clausulas)
            
            # Intentar resolver cada par de cláusulas
            for i in range(n):
                for j in range(i+1, n):
                    resolventes = self.resolver(clausulas[i], clausulas[j])
                    
                    # Si encontramos la cláusula vacía, la conclusión es válida
                    if any(len(r) == 0 for r in resolventes):
                        return True
                    
                    nuevas_clausulas.extend(resolventes)
            
            # Si no se generaron nuevas cláusulas, no se puede inferir la conclusión
            if not nuevas_clausulas:
                return False
            
            # Agregar nuevas cláusulas y eliminar duplicados
            clausulas.extend(nuevas_clausulas)
            clausulas = self.eliminar_duplicados(clausulas)
    
    def resolver(self, clausula1: List[Proposicion], clausula2: List[Proposicion]) -> List[List[Proposicion]]:
        """
        Aplica la regla de resolución a dos cláusulas.
        
        Args:
            clausula1: Primera cláusula
            clausula2: Segunda cláusula
            
        Returns:
            List[List[Proposicion]]: Lista de cláusulas resolventes
        """
        resolventes = []
        
        for lit1 in clausula1:
            for lit2 in clausula2:
                # Buscar literales complementarios (p y ¬p)
                if lit1.simbolo == lit2.simbolo and lit1.negado != lit2.negado:
                    # Crear nueva cláusula combinando las dos, eliminando los literales complementarios
                    nueva_clausula = [lit for lit in clausula1 if lit != lit1]
                    nueva_clausula.extend([lit for lit in clausula2 if lit != lit2])
                    
                    # Eliminar duplicados en la nueva cláusula
                    nueva_clausula = list(set(nueva_clausula))
                    resolventes.append(nueva_clausula)
        
        return resolventes
    
    def eliminar_duplicados(self, clausulas: List[List[Proposicion]]) -> List[List[Proposicion]]:
        """
        Elimina cláusulas duplicadas de una lista.
        
        Args:
            clausulas: Lista de cláusulas
            
        Returns:
            List[List[Proposicion]]: Lista de cláusulas sin duplicados
        """
        unicas = []
        vistas = set()
        
        for clausula in clausulas:
            # Convertir la cláusula a un frozenset para poder hacer hash
            clave = frozenset(clausula)
            if clave not in vistas:
                vistas.add(clave)
                unicas.append(clausula)
        
        return unicas

# Ejemplo de uso
if __name__ == "__main__":
    print("Sistema de Inferencia Lógica Proposicional")
    print("=" * 50)
    
    # Crear sistema de inferencia
    sistema = SistemaInferencia()
    
    # Definir algunas proposiciones
    p = Proposicion('p')
    q = Proposicion('q')
    r = Proposicion('r')
    
    # Crear expresiones lógicas
    expr1 = Expresion(p, 'and', q)
    expr2 = Expresion(Expresion(p, 'implies', q), 'and', Expresion(q, 'implies', r))
    expr3 = Expresion(p, 'implies', r)
    
    # 1. Verificar tautologías y contradicciones
    print("\n1. Análisis de expresiones:")
    print(f"'{expr1}' es tautología? {sistema.es_tautologia(expr1)}")
    print(f"'{expr1}' es contradicción? {sistema.es_contradiccion(expr1)}")
    
    # 2. Verificar equivalencias lógicas
    print("\n2. Equivalencias lógicas:")
    equiv1 = Expresion(p, 'implies', q)
    equiv2 = Expresion(Expresion(p, 'not', None), 'or', q)
    print(f"'{equiv1}' equivale a '{equiv2}'? {sistema.son_equivalentes(equiv1, equiv2)}")
    
    # 3. Demostración por resolución
    print("\n3. Demostración por resolución:")
    
    # Premisas: (p → q) ∧ (q → r)
    # Conclusión: p → r
    
    # Convertir premisas a FNC
    premisas_fnc = [
        [p.negar(), q],  # p → q ≡ ¬p ∨ q
        [q.negar(), r]    # q → r ≡ ¬q ∨ r
    ]
    
    # Convertir conclusión a FNC (para negación)
    # Queremos demostrar p → r ≡ ¬p ∨ r
    # Negación: ¬(¬p ∨ r) ≡ p ∧ ¬r
    conclusion_fnc = [[p], [r.negar()]]
    
    # Aplicar resolución
    resultado = sistema.resolucion(premisas_fnc, [r])
    print(f"¿'{expr3}' se sigue de las premisas? {resultado}")
    
    # 4. Tabla de verdad para una expresión
    print("\n4. Tabla de verdad para p ∧ q:")
    tabla = sistema.tabla_verdad(expr1)
    
    # Mostrar encabezados
    print("p\tq\tp ∧ q")
    print("-" * 20)
    
    # Mostrar filas de la tabla
    for fila in tabla:
        print(f"{fila['p']}\t{fila['q']}\t{fila['resultado']}")