from collections import defaultdict
from itertools import combinations

class FOIL:
    """Implementación del algoritmo FOIL (First Order Inductive Learner)"""
    
    def __init__(self, max_literales=4, min_cobertura=5):
        """
        Args:
            max_literales (int): Máximo de literales en cada cláusula
            min_cobertura (int): Mínimo de ejemplos positivos a cubrir
        """
        self.max_literales = max_literales
        self.min_cobertura = min_cobertura
        self.clausulas = []  # Almacena las cláusulas aprendidas
        
    def entrenar(self, ejemplos_pos, ejemplos_neg, relaciones, atributos):
        """
        Entrena el modelo FOIL con ejemplos y relaciones de fondo
        
        Args:
            ejemplos_pos (list): Ejemplos positivos (hechos objetivo)
            ejemplos_neg (list): Ejemplos negativos
            relaciones (dict): Diccionario de relaciones de fondo {nombre: [(hecho1), (hecho2)]}
            atributos (dict): Tipos y valores de los atributos {variable: tipo}
        """
        self.relaciones = relaciones
        self.atributos = atributos
        
        # Convertir ejemplos a formato de conjunto para búsquedas rápidas
        self.pos_set = set(ejemplos_pos)
        self.neg_set = set(ejemplos_neg)
        
        # Aprender cláusulas hasta cubrir todos los positivos
        while len(self.pos_set) > 0:
            clausula = self._aprender_clausula()
            if clausula is None:
                break  # No se pudo encontrar una cláusula válida
            self.clausulas.append(clausula)
            
            # Eliminar los ejemplos positivos cubiertos por esta cláusula
            cubiertos = set()
            for ejemplo in self.pos_set:
                if self._cubre(clausula, ejemplo):
                    cubiertos.add(ejemplo)
            self.pos_set -= cubiertos
            
            print(f"\nCláusula aprendida: {self._formatear_clausula(clausula)}")
            print(f"Cubre {len(cubiertos)} ejemplos positivos")
    
    def _aprender_clausula(self):
        """Aprende una nueva cláusula Horn"""
        # Inicializar con cabeza de cláusula (target)
        target = next(iter(self.pos_set)) if self.pos_set else None
        if not target:
            return None
            
        # Inicializar cláusula
        clausula = {
            'cabeza': target,
            'cuerpo': [],
            'variables': self._extraer_variables(target),
            'ejemplos_pos': set(self.pos_set),
            'ejemplos_neg': set(self.neg_set)
        }
        
        # Añadir literales hasta satisfacer criterios
        while len(clausula['cuerpo']) < self.max_literales:
            mejor_literal = None
            mejor_ganancia = -1
            mejores_ejemplos = None
            
            # Generar candidatos de literales
            literales_candidatos = self._generar_literales_candidatos(clausula)
            
            # Evaluar cada literal candidato
            for literal in literales_candidatos:
                ganancia, nuevos_pos, nuevos_neg = self._evaluar_literal(clausula, literal)
                if ganancia > mejor_ganancia:
                    mejor_ganancia = ganancia
                    mejor_literal = literal
                    mejores_ejemplos = (nuevos_pos, nuevos_neg)
            
            # Si no hay ganancia, terminar
            if mejor_literal is None or mejor_ganancia <= 0:
                break
                
            # Añadir el mejor literal a la cláusula
            clausula['cuerpo'].append(mejor_literal)
            clausula['ejemplos_pos'] = mejores_ejemplos[0]
            clausula['ejemplos_neg'] = mejores_ejemplos[1]
            
            # Actualizar variables en la cláusula
            clausula['variables'].update(self._extraer_variables(mejor_literal))
            
            # Si cubre muy pocos positivos, descartar
            if len(clausula['ejemplos_pos']) < self.min_cobertura:
                return None
        
        return clausula if len(clausula['ejemplos_neg']) == 0 else None
    
    def _generar_literales_candidatos(self, clausula):
        """Genera posibles literales para añadir al cuerpo de la cláusula"""
        candidatos = []
        vars_clausula = clausula['variables']
        
        # Literales con relaciones existentes
        for rel, hechos in self.relaciones.items():
            # Determinar aridad de la relación
            aridad = len(hechos[0]) if hechos else 0
            
            # Generar combinaciones de variables
            for vars_combo in combinations(vars_clausula.keys(), arity):
                # Crear nuevo literal
                nuevo_literal = (rel,) + tuple(vars_combo)
                candidatos.append(nuevo_literal)
        
        # Literales de igualdad entre variables
        for var1, var2 in combinations(vars_clausula.keys(), 2):
            if vars_clausula[var1] == vars_clausula[var2]:  # Mismo tipo
                candidatos.append(('=', var1, var2))
        
        return candidatos
    
    def _evaluar_literal(self, clausula, literal):
        """Evalúa un literal candidato usando la métrica FOIL-Gain"""
        nuevos_pos = set()
        nuevos_neg = set()
        
        # Filtrar ejemplos que satisfacen el nuevo literal
        for ejemplo in clausula['ejemplos_pos']:
            if self._satisface(ejemplo, clausula['variables'], literal):
                nuevos_pos.add(ejemplo)
                
        for ejemplo in clausula['ejemplos_neg']:
            if self._satisface(ejemplo, clausula['variables'], literal):
                nuevos_neg.add(ejemplo)
        
        # Calcular FOIL-Gain
        if not nuevos_pos:
            return -1, None, None
            
        t0 = len(clausula['ejemplos_pos'])
        t1 = len(nuevos_pos)
        p0 = len(clausula['ejemplos_pos']) - len(clausula['ejemplos_neg'])
        p1 = len(nuevos_pos) - len(nuevos_neg)
        
        ganancia = t1 * (np.log2(p1/t1) - np.log2(p0/t0)) if t1 > 0 else -1
        return ganancia, nuevos_pos, nuevos_neg
    
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
        cabeza_str = f"{clausula['cabeza'][0]}({','.join(clausula['cabeza'][1:])})"
        cuerpo_str = ", ".join(f"{lit[0]}({','.join(lit[1:])})" if len(lit) > 1 else lit[0] 
                          for lit in clausula['cuerpo'])
        return f"{cabeza_str} :- {cuerpo_str}" if cuerpo_str else cabeza_str
    
    def __str__(self):
        """Representación legible del modelo aprendido"""
        return "\n".join(self._formatear_clausula(c) for c in self.clausulas)

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
    foil = FOIL(max_literales=3, min_cobertura=2)
    foil.entrenar(ejemplos_pos, ejemplos_neg, relaciones, atributos)
    
    print("\n=== Modelo Final Aprendido ===")
    print(foil)