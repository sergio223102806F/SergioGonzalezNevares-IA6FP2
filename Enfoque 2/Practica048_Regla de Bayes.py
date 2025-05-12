# Importación de la librería numpy para operaciones numéricas
import numpy as np
# Importación de tipos para anotaciones de función
from typing import Dict, List, Tuple
# Importación de defaultdict para diccionarios con valores por defecto
from collections import defaultdict

# Definición de la clase principal para cálculo de probabilidades bayesianas
class BayesRuleCalculator:
    # Método constructor de la clase
    def __init__(self):
        # Diccionario para contar ocurrencias de cada hipótesis
        self.hypothesis_counts = defaultdict(int)
        # Diccionario anidado para contar evidencias por hipótesis
        self.evidence_counts = defaultdict(lambda: defaultdict(int))
        # Contador total de observaciones registradas
        self.total_observations = 0
    
    # Método para agregar una nueva observación al sistema
    def add_observation(self, hypothesis: str, evidence: str) -> None:
        # Incrementa el contador para la hipótesis dada
        self.hypothesis_counts[hypothesis] += 1
        # Incrementa el contador para la evidencia bajo esta hipótesis
        self.evidence_counts[hypothesis][evidence] += 1
        # Incrementa el contador total de observaciones
        self.total_observations += 1
    
    # Método para calcular probabilidad a priori P(H)
    def prior_probability(self, hypothesis: str) -> float:
        # Verifica si hay observaciones para evitar división por cero
        if self.total_observations == 0:
            # Retorna 0 si no hay observaciones
            return 0.0
        # Calcula P(H) = count(H) / total_observations
        return self.hypothesis_counts[hypothesis] / self.total_observations
    
    # Método para calcular verosimilitud P(E|H)
    def likelihood(self, evidence: str, hypothesis: str) -> float:
        # Verifica si la hipótesis ha sido observada
        if self.hypothesis_counts[hypothesis] == 0:
            # Retorna 0 si la hipótesis nunca ocurrió
            return 0.0
        # Calcula P(E|H) = count(E∧H) / count(H)
        return self.evidence_counts[hypothesis][evidence] / self.hypothesis_counts[hypothesis]
    
    # Método para calcular probabilidad marginal P(E)
    def marginal_evidence_probability(self, evidence: str) -> float:
        # Inicializa el acumulador en 0.0
        total = 0.0
        # Itera sobre todas las hipótesis registradas
        for hypo in self.hypothesis_counts:
            # Acumula P(E|H_i)*P(H_i) para cada hipótesis
            total += self.likelihood(evidence, hypo) * self.prior_probability(hypo)
        # Retorna la suma total P(E)
        return total
    
    # Método para calcular probabilidad posterior P(H|E)
    def posterior_probability(self, hypothesis: str, evidence: str) -> float:
        # Obtiene P(E|H) del método likelihood
        likelihood = self.likelihood(evidence, hypothesis)
        # Obtiene P(H) del método prior_probability
        prior = self.prior_probability(hypothesis)
        # Obtiene P(E) del método marginal_evidence_probability
        marginal = self.marginal_evidence_probability(evidence)
        
        # Verifica que P(E) no sea cero para evitar división por cero
        if marginal == 0:
            # Retorna 0 si no hay evidencia registrada
            return 0.0
        
        # Aplica la fórmula de Bayes: P(H|E) = P(E|H)*P(H)/P(E)
        return (likelihood * prior) / marginal
    
    # Método para actualizar probabilidades con múltiples evidencias
    def update_with_evidence(self, evidence_list: List[str]) -> Dict[str, float]:
        # Inicializa posteriores con probabilidades a priori
        posteriors = {hypo: self.prior_probability(hypo) for hypo in self.hypothesis_counts}
        
        # Itera sobre cada evidencia en la lista proporcionada
        for evidence in evidence_list:
            # Prepara diccionario para nuevos posteriores
            new_posteriors = {}
            # Inicializa acumulador para normalización
            total = 0.0
            
            # Calcula el denominador para normalización
            for hypo in posteriors:
                # Acumula P(E|H)*P(H) para todas las hipótesis
                total += self.likelihood(evidence, hypo) * posteriors[hypo]
            
            # Calcula los nuevos valores posteriores
            for hypo in posteriors:
                # Verifica que el total no sea cero
                if total > 0:
                    # Calcula P(H|E) normalizado
                    new_posteriors[hypo] = (self.likelihood(evidence, hypo) * posteriors[hypo]) / total
                else:
                    # Asigna 0 si no hay evidencia compatible
                    new_posteriors[hypo] = 0.0
            
            # Actualiza los posteriores para la siguiente evidencia
            posteriors = new_posteriors
        
        # Retorna los posteriores finales después de todas las evidencias
        return posteriors


