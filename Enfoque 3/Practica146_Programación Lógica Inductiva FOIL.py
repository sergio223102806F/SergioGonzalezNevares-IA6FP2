from collections import defaultdict  # Importa defaultdict para crear diccionarios con valores por defecto
from itertools import combinations  # Importa combinations para generar combinaciones de elementos

class FOIL:
    """Implementación del algoritmo FOIL (First Order Inductive Learner)"""

    def __init__(self, max_literales=4, min_cobertura=5):
        """
        Args:
            max_literales (int): Máximo de literales en cada cláusula
            min_cobertura (int): Mínimo de ejemplos positivos a cubrir
        """
        self.max_literales = max_literales  # Inicializa el máximo número de literales por cláusula
        self.min_cobertura = min_cobertura  # Inicializa el mínimo número de ejemplos positivos que una cláusula debe cubrir
        self.clausulas = []  # Almacena las cláusulas aprendidas (reglas lógicas)

    def entrenar(self, ejemplos_pos, ejemplos_neg, relaciones, atributos):
        """
        Entrena el modelo FOIL con ejemplos y relaciones de fondo

        Args:
            ejemplos_pos (list): Ejemplos positivos (hechos objetivo)
            ejemplos_neg (list): Ejemplos negativos
            relaciones (dict): Diccionario de relaciones de fondo {nombre: [(hecho1), (hecho2)]}
            atributos (dict): Tipos y valores de los atributos {variable: tipo}
        """
        self.relaciones = relaciones  # Almacena las relaciones de fondo (conocimiento del dominio)
        self.atributos = atributos  # Almacena los tipos de los atributos (metadatos)

        # Convertir ejemplos a formato de conjunto para búsquedas rápidas
        self.pos_set = set(ejemplos_pos)  # Convierte los ejemplos positivos a un conjunto para operaciones eficientes
        self.neg_set = set(ejemplos_neg)  # Convierte los ejemplos negativos a un conjunto

        # Aprender cláusulas hasta cubrir todos los positivos
        while len(self.pos_set) > 0:  # Mientras queden ejemplos positivos por cubrir
            clausula = self._aprender_clausula()  # Aprende una nueva cláusula (regla)
            if clausula is None:
                break  # No se pudo encontrar una cláusula válida
            self.clausulas.append(clausula)  # Agrega la cláusula aprendida a la lista de cláusulas

            # Eliminar los ejemplos positivos cubiertos por esta cláusula
            cubiertos = set()  # Conjunto para almacenar los ejemplos positivos cubiertos por la cláusula actual
            for ejemplo in self.pos_set:  # Itera sobre los ejemplos positivos restantes
                if self._cubre(clausula, ejemplo):  # Si la cláusula cubre el ejemplo
                    cubiertos.add(ejemplo)  # Agrega el ejemplo al conjunto de ejemplos cubiertos
            self.pos_set -= cubiertos  # Elimina los ejemplos cubiertos del conjunto de ejemplos positivos

            print(f"\nCláusula aprendida: {self._formatear_clausula(clausula)}")  # Imprime la cláusula aprendida en un formato legible
            print(f"Cubre {len(cubiertos)} ejemplos positivos")  # Imprime el número de ejemplos positivos cubiertos por la cláusula

    def _aprender_clausula(self):
        """Aprende una nueva cláusula Horn"""
        # Inicializar con cabeza de cláusula (target)
        target = next(iter(self.pos_set)) if self.pos_set else None  # Selecciona el primer ejemplo positivo restante como cabeza de la cláusula
        if not target:
            return None  # Si no hay ejemplos positivos restantes, no se puede aprender una cláusula

        # Inicializar cláusula
        clausula = {
            'cabeza': target,  # La cabeza de la cláusula es el hecho objetivo que se quiere aprender
            'cuerpo': [],  # El cuerpo de la cláusula (inicialmente vacío) contiene las condiciones
            'variables': self._extraer_variables(target),  # Extrae las variables del hecho objetivo (cabeza)
            'ejemplos_pos': set(self.pos_set),  # Conjunto de ejemplos positivos que la cláusula debe cubrir
            'ejemplos_neg': set(self.neg_set)  # Conjunto de ejemplos negativos que la cláusula no debe cubrir
        }

        # Añadir literales hasta satisfacer criterios
        while len(clausula['cuerpo']) < self.max_literales:  # Mientras no se haya alcanzado el máximo de literales
            mejor_literal = None  # Inicializa el mejor literal encontrado hasta ahora
            mejor_ganancia = -1  # Inicializa la mejor ganancia (calidad) encontrada hasta ahora
            mejores_ejemplos = None  # Inicializa los mejores conjuntos de ejemplos positivos y negativos

            # Generar candidatos de literales
            literales_candidatos = self._generar_literales_candidatos(clausula)  # Genera posibles literales para añadir al cuerpo de la cláusula

            # Evaluar cada literal candidato
            for literal in literales_candidatos:  # Itera sobre cada literal candidato
                ganancia, nuevos_pos, nuevos_neg = self._evaluar_literal(clausula, literal)  # Evalúa el literal usando FOIL-Gain
                if ganancia > mejor_ganancia:  # Si la ganancia es mejor que la mejor ganancia encontrada hasta ahora
                    mejor_ganancia = ganancia  # Actualiza la mejor ganancia
                    mejor_literal = literal  # Actualiza el mejor literal
                    mejores_ejemplos = (nuevos_pos, nuevos_neg)  # Actualiza los mejores conjuntos de ejemplos

            # Si no hay ganancia, terminar
            if mejor_literal is None or mejor_ganancia <= 0:  # Si no se encontró un literal que mejore la cláusula
                break  # Termina la búsqueda de literales para esta cláusula

            # Añadir el mejor literal a la cláusula
            clausula['cuerpo'].append(mejor_literal)  # Agrega el mejor literal al cuerpo de la cláusula
            clausula['ejemplos_pos'] = mejores_ejemplos[0]  # Actualiza los ejemplos positivos cubiertos por la cláusula
            clausula['ejemplos_neg'] = mejores_ejemplos[1]  # Actualiza los ejemplos negativos cubiertos por la cláusula

            # Actualizar variables en la cláusula
            clausula['variables'].update(self._extraer_variables(mejor_literal))  # Actualiza el conjunto de variables presentes en la cláusula

            # Si cubre muy pocos positivos, descartar
            if len(clausula['ejemplos_pos']) < self.min_cobertura:  # Si la cláusula cubre menos ejemplos positivos que el mínimo requerido
                return None  # Descarta la cláusula (no es suficientemente general)

        return clausula if len(clausula['ejemplos_neg']) == 0 else None  # Devuelve la cláusula si no cubre ningún ejemplo negativo, de lo contrario devuelve None

    def _generar_literales_candidatos(self, clausula):
        """Genera posibles literales para añadir al cuerpo de la cláusula"""
        candidatos = []  # Lista para almacenar los literales candidatos
        vars_clausula = clausula['variables']  # Variables presentes en la cláusula actual

        # Literales con relaciones existentes
        for rel, hechos in self.relaciones.items():  # Itera sobre las relaciones de fondo
            # Determinar aridad de la relación
            aridad = len(hechos[0]) if hechos else 0  # Obtiene la aridad (número de argumentos) de la relación

            # Generar combinaciones de variables
            for vars_combo in combinations(vars_clausula.keys(), aridad):  # Genera todas las combinaciones posibles de variables con la aridad de la relación
                # Crear nuevo literal
                nuevo_literal = (rel,) + tuple(vars_combo)  # Crea un nuevo literal con el nombre de la relación y la combinación de variables
                candidatos.append(nuevo_literal)  # Agrega el literal candidato a la lista

        # Literales de igualdad entre variables
        for var1, var2 in combinations(vars_clausula.keys(), 2):  # Genera todas las combinaciones posibles de 2 variables
            if vars_clausula[var1] == vars_clausula[var2]:  # Mismo tipo
                candidatos.append(('=', var1, var2))  # Agrega un literal de igualdad entre las variables
        return candidatos  # Devuelve la lista de literales candidatos

    def _evaluar_literal(self, clausula, literal):
        """Evalúa un literal candidato usando la métrica FOIL-Gain"""
        nuevos_pos = set()  # Conjunto para almacenar los ejemplos positivos cubiertos por la cláusula con el nuevo literal
        nuevos_neg = set()  # Conjunto para almacenar los ejemplos negativos cubiertos por la cláusula con el nuevo literal

        # Filtrar ejemplos que satisfacen el nuevo literal
        for ejemplo in clausula['ejemplos_pos']:  # Itera sobre los ejemplos positivos cubiertos por la cláusula actual
            if self._satisface(ejemplo, clausula['variables'], literal):  # Si el ejemplo satisface el literal
                nuevos_pos.add(ejemplo)  # Agrega el ejemplo a los nuevos ejemplos positivos

        for ejemplo in clausula['ejemplos_neg']:  # Itera sobre los ejemplos negativos cubiertos por la cláusula actual
            if self._satisface(ejemplo, clausula['variables'], literal):  # Si el ejemplo satisface el literal
                nuevos_neg.add(ejemplo)  # Agrega el ejemplo a los nuevos ejemplos negativos

        # Calcular FOIL-Gain
        if not nuevos_pos:
            return -1, None, None  # Si no cubre ningún ejemplo positivo, la ganancia es -1

        t0 = len(clausula['ejemplos_pos'])  # Número de ejemplos positivos cubiertos por la cláusula antes de añadir el literal
        t1 = len(nuevos_pos)  # Número de ejemplos positivos cubiertos por la cláusula después de añadir el literal
        p0 = len(clausula['ejemplos_pos']) - len(clausula['ejemplos_neg'])  # Precisión de la cláusula antes de añadir el literal
        p1 = len(nuevos_pos) - len(nuevos_neg)  # Precisión de la cláusula después de añadir el literal

        ganancia = t1 * (np.log2(p1/t1) - np.log2(p0/t0)) if t1 > 0 else -1  # Calcula la ganancia de información de FOIL
        return ganancia, nuevos_pos, nuevos_neg  # Devuelve la ganancia y los nuevos conjuntos de ejemplos

    def _satisface(self, ejemplo, variables, literal):
        """Verifica si un ejemplo satisface un literal con variables"""
        # Implementación simplificada (en realidad necesitarías unificación)
        # Esta es una versión muy simplificada para el ejemplo
        return True  # En una implementación real, harías unificación lógica aquí

    def _cubre(self, clausula, ejemplo):
        """Determina si una cláusula cubre un ejemplo"""
        # Verificación simplificada
        return ejemplo == clausula['cabeza']  # En realidad necesitarías resolución lógica

    def _formatear_clausula(self, clausula):
        """Formatea una cláusula para visualización"""
        cabeza_str = f"{clausula['cabeza'][0]}({','.join(clausula['cabeza'][1:])})"  # Formatea la cabeza de la cláusula
        cuerpo_str = ", ".join(f"{lit[0]}({','.join(lit[1:])})" if len(lit) > 1 else lit[0]
                                 for lit in clausula['cuerpo'])  # Formatea el cuerpo de la cláusula
        return f"{cabeza_str} :- {cuerpo_str}" if cuerpo_str else cabeza_str  # Devuelve la cláusula formateada en notación lógica

    def __str__(self):
        """Representación legible del modelo aprendido"""
        return "\n".join(self._formatear_clausula(c) for c in self.clausulas)  # Devuelve una representación en cadena de todas las cláusulas aprendidas

