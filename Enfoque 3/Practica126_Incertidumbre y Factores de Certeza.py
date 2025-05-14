# -*- coding: utf-8 -*-


# Importaciones necesarias
from typing import Dict, List, Optional, Tuple  # Tipos para anotaciones de tipo
from dataclasses import dataclass  # Decorador para crear clases concisas
from enum import Enum, auto  # Para definir enumeraciones
import math  # Para operaciones matemáticas

class TipoIncertidumbre(Enum):
    """Tipos de modelos de incertidumbre implementados"""
    FACTOR_CERTEZA = auto()     # Modelo de factores de certeza (MYCIN)
    PROBABILISTICO = auto()     # Modelo probabilístico simple
    LOGICA_DIFUSA = auto()      # Modelo de lógica difusa

@dataclass
class ReglaIncertidumbre:
    """Estructura para reglas con manejo de incertidumbre"""
    nombre: str,                 # Identificador único de la regla
    antecedentes: List[Tuple[str, float]],  # Lista de tuplas (premisa, peso) para los antecedentes
    consecuente: str,            # Conclusión de la regla
    factor_certeza: float,       # Factor de certeza de la regla [0, 1]
    tipo: TipoIncertidumbre      # Tipo de modelo de incertidumbre usado por esta regla

@dataclass
class HechoIncertidumbre:
    """Representa un hecho con su grado de incertidumbre"""
    contenido: str,              # Enunciado del hecho
    certeza: float,              # Grado de certeza [-1, 1] o [0, 1] dependiendo del tipo
    tipo: TipoIncertidumbre,     # Tipo de modelo de incertidumbre usado para este hecho
    fuente: str                   # Origen o cómo se obtuvo este hecho

