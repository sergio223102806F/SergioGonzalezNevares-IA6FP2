# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 17:21:27 2025

@author: elvin
"""

"""
Sistema de diagnóstico basado en reglas causales que implementa:
1. Base de conocimiento con relaciones causales y diagnósticas
2. Motor de inferencia hacia adelante y hacia atrás
3. Mecanismo de explicación de diagnósticos
4. Ejemplos médicos y técnicos
"""

from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict

# =============================================================================
# 1. DEFINICIÓN DEL SISTEMA DE DIAGNÓSTICO
# =============================================================================

class SistemaDiagnostico:
    """
    Sistema experto para diagnóstico con relaciones causales
    
    Componentes:
        - Síntomas <-> Enfermedades (diagnóstico)
        - Enfermedades <-> Complicaciones (causal)
        - Motor de inferencia combinado
    """
    
    def __init__(self):
        # Relaciones diagnóstico: síntoma -> posibles enfermedades
        self.reglas_diagnosticas: Dict[str, List[str]] = defaultdict(list)
        
        # Relaciones causales: enfermedad -> posibles complicaciones
        self.reglas_causales: Dict[str, List[str]] = defaultdict(list)
        
        # Base de hechos observados
        self.hechos_observados: Set[str] = set()
        
        # Historial de inferencias para explicaciones
        self.historial: List[Tuple[str, str]] = []
    
    def agregar_relacion_diagnostica(self, sintoma: str, enfermedad: str):
        """Establece que un síntoma puede indicar una enfermedad"""
        self.reglas_diagnosticas[sintoma].append(enfermedad)
    
    def agregar_relacion_causal(self, enfermedad: str, complicacion: str):
        """Establece que una enfermedad puede causar una complicación"""
        self.reglas_causales[enfermedad].append(complicacion)
    
    def observar(self, hecho: str):
        """Registra un hecho observado (síntoma o hallazgo)"""
        self.hechos_observados.add(hecho)
    
    def diagnosticar(self) -> Dict[str, float]:
        """
        Realiza diagnóstico basado en síntomas observados
        
        Returns:
            Diccionario {enfermedad: probabilidad}
        """
        enfermedades_posibles: Dict[str, int] = defaultdict(int)
        total_sintomas = 0
        
        # Inferencia hacia adelante: síntomas -> enfermedades
        for sintoma in self.hechos_observados:
            if sintoma in self.reglas_diagnosticas:
                for enfermedad in self.reglas_diagnosticas[sintoma]:
                    enfermedades_posibles[enfermedad] += 1
                    self.historial.append((f"Síntoma '{sintoma}'", f"sugiere '{enfermedad}'"))
                total_sintomas += 1
        
        # Calcular probabilidades relativas
        if not enfermedades_posibles:
            return {}
        
        max_puntos = max(enfermedades_posibles.values())
        return {
            enf: (puntos / max_puntos) 
            for enf, puntos in enfermedades_posibles.items()
        }
    
    def predecir_complicaciones(self, enfermedad: str) -> List[str]:
        """Predice posibles complicaciones de una enfermedad"""
        return self.reglas_causales.get(enfermedad, [])
    
    def explicar_diagnostico(self, enfermedad: str) -> str:
        """
        Genera una explicación de cómo se llegó a un diagnóstico
        
        Args:
            enfermedad: Enfermedad a explicar
            
        Returns:
            Cadena con la explicación paso a paso
        """
        explicacion = [f"Explicación para '{enfermedad}':"]
        
        # Buscar síntomas relacionados
        sintomas_relacionados = [
            sintoma for sintoma, enf_list in self.reglas_diagnosticas.items()
            if enfermedad in enf_list and sintoma in self.hechos_observados
        ]
        
        if sintomas_relacionados:
            explicacion.append("  - Síntomas observados:")
            for sintoma in sintomas_relacionados:
                explicacion.append(f"    * {sintoma}")
        
        # Buscar complicaciones posibles
        complicaciones = self.reglas_causales.get(enfermedad, [])
        if complicaciones:
            explicacion.append("  - Puede causar:")
            for comp in complicaciones:
                explicacion.append(f"    * {comp}")
        
        return "\n".join(explicacion)

# =============================================================================
# 2. EJEMPLOS DE USO
# =============================================================================

def ejemplo_medico():
    """Sistema de diagnóstico médico con relaciones causales"""
    print("\n=== SISTEMA MÉDICO DE DIAGNÓSTICO ===")
    sistema = SistemaDiagnostico()
    
    # 1. Definir relaciones diagnósticas (síntomas -> enfermedades)
    sistema.agregar_relacion_diagnostica("fiebre", "gripe")
    sistema.agregar_relacion_diagnostica("tos", "gripe")
    sistema.agregar_relacion_diagnostica("fiebre", "dengue")
    sistema.agregar_relacion_diagnostica("dolor_muscular", "dengue")
    sistema.agregar_relacion_diagnostica("erupcion_cutanea", "dengue")
    
    # 2. Definir relaciones causales (enfermedades -> complicaciones)
    sistema.agregar_relacion_causal("gripe", "neumonia")
    sistema.agregar_relacion_causal("dengue", "hemorragia")
    sistema.agregar_relacion_causal("dengue", "shock")
    
    # 3. Observar síntomas
    sistema.observar("fiebre")
    sistema.observar("dolor_muscular")
    sistema.observar("erupcion_cutanea")
    
    # 4. Realizar diagnóstico
    diagnostico = sistema.diagnosticar()
    print("\nResultados del diagnóstico:")
    for enf, prob in sorted(diagnostico.items(), key=lambda x: -x[1]):
        print(f"- {enf}: {prob*100:.1f}% de probabilidad")
        print(sistema.explicar_diagnostico(enf))
        print(f"  Complicaciones posibles: {', '.join(sistema.predecir_complicaciones(enf))}")

def ejemplo_tecnico():
    """Sistema de diagnóstico técnico para fallas en equipos"""
    print("\n=== SISTEMA TÉCNICO DE DIAGNÓSTICO ===")
    sistema = SistemaDiagnostico()
    
    # 1. Relaciones diagnósticas (síntomas -> fallas)
    sistema.agregar_relacion_diagnostica("no_enciende", "falla_alimentacion")
    sistema.agregar_relacion_diagnostica("no_enciende", "falla_placa_principal")
    sistema.agregar_relacion_diagnostica("pantalla_azul", "falla_memoria")
    sistema.agregar_relacion_diagnostica("pantalla_azul", "falla_disco")
    sistema.agregar_relacion_diagnostica("sobrecalentamiento", "falla_ventilacion")
    
    # 2. Relaciones causales (fallas -> consecuencias)
    sistema.agregar_relacion_causal("falla_ventilacion", "daño_cpu")
    sistema.agregar_relacion_causal("falla_disco", "perdida_datos")
    
    # 3. Observar síntomas
    sistema.observar("no_enciende")
    sistema.observar("sobrecalentamiento")
    
    # 4. Realizar diagnóstico
    diagnostico = sistema.diagnosticar()
    print("\nResultados del diagnóstico técnico:")
    for falla, prob in sorted(diagnostico.items(), key=lambda x: -x[1]):
        print(f"- {falla}: {prob*100:.1f}% de probabilidad")
        print(f"  Consecuencias posibles: {', '.join(sistema.predecir_complicaciones(falla))}")

if __name__ == "__main__":
    ejemplo_medico()
    ejemplo_tecnico()