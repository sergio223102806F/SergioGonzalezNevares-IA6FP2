from collections import defaultdict

class ChainRuleProbability:
    def __init__(self):
        """Inicializa contadores para probabilidades conjuntas y condicionales"""
        self.joint_counts = defaultdict(int)  # Conteo de eventos conjuntos (X₁, X₂, ..., Xₙ)
        self.conditional_counts = defaultdict(lambda: defaultdict(int))  # Conteo de eventos condicionales
        self.total_observations = 0  # Total de observaciones registradas

    def add_observation(self, *events):
        """
        Registra una observación de eventos dependientes.
        
        Args:
            *events: Secuencia de eventos en orden (X₁, X₂, ..., Xₙ)
        """
        # Guarda conteo conjunto
        self.joint_counts[events] += 1
        
        # Guarda conteos condicionales (P(Xₖ|X₁, ..., Xₖ₋₁))
        for i in range(1, len(events)):
            condition = events[:i]  # Condición (X₁, ..., Xₖ₋₁)
            event = events[i]       # Evento (Xₖ)
            self.conditional_counts[condition][event] += 1
        
        self.total_observations += 1

    def joint_probability(self, *events) -> float:
        """
        Calcula P(X₁, X₂, ..., Xₙ) usando la Regla de la Cadena.
        
        Args:
            *events: Secuencia de eventos (X₁, X₂, ..., Xₙ)
            
        Returns:
            float: Probabilidad conjunta estimada
        """
        if self.total_observations == 0:
            return 0.0  # Evita división por cero
        
        # Inicia con P(X₁)
        prob = self.joint_counts[(events[0],)] / self.total_observations
        
        # Aplica regla de la cadena: P(Xₖ|X₁, ..., Xₖ₋₁)
        for i in range(1, len(events)):
            condition = events[:i]
            event = events[i]
            
            # Si no hay datos para la condición, retorna 0
            if sum(self.conditional_counts[condition].values()) == 0:
                return 0.0
            
            # Multiplica por P(Xₖ|X₁, ..., Xₖ₋₁)
            prob *= (self.conditional_counts[condition][event] / 
                    sum(self.conditional_counts[condition].values()))
        
        return prob

# Ejemplo de uso: Pronóstico del clima
if __name__ == "__main__":
    print("=== Ejemplo de Regla de la Cadena: Pronóstico del Clima ===")
    cr = ChainRuleProbability()
    
    # Datos históricos: (Temperatura, Humedad, Lluvia)
    datos_clima = [
        ("alta", "alta", "sí"),
        ("alta", "baja", "no"),
        ("baja", "alta", "sí"),
        ("baja", "baja", "no"),
        ("alta", "alta", "sí"),
        ("baja", "alta", "sí"),
    ]
    
    # Registrar observaciones
    for temp, humedad, lluvia in datos_clima:
        cr.add_observation(temp, humedad, lluvia)
    
    # Calcular P(Temperatura=alta, Humedad=alta, Lluvia=sí)
    probabilidad = cr.joint_probability("alta", "alta", "sí")
    
    print(f"\nProbabilidad conjunta estimada:")
    print(f"P(Temperatura=alta, Humedad=alta, Lluvia=sí) = {probabilidad:.2f}")
