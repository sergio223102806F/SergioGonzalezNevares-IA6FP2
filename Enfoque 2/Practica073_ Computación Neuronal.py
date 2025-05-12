# -*- coding: utf-8 -*-                                                     # Define la codificación de caracteres del archivo como UTF-8
"""
Created on Sat Apr 26 17:36:38 2025                                         # Indica la fecha y hora de creación del archivo
                                                                           #
@author: elvin                                                              # Define el autor del archivo
"""

# Importación de bibliotecas necesarias                                      # Comentario general sobre las importaciones
import numpy as np  # Para operaciones numéricas eficientes                 # Importa la biblioteca NumPy y la asigna el alias 'np'
import matplotlib.pyplot as plt  # Para visualización de resultados        # Importa la biblioteca Matplotlib y la asigna el alias 'plt'

class RedNeuronal:                                                          # Define una nueva clase llamada RedNeuronal
    def __init__(self, capas=[2, 4, 1], tasa_aprendizaje=0.1):              # Define el constructor de la clase RedNeuronal con valores predeterminados
        """
        Constructor de la red neuronal                                      # Documentación del constructor de la red neuronal
        Args:                                                               # Inicio de la sección de argumentos
            capas: lista con número de neuronas en cada capa (ej. [entrada, oculta, salida]) # Descripción del argumento 'capas'
            tasa_aprendizaje: factor que controla el tamaño de los ajustes en los pesos # Descripción del argumento 'tasa_aprendizaje'
        """
        self.capas = capas  # Configuración de la arquitectura de la red      # Asigna la lista de capas al atributo self.capas
        self.lr = tasa_aprendizaje  # Tasa de aprendizaje (learning rate)    # Asigna la tasa de aprendizaje al atributo self.lr

        # Inicialización de pesos y sesgos (biases)                          # Comentario sobre la inicialización de pesos y sesgos
        self.pesos = []  # Lista para almacenar matrices de pesos            # Inicializa una lista vacía para almacenar las matrices de pesos
        self.sesgos = []  # Lista para almacenar vectores de sesgo           # Inicializa una lista vacía para almacenar los vectores de sesgo

        # Inicialización Xavier/Glorot para mejores resultados en el entrenamiento # Comentario sobre la inicialización de pesos
        for i in range(len(capas)-1):  # Para cada conexión entre capas      # Itera sobre las capas para inicializar pesos y sesgos
            # Inicialización de pesos con distribución normal ajustada      # Comentario sobre la inicialización de pesos
            w = np.random.randn(capas[i], capas[i+1]) * np.sqrt(2./capas[i]) # Inicializa la matriz de pesos con números aleatorios usando Xavier/Glorot
            # Inicialización de sesgos en cero                               # Comentario sobre la inicialización de sesgos
            b = np.zeros((1, capas[i+1]))                                   # Inicializa el vector de sesgos con ceros
            self.pesos.append(w)  # Añade pesos inicializados                # Agrega la matriz de pesos inicializada a la lista self.pesos
            self.sesgos.append(b)  # Añade sesgos inicializados               # Agrega el vector de sesgos inicializado a la lista self.sesgos

    def sigmoide(self, x):                                                  # Define la función de activación sigmoide
        """Función de activación sigmoide (transforma valores a rango 0-1)""" # Documentación de la función sigmoide
        return 1 / (1 + np.exp(-x))                                         # Calcula y devuelve el valor de la función sigmoide

    def derivada_sigmoide(self, x):                                         # Define la derivada de la función sigmoide
        """Derivada de la función sigmoide (usada en backpropagation)"""     # Documentación de la derivada de la sigmoide
        return x * (1 - x)                                                   # Calcula y devuelve la derivada de la función sigmoide

    def forward(self, X):                                                   # Define el método para la propagación hacia adelante
        """Propagación hacia adelante (calcula las salidas de la red)"""      # Documentación del forward pass
        self.activaciones = [X]  # Almacena activaciones de cada capa        # Inicializa la lista de activaciones con la entrada X
        self.zs = []  # Almacena valores z (antes de aplicar activación)     # Inicializa una lista vacía para almacenar los valores z

        # Para cada capa de la red...                                        # Comentario indicando el bucle sobre las capas
        for i in range(len(self.pesos)):                                   # Itera sobre las capas de la red neuronal
            # Calcula combinación lineal de entradas y pesos                # Comentario sobre el cálculo de la combinación lineal
            z = np.dot(self.activaciones[-1], self.pesos[i]) + self.sesgos[i] # Calcula la suma ponderada de las entradas más el sesgo
            # Aplica función de activación                                  # Comentario sobre la aplicación de la función de activación
            a = self.sigmoide(z)                                            # Aplica la función de activación sigmoide al valor z
            self.zs.append(z)  # Guarda valor antes de activación            # Agrega el valor z a la lista self.zs
            self.activaciones.append(a)  # Guarda valor después de activación # Agrega la activación a la lista self.activaciones

        return self.activaciones[-1]  # Devuelve salida final de la red       # Devuelve la activación de la última capa

    def backward(self, X, y, output):                                        # Define el método para la propagación hacia atrás
        """Propagación hacia atrás (calcula gradientes y ajusta pesos)"""     # Documentación del backward pass
        m = X.shape[0]  # Número de ejemplos de entrenamiento               # Obtiene el número de ejemplos en el conjunto de entrenamiento

        # Error en la capa de salida                                        # Comentario sobre el cálculo del error
        error = output - y                                                 # Calcula la diferencia entre la salida predicha y la salida real

        # Listas para almacenar gradientes                                   # Comentario sobre la inicialización de listas para gradientes
        dW = []  # Gradientes de los pesos                                   # Inicializa una lista vacía para los gradientes de los pesos
        db = []  # Gradientes de los sesgos                                  # Inicializa una lista vacía para los gradientes de los sesgos

        # Backpropagation (comenzando desde la última capa)                 # Comentario indicando el inicio del backpropagation
        for i in reversed(range(len(self.pesos))):                        # Itera sobre las capas en orden inverso
            # Cálculo del delta (error propagado)                            # Comentario sobre el cálculo del delta
            if i == len(self.pesos)-1:  # Para capa de salida               # Para la última capa
                delta = error * self.derivada_sigmoide(output)              # Calcula el delta para la capa de salida
            else:  # Para capas ocultas                                     # Para las capas ocultas
                delta = np.dot(delta, self.pesos[i+1].T) * self.derivada_sigmoide(self.activaciones[i+1]) # Calcula el delta para las capas ocultas

            # Calcula gradientes para pesos y sesgos                         # Comentario sobre el cálculo de los gradientes
            dw = np.dot(self.activaciones[i].T, delta) / m                 # Calcula el gradiente de los pesos
            dbias = np.sum(delta, axis=0, keepdims=True) / m              # Calcula el gradiente de los sesgos

            # Guarda gradientes (en orden inverso)                           # Comentario sobre el almacenamiento de los gradientes
            dW.insert(0, dw)                                               # Inserta el gradiente de los pesos al inicio de la lista dW
            db.insert(0, dbias)                                            # Inserta el gradiente de los sesgos al inicio de la lista db

        # Actualiza pesos y sesgos usando gradiente descendente             # Comentario sobre la actualización de pesos y sesgos
        for i in range(len(self.pesos)):                                   # Itera sobre las capas para actualizar pesos y sesgos
            self.pesos[i] -= self.lr * dW[i]  # Ajuste de pesos             # Actualiza los pesos restando el gradiente multiplicado por la tasa de aprendizaje
            self.sesgos[i] -= self.lr * db[i]  # Ajuste de sesgos            # Actualiza los sesgos restando el gradiente multiplicado por la tasa de aprendizaje

    def entrenar(self, X, y, epocas=1000, verbose=True):                    # Define el método para entrenar la red neuronal
        """Método para entrenar la red neuronal"""                          # Documentación del método entrenar
        for epoca in range(epocas):                                        # Itera sobre el número de épocas
            # Paso forward (cálculo de predicciones)                       # Comentario sobre el forward pass
            output = self.forward(X)                                     # Realiza una pasada hacia adelante para obtener la salida
            # Paso backward (ajuste de pesos)                              # Comentario sobre el backward pass
            self.backward(X, y, output)                                  # Realiza una pasada hacia atrás para actualizar los pesos y sesgos

            # Mostrar progreso del entrenamiento                           # Comentario sobre la visualización del progreso
            if verbose and epoca % 100 == 0:                              # Imprime la pérdida cada 100 épocas si verbose es True
                # Cálculo del error cuadrático medio                       # Comentario sobre el cálculo de la pérdida
                perdida = np.mean(np.square(output - y))                  # Calcula la pérdida (error cuadrático medio)
                print(f"Época {epoca}, Pérdida: {perdida:.4f}")            # Imprime el número de época y la pérdida actual

    def predecir(self, X, umbral=0.5):                                      # Define el método para realizar predicciones
        """Método para hacer predicciones después del entrenamiento"""    # Documentación del método predecir
        y_pred = self.forward(X)  # Obtiene predicciones continuas         # Realiza una pasada hacia adelante para obtener las predicciones
        return (y_pred > umbral).astype(int)  # Convierte a predicciones binarias # Aplica un umbral y convierte a enteros (0 o 1)

    def graficar_perdida(self, X, y, epocas=1000):                         # Define el método para graficar la pérdida
        """Método para visualizar la reducción del error durante el entrenamiento""" # Documentación del método graficar_perdida
        perdidas = []  # Almacena valores de pérdida                        # Inicializa una lista vacía para almacenar los valores de pérdida

        for _ in range(epocas):                                           # Itera sobre el número de épocas
            output = self.forward(X)                                     # Realiza una pasada hacia adelante
            self.backward(X, y, output)                                  # Realiza una pasada hacia atrás
            perdida = np.mean(np.square(output - y))                      # Calcula la pérdida
            perdidas.append(perdida)  # Guarda valor de pérdida            # Agrega el valor de pérdida a la lista

        # Configuración del gráfico                                        # Comentario sobre la configuración del gráfico
        plt.plot(perdidas)                                                # Crea un gráfico de líneas con los valores de pérdida
        plt.title("Curva de Aprendizaje")                                  # Establece el título del gráfico
        plt.xlabel("Época")                                               # Establece la etiqueta del eje x
        plt.ylabel("Pérdida")                                              # Establece la etiqueta del eje y
        plt.show()                                                        # Muestra el gráfico

