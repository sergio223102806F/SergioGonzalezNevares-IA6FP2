# -*- coding: utf-8 -*-                                                     # Define la codificación de caracteres del archivo como UTF-8
"""
Created on Sat Apr 26 17:46:11 2025                                         # Indica la fecha y hora de creación del archivo
                                                                           #
@author: elvin                                                              # Define el autor del archivo
"""

# Importación de bibliotecas necesarias                                      # Comentario general sobre las importaciones
import numpy as np  # Para operaciones numéricas eficientes                 # Importa la biblioteca NumPy y la asigna el alias 'np'
import matplotlib.pyplot as plt  # Para visualización de resultados        # Importa la biblioteca Matplotlib y la asigna el alias 'plt'
from sklearn.datasets import make_classification  # Para generar datos de ejemplo # Importa la función para crear conjuntos de datos de clasificación

class Perceptron:                                                          # Define una nueva clase llamada Perceptron
    def __init__(self, learning_rate=0.01, n_iters=1000):                  # Define el constructor de la clase Perceptron con valores predeterminados
        """
        Constructor del Perceptrón                                          # Documentación del constructor del Perceptrón
        Args:                                                               # Inicio de la sección de argumentos
            learning_rate: Controla el tamaño de los ajustes en los pesos    # Descripción del argumento 'learning_rate'
            n_iters: Número máximo de iteraciones de entrenamiento          # Descripción del argumento 'n_iters'
        """
        self.lr = learning_rate  # Tasa de aprendizaje                     # Asigna la tasa de aprendizaje al atributo self.lr
        self.n_iters = n_iters  # Límite de épocas de entrenamiento        # Asigna el número máximo de iteraciones al atributo self.n_iters
        self.weights = None  # Se inicializarán en fit()                    # Inicializa el atributo de pesos como None
        self.bias = None  # Sesgo (bias)                                     # Inicializa el atributo de sesgo como None
        self.errors = []  # Registrará errores por época                   # Inicializa una lista vacía para almacenar los errores por época

    def activation(self, x):                                               # Define la función de activación
        """Función escalón (Heaviside) para clasificación binaria"""        # Documentación de la función de activación
        return np.where(x >= 0, 1, 0)  # 1 si x >= 0, 0 en otro caso        # Aplica la función escalón a cada elemento de x

    def fit(self, X, y):                                                    # Define el método para entrenar el Perceptrón
        """Método de entrenamiento"""                                      # Documentación del método de entrenamiento
        n_samples, n_features = X.shape                                     # Obtiene el número de muestras y características de la matriz de datos X

        # 1. Inicialización de parámetros                                    # Comentario indicando la inicialización de parámetros
        self.weights = np.zeros(n_features)  # Vector de pesos inicializado en 0 # Inicializa el vector de pesos con ceros
        self.bias = 0  # Sesgo inicial                                       # Inicializa el sesgo en cero

        # 2. Bucle principal de entrenamiento                               # Comentario indicando el bucle de entrenamiento
        for _ in range(self.n_iters):                                       # Itera sobre el número de iteraciones definido
            total_error = 0  # Contador de errores por época                 # Inicializa el contador de errores para la época actual

            # 3. Iterar sobre cada muestra de entrenamiento                  # Comentario indicando la iteración sobre las muestras
            for idx, x_i in enumerate(X):                                   # Itera sobre cada muestra (x_i) y su índice (idx) en la matriz de datos X
                # 4. Calcular la salida lineal (producto punto + sesgo)     # Comentario indicando el cálculo de la salida lineal
                linear_output = np.dot(x_i, self.weights) + self.bias       # Calcula la combinación lineal de la entrada y los pesos más el sesgo

                # 5. Aplicar función de activación                           # Comentario indicando la aplicación de la función de activación
                y_pred = self.activation(linear_output)                     # Aplica la función de activación a la salida lineal

                # 6. Calcular error (diferencia entre predicción y valor real) # Comentario indicando el cálculo del error
                error = y[idx] - y_pred                                      # Calcula la diferencia entre la etiqueta real y la predicción
                total_error += abs(error)  # Sumar error absoluto           # Suma el valor absoluto del error al total de errores de la época

                # 7. Actualizar pesos y sesgo (Regla del Perceptrón)         # Comentario indicando la actualización de pesos y sesgo
                self.weights += self.lr * error * x_i                       # Actualiza los pesos según la regla del Perceptrón
                self.bias += self.lr * error                                # Actualiza el sesgo según la regla del Perceptrón

            # 8. Registrar errores por época                                # Comentario indicando el registro de errores
            self.errors.append(total_error)                                 # Agrega el total de errores de la época a la lista de errores

            # 9. Criterio de parada temprana (si clasifica todo correctamente) # Comentario indicando el criterio de parada
            if total_error == 0:                                            # Si no hay errores en la época actual
                break                                                      # Detiene el entrenamiento

    def predict(self, X):                                                  # Define el método para realizar predicciones
        """Método para hacer predicciones"""                                # Documentación del método predecir
        linear_output = np.dot(X, self.weights) + self.bias               # Calcula la combinación lineal de la entrada y los pesos más el sesgo
        return self.activation(linear_output)                               # Aplica la función de activación a la salida lineal


