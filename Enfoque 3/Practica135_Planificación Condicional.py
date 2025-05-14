from collections import defaultdict  # Importa la clase defaultdict del módulo collections
import random  # Importa el módulo random para generar números aleatorios

class ConditionalPlanner:
    """
    Planificador condicional que maneja incertidumbre mediante observaciones y acciones condicionales.
    """

    def __init__(self, dominio):  # Inicializa el planificador con un dominio de planificación condicional.
        """
        Inicializa el planificador con un dominio de planificación condicional.

        Args:
            dominio (dict): Contiene:
                - 'acciones': Acciones disponibles y sus efectos posibles
                - 'observables': Proposiciones que pueden ser observadas
        """
        self.dominio = dominio  # Almacena el diccionario del dominio
        self.acciones = dominio.get('acciones', {})  # Obtiene las acciones del dominio, o un diccionario vacío si no están definidas
        self.observables = dominio.get('observables', set())  # Obtiene las proposiciones observables del dominio, o un conjunto vacío si no están definidas

    def generar_plan_condicional(self, estado_inicial, metas, max_profundidad=10):  # Genera un plan condicional que alcanza las metas desde el estado inicial.
        """
        Genera un plan condicional que alcanza las metas desde el estado inicial.

        Args:
            estado_inicial (set): Estado inicial conocido
            metas (set): Conjunto de metas a alcanzar
            max_profundidad (int): Límite de profundidad de búsqueda

        Returns:
            dict: Árbol de plan condicional con estructura:
                {
                    'accion': nombre_accion,
                    'ramas': {
                        observacion: subplan,
                        ...
                    }
                }
        """
        return self._construir_plan(estado_inicial, metas, set(), max_profundidad)  # Llama a la función recursiva para construir el plan condicional

    def _construir_plan(self, estado, metas, historial, profundidad):  # Función recursiva para construir el plan condicional.
        """
        Función recursiva para construir el plan condicional.
        """
        # Caso base 1: Metas alcanzadas
        if metas.issubset(estado):  # Si todas las metas están incluidas en el estado actual
            return {'accion': None, 'ramas': {}}  # Plan terminado, retorna un nodo sin acción y ramas vacías

        # Caso base 2: Profundidad máxima alcanzada
        if profundidad <= 0:  # Si se ha alcanzado el límite de profundidad de búsqueda
            return None  # Fracaso, retorna None indicando que no se encontró un plan en esta rama

        # Intentar cada acción posible
        for accion_nombre, accion in self.acciones.items():  # Itera sobre cada acción definida en el dominio
            # Verificar precondiciones
            if not accion['precondiciones'].issubset(estado):  # Si las precondiciones de la acción no están satisfechas en el estado actual
                continue  # Pasa a la siguiente acción

            # Crear estructura para este plan
            plan = {
                'accion': accion_nombre,
                'ramas': {}
            }

            # Generar todos los posibles efectos
            efectos_posibles = accion['efectos_posibles']  # Obtiene la lista de posibles efectos de la acción
            exito = True  # Variable para rastrear si se encuentra un subplan exitoso para todos los resultados posibles

            for efecto_info in efectos_posibles:  # Itera sobre cada posible efecto de la acción
                prob, efectos = efecto_info['probabilidad'], efecto_info['efectos']  # Obtiene la probabilidad y los efectos del resultado

                # Crear nuevo estado hipotético
                nuevo_estado = set(estado)  # Crea una copia del estado actual
                for efecto in efectos:  # Aplica cada efecto al nuevo estado
                    if efecto.startswith('-'):
                        nuevo_estado.discard(efecto[1:])  # Elimina el efecto negativo
                    else:
                        nuevo_estado.add(efecto)  # Añade el efecto positivo

                # Determinar qué se puede observar
                observaciones_posibles = self._generar_observaciones_posibles(nuevo_estado)  # Genera las posibles observaciones en el nuevo estado

                # Para cada posible observación, construir subplan
                for obs in observaciones_posibles:  # Itera sobre cada posible observación
                    # Evitar ciclos revisando el historial
                    nuevo_historial = set(historial)  # Crea una copia del historial
                    situacion = (accion_nombre, frozenset(nuevo_estado), obs)  # Define la situación actual

                    if situacion in nuevo_historial:  # Si ya se ha visitado esta situación
                        continue  # Evita ciclos

                    nuevo_historial.add(situacion)  # Añade la situación al historial

                    # Construir subplan recursivamente
                    subplan = self._construir_plan(nuevo_estado, metas, nuevo_historial, profundidad-1)  # Llama recursivamente para construir el subplan

                    if subplan is None:  # Si no se encuentra un subplan para esta observación
                        exito = False  # Marca el intento actual de la acción como fallido
                        break  # Sale del bucle de observaciones

                    plan['ramas'][obs] = subplan  # Añade el subplan a las ramas del plan actual

                if not exito:  # Si no se encontró un subplan exitoso para todos los resultados posibles de la acción
                    break  # Sale del bucle de acciones

            if exito:  # Si se encontró un subplan exitoso para todos los resultados posibles de la acción
                return plan  # Retorna el plan condicional para esta acción

        return None  # Si no se encuentra un plan para ninguna acción, retorna None

    def _generar_observaciones_posibles(self, estado):  # Genera todas las posibles observaciones basadas en el estado actual.
        """
        Genera todas las posibles observaciones basadas en el estado actual.
        """
        observaciones = []  # Inicializa una lista para almacenar las observaciones

        # Observaciones individuales
        for obs in self.observables:  # Itera sobre cada proposición observable
            if obs in estado:  # Si la proposición observable está en el estado
                observaciones.append((obs, True))  # Añade una observación verdadera
            else:
                observaciones.append((obs, False))  # Añade una observación falsa

        # Combinaciones relevantes (simplificado para el ejemplo)
        # En una implementación real, esto dependería del dominio
        if len(observaciones) > 0:
            # Solo devolvemos observaciones individuales para simplificar
            return [frozenset([obs]) for obs, valor in observaciones if valor]

        return [frozenset()]  # Observación vacía

    def ejecutar_plan(self, plan, estado_inicial, simulador_entorno=None, verbose=False):  # Ejecuta un plan condicional en un entorno (real o simulado).
        """
        Ejecuta un plan condicional en un entorno (real o simulado).

        Args:
            plan (dict): Plan condicional a ejecutar
            estado_inicial (set): Estado inicial
            simulador_entorno (function): Función que simula el entorno
            verbose (bool): Mostrar información de depuración

        Returns:
            tuple: (exito, historia_acciones, historia_estados)
        """
        estado_actual = set(estado_inicial)  # Inicializa el estado actual
        historia_acciones = []  # Inicializa la historia de las acciones ejecutadas
        historia_estados = [set(estado_actual)]  # Inicializa la historia de los estados
        nodo_actual = plan  # Comienza la ejecución desde la raíz del plan

        while nodo_actual['accion'] is not None:  # Mientras el nodo actual tenga una acción a ejecutar
            accion = nodo_actual['accion']  # Obtiene la acción del nodo actual

            if verbose:  # Si el modo verbose está activado
                print(f"\nEstado actual: {estado_actual}")  # Imprime el estado actual
                print(f"Ejecutando acción: {accion}")  # Imprime la acción que se va a ejecutar

            # Ejecutar acción (en entorno real o simulado)
            if simulador_entorno:  # Si se proporciona un simulador de entorno
                nuevo_estado, observaciones = simulador_entorno(estado_actual, accion)  # Llama al simulador para obtener el nuevo estado y las observaciones
            else:  # Si no se proporciona un simulador
                nuevo_estado, observaciones = self._simular_accion(estado_actual, accion)  # Simula la acción internamente

            historia_acciones.append(accion)  # Añade la acción a la historia de acciones
            estado_actual = nuevo_estado  # Actualiza el estado actual
            historia_estados.append(set(estado_actual))  # Añade el nuevo estado a la historia de estados

            if verbose:  # Si el modo verbose está activado
                print(f"Resultado: {observaciones}")  # Imprime las observaciones obtenidas
                print(f"Nuevo estado: {nuevo_estado}")  # Imprime el nuevo estado

            # Seleccionar rama basada en observaciones
            if observaciones in nodo_actual['ramas']:  # Si las observaciones coinciden con una rama específica
                nodo_actual = nodo_actual['ramas'][observaciones]  # Sigue la rama correspondiente
            else:  # Si no hay una rama específica
                # Si no hay rama específica, buscar la más general
                for obs_posible, subplan in nodo_actual['ramas'].items():  # Itera sobre las ramas posibles
                    if obs_posible.issubset(observaciones):  # Si la observación posible es un subconjunto de las observaciones reales
                        nodo_actual = subplan  # Sigue esta rama más general
                        break
                else:  # Si no se encuentra ninguna rama adecuada
                    if verbose:  # Si el modo verbose está activado
                        print("¡No se encontró rama adecuada en el plan condicional!")  # Imprime un mensaje de error
                    return (False, historia_acciones, historia_estados)  # Retorna fallo

        if verbose:  # Si el modo verbose está activado
            print("\n¡Plan completado con éxito!")  # Imprime un mensaje de éxito
        return (True, historia_acciones, historia_estados)  # Retorna éxito

    def _simular_accion(self, estado, accion_nombre):  # Simula el efecto de una acción para propósitos de demostración.
        """
        Simula el efecto de una acción para propósitos de demostración.
        """
        accion = self.acciones[accion_nombre]  # Obtiene la definición de la acción
        nuevo_estado = set(estado)  # Crea una copia del estado actual

        # Elegir un efecto al azar según las probabilidades
        efectos_posibles = accion['efectos_posibles']  # Obtiene los posibles efectos
        rand_val = random.random()  # Genera un número aleatorio entre 0 y 1
        acum_prob = 0.0  # Inicializa la probabilidad acumulada

        for efecto_info in efectos_posibles:  # Itera sobre los posibles efectos
            acum_prob += efecto_info['probabilidad']  # Acumula la probabilidad
            if rand_val <= acum_prob:  # Si el valor aleatorio cae dentro de la probabilidad del efecto
                # Aplicar efectos
                for efecto in efecto_info['efectos']:  # Aplica cada efecto
                    if efecto.startswith('-'):
                        nuevo_estado.discard(efecto[1:])  # Elimina el efecto negativo
                    else:
                        nuevo_estado.add(efecto)  # Añade el efecto positivo
                break  # Sale del bucle de efectos

        # Generar observaciones
        observaciones = set()  # Inicializa el conjunto de observaciones
        for obs in self.observables:  # Itera sobre las proposiciones observables
            if obs in nuevo_estado:  # Si la proposición observable está en el nuevo estado
                observaciones.add(obs)  # Añade la observación

        return nuevo_estado, frozenset(observaciones)  # Retorna el nuevo estado y las observaciones como un frozenset


