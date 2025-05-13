# -*- coding: utf-8 -*-                                                     # Define la codificación de caracteres del archivo como UTF-8
"""
Created on Sun Apr 27 14:39:06 2025                                         # Indica la fecha y hora de creación del archivo
                                                                           #
@author: elvin                                                              # Define el autor del archivo
"""

"""
Este código implementa un sistema basado en reglas para diagnóstico y relaciones causales,
simulando cómo un sistema experto podría evaluar condiciones médicas basadas en síntomas.
"""

class SistemaDiagnostico:                                                 # Define una clase llamada SistemaDiagnostico
    """
    Clase que implementa un sistema de diagnóstico basado en reglas causales. # Documentación de la clase SistemaDiagnostico
    Utiliza dos tipos de reglas:
    1. Reglas diagnósticas: Relacionan síntomas con posibles condiciones
    2. Reglas causales: Establecen relaciones causa-efecto entre condiciones
    """
    
    def __init__(self):                                                     # Define el constructor de la clase
        # Base de conocimiento: Reglas diagnósticas (síntomas -> condición) # Comentario de la base de conocimiento de reglas diagnósticas
        self.reglas_diagnosticas = {                                        # Define un diccionario para las reglas diagnósticas
            'fiebre_alta': ['gripe', 'dengue', 'covid'],                     # Regla: si 'fiebre_alta', posibles condiciones son 'gripe', 'dengue', 'covid'
            'tos_persistente': ['gripe', 'covid', 'bronquitis'],             # Regla: si 'tos_persistente', posibles condiciones son 'gripe', 'covid', 'bronquitis'
            'dolor_cabeza': ['gripe', 'migraña', 'dengue'],                  # Regla: si 'dolor_cabeza', posibles condiciones son 'gripe', 'migraña', 'dengue'
            'erupcion_cutanea': ['dengue', 'alergia'],                     # Regla: si 'erupcion_cutanea', posibles condiciones son 'dengue', 'alergia'
            'dificultad_respirar': ['covid', 'asma', 'neumonia']             # Regla: si 'dificultad_respirar', posibles condiciones son 'covid', 'asma', 'neumonia'
        }
        
        # Base de conocimiento: Reglas causales (causa -> efecto)          # Comentario de la base de conocimiento de reglas causales
        self.reglas_causales = {                                           # Define un diccionario para las reglas causales
            'gripe_no_tratada': 'neumonia',                                # Regla: 'gripe_no_tratada' causa 'neumonia'
            'dengue_grave': 'hemorragia_interna',                           # Regla: 'dengue_grave' causa 'hemorragia_interna'
            'alergia_severa': 'shock_anafilactico',                         # Regla: 'alergia_severa' causa 'shock_anafilactico'
            'covid_grave': 'sindrome_respiratorio_agudo'                   # Regla: 'covid_grave' causa 'sindrome_respiratorio_agudo'
        }
        
        # Definición de gravedad de síntomas                              # Comentario de la definición de gravedad de síntomas
        self.sintomas_graves = {                                           # Define un diccionario para la gravedad de los síntomas
            'fiebre_alta': 40.0,                                          # Temperatura de 40.0 °C o más se considera 'fiebre_alta' grave
            'dificultad_respirar': True                                   # La presencia de 'dificultad_respirar' se considera grave
        }

    def diagnosticar(self, sintomas_paciente):                             # Define el método para realizar un diagnóstico
        """
        Realiza un diagnóstico basado en los síntomas del paciente.       # Documentación del método diagnosticar
        
        Args:
            sintomas_paciente (dict): Diccionario con síntomas {síntoma: valor} # Diccionario de síntomas del paciente y sus valores
            
        Returns:
            dict: Posibles diagnósticos con nivel de coincidencia        # Diccionario de posibles diagnósticos y su nivel de coincidencia
        """
        posibles_diagnosticos = {}                                         # Inicializa un diccionario para almacenar los posibles diagnósticos
        
        # Evaluar cada síntoma del paciente contra las reglas diagnósticas  # Comentario para la evaluación de los síntomas
        for sintoma, valor in sintomas_paciente.items():                   # Itera sobre los síntomas del paciente
            if sintoma in self.reglas_diagnosticas:                        # Si el síntoma está en las reglas diagnósticas
                # Verificar si el síntoma está presente (valor != False/None/0) # Comentario para verificar la presencia del síntoma
                if valor and (not isinstance(valor, bool) or valor is True): # Si el valor del síntoma no es falso, None o 0
                    # Para síntomas cuantitativos, verificar umbral        # Comentario para la verificación del umbral en síntomas cuantitativos
                    if sintoma in self.sintomas_graves:                    # Si el síntoma tiene un umbral de gravedad definido
                        if isinstance(valor, (int, float)) and valor >= self.sintomas_graves[sintoma]: # Si el valor es numérico y alcanza o supera el umbral
                            # Síntoma grave, mayor peso en diagnóstico     # Comentario para asignar mayor peso a síntomas graves
                            condiciones = self.reglas_diagnosticas[sintoma] # Obtiene las posibles condiciones asociadas al síntoma
                            for condicion in condiciones:                  # Itera sobre las condiciones
                                posibles_diagnosticos[condicion] = posibles_diagnosticos.get(condicion, 0) + 2 # Incrementa el nivel de coincidencia en 2 (mayor peso)
                        else:
                            # Síntoma presente pero no grave              # Comentario para síntomas presentes pero no graves
                            condiciones = self.reglas_diagnosticas[sintoma] # Obtiene las posibles condiciones asociadas al síntoma
                            for condicion in condiciones:                  # Itera sobre las condiciones
                                posibles_diagnosticos[condicion] = posibles_diagnosticos.get(condicion, 0) + 1 # Incrementa el nivel de coincidencia en 1
                    else:
                        # Síntoma cualitativo regular                    # Comentario para síntomas cualitativos regulares
                        condiciones = self.reglas_diagnosticas[sintoma]     # Obtiene las posibles condiciones asociadas al síntoma
                        for condicion in condiciones:                      # Itera sobre las condiciones
                            posibles_diagnosticos[condicion] = posibles_diagnosticos.get(condicion, 0) + 1 # Incrementa el nivel de coincidencia en 1
        
        # Ordenar diagnósticos por probabilidad (mayor coincidencia primero) # Comentario para ordenar los diagnósticos
        diagnosticos_ordenados = sorted(                                  # Ordena los diagnósticos por su nivel de coincidencia
            posibles_diagnosticos.items(),                                # Obtiene los items (condición, coincidencia) del diccionario
            key=lambda item: item[1],                                     # Define la clave de ordenamiento como el valor (coincidencia)
            reverse=True                                                  # Ordena en orden descendente (mayor coincidencia primero)
        )
        
        return diagnosticos_ordenados                                     # Retorna la lista ordenada de posibles diagnósticos

    def predecir_complicaciones(self, diagnostico_principal):             # Define el método para predecir complicaciones
        """
        Predice posibles complicaciones basadas en reglas causales.      # Documentación del método predecir_complicaciones
        
        Args:
            diagnostico_principal (str): La condición médica diagnosticada # El diagnóstico principal
            
        Returns:
            list: Posibles complicaciones/causales                       # Lista de posibles complicaciones
        """
        complicaciones = []                                              # Inicializa una lista para almacenar las complicaciones
        
        # Verificar si el diagnóstico puede evolucionar a algo más grave   # Comentario para la verificación de la evolución del diagnóstico
        for causa, efecto in self.reglas_causales.items():               # Itera sobre las reglas causales
            if causa.startswith(diagnostico_principal):                   # Si la causa comienza con el diagnóstico principal
                complicaciones.append(efecto)                            # Agrega el efecto (complicación) a la lista
        
        return complicaciones                                             # Retorna la lista de complicaciones

    def explicar_diagnostico(self, sintomas, diagnostico):               # Define el método para explicar el diagnóstico
        """
        Genera una explicación causal del diagnóstico.                   # Documentación del método explicar_diagnostico
        
        Args:
            sintomas (dict): Síntomas del paciente                       # Diccionario de síntomas del paciente
            diagnostico (str): Diagnóstico principal                      # El diagnóstico principal
            
        Returns:
            str: Explicación en lenguaje natural                         # Explicación del diagnóstico en lenguaje natural
        """
        sintomas_relacionados = []                                       # Inicializa una lista para almacenar los síntomas relacionados
        
        # Encontrar qué síntomas apoyan este diagnóstico                 # Comentario para encontrar los síntomas de apoyo
        for sintoma, condiciones in self.reglas_diagnosticas.items():    # Itera sobre las reglas diagnósticas
            if diagnostico in condiciones and sintoma in sintomas:      # Si el diagnóstico está en las condiciones del síntoma y el síntoma está presente
                sintomas_relacionados.append(sintoma)                    # Agrega el síntoma a la lista de síntomas relacionados
        
        explicacion = f"El diagnóstico de {diagnostico} se basa en los siguientes síntomas: " # Inicia la explicación
        explicacion += ", ".join(sintomas_relacionados) + ". "          # Agrega los síntomas relacionados a la explicación
        
        # Añadir posibles complicaciones                                # Comentario para añadir las posibles complicaciones
        complicaciones = self.predecir_complicaciones(diagnostico)      # Obtiene las posibles complicaciones del diagnóstico
        if complicaciones:                                               # Si hay complicaciones
            explicacion += f"Si no se trata, podría desarrollar: {', '.join(complicaciones)}." # Agrega las complicaciones a la explicación
        
        return explicacion                                               # Retorna la explicación

