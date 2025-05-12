# -*- coding: utf-8 -*-                                                     # Define la codificación de caracteres del archivo como UTF-8
"""
Created on Sat Apr 26 17:39:10 2025                                         # Indica la fecha y hora de creación del archivo
                                                                           #
@author: elvin                                                              # Define el autor del archivo
"""

import numpy as np                                                          # Importa la biblioteca NumPy y la asigna el alias 'np' para operaciones numéricas
import matplotlib.pyplot as plt                                             # Importa la biblioteca Matplotlib y la asigna el alias 'plt' para graficar
from matplotlib.gridspec import GridSpec                                     # Importa GridSpec para un diseño de subplot más flexible

class FuncionesActivacion:                                                   # Define una nueva clase llamada FuncionesActivacion
    def __init__(self):                                                     # Define el constructor de la clase FuncionesActivacion
        """Inicializa los valores para graficar las funciones"""            # Documentación del constructor
        self.x = np.linspace(-5, 5, 500)  # Rango de valores de entrada       # Crea un array de 500 valores espaciados linealmente entre -5 y 5

    # ------------------------------------------                             # Separador de secciones
    # FUNCIONES DE ACTIVACIÓN                                                # Título de la sección
    # ------------------------------------------                             # Separador de secciones

    def sigmoide(self, x):                                                  # Define la función sigmoide
        """Función Sigmoide: Transforma valores al rango (0, 1)"""           # Documentación de la función sigmoide
        return 1 / (1 + np.exp(-x))                                        # Calcula y devuelve el valor de la función sigmoide

    def tanh(self, x):                                                      # Define la función tangente hiperbólica
        """Función Tangente Hiperbólica: Transforma valores al rango (-1, 1)""" # Documentación de la función tanh
        return np.tanh(x)                                                   # Calcula y devuelve el valor de la función tanh

    def relu(self, x):                                                      # Define la función ReLU
        """Función ReLU (Rectified Linear Unit): Devuelve el máximo entre 0 y x""" # Documentación de la función ReLU
        return np.maximum(0, x)                                             # Devuelve el máximo entre 0 y cada elemento de x

    def leaky_relu(self, x, alpha=0.1):                                     # Define la función Leaky ReLU
        """Versión mejorada de ReLU que permite pequeños valores negativos""" # Documentación de la función Leaky ReLU
        return np.where(x > 0, x, alpha * x)                                # Devuelve x si x > 0, y alpha * x en caso contrario

    def softmax(self, x):                                                   # Define la función softmax
        """Usada para problemas de clasificación múltiple, normaliza salidas a probabilidades""" # Documentación de la función softmax
        exps = np.exp(x - np.max(x))  # Estabilidad numérica               # Calcula exponenciales restando el máximo para evitar overflow
        return exps / np.sum(exps)                                          # Normaliza los exponenciales para obtener probabilidades

    # ------------------------------------------                             # Separador de secciones
    # DERIVADAS (Para backpropagation)                                       # Título de la sección
    # ------------------------------------------                             # Separador de secciones

    def derivada_sigmoide(self, x):                                         # Define la derivada de la función sigmoide
        """Derivada de la función Sigmoide"""                                # Documentación de la derivada de la sigmoide
        s = self.sigmoide(x)                                                # Calcula la sigmoide de x
        return s * (1 - s)                                                  # Calcula la derivada de la sigmoide

    def derivada_tanh(self, x):                                             # Define la derivada de la función tanh
        """Derivada de la función Tanh"""                                    # Documentación de la derivada de la tanh
        return 1 - np.tanh(x)**2                                            # Calcula la derivada de la tanh

    def derivada_relu(self, x):                                             # Define la derivada de la función ReLU
        """Derivada de la función ReLU"""                                    # Documentación de la derivada de la ReLU
        return np.where(x > 0, 1, 0)                                        # Devuelve 1 si x > 0, y 0 en caso contrario

    def derivada_leaky_relu(self, x, alpha=0.1):                            # Define la derivada de la función Leaky ReLU
        """Derivada de Leaky ReLU"""                                        # Documentación de la derivada de Leaky ReLU
        return np.where(x > 0, 1, alpha)                                    # Devuelve 1 si x > 0, y alpha en caso contrario

    # ------------------------------------------                             # Separador de secciones
    # VISUALIZACIÓN                                                          # Título de la sección
    # ------------------------------------------                             # Separador de secciones

    def graficar_funciones(self):                                           # Define el método para graficar las funciones
        """Crea una figura con las gráficas de todas las funciones de activación""" # Documentación del método graficar_funciones
        fig = plt.figure(figsize=(12, 8))                                   # Crea una nueva figura con un tamaño específico
        gs = GridSpec(2, 3, figure=fig)                                     # Crea un layout de grid de 2x3 para los subplots

        # Configuración común para los subplots                             # Comentario sobre la configuración de los subplots
        config_plots = {                                                     # Diccionario con la configuración común
            'xlabel': 'Input (x)',                                          # Etiqueta para el eje x
            'ylabel': 'Output',                                           # Etiqueta para el eje y
            'grid': True,                                                 # Activa la cuadrícula
            'xlim': (-5, 5),                                               # Límites del eje x
            'ylim': (-1.5, 1.5)  # Ajustado para visualizar mejor           # Límites del eje y
        }

        # 1. Sigmoide                                                       # Comentario para el primer subplot
        ax1 = fig.add_subplot(gs[0, 0])                                     # Añade un subplot en la posición [0, 0] del grid
        ax1.plot(self.x, self.sigmoide(self.x), label='Sigmoide', color='blue') # Grafica la función sigmoide
        ax1.plot(self.x, self.derivada_sigmoide(self.x), label='Derivada', linestyle='--', color='red') # Grafica la derivada de la sigmoide
        ax1.set_title('Sigmoide y su Derivada', pad=10)                   # Establece el título del subplot
        ax1.legend()                                                       # Muestra la leyenda

        # 2. Tanh                                                           # Comentario para el segundo subplot
        ax2 = fig.add_subplot(gs[0, 1])                                     # Añade un subplot en la posición [0, 1] del grid
        ax2.plot(self.x, self.tanh(self.x), label='Tanh', color='green')    # Grafica la función tanh
        ax2.plot(self.x, self.derivada_tanh(self.x), label='Derivada', linestyle='--', color='orange') # Grafica la derivada de la tanh
        ax2.set_title('Tanh y su Derivada', pad=10)                       # Establece el título del subplot
        ax2.legend()                                                       # Muestra la leyenda

        # 3. ReLU                                                           # Comentario para el tercer subplot
        ax3 = fig.add_subplot(gs[0, 2])                                     # Añade un subplot en la posición [0, 2] del grid
        ax3.plot(self.x, self.relu(self.x), label='ReLU', color='purple')    # Grafica la función ReLU
        ax3.plot(self.x, self.derivada_relu(self.x), label='Derivada', linestyle='--', color='brown') # Grafica la derivada de la ReLU
        ax3.set_title('ReLU y su Derivada', pad=10)                       # Establece el título del subplot
        ax3.legend()                                                       # Muestra la leyenda

        # 4. Leaky ReLU                                                     # Comentario para el cuarto subplot
        ax4 = fig.add_subplot(gs[1, 0])                                     # Añade un subplot en la posición [1, 0] del grid
        ax4.plot(self.x, self.leaky_relu(self.x), label='Leaky ReLU (α=0.1)', color='teal') # Grafica la función Leaky ReLU
        ax4.plot(self.x, self.derivada_leaky_relu(self.x), label='Derivada', linestyle='--', color='magenta') # Grafica la derivada de Leaky ReLU
        ax4.set_title('Leaky ReLU y su Derivada', pad=10)                # Establece el título del subplot
        ax4.legend()                                                       # Muestra la leyenda

        # 5. Softmax (ejemplo con 3 valores)                                # Comentario para el quinto subplot
        ax5 = fig.add_subplot(gs[1, 1:])                                    # Añade un subplot que ocupa las posiciones [1, 1] y [1, 2]
        sample_input = np.array([1.0, 2.0, 3.0])                            # Define un array de entrada de ejemplo para softmax
        output = self.softmax(sample_input)                                 # Calcula la salida de softmax para el ejemplo

        bars = ax5.bar(range(len(output)), output, color=['blue', 'green', 'red']) # Crea un gráfico de barras para la salida de softmax
        ax5.set_title('Softmax (Ejemplo con inputs [1.0, 2.0, 3.0])', pad=10) # Establece el título del subplot
        ax5.set_xticks(range(len(output)))                                 # Establece las posiciones de las marcas en el eje x
        ax5.set_xticklabels(['Input 1', 'Input 2', 'Input 3'])             # Establece las etiquetas de las marcas en el eje x
        ax5.set_ylabel('Probabilidad')                                     # Establece la etiqueta del eje y

        # Añadir valores en las barras                                      # Comentario para añadir valores en las barras
        for bar in bars:                                                   # Itera sobre cada barra
            height = bar.get_height()                                      # Obtiene la altura de la barra
            ax5.text(bar.get_x() + bar.get_width()/2., height,             # Añade texto en la parte superior de cada barra
                     f'{height:.2f}', ha='center', va='bottom')

        # Aplicar configuración común                                      # Comentario para aplicar la configuración común
        for ax in [ax1, ax2, ax3, ax4]:                                   # Itera sobre los subplots a los que se aplica la configuración común
            for key, value in config_plots.items():                       # Itera sobre los pares clave-valor en config_plots
                getattr(ax, f'set_{key}')(value)                           # Llama al método set_key del objeto ax con el valor correspondiente

        plt.tight_layout()                                                 # Ajusta el espaciado entre subplots para evitar solapamientos
        plt.show()                                                         # Muestra la figura

