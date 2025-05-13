# -*- coding: utf-8 -*-                                      # Especifica la codificación del archivo como UTF-8
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

from typing import Dict, List, Tuple, Optional                  # Importa tipos para type hints
import json                                                    # Para guardar/cargar la base de conocimiento

class BaseConocimiento:
    """
    Clase que representa la base de conocimiento del sistema.
    Almacena hechos y reglas en formato lógico.
    """
    
    def __init__(self):
        self.hechos = set()                                    # Conjunto para almacenar hechos (evita duplicados)
        self.reglas = []                                       # Lista de reglas (premisas, conclusión)
        
    def agregar_hecho(self, hecho: str):
        """Añade un hecho a la base de conocimiento"""
        self.hechos.add(hecho.lower())                          # Almacena en minúsculas para normalizar
        
    def agregar_regla(self, premisas: List[str], conclusion: str):
        """
        Añade una regla a la base de conocimiento.
        """
        premisas_normalizadas = [p.lower() for p in premisas]   # Normaliza premisas a minúsculas
        conclusion_normalizada = conclusion.lower()             # Normaliza conclusión a minúsculas
        self.reglas.append((premisas_normalizadas, conclusion_normalizada))  # Añade a lista de reglas
        
    def contiene(self, hecho: str) -> bool:
        """Verifica si un hecho está en la base de conocimiento"""
        return hecho.lower() in self.hechos                     # Busca en hechos (case-insensitive)
    
    def guardar(self, archivo: str):
        """Guarda la base de conocimiento en un archivo JSON"""
        datos = {
            'hechos': list(self.hechos),                       # Convierte set a lista para JSON
            'reglas': self.reglas
        }
        with open(archivo, 'w') as f:                          # Abre archivo en modo escritura
            json.dump(datos, f)                                # Escribe datos en formato JSON
    
    def cargar(self, archivo: str):
        """Carga la base de conocimiento desde un archivo JSON"""
        with open(archivo, 'r') as f:                          # Abre archivo en modo lectura
            datos = json.load(f)                               # Carga datos desde JSON
        self.hechos = set(datos['hechos'])                     # Convierte lista a set
        self.reglas = datos['reglas']                          # Carga reglas

class MotorInferencia:
    """
    Motor de inferencia que aplica razonamiento hacia adelante (encadenamiento directo)
    para derivar nuevos hechos a partir de las reglas y hechos conocidos.
    """
    
    def __init__(self, base_conocimiento: BaseConocimiento):
        self.bc = base_conocimiento                            # Asocia el motor con una base de conocimiento
        
    def inferir(self) -> List[str]:
        """
        Ejecuta el motor de inferencia para derivar nuevos hechos.
        """
        nuevos_hechos = []                                     # Lista para nuevos hechos inferidos
        cambios = True                                         # Bandera para controlar iteraciones
        
        while cambios:                                         # Mientras haya cambios
            cambios = False
            for premisas, conclusion in self.bc.reglas:         # Para cada regla
                # Verificar si todas las premisas se cumplen
                todas_verdad = all(p in self.bc.hechos for p in premisas)  # Comprueba todas las premisas
                
                if todas_verdad and conclusion not in self.bc.hechos:  # Si se cumplen y conclusión es nueva
                    self.bc.agregar_hecho(conclusion)           # Añade conclusión a hechos
                    nuevos_hechos.append(conclusion)            # Añade a lista de nuevos hechos
                    cambios = True                              # Indica que hubo cambios
        
        return nuevos_hechos                                   # Retorna hechos nuevos inferidos
    
    def explicar(self, hecho: str) -> Optional[str]:
        """
        Genera una explicación de cómo se derivó un hecho.
        """
        if not self.bc.contiene(hecho.lower()):                 # Si el hecho no existe
            return None                                        # Retorna None
            
        explicacion = []                                        # Lista para líneas de explicación
        hecho_actual = hecho.lower()                           # Normaliza el hecho
        stack = [(hecho_actual, 0)]                            # Pila para búsqueda (hecho, nivel)
        
        while stack:                                           # Mientras haya elementos en la pila
            hecho_actual, nivel = stack.pop()                  # Saca último elemento
            espacio = "  " * nivel                             # Indentación según nivel
            
            # Buscar reglas que concluyan este hecho
            reglas_aplicables = [
                (i, premisas) 
                for i, (premisas, conc) in enumerate(self.bc.reglas) 
                if conc == hecho_actual                         # Filtra reglas que concluyan el hecho
            ]
            
            if reglas_aplicables:                               # Si hay reglas aplicables
                regla_idx, premisas = reglas_aplicables[0]      # Toma la primera regla
                explicacion.append(f"{espacio}Por la regla {regla_idx}:")  # Añade encabezado regla
                explicacion.append(f"{espacio}SI {', '.join(premisas)}")  # Añade premisas
                explicacion.append(f"{espacio}ENTONCES {hecho_actual}")  # Añade conclusión
                
                # Añadir premisas para explicar
                for p in reversed(premisas):                    # Añade premisas en orden inverso
                    stack.append((p, nivel + 1))                # Aumenta nivel de profundidad
            else:
                explicacion.append(f"{espacio}Hecho básico: {hecho_actual}")  # Hecho sin reglas
        
        return "\n".join(explicacion)                          # Une explicación con saltos de línea

