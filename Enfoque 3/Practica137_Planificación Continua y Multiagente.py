import random
import threading
import time
from collections import defaultdict

class Agent:
    """Clase base para agentes inteligentes"""
    def __init__(self, agent_id, environment):
        self.id = agent_id  # Identificador único del agente
        self.environment = environment  # Referencia al entorno compartido
        self.local_view = {}  # Estado local percibido por el agente
        self.plan = []  # Plan actual del agente
        self.lock = threading.Lock()  # Sincronización para acceso concurrente

    def perceive(self):
        """Actualiza el estado local percibido desde el entorno"""
        with self.lock:
            self.local_view = self.environment.get_state(self.id)

    def planificar(self):
        """Genera un plan basado en el estado percibido"""
        # Implementación básica (sobrescribir en subclases)
        return []

    def ejecutar_accion(self, accion):
        """Ejecuta una acción en el entorno"""
        with self.lock:
            return self.environment.execute_action(self.id, accion)

    def run(self):
        """Ciclo principal del agente (percepción-planificación-ejecución)"""
        while not self.environment.tarea_completada():
            self.perceive()  # 1. Percibir entorno
            if not self.plan:
                self.plan = self.planificar()  # 2. Generar plan si no hay uno
            
            if self.plan:
                accion = self.plan.pop(0)  # 3. Tomar primera acción del plan
                resultado = self.ejecutar_accion(accion)  # 4. Ejecutar
                if not resultado:  # Si falla la ejecución
                    self.plan = []  # 5. Replanificar si es necesario

class Environment:
    """Entorno compartido donde interactúan los agentes"""
    def __init__(self):
        self.global_state = defaultdict(bool)  # Estado global del entorno
        self.agents = {}  # Diccionario de agentes registrados
        self.metas = set()  # Metas globales del sistema
        self.lock = threading.RLock()  # Lock reentrante para sincronización

    def register_agent(self, agent):
        """Registra un agente en el entorno"""
        with self.lock:
            self.agents[agent.id] = agent

    def get_state(self, agent_id):
        """Devuelve el estado relevante para un agente específico"""
        with self.lock:
            # En este ejemplo, todos ven el estado completo
            return dict(self.global_state)

    def execute_action(self, agent_id, accion):
        """Ejecuta una acción y actualiza el estado global"""
        with self.lock:
            print(f"Agente {agent_id} ejecutando {accion}")
            # Simular efecto de la acción con 80% de éxito
            if random.random() < 0.8:
                if accion.startswith("set_"):
                    prop = accion[4:]
                    self.global_state[prop] = True
                elif accion.startswith("unset_"):
                    prop = accion[6:]
                    self.global_state[prop] = False
                return True
            return False

    def tarea_completada(self):
        """Verifica si se han alcanzado todas las metas"""
        with self.lock:
            return all(self.global_state[meta] for meta in self.metas)

class CoordinatedPlanner:
    """Planificador para coordinación multiagente"""
    def __init__(self, environment):
        self.env = environment
        self.assignment = defaultdict(list)  # Asignación de tareas por agente

    def assign_tasks(self):
        """Asigna tareas a los agentes basado en el estado global"""
        with self.env.lock:
            unmet_goals = [g for g in self.env.metas if not self.env.global_state[g]]
            
            for goal in unmet_goals:
                # Asignación simple: round-robin entre agentes
                agent_id = random.choice(list(self.env.agents.keys()))
                action = f"set_{goal}"
                self.assignment[agent_id].append(action)

    def get_plan(self, agent_id):
        """Obtiene el plan asignado a un agente específico"""
        with self.env.lock:
            return self.assignment.get(agent_id, [])

class CoordinatedAgent(Agent):
    """Agente con capacidad de planificación coordinada"""
    def __init__(self, agent_id, environment, planner):
        super().__init__(agent_id, environment)
        self.planner = planner  # Referencia al planificador coordinado

    def planificar(self):
        """Planificación coordinada con otros agentes"""
        # Obtener plan asignado por el coordinador
        return self.planner.get_plan(self.id)

class ContinuousPlanner:
    """Planificación continua con ajuste dinámico"""
    def __init__(self, environment):
        self.env = environment
        self.last_plan_time = time.time()

    def continuous_planning(self):
        """Revisa y ajusta planes periódicamente"""
        while not self.env.tarea_completada():
            current_time = time.time()
            if current_time - self.last_plan_time > 2.0:  # Cada 2 segundos
                with self.env.lock:
                    self.adapt_plans()
                self.last_plan_time = current_time
            time.sleep(0.5)

    def adapt_plans(self):
        """Ajusta los planes basado en cambios en el entorno"""
        print("Replanificación continua activada...")
        # Lógica de adaptación (implementación específica del dominio)

class Simulation:
    """Simulación del sistema multiagente"""
    def __init__(self, num_agents=3):
        self.env = Environment()
        self.coordinator = CoordinatedPlanner(self.env)
        self.continuous_planner = ContinuousPlanner(self.env)
        
        # Configurar metas del sistema
        self.env.metas = {"meta1", "meta2", "meta3"}
        
        # Crear agentes
        self.agents = [
            CoordinatedAgent(i, self.env, self.coordinator) 
            for i in range(num_agents)
        ]
        
        # Registrar agentes en el entorno
        for agent in self.agents:
            self.env.register_agent(agent)

    def run(self, simulation_time=10):
        """Ejecuta la simulación"""
        print("Iniciando simulación multiagente...")
        
        # Hilo para planificación continua
        planning_thread = threading.Thread(
            target=self.continuous_planner.continuous_planning,
            daemon=True
        )
        planning_thread.start()
        
        # Hilos para cada agente
        agent_threads = []
        for agent in self.agents:
            t = threading.Thread(target=agent.run, daemon=True)
            t.start()
            agent_threads.append(t)
        
        # Hilo para coordinación periódica
        def coordination_loop():
            while not self.env.tarea_completada():
                self.coordinator.assign_tasks()
                time.sleep(1.5)
        
        coord_thread = threading.Thread(target=coordination_loop, daemon=True)
        coord_thread.start()
        
        # Esperar tiempo de simulación o hasta completar tareas
        start_time = time.time()
        while time.time() - start_time < simulation_time:
            if self.env.tarea_completada():
                print("¡Todas las metas alcanzadas!")
                break
            time.sleep(0.5)
        
        print("Simulación completada")

# Ejemplo de uso
if __name__ == "__main__":
    sim = Simulation(num_agents=3)
    sim.run(simulation_time=15)