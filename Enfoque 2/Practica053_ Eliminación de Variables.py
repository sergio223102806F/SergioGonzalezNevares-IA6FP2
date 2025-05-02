from collections import defaultdict, OrderedDict
import itertools

class RedBayesianaVE:  # VE = Variable Elimination
    def __init__(self):
        """Inicializa la red bayesiana para eliminación de variables"""
        self.nodos = {}  # Diccionario de nodos {nombre: objeto Nodo}
        self.factores = defaultdict(dict)  # Almacena tablas de probabilidad condicional
    
    class Nodo:
        def __init__(self, nombre):
            """Inicializa un nodo de la red"""
            self.nombre = nombre
            self.padres = []  # Lista de nodos padres
    
    def agregar_nodo(self, nombre):
        """Añade un nodo a la red"""
        self.nodos[nombre] = self.Nodo(nombre)  # Crea y almacena el nodo
        return self.nodos[nombre]  # Devuelve el nodo creado
    
    def agregar_relacion(self, padre, hijo):
        """Establece una relación de dependencia entre nodos"""
        self.nodos[hijo].padres.append(self.nodos[padre])  # Añade padre al hijo
    
    def definir_probabilidad(self, nodo, prob_dict):
        """Define la tabla de probabilidad condicional para un nodo"""
        self.factores[nodo] = prob_dict  # Almacena P(nodo|padres)
    
    def eliminar_variable(self, factores, variable):
        """
        Elimina una variable marginalizando sobre sus valores
        
        Args:
            factores: Lista de factores actuales
            variable: Variable a eliminar
            
        Returns:
            Lista de nuevos factores después de eliminar la variable
        """
        nuevos_factores = []
        # Identificar factores que contienen la variable
        factores_relevantes = [f for f in factores if variable in f['variables']]
        
        if not factores_relevantes:
            return factores  # No hay factores que dependan de esta variable
            
        # Paso 1: Multiplicar factores que contienen la variable
        producto = {'variables': [], 'prob': {}}
        vars_comunes = set()  # Variables compartidas por los factores
        
        for f in factores_relevantes:
            vars_comunes.update(f['variables'])
            # Multiplicar probabilidades de los factores
            for asignacion, valor in f['prob'].items():
                if asignacion in producto['prob']:
                    producto['prob'][asignacion] *= valor
                else:
                    producto['prob'][asignacion] = valor
        
        # Variables restantes después de eliminar la variable objetivo
        vars_comunes.remove(variable)
        producto['variables'] = list(vars_comunes)
        
        # Paso 2: Sumar sobre la variable a eliminar (marginalización)
        nuevo_factor = {'variables': producto['variables'], 'prob': defaultdict(float)}
        
        for asignacion, valor in producto['prob'].items():
            # Crear nueva asignación sin la variable eliminada
            nueva_asignacion = tuple(v for v, var in zip(asignacion, producto['variables']) 
                                   if var != variable)
            nuevo_factor['prob'][nueva_asignacion] += valor
        
        # Conservar factores no afectados por la eliminación
        for f in factores:
            if variable not in f['variables']:
                nuevos_factores.append(f)
        
        nuevos_factores.append(nuevo_factor)
        return nuevos_factores
    
    def inferencia(self, consulta, evidencias={}, orden_eliminacion=None):
        """
        Realiza inferencia por eliminación de variables
        
        Args:
            consulta: Tupla (nodo, valor) que queremos calcular
            evidencias: Diccionario {nodo: valor} de variables observadas
            orden_eliminacion: Orden opcional para eliminar variables
            
        Returns:
            float: Probabilidad P(consulta|evidencias)
        """
        # Paso 1: Inicializar factores
        factores = []
        for nodo in self.nodos.values():
            # Variables involucradas en este factor (nodo + padres)
            vars_factor = [nodo.nombre] + [p.nombre for p in nodo.padres]
            prob = {}
            
            # Generar todas las combinaciones posibles de valores binarios
            valores_posibles = itertools.product(*[(True, False) for _ in vars_factor])
            
            for vals in valores_posibles:
                clave = dict(zip(vars_factor, vals))
                # Obtener P(nodo|padres) de la tabla de probabilidad
                prob[vals] = self.factores[nodo.nombre].get(
                    tuple(clave[p.nombre] for p in nodo.padres), {}).get(clave[nodo.nombre], 0)
            
            factores.append({'variables': vars_factor, 'prob': prob})
        
        # Paso 2: Aplicar evidencias (reducir factores)
        for nodo, valor in evidencias.items():
            nuevos_factores = []
            for f in factores:
                if nodo in f['variables']:
                    nuevo_prob = {}
                    idx = f['variables'].index(nodo)  # Índice de la variable evidencia
                    
                    # Filtrar asignaciones que coincidan con la evidencia
                    for asignacion, prob_val in f['prob'].items():
                        if asignacion[idx] == valor:
                            nueva_asign = tuple(v for i, v in enumerate(asignacion) 
                                         if i != idx)
                            nuevo_prob[nueva_asign] = prob_val
                    
                    # Actualizar factor reducido
                    f['prob'] = nuevo_prob
                    f['variables'].remove(nodo)
                
                # Conservar solo factores no vacíos
                if f['variables']:
                    nuevos_factores.append(f)
            
            factores = nuevos_factores
        
        # Paso 3: Determinar orden de eliminación (si no se proporciona)
        if orden_eliminacion is None:
            vars_restantes = set()
            for f in factores:
                vars_restantes.update(f['variables'])
            vars_restantes.discard(consulta[0])  # No eliminar la variable de consulta
            orden_eliminacion = list(vars_restantes)
        
        # Paso 4: Eliminar variables una por una
        for var in orden_eliminacion:
            factores = self.eliminar_variable(factores, var)
        
        # Paso 5: Calcular probabilidad final
        factor_final = factores[0]  # Debería quedar solo el factor de la consulta
        total = sum(factor_final['prob'].values())  # Probabilidad de la evidencia
        
        if total == 0:
            return 0.0  # Evitar división por cero
        
        # Calcular P(consulta,evidencias)
        prob = 0.0
        for asignacion, valor in factor_final['prob'].items():
            if asignacion[0] == consulta[1]:  # El primer elemento es la variable consulta
                prob += valor
        
        # Devolver P(consulta|evidencias) = P(consulta,evidencias)/P(evidencias)
        return prob / total

