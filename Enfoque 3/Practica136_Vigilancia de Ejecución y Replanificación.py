# Importación de bibliotecas necesarias
from collections import deque  # Para estructuras de datos FIFO (útil en búsqueda de grafos)
import random  # Para simular aleatoriedad en la ejecución de acciones
import pycosat  # Solver SAT para la planificación lógica (instalar con: pip install pycosat)

# ==================== SATPLAN (Planificación Proposicional) ====================
class SATPLAN:
    """Planificador basado en satisfacibilidad booleana (SAT)"""
    def __init__(self, acciones, estado_inicial, metas, max_pasos=10):
        # Inicialización del planificador SAT
        self.acciones = acciones  # Lista de acciones disponibles
        self.estado_inicial = estado_inicial  # Estado inicial del mundo
        self.metas = metas  # Metas a alcanzar
        self.max_pasos = max_pasos  # Límite de pasos temporales
        self.prop_a_var = {}  # Diccionario para mapear proposiciones a variables SAT
        self.var_counter = 1  # Contador de variables proposicionales

    def _generar_variable(self, nombre):
        """Asigna una variable única a una proposición/acción"""
        if nombre not in self.prop_a_var:  # Si la variable no existe
            self.prop_a_var[nombre] = self.var_counter  # Crea nueva variable
            self.var_counter += 1  # Incrementa el contador
        return self.prop_a_var[nombre]  # Retorna el ID de la variable

    def planificar(self):
        """Genera y resuelve el problema SAT"""
        clausulas = []  # Lista para almacenar las cláusulas SAT
        
        # 1. Codificación del estado inicial (todas verdaderas en tiempo 0)
        for prop in self.estado_inicial:
            var = self._generar_variable(f"{prop}_0")  # Ej: "en_A_0"
            clausulas.append([var])  # Añade cláusula unitaria positiva
            
        # 2. Codificación de metas (deben ser verdaderas al final)
        for meta in self.metas:
            var = self._generar_variable(f"{meta}_{self.max_pasos}")  # Ej: "en_C_10"
            clausulas.append([var])  # Cláusula unitaria positiva
            
        # 3. Codificación de acciones y efectos
        for paso in range(self.max_pasos):  # Para cada paso temporal
            for accion in self.acciones:  # Para cada acción
                var_accion = self._generar_variable(f"{accion['nombre']}_{paso}")  # Ej: "mover_A_B_2"
                
                # Precondiciones: Si la acción ocurre, sus precondiciones deben ser verdaderas
                for precond in accion['precondiciones']:
                    var_precond = self._generar_variable(f"{precond}_{paso}")
                    clausulas.append([-var_accion, var_precond])  # ¬acción ∨ precondición
                
                # Efectos: Si la acción ocurre, sus efectos deben cumplirse
                for efecto in accion['efectos']:
                    var_efecto = self._generar_variable(f"{efecto}_{paso+1}")
                    clausulas.append([-var_accion, var_efecto])  # ¬acción ∨ efecto
        
        # 4. Resolución con PycoSAT
        solucion = pycosat.solve(clausulas)  # Llama al solver SAT
        
        if solucion == "UNSAT":  # Si no hay solución
            return None
            
        # 5. Extracción del plan desde la solución SAT
        plan = []
        for paso in range(self.max_pasos):
            for accion in self.acciones:
                var_accion = self.prop_a_var.get(f"{accion['nombre']}_{paso}")
                if var_accion and var_accion in solucion:  # Si la acción está en la solución
                    plan.append(accion['nombre'])  # Añade al plan
                    break
                    
        return plan  # Retorna la secuencia de acciones

