# -*- coding: utf-8 -*-  # Especifica la codificación del archivo como UTF-8 para caracteres especiales
"""
Created on Sun Apr 27 13:43:57 2025  # Fecha de creación del archivo

@author: elvin  # Autor del código
"""

"""
Implementación de Filtros para Preprocesamiento de Imágenes  # Descripción general

Este código incluye:  # Lista de funcionalidades
1. Filtros de suavizado (media, gaussiano)  # Tipo de filtros
2. Filtros de realce (sobel, laplaciano)  # Filtros para bordes
3. Operaciones morfológicas (erosión, dilatación)  # Operaciones morfológicas
4. Conversiones de espacio de color  # Manejo de espacios de color
"""

import numpy as np  # Importa numpy para operaciones numéricas
import cv2  # OpenCV para operaciones de imagen  # Biblioteca principal de visión por computadora
from scipy import ndimage  # Para filtros más avanzados  # Filtros adicionales
import matplotlib.pyplot as plt  # Para visualización  # Para mostrar imágenes

class ImageProcessor:  # Define la clase principal del procesador de imágenes
    def __init__(self, image_path):  # Constructor de la clase
        """
        Inicializa el procesador de imágenes.
        
        Args:
            image_path (str): Ruta a la imagen a procesar  # Parámetro de entrada
        """
        self.image = cv2.imread(image_path)  # Carga la imagen en BGR  # Lee la imagen en formato BGR
        if self.image is None:  # Verifica si la imagen se cargó correctamente
            raise ValueError("No se pudo cargar la imagen")  # Lanza error si falla
        
        # Convierte a escala de grises por defecto para procesamiento  # Conversión estándar
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)  # Convierte BGR a escala de grises
        
    def show_image(self, title="Imagen", image=None, cmap='gray'):  # Método para mostrar imágenes
        """
        Muestra una imagen usando matplotlib.
        
        Args:
            title (str): Título de la ventana  # Título de la figura
            image: Imagen a mostrar (None para usar imagen actual)  # Imagen opcional
            cmap: Mapa de colores ('gray' para escala de grises)  # Mapa de colores
        """
        img_to_show = self.gray if image is None else image  # Decide qué imagen mostrar
        plt.figure(figsize=(8, 6))  # Crea figura de 8x6 pulgadas
        plt.imshow(img_to_show, cmap=cmap)  # Muestra la imagen
        plt.title(title)  # Añade título
        plt.axis('off')  # Oculta ejes
        plt.show()  # Muestra la figura

    def apply_mean_filter(self, kernel_size=3):  # Filtro de media
        """
        Aplica filtro de media (suavizado).
        
        Args:
            kernel_size (int): Tamaño del kernel (debe ser impar)  # Tamaño del kernel
            
        Returns:
            numpy.ndarray: Imagen filtrada  # Imagen resultante
        """
        # Valida el tamaño del kernel  # Validación de parámetro
        if kernel_size % 2 == 0:  # Verifica si es par
            raise ValueError("El tamaño del kernel debe ser impar")  # Error si es par
        
        # Crea kernel de media normalizado  # Preparación del kernel
        kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size**2)  # Kernel uniforme
        
        # Aplica convolución 2D  # Operación principal
        filtered = cv2.filter2D(self.gray, -1, kernel)  # Aplica filtro
        
        return filtered  # Devuelve imagen filtrada

    def apply_gaussian_filter(self, kernel_size=3, sigma=1.0):  # Filtro gaussiano
        """
        Aplica filtro gaussiano para suavizado.
        
        Args:
            kernel_size (int): Tamaño del kernel (debe ser impar)  # Tamaño del kernel
            sigma (float): Desviación estándar para distribución gaussiana  # Parámetro sigma
            
        Returns:
            numpy.ndarray: Imagen filtrada  # Resultado
        """
        # Valida parámetros  # Validación
        if kernel_size % 2 == 0:  # Comprueba si es par
            raise ValueError("El tamaño del kernel debe ser impar")  # Error si es par
        
        # Aplica filtro gaussiano  # Operación principal
        filtered = cv2.GaussianBlur(self.gray, (kernel_size, kernel_size), sigma)  # Filtro gaussiano
        
        return filtered  # Devuelve resultado

    def apply_median_filter(self, kernel_size=3):  # Filtro de mediana
        """
        Aplica filtro de mediana (elimina ruido sal y pimienta).
        
        Args:
            kernel_size (int): Tamaño del kernel (debe ser impar)  # Parámetro
            
        Returns:
            numpy.ndarray: Imagen filtrada  # Resultado
        """
        if kernel_size % 2 == 0:  # Validación
            raise ValueError("El tamaño del kernel debe ser impar")  # Error
        
        filtered = cv2.medianBlur(self.gray, kernel_size)  # Aplica filtro de mediana
        return filtered  # Devuelve resultado

    def apply_sobel_filter(self, direction='both'):  # Filtro Sobel
        """
        Aplica filtro Sobel para detección de bordes.
        
        Args:
            direction (str): 'x', 'y' o 'both' para dirección del gradiente  # Dirección
            
        Returns:
            numpy.ndarray: Imagen con bordes resaltados  # Resultado
        """
        # Calcula derivadas en dirección X e Y  # Operaciones
        sobelx = cv2.Sobel(self.gray, cv2.CV_64F, 1, 0, ksize=3)  # Derivada en X
        sobely = cv2.Sobel(self.gray, cv2.CV_64F, 0, 1, ksize=3)  # Derivada en Y
        
        # Combina según dirección solicitada  # Lógica de combinación
        if direction == 'x':  # Solo dirección X
            filtered = np.absolute(sobelx)  # Valor absoluto
        elif direction == 'y':  # Solo dirección Y
            filtered = np.absolute(sobely)  # Valor absoluto
        else:  # 'both'  # Ambas direcciones
            filtered = np.sqrt(sobelx**2 + sobely**2)  # Magnitud del gradiente
        
        # Normaliza a rango 0-255  # Normalización
        filtered = np.uint8(255 * filtered / np.max(filtered))  # Escala a 0-255
        return filtered  # Devuelve resultado

    def apply_laplacian_filter(self):  # Filtro Laplaciano
        """
        Aplica filtro Laplaciano para detección de bordes.
        
        Returns:
            numpy.ndarray: Imagen con bordes resaltados  # Resultado
        """
        # Aplica Laplaciano (segunda derivada)  # Operación
        laplacian = cv2.Laplacian(self.gray, cv2.CV_64F)  # Filtro Laplaciano
        
        # Normaliza y convierte a 8-bit  # Post-procesamiento
        filtered = np.uint8(np.absolute(laplacian))  # Valor absoluto y conversión
        return filtered  # Devuelve resultado

    def apply_bilateral_filter(self, d=9, sigma_color=75, sigma_space=75):  # Filtro bilateral
        """
        Filtro bilateral que preserva bordes mientras suaviza.
        
        Args:
            d: Diámetro de vecindario  # Parámetro
            sigma_color: Filtro en el espacio de color  # Sigma para color
            sigma_space: Filtro en el espacio geométrico  # Sigma para espacio
            
        Returns:
            numpy.ndarray: Imagen filtrada  # Resultado
        """
        filtered = cv2.bilateralFilter(self.gray, d, sigma_color, sigma_space)  # Aplica filtro
        return filtered  # Devuelve resultado

    def apply_morphological_operation(self, operation='erode', kernel_size=3):  # Operaciones morfológicas
        """
        Aplica operaciones morfológicas (erosión/dilatación).
        
        Args:
            operation (str): 'erode' o 'dilate'  # Tipo de operación
            kernel_size (int): Tamaño del kernel estructural  # Tamaño
            
        Returns:
            numpy.ndarray: Imagen procesada  # Resultado
        """
        # Crea kernel estructural  # Preparación
        kernel = np.ones((kernel_size, kernel_size), np.uint8)  # Kernel cuadrado
        
        # Aplica operación seleccionada  # Lógica
        if operation == 'erode':  # Erosión
            result = cv2.erode(self.gray, kernel, iterations=1)  # Aplica erosión
        elif operation == 'dilate':  # Dilatación
            result = cv2.dilate(self.gray, kernel, iterations=1)  # Aplica dilatación
        else:
            raise ValueError("Operación debe ser 'erode' o 'dilate'")  # Error
            
        return result  # Devuelve resultado

    def apply_histogram_equalization(self):  # Ecualización de histograma
        """
        Aplica ecualización de histograma para mejorar contraste.
        
        Returns:
            numpy.ndarray: Imagen ecualizada  # Resultado
        """
        # Ecualiza histograma en escala de grises  # Operación
        equalized = cv2.equalizeHist(self.gray)  # Ecualización
        return equalized  # Devuelve resultado

    def convert_to_hsv(self):  # Conversión a HSV
        """
        Convierte imagen de BGR a espacio de color HSV.
        
        Returns:
            numpy.ndarray: Imagen en espacio HSV  # Resultado
        """
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)  # Conversión
        return hsv  # Devuelve imagen HSV

    def apply_canny_edge_detection(self, threshold1=100, threshold2=200):  # Detección Canny
        """
        Detección de bordes con algoritmo Canny.
        
        Args:
            threshold1: Primer umbral para hysteresis  # Umbral bajo
            threshold2: Segundo umbral para hysteresis  # Umbral alto
            
        Returns:
            numpy.ndarray: Imagen con bordes detectados  # Resultado
        """
        edges = cv2.Canny(self.gray, threshold1, threshold2)  # Aplica Canny
        return edges  # Devuelve bordes

    def save_image(self, image, output_path):  # Guardar imagen
        """
        Guarda una imagen en disco.
        
        Args:
            image: Imagen a guardar  # Datos de imagen
            output_path (str): Ruta de salida  # Destino
        """
        cv2.imwrite(output_path, image)  # Escribe imagen

