# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 17:21:27 2025

@author: elvin
"""

"""
Este código implementa un sistema básico de Ingeniería del Conocimiento que incluye:
- Base de conocimiento
- Motor de inferencia
- Mecanismo de explicación
- Adquisición de conocimiento
"""

from typing import Dict, List, Tuple, Optional
import json

class BaseConocimiento:
    """
    Clase que representa la base de conocimiento del sistema.
    Almacena hechos y reglas en formato lógico.
    """
    
    def __init__(self):
        self.hechos = set()  # Hechos conocidos
        self.reglas = []     # Reglas en formato (premisas, conclusion)
        
    def agregar_hecho(self, hecho: str):
        """Añade un hecho a la base de conocimiento"""
        self.hechos.add(hecho.lower())
        
    def agregar_regla(self, premisas: List[str], conclusion: str):
        """
        Añade una regla a la base de conocimiento.
        
        Args:
            premisas: Lista de condiciones necesarias
            conclusion: Hecho que se deduce si las premisas son verdaderas
        """
        premisas_normalizadas = [p.lower() for p in premisas]
        conclusion_normalizada = conclusion.lower()
        self.reglas.append((premisas_normalizadas, conclusion_normalizada))
        
    def contiene(self, hecho: str) -> bool:
        """Verifica si un hecho está en la base de conocimiento"""
        return hecho.lower() in self.hechos
    
    def guardar(self, archivo: str):
        """Guarda la base de conocimiento en un archivo JSON"""
        datos = {
            'hechos': list(self.hechos),
            'reglas': self.reglas
        }
        with open(archivo, 'w') as f:
            json.dump(datos, f)
    
    def cargar(self, archivo: str):
        """Carga la base de conocimiento desde un archivo JSON"""
        with open(archivo, 'r') as f:
            datos = json.load(f)
        self.hechos = set(datos['hechos'])
        self.reglas = datos['reglas']

class MotorInferencia:
    """
    Motor de inferencia que aplica razonamiento hacia adelante (encadenamiento directo)
    para derivar nuevos hechos a partir de las reglas y hechos conocidos.
    """
    
    def __init__(self, base_conocimiento: BaseConocimiento):
        self.bc = base_conocimiento
        
    def inferir(self) -> List[str]:
        """
        Ejecuta el motor de inferencia para derivar nuevos hechos.
        
        Returns:
            Lista de nuevos hechos inferidos
        """
        nuevos_hechos = []
        cambios = True
        
        while cambios:
            cambios = False
            for premisas, conclusion in self.bc.reglas:
                # Verificar si todas las premisas se cumplen
                todas_verdad = all(p in self.bc.hechos for p in premisas)
                
                if todas_verdad and conclusion not in self.bc.hechos:
                    self.bc.agregar_hecho(conclusion)
                    nuevos_hechos.append(conclusion)
                    cambios = True
        
        return nuevos_hechos
    
    def explicar(self, hecho: str) -> Optional[str]:
        """
        Genera una explicación de cómo se derivó un hecho.
        
        Args:
            hecho: El hecho a explicar
            
        Returns:
            Cadena con la explicación o None si el hecho no existe
        """
        if not self.bc.contiene(hecho.lower()):
            return None
            
        explicacion = []
        hecho_actual = hecho.lower()
        stack = [(hecho_actual, 0)]  # (hecho, nivel de profundidad)
        
        while stack:
            hecho_actual, nivel = stack.pop()
            espacio = "  " * nivel
            
            # Buscar reglas que concluyan este hecho
            reglas_aplicables = [
                (i, premisas) 
                for i, (premisas, conc) in enumerate(self.bc.reglas) 
                if conc == hecho_actual
            ]
            
            if reglas_aplicables:
                regla_idx, premisas = reglas_aplicables[0]
                explicacion.append(f"{espacio}Por la regla {regla_idx}:")
                explicacion.append(f"{espacio}SI {', '.join(premisas)}")
                explicacion.append(f"{espacio}ENTONCES {hecho_actual}")
                
                # Añadir premisas para explicar
                for p in reversed(premisas):
                    stack.append((p, nivel + 1))
            else:
                explicacion.append(f"{espacio}Hecho básico: {hecho_actual}")
        
        return "\n".join(explicacion)

class SistemaIngenieriaConocimiento:
    """
    Sistema completo de Ingeniería del Conocimiento que integra:
    - Base de conocimiento
    - Motor de inferencia
    - Interfaz para adquisición de conocimiento
    """
    
    def __init__(self):
        self.bc = BaseConocimiento()
        self.motor = MotorInferencia(self.bc)
        
    def cargar_ejemplo_medico(self):
        """Carga un ejemplo de conocimiento médico"""
        # Hechos básicos
        self.bc.agregar_hecho("paciente tiene fiebre")
        self.bc.agregar_hecho("paciente tiene tos")
        
        # Reglas de diagnóstico
        self.bc.agregar_regla(
            ["paciente tiene fiebre", "paciente tiene tos"],
            "posible gripe"
        )
        self.bc.agregar_regla(
            ["paciente tiene fiebre", "paciente tiene erupcion"],
            "posible dengue"
        )
        self.bc.agregar_regla(
            ["posible gripe", "paciente tiene dolor muscular"],
            "diagnostico gripe"
        )
        self.bc.agregar_regla(
            ["posible dengue", "paciente tiene dolor cabeza"],
            "diagnostico dengue"
        )
        
    def interfaz_adquisicion(self):
        """Interfaz simple para adquisición de conocimiento"""
        print("\n=== Adquisición de Conocimiento ===")
        while True:
            print("\n1. Agregar hecho")
            print("2. Agregar regla")
            print("3. Terminar")
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                hecho = input("Ingrese el hecho a agregar: ")
                self.bc.agregar_hecho(hecho)
                print(f"Hecho '{hecho}' agregado.")
            elif opcion == "2":
                print("Ingrese las premisas (una por línea, línea vacía para terminar):")
                premisas = []
                while True:
                    premisa = input("Premisa: ")
                    if not premisa:
                        break
                    premisas.append(premisa)
                
                conclusion = input("Ingrese la conclusión: ")
                self.bc.agregar_regla(premisas, conclusion)
                print("Regla agregada.")
            elif opcion == "3":
                break
    
    def ejecutar_sistema(self):
        """Ejecuta el sistema completo con interfaz de usuario"""
        print("=== Sistema de Ingeniería del Conocimiento ===")
        
        # Cargar ejemplo o adquirir conocimiento
        print("\n¿Desea cargar el ejemplo médico (1) o ingresar conocimiento (2)?")
        opcion = input("Opción: ")
        
        if opcion == "1":
            self.cargar_ejemplo_medico()
            print("Ejemplo médico cargado.")
        elif opcion == "2":
            self.interfaz_adquisicion()
        
        # Mostrar estado inicial
        print("\nEstado inicial de la base de conocimiento:")
        print("Hechos:", self.bc.hechos)
        print("Reglas:", self.bc.reglas)
        
        # Ejecutar inferencia
        input("\nPresione Enter para ejecutar inferencia...")
        nuevos_hechos = self.motor.inferir()
        
        print("\nResultados de la inferencia:")
        print("Nuevos hechos derivados:", nuevos_hechos)
        print("Todos los hechos conocidos:", self.bc.hechos)
        
        # Explicar un hecho
        hecho_explicar = input("\nIngrese un hecho para explicar (o Enter para salir): ")
        if hecho_explicar:
            explicacion = self.motor.explicar(hecho_explicar)
            if explicacion:
                print("\nExplicación:")
                print(explicacion)
            else:
                print("El hecho no existe en la base de conocimiento.")

if __name__ == "__main__":
    sistema = SistemaIngenieriaConocimiento()
    sistema.ejecutar_sistema()