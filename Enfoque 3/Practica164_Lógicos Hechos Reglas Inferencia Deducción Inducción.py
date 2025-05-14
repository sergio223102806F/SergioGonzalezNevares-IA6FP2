# =============================================
# SISTEMA LÓGICO EN PYTHON
# =============================================

class SistemaLogico:
    def __init__(self):
        # Base de conocimiento: hechos y reglas
        self.hechos = set()  # Inicializa un conjunto para almacenar hechos únicos
        self.reglas = []  # Inicializa una lista para almacenar reglas (antecedente, consecuente)

    # ----------------------------
    # 1. HECHOS (Facts)
    # ----------------------------
    def agregar_hecho(self, hecho):
        """Añade un hecho a la base de conocimiento"""
        self.hechos.add(hecho)  # Agrega el hecho al conjunto de hechos

    def verificar_hecho(self, hecho):
        """Comprueba si un hecho es conocido"""
        return hecho in self.hechos  # Verifica si el hecho está en el conjunto de hechos

    # ----------------------------
    # 2. REGLAS (Rules)
    # ----------------------------
    def agregar_regla(self, antecedente, consecuente):
        """Añade una regla: Si antecedente entonces consecuente"""
        self.reglas.append((antecedente, consecuente))  # Agrega la regla a la lista de reglas

    # ----------------------------
    # 3. INFERENCIA (Forward Chaining)
    # ----------------------------
    def inferir(self):
        """Motor de inferencia: encadenamiento hacia adelante"""
        nuevos_hechos = True  # Inicializa la bandera para controlar el bucle
        while nuevos_hechos:
            nuevos_hechos = False  # Asume que no hay nuevos hechos en esta iteración
            for antecedente, consecuente in self.reglas:  # Itera sobre cada regla
                if self.verificar_hecho(antecedente) and not self.verificar_hecho(consecuente):  # Si el antecedente es conocido y el consecuente no
                    self.agregar_hecho(consecuente)  # Agrega el consecuente a los hechos conocidos
                    nuevos_hechos = True  # Marca que se agregó un nuevo hecho, para continuar el bucle
                    
    # ----------------------------
    # 4. DEDUCCIÓN (Backward Chaining)
    # ----------------------------
    def deducir(self, objetivo):
        """Encadenamiento hacia atrás para deducir un objetivo"""
        if self.verificar_hecho(objetivo):  # Si el objetivo es un hecho conocido, devuelve verdadero
            return True
        
        for antecedente, consecuente in self.reglas:  # Itera sobre las reglas
            if consecuente == objetivo:  # Si el consecuente de la regla es el objetivo
                if self.deducir(antecedente):  # Intenta deducir el antecedente de la regla recursivamente
                    return True  # Si el antecedente se deduce, el objetivo también se deduce
        return False  # Si no se encuentra una regla que deduzca el objetivo, o no se puede deducir su antecedente, devuelve falso

    # ----------------------------
    # 5. INDUCCIÓN (Aprendizaje de reglas)
    # ----------------------------
    def inducir_regla(self, ejemplos_positivos, ejemplos_negativos):
        """Induce una regla general a partir de ejemplos"""
        # Implementación simplificada
        for hecho in ejemplos_positivos:  # Itera sobre los ejemplos positivos
            if hecho not in ejemplos_negativos:  # Si el ejemplo positivo no está en los ejemplos negativos
                # Aquí iría un algoritmo de aprendizaje más sofisticado
                # Esta es una versión simplificada
                return f"Si X entonces {hecho}"  # Devuelve una regla simplificada
        return "No se pudo inducir una regla"  # Si no se puede inducir una regla, devuelve un mensaje

# =============================================
# EJEMPLO PRÁCTICO: SISTEMA EXPERTO
# =============================================
if __name__ == "__main__":
    sistema = SistemaLogico()  # Crea una instancia del sistema lógico

    # 1. Agregar hechos básicos
    sistema.agregar_hecho("pájaros_vuelan")
    sistema.agregar_hecho("pinguino_es_pajaro")

    # 2. Agregar reglas
    sistema.agregar_regla("pajaro", "vuela")  # Si es pájaro entonces vuela
    sistema.agregar_regla("pinguino_es_pajaro", "pajaro")  # Los pingüinos son pájaros
    sistema.agregar_regla("pinguino", "no_vuela")  # Pero los pingüinos no vuelan

    # 3. Inferencia (Forward Chaining)
    print("\n=== INFERENCIA ===")
    sistema.inferir()  # Ejecuta el motor de inferencia hacia adelante
    print("Hechos conocidos:", sistema.hechos)  # Imprime los hechos conocidos después de la inferencia

    # 4. Deducción (Backward Chaining)
    print("\n=== DEDUCCIÓN ===")
    objetivo = "vuela"
    print(f"¿'{objetivo}' es verdadero? {sistema.deducir(objetivo)}")  # Intenta deducir si "vuela" es verdadero

    # 5. Inducción (Aprendizaje)
    print("\n=== INDUCCIÓN ===")
    ejemplos_positivos = ["pajaro_vuela", "insecto_vuela"]
    ejemplos_negativos = ["pinguino_no_vuela", "pez_no_vuela"]
    regla_inducida = sistema.inducir_regla(ejemplos_positivos, ejemplos_negativos)  # Induce una regla a partir de los ejemplos
    print("Regla inducida:", regla_inducida)  # Imprime la regla inducida

