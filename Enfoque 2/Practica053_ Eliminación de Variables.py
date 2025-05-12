from collections import defaultdict, OrderedDict  # Importa estructuras de datos especializadas
import itertools                                 # Importa herramientas para combinaciones

class RedBayesianaVE:                            # Clase para Red Bayesiana con Eliminación de Variables
    def __init__(self):
        """Constructor que inicializa la red bayesiana"""
        self.nodos = {}                          # Diccionario de nodos {nombre: objeto Nodo}
        self.factores = defaultdict(dict)        # Almacena tablas de probabilidad condicional
    
    class Nodo:
        def __init__(self, nombre):
            """Inicializa un nodo de la red:
            nombre: Identificador del nodo
            """
            self.nombre = nombre                 # Nombre del nodo
            self.padres = []                     # Lista de nodos padres (inicialmente vacía)
    
    def agregar_nodo(self, nombre):
        """Añade un nodo a la red:
        nombre: Identificador del nuevo nodo
        """
        self.nodos[nombre] = self.Nodo(nombre)   # Crea y almacena el nodo
        return self.nodos[nombre]                # Devuelve el nodo creado
    
    def agregar_relacion(self, padre, hijo):
        """Establece una relación padre-hijo entre nodos:
        padre: Nombre del nodo padre
        hijo: Nombre del nodo hijo
        """
        self.nodos[hijo].padres.append(self.nodos[padre])  # Añade padre a la lista del hijo
    
    def definir_probabilidad(self, nodo, prob_dict):
        """Define la tabla de probabilidad condicional para un nodo:
        nodo: Nombre del nodo
        prob_dict: Diccionario con probabilidades P(nodo|padres)
        """
        self.factores[nodo] = prob_dict          # Almacena la tabla de probabilidad
    
    def eliminar_variable(self, factores, variable):
        """
        Elimina una variable marginalizando sobre sus valores:
        factores: Lista de factores actuales
        variable: Variable a eliminar
        """
        nuevos_factores = []                     # Lista para factores resultantes
        
        # Identificar factores que contienen la variable
        factores_relevantes = [f for f in factores if variable in f['variables']]
        
        if not factores_relevantes:              # Si no hay factores relevantes
            return factores                      # Retorna factores sin cambios
            
        # Paso 1: Multiplicar factores que contienen la variable
        producto = {'variables': [], 'prob': {}} # Factor producto
        vars_comunes = set()                     # Variables compartidas
        
        for f in factores_relevantes:            # Para cada factor relevante
            vars_comunes.update(f['variables'])  # Acumula variables
            # Multiplica probabilidades
            for asignacion, valor in f['prob'].items():
                if asignacion in producto['prob']:
                    producto['prob'][asignacion] *= valor
                else:
                    producto['prob'][asignacion] = val
        
        # Variables restantes después de eliminar la variable objetivo
        vars_comunes.remove(variable)
        producto['variables'] = list(vars_comunes)
        
        # Paso 2: Sumar sobre la variable (marginalización)
        nuevo_factor = {'variables': producto['variables'], 'prob': defaultdict(float)}
        
        for asignacion, valor in producto['prob'].items():
            # Nueva asignación sin la variable eliminada
            nueva_asignacion = tuple(v for v, var in zip(asignacion, producto['variables']) 
                                   if var != variable)
            nuevo_factor['prob'][nueva_asignacion] += valor
        
        # Conservar factores no afectados
        for f in factores:
            if variable not in f['variables']:
                nuevos_factores.append(f)
        
        nuevos_factores.append(nuevo_factor)     # Añade el nuevo factor
        return nuevos_factores                   # Retorna factores actualizados
    
    def inferencia(self, consulta, evidencias={}, orden_eliminacion=None):
        """
        Realiza inferencia por eliminación de variables:
        consulta: Tupla (nodo, valor) a calcular
        evidencias: Diccionario {nodo: valor} observado
        orden_eliminacion: Orden opcional para eliminar variables
        """
        # Paso 1: Inicializar factores
        factores = []                            # Lista de factores iniciales
        
        for nodo in self.nodos.values():         # Para cada nodo en la red
            # Variables en este factor (nodo + padres)
            vars_factor = [nodo.nombre] + [p.nombre for p in nodo.padres]
            prob = {}                            # Diccionario de probabilidades
            
            # Generar todas las combinaciones de valores binarios
            valores_posibles = itertools.product(*[(True, False) for _ in vars_factor])
            
            for vals in valores_posibles:        # Para cada combinación
                clave = dict(zip(vars_factor, vals))
                # Obtener P(nodo|padres) de la tabla
                prob[vals] = self.factores[nodo.nombre].get(
                    tuple(clave[p.nombre] for p in nodo.padres), {}).get(clave[nodo.nombre], 0)
            
            factores.append({'variables': vars_factor, 'prob': prob})
        
        # Paso 2: Aplicar evidencias (reducir factores)
        for nodo, valor in evidencias.items():   # Para cada evidencia
            nuevos_factores = []                 # Factores actualizados
            
            for f in factores:                   # Para cada factor
                if nodo in f['variables']:       # Si el factor contiene la evidencia
                    nuevo_prob = {}              # Nuevas probabilidades
                    idx = f['variables'].index(nodo)  # Índice de la evidencia
                    
                    # Filtrar asignaciones consistentes con la evidencia
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
            
            factores = nuevos_factores           # Actualizar lista de factores
        
        # Paso 3: Determinar orden de eliminación (si no se proporciona)
        if orden_eliminacion is None:
            vars_restantes = set()               # Variables por eliminar
            for f in factores:
                vars_restantes.update(f['variables'])
            vars_restantes.discard(consulta[0])  # Conservar variable de consulta
            orden_eliminacion = list(vars_restantes)
        
        # Paso 4: Eliminar variables una por una
        for var in orden_eliminacion:            # Eliminar en orden especificado
            factores = self.eliminar_variable(factores, var)
        
        # Paso 5: Calcular probabilidad final
        factor_final = factores[0]               # Factor resultante (solo consulta)
        total = sum(factor_final['prob'].values())  # Probabilidad de la evidencia
        
        if total == 0:                           # Evitar división por cero
            return 0.0
        
        # Calcular P(consulta,evidencias)
        prob = 0.0
        for asignacion, valor in factor_final['prob'].items():
            if asignacion[0] == consulta[1]:     # Coincide con valor de consulta
                prob += valor
        
        # Retornar P(consulta|evidencias) = P(consulta,evidencias)/P(evidencias)
        return prob / total

