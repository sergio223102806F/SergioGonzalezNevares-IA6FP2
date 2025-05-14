# -*- coding: utf-8 -*-                                  # Especifica la codificación del archivo
"""
Sistema de Planificación Avanzada                       # Documentación del módulo
Created on [Fecha]                                      # Fecha de creación
@author: [Tu nombre]                                    # Autor del código
"""

from collections import deque                           # Importa deque para colas eficientes
import random                                           # Para generación de números aleatorios
import pycosat                                          # Solver SAT para problemas de satisfacibilidad

class SATPLAN:                                          # Definición de la clase SATPLAN
    """Planificador basado en satisfacibilidad booleana"""  # Docstring de la clase
    
    def __init__(self, acciones, estado_inicial, metas, max_pasos=10):  # Constructor de la clase
        self.acciones = acciones                        # Almacena la lista de acciones
        self.estado_inicial = estado_inicial           # Guarda el estado inicial
        self.metas = metas                             # Almacena las metas a alcanzar
        self.max_pasos = max_pasos                     # Establece máximo de pasos temporales
        self.prop_a_var = {}                           # Diccionario para mapeo proposición→variable
        self.var_counter = 1                           # Contador de variables proposicionales

    def _generar_variable(self, nombre):               # Método privado para generar variables
        if nombre not in self.prop_a_var:              # Verifica si la variable no existe
            self.prop_a_var[nombre] = self.var_counter # Asigna nuevo ID de variable
            self.var_counter += 1                      # Incrementa el contador de variables
        return self.prop_a_var[nombre]                 # Retorna el ID de la variable

    def planificar(self):                              # Método principal de planificación
        clausulas = []                                 # Lista para almacenar cláusulas SAT
        
        for prop in self.estado_inicial:               # Para cada proposición en estado inicial
            var = self._generar_variable(f"{prop}_0")   # Genera variable para tiempo 0
            clausulas.append([var])                    # Añade cláusula unitaria positiva
            
        for meta in self.metas:                        # Para cada proposición meta
            var = self._generar_variable(f"{meta}_{self.max_pasos}")  # Variable para tiempo final
            clausulas.append([var])                    # Añade cláusula unitaria positiva
            
        for paso in range(self.max_pasos):             # Para cada paso temporal
            for accion in self.acciones:               # Para cada acción disponible
                var_accion = self._generar_variable(f"{accion['nombre']}_{paso}")  # Variable acción
                
                for precond in accion['precondiciones']:  # Para cada precondición
                    var_precond = self._generar_variable(f"{precond}_{paso}")  # Variable precond
                    clausulas.append([-var_accion, var_precond])  # ¬acción ∨ precondición
                
                for efecto in accion['efectos']:       # Para cada efecto de la acción
                    var_efecto = self._generar_variable(f"{efecto}_{paso+1}")  # Variable efecto
                    clausulas.append([-var_accion, var_efecto])  # ¬acción ∨ efecto
        
        solucion = pycosat.solve(clausulas)            # Resuelve el problema SAT
        
        if solucion == "UNSAT":                        # Si no hay solución
            return None                                # Retorna None
            
        plan = []                                      # Lista para almacenar el plan
        for paso in range(self.max_pasos):             # Para cada paso temporal
            for accion in self.acciones:               # Para cada acción
                var_accion = self.prop_a_var.get(f"{accion['nombre']}_{paso}")  # Obtiene variable
                if var_accion and var_accion in solucion:  # Si acción está en solución
                    plan.append(accion['nombre'])      # Añade acción al plan
                    break                              
                    
        return plan                                    # Retorna el plan encontrado

class HTNPlanner:                                      # Definición de la clase HTNPlanner
    """Planificador de Redes Jerárquicas de Tareas"""   # Docstring de la clase
    
    def __init__(self, dominio):                       # Constructor de la clase
        self.dominio = dominio                         # Almacena el dominio de planificación
        
    def planificar(self, estado_inicial, tarea_principal):  # Método de planificación
        stack = [([tarea_principal], set(estado_inicial), [])]  # Pila para DFS: (tareas, estado, plan)
        
        while stack:                                   # Mientras haya nodos por explorar
            tareas, estado, plan = stack.pop()         # Extrae último nodo (DFS)
            
            if not tareas:                             # Si no hay tareas pendientes
                return plan                            # Retorna plan solución
                
            tarea = tareas[0]                          # Tarea actual a procesar
            
            if tarea in self.dominio['acciones']:      # Si es acción primitiva
                accion = self.dominio['acciones'][tarea]  # Obtiene definición de acción
                if not accion['precondiciones'].issubset(estado):  # Verifica precondiciones
                    continue                           # Salta si no se cumplen
                    
                nuevo_estado = set(estado)             # Copia el estado actual
                for efecto in accion['efectos']:       # Aplica cada efecto
                    if efecto.startswith('-'):          # Si es efecto negativo
                        nuevo_estado.discard(efecto[1:])  # Elimina del estado
                    else:                              # Si es efecto positivo
                        nuevo_estado.add(efecto)       # Añade al estado
                
                stack.append((tareas[1:], nuevo_estado, plan + [tarea]))  # Añade a pila
            
            elif tarea in self.dominio['metodos']:     # Si es tarea abstracta
                for metodo in self.dominio['metodos'][tarea]:  # Para cada método
                    if metodo['precondiciones'].issubset(estado):  # Verifica precondiciones
                        nuevas_tareas = metodo['subtasks'] + tareas[1:]  # Reemplaza tarea
                        stack.append((nuevas_tareas, estado, plan))  # Añade a pila
        
        return None                                    # No se encontró solución

