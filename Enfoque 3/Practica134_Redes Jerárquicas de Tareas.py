from collections import deque  # Importa la clase deque para usar como pila eficiente

class HTNPlanner:
    """
    Implementación de un planificador HTN (Hierarchical Task Network).
    Este planificador descompone tareas abstractas en acciones concretas mediante métodos.
    """

    def __init__(self, dominio):  # Inicializa el planificador con un dominio HTN.
        """
        Inicializa el planificador con un dominio HTN.

        Args:
            dominio (dict): Diccionario que contiene:
                - 'acciones': Acciones primitivas disponibles
                - 'metodos': Métodos de descomposición de tareas
        """
        self.dominio = dominio  # Almacena el diccionario del dominio HTN
        self.acciones = dominio.get('acciones', {})  # Obtiene las acciones primitivas del dominio, o un diccionario vacío si no están definidas
        self.metodos = dominio.get('metodos', {})  # Obtiene los métodos de descomposición del dominio, o un diccionario vacío si no están definidos

    def planificar(self, estado_inicial, tarea_principal, verbose=False):  # Genera un plan para lograr la tarea principal desde el estado inicial.
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
        stack = deque()  # Inicializa una deque para usar como pila en la búsqueda en profundidad
        stack.append(([tarea_principal], estado_inicial, []))  # Añade el estado inicial a la pila: (tareas pendientes, estado actual, plan parcial)

        while stack:  # Mientras la pila no esté vacía (quedan estados por explorar)
            tareas, estado, plan_parcial = stack.pop()  # Obtiene el último estado de la pila

            if verbose:  # Si el modo verbose está activado
                print(f"\nTareas pendientes: {tareas}")  # Imprime las tareas que aún deben ser planificadas
                print(f"Estado actual: {estado}")  # Imprime el estado actual del mundo
                print(f"Plan parcial: {plan_parcial}")  # Imprime las acciones que ya se han añadido al plan

            if not tareas:  # Si no quedan tareas pendientes
                return plan_parcial  # ¡Plan completado! Retorna el plan parcial como el plan final

            tarea_actual = tareas[0]  # Obtiene la primera tarea de la lista de tareas pendientes

            # Caso 1: La tarea es una acción primitiva
            if tarea_actual in self.acciones:  # Si la tarea actual es una acción primitiva definida en el dominio
                if verbose:  # Si el modo verbose está activado
                    print(f"Procesando acción primitiva: {tarea_actual}")  # Imprime que se está procesando una acción primitiva

                # Verificar precondiciones
                precondiciones = self.acciones[tarea_actual].get('precondiciones', set())  # Obtiene las precondiciones de la acción, o un conjunto vacío si no tiene
                if not precondiciones.issubset(estado):  # Si las precondiciones de la acción no están satisfechas en el estado actual
                    if verbose:  # Si el modo verbose está activado
                        print(f"Precondiciones no satisfechas para {tarea_actual}")  # Imprime que las precondiciones no se cumplen
                    continue  # Backtrack: pasa a la siguiente iteración del bucle while (prueba otra rama de búsqueda)

                # Aplicar efectos
                nuevo_estado = set(estado)  # Crea una copia del estado actual para aplicar los efectos sin modificar el original
                efectos = self.acciones[tarea_actual].get('efectos', set())  # Obtiene los efectos de la acción, o un conjunto vacío si no tiene
                for efecto in efectos:  # Itera sobre cada efecto de la acción
                    if efecto.startswith('-'):  # Si el efecto comienza con '-', es una negación (eliminar del estado)
                        nuevo_estado.discard(efecto[1:])  # Elimina la proposición negada del nuevo estado
                    else:  # Si no comienza con '-', es una adición (añadir al estado)
                        nuevo_estado.add(efecto)  # Añade la proposición al nuevo estado

                # Continuar con el resto de tareas
                stack.append((tareas[1:], nuevo_estado, plan_parcial + [tarea_actual]))  # Añade el nuevo estado a la pila: (tareas restantes, nuevo estado, plan con la acción añadida)

            # Caso 2: La tarea es abstracta y tiene métodos de descomposición
            elif tarea_actual in self.metodos:  # Si la tarea actual es abstracta y tiene métodos de descomposición definidos
                if verbose:  # Si el modo verbose está activado
                    print(f"Descomponiendo tarea abstracta: {tarea_actual}")  # Imprime que se está descomponiendo una tarea abstracta

                # Probar todos los métodos posibles
                for metodo in self.metodos[tarea_actual]:  # Itera sobre cada método de descomposición para la tarea abstracta
                    # Verificar precondiciones del método
                    precond_metodo = metodo.get('precondiciones', set())  # Obtiene las precondiciones del método, o un conjunto vacío si no tiene
                    if not precond_metodo.issubset(estado):  # Si las precondiciones del método no están satisfechas en el estado actual
                        if verbose:  # Si el modo verbose está activado
                            print(f"Precondiciones no satisfechas para método {metodo['nombre']}")  # Imprime que las precondiciones del método no se cumplen
                        continue  # Pasa al siguiente método

                    # Añadir subtareas al frente de la lista
                    nuevas_tareas = metodo['subtasks'] + tareas[1:]  # Crea una nueva lista de tareas: subtareas del método + tareas restantes
                    stack.append((nuevas_tareas, estado, plan_parcial))  # Añade el nuevo estado a la pila: (nuevas tareas, estado actual, plan parcial)

            # Caso 3: Tarea desconocida
            else:  # Si la tarea actual no es una acción primitiva ni una tarea abstracta con métodos
                if verbose:  # Si el modo verbose está activado
                    print(f"Tarea desconocida: {tarea_actual}")  # Imprime que la tarea es desconocida
                continue  # Backtrack: pasa a la siguiente iteración del bucle while

        return None  # No se encontró plan si la pila se vacía sin encontrar una solución


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
    print("=== Planificador HTN ===")  # Imprime un encabezado

    # Crear planificador
    planificador = HTNPlanner(dominio_htn)  # Crea una instancia del planificador HTN

    # Definir problema
    estado_inicial = {'en_A', 'combustible_bajo'}  # Define el estado inicial del mundo
    tarea_principal = 'viajar_A_C'  # Define la tarea principal a lograr

    print(f"\nEstado inicial: {estado_inicial}")  # Imprime el estado inicial
    print(f"Tarea principal: {tarea_principal}")  # Imprime la tarea principal

    # Generar plan
    plan = planificador.planificar(estado_inicial, tarea_principal, verbose=True)  # Intenta generar un plan, con salida verbose activada

    # Mostrar resultados
    if plan:  # Si se encontró un plan (la lista 'plan' no está vacía o es None)
        print("\n¡Plan encontrado!")  # Imprime un mensaje de éxito
        for i, accion in enumerate(plan):  # Itera sobre las acciones en el plan
            print(f"Paso {i}: {accion}")  # Imprime el número de paso y la acción
    else:  # Si no se encontró un plan (plan es None)
        print("\nNo se encontró un plan válido.")  # Imprime un mensaje de fallo
