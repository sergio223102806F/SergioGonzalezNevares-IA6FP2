# -*- coding: utf-8 -*-                                                     # Define la codificación de caracteres del archivo como UTF-8
"""
Created on Sun Apr 27 13:43:57 2025                                         # Indica la fecha y hora de creación del archivo
                                                                           #
@author: elvin                                                              # Define el autor del archivo
"""

"""
Motor de Gráficos por Computadora - Renderizado 3D Básico

Este código implementa:
1. Representación de mallas 3D
2. Transformaciones geométricas
3. Proyección perspectiva
4. Rasterización de triángulos
5. Shading básico
"""

import numpy as np                                                          # Importa la biblioteca numpy para computación numérica
import math                                                               # Importa la biblioteca math para operaciones matemáticas
from PIL import Image  # Para manejo de imágenes                         # Importa la clase Image de la biblioteca PIL para manipulación de imágenes

class Vector3:                                                            # Define una nueva clase llamada Vector3
    """Clase para representar vectores en 3D y sus operaciones básicas""" # Documentación de la clase Vector3
    def __init__(self, x, y, z):                                           # Define el constructor de la clase Vector3
        self.x = x                                                        # Inicializa el componente x del vector
        self.y = y                                                        # Inicializa el componente y del vector
        self.z = z                                                        # Inicializa el componente z del vector
    
    def __add__(self, other):                                            # Define la sobrecarga del operador de suma
        """Suma de vectores componente a componente"""                      # Documentación del método __add__
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z) # Retorna un nuevo Vector3 con la suma de los componentes
    
    def __sub__(self, other):                                            # Define la sobrecarga del operador de resta
        """Resta de vectores componente a componente"""                      # Documentación del método __sub__
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z) # Retorna un nuevo Vector3 con la resta de los componentes
    
    def __mul__(self, scalar):                                          # Define la sobrecarga del operador de multiplicación por escalar
        """Multiplicación por escalar"""                                  # Documentación del método __mul__
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar) # Retorna un nuevo Vector3 con los componentes multiplicados por el escalar
    
    def dot(self, other):                                                # Define el método para calcular el producto punto
        """Producto punto entre vectores"""                               # Documentación del método dot
        return self.x*other.x + self.y*other.y + self.z*other.z             # Retorna el producto punto de los dos vectores
    
    def cross(self, other):                                              # Define el método para calcular el producto cruz
        """Producto cruz entre vectores"""                               # Documentación del método cross
        return Vector3(                                                  # Retorna un nuevo Vector3 que es el producto cruz
            self.y*other.z - self.z*other.y,                             # Calcula el componente x del producto cruz
            self.z*other.x - self.x*other.z,                             # Calcula el componente y del producto cruz
            self.x*other.y - self.y*other.x                              # Calcula el componente z del producto cruz
        )
    
    def normalize(self):                                              # Define el método para normalizar el vector
        """Normaliza el vector (longitud 1)"""                            # Documentación del método normalize
        length = math.sqrt(self.x**2 + self.y**2 + self.z**2)             # Calcula la longitud del vector
        return Vector3(self.x/length, self.y/length, self.z/length)       # Retorna un nuevo Vector3 con los componentes normalizados
    
    def to_array(self):                                                # Define el método para convertir a array numpy
        """Convierte a array numpy"""                                    # Documentación del método to_array
        return np.array([self.x, self.y, self.z])                        # Retorna un array numpy con los componentes del vector

