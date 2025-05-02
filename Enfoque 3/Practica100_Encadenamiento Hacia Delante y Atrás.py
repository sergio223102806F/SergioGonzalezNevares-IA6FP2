# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 14:39:04 2025

@author: elvin
"""

"""
Sistema de Encadenamiento en Bases de Conocimiento

Este código implementa:
1. Encadenamiento hacia adelante (forward chaining)
2. Encadenamiento hacia atrás (backward chaining)
3. Representación de hechos y reglas
4. Razonamiento basado en reglas
5. Explicación de inferencias
"""

from typing import List, Dict, Set, Optional, Tuple
from collections import defaultdict

class Hecho:
    """
    Representa un hecho en la base de conocimiento.
    
    Atributos:
        nombre (str): Identificador del hecho
        valor (bool): Valor de verdad (True/False)
        explicacion (str): Justificación del hecho
    """
    def __init__(self, nombre: str, valor: bool, explicacion: str = ""):
        self.nombre = nombre
        self.valor = valor
        self.explicacion = explicacion
    
    def __repr__(self) -> str:
        return f"Hecho('{self.nombre}', {self.valor})"
    
    def __eq__(self, other) -> bool:
        return self.nombre == other.nombre and self.valor == other.valor
    
    def __hash__(self) -> int:
        return hash((self.nombre, self.valor))

class Regla:
    """
    Representa una regla de producción (si-entonces).
    
    Atributos:
        antecedentes (Set[str]): Conjunto de nombres de hechos requeridos
        consecuente (str): Nombre del hecho resultante
        explicacion (str): Justificación de la regla
    """
    def __init__(self, antecedentes: Set[str], consecuente: str, explicacion: str = ""):
        self.antecedentes = antecedentes
        self.consecuente = consecuente
        self.explicacion = explicacion
    
    def __repr__(self) -> str:
        return f"Regla(si {self.antecedentes} entonces {self.consecuente})"
    
    def puede_aplicar(self, hechos_actuales: Set[str]) -> bool:
        """
        Determina si la regla puede aplicarse dados los hechos actuales.
        
        Args:
            hechos_actuales: Conjunto de nombres de hechos conocidos
            
        Returns:
            bool: True si todos los antecedentes están presentes
        """
        return self.antecedentes.issubset(hechos_actuales)

class BaseConocimiento:
    """
    Sistema de base de conocimiento con encadenamiento hacia adelante y atrás.
    
    Atributos:
        hechos (Dict[str, Hecho]): Hechos conocidos
        reglas (List[Regla]): Reglas de producción
        grafo_reglas (Dict[str, List[Regla]]): Mapeo de consecuentes a reglas
    """
    def __init__(self):
        self.hechos: Dict[str, Hecho] = {}
        self.reglas: List[Regla] = []
        self.grafo_reglas: Dict[str, List[Regla]] = defaultdict(list)
    
    def agregar_hecho(self, hecho: Hecho) -> None:
        """Agrega un hecho a la base de conocimiento."""
        self.hechos[hecho.nombre] = hecho
    
    def agregar_regla(self, regla: Regla) -> None:
        """Agrega una regla y actualiza el grafo de reglas."""
        self.reglas.append(regla)
        self.grafo_reglas[regla.consecuente].append(regla)
    
    def encadenamiento_adelante(self, objetivo: Optional[str] = None, verbose: bool = False) -> Set[str]:
        """
        Realiza encadenamiento hacia adelante (forward chaining).
        
        Args:
            objetivo (str): Opcional, hecho objetivo a inferir
            verbose (bool): Si True, muestra pasos detallados
            
        Returns:
            Set[str]: Conjunto de nuevos hechos inferidos
        """
        nuevos_hechos = set()
        hechos_conocidos = {h for h in self.hechos if self.hechos[h].valor}
        cambiado = True
        
        if verbose:
            print("\nIniciando encadenamiento hacia adelante...")
            print(f"Hechos iniciales: {hechos_conocidos}")
        
        while cambiado:
            cambiado = False
            
            for regla in self.reglas:
                # Verificar si la regla puede aplicarse y no se ha inferido ya su consecuente
                if (regla.puede_aplicar(hechos_conocidos) and 
                    regla.consecuente not in hechos_conocidos):
                    
                    # Crear nuevo hecho inferido
                    nuevo_hecho = Hecho(
                        regla.consecuente, 
                        True, 
                        f"Inferido por: {regla.explicacion} usando {regla.antecedentes}"
                    )
                    self.agregar_hecho(nuevo_hecho)
                    hechos_conocidos.add(regla.consecuente)
                    nuevos_hechos.add(regla.consecuente)
                    cambiado = True
                    
                    if verbose:
                        print(f"Aplicada regla: {regla}")
                        print(f"Nuevo hecho: {regla.consecuente}")
                    
                    # Si encontramos el objetivo, terminar
                    if objetivo and objetivo == regla.consecuente:
                        return nuevos_hechos
        
        return nuevos_hechos
    
    def encadenamiento_atras(self, objetivo: str, verbose: bool = False, profundidad: int = 0, max_profundidad: int = 10) -> Tuple[bool, List[str]]:
        """
        Realiza encadenamiento hacia atrás (backward chaining) para un objetivo.
        
        Args:
            objetivo (str): Hecho objetivo a demostrar
            verbose (bool): Si True, muestra pasos detallados
            profundidad (int): Profundidad actual de recursión
            max_profundidad (int): Límite máximo de recursión
            
        Returns:
            Tuple[bool, List[str]]: (True si se puede probar, lista de pasos)
        """
        if verbose:
            print("  " * profundidad + f"Objetivo: {objetivo}")
        
        # Evitar recursión infinita
        if profundidad > max_profundidad:
            if verbose:
                print("  " * profundidad + "Límite de profundidad alcanzado")
            return False, []
        
        # Caso base: si el hecho ya es conocido
        if objetivo in self.hechos and self.hechos[objetivo].valor:
            if verbose:
                print("  " * profundidad + f"Hecho conocido: {objetivo}")
            return True, [f"Hecho conocido: {objetivo}"]
        
        # Buscar reglas que puedan inferir este objetivo
        reglas_aplicables = self.grafo_reglas.get(objetivo, [])
        
        if not reglas_aplicables:
            if verbose:
                print("  " * profundidad + f"No hay reglas para inferir {objetivo}")
            return False, []
        
        pasos_totales = []
        
        for regla in reglas_aplicables:
            if verbose:
                print("  " * profundidad + f"Intentando regla: {regla}")
            
            # Intentar probar todos los antecedentes
            todos_probados = True
            pasos_regla = [f"Aplicando regla: {regla}"]
            
            for ant in regla.antecedentes:
                probado, pasos = self.encadenamiento_atras(
                    ant, verbose, profundidad + 1, max_profundidad
                )
                
                if not probado:
                    todos_probados = False
                    break
                
                pasos_regla.extend(pasos)
            
            if todos_probados:
                # Todos los antecedentes probados, podemos inferir el consecuente
                nuevo_hecho = Hecho(
                    objetivo,
                    True,
                    f"Inferido por: {regla.explicacion} usando {regla.antecedentes}"
                )
                self.agregar_hecho(nuevo_hecho)
                
                paso_final = f"Objetivo '{objetivo}' demostrado usando regla: {regla}"
                pasos_regla.append(paso_final)
                
                if verbose:
                    print("  " * profundidad + paso_final)
                
                pasos_totales.extend(pasos_regla)
                return True, pasos_totales
        
        return False, pasos_totales
    
    def explicar_hecho(self, nombre_hecho: str) -> None:
        """Muestra la explicación de cómo se obtuvo un hecho."""
        if nombre_hecho not in self.hechos:
            print(f"El hecho '{nombre_hecho}' no existe en la base de conocimiento")
            return
        
        hecho = self.hechos[nombre_hecho]
        print(f"\nExplicación para '{nombre_hecho}':")
        print(f"- Valor: {hecho.valor}")
        print(f"- Origen: {hecho.explicacion}")
        
        # Si fue inferido por una regla, mostrar información adicional
        if "Inferido por:" in hecho.explicacion:
            # Buscar reglas que tengan este hecho como consecuente
            for regla in self.reglas:
                if regla.consecuente == nombre_hecho:
                    print("\nRegla utilizada:")
                    print(f"- Antecedentes: {regla.antecedentes}")
                    print(f"- Explicación regla: {regla.explicacion}")

# Ejemplo de uso
if __name__ == "__main__":
    print("SISTEMA DE ENCADENAMIENTO HACIA ADELANTE Y ATRÁS")
    print("=" * 50)
    
    # Crear base de conocimiento
    bc = BaseConocimiento()
    
    # Agregar hechos iniciales
    bc.agregar_hecho(Hecho("es_animal", True, "Observación directa"))
    bc.agregar_hecho(Hecho("tiene_pelo", True, "Observación directa"))
    bc.agregar_hecho(Hecho("da_leche", True, "Observación directa"))
    bc.agregar_hecho(Hecho("tiene_plumas", False, "Observación directa"))
    
    # Agregar reglas (sistema experto simple)
    bc.agregar_regla(Regla(
        {"es_animal", "tiene_pelo", "da_leche"},
        "es_mamifero",
        "Los mamíferos son animales con pelo que dan leche"
    ))
    
    bc.agregar_regla(Regla(
        {"es_mamifero", "tiene_pezuñas"},
        "es_ungulado",
        "Los ungulados son mamíferos con pezuñas"
    ))
    
    bc.agregar_regla(Regla(
        {"es_mamifero", "come_carne"},
        "es_carnivoro",
        "Los carnívoros son mamíferos que comen carne"
    ))
    
    bc.agregar_regla(Regla(
        {"es_animal", "tiene_plumas"},
        "es_ave",
        "Las aves son animales con plumas"
    ))
    
    # Ejemplo 1: Encadenamiento hacia adelante
    print("\nEjemplo 1: Encadenamiento hacia adelante")
    nuevos_hechos = bc.encadenamiento_adelante(verbose=True)
    print("\nHechos inferidos hacia adelante:", nuevos_hechos)
    
    # Mostrar estado de la base de conocimiento
    print("\nEstado final de la base de conocimiento:")
    for nombre, hecho in bc.hechos.items():
        print(f"- {nombre}: {hecho.valor}")
    
    # Explicar un hecho inferido
    bc.explicar_hecho("es_mamifero")
    
    # Ejemplo 2: Encadenamiento hacia atrás
    print("\nEjemplo 2: Encadenamiento hacia atrás para 'es_ungulado'")
    
    # Agregar hecho adicional necesario
    bc.agregar_hecho(Hecho("tiene_pezuñas", True, "Observación directa"))
    
    # Realizar encadenamiento hacia atrás
    resultado, pasos = bc.encadenamiento_atras("es_ungulado", verbose=True)
    
    print("\nPasos de inferencia:")
    for paso in pasos:
        print(f"- {paso}")
    
    print(f"\n¿Se puede inferir 'es_ungulado'? {'Sí' if resultado else 'No'}")
    
    # Mostrar estado final
    print("\nEstado final de la base de conocimiento:")
    for nombre, hecho in bc.hechos.items():
        print(f"- {nombre}: {hecho.valor}")
    
    # Explicar el hecho inferido
    bc.explicar_hecho("es_ungulado")