class ADALINE:                                                            # Define una nueva clase llamada ADALINE
    def __init__(self, learning_rate=0.01, n_iters=1000):                  # Define el constructor de la clase ADALINE con valores predeterminados
        """Inicializa ADALINE con parámetros de entrenamiento"""            # Documentación del constructor de ADALINE
        self.lr = learning_rate                                             # Asigna la tasa de aprendizaje al atributo self.lr
        self.n_iters = n_iters                                               # Asigna el número máximo de iteraciones al atributo self.n_iters
        self.weights = None                                                 # Inicializa el atributo de pesos como None
        self.bias = None                                                    # Inicializa el atributo de sesgo como None
        self.losses = []  # Para registrar el error cuadrático medio        # Inicializa una lista vacía para almacenar las pérdidas

    def activation(self, x):                                               # Define la función de activación
        """Función de identidad (sin transformación)"""                      # Documentación de la función de activación
        return x  # ADALINE usa salida lineal durante entrenamiento         # Devuelve la entrada sin cambios (función de identidad)

    def compute_loss(self, y_true, y_pred):                                # Define el método para calcular la pérdida
        """Calcula el error cuadrático medio"""                              # Documentación del método compute_loss
        return 0.5 * np.mean((y_true - y_pred)**2)  # Factor 0.5 para simplificar derivada # Calcula el error cuadrático medio

    def fit(self, X, y):                                                    # Define el método para entrenar ADALINE
        """Entrenamiento con Regla Delta"""                                 # Documentación del método fit
        n_samples, n_features = X.shape                                     # Obtiene el número de muestras y características de la matriz de datos X

        # 1. Inicialización de parámetros                                    # Comentario indicando la inicialización de parámetros
        self.weights = np.zeros(n_features)                                 # Inicializa el vector de pesos con ceros
        self.bias = 0                                                       # Inicializa el sesgo en cero

        # 2. Bucle de entrenamiento                                       # Comentario indicando el bucle de entrenamiento
        for _ in range(self.n_iters):                                       # Itera sobre el número de iteraciones definido
            # 3. Calcular predicciones (sin función de activación)         # Comentario indicando el cálculo de las predicciones
            linear_output = np.dot(X, self.weights) + self.bias            # Calcula la salida lineal
            y_pred = self.activation(linear_output)                         # Aplica la función de activación (identidad)

            # 4. Calcular y almacenar pérdida                               # Comentario indicando el cálculo y almacenamiento de la pérdida
            loss = self.compute_loss(y, y_pred)                             # Calcula la pérdida
            self.losses.append(loss)                                        # Agrega la pérdida a la lista de pérdidas

            # 5. Calcular gradientes (derivadas parciales)                   # Comentario indicando el cálculo de los gradientes
            dw = -np.dot(X.T, (y - y_pred)) / n_samples  # Gradiente de pesos # Calcula el gradiente de los pesos
            db = -np.mean(y - y_pred)  # Gradiente del sesgo                # Calcula el gradiente del sesgo

            # 6. Actualizar parámetros (Descenso de gradiente)              # Comentario indicando la actualización de los parámetros
            self.weights -= self.lr * dw                                    # Actualiza los pesos usando el descenso de gradiente
            self.bias -= self.lr * db                                       # Actualiza el sesgo usando el descenso de gradiente

    def predict(self, X):                                                  # Define el método para realizar predicciones
        """Predicción con umbral en 0"""                                    # Documentación del método predecir
        linear_output = np.dot(X, self.weights) + self.bias               # Calcula la salida lineal
        return np.where(linear_output >= 0, 1, 0)  # Clasificación binaria  # Aplica un umbral para la clasificación binaria


