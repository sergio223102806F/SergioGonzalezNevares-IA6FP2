from collections import deque

class HTNPlanner:
    """
    Implementación de un planificador HTN (Hierarchical Task Network).
    Este planificador descompone tareas abstractas en acciones concretas mediante métodos.
    """
    
    def __init__(self, dominio):
        """
        Inicializa el planificador con un dominio HTN.
        
        Args:
            dominio (dict): Diccionario que contiene:
                - 'acciones': Acciones primitivas disponibles
                - 'metodos': Métodos de descomposición de tareas
        """
        self.dominio = dominio
        self.acciones = dominio.get('acciones', {})
        self.metodos = dominio.get('metodos', {})
    
    def planificar(self, estado_inicial, tarea_principal, verbose=False):
        """
        Genera un plan para lograr la tarea principal desde el estado inicial.
        
        Args:
            estado_inicial (set): Estado inicial del mundo
            tarea_principal (str): Tarea principal a lograr
            verbose (bool): Si True, muestra información de depuración
            
        Returns:
            list: Lista de acciones del plan, o None si no se encuentra solución
        """
        # Usamos búsqueda en profundidad con backtracking
        stack = deque()
        stack.append(([tarea_principal], estado_inicial, []))
        
        while stack:
            tareas, estado, plan_parcial = stack.pop()
            
            if verbose:
                print(f"\nTareas pendientes: {tareas}")
                print(f"Estado actual: {estado}")
                print(f"Plan parcial: {plan_parcial}")
            
            if not tareas:
                return plan_parcial  # ¡Plan completado!
            
            tarea_actual = tareas[0]
            
            # Caso 1: La tarea es una acción primitiva
            if tarea_actual in self.acciones:
                if verbose:
                    print(f"Procesando acción primitiva: {tarea_actual}")
                
                # Verificar precondiciones
                precondiciones = self.acciones[tarea_actual].get('precondiciones', set())
                if not precondiciones.issubset(estado):
                    if verbose:
                        print(f"Precondiciones no satisfechas para {tarea_actual}")
                    continue  # Backtrack
                
                # Aplicar efectos
                nuevo_estado = set(estado)
                efectos = self.acciones[tarea_actual].get('efectos', set())
                for efecto in efectos:
                    if efecto.startswith('-'):
                        nuevo_estado.discard(efecto[1:])
                    else:
                        nuevo_estado.add(efecto)
                
                # Continuar con el resto de tareas
                stack.append((tareas[1:], nuevo_estado, plan_parcial + [tarea_actual]))
            
            # Caso 2: La tarea es abstracta y tiene métodos de descomposición
            elif tarea_actual in self.metodos:
                if verbose:
                    print(f"Descomponiendo tarea abstracta: {tarea_actual}")
                
                # Probar todos los métodos posibles
                for metodo in self.metodos[tarea_actual]:
                    # Verificar precondiciones del método
                    precond_metodo = metodo.get('precondiciones', set())
                    if not precond_metodo.issubset(estado):
                        if verbose:
                            print(f"Precondiciones no satisfechas para método {metodo['nombre']}")
                        continue
                    
                    # Añadir subtareas al frente de la lista
                    nuevas_tareas = metodo['subtasks'] + tareas[1:]
                    stack.append((nuevas_tareas, estado, plan_parcial))
            
            # Caso 3: Tarea desconocida
            else:
                if verbose:
                    print(f"Tarea desconocida: {tarea_actual}")
                continue  # Backtrack
        
        return None  # No se encontró plan


# Ejemplo de dominio HTN
dominio_htn = {
    'acciones': {
        'mover_A_B': {
            'precondiciones': {'en_A'},
            'efectos': {'en_B', '-en_A'}
        },
        'mover_B_C': {
            'precondiciones': {'en_B'},
            'efectos': {'en_C', '-en_B'}
        },
        'mover_B_A': {
            'precondiciones': {'en_B'},
            'efectos': {'en_A', '-en_B'}
        },
        'mover_C_B': {
            'precondiciones': {'en_C'},
            'efectos': {'en_B', '-en_C'}
        },
        'cargar_combustible': {
            'precondiciones': {'en_estacion'},
            'efectos': {'combustible_lleno', '-combustible_bajo'}
        }
    },
    'metodos': {
        'viajar_A_C': [
            {
                'nombre': 'viaje_directo',
                'precondiciones': {'en_A'},
                'subtasks': ['mover_A_B', 'mover_B_C']
            },
            {
                'nombre': 'viaje_con_combustible',
                'precondiciones': {'en_A', 'combustible_bajo'},
                'subtasks': ['mover_A_B', 'cargar_combustible', 'mover_B_C']
            }
        ],
        'reabastecer': [
            {
                'nombre': 'reabastecer_directo',
                'precondiciones': {'en_estacion'},
                'subtasks': ['cargar_combustible']
            },
            {
                'nombre': 'reabastecer_viaje',
                'precondiciones': {'en_B'},
                'subtasks': ['mover_B_A', 'cargar_combustible']
            }
        ]
    }
}


# Ejemplo de uso
if __name__ == "__main__":
    print("=== Planificador HTN ===")
    
    # Crear planificador
    planificador = HTNPlanner(dominio_htn)
    
    # Definir problema
    estado_inicial = {'en_A', 'combustible_bajo'}
    tarea_principal = 'viajar_A_C'
    
    print(f"\nEstado inicial: {estado_inicial}")
    print(f"Tarea principal: {tarea_principal}")
    
    # Generar plan
    plan = planificador.planificar(estado_inicial, tarea_principal, verbose=True)
    
    # Mostrar resultados
    if plan:
        print("\n¡Plan encontrado!")
        for i, accion in enumerate(plan):
            print(f"Paso {i}: {accion}")
    else:
        print("\nNo se encontró un plan válido.")
