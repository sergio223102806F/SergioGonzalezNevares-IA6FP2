import numpy as np  # Importa la biblioteca NumPy para operaciones numéricas
from sklearn.tree import DecisionTreeClassifier  # Importa la clase DecisionTreeClassifier de scikit-learn
from sklearn.datasets import make_classification  # Importa la función make_classification para generar datos de ejemplo
from sklearn.metrics import accuracy_score  # Importa la función accuracy_score para calcular la precisión

class AdaBoost:
    """Implementación del algoritmo AdaBoost para clasificación"""

    def __init__(self, n_estimators=50):
        """
        Args:
            n_estimators (int): Número de clasificadores débiles a entrenar
        """
        self.n_estimators = n_estimators  # Inicializa el número de estimadores (clasificadores débiles)
        self.clasificadores = []  # Almacena los clasificadores débiles (árboles de decisión)
        self.pesos_clasificadores = []  # Almacena los pesos (importancia) de cada clasificador
        self.errores = []  # Almacena los errores de cada iteración

    def fit(self, X, y):
        """Entrena el modelo AdaBoost"""
        n_muestras = X.shape[0]  # Obtiene el número de muestras en el conjunto de datos

        # 1. Inicializar pesos uniformes para las muestras
        pesos_muestras = np.ones(n_muestras) / n_muestras  # Asigna a cada muestra el mismo peso inicial (1/n)

        for _ in range(self.n_estimators):  # Itera sobre el número de clasificadores débiles
            # 2. Entrenar un clasificador débil (árbol de decisión con profundidad 1 - stump)
            clf = DecisionTreeClassifier(max_depth=1)  # Crea un árbol de decisión con profundidad máxima 1 (stump)
            clf.fit(X, y, sample_weight=pesos_muestras)  # Entrena el árbol de decisión con los pesos de las muestras
            predicciones = clf.predict(X)  # Obtiene las predicciones del clasificador débil para todas las muestras

            # 3. Calcular el error ponderado
            error = np.sum(pesos_muestras * (predicciones != y)) / np.sum(pesos_muestras)
            # Calcula el error ponderado: suma de los pesos de las muestras mal clasificadas

            # 4. Calcular el peso del clasificador (alpha)
            alpha = 0.5 * np.log((1 - error) / (error + 1e-10))  # Calcula el peso del clasificador actual (alpha)
            # El 1e-10 se añade para evitar la división por cero

            # 5. Actualizar pesos de las muestras
            pesos_muestras *= np.exp(-alpha * y * predicciones)  # Actualiza los pesos de las muestras
            #  - Si la predicción es correcta (y_i = predicciones_i), el peso se reduce
            #  - Si la predicción es incorrecta, el peso aumenta
            pesos_muestras /= np.sum(pesos_muestras)  # Normaliza los pesos para que sumen 1

            # Guardar el clasificador y su peso
            self.clasificadores.append(clf)  # Almacena el clasificador débil en la lista
            self.pesos_clasificadores.append(alpha)  # Almacena el peso del clasificador
            self.errores.append(error)  # Almacena el error del clasificador

    def predict(self, X):
        """Realiza predicciones con el ensemble"""
        # Inicializar predicciones a cero
        predicciones = np.zeros(X.shape[0])  # Crea un array de ceros para almacenar las predicciones del ensemble

        # Para cada clasificador, sumar su predicción ponderada
        for clf, alpha in zip(self.clasificadores, self.pesos_clasificadores):
            predicciones += alpha * clf.predict(X)  # Suma las predicciones de cada clasificador débil, ponderadas por su peso

        # Convertir a etiquetas de clase (-1 o 1)
        return np.sign(predicciones)  # Devuelve el signo de la suma ponderada (predicción final del ensemble)

    def score(self, X, y):
        """Calcula la precisión del modelo"""
        return accuracy_score(y, self.predict(X))  # Calcula la precisión comparando las predicciones con las etiquetas reales

# ==================== Ejemplo de Uso ====================
if __name__ == "__main__":
    # 1. Generar datos de ejemplo (clasificación binaria)
    X, y = make_classification(n_samples=1000, n_features=20, n_classes=2,
                                n_informative=15, random_state=42)  # Genera un conjunto de datos de clasificación binaria
    y = np.where(y == 0, -1, 1)  # Convierte las etiquetas de clase de 0 y 1 a -1 y 1 (requerido por AdaBoost)

    # 2. Dividir en train y test
    X_train, X_test = X[:800], X[800:]  # Divide los datos en conjuntos de entrenamiento y prueba
    y_train, y_test = y[:800], y[800:]  # Divide las etiquetas en conjuntos de entrenamiento y prueba

    # 3. Crear y entrenar modelo AdaBoost
    print("Entrenando AdaBoost...")
    adaboost = AdaBoost(n_estimators=50)  # Crea una instancia del clasificador AdaBoost con 50 estimadores
    adaboost.fit(X_train, y_train)  # Entrena el modelo AdaBoost con los datos de entrenamiento

    # 4. Evaluar el modelo
    train_accuracy = adaboost.score(X_train, y_train)  # Calcula la precisión en el conjunto de entrenamiento
    test_accuracy = adaboost.score(X_test, y_test)  # Calcula la precisión en el conjunto de prueba

    print(f"\nPrecisión en entrenamiento: {train_accuracy:.4f}")  # Imprime la precisión en entrenamiento
    print(f"Precisión en prueba: {test_accuracy:.4f}")  # Imprime la precisión en prueba

    # 5. Mostrar evolución del error
    print("\nEvolución del error durante el entrenamiento:")
    for i, error in enumerate(adaboost.errores, 1):  # Itera sobre los errores de cada iteración
        print(f"Iteración {i:2d}: Error = {error:.4f}, Alpha = {adaboost.pesos_clasificadores[i-1]:.4f}")  # Imprime el error y el peso del clasificador en cada iteración
