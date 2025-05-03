import math
from collections import Counter

class NodoDecision:
    """Nodo de un árbol de decisión"""
    def __init__(self, atributo=None, valor=None, ramas=None, resultado=None):
        self.atributo = atributo  # Atributo que se evalúa en este nodo (None para hojas)
        self.valor = valor        # Valor del atributo que lleva a este nodo
        self.ramas = ramas or {}  # Diccionario {valor_atributo: subárbol}
        self.resultado = resultado  # Clase resultante (solo para nodos hoja)

    def __str__(self, nivel=0):
        """Representación visual del árbol"""
        prefijo = "  " * nivel
        if self.resultado is not None:
            return f"{prefijo}Clase: {self.resultado}"
        else:
            s = f"{prefijo}[{self.atributo}?]\n"
            for valor, subarbol in self.ramas.items():
                s += f"{prefijo}--> {valor}:\n{subarbol.__str__(nivel+1)}\n"
            return s

def entropia(etiquetas):
    """Calcula la entropía de un conjunto de etiquetas"""
    conteos = Counter(etiquetas)
    total = len(etiquetas)
    return -sum((count/total) * math.log2(count/total) for count in conteos.values())

def ganancia_informacion(datos, atributo, etiqueta_nombre="clase"):
    """Calcula la ganancia de información de un atributo"""
    # 1. Calcular entropía del conjunto total
    etiquetas = [d[etiqueta_nombre] for d in datos]
    entropia_total = entropia(etiquetas)
    
    # 2. Calcular entropía después de dividir por el atributo
    valores = {d[atributo] for d in datos}
    entropia_atributo = 0.0
    total_muestras = len(datos)
    
    for valor in valores:
        subconjunto = [d for d in datos if d[atributo] == valor]
        peso = len(subconjunto) / total_muestras
        etiquetas_sub = [d[etiqueta_nombre] for d in subconjunto]
        entropia_atributo += peso * entropia(etiquetas_sub)
    
    # 3. Ganancia = entropía_total - entropía_atributo
    return entropia_total - entropia_atributo

def id3(datos, atributos, etiqueta_nombre="clase", default=None):
    """Algoritmo ID3 para construir árboles de decisión"""
    # Caso base 1: Todos los ejemplos son de la misma clase
    etiquetas = [d[etiqueta_nombre] for d in datos]
    if len(set(etiquetas)) == 1:
        return NodoDecision(resultado=etiquetas[0])
    
    # Caso base 2: No quedan atributos para dividir
    if not atributos:
        conteo = Counter(etiquetas)
        return NodoDecision(resultado=conteo.most_common(1)[0][0])
    
    # 1. Seleccionar el mejor atributo (mayor ganancia)
    mejor_atributo = max(
        atributos, 
        key=lambda a: ganancia_informacion(datos, a, etiqueta_nombre)
    )
    
    # 2. Crear nodo con el mejor atributo
    nodo = NodoDecision(atributo=mejor_atributo)
    
    # 3. Dividir por cada valor del atributo
    valores = {d[mejor_atributo] for d in datos}
    nuevos_atributos = [a for a in atributos if a != mejor_atributo]
    
    for valor in valores:
        subdatos = [d for d in datos if d[mejor_atributo] == valor]
        
        # Caso base 3: Subconjunto vacío
        if not subdatos:
            conteo = Counter(etiquetas)
            nodo.ramas[valor] = NodoDecision(resultado=conteo.most_common(1)[0][0])
        else:
            # Llamada recursiva
            nodo.ramas[valor] = id3(subdatos, nuevos_atributos, etiqueta_nombre, default)
    
    return nodo

def clasificar(ejemplo, arbol):
    """Clasifica un nuevo ejemplo usando el árbol"""
    if arbol.resultado is not None:
        return arbol.resultado
    
    valor = ejemplo[arbol.atributo]
    if valor not in arbol.ramas:
        return None  # Valor no visto durante entrenamiento
    
    return clasificar(ejemplo, arbol.ramas[valor])

# ==================== Ejemplo de Uso ====================
if __name__ == "__main__":
    # Datos de entrenamiento (clásico juego de golf)
    datos_entrenamiento = [
        {"outlook": "sunny", "temp": "hot", "humidity": "high", "wind": "weak", "clase": "no"},
        {"outlook": "sunny", "temp": "hot", "humidity": "high", "wind": "strong", "clase": "no"},
        {"outlook": "overcast", "temp": "hot", "humidity": "high", "wind": "weak", "clase": "yes"},
        {"outlook": "rain", "temp": "mild", "humidity": "high", "wind": "weak", "clase": "yes"},
        {"outlook": "rain", "temp": "cool", "humidity": "normal", "wind": "weak", "clase": "yes"},
        {"outlook": "rain", "temp": "cool", "humidity": "normal", "wind": "strong", "clase": "no"},
        {"outlook": "overcast", "temp": "cool", "humidity": "normal", "wind": "strong", "clase": "yes"},
        {"outlook": "sunny", "temp": "mild", "humidity": "high", "wind": "weak", "clase": "no"},
        {"outlook": "sunny", "temp": "cool", "humidity": "normal", "wind": "weak", "clase": "yes"},
        {"outlook": "rain", "temp": "mild", "humidity": "normal", "wind": "weak", "clase": "yes"},
        {"outlook": "sunny", "temp": "mild", "humidity": "normal", "wind": "strong", "clase": "yes"},
        {"outlook": "overcast", "temp": "mild", "humidity": "high", "wind": "strong", "clase": "yes"},
        {"outlook": "overcast", "temp": "hot", "humidity": "normal", "wind": "weak", "clase": "yes"},
        {"outlook": "rain", "temp": "mild", "humidity": "high", "wind": "strong", "clase": "no"},
    ]

    # Atributos disponibles (excluyendo la clase)
    atributos = ["outlook", "temp", "humidity", "wind"]

    # Construir árbol
    arbol = id3(datos_entrenamiento, atributos)
    print("Árbol de decisión construido:\n")
    print(arbol)

    # Ejemplo de clasificación
    nuevo_ejemplo = {"outlook": "sunny", "temp": "cool", "humidity": "high", "wind": "strong"}
    prediccion = clasificar(nuevo_ejemplo, arbol)
    print(f"\nPredicción para {nuevo_ejemplo}: {prediccion}")