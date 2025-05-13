# -*- coding: utf-8 -*-  # Especifica la codificación del archivo como UTF-8
"""
Created on Sun Apr 27 14:36:38 2025  # Fecha de creación del archivo

@author: elvin  # Autor del código
"""

"""
Implementación de un Sistema de Base de Conocimiento  # Descripción general

Este código incluye:  # Lista de funcionalidades
1. Representación de hechos y reglas  # Modelado de conocimiento
2. Encadenamiento hacia adelante y hacia atrás  # Métodos de inferencia
3. Consultas y agregado de conocimiento  # Interfaz de usuario
4. Manejo de incertidumbre (opcional)  # Lógica difusa
5. Explicación de inferencias  # Trazabilidad
"""

from typing import Dict, List, Union, Optional  # Tipos para type hints

class Hecho:
    """
    Clase para representar hechos en la base de conocimiento.
    
    Atributos:
        nombre (str): Nombre del hecho (ej. "es_mamifero")  # Identificador
        valor (Union[bool, float]): Valor de verdad (True/False) o certeza (0-1)  # Valor
        explicacion (str): Justificación del hecho  # Contexto
    """
    def __init__(self, nombre: str, valor: Union[bool, float], explicacion: str = ""):  # Constructor
        self.nombre = nombre  # Asigna nombre
        self.valor = valor  # Asigna valor
        self.explicacion = explicacion  # Asigna explicación
    
    def __repr__(self):  # Representación formal
        return f"Hecho(nombre='{self.nombre}', valor={self.valor}, explicacion='{self.explicacion}')"  # String descriptivo

class Regla:
    """
    Clase para representar reglas en la base de conocimiento.
    
    Atributos:
        antecedentes (List[str]): Lista de hechos requeridos (ej. ["es_animal", "tiene_pelo"])  # Premisas
        consecuente (str): Hecho resultante (ej. "es_mamifero")  # Conclusión
        certeza (float): Grado de certeza de la regla (0-1)  # Factor de certeza
        explicacion (str): Justificación de la regla  # Base de la regla
    """
    def __init__(self, antecedentes: List[str], consecuente: str, certeza: float = 1.0, explicacion: str = ""):  # Constructor
        self.antecedentes = antecedentes  # Asigna antecedentes
        self.consecuente = consecuente  # Asigna consecuente
        self.certeza = certeza  # Asigna certeza
        self.explicacion = explicacion  # Asigna explicación
    
    def __repr__(self):  # Representación formal
        return f"Regla(antecedentes={self.antecedentes}, consecuente='{self.consecuente}', certeza={self.certeza})"  # String descriptivo

