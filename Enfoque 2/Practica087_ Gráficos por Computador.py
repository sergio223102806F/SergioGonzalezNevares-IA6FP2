# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 13:43:57 2025

@author: elvin
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

import numpy as np
import math
from PIL import Image  # Para manejo de imágenes

class Vector3:
    """Clase para representar vectores en 3D y sus operaciones básicas"""
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other):
        """Suma de vectores componente a componente"""
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        """Resta de vectores componente a componente"""
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar):
        """Multiplicación por escalar"""
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def dot(self, other):
        """Producto punto entre vectores"""
        return self.x*other.x + self.y*other.y + self.z*other.z
    
    def cross(self, other):
        """Producto cruz entre vectores"""
        return Vector3(
            self.y*other.z - self.z*other.y,
            self.z*other.x - self.x*other.z,
            self.x*other.y - self.y*other.x
        )
    
    def normalize(self):
        """Normaliza el vector (longitud 1)"""
        length = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        return Vector3(self.x/length, self.y/length, self.z/length)
    
    def to_array(self):
        """Convierte a array numpy"""
        return np.array([self.x, self.y, self.z])

class Matrix4:
    """Clase para matrices 4x4 y operaciones de transformación"""
    def __init__(self):
        # Inicializa como matriz identidad
        self.m = np.identity(4, dtype=np.float32)
    
    @staticmethod
    def translation(tx, ty, tz):
        """Crea matriz de traslación"""
        m = Matrix4()
        m.m[0, 3] = tx
        m.m[1, 3] = ty
        m.m[2, 3] = tz
        return m
    
    @staticmethod
    def rotation_x(angle):
        """Crea matriz de rotación en eje X (en radianes)"""
        m = Matrix4()
        cos = math.cos(angle)
        sin = math.sin(angle)
        m.m[1, 1] = cos
        m.m[1, 2] = -sin
        m.m[2, 1] = sin
        m.m[2, 2] = cos
        return m
    
    @staticmethod
    def rotation_y(angle):
        """Crea matriz de rotación en eje Y (en radianes)"""
        m = Matrix4()
        cos = math.cos(angle)
        sin = math.sin(angle)
        m.m[0, 0] = cos
        m.m[0, 2] = sin
        m.m[2, 0] = -sin
        m.m[2, 2] = cos
        return m
    
    @staticmethod
    def perspective(fov, aspect, near, far):
        """Crea matriz de proyección perspectiva"""
        m = Matrix4()
        f = 1.0 / math.tan(fov * 0.5)
        m.m[0, 0] = f / aspect
        m.m[1, 1] = f
        m.m[2, 2] = (far + near) / (near - far)
        m.m[2, 3] = (2 * far * near) / (near - far)
        m.m[3, 2] = -1.0
        m.m[3, 3] = 0.0
        return m
    
    def multiply(self, other):
        """Multiplica esta matriz por otra"""
        result = Matrix4()
        result.m = np.dot(self.m, other.m)
        return result
    
    def transform(self, vector):
        """Aplica transformación a un vector 3D (asume coordenadas homogéneas)"""
        v = np.array([vector.x, vector.y, vector.z, 1.0])
        transformed = np.dot(self.m, v)
        return Vector3(
            transformed[0]/transformed[3],
            transformed[1]/transformed[3],
            transformed[2]/transformed[3]
        )

class Mesh:
    """Clase para representar mallas 3D (vértices y triángulos)"""
    def __init__(self):
        self.vertices = []
        self.triangles = []  # Cada triángulo es índices de 3 vértices
        self.colors = []      # Color para cada triángulo
    
    def load_from_obj(self, filename):
        """Carga malla desde archivo OBJ (formato estándar)"""
        with open(filename, 'r') as f:
            for line in f:
                if line.startswith('v '):
                    # Línea de vértice: v x y z
                    parts = line.split()
                    self.vertices.append(Vector3(
                        float(parts[1]),
                        float(parts[2]),
                        float(parts[3])
                    ))
                elif line.startswith('f '):
                    # Línea de cara: f v1 v2 v3
                    parts = line.split()
                    self.triangles.append([
                        int(parts[1].split('/')[0]) - 1,
                        int(parts[2].split('/')[0]) - 1,
                        int(parts[3].split('/')[0]) - 1
                    ])
                    # Asigna color aleatorio al triángulo
                    self.colors.append((
                        np.random.randint(0, 255),
                        np.random.randint(0, 255),
                        np.random.randint(0, 255)
                    ))

