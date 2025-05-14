import numpy as np  # Importa la biblioteca NumPy para operaciones numéricas
from collections import defaultdict  # Importa defaultdict para crear diccionarios con valores por defecto (aunque no se usa en este código)

class MejorHipotesisActual:
    """Implementación del algoritmo de Mejor Hipótesis Actual (Version Space Learning)"""

    def __init__(self, tipo='conjuncion'):
        """
        Args:
            tipo (str): 'conjuncion' o 'disyuncion' para el tipo de hipótesis
        """
        self.tipo = tipo  # Inicializa el tipo de hipótesis (conjunción o disyunción)
        self.hipotesis = None  # Almacena la mejor hipótesis actual
        self.atributos = None  # Nombres de atributos
        self.valores_posibles = None  # Valores únicos por atributo
        self.clases = None  # Clases únicas

    def fit(self, X, y, atributos=None):
        """Aprende la mejor hipótesis a partir de datos de entrenamiento"""
        n_muestras, n_atributos = X.shape  # Obtiene el número de muestras y atributos
        self.atributos = atributos if atributos else [f"A{i}" for i in range(n_atributos)]
        # Si no se proporcionan nombres de atributos, se generan nombres genéricos
        self.clases = np.unique(y)  # Obtiene las clases únicas del conjunto de datos
        self.valores_posibles = [np.unique(X[:, i]) for i in range(n_atributos)]
        # Obtiene los valores únicos para cada atributo

        # Inicializar hipótesis (la más específica o general posible)
        if self.tipo == 'conjuncion':
            # Hipótesis inicial: CONJUNCIÓN de TODOS los posibles valores (más específica)
            self.hipotesis = [set(valores) for valores in self.valores_posibles]
            # Inicializa la hipótesis como la conjunción de todos los valores posibles para cada atributo.
            # Cada atributo puede tomar CUALQUIER valor al principio.
        else:
            # Hipótesis inicial: DISYUNCIÓN VACÍA (más general)
            self.hipotesis = [set() for _ in range(n_atributos)]
            # Inicializa la hipótesis como la disyunción vacía.  Ningún valor de atributo es requerido.

        # Ajustar la hipótesis con cada ejemplo positivo
        for i in range(n_muestras):  # Itera sobre cada ejemplo de entrenamiento
            if y[i] == self.clases[0]:  # Asumimos que la primera clase es la positiva
                self._ajustar_hipotesis(X[i])  # Ajusta la hipótesis actual para el ejemplo positivo

    def _ajustar_hipotesis(self, ejemplo):
        """Ajusta la hipótesis para cubrir un ejemplo positivo"""
        if self.tipo == 'conjuncion':
            # Para conjunción: generalizar la hipótesis
            for j in range(len(self.hipotesis)):  # Itera sobre cada atributo
                if ejemplo[j] not in self.hipotesis[j]:  # Si el valor del atributo del ejemplo no está en la hipótesis
                    # Si es el primer valor, reemplazar todo el conjunto
                    if len(self.hipotesis[j]) == len(self.valores_posibles[j]):
                        self.hipotesis[j] = {ejemplo[j]}  # El atributo debe ser IGUAL al valor del ejemplo.
                    else:
                        self.hipotesis[j].add(ejemplo[j])  # Agrega el valor del ejemplo a los valores aceptables del atributo
        else:
            # Para disyunción: especializar la hipótesis
            for j in range(len(self.hipotesis)):  # Itera sobre cada atributo
                if ejemplo[j] not in self.hipotesis[j]:
                    self.hipotesis[j].add(ejemplo[j])  # Agrega el valor del ejemplo a los valores aceptables para el atributo

    def predict(self, X):
        """Predice si un ejemplo cumple con la hipótesis aprendida"""
        predicciones = []  # Lista para almacenar las predicciones
        for ejemplo in X:  # Itera sobre cada ejemplo a predecir
            cumple = True  # Asume que el ejemplo cumple la hipótesis inicialmente
            for j in range(len(self.hipotesis)):  # Itera sobre cada atributo
                if self.tipo == 'conjuncion':
                    if ejemplo[j] not in self.hipotesis[j]:  # Si el valor del atributo no está en la hipótesis
                        cumple = False  # El ejemplo no cumple la hipótesis
                        break  # Sale del bucle interno
                else:  # Para disyunción
                    if len(self.hipotesis[j]) > 0 and ejemplo[j] not in self.hipotesis[j]:
                        cumple = False
                        break
            predicciones.append(self.clases[0] if cumple else self.clases[-1])
            # Si el ejemplo cumple la hipótesis, predice la primera clase; de lo contrario, predice la última clase
        return np.array(predicciones)  # Devuelve las predicciones como un array de NumPy

    def __str__(self):
        """Representación legible de la hipótesis"""
        s = f"Mejor Hipótesis Actual ({self.tipo}):\n"  # Encabezado de la representación
        for j in range(len(self.hipotesis)):  # Itera sobre cada atributo
            if self.tipo == 'conjuncion':
                if len(self.hipotesis[j]) == len(self.valores_posibles[j]):
                    s += f"{self.atributos[j]} = CUALQUIER_VALOR\n"  # Si todos los valores son aceptables, el atributo no importa
                else:
                    valores = " O ".join(sorted(self.hipotesis[j]))  # Crea una cadena con los valores aceptables
                    s += f"{self.atributos[j]} = {valores}\n"  # Imprime la condición del atributo
            else:  # Para disyunción
                if len(self.hipotesis[j]) == 0:
                    s += f"{self.atributos[j]} = NO_IMPORTA\n"  # Si ningún valor es aceptable, el atributo no importa
                else:
                    valores = " O ".join(sorted(self.hipotesis[j]))
                    s += f"{self.atributos[j]} = {valores}\n"
        return s  # Devuelve la representación en cadena