class MADALINE:                                                           # Define una nueva clase llamada MADALINE
    def __init__(self, learning_rate=0.01, n_iters=1000, n_units=2):       # Define el constructor de la clase MADALINE con valores predeterminados
        """Inicializa red MADALINE con múltiples ADALINEs"""              # Documentación del constructor de MADALINE
        self.lr = learning_rate                                             # Asigna la tasa de aprendizaje al atributo self.lr
        self.n_iters = n_iters                                               # Asigna el número máximo de iteraciones al atributo self.n_iters
        self.n_units = n_units                                               # Asigna el número de unidades ADALINE al atributo self.n_units
        # Crear capa oculta de unidades ADALINE                             # Comentario indicando la creación de la capa oculta
        self.adalines = [ADALINE(learning_rate, n_iters) for _ in range(n_units)] # Crea una lista de objetos ADALINE
        # Pesos para la capa de salida                                     # Comentario indicando los pesos de la capa de salida
        self.output_weights = np.random.rand(n_units)  # Inicialización aleatoria # Inicializa los pesos de salida con valores aleatorios
        self.output_bias = np.random.rand()  # Sesgo de salida               # Inicializa el sesgo de salida con un valor aleatorio
        self.losses = []  # Historial de pérdidas                           # Inicializa una lista vacía para almacenar las pérdidas

    def activation(self, x):                                               # Define la función de activación
        """Sigmoide para la capa de salida"""                               # Documentación de la función de activación
        return 1 / (1 + np.exp(-x))  # Transforma a rango (0,1)            # Aplica la función sigmoide

    def fit(self, X, y):                                                    # Define el método para entrenar MADALINE
        """Entrenamiento en dos fases"""                                    # Documentación del método fit
        # Fase 1: Entrenar cada ADALINE individualmente                    # Comentario indicando la primera fase del entrenamiento
        for adaline in self.adalines:                                       # Itera sobre cada unidad ADALINE
            adaline.fit(X, y)                                              # Entrena la unidad ADALINE individualmente

        # Fase 2: Entrenar capa de salida                                  # Comentario indicando la segunda fase del entrenamiento
        for _ in range(self.n_iters):                                       # Itera sobre el número de iteraciones definido
            # 1. Calcular salidas de la capa oculta                         # Comentario indicando el cálculo de las salidas de la capa oculta
            hidden_outputs = np.array([                                     # Crea un array con las salidas de cada unidad ADALINE
                adaline.activation(np.dot(X, adaline.weights) + adaline.bias)
                for adaline in self.adalines
            ]).T  # Transponer para formato correcto                         # Transpone la matriz para tener las salidas en el formato correcto

            # 2. Calcular salida final (con sigmoide)                      # Comentario indicando el cálculo de la salida final
            output = self.activation(                                      # Calcula la salida de la red aplicando la función de activación
                np.dot(hidden_outputs, self.output_weights) + self.output_bias
            )

            # 3. Calcular y almacenar pérdida                             # Comentario indicando el cálculo y almacenamiento de la pérdida
            loss = 0.5 * np.mean((y - output)**2)                           # Calcula el error cuadrático medio
            self.losses.append(loss)                                        # Agrega la pérdida a la lista de pérdidas

            # 4. Calcular error y delta para backpropagation               # Comentario indicando el cálculo del error y delta
            error = output - y                                             # Calcula el error entre la salida predicha y la real
            delta_output = error * output * (1 - output)  # Derivada de sigmoide # Calcula el delta para la capa de salida usando la derivada de la sigmoide

            # 5. Actualizar pesos de salida                                 # Comentario indicando la actualización de los pesos de salida
            self.output_weights -= self.lr * np.dot(hidden_outputs.T, delta_output) # Actualiza los pesos de salida
            self.output_bias -= self.lr * np.sum(delta_output)              # Actualiza el sesgo de salida

    def predict(self, X):                                                  # Define el método para realizar predicciones
        """Genera predicciones"""                                        # Documentación del método predecir
        # 1. Calcular salidas de la capa oculta                         # Comentario indicando el cálculo de las salidas de la capa oculta
        hidden_outputs = np.array([                                     # Crea un array con las salidas de cada unidad ADALINE
            adaline.activation(np.dot(X, adaline.weights) + adaline.bias)
            for adaline in self.adalines
        ]).T

        # 2. Calcular salida final                                       # Comentario indicando el cálculo de la salida final
        output = np.dot(hidden_outputs, self.output_weights) + self.output_bias

        # 3. Aplicar umbral de decisión                                   # Comentario indicando la aplicación del umbral
        return np.where(output >= 0.5, 1, 0)  # Clasificación binaria      # Aplica un umbral para la clasificación binaria


