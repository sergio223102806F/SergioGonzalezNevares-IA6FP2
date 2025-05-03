import random
from collections import defaultdict
from abc import ABC, abstractmethod

# ==================== Clases Abstractas Base ====================
class Razonador(ABC):
    """Clase abstracta para módulos de razonamiento"""
    @abstractmethod
    def inferir(self, estado):
        """Genera inferencias basadas en el estado actual"""
        pass

class Aprendiz(ABC):
    """Clase abstracta para módulos de aprendizaje"""
    @abstractmethod
    def aprender(self, experiencia):
        """Actualiza el modelo basado en nueva experiencia"""
        pass

# ==================== Razonamiento Basado en Reglas ====================
class RazonamientoReglas(Razonador):
    """Sistema experto basado en reglas lógicas"""
    def __init__(self, reglas):
        self.reglas = reglas  # Lista de tuplas (precondiciones, conclusion)
        
    def inferir(self, estado):
        """Encadenamiento hacia adelante"""
        nuevas_conclusiones = set()
        cambiado = True
        
        while cambiado:
            cambiado = False
            for precond, conclusion in self.reglas:
                if all(p in estado for p in precond) and conclusion not in estado:
                    estado.add(conclusion)
                    nuevas_conclusiones.add(conclusion)
                    cambiado = True
                    
        return nuevas_conclusiones

# ==================== Razonamiento Probabilístico ====================
class RazonamientoProbabilistico(Razonador):
    """Inferencia con incertidumbre usando redes bayesianas simples"""
    def __init__(self, relaciones):
        """
        relaciones: dict {efecto: [(causa, probabilidad), ...]}
        """
        self.relaciones = relaciones
        
    def inferir(self, estado):
        """Calcula probabilidades de eventos no observados"""
        resultados = {}
        
        for efecto, causas in self.relaciones.items():
            if efecto not in estado:
                prob = 1.0
                for causa, prob_causal in causas:
                    if causa in estado:
                        prob *= (1 - prob_causal)
                resultados[efecto] = 1 - prob
                
        return resultados

# ==================== Aprendizaje por Refuerzo ====================
class AprendizRefuerzo(Aprendiz):
    """Aprendizaje basado en recompensas (Q-learning simplificado)"""
    def __init__(self, acciones, alpha=0.1, gamma=0.9):
        self.q_table = defaultdict(float)  # Tabla Q: (estado, acción) -> valor
        self.acciones = acciones
        self.alpha = alpha  # Tasa de aprendizaje
        self.gamma = gamma  # Factor de descuento
        
    def elegir_accion(self, estado, epsilon=0.1):
        """Epsilon-greedy: exploración vs explotación"""
        if random.random() < epsilon:
            return random.choice(self.acciones)
        else:
            q_values = [self.q_table[(estado, a)] for a in self.acciones]
            max_q = max(q_values)
            return random.choice([a for i, a in enumerate(self.acciones) if q_values[i] == max_q])
    
    def aprender(self, experiencia):
        """Actualiza Q-table usando (s, a, r, s')"""
        estado, accion, recompensa, nuevo_estado = experiencia
        
        # Máximo valor Q para el nuevo estado
        max_q_nuevo = max([self.q_table[(nuevo_estado, a)] for a in self.acciones], default=0)
        
        # Fórmula Q-learning
        self.q_table[(estado, accion)] += self.alpha * (
            recompensa + self.gamma * max_q_nuevo - self.q_table[(estado, accion)]
        )

# ==================== Aprendizaje Supervisado (Simplificado) ====================
class AprendizSupervisado(Aprendiz):
    """Clasificador basado en reglas de decisión (simplificado)"""
    def __init__(self):
        self.modelo = None
        self.caracteristicas = []
        
    def entrenar(self, X, y):
        """Entrenamiento con datos etiquetados (simplificado)"""
        # En una implementación real usaríamos scikit-learn, TensorFlow, etc.
        self.caracteristicas = list(X[0].keys()) if X else []
        self.modelo = {"reglas": []}  # Modelo ficticio
        
    def predecir(self, muestra):
        """Predicción basada en el modelo (simplificado)"""
        return random.choice([True, False]) if self.modelo else None
    
    def aprender(self, experiencia):
        """Actualización online del modelo"""
        X, y = experiencia
        if not self.modelo:
            self.entrenar([X], [y])
        # Lógica de actualización incremental iría aquí