# Ejemplo de dominio de planificación condicional
dominio_condicional = {
    'acciones': {
        'inspeccionar': {
            'precondiciones': {'ubicacion_A'},
            'efectos_posibles': [
                {
                    'probabilidad': 0.7,
                    'efectos': {'-falla_detectable', 'falla_identificada'}
                },
                {
                    'probabilidad': 0.3,
                    'efectos': {'-falla_detectable'}
                }
            ]
        },
        'reparar': {
            'precondiciones': {'falla_identificada'},
            'efectos_posibles': [
                {
                    'probabilidad': 0.9,
                    'efectos': {'-falla_identificada', 'sistema_reparado'}
                },
                {
                    'probabilidad': 0.1,
                    'efectos': {'-falla_identificada'}
                }
            ]
        },
        'diagnosticar': {
            'precondiciones': {'ubicacion_A', 'falla_detectable'},
            'efectos_posibles': [
                {
                    'probabilidad': 1.0,
                    'efectos': {'falla_identificada', '-falla_detectable'}
                }
            ]
        }
    },
    'observables': {
        'falla_detectable',
        'falla_identificada',
        'sistema_reparado'
    }
}


# Ejemplo de uso
if __name__ == "__main__":
    print("=== Planificación Condicional ===")  # Imprime un encabezado

    # Crear planificador
    planificador = ConditionalPlanner(dominio_condicional)  # Crea una instancia del planificador condicional

    # Definir problema
    estado_inicial = {'ubicacion_A', 'falla_detectable'}  # Define el estado inicial
    metas = {'sistema_reparado'}  # Define las metas a alcanzar

    print(f"\nEstado inicial: {estado_inicial}")  # Imprime el estado inicial
    print(f"Metas: {metas}")  # Imprime las metas

    # Generar plan condicional
    print("\nGenerando plan condicional...")  # Imprime un mensaje indicando que se está generando el plan
    plan = planificador.generar_plan_condicional(estado_inicial, metas)  # Genera el plan condicional

    if plan:  # Si se generó un plan
        print("\n¡Plan condicional generado con éxito!")  # Imprime un mensaje de éxito

        # Función para imprimir el plan de forma legible
        def imprimir_plan(nodo, nivel=0):  # Define una función recursiva para imprimir el plan
            indent = "  " * nivel  # Crea una indentación para la salida
            if nodo['accion'] is None:  # Si el nodo no tiene acción, es el final del plan
                print(f"{indent}FIN")  # Imprime "FIN"
                return

            print(f"{indent}Acción: {nodo['accion']}")  # Imprime la acción del nodo
            for obs, subplan in nodo['ramas'].items():  # Itera sobre las ramas del nodo (basadas en observaciones)
                print(f"{indent}Si se observa: {set(obs)}")  # Imprime la observación que lleva a este subplan
                imprimir_plan(subplan, nivel+1)  # Llama recursivamente para imprimir el subplan

        imprimir_plan(plan)  # Imprime el plan condicional

        # Ejecutar plan (simulado)
        print("\nEjecutando plan...")  # Imprime un mensaje indicando que se está ejecutando el plan
        exito, acciones, estados = planificador.ejecutar_plan(plan, estado_inicial, verbose=True)  # Ejecuta el plan y obtiene el resultado, las acciones y los estados

        print("\nResumen de ejecución:")  # Imprime un encabezado para el resumen de la ejecución
        for i, (accion, estado) in enumerate(zip(acciones, estados[1:])):  # Itera sobre las acciones y los estados durante la ejecución
            print(f"Paso {i}: Acción '{accion}' -> Estado: {estado}")  # Imprime el paso, la acción y el estado resultante

        print(f"\nResultado final: {'Éxito' if exito else 'Fallo'}")  # Imprime el resultado final de la ejecución
    else:  # Si no se pudo generar un plan
        print("\nNo se pudo generar un plan condicional válido.")  # Imprime un mensaje de fallo