# Ejemplo: Sistema de alarma por robo
if __name__ == "__main__":
    print("=== Inferencia por Eliminación de Variables ===")
    rb = RedBayesianaVE()                        # Crea instancia de red bayesiana
    
    # 1. Crear nodos de la red
    rb.agregar_nodo("Robo")                      # Nodo Robo
    rb.agregar_nodo("Terremoto")                 # Nodo Terremoto
    rb.agregar_nodo("Alarma")                    # Nodo Alarma
    rb.agregar_nodo("JuanLlama")                 # Nodo JuanLlama
    rb.agregar_nodo("MariaLlama")                # Nodo MariaLlama
    
    # 2. Definir estructura de dependencias
    rb.agregar_relacion("Robo", "Alarma")        # Robo -> Alarma
    rb.agregar_relacion("Terremoto", "Alarma")   # Terremoto -> Alarma
    rb.agregar_relacion("Alarma", "JuanLlama")   # Alarma -> JuanLlama
    rb.agregar_relacion("Alarma", "MariaLlama")  # Alarma -> MariaLlama
    
    # 3. Definir probabilidades condicionales
    
    # P(Robo) - Probabilidad marginal
    rb.definir_probabilidad("Robo", {(): {True: 0.001, False: 0.999}})
    
    # P(Terremoto) - Probabilidad marginal
    rb.definir_probabilidad("Terremoto", {(): {True: 0.002, False: 0.998}})
    
    # P(Alarma | Robo, Terremoto)
    rb.definir_probabilidad("Alarma", {
        (True, True): {True: 0.95, False: 0.05},    # Robo y Terremoto
        (True, False): {True: 0.94, False: 0.06},   # Solo Robo
        (False, True): {True: 0.29, False: 0.71},   # Solo Terremoto
        (False, False): {True: 0.001, False: 0.999} # Ninguno
    })
    
    # P(JuanLlama | Alarma)
    rb.definir_probabilidad("JuanLlama", {
        (True,): {True: 0.9, False: 0.1},    # Alarma activada
        (False,): {True: 0.05, False: 0.95}  # Alarma no activada
    })
    
    # P(MariaLlama | Alarma)
    rb.definir_probabilidad("MariaLlama", {
        (True,): {True: 0.7, False: 0.3},    # Alarma activada
        (False,): {True: 0.01, False: 0.99}  # Alarma no activada
    })
    
    # 4. Realizar consulta: P(Robo=True | JuanLlama=True, MariaLlama=True)
    probabilidad = rb.inferencia(
        ("Robo", True),                      # Probabilidad de robo
        {"JuanLlama": True, "MariaLlama": True}  # Evidencias observadas
    )
    
    # 5. Mostrar resultados
    print(f"\nProbabilidad de robo dado que Juan y María llaman:")
    print(f"P(Robo=True | JuanLlama=True, MariaLlama=True) = {probabilidad:.6f}")