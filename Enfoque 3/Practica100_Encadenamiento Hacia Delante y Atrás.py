
# -*- coding: utf-8 -*-  # Especifica la codificación del archivo como UTF-8
"""
Created on Sun Apr 27 14:39:04 2025  # Fecha de creación del archivo

@author: elvin  # Autor del código
"""

"""
Sistema de Encadenamiento en Bases de Conocimiento  # Descripción general

Este código implementa:  # Lista de funcionalidades
1. Encadenamiento hacia adelante (forward chaining)  # Inferencia hacia adelante
2. Encadenamiento hacia atrás (backward chaining)  # Inferencia hacia atrás
3. Representación de hechos y reglas  # Modelado de conocimiento
4. Razonamiento basado en reglas  # Motor de inferencia
5. Explicación de inferencias  # Trazabilidad de conclusiones
"""

from typing import List, Dict, Set, Optional, Tuple  # Tipos para type hints
from collections import defaultdict  # Para diccionarios con valores por defecto

class Hecho:
    """
    Representa un hecho en la base de conocimiento.
    
    Atributos:
        nombre (str): Identificador del hecho  # Nombre único
        valor (bool): Valor de verdad (True/False)  # Estado del hecho
        explicacion (str): Justificación del hecho  # Origen del conocimiento
    """
    def __init__(self, nombre: str, valor: bool, explicacion: str = ""):  # Constructor
        self.nombre = nombre  # Asigna nombre del hecho
        self.valor = valor  # Asigna valor de verdad
        self.explicacion = explicacion  # Asigna explicación
    
    def __repr__(self) -> str:  # Representación formal
        return f"Hecho('{self.nombre}', {self.valor})"  # Formato string
    
    def __eq__(self, other) -> bool:  # Comparación
        return self.nombre == other.nombre and self.valor == other.valor  # Compara nombre y valor
    
    def __hash__(self) -> int:  # Hash para usar en conjuntos
        return hash((self.nombre, self.valor))  # Hash basado en nombre y valor

class Regla:
    """
    Representa una regla de producción (si-entonces).
    
    Atributos:
        antecedentes (Set[str]): Conjunto de nombres de hechos requeridos  # Premisas
        consecuente (str): Nombre del hecho resultante  # Conclusión
        explicacion (str): Justificación de la regla  # Base de la regla
    """
    def __init__(self, antecedentes: Set[str], consecuente: str, explicacion: str = ""):  # Constructor
        self.antecedentes = antecedentes  # Asigna antecedentes
        self.consequente = consecuente  # Asigna consecuente
        self.explicacion = explicacion  # Asigna explicación
    
    def __repr__(self) -> str:  # Representación formal
        return f"Regla(si {self.antecedentes} entonces {self.consequente})"  # Formato regla
    
    def puede_aplicar(self, hechos_actuales: Set[str]) -> bool:  # Verificación aplicabilidad
        """
        Determina si la regla puede aplicarse dados los hechos actuales.
        
        Args:
            hechos_actuales: Conjunto de nombres de hechos conocidos  # Contexto actual
            
        Returns:
            bool: True si todos los antecedentes están presentes  # Puede aplicarse
        """
        return self.antecedentes.issubset(hechos_actuales)  # Todos los antecedentes presentes

