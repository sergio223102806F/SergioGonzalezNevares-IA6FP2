# Importación de librerías necesarias
from collections import defaultdict  # Para diccionarios con valores por defecto
import itertools  # Para generar combinaciones de valores

class RedBayesiana:
    def __init__(self):
        """Inicializa la red bayesiana vacía"""
        self.nodos = {}  # Diccionario {nombre: Nodo} para almacenar nodos
        self.estructura = defaultdict(list)  # Diccionario {padre: [hijos]} para estructura de la red
    
    class Nodo:
        def __init__(self, nombre):
            """Inicializa un nodo de la red"""
            self.nombre = nombre  # Nombre identificador del nodo
            self.padres = []  # Lista de nodos padres
            self.tabla_prob = {}  # Tabla de probabilidades condicionales {(val_padres): prob}
    
    def agregar_nodo(self, nombre):
        """Añade un nuevo nodo a la red"""
        self.nodos[nombre] = self.Nodo(nombre)  # Crea y almacena el nodo
        return self.nodos[nombre]  # Devuelve el nodo creado
    
    def agregar_relacion(self, padre, hijo):
        """Establece una relación de dependencia entre nodos"""
        self.nodos[hijo].padres.append(self.nodos[padre])  # Añade padre al hijo
        self.estructura[padre].append(hijo)  # Registra la relación en la estructura
    
    def definir_probabilidad(self, nodo, prob_dict):
        """Define la tabla de probabilidad condicional para un nodo"""
        self.nodos[nodo].tabla_prob = prob_dict  # Asigna la tabla de probabilidades
    
    def inferencia_por_enumeracion(self, consulta, evidencias={}):
        """
        Realiza inferencia por enumeración completa
        
        Args:
            consulta: Tupla (nodo, valor) que queremos calcular
            evidencias: Diccionario {nodo: valor} de variables observadas
            
        Returns:
            float: Probabilidad P(consulta|evidencias)
        """
        # Obtener nodos en orden topológico (padres antes que hijos)
        nodos_ordenados = self.orden_topologico()
        
        # Identificar variables ocultas (no consulta ni evidencias)
        ocultos = [n for n in nodos_ordenados 
                  if n != consulta[0] and n not in evidencias]
        
        # Inicializar acumuladores de probabilidad
        prob = 0.0  # Acumulador para P(consulta,evidencias)
        prob_normalizacion = 0.0  # Acumulador para P(evidencias)
        
        # Generar todas las combinaciones posibles de variables ocultas
        valores_posibles = {n: [True, False] for n in ocultos}  # Valores binarios
        combinaciones = itertools.product(*[valores_posibles[n] for n in ocultos])
        
        # Evaluar cada combinación posible
        for combo in combinaciones:
            # Crear instancia completa de variables
            instancia = dict(zip(ocultos, combo))  # Asigna valores a ocultos
            instancia.update(evidencias)  # Añade evidencias
            instancia[consulta[0]] = consulta[1]  # Añade valor de consulta
            
            # Calcular probabilidad conjunta para esta instancia
            prob_conjunta = 1.0  # Inicializar probabilidad conjunta
            
            for nodo in nodos_ordenados:
                nodo_obj = self.nodos[nodo]
                valor = instancia[nodo]  # Valor actual del nodo
                
                if not nodo_obj.padres:
                    # Nodo sin padres: usar probabilidad marginal
                    prob_conjunta *= nodo_obj.tabla_prob.get(valor, 0)
                else:
                    # Nodo con padres: usar probabilidad condicional
                    padres_vals = tuple(instancia[p.nombre] for p in nodo_obj.padres)
                    prob_conjunta *= nodo_obj.tabla_prob.get(padres_vals, {}).get(valor, 0)
            
            # Acumular según si coincide con la consulta
            if consulta[1] == instancia[consulta[0]]:
                prob += prob_conjunta
            prob_normalizacion += prob_conjunta
        
        # Devolver probabilidad condicional normalizada
        return prob / prob_normalizacion if prob_normalizacion != 0 else 0
    
    def orden_topologico(self):
        """Devuelve los nodos en orden topológico (padres antes de hijos)"""
        visitados = set()  # Nodos ya procesados
        orden = []  # Resultado del ordenamiento
        
        def dfs(nodo):
            """Recorrido en profundidad para orden topológico"""
            if nodo not in visitados:
                visitados.add(nodo)
                for hijo in self.estructura[nodo]:
                    dfs(hijo)
                orden.append(nodo)
        
        # Aplicar DFS a cada nodo no visitado
        for nodo in self.nodos:
            if nodo not in visitados:
                dfs(nodo)
        
        return orden[::-1]  # Invertir para obtener el orden correcto

# Ejemplo de uso: Sistema de alarma por robo
if __name__ == "__main__":
    print("=== Inferencia por Enumeración en Red Bayesiana ===")
    rb = RedBayesiana()
    
    # 1. Crear nodos de la red
    rb.agregar_nodo("Robo")  # Nodo para robo
    rb.agregar_nodo("Terremoto")  # Nodo para terremoto
    rb.agregar_nodo("Alarma")  # Nodo para alarma
    rb.agregar_nodo("JuanLlama")  # Nodo para Juan llama
    rb.agregar_nodo("MariaLlama")  # Nodo para María llama
    
    # 2. Definir estructura de dependencias
    rb.agregar_relacion("Robo", "Alarma")  # Robo afecta a Alarma
    rb.agregar_relacion("Terremoto", "Alarma")  # Terremoto afecta a Alarma
    rb.agregar_relacion("Alarma", "JuanLlama")  # Alarma afecta a JuanLlama
    rb.agregar_relacion("Alarma", "MariaLlama")  # Alarma afecta a MariaLlama
    
    # 3. Definir probabilidades condicionales
    
    # Probabilidades marginales P(Robo)
    rb.definir_probabilidad("Robo", {True: 0.001, False: 0.999})
    
    # Probabilidades marginales P(Terremoto)
    rb.definir_probabilidad("Terremoto", {True: 0.002, False: 0.998})
    
    # Tabla P(Alarma | Robo, Terremoto)
    rb.definir_probabilidad("Alarma", {
        (True, True): 0.95,    # Robo y Terremoto: alta probabilidad
        (True, False): 0.94,   # Solo Robo: probabilidad alta
        (False, True): 0.29,   # Solo Terremoto: probabilidad media
        (False, False): 0.001  # Ninguno: probabilidad muy baja
    })
    
    # Tabla P(JuanLlama | Alarma)
    rb.definir_probabilidad("JuanLlama", {True: 0.9, False: 0.1})
    
    # Tabla P(MariaLlama | Alarma)
    rb.definir_probabilidad("MariaLlama", {True: 0.7, False: 0.3})
    
    # 4. Realizar consulta de inferencia
    # P(Robo=True | JuanLlama=True, MariaLlama=True)
    probabilidad = rb.inferencia_por_enumeracion(
        ("Robo", True),  # Consulta: Robo=True
        {"JuanLlama": True, "MariaLlama": True}  # Evidencias
    )
    
    # 5. Mostrar resultados
    print(f"\nProbabilidad de robo dado que Juan y María llaman:")
    print(f"P(Robo=True | JuanLlama=True, MariaLlama=True) = {probabilidad:.6f}")

