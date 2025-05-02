

# Importación de librerías necesarias
import numpy as np  # Para operaciones numéricas avanzadas
from collections import defaultdict  # Para diccionarios con valores por defecto
from typing import Dict, List, Tuple, Union  # Para anotaciones de tipo

class ProbabilityCalculator:
    # Constructor de la clase
    def __init__(self):
        """Inicializa el calculador con estructuras para conteo de probabilidades"""
        # Diccionario para conteos conjuntos de (X,Y) con valor por defecto 0
        self.joint_counts = defaultdict(int)
        # Diccionario para conteos marginales de X con valor por defecto 0
        self.marginal_counts = defaultdict(int)
        # Contador total de observaciones registradas
        self.total_observations = 0
    
    # Método para registrar observaciones conjuntas
    def add_observation(self, x: str, y: str) -> None:
        """
        Registra una observación conjunta de variables X e Y.
        
        Args:
            x (str): Valor de la variable X
            y (str): Valor de la variable Y
        """
        # Incrementa el contador para el par (X,Y)
        self.joint_counts[(x, y)] += 1
        # Incrementa el contador marginal para X
        self.marginal_counts[x] += 1
        # Incrementa el contador total de observaciones
        self.total_observations += 1
    
    # Método para calcular probabilidad conjunta P(X=x, Y=y)
    def joint_probability(self, x: str, y: str) -> float:
        """
        Calcula la probabilidad conjunta como frecuencia relativa.
        
        Args:
            x (str): Valor de X
            y (str): Valor de Y
            
        Returns:
            float: Probabilidad conjunta estimada (0 si no hay datos)
        """
        # Maneja caso cuando no hay observaciones
        if self.total_observations == 0:
            return 0.0
        # Calcula P(X,Y) = conteo(X,Y) / total_observaciones
        return self.joint_counts[(x, y)] / self.total_observations
    
    # Método para calcular probabilidad marginal P(X=x)
    def marginal_probability(self, x: str) -> float:
        """
        Calcula la probabilidad marginal de X.
        
        Args:
            x (str): Valor de X
            
        Returns:
            float: Probabilidad marginal estimada (0 si no hay datos)
        """
        # Maneja caso cuando no hay observaciones
        if self.total_observations == 0:
            return 0.0
        # Calcula P(X) = conteo(X) / total_observaciones
        return self.marginal_counts[x] / self.total_observations
    
    # Método para calcular probabilidad condicional P(Y=y|X=x)
    def conditional_probability(self, x: str, y: str) -> float:
        """
        Calcula la probabilidad condicional usando definición clásica.
        
        Args:
            x (str): Valor de la condición X
            y (str): Valor de Y dado X
            
        Returns:
            float: Probabilidad condicional estimada (0 si X no observado)
        """
        # Maneja caso cuando X no ha sido observado
        if self.marginal_counts[x] == 0:
            return 0.0
        # Calcula P(Y|X) = P(X,Y) / P(X) = conteo(X,Y) / conteo(X)
        return self.joint_counts[(x, y)] / self.marginal_counts[x]
    
    # Método para normalizar probabilidades
    def normalize_probabilities(self, probabilities: Dict[str, float]) -> Dict[str, float]:
        """
        Normaliza valores para que sumen 1 (distribución de probabilidad válida).
        
        Args:
            probabilities (Dict[str, float]): Valores no normalizados
            
        Returns:
            Dict[str, float]: Valores normalizados que suman 1
        """
        # Calcula la suma total de los valores
        total = sum(probabilities.values())
        # Maneja caso cuando la suma es 0 (evita división por cero)
        if total == 0:
            return {k: 0.0 for k in probabilities}
        # Divide cada valor por la suma total para normalizar
        return {k: v/total for k, v in probabilities.items()}
    
    # Método para aplicar función softmax
    def softmax(self, values: Dict[str, float], temperature: float = 1.0) -> Dict[str, float]:
        """
        Transforma valores arbitrarios en probabilidades usando softmax.
        
        Args:
            values (Dict[str, float]): Valores a transformar
            temperature (float): Parámetro que controla la suavidad (default 1.0)
            
        Returns:
            Dict[str, float]: Probabilidades resultantes
        """
        # Maneja caso de diccionario vacío
        if not values:
            return {}
            
        # Prepara los datos para el cálculo
        keys = list(values.keys())  # Lista de claves
        vals = np.array([values[k] for k in keys]) / temperature  # Aplica temperatura
        
        # Cálculo numéricamente estable de softmax
        exp_vals = np.exp(vals - np.max(vals))  # Resta el máximo para estabilidad
        softmax_probs = exp_vals / np.sum(exp_vals)  # Normaliza para sumar 1
        
        # Reconstruye el diccionario con los resultados
        return {k: softmax_probs[i] for i, k in enumerate(keys)}
    
    # Método para inferencia bayesiana
    def bayesian_inference(self, prior: Dict[str, float], 
                         likelihoods: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, float]]:
        """
        Realiza inferencia bayesiana para múltiples evidencias posibles.
        
        Args:
            prior (Dict[str, float]): Probabilidades a priori P(X)
            likelihoods (Dict[str, Dict[str, float]]): Verosimilitudes P(Y|X) para cada Y
            
        Returns:
            Dict[str, Dict[str, float]]: Probabilidades posteriores P(X|Y) para cada Y
        """
        # Verifica y normaliza las probabilidades a priori si es necesario
        if not np.isclose(sum(prior.values()), 1.0, atol=1e-3):
            prior = self.normalize_probabilities(prior)
        
        # Diccionario para almacenar todos los resultados
        posteriors = {}
        
        # Calcula posteriores para cada tipo de evidencia Y
        for y in likelihoods:
            # Calcula P(Y) = sumatoria sobre X de P(Y|X)*P(X)
            py = sum(likelihoods[y][x] * prior[x] for x in prior)
            
            # Calcula P(X|Y) para cada X
            posterior = {}
            for x in prior:
                if py > 0:
                    # Aplica teorema de Bayes: P(X|Y) = P(Y|X)*P(X)/P(Y)
                    posterior[x] = (likelihoods[y][x] * prior[x]) / py
                else:
                    posterior[x] = 0.0  # Si P(Y)=0, no hay información
            
            posteriors[y] = posterior  # Almacena resultados para esta evidencia
        
        return posteriors