class SistemaIncertidumbre:
    """
    Sistema para manejo de incertidumbre usando:
    - Factores de certeza (MYCIN)
    - Probabilidades simples
    - Lógica difusa básica
    """

    def __init__(self):
        """Inicializa las estructuras del sistema"""
        self.hechos: Dict[str, HechoIncertidumbre] = {}     # Diccionario para almacenar los hechos conocidos con su incertidumbre
        self.reglas: Dict[str, ReglaIncertidumbre] = {}     # Diccionario para almacenar las reglas de inferencia con su incertidumbre
        self.historial: List[str] = []                     # Lista para guardar un registro de las operaciones realizadas

    def agregar_hecho(self, hecho: HechoIncertidumbre) -> bool:
        """
        Añade un nuevo hecho al sistema, combinando certeza si ya existe
        """
        # Verificar rango de certeza según el tipo
        if hecho.tipo == TipoIncertidumbre.FACTOR_CERTEZA:  # Si el modelo es de factor de certeza
            if not -1 <= hecho.certeza <= 1:  # El factor de certeza debe estar entre -1 y 1
                return False  # Retorna False si el rango es inválido
        else:  # Para modelos probabilísticos y difusos
            if not 0 <= hecho.certeza <= 1:  # La certeza debe estar entre 0 y 1
                return False  # Retorna False si el rango es inválido

        if hecho.contenido in self.hechos:  # Si el hecho ya existe en el sistema
            # Combinar factores de certeza si el hecho ya existe
            existente = self.hechos[hecho.contenido]  # Obtiene el hecho existente
            if existente.tipo != hecho.tipo:  # Si los tipos de incertidumbre son diferentes
                return False  # No se pueden combinar, retorna False

            if existente.tipo == TipoIncertidumbre.FACTOR_CERTEZA:  # Si el modelo es de factor de certeza (MYCIN)
                # Combinación MYCIN de factores de certeza
                nueva_certeza = existente.certeza + hecho.certeza * (1 - existente.certeza)  # Fórmula de combinación para factores de certeza positivos
            else:  # Para otros modelos (probabilístico o difuso)
                # Para otros modelos, tomar el máximo (podría mejorarse)
                nueva_certeza = max(existente.certeza, hecho.certeza)  # Se toma el máximo grado de certeza
            self.hechos[hecho.contenido].certeza = nueva_certeza  # Actualiza la certeza del hecho existente
            self.historial.append(f"Actualizado hecho {hecho.contenido} con certeza {nueva_certeza:.2f}")  # Registra la actualización en el historial
        else:  # Si el hecho no existe en el sistema
            self.hechos[hecho.contenido] = hecho  # Añade el nuevo hecho al diccionario de hechos
            self.historial.append(f"Añadido hecho {hecho.contenido} con certeza {hecho.certeza:.2f}")  # Registra la adición en el historial

        return True  # Retorna True si el hecho se añadió o actualizó correctamente

    def agregar_regla(self, regla: ReglaIncertidumbre) -> bool:
        """
        Añade una nueva regla al sistema
        """
        # Validar la regla según su tipo
        if regla.tipo == TipoIncertidumbre.FACTOR_CERTEZA:  # Si el modelo es de factor de certeza
            if not -1 <= regla.factor_certeza <= 1:  # El factor de certeza de la regla debe estar entre -1 y 1
                return False  # Retorna False si el rango es inválido
        else:  # Para modelos probabilísticos y difusos
            if not 0 <= regla.factor_certeza <= 1:  # El factor de certeza de la regla debe estar entre 0 y 1
                return False  # Retorna False si el rango es inválido

        self.reglas[regla.nombre] = regla  # Añade la nueva regla al diccionario de reglas usando su nombre como clave
        self.historial.append(f"Añadida regla {regla.nombre}")  # Registra la adición de la regla en el historial
        return True  # Retorna True si la regla se añadió correctamente

    def inferir(self, objetivo: str) -> Optional[float]:
        """
        Realiza inferencia con incertidumbre sobre un objetivo específico
        """
        if objetivo in self.hechos:  # Si el objetivo ya es un hecho conocido
            return self.hechos[objetivo].certeza  # Retorna su certeza actual

        # Buscar reglas que concluyan el objetivo
        reglas_aplicables = [  # Crea una lista de reglas cuya conclusión coincide con el objetivo
            r for r in self.reglas.values()
            if r.consecuente == objetivo
        ]

        if not reglas_aplicables:  # Si no se encontraron reglas que concluyan el objetivo
            return None  # No se puede inferir, retorna None

        certezas = []  # Lista para almacenar las certezas resultantes de aplicar las reglas

        for regla in reglas_aplicables:  # Itera sobre las reglas aplicables
            # Calcular certeza de los antecedentes
            certeza_antecedentes = self._calcular_certeza_antecedentes(regla)  # Llama a la función para calcular la certeza combinada de los antecedentes
            if certeza_antecedentes is not None:  # Si se pudo calcular la certeza de los antecedentes (no hay antecedentes desconocidos)
                # Aplicar factor de certeza de la regla
                if regla.tipo == TipoIncertidumbre.FACTOR_CERTEZA:  # Si el modelo es de factor de certeza
                    certeza_consecuente = certeza_antecedentes * regla.factor_certeza  # La certeza del consecuente es la certeza de los antecedentes multiplicada por el FC de la regla
                else:  # Para otros modelos
                    certeza_consecuente = certeza_antecedentes * regla.factor_certeza  # Similar al factor de certeza
                certezas.append(certeza_consecuente)  # Añade la certeza del consecuente a la lista de certezas

        if not certezas:  # Si no se pudo obtener certeza de ninguna regla aplicable
            return None  # No se pudo inferir, retorna None

        # Combinar las certezas de todas las reglas aplicables
        if reglas_aplicables[0].tipo == TipoIncertidumbre.FACTOR_CERTEZA:  # Si el modelo es de factor de certeza (MYCIN)
            # Combinación MYCIN de factores de certeza
            certeza_final = 0  # Inicializa la certeza final
            for c in certezas:  # Itera sobre las certezas obtenidas de las reglas
                if certeza_final >= 0 and c >= 0:  # Si ambas certezas son positivas o cero
                    certeza_final += c * (1 - certeza_final)  # Fórmula de combinación para certezas positivas
                elif certeza_final < 0 and c < 0:  # Si ambas certezas son negativas
                    certeza_final += c * (1 + certeza_final)  # Fórmula de combinación para certezas negativas
                else:  # Si las certezas tienen signos opuestos
                    certeza_final = (certeza_final + c) / (1 - min(abs(certeza_final), abs(c)))  # Fórmula de combinación para certezas con signos opuestos
        else:  # Para otros modelos
            # Para otros modelos, tomar el máximo
            certeza_final = max(certezas)  # Se toma la certeza más alta obtenida

        # Guardar el nuevo hecho inferido
        self.agregar_hecho(HechoIncertidumbre(  # Crea un nuevo hecho con la certeza inferida
            contenido=objetivo,
            certeza=certeza_final,
            tipo=reglas_aplicables[0].tipo,
            fuente=f"Inferido por {len(reglas_aplicables)} reglas"  # Indica que fue inferido por las reglas aplicables
        ))

        return certeza_final  # Retorna la certeza final inferida para el objetivo

    def _calcular_certeza_antecedentes(self, regla: ReglaIncertidumbre) -> Optional[float]:
        """
        Calcula la certeza combinada de los antecedentes de una regla
        """
        certezas = []  # Lista para almacenar las certezas de los antecedentes

        for premisa, peso in regla.antecedentes:  # Itera sobre los antecedentes de la regla (premisa y su peso)
            if premisa not in self.hechos:  # Si alguna premisa no es un hecho conocido
                return None  # No se puede calcular la certeza de los antecedentes, retorna None

            hecho = self.hechos[premisa]  # Obtiene el hecho correspondiente a la premisa
            certeza_premisa = hecho.certeza * peso  # La certeza de la premisa se ve afectada por su peso

            # Para factores de certeza, ajustar rango
            if hecho.tipo == TipoIncertidumbre.FACTOR_CERTEZA:  # Si el modelo es de factor de certeza
                certeza_premisa = max(-1, min(1, certeza_premisa))  # Asegura que la certeza esté en el rango [-1, 1]
            else:  # Para otros modelos
                certeza_premisa = max(0, min(1, certeza_premisa))  # Asegura que la certeza esté en el rango [0, 1]

            certezas.append(certeza_premisa)  # Añade la certeza de la premisa (con su peso) a la lista de certezas

        # Calcular combinación según tipo de regla
        if regla.tipo == TipoIncertidumbre.FACTOR_CERTEZA:  # Si el modelo es de factor de certeza (MYCIN)
            # Para MYCIN, tomar el mínimo de los antecedentes
            return min(certezas) if certezas else 0  # La certeza de los antecedentes es el mínimo de las certezas de las premisas
        else:  # Para otros modelos
            # Para otros modelos, tomar el producto
            return math.prod(certezas) if certezas else 0  # La certeza de los antecedentes es el producto de las certezas de las premisas

    def mostrar_estado(self) -> Dict:
        """
        Muestra el estado actual del sistema
        """
        return {  # Retorna un diccionario con el estado del sistema
            "total_hechos": len(self.hechos),  # Número total de hechos en el sistema
            "hechos_positivos": sum(1 for h in self.hechos.values() if h.certeza > 0),  # Número de hechos con certeza positiva
            "hechos_negativos": sum(1 for h in self.hechos.values() if h.certeza < 0),  # Número de hechos con certeza negativa
            "total_reglas": len(self.reglas),  # Número total de reglas en el sistema
            "ultimas_operaciones": self.historial[-5:] if self.historial else []  # Las últimas 5 operaciones realizadas (si hay alguna)
        }