# Bloque principal de ejecución                                          # Comentario indicando el bloque principal
if __name__ == "__main__":                                               # Asegura que el código dentro solo se ejecute si el script es el principal
    # Datos de entrenamiento (compuerta XOR)                             # Comentario sobre los datos de entrenamiento
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])  # Entradas             # Define la matriz de entrada para la compuerta XOR
    y = np.array([[0], [1], [1], [0]])  # Salidas esperadas            # Define la matriz de salida esperada para la compuerta XOR

    # Crear instancia de la red neuronal                                 # Comentario sobre la creación de la instancia
    rn = RedNeuronal(capas=[2, 4, 1], tasa_aprendizaje=0.1)             # Crea una instancia de la clase RedNeuronal

    # Entrenamiento de la red                                           # Comentario sobre el entrenamiento de la red
    print("Entrenando la red neuronal...")                               # Imprime un mensaje indicando el inicio del entrenamiento
    rn.entrenar(X, y, epocas=5000)                                      # Llama al método entrenar para entrenar la red

    # Visualización de la curva de aprendizaje                          # Comentario sobre la visualización de la curva de aprendizaje
    rn.graficar_perdida(X, y, epocas=5000)                               # Llama al método graficar_perdida para mostrar la curva de aprendizaje

    # Predicción final                                                  # Comentario sobre la predicción final
    print("\nPredicciones finales:")                                    # Imprime un encabezado para las predicciones finales
    for i in range(len(X)):                                              # Itera sobre cada ejemplo de entrada
        prediccion = rn.predecir(X[i:i+1])[0][0]                        # Realiza una predicción para la entrada actual
        print(f"Entrada: {X[i]}, Predicción: {prediccion}")             # Imprime la entrada y la predicción correspondiente

    # Visualización de la frontera de decisión                          # Comentario sobre la visualización de la frontera de decisión
    plt.figure(figsize=(8, 6))                                         # Crea una nueva figura para el gráfico
    # Crear malla para evaluación                                       # Comentario sobre la creación de la malla
    x_min, x_max = -0.5, 1.5                                           # Define los límites mínimos y máximos para el eje x
    y_min, y_max = -0.5, 1.5                                           # Define los límites mínimos y máximos para el eje y
    h = 0.01                                                           # Define la resolución de la malla
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                           np.arange(y_min, y_max, h))                 # Crea una malla de puntos

    # Predecir para toda la malla                                       # Comentario sobre la predicción para la malla
    Z = rn.predecir(np.c_[xx.ravel(), yy.ravel()])                     # Realiza predicciones para todos los puntos de la malla
    Z = Z.reshape(xx.shape)                                            # Redimensiona las predicciones para que coincidan con la forma de la malla

    # Graficar resultados                                             # Comentario sobre la graficación de los resultados
    plt.contourf(xx, yy, Z, alpha=0.8)                                 # Dibuja las regiones de decisión
    plt.scatter(X[:, 0], X[:, 1], c=y.ravel(), edgecolors='k')         # Dibuja los puntos de datos con sus colores correspondientes
    plt.title("Frontera de Decisión para XOR")                         # Establece el título del gráfico
    plt.show()                                                        # Muestra el gráfico