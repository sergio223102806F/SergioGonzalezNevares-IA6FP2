import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score

class AdaBoost:
    """Implementación del algoritmo AdaBoost para clasificación"""
    
    def __init__(self, n_estimators=50):
        """
        Args:
            n_estimators (int): Número de clasificadores débiles a entrenar
        """
        self.n_estimators = n_estimators
        self.clasificadores = []  # Almacena los clasificadores débiles
        self.pesos_clasificadores = []  # Almacena los pesos (importancia) de cada clasificador
        self.errores = []  # Almacena los errores de cada iteración

    def fit(self, X, y):
        """Entrena el modelo AdaBoost"""
        n_muestras = X.shape[0]
        
        # 1. Inicializar pesos uniformes para las muestras
        pesos_muestras = np.ones(n_muestras) / n_muestras
        
        for _ in range(self.n_estimators):
            # 2. Entrenar un clasificador débil (árbol de decisión con profundidad 1)
            clf = DecisionTreeClassifier(max_depth=1)
            clf.fit(X, y, sample_weight=pesos_muestras)
            predicciones = clf.predict(X)
            
            # 3. Calcular el error ponderado
            error = np.sum(pesos_muestras * (predicciones != y)) / np.sum(pesos_muestras)
            
            # 4. Calcular el peso del clasificador (alpha)
            alpha = 0.5 * np.log((1 - error) / (error + 1e-10))  # Evitar división por cero
            
            # 5. Actualizar pesos de las muestras
            pesos_muestras *= np.exp(-alpha * y * predicciones)
            pesos_muestras /= np.sum(pesos_muestras)  # Normalizar
            
            # Guardar el clasificador y su peso
            self.clasificadores.append(clf)
            self.pesos_clasificadores.append(alpha)
            self.errores.append(error)

    def predict(self, X):
        """Realiza predicciones con el ensemble"""
        # Inicializar predicciones a cero
        predicciones = np.zeros(X.shape[0])
        
        # Para cada clasificador, sumar su predicción ponderada
        for clf, alpha in zip(self.clasificadores, self.pesos_clasificadores):
            predicciones += alpha * clf.predict(X)
            
        # Convertir a etiquetas de clase (-1 o 1)
        return np.sign(predicciones)

    def score(self, X, y):
        """Calcula la precisión del modelo"""
        return accuracy_score(y, self.predict(X))

# ==================== Ejemplo de Uso ====================
if __name__ == "__main__":
    # 1. Generar datos de ejemplo (clasificación binaria)
    X, y = make_classification(n_samples=1000, n_features=20, n_classes=2, 
                              n_informative=15, random_state=42)
    y = np.where(y == 0, -1, 1)  # Convertir etiquetas a -1 y 1 para AdaBoost
    
    # 2. Dividir en train y test
    X_train, X_test = X[:800], X[800:]
    y_train, y_test = y[:800], y[800:]
    
    # 3. Crear y entrenar modelo AdaBoost
    print("Entrenando AdaBoost...")
    adaboost = AdaBoost(n_estimators=50)
    adaboost.fit(X_train, y_train)
    
    # 4. Evaluar el modelo
    train_accuracy = adaboost.score(X_train, y_train)
    test_accuracy = adaboost.score(X_test, y_test)
    
    print(f"\nPrecisión en entrenamiento: {train_accuracy:.4f}")
    print(f"Precisión en prueba: {test_accuracy:.4f}")
    
    # 5. Mostrar evolución del error
    print("\nEvolución del error durante el entrenamiento:")
    for i, error in enumerate(adaboost.errores, 1):
        print(f"Iteración {i:2d}: Error = {error:.4f}, Alpha = {adaboost.pesos_clasificadores[i-1]:.4f}")