# Ejemplo de uso                                                        # Comentario para la sección de ejemplo de uso
if __name__ == "__main__":                                               # Asegura que el código dentro solo se ejecute si el script es el principal
    print("➡️ Visualización de Funciones de Activación en Redes Neuronales") # Imprime un mensaje descriptivo
    activaciones = FuncionesActivacion()                                  # Crea una instancia de la clase FuncionesActivacion
    activaciones.graficar_funciones()                                   # Llama al método para graficar las funciones

    # Demostración práctica                                               # Comentario para la demostración práctica
    print("\n🔍 Ejemplo Práctico:")                                     # Imprime un encabezado para el ejemplo práctico
    valores = np.array([-2.0, -0.5, 0.0, 0.5, 2.0])                      # Define un array de valores de entrada
    print("Valores de entrada:", valores)                                 # Imprime los valores de entrada
    print("Sigmoide:", np.round(activaciones.sigmoide(valores), 4))       # Imprime el resultado de la función sigmoide redondeado a 4 decimales
    print("Tanh:", np.round(activaciones.tanh(valores), 4))           # Imprime el resultado de la función tanh redondeado a 4 decimales
    print("ReLU:", np.round(activaciones.relu(valores), 4))           # Imprime el resultado de la función ReLU redondeado a 4 decimales
    print("Leaky ReLU:", np.round(activaciones.leaky_relu(valores), 4)) # Imprime el resultado de la función Leaky ReLU redondeado a 4 decimales
    print("Softmax (para [1.0, 2.0, 3.0]):", np.round(activaciones.softmax(np.array([1.0, 2.0, 3.0])), 4)) # Imprime el resultado de softmax para un ejemplo, redondeado a 4 decimales