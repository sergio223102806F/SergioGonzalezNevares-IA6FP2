# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 14:36:38 2025

@author: elvin
"""

"""
Implementación de un Sistema de Base de Conocimiento

Este código incluye:
1. Representación de hechos y reglas
2. Encadenamiento hacia adelante y hacia atrás
3. Consultas y agregado de conocimiento
4. Manejo de incertidumbre (opcional)
5. Explicación de inferencias
"""

from typing import Dict, List, Union, Optional

class Hecho:
    """
    Clase para representar hechos en la base de conocimiento.
    
    Atributos:
        nombre (str): Nombre del hecho (ej. "es_mamifero")
        valor (Union[bool, float]): Valor de verdad (True/False) o certeza (0-1)
        explicacion (str): Justificación del hecho
    """
    def __init__(self, nombre: str, valor: Union[bool, float], explicacion: str = ""):
        self.nombre = nombre
        self.valor = valor
        self.explicacion = explicacion
    
    def __repr__(self):
        return f"Hecho(nombre='{self.nombre}', valor={self.valor}, explicacion='{self.explicacion}')"

class Regla:
    """
    Clase para representar reglas en la base de conocimiento.
    
    Atributos:
        antecedentes (List[str]): Lista de hechos requeridos (ej. ["es_animal", "tiene_pelo"])
        consecuente (str): Hecho resultante (ej. "es_mamifero")
        certeza (float): Grado de certeza de la regla (0-1)
        explicacion (str): Justificación de la regla
    """
    def __init__(self, antecedentes: List[str], consecuente: str, certeza: float = 1.0, explicacion: str = ""):
        self.antecedentes = antecedentes
        self.consecuente = consecuente
        self.certeza = certeza
        self.explicacion = explicacion
    
    def __repr__(self):
        return f"Regla(antecedentes={self.antecedentes}, consecuente='{self.consecuente}', certeza={self.certeza})"

class BaseConocimiento:
    """
    Sistema de Base de Conocimiento con capacidades de razonamiento.
    
    Atributos:
        hechos (Dict[str, Hecho]): Diccionario de hechos conocidos
        reglas (List[Regla]): Lista de reglas de inferencia
    """
    def __init__(self):
        self.hechos: Dict[str, Hecho] = {}
        self.reglas: List[Regla] = []
    
    def agregar_hecho(self, hecho: Hecho) -> None:
        """
        Agrega un hecho a la base de conocimiento.
        
        Args:
            hecho (Hecho): Hecho a agregar
        """
        self.hechos[hecho.nombre] = hecho
    
    def agregar_regla(self, regla: Regla) -> None:
        """
        Agrega una regla a la base de conocimiento.
        
        Args:
            regla (Regla): Regla a agregar
        """
        self.reglas.append(regla)
    
    def consultar(self, nombre_hecho: str, usar_explicacion: bool = False) -> Optional[Union[bool, float]]:
        """
        Consulta un hecho en la base de conocimiento.
        
        Args:
            nombre_hecho (str): Nombre del hecho a consultar
            usar_explicacion (bool): Si True, muestra la explicación
            
        Returns:
            Union[bool, float, None]: Valor del hecho o None si no existe
        """
        hecho = self.hechos.get(nombre_hecho)
        if hecho:
            if usar_explicacion:
                print(f"Explicación para '{nombre_hecho}': {hecho.explicacion}")
            return hecho.valor
        return None
    
    def encadenamiento_adelante(self) -> None:
        """
        Realiza encadenamiento hacia adelante para inferir nuevos hechos.
        
        Itera sobre las reglas y aplica aquellas cuyos antecedentes son conocidos.
        """
        cambios = True
        while cambios:
            cambios = False
            for regla in self.reglas:
                # Verificar si todos los antecedentes son conocidos y verdaderos
                todos_verdaderos = all(
                    self.hechos.get(ant) and self.hechos[ant].valor
                    for ant in regla.antecedentes
                )
                
                if todos_verdaderos and regla.consecuente not in self.hechos:
                    # Calcular valor del consecuente (considerando certeza)
                    valor_antecedentes = min(
                        self.hechos[ant].valor for ant in regla.antecedentes
                    )
                    nuevo_valor = valor_antecedentes * regla.certeza
                    
                    # Crear explicación
                    explicacion = f"Inferido por regla: {regla.explicacion}. "
                    explicacion += f"Antecedentes: {', '.join(regla.antecedentes)}"
                    
                    # Agregar nuevo hecho
                    nuevo_hecho = Hecho(regla.consecuente, nuevo_valor, explicacion)
                    self.agregar_hecho(nuevo_hecho)
                    cambios = True
    
    def encadenamiento_atras(self, objetivo: str, profundidad: int = 0, max_profundidad: int = 10) -> bool:
        """
        Realiza encadenamiento hacia atrás para verificar un objetivo.
        
        Args:
            objetivo (str): Nombre del hecho a verificar
            profundidad (int): Profundidad actual de recursión (para evitar ciclos)
            max_profundidad (int): Límite de profundidad de recursión
            
        Returns:
            bool: True si el objetivo puede ser inferido, False en caso contrario
        """
        # Evitar recursión infinita
        if profundidad > max_profundidad:
            return False
        
        # Si el hecho ya existe, retornar su valor
        if objetivo in self.hechos:
            return bool(self.hechos[objetivo].valor)
        
        # Buscar reglas que puedan inferir el objetivo
        for regla in self.reglas:
            if regla.consecuente == objetivo:
                # Verificar si todos los antecedentes pueden ser probados
                todos_probados = all(
                    self.encadenamiento_atras(ant, profundidad + 1, max_profundidad)
                    for ant in regla.antecedentes
                )
                
                if todos_probados:
                    # Calcular valor del consecuente
                    valor_antecedentes = min(
                        self.hechos[ant].valor for ant in regla.antecedentes
                        if ant in self.hechos
                    )
                    nuevo_valor = valor_antecedentes * regla.certeza
                    
                    # Crear explicación
                    explicacion = f"Inferido por regla: {regla.explicacion}. "
                    explicacion += f"Antecedentes: {', '.join(regla.antecedentes)}"
                    
                    # Agregar nuevo hecho
                    self.agregar_hecho(Hecho(objetivo, nuevo_valor, explicacion))
                    return True
        
        return False
    
    def mostrar_conocimiento(self, mostrar_explicaciones: bool = False) -> None:
        """
        Muestra todo el conocimiento almacenado.
        
        Args:
            mostrar_explicaciones (bool): Si True, muestra las explicaciones
        """
        print("\n=== HECHOS ===")
        for nombre, hecho in self.hechos.items():
            valor_str = f"{hecho.valor:.2f}" if isinstance(hecho.valor, float) else str(hecho.valor)
            print(f"- {nombre}: {valor_str}")
            if mostrar_explicaciones and hecho.explicacion:
                print(f"  Explicación: {hecho.explicacion}")
        
        print("\n=== REGLAS ===")
        for i, regla in enumerate(self.reglas, 1):
            print(f"{i}. SI {', '.join(regla.antecedentes)} ENTONCES {regla.consecuente} (Certeza: {regla.certeza:.2f})")
            if mostrar_explicaciones and regla.explicacion:
                print(f"   Explicación: {regla.explicacion}")

# Ejemplo de uso
if __name__ == "__main__":
    print("Sistema de Base de Conocimiento")
    print("=" * 40)
    
    # Crear base de conocimiento
    bc = BaseConocimiento()
    
    # Agregar hechos iniciales (con valores de certeza entre 0 y 1)
    bc.agregar_hecho(Hecho("es_animal", True, "Observación directa"))
    bc.agregar_hecho(Hecho("tiene_pelo", True, "Observación directa"))
    bc.agregar_hecho(Hecho("da_leche", True, "Observación directa"))
    bc.agregar_hecho(Hecho("tiene_plumas", False, "Observación directa"))
    bc.agregar_hecho(Hecho("vuela", False, "Observación directa"))
    bc.agregar_hecho(Hecho("pone_huevos", False, "Observación directa"))
    
    # Agregar reglas (sistema experto simple para clasificación de animales)
    bc.agregar_regla(Regla(
        ["es_animal", "tiene_pelo", "da_leche"],
        "es_mamifero",
        0.9,
        "Los mamíferos son animales con pelo que dan leche"
    ))
    
    bc.agregar_regla(Regla(
        ["es_animal", "tiene_plumas", "vuela", "pone_huevos"],
        "es_ave",
        0.95,
        "Las aves son animales con plumas que vuelan y ponen huevos"
    ))
    
    bc.agregar_regla(Regla(
        ["es_mamifero", "tiene_pezuñas"],
        "es_ungulado",
        0.8,
        "Los ungulados son mamíferos con pezuñas"
    ))
    
    bc.agregar_regla(Regla(
        ["es_mamifero", "come_carne"],
        "es_carnivoro",
        0.85,
        "Los carnívoros son mamíferos que comen carne"
    ))
    
    # Mostrar conocimiento inicial
    print("\nConocimiento inicial:")
    bc.mostrar_conocimiento()
    
    # Realizar encadenamiento hacia adelante
    print("\nRealizando encadenamiento hacia adelante...")
    bc.encadenamiento_adelante()
    
    # Mostrar conocimiento después de inferencia
    print("\nConocimiento después de inferencia:")
    bc.mostrar_conocimiento(mostrar_explicaciones=True)
    
    # Consultar un hecho específico con explicación
    print("\nConsultando un hecho con explicación:")
    resultado = bc.consultar("es_mamifero", usar_explicacion=True)
    print(f"Resultado: {resultado}")
    
    # Realizar encadenamiento hacia atrás para un objetivo
    print("\nRealizando encadenamiento hacia atrás para 'es_ungulado':")
    bc.agregar_hecho(Hecho("tiene_pezuñas", True, "Observación directa"))
    exito = bc.encadenamiento_atras("es_ungulado")
    print(f"¿Se pudo inferir 'es_ungulado'? {'Sí' if exito else 'No'}")
    
    # Mostrar conocimiento final
    print("\nConocimiento final:")
    bc.mostrar_conocimiento(mostrar_explicaciones=True)