# Bloque principal de ejecución                                          # Comentario indicando el bloque principal
if __name__ == "__main__":                                               # Asegura que el código dentro solo se ejecute si el script es el principal
    # 1. Generar datos de clasificación binaria                         # Comentario indicando la generación de datos
    X, y = make_classification(                                          # Genera un conjunto de datos de clasificación binaria
        n_samples=100,  # 100 muestras                                  # Especifica el número de muestras
        n_features=2,  # 2 características                               # Especifica el número de características
        n_classes=2,  # 2 clases                                      # Especifica el número de clases
        n_clusters_per_class=1,  # 1 grupo por clase                    # Especifica el número de clusters por clase
        random_state=42  # Semilla para reproducibilidad                # Establece la semilla aleatoria para la reproducibilidad
    )

    # 2. Crear instancias de los modelos                               # Comentario indicando la creación de instancias
    perceptron = Perceptron(learning_rate=0.01, n_iters=100)           # Crea una instancia del Perceptrón
    adaline = ADALINE(learning_rate=0.001, n_iters=200)                # Crea una instancia de ADALINE
    madaline = MADALINE(learning_rate=0.001, n_iters=300, n_units=2)    # Crea una instancia de MADALINE

    # 3. Entrenar modelos                                              # Comentario indicando el entrenamiento de los modelos
    perceptron.fit(X, y)                                               # Entrena el Perceptrón
    adaline.fit(X, y)                                                  # Entrena ADALINE
    madaline.fit(X, y)                                                 # Entrena MADALINE

    # 4. Visualizar curvas de aprendizaje                             # Comentario indicando la visualización de las curvas de aprendizaje
    plt.figure(figsize=(15, 5))                                        # Crea una nueva figura para los gráficos

    # Gráfico del Perceptrón                                           # Comentario indicando el gráfico del Perceptrón
    plt.subplot(131)                                                  # Crea el primer subplot (1 fila, 3 columnas, posición 1)
    plt