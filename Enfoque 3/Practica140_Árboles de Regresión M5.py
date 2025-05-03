import numpy as np
from sklearn.linear_model import LinearRegression
from collections import defaultdict

class NodoRegresion:
    """Nodo para árboles de regresión M5"""
    def __init__(self, atributo=None, valor=None, ramas=None, modelo=None, valor_pred=None):
        self.atributo = atributo    # Atributo para dividir (None en hojas)
        self.valor = valor          # Valor del atributo que lleva a este nodo
        self.ramas = ramas or {}    # Subárboles {valor: nodo}
        self.modelo = modelo        # Modelo lineal (en hojas)
        self.valor_pred = valor_pred  # Valor constante (para hojas simples)

    def __str__(self, nivel=0):
        """Representación visual del árbol"""
        prefijo = "  " * nivel
        if self.modelo is not None:
            return f"{prefijo}Modelo: {self.modelo.coef_}*X + {self.modelo.intercept_}"
        elif self.valor_pred is not None:
            return f"{prefijo}Valor: {self.valor_pred:.2f}"
        else:
            s = f"{prefijo}[{self.atributo}?]\n"
            for valor, subarbol in self.ramas.items():
                s += f"{prefijo}--> {valor}:\n{subarbol.__str__(nivel+1)}\n"
            return s

def error_cuadratico_medio(y):
    """Calcula el error cuadrático medio como medida de dispersión"""
    if len(y) == 0:
        return 0
    media = np.mean(y)
    return np.mean((y - media)**2)

def mejor_division(X, y, atributos):
    """Encuentra el mejor atributo y valor para dividir"""
    mejor_atributo = None
    mejor_valor = None
    mejor_reduccion = -np.inf
    
    for atributo in atributos:
        valores = np.unique(X[:, atributos.index(atributo)])
        
        for valor in valores:
            mascara = X[:, atributos.index(atributo)] == valor
            y_izq = y[mascara]
            y_der = y[~mascara]
            
            reduccion = error_cuadratico_medio(y) - (
                (len(y_izq)/len(y)) * error_cuadratico_medio(y_izq) +
                (len(y_der)/len(y)) * error_cuadratico_medio(y_der)
            )
            
            if reduccion > mejor_reduccion:
                mejor_reduccion = reduccion
                mejor_atributo = atributo
                mejor_valor = valor
                
    return mejor_atributo, mejor_valor

def m5(X, y, atributos, min_muestras=5, max_profundidad=5):
    """Algoritmo M5 para árboles de regresión"""
    # Caso base 1: Muy pocas muestras
    if len(y) < min_muestras or max_profundidad == 0:
        modelo = LinearRegression().fit(X, y)
        return NodoRegresion(modelo=modelo)
    
    # Caso base 2: Todos los valores iguales
    if np.all(y == y[0]):
        return NodoRegresion(valor_pred=y[0])
    
    # 1. Encontrar la mejor división
    mejor_atrib, mejor_val = mejor_division(X, y, atributos)
    
    if mejor_atrib is None:  # No se encontró división útil
        modelo = LinearRegression().fit(X, y)
        return NodoRegresion(modelo=modelo)
    
    # 2. Crear nodo con la división
    nodo = NodoRegresion(atributo=mejor_atrib)
    idx_atrib = atributos.index(mejor_atrib)
    
    # 3. Dividir el dataset
    mascara = X[:, idx_atrib] == mejor_val
    X_izq, y_izq = X[mascara], y[mascara]
    X_der, y_der = X[~mascara], y[~mascara]
    
    # 4. Construir subárboles recursivamente
    nuevos_atributos = [a for a in atributos if a != mejor_atrib]
    nodo.ramas[mejor_val] = m5(X_izq, y_izq, nuevos_atributos, min_muestras, max_profundidad-1)
    nodo.ramas[f"no_{mejor_val}"] = m5(X_der, y_der, nuevos_atributos, min_muestras, max_profundidad-1)
    
    return nodo

def predecir(x, arbol, atributos):
    """Realiza una predicción con el árbol M5"""
    if arbol.modelo is not None:
        return arbol.modelo.predict([x])[0]
    elif arbol.valor_pred is not None:
        return arbol.valor_pred
    else:
        idx_atrib = atributos.index(arbol.atributo)
        valor = x[idx_atrib]
        if valor in arbol.ramas:
            return predecir(x, arbol.ramas[valor], atributos)
        else:
            # Si el valor no se vio en entrenamiento, usar cualquier rama
            subarbol = next(iter(arbol.ramas.values()))
            return predecir(x, subarbol, atributos)

# ==================== Ejemplo de Uso ====================
if __name__ == "__main__":
    # Datos de ejemplo: precio de casas (simulado)
    # Atributos: [metros_cuadrados, num_habitaciones, zona]
    X = np.array([
        [120, 3, "centro"],
        [90, 2, "centro"],
        [150, 4, "norte"],
        [80, 2, "sur"],
        [200, 5, "norte"],
        [70, 1, "sur"],
        [180, 4, "norte"],
        [95, 2, "centro"]
    ])
    y = np.array([250000, 200000, 350000, 180000, 420000, 150000, 380000, 210000])
    
    atributos = ["metros", "habitaciones", "zona"]
    
    # Convertir atributos categóricos a índices
    zonas = {"centro": 0, "norte": 1, "sur": 2}
    X_numerico = X.copy()
    X_numerico[:, 2] = [zonas[z] for z in X[:, 2]]
    X_numerico = X_numerico.astype(float)
    
    # Construir árbol
    arbol_m5 = m5(X_numerico, y, atributos, min_muestras=2, max_profundidad=3)
    print("Árbol M5 construido:\n")
    print(arbol_m5)
    
    # Ejemplo de predicción
    nueva_casa = [110, 3, "centro"]  # 110m², 3 hab, zona centro
    nueva_casa_numerico = [110, 3, zonas["centro"]]
    prediccion = predecir(nueva_casa_numerico, arbol_m5, atributos)
    print(f"\nPredicción para {nueva_casa}: ${prediccion:,.2f}")