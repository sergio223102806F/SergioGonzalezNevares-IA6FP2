```python
# -*- coding: utf-8 -*-                                                     # Define la codificación de caracteres del archivo como UTF-8
"""
Created on Sun Apr 27 17:21:27 2025                                         # Indica la fecha y hora de creación del archivo
                                                                           #
@author: elvin                                                              # Define el autor del archivo
"""

"""
Sistema de diagnóstico basado en reglas causales que implementa:
1. Base de conocimiento con relaciones causales y diagnósticas
2. Motor de inferencia hacia adelante y hacia atrás
3. Mecanismo de explicación de diagnósticos
4. Ejemplos médicos y técnicos
"""

from typing import Dict, List, Set, Tuple, Optional                       # Importa tipos para anotaciones de tipo
from collections import defaultdict                                      # Importa defaultdict desde el módulo collections

# ============================================================================= # Separador de sección
# 1. DEFINICIÓN DEL SISTEMA DE DIAGNÓSTICO                                # Separador de sección
# ============================================================================= # Separador de sección

class SistemaDiagnostico:                                                 # Define una clase llamada SistemaDiagnostico
    """
    Sistema experto para diagnóstico con relaciones causales              # Documentación de la clase SistemaDiagnostico
    
    Componentes:
        - Síntomas <-> Enfermedades (diagnóstico)
        - Enfermedades <-> Complicaciones (causal)
        - Motor de inferencia combinado
    """
    
    def __init__(self):                                                     # Define el constructor de la clase
        # Relaciones diagnóstico: síntoma -> posibles enfermedades         # Comentario de las reglas de diagnóstico
        self.reglas_diagnosticas: Dict[str, List[str]] = defaultdict(list) # Inicializa un diccionario con valores predeterminados como listas
        
        # Relaciones causales: enfermedad -> posibles complicaciones        # Comentario de las reglas causales
        self.reglas_causales: Dict[str, List[str]] = defaultdict(list)     # Inicializa un diccionario con valores predeterminados como listas
        
        # Base de hechos observados                                       # Comentario de la base de hechos observados
        self.hechos_observados: Set[str] = set()                           # Inicializa un conjunto para almacenar los hechos observados
        
        # Historial de inferencias para explicaciones                     # Comentario del historial de inferencias
        self.historial: List[Tuple[str, str]] = []                        # Inicializa una lista para almacenar el historial de inferencias
    
    def agregar_relacion_diagnostica(self, sintoma: str, enfermedad: str): # Define el método para agregar una relación diagnóstica
        """Establece que un síntoma puede indicar una enfermedad"""      # Documentación del método agregar_relacion_diagnostica
        self.reglas_diagnosticas[sintoma].append(enfermedad)              # Agrega la enfermedad a la lista de posibles enfermedades para el síntoma
    
    def agregar_relacion_causal(self, enfermedad: str, complicacion: str): # Define el método para agregar una relación causal
        """Establece que una enfermedad puede causar una complicación"""   # Documentación del método agregar_relacion_causal
        self.reglas_causales[enfermedad].append(complicacion)             # Agrega la complicación a la lista de posibles complicaciones para la enfermedad
    
    def observar(self, hecho: str):                                        # Define el método para registrar un hecho observado
        """Registra un hecho observado (síntoma o hallazgo)"""            # Documentación del método observar
        self.hechos_observados.add(hecho)                                  # Agrega el hecho al conjunto de hechos observados
    
    def diagnosticar(self) -> Dict[str, float]:                            # Define el método para realizar el diagnóstico
        """
        Realiza diagnóstico basado en síntomas observados                 # Documentación del método diagnosticar
        
        Returns:
            Diccionario {enfermedad: probabilidad}                       # Retorna un diccionario con enfermedades y sus probabilidades
        """
        enfermedades_posibles: Dict[str, int] = defaultdict(int)         # Inicializa un diccionario con valores predeterminados como enteros
        total_sintomas = 0                                               # Inicializa un contador para el total de síntomas observados
        
        # Inferencia hacia adelante: síntomas -> enfermedades              # Comentario de la inferencia hacia adelante
        for sintoma in self.hechos_observados:                            # Itera sobre los síntomas observados
            if sintoma in self.reglas_diagnosticas:                        # Si el síntoma está en las reglas diagnósticas
                for enfermedad in self.reglas_diagnosticas[sintoma]:      # Itera sobre las posibles enfermedades para el síntoma
                    enfermedades_posibles[enfermedad] += 1               # Incrementa el contador de la enfermedad
                    self.historial.append((f"Síntoma '{sintoma}'", f"sugiere '{enfermedad}'")) # Agrega la inferencia al historial
                total_sintomas += 1                                      # Incrementa el contador total de síntomas
        
        # Calcular probabilidades relativas                               # Comentario del cálculo de probabilidades
        if not enfermedades_posibles:                                    # Si no hay enfermedades posibles
            return {}                                                    # Retorna un diccionario vacío
        
        max_puntos = max(enfermedades_posibles.values())                 # Obtiene el máximo número de síntomas coincidentes para una enfermedad
        return {                                                         # Retorna un diccionario con las probabilidades de las enfermedades
            enf: (puntos / max_puntos)                                    # Calcula la probabilidad relativa dividiendo los puntos por el máximo
            for enf, puntos in enfermedades_posibles.items()             # Itera sobre las enfermedades y sus puntos
        }
    
    def predecir_complicaciones(self, enfermedad: str) -> List[str]:      # Define el método para predecir complicaciones
        """Predice posibles complicaciones de una enfermedad"""           # Documentación del método predecir_complicaciones
        return self.reglas_causales.get(enfermedad, [])                   # Retorna la lista de complicaciones para la enfermedad, o una lista vacía si no hay
    
    def explicar_diagnostico(self, enfermedad: str) -> str:               # Define el método para explicar el diagnóstico
        """
        Genera una explicación de cómo se llegó a un diagnóstico          # Documentación del método explicar_diagnostico
        
        Args:
            enfermedad: Enfermedad a explicar                           # La enfermedad para la cual se genera la explicación
            
        Returns:
            Cadena con la explicación paso a paso                        # Retorna una cadena con la explicación del diagnóstico
        """
        explicacion = [f"Explicación para '{enfermedad}':"]             # Inicializa una lista con la introducción de la explicación
        
        # Buscar síntomas relacionados                                   # Comentario de la búsqueda de síntomas relacionados
        sintomas_relacionados = [                                        # Crea una lista de síntomas relacionados a la enfermedad y observados
            sintoma for sintoma, enf_list in self.reglas_diagnosticas.items()
            if enfermedad in enf_list and sintoma in self.hechos_observados
        ]
        
        if sintomas_relacionados:                                        # Si hay síntomas relacionados
            explicacion.append("  - Síntomas observados:")              # Agrega un encabezado para los síntomas observados
            for sintoma in sintomas_relacionados:                        # Itera sobre los síntomas relacionados
                explicacion.append(f"    * {sintoma}")                  # Agrega cada síntoma a la explicación
        
        # Buscar complicaciones posibles                                 # Comentario de la búsqueda de complicaciones posibles
        complicaciones = self.reglas_causales.get(enfermedad, [])         # Obtiene las posibles complicaciones para la enfermedad
        if complicaciones:                                               # Si hay complicaciones posibles
            explicacion.append("  - Puede causar:")                     # Agrega un encabezado para las posibles complicaciones
            for comp in complicaciones:                                   # Itera sobre las complicaciones
                explicacion.append(f"    * {comp}")                     # Agrega cada complicación a la explicación
        
        return "\n".join(explicacion)                                   # Une las líneas de la explicación con saltos de línea

# ============================================================================= # Separador de sección
# 2. EJEMPLOS DE USO                                                      # Separador de sección
# ============================================================================= # Separador de sección

def ejemplo_medico():                                                    # Define la función para el ejemplo médico
    """Sistema de diagnóstico médico con relaciones causales"""         # Documentación de la función ejemplo_medico
    print("\n=== SISTEMA MÉDICO DE DIAGNÓSTICO ===")                     # Imprime un encabezado para el sistema médico
    sistema = SistemaDiagnostico()                                       # Crea una instancia de la clase SistemaDiagnostico
    
    # 1. Definir relaciones diagnósticas (síntomas -> enfermedades)       # Comentario de la definición de relaciones diagnósticas
    sistema.agregar_relacion_diagnostica("fiebre", "gripe")              # Agrega la relación: "fiebre" sugiere "gripe"
    sistema.agregar_relacion_diagnostica("tos", "gripe")                 # Agrega la relación: "tos" sugiere "gripe"
    sistema.agregar_relacion_diagnostica("fiebre", "dengue")             # Agrega la relación: "fiebre" sugiere "dengue"
    sistema.agregar_relacion_diagnostica("dolor_muscular", "dengue")      # Agrega la relación: "dolor_muscular" sugiere "dengue"
    sistema.agregar_relacion_diagnostica("erupcion_cutanea", "dengue")    # Agrega la relación: "erupcion_cutanea" sugiere "dengue"
    
    # 2. Definir relaciones causales (enfermedades -> complicaciones)      # Comentario de la definición de relaciones causales
    sistema.agregar_relacion_causal("gripe", "neumonia")                # Agrega la relación: "gripe" puede causar "neumonia"
    sistema.agregar_relacion_causal("dengue", "hemorragia")              # Agrega la relación: "dengue" puede causar "hemorragia"
    sistema.agregar_relacion_causal("dengue", "shock")                   # Agrega la relación: "dengue" puede causar "shock"
    
    # 3. Observar síntomas                                             # Comentario de la observación de síntomas
    sistema.observar("fiebre")                                           # Registra el síntoma "fiebre"
    sistema.observar("dolor_muscular")                                   # Registra el síntoma "dolor_muscular"
    sistema.observar("erupcion_cutanea")                                 # Registra el síntoma "erupcion_cutanea"
    
    # 4. Realizar diagnóstico                                           # Comentario de la realización del diagnóstico
    diagnostico = sistema.diagnosticar()                                 # Realiza el diagnóstico basado en los síntomas observados
    print("\nResultados del diagnóstico:")                             # Imprime un encabezado para los resultados del diagnóstico
    for enf, prob in sorted(diagnostico.items(), key=lambda x: -x[1]):    # Itera sobre los resultados del diagnóstico ordenados por probabilidad descendente
        print(f"- {enf}: {prob*100:.1f}% de probabilidad")              # Imprime la enfermedad y su probabilidad
        print(sistema.explicar_diagnostico(enf))                        # Imprime la explicación del diagnóstico para la enfermedad
        print(f"  Complicaciones posibles: {', '.join(sistema.predecir_complicaciones(enf))}") # Imprime las posibles complicaciones de la enfermedad

def ejemplo_tecnico():                                                  # Define la función para el ejemplo técnico
    """Sistema de diagnóstico técnico para fallas en equipos"""       # Documentación de la función ejemplo_tecnico
    print("\n=== SISTEMA TÉCNICO DE DIAGNÓSTICO ===")                   # Imprime un encabezado para el sistema técnico
    sistema = SistemaDiagnostico()                                       # Crea una instancia de la clase SistemaDiagnostico
    
    # 1. Relaciones diagnósticas (síntomas -> fallas)                   # Comentario de las relaciones diagnósticas técnicas
    sistema.agregar_relacion_diagnostica("no_enciende", "falla_alimentacion") # Agrega la relación: "no_enciende" sugiere "falla_alimentacion"
    sistema.agregar_relacion_diagnostica("no_enciende", "falla_placa_principal") # Agrega la relación: "no_enciende" sugiere "falla_placa_principal"
    sistema.agregar_relacion_diagnostica("pantalla_azul", "falla_memoria")   # Agrega la relación: "pantalla_azul" sugiere "falla_memoria"
    sistema.agregar_relacion_diagnostica("pantalla_azul", "falla_disco")     # Agrega la relación: "pantalla_azul" sugiere "falla_disco"
    sistema.agregar_relacion_diagnostica("sobrecalentamiento", "falla_ventilacion") # Agrega la relación: "sobrecalentamiento" sugiere "falla_ventilacion"
    
    # 2. Relaciones causales (fallas -> consecuencias)                  # Comentario de las relaciones causales técnicas
    sistema.agregar_relacion_causal("falla_ventilacion", "daño_cpu")      # Agrega la relación: "falla_ventilacion" puede causar "daño_cpu"
    sistema.agregar_relacion_causal("falla_disco", "perdida_datos")        # Agrega la relación: "falla_disco" puede causar "perdida_datos"
    
    # 3. Observar síntomas                                             # Comentario de la observación de síntomas técnicos
    sistema.observar("no_enciende")                                     # Registra el síntoma "no_enciende"
    sistema.observar("sobrecalentamiento")                             # Registra el síntoma "sobrecalentamiento"
    
    # 4. Realizar diagnóstico                                           # Comentario de la realización del diagnóstico técnico
    diagnostico = sistema.diagnosticar()                                 # Realiza el diagnóstico basado en los síntomas observados
    print("\nResultados del diagnóstico técnico:")                     # Imprime un encabezado para los resultados del diagnóstico técnico
    for falla, prob in sorted(diagnostico.items(), key=lambda x: -x[1]): # Itera sobre los resultados del diagnóstico ordenados por probabilidad descendente
        print(f"- {falla}: {prob*100:.1f}% de probabilidad")           # Imprime la falla y su probabilidad
        print(f"  Consecuencias posibles: {', '.join(sistema.predecir_complicaciones(falla))}") # Imprime las posibles consecuencias de la falla

if __name__ == "__main__":                                                 # Bloque de código que se ejecuta cuando el script se llama directamente
    ejemplo_medico()                                                       # Llama a la función ejemplo_medico
    ejemplo_tecnico()                                                      # Llama a la función ejemplo_tecnico
```