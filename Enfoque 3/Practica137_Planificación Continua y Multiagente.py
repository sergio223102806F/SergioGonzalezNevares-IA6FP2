import random
import threading
import time
from collections import defaultdict

class Agent:
    """Clase base para agentes inteligentes"""
    def __init__(self, agent_id, environment):  # Inicializa el agente con un ID y el entorno
        self.id = agent_id  # Identificador único del agente
        self.environment = environment  # Referencia al entorno compartido
        self.local_view = {}  # Estado local percibido por el agente
        self.plan = []  # Plan actual del agente (lista de acciones)
        self.lock = threading.Lock()  # Sincronización para acceso concurrente a los atributos del agente

    def perceive(self):  # Actualiza el estado local percibido desde el entorno
        """Actualiza el estado local percibido desde el entorno"""
        with self.lock:  # Adquiere el lock para acceder de forma segura al entorno
            self.local_view = self.environment.get_state(self.id)  # Obtiene el estado del entorno relevante para este agente

    def planificar(self):  # Genera un plan basado en el estado percibido
        """Genera un plan basado en el estado percibido"""
        # Implementación básica (sobrescribir en subclases para lógica de planificación específica)
        return []

    def ejecutar_accion(self, accion):  # Ejecuta una acción en el entorno
        """Ejecuta una acción en el entorno"""
        with self.lock:  # Adquiere el lock para interactuar de forma segura con el entorno
            return self.environment.execute_action(self.id, accion)  # Llama a la función del entorno para ejecutar la acción

    def run(self):  # Ciclo principal del agente (percepción-planificación-ejecución)
        """Ciclo principal del agente (percepción-planificación-ejecución)"""
        while not self.environment.tarea_completada():  # Continúa hasta que la tarea global esté completada
            self.perceive()  # 1. Percibir el entorno para actualizar la vista local
            if not self.plan:  # Si el agente no tiene un plan actual
                self.plan = self.planificar()  # 2. Generar un nuevo plan basado en la percepción actual

            if self.plan:  # Si el agente tiene un plan
                accion = self.plan.pop(0)  # 3. Tomar la primera acción del plan
                resultado = self.ejecutar_accion(accion)  # 4. Ejecutar la acción en el entorno
                if not resultado:  # Si la ejecución de la acción falló
                    self.plan = []  # 5. Replanificar si la acción no tuvo éxito

class Environment:
    """Entorno compartido donde interactúan los agentes"""
    def __init__(self):  # Inicializa el entorno con estado global, agentes, metas y un lock
        self.global_state = defaultdict(bool)  # Estado global del entorno (diccionario con valores booleanos por defecto False)
        self.agents = {}  # Diccionario para almacenar los agentes registrados en el entorno (ID -> Agente)
        self.metas = set()  # Conjunto de metas globales que el sistema debe alcanzar
        self.lock = threading.RLock()  # Lock reentrante para permitir que el mismo hilo adquiera el lock varias veces

    def register_agent(self, agent):  # Registra un agente en el entorno
        """Registra un agente en el entorno"""
        with self.lock:  # Adquiere el lock para modificar de forma segura la lista de agentes
            self.agents[agent.id] = agent  # Añade el agente al diccionario usando su ID

    def get_state(self, agent_id):  # Devuelve el estado relevante para un agente específico
        """Devuelve el estado relevante para un agente específico"""
        with self.lock:  # Adquiere el lock para acceder de forma segura al estado global
            # En este ejemplo, todos los agentes tienen una visión completa del estado global
            return dict(self.global_state)  # Retorna una copia del estado global

    def execute_action(self, agent_id, accion):  # Ejecuta una acción y actualiza el estado global
        """Ejecuta una acción y actualiza el estado global"""
        with self.lock:  # Adquiere el lock para modificar de forma segura el estado global
            print(f"Agente {agent_id} ejecutando {accion}")  # Imprime qué agente está ejecutando qué acción
            # Simular el efecto de la acción con un 80% de probabilidad de éxito
            if random.random() < 0.8:
                if accion.startswith("set_"):  # Si la acción comienza con "set_", establece una propiedad a True
                    prop = accion[4:]  # Extrae el nombre de la propiedad
                    self.global_state[prop] = True  # Establece la propiedad en el estado global a True
                elif accion.startswith("unset_"):  # Si la acción comienza con "unset_", establece una propiedad a False
                    prop = accion[6:]  # Extrae el nombre de la propiedad
                    self.global_state[prop] = False  # Establece la propiedad en el estado global a False
                return True  # Indica que la acción fue exitosa
            return False  # Indica que la acción falló

    def tarea_completada(self):  # Verifica si se han alcanzado todas las metas
        """Verifica si se han alcanzado todas las metas"""
        with self.lock:  # Adquiere el lock para acceder de forma segura al estado global y a las metas
            return all(self.global_state[meta] for meta in self.metas)  # Retorna True si todas las metas están en el estado global como True

