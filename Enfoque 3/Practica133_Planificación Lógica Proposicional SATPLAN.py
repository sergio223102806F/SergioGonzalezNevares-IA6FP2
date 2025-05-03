import pycosat  # Necesitas instalar esto: pip install pycosat

class SATPLAN:
    def __init__(self, acciones, estado_inicial, metas, max_pasos=10):
        """
        Inicializa el planificador SATPLAN.
        
        Args:
            acciones (list): Lista de diccionarios que describen las acciones.
            estado_inicial (set): Proposiciones verdaderas al inicio.
            metas (set): Proposiciones que deben ser verdaderas al final.
            max_pasos (int): Máximo número de pasos temporales a considerar.
        """
        self.acciones = acciones
        self.estado_inicial = estado_inicial
        self.metas = metas
        self.max_pasos = max_pasos
        self.prop_a_var = {}  # Mapeo de proposiciones a variables SAT
        self.var_counter = 1  # Contador para variables únicas

    def _generar_variable(self, nombre):
        """Asigna o recupera una variable SAT para un nombre descriptivo."""
        if nombre not in self.prop_a_var:
            self.prop_a_var[nombre] = self.var_counter
            self.var_counter += 1
        return self.prop_a_var[nombre]

    def _obtener_todas_proposiciones(self):
        """Obtiene todas las proposiciones únicas del problema."""
        proposiciones = set(self.estado_inicial)
        proposiciones.update(self.metas)
        
        for accion in self.acciones:
            proposiciones.update(accion['precondiciones'])
            proposiciones.update(accion['efectos'])
            
        return proposiciones

    def _generar_codificacion_sat(self):
        """Genera la codificación SAT del problema de planificación."""
        clausulas = []
        
        # 1. Codificar estado inicial (tiempo 0)
        for prop in self.estado_inicial:
            var = self._generar_variable(f"{prop}_0")
            clausulas.append([var])  # Proposiciones iniciales son verdaderas

        # 2. Codificar metas (deben ser verdaderas en el último paso)
        ultimo_paso = self.max_pasos
        for meta in self.metas:
            var_meta = self._generar_variable(f"{meta}_{ultimo_paso}")
            clausulas.append([var_meta])

        # 3. Codificar acciones y efectos para cada paso
        for paso in range(self.max_pasos):
            vars_acciones_paso = []
            
            for accion in self.acciones:
                var_accion = self._generar_variable(f"{accion['nombre']}_{paso}")
                vars_acciones_paso.append(var_accion)
                
                # Precondiciones de la acción
                for precond in accion['precondiciones']:
                    var_precond = self._generar_variable(f"{precond}_{paso}")
                    clausulas.append([-var_accion, var_precond])  # Acción → Precondición
                
                # Efectos de la acción
                for efecto in accion['efectos']:
                    var_efecto = self._generar_variable(f"{efecto}_{paso+1}")
                    clausulas.append([-var_accion, var_efecto])  # Acción → Efecto

            # Restricción: al menos una acción por paso (opcional)
            clausulas.append(vars_acciones_paso)
            
            # Restricción: como máximo una acción por paso (exclusión mutua)
            for i in range(len(self.acciones)):
                for j in range(i+1, len(self.acciones)):
                    var1 = self._generar_variable(f"{self.acciones[i]['nombre']}_{paso}")
                    var2 = self._generar_variable(f"{self.acciones[j]['nombre']}_{paso}")
                    clausulas.append([-var1, -var2])  # No pueden ser ambas verdaderas

            # Frame axioms: lo que no cambia persiste
            for prop in self._obtener_todas_proposiciones():
                var_actual = self._generar_variable(f"{prop}_{paso}")
                var_siguiente = self._generar_variable(f"{prop}_{paso+1}")
                
                # Generar cláusulas para persistencia
                # Si una acción que afecta esta prop ocurre, no necesitamos frame axiom
                acciones_que_afectan = [a for a in self.acciones if prop in a['efectos'] or f"-{prop}" in a['efectos']]
                vars_acciones_afectan = [self._generar_variable(f"{a['nombre']}_{paso}") for a in acciones_que_afectan]
                
                if vars_acciones_afectan:
                    # Si ninguna acción que afecta la prop ocurre, entonces persiste
                    clausulas.append([var_actual, -var_siguiente] + vars_acciones_afectan)
                    clausulas.append([-var_actual, var_siguiente] + vars_acciones_afectan)
                else:
                    # Si no hay acciones que afecten esta prop, debe persistir
                    clausulas.append([var_actual, -var_siguiente])
                    clausulas.append([-var_actual, var_siguiente])

        return clausulas

    def resolver(self):
        """Resuelve el problema de planificación usando un SAT solver."""
        clausulas = self._generar_codificacion_sat()
        
        try:
            solucion = pycosat.solve(clausulas)
        except Exception as e:
            print(f"Error al resolver SAT: {e}")
            return None
            
        if isinstance(solucion, str) and solucion == "UNSAT":
            return None  # No se encontró solución
            
        # Extraer el plan de la solución SAT
        plan = []
        for paso in range(self.max_pasos):
            for accion in self.acciones:
                var_accion = self.prop_a_var.get(f"{accion['nombre']}_{paso}")
                if var_accion and var_accion in solucion:
                    plan.append(accion['nombre'])
                    break
                    
        return plan if plan else None


# Ejemplo completo de uso
if __name__ == "__main__":
    # Definir acciones disponibles
    acciones = [
        {
            'nombre': 'mover_A_B',
            'precondiciones': {'en_A'},
            'efectos': {'en_B', '-en_A'}
        },
        {
            'nombre': 'mover_B_A',
            'precondiciones': {'en_B'},
            'efectos': {'en_A', '-en_B'}
        },
        {
            'nombre': 'mover_B_C',
            'precondiciones': {'en_B'},
            'efectos': {'en_C', '-en_B'}
        },
        {
            'nombre': 'mover_C_B',
            'precondiciones': {'en_C'},
            'efectos': {'en_B', '-en_C'}
        }
    ]
    
    # Definir problema de planificación
    estado_inicial = {'en_A'}
    metas = {'en_C'}
    
    print("=== Problema de Planificación ===")
    print(f"Estado inicial: {estado_inicial}")
    print(f"Metas: {metas}")
    print(f"Acciones disponibles: {[a['nombre'] for a in acciones]}")
    
    # Crear y ejecutar planificador
    print("\nEjecutando SATPLAN...")
    planificador = SATPLAN(acciones, estado_inicial, metas, max_pasos=5)
    plan = planificador.resolver()
    
    # Mostrar resultados
    if plan:
        print("\n¡Plan encontrado!")
        for i, accion in enumerate(plan):
            print(f"Paso {i}: {accion}")
    else:
        print("\nNo se encontró un plan válido dentro del límite de pasos.")