# ==================== Ejemplo de Uso ====================
if __name__ == "__main__":
    # Datos de ejemplo: diagnóstico de enfermedad (Sí/No)
    # Atributos: Fiebre (Alta, Media, Baja), Tos (Si, No), DolorCabeza (Si, No)
    X = np.array([
        ['Alta', 'Si', 'Si'],
        ['Alta', 'Si', 'No'],
        ['Media', 'No', 'Si'],
        ['Baja', 'No', 'No'],
        ['Alta', 'No', 'Si']
    ])
    y = np.array(['Enfermo', 'Enfermo', 'Sano', 'Sano', 'Enfermo'])
    atributos = ['Fiebre', 'Tos', 'DolorCabeza']

    print("=== Aprendizaje por Mejor Hipótesis Actual ===")

    print("\n1. Hipótesis en CONJUNCIÓN (más específica):")
    modelo_conj = MejorHipotesisActual(tipo='conjuncion')  # Crea un modelo de Mejor Hipótesis Actual para conjunciones
    modelo_conj.fit(X, y, atributos)  # Entrena el modelo con los datos
    print(modelo_conj)  # Imprime la hipótesis aprendida

    print("\nPredicciones:")
    X_test = np.array([['Alta', 'Si', 'Si'], ['Baja', 'No', 'Si']])  # Datos de prueba
    print(f"Datos: {X_test}")  # Imprime los datos de prueba
    print(f"Predicciones: {modelo_conj.predict(X_test)}")  # Imprime las predicciones del modelo

    print("\n2. Hipótesis en DISYUNCIÓN (más general):")
    modelo_disy = MejorHipotesisActual(tipo='disyuncion')  # Crea un modelo de Mejor Hipótesis Actual para disyunciones
    modelo_disy.fit(X, y, atributos)  # Entrena el modelo
    print(modelo_disy)  # Imprime la hipótesis aprendida

    print("\nPredicciones:")
    print(f"Datos: {X_test}")
    print(f"Predicciones: {modelo_disy.predict(X_test)}")  # Imprime las predicciones del modelo