class CoordinatedPlanner:
    """Planificador para coordinación multiagente"""
    def __init__(self, environment):  # Inicializa el planificador coordinado con el entorno
        self.env = environment
        self.assignment = defaultdict(list)  # Asignación de tareas por agente (agente_id -> lista de acciones)

    def assign_tasks(self):  # Asigna tareas a los agentes basado en el estado global
        """Asigna tareas a los agentes basado en el estado global"""
        with self.env.lock:  # Adquiere el lock para acceder de forma segura al estado global y a los agentes
            unmet_goals = [g for g in self.env.metas if not self.env.global_state[g]]  # Lista de metas que aún no se han alcanzado

            for goal in unmet_goals:  # Itera sobre cada meta no alcanzada
                # Asignación simple: elige un agente al azar para intentar alcanzar la meta
                agent_id = random.choice(list(self.env.agents.keys()))
                action = f"set_{goal}"  # Crea una acción para establecer la meta como verdadera
                self.assignment[agent_id].append(action)  # Asigna esta acción al plan del agente

    def get_plan(self, agent_id):  # Obtiene el plan asignado a un agente específico
        """Obtiene el plan asignado a un agente específico"""
        with self.env.lock:  # Adquiere el lock para acceder de forma segura a la asignación de tareas
            return self.assignment.get(agent_id, [])  # Retorna la lista de acciones asignada al agente, o una lista vacía si no hay asignación

class CoordinatedAgent(Agent):
    """Agente con capacidad de planificación coordinada"""
    def __init__(self, agent_id, environment, planner):  # Inicializa el agente coordinado con ID, entorno y planificador
        super().__init__(agent_id, environment)  # Llama al constructor de la clase padre (Agent)
        self.planner = planner  # Referencia al planificador coordinado que asigna tareas a este agente

    def planificar(self):  # Planificación coordinada con otros agentes
        """Planificación coordinada con otros agentes"""
        # Obtener el plan asignado por el coordinador
        return self.planner.get_plan(self.id)  # Retorna el plan (lista de acciones) que el planificador coordinado ha asignado a este agente

class ContinuousPlanner:
    """Planificación continua con ajuste dinámico"""
    def __init__(self, environment):  # Inicializa el planificador continuo con el entorno
        self.env = environment
        self.last_plan_time = time.time()  # Guarda el tiempo de la última replanificación

    def continuous_planning(self):  # Revisa y ajusta los planes periódicamente
        """Revisa y ajusta los planes periódicamente"""
        while not self.env.tarea_completada():  # Continúa hasta que la tarea global esté completada
            current_time = time.time()  # Obtiene el tiempo actual
            if current_time - self.last_plan_time > 2.0:  # Si han pasado más de 2 segundos desde la última replanificación
                with self.env.lock:  # Adquiere el lock del entorno para acceder de forma segura a los agentes y al estado
                    self.adapt_plans()  # Llama a la función para adaptar los planes
                self.last_plan_time = current_time  # Actualiza el tiempo de la última replanificación
            time.sleep(0.5)  # Espera un breve periodo antes de la siguiente revisión

    def adapt_plans(self):  # Ajusta los planes basado en cambios en el entorno
        """Ajusta los planes basado en cambios en el entorno"""
        print("Replanificación continua activada...")
        # Lógica de adaptación (aquí se podría implementar una lógica más sofisticada para reasignar tareas o modificar los planes de los agentes según el estado actual del entorno)
        # En este ejemplo, la adaptación es simplemente una impresión en pantalla.

class Simulation:
    """Simulación del sistema multiagente"""
    def __init__(self, num_agents=3):  # Inicializa la simulación con un número de agentes
        self.env = Environment()  # Crea el entorno compartido
        self.coordinator = CoordinatedPlanner(self.env)  # Crea el planificador coordinado
        self.continuous_planner = ContinuousPlanner(self.env)  # Crea el planificador continuo

        # Configurar las metas del sistema
        self.env.metas = {"meta1", "meta2", "meta3"}

        # Crear los agentes coordinados y registrarlos en el entorno
        self.agents = [
            CoordinatedAgent(i, self.env, self.coordinator)
            for i in range(num_agents)
        ]
        for agent in self.agents:
            self.env.register_agent(agent)

    def run(self, simulation_time=10):  # Ejecuta la simulación durante un tiempo determinado
        """Ejecuta la simulación"""
        print("Iniciando simulación multiagente...")

        # Hilo para la planificación continua (se ejecuta en segundo plano)
        planning_thread = threading.Thread(
            target=self.continuous_planner.continuous_planning,
            daemon=True  # El hilo se detendrá cuando el programa principal termine
        )
        planning_thread.start()

        # Hilos para cada agente (cada agente se ejecuta en su propio hilo)
        agent_threads = []
        for agent in self.agents:
            t = threading.Thread(target=agent.run, daemon=True)
            t.start()
            agent_threads.append(t)

        # Hilo para la coordinación periódica de tareas entre agentes
        def coordination_loop():
            while not self.env.tarea_completada():
                self.coordinator.assign_tasks()
                time.sleep(1.5)  # Coordina las tareas cada 1.5 segundos

        coord_thread = threading.Thread(target=coordination_loop, daemon=True)
        coord_thread.start()

        # Esperar el tiempo de simulación o hasta que todas las tareas estén completadas
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