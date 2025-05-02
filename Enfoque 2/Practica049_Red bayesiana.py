

# Importación de librería para diccionarios con valores por defecto
from collections import defaultdict

class NodoBayesiano:
    def __init__(self, nombre):
        """Constructor de nodo bayesiano
        
        Args:
            nombre (str): Nombre identificador del nodo
        """
        self.nombre = nombre  # Almacena el nombre del nodo
        self.padres = []  # Lista para almacenar nodos padres
        self.tabla_prob = {}  # Diccionario para probabilidades condicionales P(X|padres)
    
    def agregar_padre(self, padre):
        """Conecta un nodo padre a este nodo
        
        Args:
            padre (NodoBayesiano): Nodo padre a agregar
        """
        self.padres.append(padre)  # Añade el padre a la lista
    
    def definir_prob(self, prob: dict):
        """Configura la tabla de probabilidades condicionales
        
        Args:
            prob (dict): Diccionario con probabilidades P(X|combinación de padres)
                        Ej: {(True,True): 0.9, (True,False): 0.3}
        """
        self.tabla_prob = prob  # Asigna la tabla de probabilidades

class RedBayesiana:
    def __init__(self):
        """Constructor de la red bayesiana"""
        self.nodos = {}  # Diccionario para almacenar todos los nodos {nombre: objeto}
    
    def agregar_nodo(self, nombre):
        """Crea y agrega un nuevo nodo a la red
        
        Args:
            nombre (str): Nombre del nuevo nodo
            
        Returns:
            NodoBayesiano: El nodo recién creado
        """
        self.nodos[nombre] = NodoBayesiano(nombre)  # Crea y almacena el nodo
        return self.nodos[nombre]  # Devuelve el nodo creado
    
    def inferencia(self, nodo: str, evidencia: dict) -> float:
        """Realiza inferencia probabilística (versión simplificada)
        
        Args:
            nodo (str): Nombre del nodo a consultar
            evidencia (dict): Diccionario con valores observados {nodo: valor}
            
        Returns:
            float: Probabilidad P(nodo|evidencia)
        """
        nodo_obj = self.nodos[nodo]  # Obtiene el objeto nodo
        
        # Caso base: nodo sin padres (probabilidad marginal)
        if not nodo_obj.padres:
            return nodo_obj.tabla_prob.get(True, 0)  # Devuelve P(X) directamente
            
        # Intenta encontrar coincidencia con la evidencia
        for padre in nodo_obj.padres:
            if padre.nombre in evidencia:
                # Obtiene el valor del padre desde la evidencia
                valor_padre = evidencia[padre.nombre]
                # Busca en la tabla de probabilidades
                return nodo_obj.tabla_prob.get(valor_padre, 0)
        
        # Valor por defecto si no hay información suficiente
        return 0.5

# Ejemplo de uso - Sistema de diagnóstico médico
if __name__ == "__main__":
    print("=== Red Bayesiana de Diagnóstico Médico ===")
    
    # 1. Crear la red bayesiana
    rb = RedBayesiana()  # Instancia de la red
    
    # 2. Crear los nodos (variables)
    fiebre = rb.agregar_nodo('fiebre')  # Nodo para fiebre
    tos = rb.agregar_nodo('tos')  # Nodo para tos
    gripe = rb.agregar_nodo('gripe')  # Nodo para gripe
    
    # 3. Definir la estructura de la red
    gripe.agregar_padre(fiebre)  # Fiebre afecta probabilidad de gripe
    gripe.agregar_padre(tos)  # Tos afecta probabilidad de gripe
    
    # 4. Configurar probabilidades
    
    # Tabla de probabilidad condicional para gripe
    # P(gripe|fiebre, tos) en todas las combinaciones
    gripe.definir_prob({
        (True, True): 0.9,    # Alta probabilidad con fiebre y tos
        (True, False): 0.6,   # Probabilidad media con solo fiebre
        (False, True): 0.3,   # Probabilidad baja con solo tos
        (False, False): 0.05  # Muy baja probabilidad sin síntomas
    })
    
    # Probabilidades marginales (simplificado para ejemplo)
    fiebre.definir_prob({True: 0.2})  # P(fiebre) = 20%
    tos.definir_prob({True: 0.3})     # P(tos) = 30%
    
    # 5. Realizar consulta de inferencia
    evidencia = {'fiebre': True, 'tos': False}  # Síntomas observados
    prob = rb.inferencia('gripe', evidencia)  # Calcula P(gripe|evidencia)
    
    # 6. Mostrar resultado
    print(f"\nProbabilidad de gripe dado fiebre=True y tos=False:")
    print(f"P(gripe|fiebre,¬tos) = {prob:.2f} ({prob*100:.0f}%)")