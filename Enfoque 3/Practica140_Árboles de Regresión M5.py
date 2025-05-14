# -*- coding: utf-8 -*-                                                     # Define la codificación de caracteres del archivo como UTF-8
import numpy as np                                                        # Importa la librería NumPy y la asigna al alias np
from sklearn.linear_model import LinearRegression                         # Importa la clase LinearRegression del módulo sklearn.linear_model
from collections import defaultdict                                      # Importa defaultdict desde el módulo collections

class NodoRegresion:                                                      # Define una clase llamada NodoRegresion
    """Nodo para árboles de regresión M5"""                                # Documentación de la clase NodoRegresion
    def __init__(self, atributo=None, valor=None, ramas=None, modelo=None, valor_pred=None): # Define el constructor de la clase
        self.atributo = atributo                                        # Atributo para dividir (None en hojas)
        self.valor = valor                                              # Valor del atributo que lleva a este nodo
        self.ramas = ramas or {}                                        # Subárboles {valor: nodo}
        self.modelo = modelo                                            # Modelo lineal (en hojas)
        self.valor_pred = valor_pred                                    # Valor constante (para hojas simples)

    def __str__(self, nivel=0):                                         # Define la representación en string del objeto
        """Representación visual del árbol"""                             # Documentación del método __str__
        prefijo = "  " * nivel                                          # Define el prefijo para la indentación
        if self.modelo is not None:                                     # Si el nodo tiene un modelo lineal
            return f"{prefijo}Modelo: {self.modelo.coef_}*X + {self.modelo.intercept_}" # Retorna la representación del modelo
        elif self.valor_pred is not None:                               # Si el nodo tiene un valor de predicción constante
            return f"{prefijo}Valor: {self.valor_pred:.2f}"               # Retorna la representación del valor
        else:                                                          # Si el nodo es un nodo de división
            s = f"{prefijo}[{self.atributo}?]\n"                         # Inicializa la string con el atributo de división
            for valor, subarbol in self.ramas.items():                   # Itera sobre las ramas del nodo
                s += f"{prefijo}--> {valor}:\n{subarbol.__str__(nivel+1)}\n" # Añade la representación del subárbol con mayor indentación
            return s                                                     # Retorna la representación del nodo

def error_cuadratico_medio(y):                                          # Define la función error_cuadratico_medio
    """Calcula el error cuadrático medio como medida de dispersión"""     # Documentación de la función error_cuadratico_medio
    if len(y) == 0:                                                     # Si la longitud de y es 0
        return 0                                                       # Retorna 0
    media = np.mean(y)                                                 # Calcula la media de y
    return np.mean((y - media)**2)                                     # Calcula el error cuadrático medio

def mejor_division(X, y, atributos):                                    # Define la función mejor_division
    """Encuentra el mejor atributo y valor para dividir"""                # Documentación de la función mejor_division
    mejor_atributo = None                                              # Inicializa el mejor atributo como None
    mejor_valor = None                                                 # Inicializa el mejor valor como None
    mejor_reduccion = -np.inf                                          # Inicializa la mejor reducción como infinito negativo

    for atributo in atributos:                                         # Itera sobre los atributos
        valores = np.unique(X[:, atributos.index(atributo)])           # Obtiene los valores únicos del atributo en X

        for valor in valores:                                           # Itera sobre los valores del atributo
            mascara = X[:, atributos.index(atributo)] == valor         # Crea una máscara booleana para el valor del atributo
            y_izq = y[mascara]                                           # Divide y en la parte izquierda
            y_der = y[~mascara]                                          # Divide y en la parte derecha

            reduccion = error_cuadratico_medio(y) - (                  # Calcula la reducción del error
                (len(y_izq)/len(y)) * error_cuadratico_medio(y_izq) +
                (len(y_der)/len(y)) * error_cuadratico_medio(y_der)
            )

            if reduccion > mejor_reduccion:                            # Si la reducción actual es mejor que la mejor reducción encontrada
                mejor_reduccion = reduccion                              # Actualiza la mejor reducción
                mejor_atributo = atributo                                # Actualiza el mejor atributo
                mejor_valor = valor                                      # Actualiza el mejor valor

    return mejor_atributo, mejor_valor                                  # Retorna el mejor atributo y el mejor valor

