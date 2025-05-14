# -*- coding: utf-8 -*-
"""
Sistema Cognitivo Integrado que combina múltiples enfoques de IA
Created on [Fecha]
@author: [Tu nombre]
"""

import random                          # Para generación de números aleatorios
from collections import defaultdict    # Para diccionarios con valores por defecto
from abc import ABC, abstractmethod    # Para crear clases abstractas

# ==================== Clases Abstractas Base ====================
class Razonador(ABC):                  # Define la interfaz para razonamiento
    """Clase base abstracta para módulos de razonamiento"""
    @abstractmethod
    def inferir(self, estado):         # Método abstracto para realizar inferencias
        """Genera conclusiones basadas en el estado actual"""
        pass

class Aprendiz(ABC):                   # Define la interfaz para aprendizaje
    """Clase base abstracta para módulos de aprendizaje"""
    @abstractmethod 
    def aprender(self, experiencia):   # Método abstracto para aprendizaje
        """Actualiza el modelo con nueva experiencia"""
        pass

# ==================== Razonamiento Basado en Reglas ==================== 
class RazonamientoReglas(Razonador):    # Implementa razonamiento con reglas
    """Sistema experto basado en reglas lógicas"""
    def __init__(self, reglas):        # Constructor que recibe las reglas
        """
        Inicializa el sistema con reglas en formato:
        [(precondiciones, conclusión), ...]
        """
        self.reglas = reglas           # Almacena las reglas del sistema
        
    def inferir(self, estado):         # Implementación de inferencia
        """Aplica encadenamiento hacia adelante sobre el estado"""
        nuevas_conclusiones = set()    # Conjunto para nuevas conclusiones
        cambiado = True                # Bandera para controlar iteraciones
        
        while cambiado:                # Repite mientras haya cambios
            cambiado = False
            for precond, conclusion in self.reglas:  # Para cada regla
                if all(p in estado for p in precond) and conclusion not in estado:
                    estado.add(conclusion)          # Agrega conclusión
                    nuevas_conclusiones.add(conclusion)
                    cambiado = True                 # Marca cambio
                    
        return nuevas_conclusiones     # Devuelve nuevas conclusiones

# ==================== Razonamiento Probabilístico ====================
class RazonamientoProbabilistico(Razonador):  # Implementa razonamiento con incertidumbre
    """Sistema de inferencia probabilística simple"""
    def __init__(self, relaciones):    # Constructor que recibe relaciones
        """
        Inicializa con relaciones causales:
        {efecto: [(causa, probabilidad), ...]}
        """
        self.relaciones = relaciones   # Almacena las relaciones
        
    def inferir(self, estado):        # Implementación de inferencia
        """Calcula probabilidades de eventos no observados"""
        resultados = {}               # Diccionario para resultados
        
        for efecto, causas in self.relaciones.items():  # Para cada efecto
            if efecto not in estado:  # Solo si no está observado
                prob = 1.0            # Inicializa probabilidad
                for causa, prob_causal in causas:  # Para cada causa
                    if causa in estado:            # Si la causa existe
                        prob *= (1 - prob_causal)  # Actualiza probabilidad
                resultados[efecto] = 1 - prob      # Guarda probabilidad
                
        return resultados             # Devuelve probabilidades

# ==================== Aprendizaje por Refuerzo ==================== 
class AprendizRefuerzo(Aprendiz):     # Implementa Q-learning simplificado
    """Agente de aprendizaje por refuerzo"""
    def __init__(self, acciones, alpha=0.1, gamma=0.9):  # Constructor
        """
        Inicializa con:
        - acciones: lista de acciones posibles
        - alpha: tasa de aprendizaje
        - gamma: factor de descuento
        """
        self.q_table = defaultdict(float)  # Tabla Q: (estado, acción) -> valor
        self.acciones = acciones     # Almacena acciones posibles
        self.alpha = alpha          # Tasa de aprendizaje
        self.gamma = gamma          # Factor de descuento
        
    def elegir_accion(self, estado, epsilon=0.1):  # Política ε-greedy
        """Selecciona acción según política ε-greedy"""
        if random.random() < epsilon:  # Exploración: acción aleatoria
            return random.choice(self.acciones)
        else:                         # Explotación: mejor acción
            q_values = [self.q_table[(estado, a)] for a in self.acciones]
            max_q = max(q_values)     # Encuentra máximo valor Q
            return random.choice([a for i, a in enumerate(self.acciones) 
                                    if q_values[i] == max_q])
    
    def aprender(self, experiencia):  # Implementa Q-learning
        """Actualiza la Q-table con nueva experiencia"""
        estado, accion, recompensa, nuevo_estado = experiencia  # Desempaqueta
        
        max_q_nuevo = max([self.q_table[(nuevo_estado, a)]  # Máximo Q futuro
                         for a in self.acciones], default=0)
        
        # Actualización Q-learning
        self.q_table[(estado, accion)] += self.alpha * (
            recompensa + self.gamma * max_q_nuevo - self.q_table[(estado, accion)])