# ==================== Ejemplo de Uso ====================
if __name__ == "__main__":
    print("=== Ejemplo FOIL: Aprender relación 'abuelo' ===")

    # Relaciones de fondo (knowledge base)
    relaciones = {
        'padre': [('juan', 'pedro'), ('pedro', 'carlos'), ('pedro', 'maria'),
                  ('manuel', 'jorge'), ('jorge', 'diego')],
        'madre': [('ana', 'pedro'), ('luisa', 'carlos'), ('luisa', 'maria'),
                  ('rosa', 'jorge'), ('clara', 'diego')]
    }

    # Ejemplos positivos y negativos
    ejemplos_pos = [('abuelo', 'juan', 'carlos'), ('abuelo', 'juan', 'maria'),
                    ('abuelo', 'manuel', 'diego')]
    ejemplos_neg = [('abuelo', 'juan', 'pedro'), ('abuelo', 'pedro', 'carlos'),
                    ('abuelo', 'ana', 'maria'), ('abuelo', 'rosa', 'diego')]

    # Atributos/variables
    atributos = {'X': 'persona', 'Y': 'persona', 'Z': 'persona'}

    # Crear y entrenar FOIL
    foil = FOIL(max_literales=3, min_cobertura=2)  # Crea una instancia del algoritmo FOIL
    foil.entrenar(ejemplos_pos, ejemplos_neg, relaciones, atributos)  # Entrena el modelo FOIL

    print("\n=== Modelo Final Aprendido ===")
    print(foil)  # Imprime el modelo aprendido (las cláusulas lógicas)