# Ejemplo: Sistema de alarma por robo
if __name__ == "__main__":
    print("=== Inferencia por Eliminación de Variables ===")
    rb = RedBayesianaVE()
    
    # 1. Crear nodos
    rb.agregar_nodo("Robo")
    rb.agregar_nodo("Terremoto")
    rb.agregar_nodo("Alarma")
    rb.agregar_nodo("JuanLlama")
    rb.agregar_nodo("MariaLlama")
    
    # 2. Definir estructura de dependencias
    rb.agregar_relacion("Robo", "Alarma")
    rb.agregar_relacion("Terremoto", "Alarma")
    rb.agregar_relacion("Alarma", "JuanLlama")
    rb.agregar_relacion("Alarma", "MariaLlama")
    
    # 3. Definir probabilidades condicionales
    
    # P(Robo) - Probabilidad marginal
    rb.definir_probabilidad("Robo", {(): {True: 0.001, False: 0.999}})
    
    # P(Terremoto) - Probabilidad marginal
    rb.definir_probabilidad("Terremoto", {(): {True: 0.002, False: 0.998}})
    
    # P(Alarma | Robo, Terremoto)
    rb.definir_probabilidad("Alarma", {
        (True, True): {True: 0.95, False: 0.05},
        (True, False): {True: 0.94, False: 0.06},
        (False, True): {True: 0.29, False: 0.71},
        (False, False): {True: 0.001, False: 0.999}
    })
    
    # P(JuanLlama | Alarma)
    rb.definir_probabilidad("JuanLlama", {
        (True,): {True: 0.9, False: 0.1},
        (False,): {True: 0.05, False: 0.95}
    })
    
    # P(MariaLlama | Alarma)
    rb.definir_probabilidad("MariaLlama", {
        (True,): {True: 0.7, False: 0.3},
        (False,): {True: 0.01, False: 0.99}
    })
    
    # 4. Realizar consulta: P(Robo=True | JuanLlama=True, MariaLlama=True)
    probabilidad = rb.inferencia(
        ("Robo", True),  # Consulta
        {"JuanLlama": True, "MariaLlama": True}  # Evidencias
    )
    
    # 5. Mostrar resultados
    print(f"\nProbabilidad de robo dado que Juan y María llaman:")
    print(f"P(Robo=True | JuanLlama=True, MariaLlama=True) = {probabilidad:.6f}")