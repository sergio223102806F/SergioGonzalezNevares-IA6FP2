import pycosat  # Necesitas instalar esto: pip install pycosat

class SATPLAN:
    def __init__(self, acciones, estado_inicial, metas, max_pasos=10):  # Inicializa el planificador SATPLAN.
        """
        Inicializa el planificador SATPLAN.

        Args:
            acciones (list): Lista de diccionarios que describen las acciones.
            estado_inicial (set): Proposiciones verdaderas al inicio.
            metas (set): Proposiciones que deben ser verdaderas al final.
            max_pasos (int): Máximo número de pasos temporales a considerar.
        """
        self.acciones = acciones  # Guarda la lista de acciones disponibles
        self.estado_inicial = estado_inicial  # Guarda el conjunto de proposiciones verdaderas al inicio
        self.metas = metas  # Guarda el conjunto de proposiciones que deben ser verdaderas al final
        self.max_pasos = max_pasos  # Guarda el máximo número de pasos temporales a considerar
        self.prop_a_var = {}  # Mapeo de proposiciones a variables SAT
        self.var_counter = 1  # Contador para variables únicas

    def _generar_variable(self, nombre):  # Asigna o recupera una variable SAT para un nombre descriptivo.
        """Asigna o recupera una variable SAT para un nombre descriptivo."""
        if nombre not in self.prop_a_var:  # Si el nombre no está en el mapeo de proposiciones a variables
            self.prop_a_var[nombre] = self.var_counter  # Asigna el contador actual como la variable para este nombre
            self.var_counter += 1  # Incrementa el contador para la siguiente variable única
        return self.prop_a_var[nombre]  # Retorna la variable SAT asociada al nombre

    def _obtener_todas_proposiciones(self):  # Obtiene todas las proposiciones únicas del problema.
        """Obtiene todas las proposiciones únicas del problema."""
        proposiciones = set(self.estado_inicial)  # Inicializa el conjunto de proposiciones con el estado inicial
        proposiciones.update(self.metas)  # Añade las proposiciones de las metas al conjunto

        for accion in self.acciones:  # Itera sobre cada acción en la lista de acciones
            proposiciones.update(accion['precondiciones'])  # Añade las precondiciones de la acción al conjunto
            proposiciones.update(accion['efectos'])  # Añade los efectos de la acción al conjunto

        return proposiciones  # Retorna el conjunto de todas las proposiciones únicas

    def _generar_codificacion_sat(self):  # Genera la codificación SAT del problema de planificación.
        """Genera la codificación SAT del problema de planificación."""
        clausulas = []  # Inicializa una lista vacía para almacenar las cláusulas SAT

        # 1. Codificar estado inicial (tiempo 0)
        for prop in self.estado_inicial:  # Itera sobre cada proposición en el estado inicial
            var = self._generar_variable(f"{prop}_0")  # Genera una variable SAT para la proposición en el tiempo 0
            clausulas.append([var])  # Proposiciones iniciales son verdaderas

        # 2. Codificar metas (deben ser verdaderas en el último paso)
        ultimo_paso = self.max_pasos  # Define el último paso temporal
        for meta in self.metas:  # Itera sobre cada meta
            var_meta = self._generar_variable(f"{meta}_{ultimo_paso}")  # Genera una variable SAT para la meta en el último paso
            clausulas.append([var_meta])  # Las metas deben ser verdaderas en el último paso

        # 3. Codificar acciones y efectos para cada paso
        for paso in range(self.max_pasos):  # Itera sobre cada paso de tiempo
            vars_acciones_paso = []  # Lista para guardar las variables de las acciones en este paso

            for accion in self.acciones:  # Itera sobre cada acción disponible
                var_accion = self._generar_variable(f"{accion['nombre']}_{paso}")  # Genera una variable SAT para la acción en este paso
                vars_acciones_paso.append(var_accion)  # Añade la variable de la acción a la lista de acciones del paso

                # Precondiciones de la acción
                for precond in accion['precondiciones']:  # Itera sobre las precondiciones de la acción
                    var_precond = self._generar_variable(f"{precond}_{paso}")  # Genera una variable SAT para la precondición en este paso
                    clausulas.append([-var_accion, var_precond])  # Acción → Precondición

                # Efectos de la acción
                for efecto in accion['efectos']:  # Itera sobre los efectos de la acción
                    var_efecto = self._generar_variable(f"{efecto}_{paso+1}")  # Genera una variable SAT para el efecto en el siguiente paso
                    clausulas.append([-var_accion, var_efecto])  # Acción → Efecto

            # Restricción: al menos una acción por paso (opcional)
            clausulas.append(vars_acciones_paso)  # Al menos una acción por paso

            # Restricción: como máximo una acción por paso (exclusión mutua)
            for i in range(len(self.acciones)):  # Itera sobre las acciones
                for j in range(i+1, len(self.acciones)):  # Itera sobre las siguientes acciones
                    var1 = self._generar_variable(f"{self.acciones[i]['nombre']}_{paso}")  # Variable para la acción i en este paso
                    var2 = self._generar_variable(f"{self.acciones[j]['nombre']}_{paso}")  # Variable para la acción j en este paso
                    clausulas.append([-var1, -var2])  # No pueden ser ambas verdaderas

            # Frame axioms: lo que no cambia persiste
            for prop in self._obtener_todas_proposiciones():  # Itera sobre todas las proposiciones
                var_actual = self._generar_variable(f"{prop}_{paso}")  # Variable para la proposición en el paso actual
                var_siguiente = self._generar_variable(f"{prop}_{paso+1}")  # Variable para la proposición en el siguiente paso

                # Generar cláusulas para persistencia
                # Si una acción que afecta esta prop ocurre, no necesitamos frame axiom
                acciones_que_afectan = [a for a in self.acciones if prop in a['efectos'] or f"-{prop}" in a['efectos']]  # Acciones que afectan esta proposición
                vars_acciones_afectan = [self._generar_variable(f"{a['nombre']}_{paso}") for a in acciones_que_afectan]  # Variables de las acciones que afectan

                if vars_acciones_afectan:  # Si hay acciones que afectan la proposición
                    # Si ninguna acción que afecta la prop ocurre, entonces persiste
                    clausulas.append([var_actual, -var_siguiente] + vars_acciones_afectan)  # Persistencia si no hay acción que afecte
                    clausulas.append([-var_actual, var_siguiente] + vars_acciones_afectan)  # Persistencia si no hay acción que afecte
                else:  # Si no hay acciones que afectan la proposición
                    # Si no hay acciones que afecten esta prop, debe persistir
                    clausulas.append([var_actual, -var_siguiente])  # Persistencia si no hay acciones que afecten
                    clausulas.append([-var_actual, var_siguiente])  # Persistencia si no hay acciones que afecten

        return clausulas  # Retorna las cláusulas SAT

    def resolver(self):  # Resuelve el problema de planificación usando un SAT solver.
        """Resuelve el problema de planificación usando un SAT solver."""
        clausulas = self._generar_codificacion_sat()  # Genera la codificación SAT

        try:  # Intenta resolver las cláusulas SAT
            solucion = pycosat.solve(clausulas)  # Llama al solver SAT
        except Exception as e:  # Captura cualquier error durante la resolución
            print(f"Error al resolver SAT: {e}")  # Imprime el error
            return None  # Retorna None si hay un error

        if isinstance(solucion, str) and solucion == "UNSAT":  # Si no se encuentra solución
            return None  # Retorna None si el problema es insatisfacible

        # Extraer el plan de la solución SAT
        plan = []  # Inicializa una lista vacía para el plan
        for paso in range(self.max_pasos):  # Itera sobre los pasos de tiempo
            for accion in self.acciones:  # Itera sobre las acciones
                var_accion = self.prop_a_var.get(f"{accion['nombre']}_{paso}")  # Obtiene la variable SAT de la acción
                if var_accion and var_accion in solucion:  # Si la variable de la acción es verdadera en la solución
                    plan.append(accion['nombre'])  # Añade el nombre de la acción al plan
                    break  # Pasa al siguiente paso
            else:
                pass # No se ejecutó ninguna acción en este paso

        return plan if plan else None  # Retorna el plan si no está vacío, sino None


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

    print("=== Problema de Planificación ===")  # Imprime el encabezado del problema
    print(f"Estado inicial: {estado_inicial}")  # Imprime el estado inicial
    print(f"Metas: {metas}")  # Imprime las metas
    print(f"Acciones disponibles: {[a['nombre'] for a in acciones]}")  # Imprime las acciones disponibles

    # Crear y ejecutar planificador
    print("\nEjecutando SATPLAN...")  # Imprime un mensaje de ejecución
    planificador = SATPLAN(acciones, estado_inicial, metas, max_pasos=5)  # Crea una instancia del planificador
    plan = planificador.resolver()  # Resuelve el problema de planificación

    # Mostrar resultados
    if plan:  # Si se encontró un plan
        print("\n¡Plan encontrado!")  # Imprime un mensaje de éxito
        for i, accion in enumerate(plan):  # Itera sobre las acciones del plan
            print(f"Paso {i}: {accion}")  # Imprime el paso y la acción
    else:  # Si no se encontró un plan
        print("\nNo se encontró un plan válido dentro del límite de pasos.")  # Imprime un mensaje de fallo