# Ejemplo de uso  # Bloque principal
if __name__ == "__main__":  # Ejecución directa
    try:  # Manejo de errores
        # 1. Crea procesador con imagen de ejemplo  # Paso 1
        processor = ImageProcessor("ejemplo.jpg")  # Instancia el procesador
        
        # 2. Muestra imagen original  # Paso 2
        processor.show_image("Original")  # Muestra original
        
        # 3. Aplica diferentes filtros  # Paso 3
        mean_filtered = processor.apply_mean_filter(5)  # Filtro de media
        processor.show_image("Filtro de Media", mean_filtered)  # Muestra resultado
        
        gaussian_filtered = processor.apply_gaussian_filter(5, 1.5)  # Filtro gaussiano
        processor.show_image("Filtro Gaussiano", gaussian_filtered)  # Muestra resultado
        
        sobel_edges = processor.apply_sobel_filter('both')  # Filtro Sobel
        processor.show_image("Bordes con Sobel", sobel_edges)  # Muestra bordes
        
        equalized = processor.apply_histogram_equalization()  # Ecualización
        processor.show_image("Histograma Ecualizado", equalized)  # Muestra resultado
        
        # 4. Guarda resultados  # Paso 4
        processor.save_image(gaussian_filtered, "suavizado.jpg")  # Guarda suavizado
        processor.save_image(sobel_edges, "bordes.jpg")  # Guarda bordes
        
        print("Procesamiento completado. Resultados guardados.")  # Mensaje final
        
    except Exception as e:  # Captura errores
        print(f"Error: {str(e)}")  # Muestra error