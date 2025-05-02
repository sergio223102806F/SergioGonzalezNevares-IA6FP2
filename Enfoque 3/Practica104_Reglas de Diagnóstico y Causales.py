# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 14:39:06 2025

@author: elvin
"""

"""
Este código implementa un sistema basado en reglas para diagnóstico y relaciones causales,
simulando cómo un sistema experto podría evaluar condiciones médicas basadas en síntomas.
"""

class SistemaDiagnostico:
    """
    Clase que implementa un sistema de diagnóstico basado en reglas causales.
    Utiliza dos tipos de reglas:
    1. Reglas diagnósticas: Relacionan síntomas con posibles condiciones
    2. Reglas causales: Establecen relaciones causa-efecto entre condiciones
    """
    
    def __init__(self):
        # Base de conocimiento: Reglas diagnósticas (síntomas -> condición)
        self.reglas_diagnosticas = {
            'fiebre_alta': ['gripe', 'dengue', 'covid'],
            'tos_persistente': ['gripe', 'covid', 'bronquitis'],
            'dolor_cabeza': ['gripe', 'migraña', 'dengue'],
            'erupcion_cutanea': ['dengue', 'alergia'],
            'dificultad_respirar': ['covid', 'asma', 'neumonia']
        }
        
        # Base de conocimiento: Reglas causales (causa -> efecto)
        self.reglas_causales = {
            'gripe_no_tratada': 'neumonia',
            'dengue_grave': 'hemorragia_interna',
            'alergia_severa': 'shock_anafilactico',
            'covid_grave': 'sindrome_respiratorio_agudo'
        }
        
        # Definición de gravedad de síntomas
        self.sintomas_graves = {
            'fiebre_alta': 40.0,  # Temperatura en °C considerada grave
            'dificultad_respirar': True  # Presencia del síntoma ya es grave
        }

    def diagnosticar(self, sintomas_paciente):
        """
        Realiza un diagnóstico basado en los síntomas del paciente.
        
        Args:
            sintomas_paciente (dict): Diccionario con síntomas {síntoma: valor}
            
        Returns:
            dict: Posibles diagnósticos con nivel de coincidencia
        """
        posibles_diagnosticos = {}
        
        # Evaluar cada síntoma del paciente contra las reglas diagnósticas
        for sintoma, valor in sintomas_paciente.items():
            if sintoma in self.reglas_diagnosticas:
                # Verificar si el síntoma está presente (valor != False/None/0)
                if valor and (not isinstance(valor, bool) or valor is True):
                    # Para síntomas cuantitativos, verificar umbral
                    if sintoma in self.sintomas_graves:
                        if isinstance(valor, (int, float)) and valor >= self.sintomas_graves[sintoma]:
                            # Síntoma grave, mayor peso en diagnóstico
                            condiciones = self.reglas_diagnosticas[sintoma]
                            for condicion in condiciones:
                                posibles_diagnosticos[condicion] = posibles_diagnosticos.get(condicion, 0) + 2
                        else:
                            # Síntoma presente pero no grave
                            condiciones = self.reglas_diagnosticas[sintoma]
                            for condicion in condiciones:
                                posibles_diagnosticos[condicion] = posibles_diagnosticos.get(condicion, 0) + 1
                    else:
                        # Síntoma cualitativo regular
                        condiciones = self.reglas_diagnosticas[sintoma]
                        for condicion in condiciones:
                            posibles_diagnosticos[condicion] = posibles_diagnosticos.get(condicion, 0) + 1
        
        # Ordenar diagnósticos por probabilidad (mayor coincidencia primero)
        diagnosticos_ordenados = sorted(
            posibles_diagnosticos.items(),
            key=lambda item: item[1],
            reverse=True
        )
        
        return diagnosticos_ordenados

    def predecir_complicaciones(self, diagnostico_principal):
        """
        Predice posibles complicaciones basadas en reglas causales.
        
        Args:
            diagnostico_principal (str): La condición médica diagnosticada
            
        Returns:
            list: Posibles complicaciones/causales
        """
        complicaciones = []
        
        # Verificar si el diagnóstico puede evolucionar a algo más grave
        for causa, efecto in self.reglas_causales.items():
            if causa.startswith(diagnostico_principal):
                complicaciones.append(efecto)
        
        return complicaciones

    def explicar_diagnostico(self, sintomas, diagnostico):
        """
        Genera una explicación causal del diagnóstico.
        
        Args:
            sintomas (dict): Síntomas del paciente
            diagnostico (str): Diagnóstico principal
            
        Returns:
            str: Explicación en lenguaje natural
        """
        sintomas_relacionados = []
        
        # Encontrar qué síntomas apoyan este diagnóstico
        for sintoma, condiciones in self.reglas_diagnosticas.items():
            if diagnostico in condiciones and sintoma in sintomas:
                sintomas_relacionados.append(sintoma)
        
        explicacion = f"El diagnóstico de {diagnostico} se basa en los siguientes síntomas: "
        explicacion += ", ".join(sintomas_relacionados) + ". "
        
        # Añadir posibles complicaciones
        complicaciones = self.predecir_complicaciones(diagnostico)
        if complicaciones:
            explicacion += f"Si no se trata, podría desarrollar: {', '.join(complicaciones)}."
        
        return explicacion

def ejemplo_uso():
    """
    Ejemplo práctico de uso del sistema de diagnóstico.
    """
    sistema = SistemaDiagnostico()
    
    # Caso 1: Paciente con síntomas de gripe
    sintomas_paciente1 = {
        'fiebre_alta': 38.5,
        'tos_persistente': True,
        'dolor_cabeza': True
    }
    
    print("\n=== Caso 1 ===")
    print("Síntomas:", sintomas_paciente1)
    diagnostico1 = sistema.diagnosticar(sintomas_paciente1)
    print("Posibles diagnósticos:", diagnostico1)
    
    if diagnostico1:
        diagnostico_principal = diagnostico1[0][0]
        print("\nExplicación:")
        print(sistema.explicar_diagnostico(sintomas_paciente1, diagnostico_principal))
        
        complicaciones = sistema.predecir_complicaciones(diagnostico_principal)
        if complicaciones:
            print("Posibles complicaciones:", complicaciones)
    
    # Caso 2: Paciente con posible dengue
    sintomas_paciente2 = {
        'fiebre_alta': 40.5,  # Fiebre muy alta
        'dolor_cabeza': True,
        'erupcion_cutanea': True
    }
    
    print("\n=== Caso 2 ===")
    print("Síntomas:", sintomas_paciente2)
    diagnostico2 = sistema.diagnosticar(sintomas_paciente2)
    print("Posibles diagnósticos:", diagnostico2)
    
    if diagnostico2:
        diagnostico_principal = diagnostico2[0][0]
        print("\nExplicación:")
        print(sistema.explicar_diagnostico(sintomas_paciente2, diagnostico_principal))
        
        complicaciones = sistema.predecir_complicaciones(diagnostico_principal)
        if complicaciones:
            print("Posibles complicaciones:", complicaciones)

if __name__ == "__main__":
    print("=== Sistema de Diagnóstico Basado en Reglas Causales ===")
    ejemplo_uso()