class MonitorReplanner:                                # Definición de la clase MonitorReplanner
    """Sistema de ejecución con monitoreo y replanificación"""  # Docstring de la clase
    
    def __init__(self, dominio, planner_class):        # Constructor de la clase
        self.dominio = dominio                         # Almacena el dominio
        self.PlannerClass = planner_class              # Clase del planificador a usar
        self.plan_actual = None                        # Plan actual en ejecución
        self.estado_actual = None                      # Estado actual del mundo
        
    def ejecutar_y_monitorear(self, estado_inicial, metas, max_intentos=3):  # Método principal
        self.estado_actual = set(estado_inicial)       # Inicializa estado actual
        intentos = 0                                   # Contador de intentos
        
        while intentos < max_intentos:                 # Mientras queden intentos
            intentos += 1                              # Incrementa contador
            
            planner = self.PlannerClass(self.dominio)  # Crea instancia del planificador
            self.plan_actual = planner.planificar(self.estado_actual, metas)  # Genera plan
            
            if not self.plan_actual:                   # Si no se pudo generar plan
                return False, []                       # Retorna fallo
                
            exito, acciones = self._ejecutar_plan()    # Ejecuta el plan
            if exito:                                  # Si tuvo éxito
                return True, acciones                  # Retorna éxito y acciones
                
        return False, []                              # Retorna fallo si agota intentos
        
    def _ejecutar_plan(self):                         # Método privado para ejecución
        acciones_ejecutadas = []                      # Lista de acciones ejecutadas
        
        for accion in self.plan_actual:               # Para cada acción en el plan
            exito, nuevo_estado = self._simular_ejecucion(accion)  # Simula ejecución
            if not exito:                             # Si falló la ejecución
                return False, acciones_ejecutadas     # Retorna fallo
                
            self.estado_actual = nuevo_estado         # Actualiza estado
            acciones_ejecutadas.append(accion)        # Registra acción ejecutada
            
            if self._metas_cumplidas():               # Verifica si se cumplieron metas
                return True, acciones_ejecutadas       # Retorna éxito
                
        return self._metas_cumplidas(), acciones_ejecutadas  # Retorna resultado final
        
    def _simular_ejecucion(self, accion):             # Método privado para simulación
        if random.random() > 0.9:                     # 10% probabilidad de fallo
            return False, self.estado_actual          # Retorna fallo
            
        nuevo_estado = set(self.estado_actual)        # Copia estado actual
        for efecto in self.dominio['acciones'][accion]['efectos']:  # Aplica efectos
            if efecto.startswith('-'):                # Si es efecto negativo
                nuevo_estado.discard(efecto[1:])      # Elimina del estado
            else:                                    # Si es efecto positivo
                nuevo_estado.add(efecto)             # Añade al estado
                
        return True, nuevo_estado                    # Retorna éxito y nuevo estado
        
    def _metas_cumplidas(self):                      # Método privado para verificar metas
        return all(meta in self.estado_actual for meta in self.dominio['metas'])  # Verifica todas

if __name__ == "__main__":                           # Bloque principal de ejecución
    dominio_ejemplo = {                              # Define dominio de ejemplo
        'acciones': {
            'mover_A_B': {
                'precondiciones': {'en_A'},
                'efectos': {'en_B', '-en_A'}
            },
            'mover_B_C': {
                'precondiciones': {'en_B'},
                'efectos': {'en_C', '-en_B'}
            }
        },
        'metodos': {
            'viajar_A_C': [{
                'precondiciones': {'en_A'},
                'subtasks': ['mover_A_B', 'mover_B_C']
            }]
        },
        'metas': {'en_C'}
    }

    print("=== Demostración de Planificación ===")    # Encabezado de demostración
    
    print("\n1. Planificación con SATPLAN:")         # Prueba SATPLAN
    satplan = SATPLAN(                               # Crea instancia de SATPLAN
        list(dominio_ejemplo['acciones'].values()),  # Pasa lista de acciones
        {'en_A'},                                    # Estado inicial
        {'en_C'}                                     # Metas
    )
    print(f"Plan generado: {satplan.planificar()}")  # Muestra plan generado
    
    print("\n2. Planificación HTN:")                 # Prueba HTN
    htn = HTNPlanner(dominio_ejemplo)                # Crea instancia de HTNPlanner
    print(f"Plan generado: {htn.planificar({'en_A'}, 'viajar_A_C')}")  # Muestra plan
    
    print("\n3. Ejecución con MonitorReplanner:")    # Prueba MonitorReplanner
    monitor = MonitorReplanner(dominio_ejemplo, HTNPlanner)  # Crea instancia
    exito, acciones = monitor.ejecutar_y_monitorear({'en_A'}, {'en_C'})  # Ejecuta
    print(f"Resultado: {'Éxito' if exito else 'Fallo'}")     # Muestra resultado
    print(f"Acciones ejecutadas: {acciones}")                # Muestra acciones