def m5(X, y, atributos, min_muestras=5, max_profundidad=5):              # Define la función m5
    """Algoritmo M5 para árboles de regresión"""                         # Documentación de la función m5
    # Caso base 1: Muy pocas muestras                                   # Comentario para el caso base 1
    if len(y) < min_muestras or max_profundidad == 0:                  # Si el número de muestras es menor que el mínimo o la profundidad máxima es 0
        modelo = LinearRegression().fit(X, y)                           # Ajusta un modelo de regresión lineal a los datos
        return NodoRegresion(modelo=modelo)                             # Retorna un nodo hoja con el modelo lineal

    # Caso base 2: Todos los valores iguales                             # Comentario para el caso base 2
    if np.all(y == y[0]):                                               # Si todos los valores en y son iguales
        return NodoRegresion(valor_pred=y[0])                           # Retorna un nodo hoja con el valor de predicción constante

    # 1. Encontrar la mejor división                                    # Comentario para el paso 1
    mejor_atrib, mejor_val = mejor_division(X, y, atributos)           # Encuentra el mejor atributo y valor para dividir

    if mejor_atrib is None:                                            # Si no se encontró división útil
        modelo = LinearRegression().fit(X, y)                           # Ajusta un modelo de regresión lineal a los datos
        return NodoRegresion(modelo=modelo)                             # Retorna un nodo hoja con el modelo lineal

    # 2. Crear nodo con la división                                     # Comentario para el paso 2
    nodo = NodoRegresion(atributo=mejor_atrib)                          # Crea un nuevo nodo con el mejor atributo
    idx_atrib = atributos.index(mejor_atrib)                           # Obtiene el índice del mejor atributo

    # 3. Dividir el dataset                                            # Comentario para el paso 3
    mascara = X[:, idx_atrib] == mejor_val                             # Crea una máscara booleana para el mejor valor del atributo
    X_izq, y_izq = X[mascara], y[mascara]                               # Divide X e y en la parte izquierda
    X_der, y_der = X[~mascara], y[~mascara]                             # Divide X e y en la parte derecha

    # 4. Construir subárboles recursivamente                            # Comentario para el paso 4
    nuevos_atributos = [a for a in atributos if a != mejor_atrib]      # Crea una lista de atributos sin el mejor atributo
    nodo.ramas[mejor_val] = m5(X_izq, y_izq, nuevos_atributos, min_muestras, max_profundidad-1) # Construye el subárbol izquierdo recursivamente
    nodo.ramas[f"no_{mejor_val}"] = m5(X_der, y_der, nuevos_atributos, min_muestras, max_profundidad-1) # Construye el subárbol derecho recursivamente

    return nodo                                                        # Retorna el nodo construido

def predecir(x, arbol, atributos):                                     # Define la función predecir
    """Realiza una predicción con el árbol M5"""                        # Documentación de la función predecir
    if arbol.modelo is not None:                                     # Si el nodo tiene un modelo lineal
        return arbol.modelo.predict([x])[0]                           # Retorna la predicción del modelo lineal
    elif arbol.valor_pred is not None:                               # Si el nodo tiene un valor de predicción constante
        return arbol.valor_pred                                        # Retorna el valor de predicción constante
    else:                                                          # Si el nodo es un nodo de división
        idx_atrib = atributos.index(arbol.atributo)                   # Obtiene el índice del atributo de división
        valor = x[idx_atrib]                                           # Obtiene el valor del atributo en el punto de datos
        if valor in arbol.ramas:                                     # Si el valor existe como una rama
            return predecir(x, arbol.ramas[valor], atributos)          # Llama a predecir recursivamente en la rama correspondiente
        else:                                                      # Si el valor no existe como una rama
            # Si el valor no se vio en entrenamiento, usar cualquier rama # Comentario para el caso de valor no visto
            subarbol = next(iter(arbol.ramas.values()))               # Obtiene el primer subárbol
            return predecir(x, subarbol, atributos)                  # Llama a predecir recursivamente en ese subárbol

# ==================== Ejemplo de Uso ====================                 # Separador de sección
if __name__ == "__main__":                                                 # Bloque de código que se ejecuta cuando el script se llama directamente
    # Datos de ejemplo: precio de casas (simulado)                       # Comentario para los datos de ejemplo
    # Atributos: [metros_cuadrados, num_habitaciones, zona]              # Comentario para los atributos
    X = np.array([                                                      # Define el array de características X
        [120, 3, "centro"],
        [90, 2, "centro"],
        [150, 4, "norte"],
        [80, 2, "sur"],
        [200, 5, "norte"],
        [70, 1, "sur"],
        [180, 4, "norte"],
        [95, 2, "centro"]
    ])
    y = np.array([250000, 200000, 350000, 180000, 420000, 150000, 380000, 210000]) # Define el array de la variable objetivo y

    atributos = ["metros", "habitaciones", "zona"]                      # Define la lista de nombres de los atributos

    # Convertir atributos categóricos a índices                       # Comentario para la conversión de atributos categóricos
    zonas = {"centro": 0, "norte": 1, "sur": 2}                        # Define un diccionario para mapear zonas a índices
    X_numerico = X.copy()                                              # Crea una copia de X
    X_numerico[:, 2] = [zonas[z] for z in X[:, 2]]                     # Convierte la columna de zonas a valores numéricos
    X_numerico = X_numerico.astype(float)                              # Convierte X_numerico a tipo float

    # Construir árbol                                                  # Comentario para la construcción del árbol
    arbol_m5 = m5(X_numerico, y, atributos, min_muestras=2, max_profundidad=3) # Construye el árbol M5
    print("Árbol M5 construido:\n")                                   # Imprime un encabezado
    print(arbol_m5)                                                    # Imprime el árbol M5

    # Ejemplo de predicción                                            # Comentario para el ejemplo de predicción
    nueva_casa = [110, 3, "centro"]                                   # Define los datos de una nueva casa
    nueva_casa_numerico = [110, 3, zonas["centro"]]                     # Convierte los atributos de la nueva casa a numérico
    prediccion = predecir(nueva_casa_numerico, arbol_m5, atributos)    # Realiza la predicción para la nueva casa
    print(f"\nPredicción para {nueva_casa}: ${prediccion:,.2f}")        # Imprime la predicción