def ejemplo_uso():                                                      # Define la función para el ejemplo de uso
    """
    Ejemplo práctico de uso del sistema de diagnóstico.                # Documentación de la función ejemplo_uso
    """
    sistema = SistemaDiagnostico()                                       # Crea una instancia de la clase SistemaDiagnostico
    
    # Caso 1: Paciente con síntomas de gripe                           # Comentario para el Caso 1
    sintomas_paciente1 = {                                             # Define los síntomas del paciente 1
        'fiebre_alta': 38.5,
        'tos_persistente': True,
        'dolor_cabeza': True
    }
    
    print("\n=== Caso 1 ===")                                         # Imprime un encabezado para el Caso 1
    print("Síntomas:", sintomas_paciente1)                             # Imprime los síntomas del paciente 1
    diagnostico1 = sistema.diagnosticar(sintomas_paciente1)             # Realiza el diagnóstico para el paciente 1
    print("Posibles diagnósticos:", diagnostico1)                       # Imprime los posibles diagnósticos para el paciente 1
    
    if diagnostico1:                                                  # Si se encontraron diagnósticos
        diagnostico_principal = diagnostico1[0][0]                    # Obtiene el diagnóstico principal (el primero en la lista ordenada)
        print("\nExplicación:")                                      # Imprime un encabezado para la explicación
        print(sistema.explicar_diagnostico(sintomas_paciente1, diagnostico_principal)) # Imprime la explicación del diagnóstico
        
        complicaciones = sistema.predecir_complicaciones(diagnostico_principal) # Predice las posibles complicaciones
        if complicaciones:                                           # Si hay complicaciones
            print("Posibles complicaciones:", complicaciones)         # Imprime las posibles complicaciones
    
    # Caso 2: Paciente con posible dengue                            # Comentario para el Caso 2
    sintomas_paciente2 = {                                             # Define los síntomas del paciente 2
        'fiebre_alta': 40.5,                                          # Fiebre muy alta
        'dolor_cabeza': True,
        'erupcion_cutanea': True
    }
    
    print("\n=== Caso 2 ===")                                         # Imprime un encabezado para el Caso 2
    print("Síntomas:", sintomas_paciente2)                             # Imprime los síntomas del paciente 2
    diagnostico2 = sistema.diagnosticar(sintomas_paciente2)             # Realiza el diagnóstico para el paciente 2
    print("Posibles diagnósticos:", diagnostico2)                       # Imprime los posibles diagnósticos para el paciente 2
    
    if diagnostico2:                                                  # Si se encontraron diagnósticos
        diagnostico_principal = diagnostico2[0][0]                    # Obtiene el diagnóstico principal
        print("\nExplicación:")                                      # Imprime un encabezado para la explicación
        print(sistema.explicar_diagnostico(sintomas_paciente2, diagnostico_principal)) # Imprime la explicación del diagnóstico
        
        complicaciones = sistema.predecir_complicaciones(diagnostico_principal) # Predice las posibles complicaciones
        if complicaciones:                                           # Si hay complicaciones
            print("Posibles complicaciones:", complicaciones)         # Imprime las posibles complicaciones

if __name__ == "__main__":                                                 # Bloque de código que se ejecuta cuando el script se llama directamente
    print("=== Sistema de Diagnóstico Basado en Reglas Causales ===")      # Imprime un encabezado para el sistema
    ejemplo_uso()                                                          # Llama a la función ejemplo_uso