# ==================== Sistema Cognitivo Integrado ====================
class SistemaCognitivo:               # Sistema integrado completo
    """Arquitectura cognitiva que combina múltiples enfoques"""
    def __init__(self):               # Constructor
        # Inicializa módulos de razonamiento
        self.razonadores = {
            "reglas": RazonamientoReglas([          # Razonamiento basado en reglas
                ({"llueve", "noche"}, "carretera_mojada"),
                ({"carretera_mojada"}, "riesgo_accidente")
            ]),
            "probabilistico": RazonamientoProbabilistico({  # Razonamiento probabilístico
                "fallo_motor": [("temperatura_alta", 0.7), 
                               ("vibraciones_fuertes", 0.4)]
            })
        }
        
        # Inicializa módulos de aprendizaje
        self.aprendices = {
            "refuerzo": AprendizRefuerzo(["acelerar", "frenar", "girar"]),
            "supervisado": AprendizSupervisado()
        }
        
        self.memoria = set()          # Base de conocimiento
        self.historial = []           # Registro de experiencias
        
    def procesar_entrada(self, observaciones):  # Procesa nuevas observaciones
        """Integra nuevas observaciones y genera respuesta"""
        self.memoria.update(observaciones)      # Actualiza memoria
        
        # Aplica todos los razonadores
        for nombre, razonador in self.razonadores.items():
            resultados = razonador.inferir(self.memoria)
            
            if isinstance(resultados, dict):    # Para resultados probabilísticos
                for k, v in resultados.items():
                    if v > 0.7:                # Umbral de certeza
                        self.memoria.add(k)
            else:                              # Para otros resultados
                self.memoria.update(resultados)
        
        # Selecciona acción usando aprendizaje por refuerzo
        return self.aprendices["refuerzo"].elegir_accion(frozenset(self.memoria))
    
    def actualizar_modelos(self, experiencia):  # Actualiza con nueva experiencia
        """Aprende de la experiencia recibida"""
        self.historial.append(experiencia)     # Guarda en historial
        
        for aprendiz in self.aprendices.values():  # Actualiza todos los aprendices
            aprendiz.aprender(experiencia)
        
        if len(self.historial) % 100 == 0:     # Revisión periódica
            self._revisar_reglas()
    
    def _revisar_reglas(self):                 # Método interno
        """Ajusta reglas basado en experiencia acumulada"""
        patrones_frecuentes = set()
        
        # Detecta patrones frecuentes (ejemplo simplificado)
        if sum(1 for e in self.historial if "riesgo_accidente" in e[0]) > 20:
            patrones_frecuentes.add("nuevo_patron_riesgo")
        
        # Actualiza reglas si hay patrones nuevos
        if patrones_frecuentes:
            nuevas_reglas = list(self.razonadores["reglas"].reglas)
            nuevas_reglas.append(({"nuevo_patron_riesgo"}, "accion_preventiva"))
            self.razonadores["reglas"].reglas = nuevas_reglas

# ==================== Ejemplo de Uso ====================
if __name__ == "__main__":            # Punto de entrada principal
    print("=== Demostración Sistema Cognitivo ===")
    
    sistema = SistemaCognitivo()      # Crea instancia del sistema
    
    for i in range(50):               # Simula 50 iteraciones
        obs = set()                   # Genera observaciones aleatorias
        if random.random() > 0.7:
            obs.add("llueve")
        if random.random() > 0.8:
            obs.add("noche")
        if random.random() > 0.3:
            obs.add("temperatura_alta")
        
        accion = sistema.procesar_entrada(obs)  # Procesa observaciones
        
        # Recompensa basada en estado interno
        recompensa = 1 if "riesgo_accidente" not in sistema.memoria else -2
        
        # Crea experiencia y actualiza modelos
        experiencia = (frozenset(sistema.memoria), accion, 
                      recompensa, frozenset(obs))
        sistema.actualizar_modelos(experiencia)
        
        # Muestra progreso
        print(f"\nIteración {i+1}:")
        print(f"Observaciones: {obs}")
        print(f"Estado interno: {sistema.memoria}")
        print(f"Acción: {accion}")
        print(f"Recompensa: {recompensa}")
    
    # Muestra resultados finales
    print("\n=== Resultados Finales ===")
    print("Reglas aprendidas:", sistema.razonadores["reglas"].reglas)
    print("Muestra de Q-table:", 
          dict(list(sistema.aprendices["refuerzo"].q_table.items())[:3]))