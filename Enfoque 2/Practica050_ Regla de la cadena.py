from collections import defaultdict  # Importa defaultdict para diccionarios con valores por defecto

class ChainRuleProbability:
    def __init__(self):
        """Inicializa contadores para probabilidades conjuntas y condicionales"""
        # Diccionario que cuenta ocurrencias conjuntas de eventos (X₁, X₂, ..., Xₙ)
        # Ejemplo: {('alta', 'alta', 'sí'): 2}
        self.joint_counts = defaultdict(int)  

        # Diccionario anidado que cuenta ocurrencias condicionales P(Xₖ|X₁, ..., Xₖ₋₁)
        # Ejemplo: {('alta',): {'alta': 3, 'baja': 1}}
        self.conditional_counts = defaultdict(lambda: defaultdict(int))  

        # Contador total de observaciones registradas
        self.total_observations = 0  

    def add_observation(self, *events):
        """
        Registra una observación de eventos dependientes.
        
        Args:
            *events: Secuencia de eventos en orden (X₁, X₂, ..., Xₙ)
        """
        # 1. Actualiza conteo conjunto (como tupla)
        self.joint_counts[events] += 1
        
        # 2. Actualiza conteos condicionales para cada P(Xₖ|X₁, ..., Xₖ₋₁)
        for i in range(1, len(events)):
            condition = events[:i]  # Condición: eventos anteriores (X₁, ..., Xₖ₋₁)
            event = events[i]       # Evento actual (Xₖ)
            self.conditional_counts[condition][event] += 1
        
        # 3. Incrementa el total de observaciones
        self.total_observations += 1

    def joint_probability(self, *events) -> float:
        """
        Calcula P(X₁, X₂, ..., Xₙ) usando la Regla de la Cadena.
        
        Args:
            *events: Secuencia de eventos (X₁, X₂, ..., Xₙ)
            
        Returns:
            float: Probabilidad conjunta estimada (0 si no hay datos)
        """
        # Caso especial: sin observaciones registradas
        if self.total_observations == 0:
            return 0.0  

        # Paso 1: Calcula P(X₁) = count(X₁) / total_observations
        prob = self.joint_counts[(events[0],)] / self.total_observations
        
        # Paso 2: Aplica regla de la cadena para P(Xₖ|X₁, ..., Xₖ₋₁)
        for i in range(1, len(events)):
            condition = events[:i]  # Condición (eventos anteriores)
            event = events[i]       # Evento actual
            
            # Si no hay datos para esta condición, probabilidad = 0
            if sum(self.conditional_counts[condition].values()) == 0:
                return 0.0
            
            # Multiplica por P(Xₖ|X₁, ..., Xₖ₋₁) = count(Xₖ|condición) / total(condición)
            prob *= (self.conditional_counts[condition][event] / 
                    sum(self.conditional_counts[condition].values()))
        
        return prob

# Ejemplo de uso: Pronóstico del clima
if __name__ == "__main__":
    print("=== Ejemplo de Regla de la Cadena: Pronóstico del Clima ===")
    cr = ChainRuleProbability()  # Crea una instancia del calculador
    
    # Dataset histórico: cada tupla es (Temperatura, Humedad, Lluvia)
    datos_clima = [
        ("alta", "alta", "sí"),  # Observación 1
        ("alta", "baja", "no"),  # Observación 2
        ("baja", "alta", "sí"),  # Observación 3
        ("baja", "baja", "no"),  # Observación 4
        ("alta", "alta", "sí"),  # Observación 5 (repite primera condición)
        ("baja", "alta", "sí"),  # Observación 6
    ]
    
    # Procesa cada observación del dataset
    for temp, humedad, lluvia in datos_clima:
        cr.add_observation(temp, humedad, lluvia)
    
    # Calcula P(Temperatura=alta, Humedad=alta, Lluvia=sí)
    probabilidad = cr.joint_probability("alta", "alta", "sí")
    
    # Muestra resultados (formateado a 2 decimales)
    print(f"\nProbabilidad conjunta estimada:")
    print(f"P(Temperatura=alta, Humedad=alta, Lluvia=sí) = {probabilidad:.2f}")