# ==================== HTNPlanner (Redes Jerárquicas) ====================
class HTNPlanner:
    """Planificador de Redes Jerárquicas de Tareas"""
    def __init__(self, dominio):
        self.dominio = dominio  # Dominio con acciones y métodos
        
    def planificar(self, estado_inicial, tarea_principal):
        """Planificación HTN con descomposición de tareas"""
        # Usa DFS para explorar posibles descomposiciones
        stack = [([tarea_principal], set(estado_inicial), [])]  # (tareas_pendientes, estado, plan_parcial)
        
        while stack:
            tareas, estado, plan = stack.pop()  # LIFO para DFS
            
            if not tareas:  # Si no hay tareas pendientes
                return plan  # ¡Plan completado!
                
            tarea = tareas[0]  # Tarea actual
            
            # Caso 1: Es una acción primitiva
            if tarea in self.dominio['acciones']:
                accion = self.dominio['acciones'][tarea]
                # Verifica precondiciones
                if not accion['precondiciones'].issubset(estado):
                    continue  # Backtrack si no se cumplen
                    
                # Aplica efectos
                nuevo_estado = set(estado)
                for efecto in accion['efectos']:
                    if efecto.startswith('-'):
                        nuevo_estado.discard(efecto[1:])  # Elimina efecto negativo
                    else:
                        nuevo_estado.add(efecto)  # Añade efecto positivo
                
                # Continúa con las tareas restantes
                stack.append((tareas[1:], nuevo_estado, plan + [tarea]))
            
            # Caso 2: Es una tarea abstracta
            elif tarea in self.dominio['metodos']:
                # Prueba todos los métodos de descomposición
                for metodo in self.dominio['metodos'][tarea]:
                    if metodo['precondiciones'].issubset(estado):  # Verifica precondiciones
                        # Reemplaza tarea abstracta por subtareas
                        nuevas_tareas = metodo['subtasks'] + tareas[1:]
                        stack.append((nuevas_tareas, estado, plan))
        
        return None  # No se encontró plan

# ==================== ConditionalPlanner (Planificación Condicional) ====================
class ConditionalPlanner:
    """Planificación condicional con observaciones"""
    def __init__(self, dominio):
        self.dominio = dominio
        
    def planificar(self, estado_inicial, metas):
        """Genera un plan condicional con ramas"""
        return self._construir_plan(set(estado_inicial), set(metas), set(), 10)
        
    def _construir_plan(self, estado, metas, historial, profundidad):
        if profundidad <= 0:  # Límite de recursión
            return None
            
        if metas.issubset(estado):  # Metas ya cumplidas
            return {'accion': None, 'ramas': {}}
            
        # Prueba cada acción posible
        for accion_nombre, accion in self.dominio['acciones'].items():
            if not accion['precondiciones'].issubset(estado):
                continue  # Salta si no se cumplen precondiciones
                
            plan = {'accion': accion_nombre, 'ramas': {}}  # Nodo del plan
            exito = True
            
            # Considera todos los posibles efectos (con incertidumbre)
            for efecto_info in accion['efectos_posibles']:
                nuevo_estado = set(estado)
                # Aplica efectos
                for efecto in efecto_info['efectos']:
                    if efecto.startswith('-'):
                        nuevo_estado.discard(efecto[1:])
                    else:
                        nuevo_estado.add(efecto)
                
                # Genera posibles observaciones post-acción
                for obs in self._generar_observaciones(nuevo_estado):
                    situacion = (accion_nombre, frozenset(nuevo_estado), obs)
                    if situacion in historial:
                        continue  # Evita ciclos
                        
                    nuevo_historial = set(historial)
                    nuevo_historial.add(situacion)
                    
                    # Construye subplan recursivamente
                    subplan = self._construir_plan(nuevo_estado, metas, nuevo_historial, profundidad-1)
                    if not subplan:
                        exito = False
                        break
                        
                    plan['ramas'][obs] = subplan  # Añade rama condicional
                
                if not exito:
                    break
                    
            if exito:
                return plan  # Retorna plan completo
                
        return None  # No se encontró plan