class BaseConocimiento:
    """
    Sistema de base de conocimiento con encadenamiento hacia adelante y atrás.
    
    Atributos:
        hechos (Dict[str, Hecho]): Hechos conocidos  # Base de hechos
        reglas (List[Regla]): Reglas de producción  # Base de reglas
        grafo_reglas (Dict[str, List[Regla]]): Mapeo de consecuentes a reglas  # Índice para búsqueda
    """
    def __init__(self):  # Constructor
        self.hechos: Dict[str, Hecho] = {}  # Diccionario de hechos
        self.reglas: List[Regla] = []  # Lista de reglas
        self.grafo_reglas: Dict[str, List[Regla]] = defaultdict(list)  # Grafo de reglas
    
    def agregar_hecho(self, hecho: Hecho) -> None:  # Método para agregar hechos
        """Agrega un hecho a la base de conocimiento."""
        self.hechos[hecho.nombre] = hecho  # Añade al diccionario
    
    def agregar_regla(self, regla: Regla) -> None:  # Método para agregar reglas
        """Agrega una regla y actualiza el grafo de reglas."""
        self.reglas.append(regla)  # Añade a la lista
        self.grafo_reglas[regla.consequente].append(regla)  # Indexa por consecuente
    
    def encadenamiento_adelante(self, objetivo: Optional[str] = None, verbose: bool = False) -> Set[str]:  # Forward chaining
        """
        Realiza encadenamiento hacia adelante (forward chaining).
        
        Args:
            objetivo (str): Opcional, hecho objetivo a inferir  # Meta específica
            verbose (bool): Si True, muestra pasos detallados  # Modo detallado
            
        Returns:
            Set[str]: Conjunto de nuevos hechos inferidos  # Hechos derivados
        """
        nuevos_hechos = set()  # Para almacenar nuevos hechos
        hechos_conocidos = {h for h in self.hechos if self.hechos[h].valor}  # Hechos verdaderos
        cambiado = True  # Flag para controlar iteraciones
        
        if verbose:  # Si modo detallado
            print("\nIniciando encadenamiento hacia adelante...")
            print(f"Hechos iniciales: {hechos_conocidos}")
        
        while cambiado:  # Mientras haya cambios
            cambiado = False  # Reset flag
            
            for regla in self.reglas:  # Para cada regla
                # Verificar si la regla puede aplicarse y no se ha inferido ya su consecuente
                if (regla.puede_aplicar(hechos_conocidos) and 
                    regla.consequente not in hechos_conocidos):
                    
                    # Crear nuevo hecho inferido
                    nuevo_hecho = Hecho(
                        regla.consequente, 
                        True, 
                        f"Inferido por: {regla.explicacion} usando {regla.antecedentes}"
                    )
                    self.agregar_hecho(nuevo_hecho)  # Añade hecho
                    hechos_conocidos.add(regla.consequente)  # Actualiza conocidos
                    nuevos_hechos.add(regla.consequente)  # Añade a nuevos
                    cambiado = True  # Indica cambio
                    
                    if verbose:  # Si modo detallado
                        print(f"Aplicada regla: {regla}")
                        print(f"Nuevo hecho: {regla.consequente}")
                    
                    # Si encontramos el objetivo, terminar
                    if objetivo and objetivo == regla.consequente:
                        return nuevos_hechos  # Termina temprano si se alcanza objetivo
        
        return nuevos_hechos  # Retorna todos los nuevos hechos
    
    def encadenamiento_atras(self, objetivo: str, verbose: bool = False, profundidad: int = 0, max_profundidad: int = 10) -> Tuple[bool, List[str]]:  # Backward chaining
        """
        Realiza encadenamiento hacia atrás (backward chaining) para un objetivo.
        
        Args:
            objetivo (str): Hecho objetivo a demostrar  # Meta a probar
            verbose (bool): Si True, muestra pasos detallados  # Modo detallado
            profundidad (int): Profundidad actual de recursión  # Control de recursión
            max_profundidad (int): Límite máximo de recursión  # Prevención de stack overflow
            
        Returns:
            Tuple[bool, List[str]]: (True si se puede probar, lista de pasos)  # Resultado y traza
        """
        if verbose:  # Si modo detallado
            print("  " * profundidad + f"Objetivo: {objetivo}")
        
        # Evitar recursión infinita
        if profundidad > max_profundidad:  # Si supera límite
            if verbose:
                print("  " * profundidad + "Límite de profundidad alcanzado")
            return False, []  # Retorna fallo
        
        # Caso base: si el hecho ya es conocido
        if objetivo in self.hechos and self.hechos[objetivo].valor:  # Si hecho es verdadero
            if verbose:
                print("  " * profundidad + f"Hecho conocido: {objetivo}")
            return True, [f"Hecho conocido: {objetivo}"]  # Retorna éxito
        
        # Buscar reglas que puedan inferir este objetivo
        reglas_aplicables = self.grafo_reglas.get(objetivo, [])  # Reglas que concluyen objetivo
        
        if not reglas_aplicables:  # Si no hay reglas
            if verbose:
                print("  " * profundidad + f"No hay reglas para inferir {objetivo}")
            return False, []  # Retorna fallo
        
        pasos_totales = []  # Para almacenar pasos de inferencia
        
        for regla in reglas_aplicables:  # Para cada regla aplicable
            if verbose:
                print("  " * profundidad + f"Intentando regla: {regla}")
            
            # Intentar probar todos los antecedentes
            todos_probados = True  # Flag
            pasos_regla = [f"Aplicando regla: {regla}"]  # Pasos de esta regla
            
            for ant in regla.antecedentes:  # Para cada antecedente
                probado, pasos = self.encadenamiento_atras(  # Llamada recursiva
                    ant, verbose, profundidad + 1, max_profundidad
                )
                
                if not probado:  # Si no se puede probar antecedente
                    todos_probados = False
                    break  # Aborta esta regla
                
                pasos_regla.extend(pasos)  # Añade pasos del antecedente
            
            if todos_probados:  # Si todos los antecedentes se probaron
                # Inferir el consecuente
                nuevo_hecho = Hecho(
                    objetivo,
                    True,
                    f"Inferido por: {regla.explicacion} usando {regla.antecedentes}"
                )
                self.agregar_hecho(nuevo_hecho)  # Añade hecho inferido
                
                paso_final = f"Objetivo '{objetivo}' demostrado usando regla: {regla}"
                pasos_regla.append(paso_final)  # Añade paso final
                
                if verbose:
                    print("  " * profundidad + paso_final)
                
                pasos_totales.extend(pasos_regla)  # Añade pasos de esta rama
                return True, pasos_totales  # Retorna éxito
        
        return False, pasos_totales  # Si ninguna regla funcionó
    
    def explicar_hecho(self, nombre_hecho: str) -> None:  # Método de explicación
        """Muestra la explicación de cómo se obtuvo un hecho."""
        if nombre_hecho not in self.hechos:  # Si hecho no existe
            print(f"El hecho '{nombre_hecho}' no existe en la base de conocimiento")
            return
        
        hecho = self.hechos[nombre_hecho]  # Obtiene hecho
        print(f"\nExplicación para '{nombre_hecho}':")  # Encabezado
        print(f"- Valor: {hecho.valor}")  # Muestra valor
        print(f"- Origen: {hecho.explicacion}")  # Muestra explicación
        
        # Si fue inferido por una regla, mostrar información adicional
        if "Inferido por:" in hecho.explicacion:  # Si es inferido
            # Buscar reglas que tengan este hecho como consecuente
            for regla in self.reglas:  # Para cada regla
                if regla.consequente == nombre_hecho:  # Si regla concluye este hecho
                    print("\nRegla utilizada:")  # Detalle de regla
                    print(f"- Antecedentes: {regla.antecedentes}")
                    print(f"- Explicación regla: {regla.explicacion}")

