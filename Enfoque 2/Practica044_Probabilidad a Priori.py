

# Importación de la librería numpy para operaciones numéricas avanzadas
import numpy as np  

# Importación de defaultdict para crear diccionarios con valores por defecto
from collections import defaultdict  

# Importación de tipos para anotaciones de tipo (type hints)
from typing import Dict, List, Tuple  

# Definición de la clase principal para manejar probabilidades a priori
class PriorProbability:
    # Método constructor de la clase
    def __init__(self):
        """Inicializa el calculador con estructuras para conteo de categorías"""
        # defaultdict que inicializa nuevos elementos con valor 0 (int)
        self.category_counts = defaultdict(int)  
        # Contador total de observaciones registradas
        self.total_count = 0  
    
    # Método para añadir una observación individual
    def add_observation(self, category: str) -> None:
        """
        Registra una nueva observación de una categoría.
        
        Args:
            category (str): Nombre de la categoría a registrar
        """
        # Incrementa el contador específico de la categoría
        self.category_counts[category] += 1  
        # Incrementa el contador total de observaciones
        self.total_count += 1  
    
    # Método para añadir múltiples observaciones
    def add_batch_observations(self, observations: List[str]) -> None:
        """
        Registra un conjunto de observaciones.
        
        Args:
            observations (List[str]): Lista de categorías a registrar
        """
        # Itera sobre cada elemento de la lista de observaciones
        for category in observations:  
            # Llama al método de añadir observación individual
            self.add_observation(category)  
    
    # Método para calcular probabilidad de una categoría
    def get_prior_probability(self, category: str) -> float:
        """
        Calcula P(categoría) = conteo(categoría)/total_observaciones
        
        Args:
            category (str): Categoría a calcular
            
        Returns:
            float: Probabilidad estimada (0 si no hay datos)
        """
        # Comprueba si no hay observaciones registradas
        if self.total_count == 0:  
            return 0.0  # Devuelve 0 para evitar división por cero
        # Calcula la probabilidad como frecuencia relativa
        return self.category_counts[category] / self.total_count  
    
    # Método para obtener todas las probabilidades
    def get_all_priors(self) -> Dict[str, float]:
        """
        Obtiene las probabilidades para todas las categorías registradas.
        
        Returns:
            Dict[str, float]: Diccionario {categoría: probabilidad}
        """
        # Diccionario por comprensión que mapea cada categoría a su probabilidad
        return {cat: self.get_prior_probability(cat) for cat in self.category_counts}  
    
    # Método para actualización bayesiana
    def bayesian_update(self, prior: Dict[str, float], likelihood: Dict[str, float]) -> Dict[str, float]:
        """
        Actualiza creencias usando el teorema de Bayes: P(H|D) = P(D|H)*P(H)/P(D)
        
        Args:
            prior (Dict[str, float]): Probabilidades a priori P(H)
            likelihood (Dict[str, float]): Verosimilitudes P(D|H)
            
        Returns:
            Dict[str, float]: Probabilidades posteriores P(H|D)
            
        Raises:
            ValueError: Si las probabilidades a priori no suman ~1
        """
        # Verifica que las probabilidades a priori sumen aproximadamente 1
        if not np.isclose(sum(prior.values()), 1.0, atol=1e-3):  
            raise ValueError("Las probabilidades a priori deben sumar 1")
            
        # Calcula P(D) = sum(P(D|H_i)*P(H_i)) para todas las hipótesis
        marginal = sum(prior[h] * likelihood[h] for h in prior)  
        
        # Calcula P(H|D) para cada hipótesis
        posterior = {h: (prior[h] * likelihood[h]) / marginal for h in prior}  
        return posterior  
    
    # Método para suavizado de Laplace
    def laplace_smoothing(self, category: str, alpha: float = 1.0) -> float:
        """
        Aplica suavizado de Laplace para evitar probabilidades cero.
        
        Fórmula: P = (count(category) + alpha)/(total + alpha*num_categories)
        
        Args:
            category (str): Categoría a calcular
            alpha (float, optional): Factor de suavizado. Default 1.0
            
        Returns:
            float: Probabilidad suavizada
        """
        # Maneja caso cuando no hay observaciones
        if self.total_count == 0:  
            return 0.0  
            
        # Obtiene el número total de categorías distintas
        total_categories = len(self.category_counts)  
        # Aplica la fórmula de suavizado de Laplace
        return (self.category_counts[category] + alpha) / (self.total_count + alpha * total_categories)  