# ==================== MonitorReplanner (Vigilancia y Replanificación) ====================
class MonitorReplanner:
    """Sistema integrado de vigilancia y replanificación"""
    def __init__(self, dominio, planner_class):
        self.dominio = dominio  # Dominio de planificación
        self.PlannerClass = planner_class  # Clase del planificador base (SATPLAN, HTN, etc.)
        self.plan_actual = None  # Plan actual en ejecución
        self.estado_actual = None  # Estado actual del mundo
        
    def ejecutar_y_monitorear(self, estado_inicial, metas, max_intentos=3):
        """Ciclo principal de ejecución-monitoreo-replanificación"""
        self.estado_actual = set(estado_inicial)
        intentos = 0
        
        while intentos < max_intentos:
            intentos += 1
            
            # 1. Fase de planificación
            planner = self.PlannerClass(self.dominio)
            self.plan_actual = planner.planificar(self.estado_actual, metas)
            
            if not self.plan_actual:
                return False, []  # Falla si no hay plan
                
            # 2. Fase de ejecución
            exito, acciones = self._ejecutar_plan()
            
            if exito:
                return True, acciones  # Éxito si se alcanzan metas
                
        return False, []  # Falla si se agotan intentos
        
    def _ejecutar_plan(self):
        """Ejecuta el plan actual con monitoreo"""
        acciones_ejecutadas = []
        
        for accion in self.plan_actual:
            # Simula ejecución con posible fallo (10% de probabilidad)
            exito, nuevo_estado = self._simular_ejecucion(accion)
            
            if not exito:
                return False, acciones_ejecutadas  # Falla ejecución
                
            self.estado_actual = nuevo_estado
            acciones_ejecutadas.append(accion)
            
            if self._metas_cumplidas():
                return True, acciones_ejecutadas  # Éxito
                
        return self._metas_cumplidas(), acciones_ejecutadas
        
    def _simular_ejecucion(self, accion):
        """Simula la ejecución de una acción con posibles fallos"""
        if random.random() > 0.9:  # 10% de probabilidad de fallo
            return False, self.estado_actual
            
        nuevo_estado = set(self.estado_actual)
        for efecto in self.dominio['acciones'][accion]['efectos']:
            if efecto.startswith('-'):
                nuevo_estado.discard(efecto[1:])  # Elimina efecto negativo
            else:
                nuevo_estado.add(efecto)  # Añade efecto positivo
                
        return True, nuevo_estado
        
    def _metas_cumplidas(self):
        """Verifica si se cumplieron todas las metas"""
        return all(meta in self.estado_actual for meta in self.dominio['metas'])

# ==================== Ejemplo de Uso Integrado ====================
if __name__ == "__main__":
    # Configuración del dominio compartido
    dominio_compartido = {
        'acciones': {
            'mover_A_B': {
                'precondiciones': {'en_A'},
                'efectos': {'en_B', '-en_A'},
                'efectos_posibles': [{'probabilidad': 1.0, 'efectos': ['en_B', '-en_A']}]
            },
            'mover_B_C': {
                'precondiciones': {'en_B'},
                'efectos': {'en_C', '-en_B'},
                'efectos_posibles': [{'probabilidad': 1.0, 'efectos': ['en_C', '-en_B']}]
            }
        },
        'metodos': {
            'viajar_A_C': [{
                'nombre': 'viaje_directo',
                'precondiciones': {'en_A'},
                'subtasks': ['mover_A_B', 'mover_B_C']
            }]
        },
        'observables': {'en_A', 'en_B', 'en_C'},
        'metas': {'en_C'}
    }

    print("=== Demostración Integrada ===")
    
    # Prueba SATPLAN
    print("\n1. Probando SATPLAN:")
    satplan = SATPLAN(
        list(dominio_compartido['acciones'].values()),  # Lista de acciones
        {'en_A'},  # Estado inicial
        {'en_C'}   # Metas
    )
    plan_sat = satplan.planificar()
    print(f"Plan SAT: {plan_sat}")
    
    # Prueba HTN
    print("\n2. Probando HTNPlanner:")
    htn = HTNPlanner(dominio_compartido)
    plan_htn = htn.planificar({'en_A'}, 'viajar_A_C')
    print(f"Plan HTN: {plan_htn}")
    
    # Prueba Conditional
    print("\n3. Probando ConditionalPlanner:")
    conditional = ConditionalPlanner(dominio_compartido)
    plan_cond = conditional.planificar({'en_A'}, {'en_C'})
    print(f"Plan condicional: {plan_cond}")
    
    # Prueba MonitorReplanner con HTN
    print("\n4. Probando MonitorReplanner con HTN:")
    monitor = MonitorReplanner(dominio_compartido, HTNPlanner)
    exito, acciones = monitor.ejecutar_y_monitorear({'en_A'}, {'en_C'})
    print(f"Resultado: {'Éxito' if exito else 'Fallo'}")
    print(f"Acciones ejecutadas: {acciones}")