# Bloque principal de demostración
if __name__ == "__main__":
    print("=== Probabilidad Condicionada y Normalización ===\n")
    
    # Crea instancia del calculador
    pc = ProbabilityCalculator()
    
    # Datos de ejemplo: condiciones climáticas (X) y actividades (Y)
    data = [
        ('soleado', 'playa'),
        ('soleado', 'playa'),
        ('soleado', 'parque'),
        ('nublado', 'parque'),
        ('nublado', 'centro_comercial'),
        ('lluvia', 'centro_comercial'),
        ('lluvia', 'centro_comercial'),
        ('lluvia', 'cine'),
        ('nublado', 'parque'),
        ('soleado', 'playa')
    ]
    
    # Registra todas las observaciones
    for x, y in data:
        pc.add_observation(x, y)
    
    # 1. Demostración de probabilidades conjuntas y marginales
    print("1. Probabilidades Conjuntas y Marginales:")
    print(f"P(soleado, playa) = {pc.joint_probability('soleado', 'playa'):.2f}")
    print(f"P(nublado) = {pc.marginal_probability('nublado'):.2f}\n")
    
    # 2. Demostración de probabilidades condicionales
    print("2. Probabilidades Condicionadas:")
    print(f"P(playa|soleado) = {pc.conditional_probability('soleado', 'playa'):.2f}")
    print(f"P(cine|lluvia) = {pc.conditional_probability('lluvia', 'cine'):.2f}\n")
    
    # 3. Demostración de normalización
    print("3. Normalización de Probabilidades:")
    unnormalized = {'A': 3, 'B': 2, 'C': 5}  # Valores no normalizados
    print(f"Antes de normalizar: {unnormalized}")
    normalized = pc.normalize_probabilities(unnormalized)  # Aplica normalización
    print(f"Después de normalizar: { {k: round(v, 2) for k, v in normalized.items()} }\n")
    
    # 4. Demostración de función softmax
    print("4. Transformación Softmax:")
    scores = {'Opción1': 2.0, 'Opción2': 1.0, 'Opción3': 0.5}  # Puntuaciones
    print(f"Scores originales: {scores}")
    softmax_probs = pc.softmax(scores)  # Aplica softmax
    print(f"Probabilidades con softmax: { {k: round(v, 3) for k, v in softmax_probs.items()} }\n")
    
    # 5. Demostración de inferencia bayesiana
    print("5. Inferencia Bayesiana:")
    # Probabilidades a priori sobre estados de salud
    prior = {'Healthy': 0.7, 'Sick': 0.3}
    # Verosimilitudes de síntomas para cada estado
    likelihoods = {
        'Fever': {'Healthy': 0.01, 'Sick': 0.9},  # P(Fiebre|Estado)
        'NoFever': {'Healthy': 0.99, 'Sick': 0.1}  # P(NoFiebre|Estado)
    }
    
    # Realiza inferencia bayesiana
    posteriors = pc.bayesian_inference(prior, likelihoods)
    # Muestra resultados para cada evidencia posible
    for evidence, posterior in posteriors.items():
        print(f"\nEvidencia: {evidence}")
        for state, prob in posterior.items():
            print(f"P({state}|{evidence}) = {prob:.4f}")