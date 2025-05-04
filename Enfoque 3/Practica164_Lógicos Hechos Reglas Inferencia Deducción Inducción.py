# =============================================
# SISTEMA LÓGICO EN PYTHON
# =============================================

class SistemaLogico:
    def __init__(self):
        # Base de conocimiento: hechos y reglas
        self.hechos = set()
        self.reglas = []

    # ----------------------------
    # 1. HECHOS (Facts)
    # ----------------------------
    def agregar_hecho(self, hecho):
        """Añade un hecho a la base de conocimiento"""
        self.hechos.add(hecho)

    def verificar_hecho(self, hecho):
        """Comprueba si un hecho es conocido"""
        return hecho in self.hechos

    # ----------------------------
    # 2. REGLAS (Rules)
    # ----------------------------
    def agregar_regla(self, antecedente, consecuente):
        """Añade una regla: Si antecedente entonces consecuente"""
        self.reglas.append((antecedente, consecuente))

    # ----------------------------
    # 3. INFERENCIA (Forward Chaining)
    # ----------------------------
    def inferir(self):
        """Motor de inferencia: encadenamiento hacia adelante"""
        nuevos_hechos = True
        while nuevos_hechos:
            nuevos_hechos = False
            for antecedente, consecuente in self.reglas:
                if self.verificar_hecho(antecedente) and not self.verificar_hecho(consecuente):
                    self.agregar_hecho(consecuente)
                    nuevos_hechos = True

    # ----------------------------
    # 4. DEDUCCIÓN (Backward Chaining)
    # ----------------------------
    def deducir(self, objetivo):
        """Encadenamiento hacia atrás para deducir un objetivo"""
        if self.verificar_hecho(objetivo):
            return True
        
        for antecedente, consecuente in self.reglas:
            if consecuente == objetivo:
                if self.deducir(antecedente):
                    return True
        return False

    # ----------------------------
    # 5. INDUCCIÓN (Aprendizaje de reglas)
    # ----------------------------
    def inducir_regla(self, ejemplos_positivos, ejemplos_negativos):
        """Induce una regla general a partir de ejemplos"""
        # Implementación simplificada
        for hecho in ejemplos_positivos:
            if hecho not in ejemplos_negativos:
                # Aquí iría un algoritmo de aprendizaje más sofisticado
                # Esta es una versión simplificada
                return f"Si X entonces {hecho}"
        return "No se pudo inducir una regla"

# =============================================
# EJEMPLO PRÁCTICO: SISTEMA EXPERTO
# =============================================
if __name__ == "__main__":
    sistema = SistemaLogico()

    # 1. Agregar hechos básicos
    sistema.agregar_hecho("pájaros_vuelan")
    sistema.agregar_hecho("pinguino_es_pajaro")

    # 2. Agregar reglas
    sistema.agregar_regla("pajaro", "vuela")  # Si es pájaro entonces vuela
    sistema.agregar_regla("pinguino_es_pajaro", "pajaro")  # Los pingüinos son pájaros
    sistema.agregar_regla("pinguino", "no_vuela")  # Pero los pingüinos no vuelan

    # 3. Inferencia (Forward Chaining)
    print("\n=== INFERENCIA ===")
    sistema.inferir()
    print("Hechos conocidos:", sistema.hechos)  # Debería incluir "pajaro" y "vuela"

    # 4. Deducción (Backward Chaining)
    print("\n=== DEDUCCIÓN ===")
    objetivo = "vuela"
    print(f"¿'{objetivo}' es verdadero? {sistema.deducir(objetivo)}")

    # 5. Inducción (Aprendizaje)
    print("\n=== INDUCCIÓN ===")
    ejemplos_positivos = ["pajaro_vuela", "insecto_vuela"]
    ejemplos_negativos = ["pinguino_no_vuela", "pez_no_vuela"]
    regla_inducida = sistema.inducir_regla(ejemplos_positivos, ejemplos_negativos)
    print("Regla inducida:", regla_inducida)