# ==================== Sistema Integrado ====================
class SistemaCognitivo:
    """Arquitectura que integra razonamiento y aprendizaje"""
    def __init__(self):
        # Inicializar módulos
        self.razonadores = {
            "reglas": RazonamientoReglas([
                ({"llueve", "noche"}, "carretera_mojada"),
                ({"carretera_mojada"}, "riesgo_accidente")
            ]),
            "probabilistico": RazonamientoProbabilistico({
                "fallo_motor": [("temperatura_alta", 0.7), ("vibraciones_fuertes", 0.4)]
            })
        }
        
        self.aprendices = {
            "refuerzo": AprendizRefuerzo(["acelerar", "frenar", "girar"]),
            "supervisado": AprendizSupervisado()
        }
        
        self.memoria = set()  # Estado actual del conocimiento
        self.historial = []    # Registro de experiencias
        
    def procesar_entrada(self, observaciones):
        """Procesa nuevas observaciones a través de todos los módulos"""
        # 1. Actualizar estado con observaciones directas
        self.memoria.update(observaciones)
        
        # 2. Aplicar razonadores
        for nombre, razonador in self.razonadores.items():
            resultados = razonador.inferir(self.memoria)
            if isinstance(resultados, dict):  # Para resultados probabilísticos
                for k, v in resultados.items():
                    if v > 0.7:  # Umbral de certeza
                        self.memoria.add(k)
            else:
                self.memoria.update(resultados)
        
        # 3. Tomar decisión basada en aprendizaje
        accion = self.aprendices["refuerzo"].elegir_accion(frozenset(self.memoria))
        
        return accion
    
    def actualizar_modelos(self, experiencia):
        """Actualiza los modelos de aprendizaje con nueva experiencia"""
        # 1. Almacenar en historial
        self.historial.append(experiencia)
        
        # 2. Actualizar aprendices
        for aprendiz in self.aprendices.values():
            aprendiz.aprender(experiencia)
        
        # 3. Revisar reglas basadas en patrones históricos
        if len(self.historial) % 100 == 0:  # Cada 100 experiencias
            self._revisar_reglas()
    
    def _revisar_reglas(self):
        """Ajusta reglas basado en experiencia acumulada (simplificado)"""
        # En un sistema real se usaría minería de datos o análisis estadístico
        patrones_frecuentes = set()
        
        # Lógica ficticia para detectar patrones
        if sum(1 for e in self.historial if "riesgo_accidente" in e[0]) > 20:
            patrones_frecuentes.add("nuevo_patron_riesgo")
        
        # Actualizar razonador de reglas
        if patrones_frecuentes:
            nuevas_reglas = list(self.razonadores["reglas"].reglas)
            nuevas_reglas.append(({"nuevo_patron_riesgo"}, "accion_preventiva"))
            self.razonadores["reglas"].reglas = nuevas_reglas

# ==================== Ejemplo de Uso ====================
if __name__ == "__main__":
    print("=== Demostración Sistema Integrado ===")
    
    # 1. Inicializar sistema cognitivo
    sistema = SistemaCognitivo()
    
    # 2. Simular ciclo de percepción-acción-aprendizaje
    for i in range(50):  # 50 iteraciones de simulación
        # Observaciones del entorno (simuladas)
        obs = set()
        if random.random() > 0.7:
            obs.add("llueve")
        if random.random() > 0.8:
            obs.add("noche")
        if random.random() > 0.3:
            obs.add("temperatura_alta")
        
        # Procesamiento cognitivo
        accion = sistema.procesar_entrada(obs)
        
        # Simular resultado/recompensa (simplificado)
        recompensa = 1 if "riesgo_accidente" not in sistema.memoria else -2
        
        # Actualización del aprendizaje
        experiencia = (frozenset(sistema.memoria), accion, recompensa, frozenset(obs))
        sistema.actualizar_modelos(experiencia)
        
        # Mostrar estado
        print(f"\nIteración {i+1}:")
        print(f"Observaciones: {obs}")
        print(f"Estado interno: {sistema.memoria}")
        print(f"Acción elegida: {accion}")
        print(f"Recompensa: {recompensa}")
    
    print("\nResultados finales:")
    print(f"Reglas aprendidas: {sistema.razonadores['reglas'].reglas}")
    print(f"Q-table muestra: {dict(list(sistema.aprendices['refuerzo'].q_table.items())[:3])}")