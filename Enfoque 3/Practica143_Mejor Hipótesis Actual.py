import numpy as np
from collections import defaultdict

class MejorHipotesisActual:
    """Implementación del algoritmo de Mejor Hipótesis Actual (Version Space Learning)"""
    
    def __init__(self, tipo='conjuncion'):
        """
        Args:
            tipo (str): 'conjuncion' o 'disyuncion' para el tipo de hipótesis
        """
        self.tipo = tipo
        self.hipotesis = None  # Almacena la mejor hipótesis actual
        self.atributos = None  # Nombres de atributos
        self.valores_posibles = None  # Valores únicos por atributo
        self.clases = None  # Clases únicas
        
    def fit(self, X, y, atributos=None):
        """Aprende la mejor hipótesis a partir de datos de entrenamiento"""
        n_muestras, n_atributos = X.shape
        self.atributos = atributos if atributos else [f"A{i}" for i in range(n_atributos)]
        self.clases = np.unique(y)
        self.valores_posibles = [np.unique(X[:, i]) for i in range(n_atributos)]
        
        # Inicializar hipótesis (la más específica o general posible)
        if self.tipo == 'conjuncion':
            # Hipótesis inicial: CONJUNCIÓN de TODOS los posibles valores (más específica)
            self.hipotesis = [set(valores) for valores in self.valores_posibles]
        else:
            # Hipótesis inicial: DISYUNCIÓN VACÍA (más general)
            self.hipotesis = [set() for _ in range(n_atributos)]
        
        # Ajustar la hipótesis con cada ejemplo positivo
        for i in range(n_muestras):
            if y[i] == self.clases[0]:  # Asumimos que la primera clase es la positiva
                self._ajustar_hipotesis(X[i])
    
    def _ajustar_hipotesis(self, ejemplo):
        """Ajusta la hipótesis para cubrir un ejemplo positivo"""
        if self.tipo == 'conjuncion':
            # Para conjunción: generalizar la hipótesis
            for j in range(len(self.hipotesis)):
                if ejemplo[j] not in self.hipotesis[j]:
                    # Si es el primer valor, reemplazar todo el conjunto
                    if len(self.hipotesis[j]) == len(self.valores_posibles[j]):
                        self.hipotesis[j] = {ejemplo[j]}
                    else:
                        self.hipotesis[j].add(ejemplo[j])
        else:
            # Para disyunción: especializar la hipótesis
            for j in range(len(self.hipotesis)):
                if ejemplo[j] not in self.hipotesis[j]:
                    self.hipotesis[j].add(ejemplo[j])
    
    def predict(self, X):
        """Predice si un ejemplo cumple con la hipótesis aprendida"""
        predicciones = []
        for ejemplo in X:
            cumple = True
            for j in range(len(self.hipotesis)):
                if self.tipo == 'conjuncion':
                    if ejemplo[j] not in self.hipotesis[j]:
                        cumple = False
                        break
                else:
                    if len(self.hipotesis[j]) > 0 and ejemplo[j] not in self.hipotesis[j]:
                        cumple = False
                        break
            predicciones.append(self.clases[0] if cumple else self.clases[-1])
        return np.array(predicciones)
    
    def __str__(self):
        """Representación legible de la hipótesis"""
        s = f"Mejor Hipótesis Actual ({self.tipo}):\n"
        for j in range(len(self.hipotesis)):
            if self.tipo == 'conjuncion':
                if len(self.hipotesis[j]) == len(self.valores_posibles[j]):
                    s += f"{self.atributos[j]} = CUALQUIER_VALOR\n"
                else:
                    valores = " O ".join(sorted(self.hipotesis[j]))
                    s += f"{self.atributos[j]} = {valores}\n"
            else:
                if len(self.hipotesis[j]) == 0:
                    s += f"{self.atributos[j]} = NO_IMPORTA\n"
                else:
                    valores = " O ".join(sorted(self.hipotesis[j]))
                    s += f"{self.atributos[j]} = {valores}\n"
        return s

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
    modelo_conj = MejorHipotesisActual(tipo='conjuncion')
    modelo_conj.fit(X, y, atributos)
    print(modelo_conj)
    
    print("\nPredicciones:")
    X_test = np.array([['Alta', 'Si', 'Si'], ['Baja', 'No', 'Si']])
    print(f"Datos: {X_test}")
    print(f"Predicciones: {modelo_conj.predict(X_test)}")
    
    print("\n2. Hipótesis en DISYUNCIÓN (más general):")
    modelo_disy = MejorHipotesisActual(tipo='disyuncion')
    modelo_disy.fit(X, y, atributos)
    print(modelo_disy)
    
    print("\nPredicciones:")
    print(f"Datos: {X_test}")
    print(f"Predicciones: {modelo_disy.predict(X_test)}")