# Ejemplo de uso  # Bloque principal
if __name__ == "__main__":
    print("SISTEMA DE ENCADENAMIENTO HACIA ADELANTE Y ATRÁS")  # Título
    print("=" * 50)  # Separador
    
    # Crear base de conocimiento  # Paso 1: Inicialización
    bc = BaseConocimiento()  # Instancia base de conocimiento
    
    # Agregar hechos iniciales  # Paso 2: Hechos iniciales
    bc.agregar_hecho(Hecho("es_animal", True, "Observación directa"))  # Hecho 1
    bc.agregar_hecho(Hecho("tiene_pelo", True, "Observación directa"))  # Hecho 2
    bc.agregar_hecho(Hecho("da_leche", True, "Observación directa"))  # Hecho 3
    bc.agregar_hecho(Hecho("tiene_plumas", False, "Observación directa"))  # Hecho 4
    
    # Agregar reglas (sistema experto simple)  # Paso 3: Reglas de inferencia
    bc.agregar_regla(Regla(  # Regla 1
        {"es_animal", "tiene_pelo", "da_leche"},  # Antecedentes
        "es_mamifero",  # Consecuente
        "Los mamíferos son animales con pelo que dan leche"  # Explicación
    ))
    
    bc.agregar_regla(Regla(  # Regla 2
        {"es_mamifero", "tiene_pezuñas"},  # Antecedentes
        "es_ungulado",  # Consecuente
        "Los ungulados son mamíferos con pezuñas"  # Explicación
    ))
    
    bc.agregar_regla(Regla(  # Regla 3
        {"es_mamifero", "come_carne"},  # Antecedentes
        "es_carnivoro",  # Consecuente
        "Los carnívoros son mamíferos que comen carne"  # Explicación
    ))
    
    bc.agregar_regla(Regla(  # Regla 4
        {"es_animal", "tiene_plumas"},  # Antecedentes
        "es_ave",  # Consecuente
        "Las aves son animales con plumas"  # Explicación
    ))
    
    # Ejemplo 1: Encadenamiento hacia adelante  # Caso 1: Forward chaining
    print("\nEjemplo 1: Encadenamiento hacia adelante")
    nuevos_hechos = bc.encadenamiento_adelante(verbose=True)  # Ejecuta con modo detallado
    print("\nHechos inferidos hacia adelante:", nuevos_hechos)  # Muestra resultados
    
    # Mostrar estado de la base de conocimiento  # Paso 4: Mostrar estado
    print("\nEstado final de la base de conocimiento:")
    for nombre, hecho in bc.hechos.items():  # Para cada hecho
        print(f"- {nombre}: {hecho.valor}")  # Muestra nombre y valor
    
    # Explicar un hecho inferido  # Paso 5: Explicación
    bc.explicar_hecho("es_mamifero")  # Explica cómo se obtuvo este hecho
    
    # Ejemplo 2: Encadenamiento hacia atrás  # Caso 2: Backward chaining
    print("\nEjemplo 2: Encadenamiento hacia atrás para 'es_ungulado'")
    
    # Agregar hecho adicional necesario  # Paso 6: Añade hecho faltante
    bc.agregar_hecho(Hecho("tiene_pezuñas", True, "Observación directa"))
    
    # Realizar encadenamiento hacia atrás  # Paso 7: Ejecuta backward chaining
    resultado, pasos = bc.encadenamiento_atras("es_ungulado", verbose=True)
    
    print("\nPasos de inferencia:")  # Muestra traza
    for paso in pasos:  # Para cada paso
        print(f"- {paso}")  # Imprime paso
    
    print(f"\n¿Se puede inferir 'es_ungulado'? {'Sí' if resultado else 'No'}")  # Resultado final
    
    # Mostrar estado final  # Paso 8: Estado final
    print("\nEstado final de la base de conocimiento:")
    for nombre, hecho in bc.hechos.items():  # Para cada hecho
        print(f"- {nombre}: {hecho.valor}")  # Muestra nombre y valor
    
    # Explicar el hecho inferido  # Paso 9: Explicación final
    bc.explicar_hecho("es_ungulado")  # Explica cómo se obtuvo este hecho
```