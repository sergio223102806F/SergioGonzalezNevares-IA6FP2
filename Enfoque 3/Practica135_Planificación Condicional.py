from collections import defaultdict
import random

class ConditionalPlanner:
    """
    Planificador condicional que maneja incertidumbre mediante observaciones y acciones condicionales.
    """
    
    def __init__(self, dominio):
        """
        Inicializa el planificador con un dominio de planificación condicional.
        
        Args:
            dominio (dict): Contiene:
                - 'acciones': Acciones disponibles y sus efectos posibles
                - 'observables': Proposiciones que pueden ser observadas
        """
        self.dominio = dominio
        self.acciones = dominio.get('acciones', {})
        self.observables = dominio.get('observables', set())
        
    def generar_plan_condicional(self, estado_inicial, metas, max_profundidad=10):
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
        return self._construir_plan(estado_inicial, metas, set(), max_profundidad)
    
    def _construir_plan(self, estado, metas, historial, profundidad):
        """
        Función recursiva para construir el plan condicional.
        """
        # Caso base 1: Metas alcanzadas
        if metas.issubset(estado):
            return {'accion': None, 'ramas': {}}  # Plan terminado
            
        # Caso base 2: Profundidad máxima alcanzada
        if profundidad <= 0:
            return None  # Fracaso
            
        # Intentar cada acción posible
        for accion_nombre, accion in self.acciones.items():
            # Verificar precondiciones
            if not accion['precondiciones'].issubset(estado):
                continue
                
            # Crear estructura para este plan
            plan = {
                'accion': accion_nombre,
                'ramas': {}
            }
            
            # Generar todos los posibles efectos
            efectos_posibles = accion['efectos_posibles']
            exito = True
            
            for efecto_info in efectos_posibles:
                prob, efectos = efecto_info['probabilidad'], efecto_info['efectos']
                
                # Crear nuevo estado hipotético
                nuevo_estado = set(estado)
                for efecto in efectos:
                    if efecto.startswith('-'):
                        nuevo_estado.discard(efecto[1:])
                    else:
                        nuevo_estado.add(efecto)
                
                # Determinar qué se puede observar
                observaciones_posibles = self._generar_observaciones_posibles(nuevo_estado)
                
                # Para cada posible observación, construir subplan
                for obs in observaciones_posibles:
                    # Evitar ciclos revisando el historial
                    nuevo_historial = set(historial)
                    situacion = (accion_nombre, frozenset(nuevo_estado), obs)
                    
                    if situacion in nuevo_historial:
                        continue
                        
                    nuevo_historial.add(situacion)
                    
                    # Construir subplan recursivamente
                    subplan = self._construir_plan(nuevo_estado, metas, nuevo_historial, profundidad-1)
                    
                    if subplan is None:
                        exito = False
                        break
                        
                    plan['ramas'][obs] = subplan
                
                if not exito:
                    break
                    
            if exito:
                return plan
                
        return None
    
    def _generar_observaciones_posibles(self, estado):
        """
        Genera todas las posibles observaciones basadas en el estado actual.
        """
        observaciones = []
        
        # Observaciones individuales
        for obs in self.observables:
            if obs in estado:
                observaciones.append((obs, True))
            else:
                observaciones.append((obs, False))
        
        # Combinaciones relevantes (simplificado para el ejemplo)
        # En una implementación real, esto dependería del dominio
        if len(observaciones) > 0:
            # Solo devolvemos observaciones individuales para simplificar
            return [frozenset([obs]) for obs, valor in observaciones if valor]
        
        return [frozenset()]  # Observación vacía
    
    def ejecutar_plan(self, plan, estado_inicial, simulador_entorno=None, verbose=False):
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
        estado_actual = set(estado_inicial)
        historia_acciones = []
        historia_estados = [set(estado_actual)]
        nodo_actual = plan
        
        while nodo_actual['accion'] is not None:
            accion = nodo_actual['accion']
            
            if verbose:
                print(f"\nEstado actual: {estado_actual}")
                print(f"Ejecutando acción: {accion}")
            
            # Ejecutar acción (en entorno real o simulado)
            if simulador_entorno:
                nuevo_estado, observaciones = simulador_entorno(estado_actual, accion)
            else:
                nuevo_estado, observaciones = self._simular_accion(estado_actual, accion)
            
            historia_acciones.append(accion)
            estado_actual = nuevo_estado
            historia_estados.append(set(estado_actual))
            
            if verbose:
                print(f"Resultado: {observaciones}")
                print(f"Nuevo estado: {nuevo_estado}")
            
            # Seleccionar rama basada en observaciones
            if observaciones in nodo_actual['ramas']:
                nodo_actual = nodo_actual['ramas'][observaciones]
            else:
                # Si no hay rama específica, buscar la más general
                for obs_posible, subplan in nodo_actual['ramas'].items():
                    if obs_posible.issubset(observaciones):
                        nodo_actual = subplan
                        break
                else:
                    if verbose:
                        print("¡No se encontró rama adecuada en el plan condicional!")
                    return (False, historia_acciones, historia_estados)
        
        if verbose:
            print("\n¡Plan completado con éxito!")
        return (True, historia_acciones, historia_estados)
    
    def _simular_accion(self, estado, accion_nombre):
        """
        Simula el efecto de una acción para propósitos de demostración.
        """
        accion = self.acciones[accion_nombre]
        nuevo_estado = set(estado)
        
        # Elegir un efecto al azar según las probabilidades
        efectos_posibles = accion['efectos_posibles']
        rand_val = random.random()
        acum_prob = 0.0
        
        for efecto_info in efectos_posibles:
            acum_prob += efecto_info['probabilidad']
            if rand_val <= acum_prob:
                # Aplicar efectos
                for efecto in efecto_info['efectos']:
                    if efecto.startswith('-'):
                        nuevo_estado.discard(efecto[1:])
                    else:
                        nuevo_estado.add(efecto)
                break
        
        # Generar observaciones
        observaciones = set()
        for obs in self.observables:
            if obs in nuevo_estado:
                observaciones.add(obs)
        
        return nuevo_estado, frozenset(observaciones)


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
    print("=== Planificación Condicional ===")
    
    # Crear planificador
    planificador = ConditionalPlanner(dominio_condicional)
    
    # Definir problema
    estado_inicial = {'ubicacion_A', 'falla_detectable'}
    metas = {'sistema_reparado'}
    
    print(f"\nEstado inicial: {estado_inicial}")
    print(f"Metas: {metas}")
    
    # Generar plan condicional
    print("\nGenerando plan condicional...")
    plan = planificador.generar_plan_condicional(estado_inicial, metas)
    
    if plan:
        print("\n¡Plan condicional generado con éxito!")
        
        # Función para imprimir el plan de forma legible
        def imprimir_plan(nodo, nivel=0):
            indent = "  " * nivel
            if nodo['accion'] is None:
                print(f"{indent}FIN")
                return
                
            print(f"{indent}Acción: {nodo['accion']}")
            for obs, subplan in nodo['ramas'].items():
                print(f"{indent}Si se observa: {set(obs)}")
                imprimir_plan(subplan, nivel+1)
        
        imprimir_plan(plan)
        
        # Ejecutar plan (simulado)
        print("\nEjecutando plan...")
        exito, acciones, estados = planificador.ejecutar_plan(plan, estado_inicial, verbose=True)
        
        print("\nResumen de ejecución:")
        for i, (accion, estado) in enumerate(zip(acciones, estados[1:])):
            print(f"Paso {i}: Acción '{accion}' -> Estado: {estado}")
        
        print(f"\nResultado final: {'Éxito' if exito else 'Fallo'}")
    else:
        print("\nNo se pudo generar un plan condicional válido.")