class SistemaIngenieriaConocimiento:
    """
    Sistema completo de Ingeniería del Conocimiento que integra:
    - Base de conocimiento
    - Motor de inferencia
    - Interfaz para adquisición de conocimiento
    """
    
    def __init__(self):
        self.bc = BaseConocimiento()                           # Crea base de conocimiento
        self.motor = MotorInferencia(self.bc)                  # Crea motor con esta base
        
    def cargar_ejemplo_medico(self):
        """Carga un ejemplo de conocimiento médico"""
        # Hechos básicos
        self.bc.agregar_hecho("paciente tiene fiebre")         # Hecho 1
        self.bc.agregar_hecho("paciente tiene tos")            # Hecho 2
        
        # Reglas de diagnóstico
        self.bc.agregar_regla(                                 # Regla 1
            ["paciente tiene fiebre", "paciente tiene tos"],
            "posible gripe"
        )
        self.bc.agregar_regla(                                 # Regla 2
            ["paciente tiene fiebre", "paciente tiene erupcion"],
            "posible dengue"
        )
        self.bc.agregar_regla(                                 # Regla 3
            ["posible gripe", "paciente tiene dolor muscular"],
            "diagnostico gripe"
        )
        self.bc.agregar_regla(                                 # Regla 4
            ["posible dengue", "paciente tiene dolor cabeza"],
            "diagnostico dengue"
        )
        
    def interfaz_adquisicion(self):
        """Interfaz simple para adquisición de conocimiento"""
        print("\n=== Adquisición de Conocimiento ===")          # Encabezado
        while True:                                            # Bucle principal
            print("\n1. Agregar hecho")                        # Opción 1
            print("2. Agregar regla")                          # Opción 2
            print("3. Terminar")                               # Opción 3
            opcion = input("Seleccione una opción: ")          # Lee opción
            
            if opcion == "1":                                  # Agregar hecho
                hecho = input("Ingrese el hecho a agregar: ")  # Lee hecho
                self.bc.agregar_hecho(hecho)                   # Añade a base
                print(f"Hecho '{hecho}' agregado.")             # Confirma
            elif opcion == "2":                                # Agregar regla
                print("Ingrese las premisas (una por línea, línea vacía para terminar):")
                premisas = []                                  # Lista para premisas
                while True:
                    premisa = input("Premisa: ")               # Lee premisa
                    if not premisa:                            # Si línea vacía
                        break                                 # Termina entrada
                    premisas.append(premisa)                   # Añade premisa
                
                conclusion = input("Ingrese la conclusión: ")  # Lee conclusión
                self.bc.agregar_regla(premisas, conclusion)    # Añade regla
                print("Regla agregada.")                       # Confirma
            elif opcion == "3":                                # Terminar
                break                                         # Sale del bucle
    
    def ejecutar_sistema(self):
        """Ejecuta el sistema completo con interfaz de usuario"""
        print("=== Sistema de Ingeniería del Conocimiento ===")  # Título
        
        # Cargar ejemplo o adquirir conocimiento
        print("\n¿Desea cargar el ejemplo médico (1) o ingresar conocimiento (2)?")
        opcion = input("Opción: ")                             # Lee opción
        
        if opcion == "1":                                      # Cargar ejemplo
            self.cargar_ejemplo_medico()                       # Ejecuta método
            print("Ejemplo médico cargado.")                    # Confirma
        elif opcion == "2":                                    # Ingresar conocimiento
            self.interfaz_adquisicion()                        # Ejecuta interfaz
        
        # Mostrar estado inicial
        print("\nEstado inicial de la base de conocimiento:")
        print("Hechos:", self.bc.hechos)                       # Muestra hechos
        print("Reglas:", self.bc.reglas)                       # Muestra reglas
        
        # Ejecutar inferencia
        input("\nPresione Enter para ejecutar inferencia...")  # Espera usuario
        nuevos_hechos = self.motor.inferir()                   # Ejecuta inferencia
        
        print("\nResultados de la inferencia:")
        print("Nuevos hechos derivados:", nuevos_hechos)       # Muestra nuevos hechos
        print("Todos los hechos conocidos:", self.bc.hechos)    # Muestra todos los hechos
        
        # Explicar un hecho
        hecho_explicar = input("\nIngrese un hecho para explicar (o Enter para salir): ")
        if hecho_explicar:                                     # Si se ingresó hecho
            explicacion = self.motor.explicar(hecho_explicar)   # Genera explicación
            if explicacion:                                    # Si existe explicación
                print("\nExplicación:")
                print(explicacion)                             # Muestra explicación
            else:
                print("El hecho no existe en la base de conocimiento.")  # Mensaje error

if __name__ == "__main__":
    sistema = SistemaIngenieriaConocimiento()                  # Crea sistema
    sistema.ejecutar_sistema()                                 # Ejecuta sistema principal