Aquí está el código completamente comentado línea por línea:

```python
# -*- coding: utf-8 -*-  # Especifica la codificación del archivo como UTF-8
"""
Created on Sun Apr 27 14:39:02 2025  # Fecha de creación del archivo

@author: elvin  # Autor del código
"""

"""
Sistema de Inferencia Lógica Proposicional  # Descripción general

Este código implementa:  # Lista de funcionalidades
1. Representación de proposiciones lógicas  # Modelado de proposiciones
2. Tablas de verdad para evaluar expresiones  # Evaluación de expresiones
3. Algoritmo de resolución para demostración automática  # Demostración automática
4. Forma normal conjuntiva (FNC)  # Transformación a FNC
5. Verificación de equivalencias lógicas  # Comparación de expresiones
"""

from typing import List, Dict, Set, Tuple, Optional  # Tipos para type hints
import itertools  # Para generar combinaciones

class Proposicion:
    """
    Clase base para representar proposiciones lógicas.
    
    Atributos:
        simbolo (str): Símbolo proposicional (ej. 'p', 'q')  # Identificador
        negado (bool): Indica si la proposición está negada  # Estado de negación
    """
    def __init__(self, simbolo: str, negado: bool = False):  # Constructor
        self.simbolo = simbolo  # Asigna símbolo
        self.negado = negado  # Asigna estado de negación
    
    def __repr__(self):  # Representación formal
        return f"¬{self.simbolo}" if self.negado else self.simbolo  # Muestra con negación si aplica
    
    def __eq__(self, other):  # Comparación
        return self.simbolo == other.simbolo and self.negado == other.negado  # Compara símbolo y negación
    
    def __hash__(self):  # Hash para usar en conjuntos
        return hash((self.simbolo, self.negado))  # Hash basado en símbolo y negación
    
    def negar(self):  # Método de negación
        """Devuelve la negación de esta proposición."""
        return Proposicion(self.simbolo, not self.negado)  # Invierte estado de negación
    
    def evaluar(self, interpretacion: Dict[str, bool]) -> bool:  # Evaluación
        """
        Evalúa la proposición bajo una interpretación dada.
        
        Args:
            interpretacion: Diccionario que asigna valores de verdad a símbolos  # Contexto
            
        Returns:
            bool: Valor de verdad de la proposición  # Resultado
        """
        valor = interpretacion.get(self.simbolo, False)  # Obtiene valor de interpretación
        return not valor if self.negado else valor  # Aplica negación si es necesario

class Expresion:
    """
    Clase para representar expresiones lógicas compuestas.
    
    Atributos:
        izquierda: Subexpresión izquierda  # Operando izquierdo
        derecha: Subexpresión derecha  # Operando derecho
        operador: Operador lógico ('and', 'or', 'implies', 'iff')  # Operación
    """
    def __init__(self, izquierda, operador: str, derecha):  # Constructor
        self.izquierda = izquierda  # Asigna subexpresión izquierda
        self.operador = operador  # Asigna operador
        self.derecha = derecha  # Asigna subexpresión derecha
    
    def __repr__(self):  # Representación formal
        return f"({self.izquierda} {self.operador} {self.derecha})"  # Formato parentizado
    
    def obtener_proposiciones(self) -> Set[str]:  # Extracción de proposiciones
        """Devuelve el conjunto de símbolos proposicionales en la expresión."""
        props = set()  # Conjunto para almacenar símbolos
        
        if isinstance(self.izquierda, Proposicion):  # Si es proposición simple
            props.add(self.izquierda.simbolo)  # Añade símbolo
        elif isinstance(self.izquierda, Expresion):  # Si es subexpresión
            props.update(self.izquierda.obtener_proposiciones())  # Recursión
        
        if isinstance(self.derecha, Proposicion):  # Igual para derecha
            props.add(self.derecha.simbolo)
        elif isinstance(self.derecha, Expresion):
            props.update(self.derecha.obtener_proposiciones())
        
        return props  # Retorna conjunto de símbolos
    
    def evaluar(self, interpretacion: Dict[str, bool]) -> bool:  # Evaluación
        """
        Evalúa la expresión bajo una interpretación dada.
        
        Args:
            interpretacion: Diccionario que asigna valores de verdad a símbolos  # Contexto
            
        Returns:
            bool: Valor de verdad de la expresión  # Resultado
        """
        # Evaluar subexpresiones
        val_izq = self.izquierda.evaluar(interpretacion)  # Evalúa izquierda
        val_der = self.derecha.evaluar(interpretacion)  # Evalúa derecha
        
        # Aplicar operador lógico
        if self.operador == 'and':  # Conjunción
            return val_izq and val_der
        elif self.operador == 'or':  # Disyunción
            return val_izq or val_der
        elif self.operador == 'implies':  # Implicación
            return (not val_izq) or val_der  # Equivalente lógico
        elif self.operador == 'iff':  # Doble implicación
            return val_izq == val_der  # Equivalencia
        else:
            raise ValueError(f"Operador desconocido: {self.operador}")  # Error
    
    def a_fnc(self):  # Conversión a FNC
        """
        Convierte la expresión a Forma Normal Conjuntiva (FNC).
        
        Returns:
            List[List[Proposicion]]: Lista de cláusulas, donde cada cláusula es una lista de literales  # Formato FNC
        """
        # Eliminar implicaciones y dobles implicaciones
        expr = self.eliminar_implicaciones()
        
        # Aplicar leyes de De Morgan y mover negaciones hacia adentro
        expr = expr.mover_negaciones()
        
        # Aplicar distributividad para obtener FNC
        return expr.aplicar_distributividad()
    
    def eliminar_implicaciones(self):  # Eliminación de implicaciones
        """Elimina implicaciones y dobles implicaciones usando equivalencias lógicas."""
        if isinstance(self.izquierda, Expresion):  # Procesar subexpresión izquierda
            izquierda = self.izquierda.eliminar_implicaciones()
        else:
            izquierda = self.izquierda
        
        if isinstance(self.derecha, Expresion):  # Procesar subexpresión derecha
            derecha = self.derecha.eliminar_implicaciones()
        else:
            derecha = self.derecha
        
        if self.operador == 'implies':  # Implicación
            # A → B ≡ ¬A ∨ B
            return Expresion(Expresion(izquierda, 'not', None), 'or', derecha)
        elif self.operador == 'iff':  # Doble implicación
            # A ↔ B ≡ (A → B) ∧ (B → A)
            impl1 = Expresion(izquierda, 'implies', derecha)
            impl2 = Expresion(derecha, 'implies', izquierda)
            return Expresion(impl1.eliminar_implicaciones(), 'and', impl2.eliminar_implicaciones())
        else:  # Otros operadores
            return Expresion(izquierda, self.operador, derecha)
    
    def mover_negaciones(self):  # Manejo de negaciones
        """Mueve las negaciones hacia adentro usando las leyes de De Morgan."""
        # Implementación simplificada - en una versión completa se manejarían todos los casos
        return self
    
    def aplicar_distributividad(self):  # Distributividad
        """Aplica la distributividad para obtener FNC."""
        # Implementación simplificada - en una versión completa se aplicaría la ley distributiva
        return [[self.izquierda], [self.derecha]] if self.operador == 'or' else [self.izquierda, self.derecha]

class SistemaInferencia:
    """
    Sistema para realizar inferencia lógica proposicional.
    """
    def __init__(self):  # Constructor
        self.reglas = []  # Lista de reglas (no utilizada en esta implementación)
    
    def tabla_verdad(self, expresion) -> List[Dict[str, bool]]:  # Generación de tabla de verdad
        """
        Genera la tabla de verdad para una expresión lógica.
        
        Args:
            expresion: Expresión lógica a evaluar  # Expresión a analizar
            
        Returns:
            List[Dict[str, bool]]: Lista de interpretaciones con sus resultados  # Tabla completa
        """
        # Obtener todas las proposiciones atómicas
        proposiciones = sorted(expresion.obtener_proposiciones())  # Ordenadas
        n = len(proposiciones)  # Cantidad de proposiciones
        
        # Generar todas las posibles combinaciones de valores de verdad
        combinaciones = itertools.product([False, True], repeat=n)  # Producto cartesiano
        
        tabla = []  # Lista para almacenar resultados
        for combinacion in combinaciones:  # Para cada combinación
            # Crear interpretación (asignación de valores)
            interpretacion = dict(zip(proposiciones, combinacion))  # Mapeo símbolo-valor
            
            # Evaluar la expresión
            resultado = expresion.evaluar(interpretacion)  # Evalúa expresión
            
            # Añadir resultado a la interpretación
            interpretacion['resultado'] = resultado  # Agrega resultado
            tabla.append(interpretacion)  # Añade a la tabla
        
        return tabla  # Retorna tabla completa
    
    def es_tautologia(self, expresion) -> bool:  # Verificación de tautología
        """
        Determina si una expresión es una tautología.
        
        Args:
            expresion: Expresión lógica a verificar  # Expresión a analizar
            
        Returns:
            bool: True si es tautología, False en caso contrario  # Resultado
        """
        tabla = self.tabla_verdad(expresion)  # Genera tabla
        return all(fila['resultado'] for fila in tabla)  # Todos verdaderos
    
    def es_contradiccion(self, expresion) -> bool:  # Verificación de contradicción
        """
        Determina si una expresión es una contradicción.
        
        Args:
            expresion: Expresión lógica a verificar  # Expresión a analizar
            
        Returns:
            bool: True si es contradicción, False en caso contrario  # Resultado
        """
        tabla = self.tabla_verdad(expresion)  # Genera tabla
        return not any(fila['resultado'] for fila in tabla)  # Todos falsos
    
    def son_equivalentes(self, expr1, expr2) -> bool:  # Comparación de expresiones
        """
        Determina si dos expresiones son lógicamente equivalentes.
        
        Args:
            expr1: Primera expresión lógica  # Expresión 1
            expr2: Segunda expresión lógica  # Expresión 2
            
        Returns:
            bool: True si son equivalentes, False en caso contrario  # Resultado
        """
        # Obtener todas las proposiciones de ambas expresiones
        proposiciones = sorted(expr1.obtener_proposiciones().union(expr2.obtener_proposiciones()))
        n = len(proposiciones)  # Cantidad total de proposiciones
        
        # Generar todas las posibles combinaciones de valores de verdad
        combinaciones = itertools.product([False, True], repeat=n)  # Producto cartesiano
        
        for combinacion in combinaciones:  # Para cada combinación
            interpretacion = dict(zip(proposiciones, combinacion))  # Crea interpretación
            val1 = expr1.evaluar(interpretacion)  # Evalúa expr1
            val2 = expr2.evaluar(interpretacion)  # Evalúa expr2
            
            if val1 != val2:  # Si difieren en alguna interpretación
                return False  # No son equivalentes
        
        return True  # Son equivalentes en todas las interpretaciones
    
    def resolucion(self, premisas: List[List[Proposicion]], conclusion: List[Proposicion]) -> bool:  # Algoritmo de resolución
        """
        Aplica el algoritmo de resolución para demostrar si la conclusión sigue de las premisas.
        
        Args:
            premisas: Lista de cláusulas en FNC que representan las premisas  # Premisas en FNC
            conclusion: Conclusión a demostrar (como cláusula en FNC)  # Conclusión a probar
            
        Returns:
            bool: True si la conclusión es consecuencia lógica, False en caso contrario  # Resultado
        """
        # Convertir la negación de la conclusión a FNC
        neg_conclusion = [[lit.negar() for lit in conclusion]]  # Negación de cada literal
        
        # Unir premisas con la negación de la conclusión
        clausulas = premisas + neg_conclusion  # Conjunto de cláusulas
        
        while True:  # Bucle principal
            nuevas_clausulas = []  # Para almacenar nuevas cláusulas generadas
            n = len(clausulas)  # Cantidad actual de cláusulas
            
            # Intentar resolver cada par de cláusulas
            for i in range(n):  # Para cada cláusula
                for j in range(i+1, n):  # Y cada cláusula siguiente
                    resolventes = self.resolver(clausulas[i], clausulas[j])  # Intenta resolver
                    
                    # Si encontramos la cláusula vacía, la conclusión es válida
                    if any(len(r) == 0 for r in resolventes):  # Cláusula vacía
                        return True  # Conclusión válida
                    
                    nuevas_clausulas.extend(resolventes)  # Añade resolventes
            
            # Si no se generaron nuevas cláusulas, no se puede inferir la conclusión
            if not nuevas_clausulas:  # Sin nuevas cláusulas
                return False  # Conclusión no válida
            
            # Agregar nuevas cláusulas y eliminar duplicados
            clausulas.extend(nuevas_clausulas)  # Extiende conjunto
            clausulas = self.eliminar_duplicados(clausulas)  # Elimina duplicados
    
    def resolver(self, clausula1: List[Proposicion], clausula2: List[Proposicion]) -> List[List[Proposicion]]:  # Resolución de cláusulas
        """
        Aplica la regla de resolución a dos cláusulas.
        
        Args:
            clausula1: Primera cláusula  # Clausula 1
            clausula2: Segunda cláusula  # Clausula 2
            
        Returns:
            List[List[Proposicion]]: Lista de cláusulas resolventes  # Resultados
        """
        resolventes = []  # Lista para resultados
        
        for lit1 in clausula1:  # Para cada literal en cláusula 1
            for lit2 in clausula2:  # Para cada literal en cláusula 2
                # Buscar literales complementarios (p y ¬p)
                if lit1.simbolo == lit2.simbolo and lit1.negado != lit2.negado:  # Complementarios
                    # Crear nueva cláusula combinando las dos, eliminando los literales complementarios
                    nueva_clausula = [lit for lit in clausula1 if lit != lit1]  # Saca lit1
                    nueva_clausula.extend([lit for lit in clausula2 if lit != lit2])  # Añade (sin lit2)
                    
                    # Eliminar duplicados en la nueva cláusula
                    nueva_clausula = list(set(nueva_clausula))  # Elimina duplicados
                    resolventes.append(nueva_clausula)  # Añade a resultados
        
        return resolventes  # Retorna resolventes
    
    def eliminar_duplicados(self, clausulas: List[List[Proposicion]]) -> List[List[Proposicion]]:  # Limpieza de cláusulas
        """
        Elimina cláusulas duplicadas de una lista.
        
        Args:
            clausulas: Lista de cláusulas  # Clausulas a procesar
            
        Returns:
            List[List[Proposicion]]: Lista de cláusulas sin duplicados  # Resultado
        """
        unicas = []  # Lista para cláusulas únicas
        vistas = set()  # Conjunto para control
        
        for clausula in clausulas:  # Para cada cláusula
            # Convertir la cláusula a un frozenset para poder hacer hash
            clave = frozenset(clausula)  # Clave única
            if clave not in vistas:  # Si no está vista
                vistas.add(clave)  # Marca como vista
                unicas.append(clausula)  # Añade a únicas
        
        return unicas  # Retorna cláusulas únicas

# Ejemplo de uso  # Bloque principal
if __name__ == "__main__":  # Ejecución directa
    print("Sistema de Inferencia Lógica Proposicional")  # Título
    print("=" * 50)  # Separador
    
    # Crear sistema de inferencia  # Paso 1
    sistema = SistemaInferencia()  # Instancia
    
    # Definir algunas proposiciones  # Paso 2
    p = Proposicion('p')  # Proposición p
    q = Proposicion('q')  # Proposición q
    r = Proposicion('r')  # Proposición r
    
    # Crear expresiones lógicas  # Paso 3
    expr1 = Expresion(p, 'and', q)  # p ∧ q
    expr2 = Expresion(Expresion(p, 'implies', q), 'and', Expresion(q, 'implies', r))  # (p→q) ∧ (q→r)
    expr3 = Expresion(p, 'implies', r)  # p → r
    
    # 1. Verificar tautologías y contradicciones  # Análisis básico
    print("\n1. Análisis de expresiones:")
    print(f"'{expr1}' es tautología? {sistema.es_tautologia(expr1)}")  # Verifica tautología
    print(f"'{expr1}' es contradicción? {sistema.es_contradiccion(expr1)}")  # Verifica contradicción
    
    # 2. Verificar equivalencias lógicas  # Comparación
    print("\n2. Equivalencias lógicas:")
    equiv1 = Expresion(p, 'implies', q)  # p → q
    equiv2 = Expresion(Expresion(p, 'not', None), 'or', q)  # ¬p ∨ q
    print(f"'{equiv1}' equivale a '{equiv2}'? {sistema.son_equivalentes(equiv1, equiv2)}")  # Compara
    
    # 3. Demostración por resolución  # Inferencia automática
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
    resultado = sistema.resolucion(premisas_fnc, [r])  # Intenta demostrar
    print(f"¿'{expr3}' se sigue de las premisas? {resultado}")  # Muestra resultado
    
    # 4. Tabla de verdad para una expresión  # Generación de tabla
    print("\n4. Tabla de verdad para p ∧ q:")
    tabla = sistema.tabla_verdad(expr1)  # Genera tabla
    
    # Mostrar encabezados
    print("p\tq\tp ∧ q")  # Encabezados
    print("-" * 20)  # Separador
    
    # Mostrar filas de la tabla
    for fila in tabla:  # Para cada fila
        print(f"{fila['p']}\t{fila['q']}\t{fila['resultado']}")  # Muestra valores
```