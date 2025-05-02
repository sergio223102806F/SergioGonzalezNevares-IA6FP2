


# Importación de librerías necesarias
import numpy as np  # Para operaciones numéricas
from typing import Dict, List, Tuple  # Para anotaciones de tipo
from collections import defaultdict  # Para diccionarios con valores por defecto

class BayesRuleCalculator:
    def __init__(self):
        """Inicializa el calculador de la Regla de Bayes"""
        # Diccionario para almacenar conteos de eventos (hipótesis)
        self.hypothesis_counts = defaultdict(int)
        # Diccionario para almacenar conteos de evidencias dado cada hipótesis
        self.evidence_counts = defaultdict(lambda: defaultdict(int))
        # Contador total de observaciones
        self.total_observations = 0
    
    def add_observation(self, hypothesis: str, evidence: str) -> None:
        """
        Registra una observación de una hipótesis con su evidencia correspondiente.
        
        Args:
            hypothesis: Hipótesis observada (categoría o clase)
            evidence: Evidencia observada (característica o síntoma)
        """
        # Incrementa el contador para la hipótesis
        self.hypothesis_counts[hypothesis] += 1
        # Incrementa el contador para la evidencia dada la hipótesis
        self.evidence_counts[hypothesis][evidence] += 1
        # Incrementa el contador total
        self.total_observations += 1
    
    def prior_probability(self, hypothesis: str) -> float:
        """
        Calcula la probabilidad a priori P(H) de una hipótesis.
        
        Args:
            hypothesis: Hipótesis a calcular
            
        Returns:
            Probabilidad a priori estimada
        """
        if self.total_observations == 0:
            return 0.0  # Evita división por cero
        return self.hypothesis_counts[hypothesis] / self.total_observations
    
    def likelihood(self, evidence: str, hypothesis: str) -> float:
        """
        Calcula la verosimilitud P(E|H) de la evidencia dada la hipótesis.
        
        Args:
            evidence: Evidencia observada
            hypothesis: Hipótesis dada
            
        Returns:
            Verosimilitud estimada
        """
        if self.hypothesis_counts[hypothesis] == 0:
            return 0.0  # Evita división por cero
        return self.evidence_counts[hypothesis][evidence] / self.hypothesis_counts[hypothesis]
    
    def marginal_evidence_probability(self, evidence: str) -> float:
        """
        Calcula la probabilidad marginal de la evidencia P(E).
        
        Args:
            evidence: Evidencia a calcular
            
        Returns:
            Probabilidad marginal estimada
        """
        if self.total_observations == 0:
            return 0.0
        # Suma P(E|H_i)*P(H_i) para todas las hipótesis
        total = 0.0
        for hypo in self.hypothesis_counts:
            total += self.likelihood(evidence, hypo) * self.prior_probability(hypo)
        return total
    
    def posterior_probability(self, hypothesis: str, evidence: str) -> float:
        """
        Calcula la probabilidad posterior P(H|E) usando la Regla de Bayes.
        
        Args:
            hypothesis: Hipótesis a evaluar
            evidence: Evidencia observada
            
        Returns:
            Probabilidad posterior estimada
        """
        # P(E|H)
        likelihood = self.likelihood(evidence, hypothesis)
        # P(H)
        prior = self.prior_probability(hypothesis)
        # P(E)
        marginal = self.marginal_evidence_probability(evidence)
        
        if marginal == 0:
            return 0.0  # Evita división por cero
        
        # Aplica la Regla de Bayes: P(H|E) = P(E|H)*P(H)/P(E)
        return (likelihood * prior) / marginal
    
    def update_with_evidence(self, evidence_list: List[str]) -> Dict[str, float]:
        """
        Actualiza las probabilidades secuencialmente con múltiples evidencias.
        
        Args:
            evidence_list: Lista de evidencias observadas en orden
            
        Returns:
            Probabilidades posteriores finales
        """
        # Comienza con las probabilidades a priori
        posteriors = {hypo: self.prior_probability(hypo) for hypo in self.hypothesis_counts}
        
        # Actualiza secuencialmente con cada evidencia
        for evidence in evidence_list:
            new_posteriors = {}
            total = 0.0
            
            # Calcula el denominador (probabilidad marginal de la evidencia)
            for hypo in posteriors:
                total += self.likelihood(evidence, hypo) * posteriors[hypo]
            
            # Calcula los nuevos posteriores
            for hypo in posteriors:
                if total > 0:
                    new_posteriors[hypo] = (self.likelihood(evidence, hypo) * posteriors[hypo]) / total
                else:
                    new_posteriors[hypo] = 0.0
            
            posteriors = new_posteriors
        
        return posteriors


# Ejemplo de uso médico
if __name__ == "__main__":
    print("=== Ejemplo de la Regla de Bayes en Diagnóstico Médico ===\n")
    
    # Crear instancia del calculador
    brc = BayesRuleCalculator()
    
    # Datos de entrenamiento: (enfermedad, síntoma)
    training_data = [
        ('gripe', 'fiebre'), ('gripe', 'fiebre'), ('gripe', 'tos'),
        ('resfriado', 'tos'), ('resfriado', 'congestión'), ('resfriado', 'congestión'),
        ('alergia', 'congestión'), ('alergia', 'estornudos'), ('alergia', 'estornudos'),
        ('gripe', 'fiebre'), ('resfriado', 'tos'), ('alergia', 'congestión')
    ]
    
    # Agregar datos de entrenamiento
    for disease, symptom in training_data:
        brc.add_observation(disease, symptom)
    
    # 1. Mostrar probabilidades a priori
    print("1. Probabilidades a priori de las enfermedades:")
    diseases = brc.hypothesis_counts.keys()
    for disease in diseases:
        print(f"P({disease}) = {brc.prior_probability(disease):.3f}")
    
    # 2. Mostrar verosimilitudes de síntomas
    print("\n2. Verosimilitudes de síntomas para cada enfermedad:")
    symptoms = set(sym for _, sym in training_data)
    for disease in diseases:
        print(f"\nPara {disease}:")
        for symptom in symptoms:
            print(f"  P({symptom}|{disease}) = {brc.likelihood(symptom, disease):.3f}")
    
    # 3. Calcular probabilidad posterior para un síntoma
    print("\n3. Probabilidad posterior dada fiebre:")
    for disease in diseases:
        posterior = brc.posterior_probability(disease, 'fiebre')
        print(f"P({disease}|fiebre) = {posterior:.3f}")
    
    # 4. Actualización secuencial con múltiples síntomas
    print("\n4. Actualización secuencial con ['congestión', 'tos']:")
    final_posteriors = brc.update_with_evidence(['congestión', 'tos'])
    for disease, prob in final_posteriors.items():
        print(f"P({disease}|evidencia) = {prob:.3f}")
    
    # 5. Ejemplo completo con nuevos datos
    print("\n5. Ejemplo completo con nuevos síntomas:")
    test_symptoms = ['fiebre', 'tos']
    print(f"Síntomas observados: {test_symptoms}")
    
    # Calcular probabilidades posteriores
    posteriors = brc.update_with_evidence(test_symptoms)
    
    # Mostrar resultados
    most_likely = max(posteriors.items(), key=lambda x: x[1])
    print("\nResultados del diagnóstico:")
    for disease, prob in posteriors.items():
        print(f"- {disease}: {prob*100:.1f}% probabilidad")
    
    print(f"\nDiagnóstico más probable: {most_likely[0]} ({most_likely[1]*100:.1f}% probabilidad)")