class BaseConocimiento:
    """
    Sistema de Base de Conocimiento con capacidades de razonamiento.
    
    Atributos:
        hechos (Dict[str, Hecho]): Diccionario de hechos conocidos  # Base de hechos
        reglas (List[Regla]): Lista de reglas de inferencia  # Base de reglas
    """
    def __init__(self):  # Constructor
        self.hechos: Dict[str, Hecho] = {}  # Inicializa diccionario de hechos
        self.reglas: List[Regla] = []  # Inicializa lista de reglas
    
    def agregar_hecho(self, hecho: Hecho) -> None:  # Método para agregar hechos
        """
        Agrega un hecho a la base de conocimiento.
        
        Args:
            hecho (Hecho): Hecho a agregar  # Input
        """
        self.hechos[hecho.nombre] = hecho  # Añade al diccionario
    
    def agregar_regla(self, regla: Regla) -> None:  # Método para agregar reglas
        """
        Agrega una regla a la base de conocimiento.
        
        Args:
            regla (Regla): Regla a agregar  # Input
        """
        self.reglas.append(regla)  # Añade a la lista
    
    def consultar(self, nombre_hecho: str, usar_explicacion: bool = False) -> Optional[Union[bool, float]]:  # Método de consulta
        """
        Consulta un hecho en la base de conocimiento.
        
        Args:
            nombre_hecho (str): Nombre del hecho a consultar  # Hecho buscado
            usar_explicacion (bool): Si True, muestra la explicación  # Flag para explicación
            
        Returns:
            Union[bool, float, None]: Valor del hecho o None si no existe  # Resultado
        """
        hecho = self.hechos.get(nombre_hecho)  # Busca el hecho
        if hecho:  # Si existe
            if usar_explicacion:  # Si se pidió explicación
                print(f"Explicación para '{nombre_hecho}': {hecho.explicacion}")  # Muestra explicación
            return hecho.valor  # Retorna valor
        return None  # Retorna None si no existe
    
    def encadenamiento_adelante(self) -> None:  # Forward chaining
        """
        Realiza encadenamiento hacia adelante para inferir nuevos hechos.
        
        Itera sobre las reglas y aplica aquellas cuyos antecedentes son conocidos.
        """
        cambios = True  # Flag para controlar iteraciones
        while cambios:  # Mientras haya cambios
            cambios = False  # Reset flag
            for regla in self.reglas:  # Para cada regla
                # Verificar si todos los antecedentes son conocidos y verdaderos
                todos_verdaderos = all(  # Evalúa todos los antecedentes
                    self.hechos.get(ant) and self.hechos[ant].valor  # Existe y es verdadero
                    for ant in regla.antecedentes  # Para cada antecedente
                )
                
                if todos_verdaderos and regla.consecuente not in self.hechos:  # Si se puede inferir
                    # Calcular valor del consecuente (considerando certeza)
                    valor_antecedentes = min(  # Toma el mínimo valor
                        self.hechos[ant].valor for ant in regla.antecedentes  # De los antecedentes
                    )
                    nuevo_valor = valor_antecedentes * regla.certeza  # Aplica factor de certeza
                    
                    # Crear explicación
                    explicacion = f"Inferido por regla: {regla.explicacion}. "  # Base de la regla
                    explicacion += f"Antecedentes: {', '.join(regla.antecedentes)}"  # Lista antecedentes
                    
                    # Agregar nuevo hecho
                    nuevo_hecho = Hecho(regla.consecuente, nuevo_valor, explicacion)  # Crea hecho
                    self.agregar_hecho(nuevo_hecho)  # Añade a la base
                    cambios = True  # Indica que hubo cambio
    
    def encadenamiento_atras(self, objetivo: str, profundidad: int = 0, max_profundidad: int = 10) -> bool:  # Backward chaining
        """
        Realiza encadenamiento hacia atrás para verificar un objetivo.
        
        Args:
            objetivo (str): Nombre del hecho a verificar  # Hecho objetivo
            profundidad (int): Profundidad actual de recursión (para evitar ciclos)  # Control de recursión
            max_profundidad (int): Límite de profundidad de recursión  # Límite seguridad
            
        Returns:
            bool: True si el objetivo puede ser inferido, False en caso contrario  # Resultado
        """
        # Evitar recursión infinita
        if profundidad > max_profundidad:  # Si superó el límite
            return False  # Termina recursión
        
        # Si el hecho ya existe, retornar su valor
        if objetivo in self.hechos:  # Si está en la base
            return bool(self.hechos[objetivo].valor)  # Retorna su valor booleano
        
        # Buscar reglas que puedan inferir el objetivo
        for regla in self.reglas:  # Para cada regla
            if regla.consecuente == objetivo:  # Si su consecuente es el objetivo
                # Verificar si todos los antecedentes pueden ser probados
                todos_probados = all(  # Evalúa todos
                    self.encadenamiento_atras(ant, profundidad + 1, max_profundidad)  # Llama recursivamente
                    for ant in regla.antecedentes  # Para cada antecedente
                )
                
                if todos_probados:  # Si todos se probaron
                    # Calcular valor del consecuente
                    valor_antecedentes = min(  # Toma el mínimo
                        self.hechos[ant].valor for ant in regla.antecedentes  # De los antecedentes
                        if ant in self.hechos  # Que existan
                    )
                    nuevo_valor = valor_antecedentes * regla.certeza  # Aplica certeza
                    
                    # Crear explicación
                    explicacion = f"Inferido por regla: {regla.explicacion}. "  # Base de la regla
                    explicacion += f"Antecedentes: {', '.join(regla.antecedentes)}"  # Lista antecedentes
                    
                    # Agregar nuevo hecho
                    self.agregar_hecho(Hecho(objetivo, nuevo_valor, explicacion))  # Crea y añade
                    return True  # Indica éxito
        
        return False  # Si no se pudo inferir
    
    def mostrar_conocimiento(self, mostrar_explicaciones: bool = False) -> None:  # Método de visualización
        """
        Muestra todo el conocimiento almacenado.
        
        Args:
            mostrar_explicaciones (bool): Si True, muestra las explicaciones  # Flag para explicaciones
        """
        print("\n=== HECHOS ===")  # Encabezado
        for nombre, hecho in self.hechos.items():  # Para cada hecho
            valor_str = f"{hecho.valor:.2f}" if isinstance(hecho.valor, float) else str(hecho.valor)  # Formatea valor
            print(f"- {nombre}: {valor_str}")  # Muestra nombre-valor
            if mostrar_explicaciones and hecho.explicacion:  # Si se pidió explicación
                print(f"  Explicación: {hecho.explicacion}")  # Muestra explicación
        
        print("\n=== REGLAS ===")  # Encabezado
        for i, regla in enumerate(self.reglas, 1):  # Para cada regla (numerada)
            print(f"{i}. SI {', '.join(regla.antecedentes)} ENTONCES {regla.consecuente} (Certeza: {regla.certeza:.2f})")  # Muestra regla
            if mostrar_explicaciones and regla.explicacion:  # Si se pidió explicación
                print(f"   Explicación: {regla.explicacion}")  # Muestra explicación