class Renderer:
    """Clase principal para renderizado"""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Buffer de color (imagen RGB)
        self.color_buffer = np.zeros((height, width, 3), dtype=np.uint8)
        # Buffer de profundidad (para visible surface determination)
        self.depth_buffer = np.full((height, width), float('inf'))
    
    def clear(self, color=(0, 0, 0)):
        """Limpia los buffers con color especificado"""
        self.color_buffer[:, :] = color
        self.depth_buffer.fill(float('inf'))
    
    def rasterize_triangle(self, v0, v1, v2, color):
        """Rasteriza un triángulo en los buffers"""
        # Convertir coordenadas de pantalla a píxeles
        x0, y0 = int((v0.x + 1) * 0.5 * self.width), int((1 - (v0.y + 1) * 0.5) * self.height)
        x1, y1 = int((v1.x + 1) * 0.5 * self.width), int((1 - (v1.y + 1) * 0.5) * self.height)
        x2, y2 = int((v2.x + 1) * 0.5 * self.width), int((1 - (v2.y + 1) * 0.5) * self.height)
        
        # Calcular bounding box del triángulo
        min_x = max(0, min(x0, x1, x2))
        max_x = min(self.width-1, max(x0, x1, x2))
        min_y = max(0, min(y0, y1, y2))
        max_y = min(self.height-1, max(y0, y1, y2))
        
        # Función para calcular coordenadas baricéntricas
        def barycentric(x, y):
            denom = (y1 - y2)*(x0 - x2) + (x2 - x1)*(y0 - y2)
            a = ((y1 - y2)*(x - x2) + (x2 - x1)*(y - y2)) / denom
            b = ((y2 - y0)*(x - x2) + (x0 - x2)*(y - y2)) / denom
            c = 1 - a - b
            return a, b, c
        
        # Rasterizar cada píxel en el bounding box
        for y in range(min_y, max_y+1):
            for x in range(min_x, max_x+1):
                a, b, c = barycentric(x, y)
                
                # Verificar si el punto está dentro del triángulo
                if a >= 0 and b >= 0 and c >= 0:
                    # Calcular profundidad interpolada
                    z = a*v0.z + b*v1.z + c*v2.z
                    
                    # Comprobar si es el píxel más cercano
                    if z < self.depth_buffer[y, x]:
                        self.depth_buffer[y, x] = z
                        self.color_buffer[y, x] = color
    
    def render_mesh(self, mesh, view_matrix, projection_matrix):
        """Renderiza una malla completa"""
        # Matriz de transformación completa
        mvp = projection_matrix.multiply(view_matrix)
        
        # Procesar cada triángulo
        for i, triangle in enumerate(mesh.triangles):
            # Obtener vértices del triángulo
            v0 = mesh.vertices[triangle[0]]
            v1 = mesh.vertices[triangle[1]]
            v2 = mesh.vertices[triangle[2]]
            
            # Aplicar transformaciones
            tv0 = mvp.transform(v0)
            tv1 = mvp.transform(v1)
            tv2 = mvp.transform(v2)
            
            # Calcular normal para backface culling
            normal = (tv1 - tv0).cross(tv2 - tv0)
            
            # Solo renderizar si la cara está orientada hacia la cámara
            if normal.z < 0:
                # Obtener color del triángulo
                color = mesh.colors[i]
                
                # Rasterizar triángulo
                self.rasterize_triangle(tv0, tv1, tv2, color)
    
    def save_image(self, filename):
        """Guarda el buffer de color como imagen PNG"""
        img = Image.fromarray(self.color_buffer, 'RGB')
        img.save(filename)

# Ejemplo de uso
if __name__ == "__main__":
    print("Renderizando escena 3D básica...")
    
    # 1. Crear renderizador con resolución 800x600
    renderer = Renderer(800, 600)
    renderer.clear(color=(50, 50, 100))  # Fondo azul oscuro
    
    # 2. Cargar malla 3D desde archivo OBJ
    mesh = Mesh()
    try:
        mesh.load_from_obj("cube.obj")  # Archivo debe existir
    except FileNotFoundError:
        # Crear cubo manualmente si no hay archivo
        print("Archivo no encontrado, usando cubo predeterminado")
        # Vértices del cubo
        mesh.vertices = [
            Vector3(-1,-1,-1), Vector3(1,-1,-1), Vector3(1,1,-1), Vector3(-1,1,-1),
            Vector3(-1,-1,1), Vector3(1,-1,1), Vector3(1,1,1), Vector3(-1,1,1)
        ]
        # Triángulos del cubo (12 triángulos, 2 por cara)
        mesh.triangles = [
            [0,1,2], [0,2,3], [1,5,6], [1,6,2],  # Cara frontal y derecha
            [5,4,7], [5,7,6], [4,0,3], [4,3,7],  # Cara trasera e izquierda
            [3,2,6], [3,6,7], [4,5,1], [4,1,0]   # Cara superior e inferior
        ]
        # Colores aleatorios para cada triángulo
        mesh.colors = [(np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)) 
                      for _ in range(12)]
    
    # 3. Configurar matrices de vista y proyección
    view_matrix = Matrix4.translation(0, 0, -5).multiply(
        Matrix4.rotation_y(math.radians(30)).multiply(
            Matrix4.rotation_x(math.radians(20))
        )
    )
    
    projection_matrix = Matrix4.perspective(
        fov=math.radians(60),  # Campo de visión 60 grados
        aspect=800/600,        # Relación de aspecto
        near=0.1,              # Plano cercano
        far=100.0              # Plano lejano
    )
    
    # 4. Renderizar la malla
    renderer.render_mesh(mesh, view_matrix, projection_matrix)
    
    # 5. Guardar resultado
    renderer.save_image("render.png")
    print("Imagen guardada como render.png")