class Matrix4:                                                            # Define una nueva clase llamada Matrix4
    """Clase para matrices 4x4 y operaciones de transformación"""       # Documentación de la clase Matrix4
    def __init__(self):                                                     # Define el constructor de la clase Matrix4
        # Inicializa como matriz identidad                               # Comentario explicando la inicialización
        self.m = np.identity(4, dtype=np.float32)                         # Inicializa la matriz como una matriz identidad de 4x4 de tipo float32
    
    @staticmethod                                                         # Indica que el siguiente método es estático
    def translation(tx, ty, tz):                                        # Define un método estático para crear una matriz de traslación
        """Crea matriz de traslación"""                                  # Documentación del método translation
        m = Matrix4()                                                    # Crea una nueva instancia de Matrix4
        m.m[0, 3] = tx                                                   # Establece el componente de traslación en x
        m.m[1, 3] = ty                                                   # Establece el componente de traslación en y
        m.m[2, 3] = tz                                                   # Establece el componente de traslación en z
        return m                                                         # Retorna la matriz de traslación
    
    @staticmethod                                                         # Indica que el siguiente método es estático
    def rotation_x(angle):                                              # Define un método estático para crear una matriz de rotación en el eje X
        """Crea matriz de rotación en eje X (en radianes)"""              # Documentación del método rotation_x
        m = Matrix4()                                                    # Crea una nueva instancia de Matrix4
        cos = math.cos(angle)                                            # Calcula el coseno del ángulo
        sin = math.sin(angle)                                            # Calcula el seno del ángulo
        m.m[1, 1] = cos                                                   # Establece el componente de rotación
        m.m[1, 2] = -sin                                                  # Establece el componente de rotación
        m.m[2, 1] = sin                                                   # Establece el componente de rotación
        m.m[2, 2] = cos                                                   # Establece el componente de rotación
        return m                                                         # Retorna la matriz de rotación en X
    
    @staticmethod                                                         # Indica que el siguiente método es estático
    def rotation_y(angle):                                              # Define un método estático para crear una matriz de rotación en el eje Y
        """Crea matriz de rotación en eje Y (en radianes)"""              # Documentación del método rotation_y
        m = Matrix4()                                                    # Crea una nueva instancia de Matrix4
        cos = math.cos(angle)                                            # Calcula el coseno del ángulo
        sin = math.sin(angle)                                            # Calcula el seno del ángulo
        m.m[0, 0] = cos                                                   # Establece el componente de rotación
        m.m[0, 2] = sin                                                   # Establece el componente de rotación
        m.m[2, 0] = -sin                                                  # Establece el componente de rotación
        m.m[2, 2] = cos                                                   # Establece el componente de rotación
        return m                                                         # Retorna la matriz de rotación en Y
    
    @staticmethod                                                         # Indica que el siguiente método es estático
    def perspective(fov, aspect, near, far):                            # Define un método estático para crear una matriz de proyección perspectiva
        """Crea matriz de proyección perspectiva"""                       # Documentación del método perspective
        m = Matrix4()                                                    # Crea una nueva instancia de Matrix4
        f = 1.0 / math.tan(fov * 0.5)                                    # Calcula el factor de escala de la perspectiva
        m.m[0, 0] = f / aspect                                           # Establece el componente de la matriz de perspectiva
        m.m[1, 1] = f                                                     # Establece el componente de la matriz de perspectiva
        m.m[2, 2] = (far + near) / (near - far)                         # Establece el componente de la matriz de perspectiva
        m.m[2, 3] = (2 * far * near) / (near - far)                     # Establece el componente de la matriz de perspectiva
        m.m[3, 2] = -1.0                                                  # Establece el componente de la matriz de perspectiva
        m.m[3, 3] = 0.0                                                    # Establece el componente de la matriz de perspectiva
        return m                                                         # Retorna la matriz de proyección perspectiva
    
    def multiply(self, other):                                          # Define el método para multiplicar la matriz actual por otra
        """Multiplica esta matriz por otra"""                            # Documentación del método multiply
        result = Matrix4()                                               # Crea una nueva instancia de Matrix4 para el resultado
        result.m = np.dot(self.m, other.m)                               # Realiza la multiplicación de matrices usando numpy.dot
        return result                                                    # Retorna la matriz resultante de la multiplicación
    
    def transform(self, vector):                                        # Define el método para aplicar la transformación a un vector 3D
        """Aplica transformación a un vector 3D (asume coordenadas homogéneas)""" # Documentación del método transform
        v = np.array([vector.x, vector.y, vector.z, 1.0])               # Convierte el Vector3 a un array numpy con coordenada homogénea
        transformed = np.dot(self.m, v)                                  # Multiplica la matriz de transformación por el vector
        return Vector3(                                                  # Retorna un nuevo Vector3 con las coordenadas transformadas
            transformed[0]/transformed[3],                             # Divide por la coordenada homogénea para obtener la coordenada x proyectada
            transformed[1]/transformed[3],                             # Divide por la coordenada homogénea para obtener la coordenada y proyectada
            transformed[2]/transformed[3]                              # Divide por la coordenada homogénea para obtener la coordenada z proyectada
        )

class Mesh:                                                               # Define una nueva clase llamada Mesh
    """Clase para representar mallas 3D (vértices y triángulos)"""       # Documentación de la clase Mesh
    def __init__(self):                                                     # Define el constructor de la clase Mesh
        self.vertices = []                                                # Inicializa una lista vacía para almacenar los vértices
        self.triangles = []  # Cada triángulo es índices de 3 vértices       # Inicializa una lista vacía para almacenar los triángulos (índices de vértices)
        self.colors = []    # Color para cada triángulo                     # Inicializa una lista vacía para almacenar los colores de cada triángulo
    
    def load_from_obj(self, filename):                                   # Define el método para cargar una malla desde un archivo OBJ
        """Carga malla desde archivo OBJ (formato estándar)"""              # Documentación del método load_from_obj
        with open(filename, 'r') as f:                                    # Abre el archivo OBJ en modo lectura
            for line in f:                                                # Itera sobre cada línea del archivo
                if line.startswith('v '):                                 # Si la línea comienza con 'v ', es una línea de vértice
                    # Línea de vértice: v x y z                             # Comentario explicando el formato de la línea de vértice
                    parts = line.split()                                 # Divide la línea en partes separadas por espacios
                    self.vertices.append(Vector3(                          # Crea un nuevo Vector3 con las coordenadas y lo añade a la lista de vértices
                        float(parts[1]),                                  # Convierte la segunda parte a float (coordenada x)
                        float(parts[2]),                                  # Convierte la tercera parte a float (coordenada y)
                        float(parts[3])                                   # Convierte la cuarta parte a float (coordenada z)
                    ))
                elif line.startswith('f '):                               # Si la línea comienza con 'f ', es una línea de cara (triángulo)
                    # Línea de cara: f v1 v2 v3                             # Comentario explicando el formato de la línea de cara
                    parts = line.split()                                 # Divide la línea en partes separadas por espacios
                    self.triangles.append([                               # Añade una lista de índices de vértices a la lista de triángulos
                        int(parts[1].split('/')[0]) - 1,                   # Obtiene el índice del primer vértice y lo ajusta a base 0
                        int(parts[2].split('/')[0]) - 1,                   # Obtiene el índice del segundo vértice y lo ajusta a base 0
                        int(parts[3].split('/')[0]) - 1                    # Obtiene el índice del tercer vértice y lo ajusta a base 0
                    ])
                    # Asigna color aleatorio al triángulo                   # Comentario explicando la asignación de color
                    self.colors.append((                                  # Añade una tupla con tres valores aleatorios (0-255) como color
                        np.random.randint(0, 255),                          # Genera un valor entero aleatorio para el componente rojo
                        np.random.randint(0, 255),                          # Genera un valor entero aleatorio para el componente verde
                        np.random.randint(0, 255)                           # Genera un valor entero aleatorio para el componente azul
                    ))