# Ejemplo de uso  # Bloque principal
if __name__ == "__main__":  # Ejecución directa
    print("Sistema de Base de Conocimiento")  # Título
    print("=" * 40)  # Separador
    
    # Crear base de conocimiento  # Paso 1
    bc = BaseConocimiento()  # Instancia
    
    # Agregar hechos iniciales (con valores de certeza entre 0 y 1)  # Paso 2
    bc.agregar_hecho(Hecho("es_animal", True, "Observación directa"))  # Hecho 1
    bc.agregar_hecho(Hecho("tiene_pelo", True, "Observación directa"))  # Hecho 2
    bc.agregar_hecho(Hecho("da_leche", True, "Observación directa"))  # Hecho 3
    bc.agregar_hecho(Hecho("tiene_plumas", False, "Observación directa"))  # Hecho 4
    bc.agregar_hecho(Hecho("vuela", False, "Observación directa"))  # Hecho 5
    bc.agregar_hecho(Hecho("pone_huevos", False, "Observación directa"))  # Hecho 6
    
    # Agregar reglas (sistema experto simple para clasificación de animales)  # Paso 3
    bc.agregar_regla(Regla(  # Regla 1
        ["es_animal", "tiene_pelo", "da_leche"],  # Antecedentes
        "es_mamifero",  # Consecuente
        0.9,  # Certeza
        "Los mamíferos son animales con pelo que dan leche"  # Explicación
    ))
    
    bc.agregar_regla(Regla(  # Regla 2
        ["es_animal", "tiene_plumas", "vuela", "pone_huevos"],  # Antecedentes
        "es_ave",  # Consecuente
        0.95,  # Certeza
        "Las aves son animales con plumas que vuelan y ponen huevos"  # Explicación
    ))
    
    bc.agregar_regla(Regla(  # Regla 3
        ["es_mamifero", "tiene_pezuñas"],  # Antecedentes
        "es_ungulado",  # Consecuente
        0.8,  # Certeza
        "Los ungulados son mamíferos con pezuñas"  # Explicación
    ))
    
    bc.agregar_regla(Regla(  # Regla 4
        ["es_mamifero", "come_carne"],  # Antecedentes
        "es_carnivoro",  # Consecuente
        0.85,  # Certeza
        "Los carnívoros son mamíferos que comen carne"  # Explicación
    ))
    
    # Mostrar conocimiento inicial  # Paso 4
    print("\nConocimiento inicial:")  # Encabezado
    bc.mostrar_conocimiento()  # Llama al método
    
    # Realizar encadenamiento hacia adelante  # Paso 5
    print("\nRealizando encadenamiento hacia adelante...")  # Mensaje
    bc.encadenamiento_adelante()  # Llama al método
    
    # Mostrar conocimiento después de inferencia  # Paso 6
    print("\nConocimiento después de inferencia:")  # Encabezado
    bc.mostrar_conocimiento(mostrar_explicaciones=True)  # Con explicaciones
    
    # Consultar un hecho específico con explicación  # Paso 7
    print("\nConsultando un hecho con explicación:")  # Encabezado
    resultado = bc.consultar("es_mamifero", usar_explicacion=True)  # Consulta con explicación
    print(f"Resultado: {resultado}")  # Muestra resultado
    
    # Realizar encadenamiento hacia atrás para un objetivo  # Paso 8
    print("\nRealizando encadenamiento hacia atrás para 'es_ungulado':")  # Mensaje
    bc.agregar_hecho(Hecho("tiene_pezuñas", True, "Observación directa"))  # Añade hecho necesario
    exito = bc.encadenamiento_atras("es_ungulado")  # Intenta inferir
    print(f"¿Se pudo inferir 'es_ungulado'? {'Sí' if exito else 'No'}")  # Muestra resultado
    
    # Mostrar conocimiento final  # Paso 9
    print("\nConocimiento final:")  # Encabezado
    bc.mostrar_conocimiento(mostrar_explicaciones=True)  # Con explicaciones