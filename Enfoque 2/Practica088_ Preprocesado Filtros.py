# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 13:43:57 2025

@author: elvin
"""

"""
Implementación de Filtros para Preprocesamiento de Imágenes

Este código incluye:
1. Filtros de suavizado (media, gaussiano)
2. Filtros de realce (sobel, laplaciano)
3. Operaciones morfológicas (erosión, dilatación)
4. Conversiones de espacio de color
"""

import numpy as np
import cv2  # OpenCV para operaciones de imagen
from scipy import ndimage  # Para filtros más avanzados
import matplotlib.pyplot as plt  # Para visualización

class ImageProcessor:
    def __init__(self, image_path):
        """
        Inicializa el procesador de imágenes.
        
        Args:
            image_path (str): Ruta a la imagen a procesar
        """
        self.image = cv2.imread(image_path)  # Carga la imagen en BGR
        if self.image is None:
            raise ValueError("No se pudo cargar la imagen")
        
        # Convierte a escala de grises por defecto para procesamiento
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
    def show_image(self, title="Imagen", image=None, cmap='gray'):
        """
        Muestra una imagen usando matplotlib.
        
        Args:
            title (str): Título de la ventana
            image: Imagen a mostrar (None para usar imagen actual)
            cmap: Mapa de colores ('gray' para escala de grises)
        """
        img_to_show = self.gray if image is None else image
        plt.figure(figsize=(8, 6))
        plt.imshow(img_to_show, cmap=cmap)
        plt.title(title)
        plt.axis('off')
        plt.show()

    def apply_mean_filter(self, kernel_size=3):
        """
        Aplica filtro de media (suavizado).
        
        Args:
            kernel_size (int): Tamaño del kernel (debe ser impar)
            
        Returns:
            numpy.ndarray: Imagen filtrada
        """
        # Valida el tamaño del kernel
        if kernel_size % 2 == 0:
            raise ValueError("El tamaño del kernel debe ser impar")
        
        # Crea kernel de media normalizado
        kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size**2)
        
        # Aplica convolución 2D
        filtered = cv2.filter2D(self.gray, -1, kernel)
        
        return filtered

    def apply_gaussian_filter(self, kernel_size=3, sigma=1.0):
        """
        Aplica filtro gaussiano para suavizado.
        
        Args:
            kernel_size (int): Tamaño del kernel (debe ser impar)
            sigma (float): Desviación estándar para distribución gaussiana
            
        Returns:
            numpy.ndarray: Imagen filtrada
        """
        # Valida parámetros
        if kernel_size % 2 == 0:
            raise ValueError("El tamaño del kernel debe ser impar")
        
        # Aplica filtro gaussiano
        filtered = cv2.GaussianBlur(self.gray, (kernel_size, kernel_size), sigma)
        
        return filtered

    def apply_median_filter(self, kernel_size=3):
        """
        Aplica filtro de mediana (elimina ruido sal y pimienta).
        
        Args:
            kernel_size (int): Tamaño del kernel (debe ser impar)
            
        Returns:
            numpy.ndarray: Imagen filtrada
        """
        if kernel_size % 2 == 0:
            raise ValueError("El tamaño del kernel debe ser impar")
        
        filtered = cv2.medianBlur(self.gray, kernel_size)
        return filtered

    def apply_sobel_filter(self, direction='both'):
        """
        Aplica filtro Sobel para detección de bordes.
        
        Args:
            direction (str): 'x', 'y' o 'both' para dirección del gradiente
            
        Returns:
            numpy.ndarray: Imagen con bordes resaltados
        """
        # Calcula derivadas en dirección X e Y
        sobelx = cv2.Sobel(self.gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(self.gray, cv2.CV_64F, 0, 1, ksize=3)
        
        # Combina según dirección solicitada
        if direction == 'x':
            filtered = np.absolute(sobelx)
        elif direction == 'y':
            filtered = np.absolute(sobely)
        else:  # 'both'
            filtered = np.sqrt(sobelx**2 + sobely**2)
        
        # Normaliza a rango 0-255
        filtered = np.uint8(255 * filtered / np.max(filtered))
        return filtered

    def apply_laplacian_filter(self):
        """
        Aplica filtro Laplaciano para detección de bordes.
        
        Returns:
            numpy.ndarray: Imagen con bordes resaltados
        """
        # Aplica Laplaciano (segunda derivada)
        laplacian = cv2.Laplacian(self.gray, cv2.CV_64F)
        
        # Normaliza y convierte a 8-bit
        filtered = np.uint8(np.absolute(laplacian))
        return filtered

    def apply_bilateral_filter(self, d=9, sigma_color=75, sigma_space=75):
        """
        Filtro bilateral que preserva bordes mientras suaviza.
        
        Args:
            d: Diámetro de vecindario
            sigma_color: Filtro en el espacio de color
            sigma_space: Filtro en el espacio geométrico
            
        Returns:
            numpy.ndarray: Imagen filtrada
        """
        filtered = cv2.bilateralFilter(self.gray, d, sigma_color, sigma_space)
        return filtered

    def apply_morphological_operation(self, operation='erode', kernel_size=3):
        """
        Aplica operaciones morfológicas (erosión/dilatación).
        
        Args:
            operation (str): 'erode' o 'dilate'
            kernel_size (int): Tamaño del kernel estructural
            
        Returns:
            numpy.ndarray: Imagen procesada
        """
        # Crea kernel estructural
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        
        # Aplica operación seleccionada
        if operation == 'erode':
            result = cv2.erode(self.gray, kernel, iterations=1)
        elif operation == 'dilate':
            result = cv2.dilate(self.gray, kernel, iterations=1)
        else:
            raise ValueError("Operación debe ser 'erode' o 'dilate'")
            
        return result

    def apply_histogram_equalization(self):
        """
        Aplica ecualización de histograma para mejorar contraste.
        
        Returns:
            numpy.ndarray: Imagen ecualizada
        """
        # Ecualiza histograma en escala de grises
        equalized = cv2.equalizeHist(self.gray)
        return equalized

    def convert_to_hsv(self):
        """
        Convierte imagen de BGR a espacio de color HSV.
        
        Returns:
            numpy.ndarray: Imagen en espacio HSV
        """
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        return hsv

    def apply_canny_edge_detection(self, threshold1=100, threshold2=200):
        """
        Detección de bordes con algoritmo Canny.
        
        Args:
            threshold1: Primer umbral para hysteresis
            threshold2: Segundo umbral para hysteresis
            
        Returns:
            numpy.ndarray: Imagen con bordes detectados
        """
        edges = cv2.Canny(self.gray, threshold1, threshold2)
        return edges

    def save_image(self, image, output_path):
        """
        Guarda una imagen en disco.
        
        Args:
            image: Imagen a guardar
            output_path (str): Ruta de salida
        """
        cv2.imwrite(output_path, image)

# Ejemplo de uso
if __name__ == "__main__":
    try:
        # 1. Crea procesador con imagen de ejemplo
        processor = ImageProcessor("ejemplo.jpg")
        
        # 2. Muestra imagen original
        processor.show_image("Original")
        
        # 3. Aplica diferentes filtros
        mean_filtered = processor.apply_mean_filter(5)
        processor.show_image("Filtro de Media", mean_filtered)
        
        gaussian_filtered = processor.apply_gaussian_filter(5, 1.5)
        processor.show_image("Filtro Gaussiano", gaussian_filtered)
        
        sobel_edges = processor.apply_sobel_filter('both')
        processor.show_image("Bordes con Sobel", sobel_edges)
        
        equalized = processor.apply_histogram_equalization()
        processor.show_image("Histograma Ecualizado", equalized)
        
        # 4. Guarda resultados
        processor.save_image(gaussian_filtered, "suavizado.jpg")
        processor.save_image(sobel_edges, "bordes.jpg")
        
        print("Procesamiento completado. Resultados guardados.")
        
    except Exception as e:
        print(f"Error: {str(e)}")