def ejemplo_mycin():
    """
    Demuestra el sistema con el clásico modelo de factores de certeza de MYCIN
    para diagnóstico médico.
    """
    sistema = SistemaIncertidumbre()  # Crea una instancia del sistema de incertidumbre

    # 1. Añadir hechos iniciales (síntomas y datos del paciente)
    sistema.agregar_hecho(HechoIncertidumbre(  # Añade el hecho "Fiebre alta" con una certeza de 0.8 (factor de certeza)
        contenido="Fiebre alta",
        certeza=0.8,
        tipo=TipoIncertidumbre.FACTOR_CERTEZA,
        fuente="Observación médica"
    ))

    sistema.agregar_hecho(HechoIncertidumbre(  # Añade el hecho "Dolor de cabeza" con una certeza de 0.6 (factor de certeza)
        contenido="Dolor de cabeza",
        certeza=0.6,
        tipo=TipoIncertidumbre.FACTOR_CERTEZA,
        fuente="Reporte paciente"
    ))

    # 2. Añadir reglas de diagnóstico (simplificadas)
    sistema.agregar_regla(ReglaIncertidumbre(  # Añade la regla R1: Si hay fiebre alta (peso 0.9) Y dolor de cabeza (peso 0.7), ENTONCES hay Gripe (FC 0.8)
        nombre="R1",
        antecedentes=[("Fiebre alta", 0.9), ("Dolor de cabeza", 0.7)],
        consecuente="Gripe",
        factor_certeza=0.8,
        tipo=TipoIncertidumbre.FACTOR_CERTEZA
    ))

    sistema.agregar_regla(ReglaIncertidumbre(  # Añade la regla R2: Si hay fiebre alta (peso 1.0) Y dolor de cabeza (peso 0.3), ENTONCES hay Sinusitis (FC 0.6)
        nombre="R2",
        antecedentes=[("Fiebre alta", 1.0), ("Dolor de cabeza", 0.3)],
        consecuente="Sinusitis",
        factor_certeza=0.6,
        tipo=TipoIncertidumbre.FACTOR_CERTEZA
    ))

    # 3. Realizar inferencia
    print("\n=== DIAGNÓSTICO MÉDICO CON FACTORES DE CERTEZA ===")  # Imprime un encabezado
    print("\nInferiendo diagnóstico de Gripe...")  # Indica que se está infiriendo la certeza de "Gripe"
    certeza_gripe = sistema.inferir("Gripe")  # Llama a la función de inferencia para obtener la certeza de "Gripe"
    print(f"Certeza de Gripe: {certeza_gripe:.2f}")  # Imprime la certeza inferida para "Gripe"

    print("\nInferiendo diagnóstico de Sinusitis...")  # Indica que se está infiriendo la certeza de "Sinusitis"
    certeza_sinusitis = sistema.inferir("Sinusitis")  # Llama a la función de inferencia para obtener la certeza de "Sinusitis"
    print(f"Certeza de Sinusitis: {certeza_sinusitis:.2f}")  # Imprime la certeza inferida para "Sinusitis"

    # 4. Mostrar estado del sistema
    print("\nEstado del sistema:")  # Imprime un encabezado para el estado del sistema
    for k, v in sistema.mostrar_estado().items():  # Itera sobre los elementos del estado del sistema
        print(f"{k}: {v}")  # Imprime la clave y el valor de cada elemento del estado

if __name__ == "__main__":
    ejemplo_mycin()  # Llama a la función de ejemplo cuando el script se ejecuta directamente