class Renderer:                                                             # Define una nueva clase llamada Renderer
    """Clase principal para renderizado"""                                # Documentación de la clase Renderer
    def __init__(self, width, height):                                    # Define el constructor de la clase Renderer
        self.width = width                                                # Inicializa el ancho del buffer de color
        self.height = height                                              # Inicializa la altura del buffer de color
        # Buffer de color (imagen RGB)                                    # Comentario explicando el buffer de color
        self.color_buffer = np.zeros((height, width, 3), dtype=np.uint8) # Inicializa un array numpy de ceros para el buffer de color (alto x ancho x 3 canales RGB)
        # Buffer de profundidad (para visible surface determination)       # Comentario explicando el buffer de profundidad
        self.depth_buffer = np.full((height, width), float('inf'))       # Inicializa un array numpy lleno de infinito para el buffer de profundidad
    
    def clear(self, color=(0, 0, 0)):                                     # Define el método para limpiar los buffers
        """Limpia los buffers con color especificado"""                    # Documentación del método clear
        self.color_buffer[:, :] = color                                  # Llena todo el buffer de color con el color especificado
        self.depth_buffer.fill(float('inf'))                             # Llena todo el buffer de profundidad con infinito
    
    def rasterize_triangle(self, v0, v1, v2, color):                      # Define el método para rasterizar un triángulo
        """Rasteriza un triángulo en los buffers"""                       # Documentación del método rasterize_triangle
        # Convertir coordenadas de pantalla a píxeles                    # Comentario explicando la conversión de coordenadas
        x0, y0 = int((v0.x + 1) * 0.5 * self.width), int((1 - (v0.y + 1) * 0.5) * self.height) # Convierte las coordenadas normalizadas a coordenadas de píxel
        x1, y1 = int((v1.x + 1) * 0.5 * self.width), int((1 - (v1.y + 1) * 0.5) * self.height) # Convierte las coordenadas normalizadas a coordenadas de píxel
        x2, y2 = int((v2.x + 1) * 0.5 * self.width), int((1 - (v2.y + 1) * 0.5) * self.height) # Convierte las coordenadas normalizadas a coordenadas de píxel
        
        # Calcular bounding box del triángulo                           # Comentario explicando el cálculo del bounding box
        min_x = max(0, min(x0, x1, x2))                                 # Calcula el mínimo x y lo asegura dentro de los límites
        max_x = min(self.width-1, max(x0, x1, x2))                      # Calcula el máximo x y lo asegura dentro de los límites
        min_y = max(0, min(y0, y1, y2))                                 # Calcula el mínimo y y lo asegura dentro de los límites
        max_y = min(self.height-1, max(y0, y1, y2))                    # Calcula el máximo y y lo asegura dentro de los límites
        
        # Función para calcular coordenadas baricéntricas                # Comentario explicando la función baricéntrica
        def barycentric(x, y):                                          # Define una función local para calcular coordenadas baricéntricas
            denom = (y1 - y2)*(x0 - x2) + (x2 - x1)*(y0 - y2)             # Calcula el denominador para las coordenadas baricéntricas
            a = ((y1 - y2)*(x - x2) + (x2 - x1)*(y - y2)) / denom       # Calcula la coordenada baricéntrica a
            b = ((y2 - y0)*(x - x2) + (x0 - x2)*(y - y2)) / denom       # Calcula la coordenada baricéntrica b
            c = 1 - a - b                                              # Calcula la coordenada baricéntrica c
            return a, b, c                                             # Retorna las coordenadas baricéntricas
        
        # Rasterizar cada píxel en el bounding box                      # Comentario explicando la rasterización