# Ejemplo de uso del módulo
if __name__ == "__main__":
    # Título del ejemplo
    print("=== Ejemplo de Probabilidad a Priori ===\n")  
    
    # 1. Ejemplo básico de probabilidades a priori
    print("1. Probabilidades a priori básicas:")  
    # Crea una instancia del calculador
    pp = PriorProbability()  
    # Datos de ejemplo (condiciones meteorológicas)
    weather_data = ['soleado', 'soleado', 'nublado', 'lluvia', 'soleado', 
                   'nublado', 'nublado', 'soleado', 'lluvia', 'lluvia']  
    # Añade todos los datos de una vez
    pp.add_batch_observations(weather_data)  
    
    # Obtiene y muestra todas las probabilidades calculadas
    priors = pp.get_all_priors()  
    for category, prob in priors.items():  
        print(f"P({category}) = {prob:.2f}")  
    
    # 2. Ejemplo de actualización bayesiana
    print("\n2. Actualización bayesiana:")  
    # Define probabilidades a priori iniciales
    hypotheses_prior = {'H1': 0.5, 'H2': 0.3, 'H3': 0.2}  
    # Define verosimilitudes de los datos para cada hipótesis
    likelihoods = {'H1': 0.7, 'H2': 0.2, 'H3': 0.1}  
    
    # Realiza la actualización bayesiana
    posterior = pp.bayesian_update(hypotheses_prior, likelihoods)  
    # Muestra las probabilidades posteriores
    for h, prob in posterior.items():  
        print(f"P({h}|D) = {prob:.4f}")  
    
    # 3. Ejemplo de suavizado de Laplace
    print("\n3. Suavizado de Laplace:")  
    # Muestra probabilidad para categoría no vista en los datos
    print("Probabilidad para 'nieve' (no vista):")  
    print(f"Sin suavizado: P(nieve) = {pp.get_prior_probability('nieve'):.2f}")  
    print(f"Con suavizado (α=1): P(nieve) = {pp.laplace_smoothing('nieve'):.4f}")  
    
    # 4. Ejemplo completo con clasificador Naive Bayes
    print("\n4. Ejemplo con clasificador Naive Bayes:")  
    # Datos de entrenamiento (clase, característica)
    train_data = [
        ('bueno', 'soleado'),
        ('bueno', 'soleado'),
        ('bueno', 'nublado'),
        ('malo', 'lluvia'),
        ('malo', 'lluvia'),
        ('malo', 'nublado'),
        ('bueno', 'nublado'),
        ('bueno', 'soleado')
    ]  
    
    # Inicializa calculador para probabilidades de clase
    class_pp = PriorProbability()  
    # Inicializa diccionario de calculadores para P(característica|clase)
    feature_pp = defaultdict(PriorProbability)  
    
    # Procesa cada observación del conjunto de entrenamiento
    for label, feature in train_data:  
        # Añade la clase al contador general
        class_pp.add_observation(label)  
        # Añade la característica al contador específico de esa clase
        feature_pp[label].add_observation(feature)  
    
    # Muestra las probabilidades a priori de cada clase
    print("\nProbabilidades a priori de clases:")  
    for cls, prob in class_pp.get_all_priors().items():  
        print(f"P({cls}) = {prob:.2f}")  
    
    # Muestra las probabilidades condicionales P(característica|clase)
    print("\nProbabilidades condicionales:")  
    for label in feature_pp:  
        print(f"\nPara clase '{label}':")  
        for feature, prob in feature_pp[label].get_all_priors().items():  
            print(f"P({feature}|{label}) = {prob:.2f}")  