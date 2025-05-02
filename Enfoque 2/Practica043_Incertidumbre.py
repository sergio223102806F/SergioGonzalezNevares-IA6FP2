
# Importación de librerías necesarias
import numpy as np  # Para operaciones numéricas y generación de números aleatorios
from enum import Enum  # Para crear enumeraciones de tipos de incertidumbre
from typing import Dict, Tuple, List  # Para anotaciones de tipos

# Definición de los tipos de incertidumbre como enumeración
class UncertaintyType(Enum):
    PROBABILISTIC = 1  # Método probabilístico clásico
    FUZZY = 2  # Lógica difusa
    DEMPSTER_SHAFER = 3  # Teoría de Dempster-Shafer

# Clase principal para manejar diferentes tipos de incertidumbre
class UncertaintyManager:
    def __init__(self):
        """Inicializa el gestor de incertidumbre con diferentes métodos"""
        pass  # No necesita inicialización especial
    
    # Método para manejar incertidumbre probabilística
    def probabilistic_uncertainty(self, probabilities: Dict[str, float]) -> Tuple[str, float]:
        """
        Maneja incertidumbre usando probabilidades clásicas.
        
        Args:
            probabilities: Diccionario de opciones con sus probabilidades (deben sumar 1)
            
        Returns:
            Tupla con la opción seleccionada y su probabilidad
        """
        # Verifica que las probabilidades sumen aproximadamente 1
        if not np.isclose(sum(probabilities.values()), 1.0, atol=1e-3):
            raise ValueError("Las probabilidades deben sumar 1")
            
        # Prepara las opciones y probabilidades para la selección aleatoria
        options = list(probabilities.keys())  # Lista de opciones
        probs = list(probabilities.values())  # Lista de probabilidades
        chosen = np.random.choice(options, p=probs)  # Selección aleatoria basada en probabilidades
        return chosen, probabilities[chosen]  # Retorna opción seleccionada y su probabilidad
    
    # Método para calcular membresía difusa
    def fuzzy_membership(self, value: float, low: float, medium: float, high: float) -> Dict[str, float]:
        """
        Calcula los grados de pertenencia difusa para un valor dado.
        
        Args:
            value: Valor a evaluar
            low: Límite superior para 'bajo'
            medium: Punto medio para 'medio'
            high: Límite inferior para 'alto'
            
        Returns:
            Diccionario con los grados de pertenencia para cada conjunto difuso
        """
        # Inicializa los grados de pertenencia
        memberships = {
            'bajo': 0.0,
            'medio': 0.0,
            'alto': 0.0
        }
        
        # Función de pertenencia para 'bajo' (triangular izquierda)
        if value <= low:
            memberships['bajo'] = 1.0  # Máxima pertenencia si está debajo del límite bajo
        elif value < medium:
            memberships['bajo'] = (medium - value) / (medium - low)  # Cálculo lineal
        
        # Función de pertenencia para 'medio' (triangular)
        if low < value <= medium:
            memberships['medio'] = (value - low) / (medium - low)  # Pendiente ascendente
        elif medium < value < high:
            memberships['medio'] = (high - value) / (high - medium)  # Pendiente descendente
        
        # Función de pertenencia para 'alto' (triangular derecha)
        if value >= high:
            memberships['alto'] = 1.0  # Máxima pertenencia si está arriba del límite alto
        elif value > medium:
            memberships['alto'] = (value - medium) / (high - medium)  # Cálculo lineal
            
        return memberships  # Retorna los grados de pertenencia calculados
    
    # Método para combinar evidencias usando Dempster-Shafer
    def dempster_shafer(self, evidence1: Dict[str, float], evidence2: Dict[str, float]) -> Dict[str, float]:
        """
        Combina dos evidencias usando la teoría de Dempster-Shafer.
        
        Args:
            evidence1: Primer conjunto de evidencias (hipótesis -> masa)
            evidence2: Segundo conjunto de evidencias (hipótesis -> masa)
            
        Returns:
            Diccionario con las masas combinadas
        """
        # Verificar que las evidencias sumen 1 (normalizadas)
        if not np.isclose(sum(evidence1.values()), 1.0, atol=1e-3) or not np.isclose(sum(evidence2.values()), 1.0, atol=1e-3):
            raise ValueError("Las masas de evidencia deben sumar 1")
            
        # Obtener todas las hipótesis únicas de ambas evidencias
        hypotheses = set(evidence1.keys()).union(set(evidence2.keys()))
        # Inicializar el resultado combinado
        combined = {h: 0.0 for h in hypotheses}
        conflict = 0.0  # Medida de conflicto entre evidencias
        
        # Calcular combinación y conflicto
        for h1 in evidence1:
            for h2 in evidence2:
                if h1 == h2:  # Si las hipótesis coinciden
                    combined[h1] += evidence1[h1] * evidence2[h2]  # Combinar masas
                else:
                    conflict += evidence1[h1] * evidence2[h2]  # Acumular conflicto
        
        # Normalizar considerando el conflicto (regla de combinación)
        if conflict < 1.0:
            for h in combined:
                combined[h] /= (1.0 - conflict)  # Normalización
        
        return combined  # Retorna las masas combinadas
    
    # Método principal para manejar incertidumbre
    def handle_uncertainty(self, method: UncertaintyType, **kwargs):
        """
        Método principal para manejar diferentes tipos de incertidumbre.
        
        Args:
            method: Tipo de método a usar (PROBABILISTIC, FUZZY, DEMPSTER_SHAFER)
            **kwargs: Argumentos específicos para cada método
        """
        # Selecciona el método apropiado basado en el tipo de incertidumbre
        if method == UncertaintyType.PROBABILISTIC:
            return self.probabilistic_uncertainty(kwargs['probabilities'])
        elif method == UncertaintyType.FUZZY:
            return self.fuzzy_membership(kwargs['value'], kwargs['low'], kwargs['medium'], kwargs['high'])
        elif method == UncertaintyType.DEMPSTER_SHAFER:
            return self.dempster_shafer(kwargs['evidence1'], kwargs['evidence2'])
        else:
            raise ValueError("Método de incertidumbre no soportado")


# Bloque principal de ejecución (ejemplos de uso)
if __name__ == "__main__":
    um = UncertaintyManager()  # Crear instancia del gestor de incertidumbre
    
    # Ejemplo 1: Incertidumbre probabilística
    print("\n1. Incertidumbre Probabilística:")
    prob_result = um.handle_uncertainty(
        UncertaintyType.PROBABILISTIC,
        probabilities={'A': 0.3, 'B': 0.5, 'C': 0.2}
    )
    print(f"Opción seleccionada: {prob_result[0]} con probabilidad {prob_result[1]}")
    
    # Ejemplo 2: Lógica difusa
    print("\n2. Lógica Difusa:")
    fuzzy_result = um.handle_uncertainty(
        UncertaintyType.FUZZY,
        value=65,
        low=30,
        medium=60,
        high=90
    )
    print(f"Grados de pertenencia: {fuzzy_result}")
    
    # Ejemplo 3: Teoría de Dempster-Shafer
    print("\n3. Teoría de Dempster-Shafer:")
    ds_result = um.handle_uncertainty(
        UncertaintyType.DEMPSTER_SHAFER,
        evidence1={'H1': 0.6, 'H2': 0.3, 'H3': 0.1},
        evidence2={'H1': 0.5, 'H2': 0.2, 'H3': 0.3}
    )
    print(f"Evidencia combinada: {ds_result}")