# Bloque principal de ejecución del programa
if __name__ == "__main__":
    # Mensaje de inicio del programa
    print("=== Sistema de Diagnóstico Médico con Bayes ===\n")
    
    # Crea una instancia del calculador bayesiano
    brc = BayesRuleCalculator()
    
    # Datos de entrenamiento: pares (enfermedad, síntoma)
    training_data = [
        ('gripe', 'fiebre'), ('gripe', 'fiebre'), ('gripe', 'tos'),
        ('resfriado', 'tos'), ('resfriado', 'congestión'), ('resfriado', 'congestión'),
        ('alergia', 'congestión'), ('alergia', 'estornudos'), ('alergia', 'estornudos'),
        ('gripe', 'fiebre'), ('resfriado', 'tos'), ('alergia', 'congestión')
    ]
    
    # Agrega cada observación al calculador bayesiano
    for disease, symptom in training_data:
        brc.add_observation(disease, symptom)
    
    # 1. Muestra las probabilidades a priori de cada enfermedad
    print("1. Probabilidades a priori:")
    # Itera sobre todas las enfermedades registradas
    for disease in brc.hypothesis_counts:
        # Muestra P(Enfermedad) con 3 decimales
        print(f"P({disease}) = {brc.prior_probability(disease):.3f}")
    
    # 2. Muestra las verosimilitudes P(Síntoma|Enfermedad)
    print("\n2. Verosimilitudes P(Síntoma|Enfermedad):")
    # Obtiene todos los síntomas únicos del conjunto de entrenamiento
    symptoms = set(sym for _, sym in training_data)
    # Itera sobre cada enfermedad
    for disease in brc.hypothesis_counts:
        # Muestra nombre de la enfermedad
        print(f"\n{disease}:")
        # Itera sobre cada síntoma
        for symptom in symptoms:
            # Muestra P(Síntoma|Enfermedad) con 3 decimales
            print(f"  P({symptom}|{disease}) = {brc.likelihood(symptom, disease):.3f}")
    
    # 3. Ejemplo de diagnóstico con solo fiebre
    print("\n3. Diagnóstico para paciente con fiebre:")
    # Itera sobre cada enfermedad
    for disease in brc.hypothesis_counts:
        # Calcula P(Enfermedad|fiebre)
        prob = brc.posterior_probability(disease, 'fiebre')
        # Muestra el resultado con 3 decimales
        print(f"P({disease}|fiebre) = {prob:.3f}")
    
    # 4. Diagnóstico con múltiples síntomas (congestión y tos)
    print("\n4. Diagnóstico para paciente con congestión y tos:")
    # Calcula probabilidades posteriores para ambas evidencias
    final_probs = brc.update_with_evidence(['congestión', 'tos'])
    # Itera sobre los resultados
    for disease, prob in final_probs.items():
        # Muestra cada probabilidad con 3 decimales
        print(f"P({disease}|evidencia) = {prob:.3f}")
    
    # 5. Caso de prueba completo con fiebre y tos
    print("\n5. Caso de prueba con fiebre y tos:")
    # Define los síntomas a evaluar
    test_symptoms = ['fiebre', 'tos']
    # Realiza el cálculo bayesiano
    diagnosis = brc.update_with_evidence(test_symptoms)
    
    # Muestra encabezado de resultados
    print("\nResultados del diagnóstico:")
    # Itera sobre cada enfermedad y su probabilidad
    for disease, prob in diagnosis.items():
        # Muestra la probabilidad en porcentaje con 1 decimal
        print(f"- {disease}: {prob*100:.1f}%")
    
    # Encuentra el diagnóstico más probable
    best_diagnosis = max(diagnosis.items(), key=lambda x: x[1])
    # Muestra el diagnóstico más probable con su porcentaje
    print(f"\nDiagnóstico más probable: {best_diagnosis[0]} ({best_diagnosis[1]*100:.1f}%)")