# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 13:43:57 2025

@author: elvin
"""
"""
Implementación de Detección de Aristas y Segmentación de Imágenes

Este código incluye:
1. Detección de bordes (Canny, Sobel, Laplaciano)
2. Transformada de Hough para detección de líneas/círculos
3. Segmentación por umbralización
4. Segmentación por watershed
5. Contornos y regiones conectadas
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.feature import canny
from skimage.segmentation import watershed
from skimage.filters import sobel
from scipy import ndimage as ndi

class EdgeSegmenter:
    def __init__(self, image_path):
        """
        Inicializa el procesador de imágenes.
        
        Args:
            image_path (str): Ruta a la imagen a procesar
        """
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise ValueError("No se pudo cargar la imagen")
        
        # Convertir a escala de grises para procesamiento
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        # Suavizar imagen para reducir ruido
        self.blurred = cv2.GaussianBlur(self.gray, (5, 5), 0)
    
    def show_images(self, images, titles=None, cmap='gray'):
        """
        Muestra múltiples imágenes en una sola figura.
        
        Args:
            images (list): Lista de imágenes a mostrar
            titles (list): Lista de títulos para cada imagen
            cmap (str): Mapa de colores para matplotlib
        """
        plt.figure(figsize=(15, 10))
        for i, img in enumerate(images):
            plt.subplot(1, len(images), i+1)
            plt.imshow(img, cmap=cmap)
            if titles and i < len(titles):
                plt.title(titles[i])
            plt.axis('off')
        plt.show()
    
    def detect_edges_canny(self, low_threshold=50, high_threshold=150):
        """
        Detección de bordes con algoritmo Canny.
        
        Args:
            low_threshold (int): Umbral inferior para hysteresis
            high_threshold (int): Umbral superior para hysteresis
            
        Returns:
            numpy.ndarray: Imagen binaria con bordes detectados
        """
        edges = cv2.Canny(self.blurred, low_threshold, high_threshold)
        return edges
    
    def detect_edges_sobel(self, ksize=3):
        """
        Detección de bordes usando operador Sobel.
        
        Args:
            ksize (int): Tamaño del kernel de Sobel
            
        Returns:
            numpy.ndarray: Magnitud del gradiente
        """
        # Calcular gradientes en X e Y
        grad_x = cv2.Sobel(self.blurred, cv2.CV_64F, 1, 0, ksize=ksize)
        grad_y = cv2.Sobel(self.blurred, cv2.CV_64F, 0, 1, ksize=ksize)
        
        # Calcular magnitud y dirección del gradiente
        magnitude = np.sqrt(grad_x**2 + grad_y**2)
        direction = np.arctan2(grad_y, grad_x)
        
        # Normalizar a rango 0-255
        magnitude = np.uint8(255 * magnitude / np.max(magnitude))
        
        return magnitude, direction
    
    def detect_edges_laplacian(self):
        """
        Detección de bordes usando Laplaciano.
        
        Returns:
            numpy.ndarray: Imagen con bordes resaltados
        """
        laplacian = cv2.Laplacian(self.blurred, cv2.CV_64F)
        laplacian = np.uint8(np.absolute(laplacian))
        return laplacian
    
    def hough_lines(self, edges, rho=1, theta=np.pi/180, threshold=100):
        """
        Detección de líneas rectas usando Transformada de Hough.
        
        Args:
            edges: Imagen binaria de bordes
            rho (float): Resolución de distancia en píxeles
            theta (float): Resolución angular en radianes
            threshold (int): Umbral mínimo de votos
            
        Returns:
            list: Lista de líneas detectadas (rho, theta)
            numpy.ndarray: Imagen con líneas dibujadas
        """
        lines = cv2.HoughLines(edges, rho, theta, threshold)
        
        # Crear imagen de salida con líneas dibujadas
        line_image = np.copy(self.image)
        
        if lines is not None:
            for line in lines:
                rho, theta = line[0]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))
                cv2.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        
        return lines, line_image
    
    def hough_circles(self, edges, min_dist=20, param1=50, param2=30, min_radius=0, max_radius=0):
        """
        Detección de círculos usando Transformada de Hough.
        
        Args:
            edges: Imagen binaria de bordes
            min_dist (int): Distancia mínima entre centros
            param1 (int): Umbral superior para Canny interno
            param2 (int): Umbral para detección de centros
            min_radius (int): Radio mínimo a detectar
            max_radius (int): Radio máximo a detectar
            
        Returns:
            numpy.ndarray: Círculos detectados (x, y, radio)
            numpy.ndarray: Imagen con círculos dibujados
        """
        circles = cv2.HoughCircles(
            edges, 
            cv2.HOUGH_GRADIENT, 
            dp=1, 
            minDist=min_dist,
            param1=param1,
            param2=param2,
            minRadius=min_radius,
            maxRadius=max_radius
        )
        
        # Crear imagen de salida con círculos dibujados
        circle_image = np.copy(self.image)
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                cv2.circle(circle_image, (i[0], i[1]), i[2], (0, 255, 0), 2)
                cv2.circle(circle_image, (i[0], i[1]), 2, (0, 0, 255), 3)
        
        return circles, circle_image
    
    def threshold_segmentation(self, thresh=127, maxval=255, mode='binary'):
        """
        Segmentación por umbralización.
        
        Args:
            thresh (int): Valor de umbral
            maxval (int): Valor máximo para píxeles sobre el umbral
            mode (str): Tipo de umbralización ('binary', 'otsu', 'adaptive')
            
        Returns:
            numpy.ndarray: Imagen binaria segmentada
        """
        if mode == 'binary':
            _, segmented = cv2.threshold(self.blurred, thresh, maxval, cv2.THRESH_BINARY)
        elif mode == 'otsu':
            _, segmented = cv2.threshold(self.blurred, 0, maxval, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        elif mode == 'adaptive':
            segmented = cv2.adaptiveThreshold(
                self.blurred, maxval, 
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 11, 2
            )
        else:
            raise ValueError("Modo debe ser 'binary', 'otsu' o 'adaptive'")
        
        return segmented
    
    def watershed_segmentation(self):
        """
        Segmentación usando algoritmo watershed.
        
        Returns:
            numpy.ndarray: Etiquetas de segmentación
            numpy.ndarray: Imagen con regiones coloreadas
        """
        # Aplicar umbralización para obtener marcadores
        ret, thresh = cv2.threshold(self.blurred, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        
        # Eliminar ruido con opening morfológico
        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
        
        # Encontrar área de fondo segura
        sure_bg = cv2.dilate(opening, kernel, iterations=3)
        
        # Encontrar área de primer plano segura
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        ret, sure_fg = cv2.threshold(dist_transform, 0.7*dist_transform.max(), 255, 0)
        sure_fg = np.uint8(sure_fg)
        
        # Encontrar región desconocida
        unknown = cv2.subtract(sure_bg, sure_fg)
        
        # Etiquetar marcadores
        ret, markers = cv2.connectedComponents(sure_fg)
        markers = markers + 1
        markers[unknown == 255] = 0
        
        # Aplicar watershed
        markers = cv2.watershed(self.image, markers)
        
        # Colorear las regiones
        colored = np.zeros_like(self.image, dtype=np.uint8)
        colored[markers == -1] = [255, 0, 0]  # Bordes en azul
        for label in np.unique(markers):
            if label > 1:
                colored[markers == label] = np.random.randint(0, 255, size=3)
        
        return markers, colored
    
    def find_contours(self, binary_image):
        """
        Encuentra contornos en una imagen binaria.
        
        Args:
            binary_image: Imagen binaria de entrada
            
        Returns:
            list: Lista de contornos encontrados
            numpy.ndarray: Imagen con contornos dibujados
        """
        contours, hierarchy = cv2.findContours(
            binary_image, 
            cv2.RETR_TREE, 
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        # Dibujar contornos en imagen original
        contour_image = np.copy(self.image)
        cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)
        
        return contours, contour_image
    
    def connected_components(self, binary_image):
        """
        Etiqueta componentes conectados en una imagen binaria.
        
        Args:
            binary_image: Imagen binaria de entrada
            
        Returns:
            numpy.ndarray: Mapa de etiquetas
            int: Número de componentes
            numpy.ndarray: Imagen coloreada por componente
        """
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_image)
        
        # Crear imagen coloreada aleatoriamente
        colored = np.zeros((labels.shape[0], labels.shape[1], 3), dtype=np.uint8)
        for label in range(1, num_labels):
            colored[labels == label] = np.random.randint(0, 255, size=3)
        
        return labels, num_labels, colored

# Ejemplo de uso
if __name__ == "__main__":
    try:
        # 1. Crear segmentador con imagen de ejemplo
        segmenter = EdgeSegmenter("imagen.jpg")
        
        # 2. Detección de bordes
        canny_edges = segmenter.detect_edges_canny()
        sobel_mag, _ = segmenter.detect_edges_sobel()
        laplacian = segmenter.detect_edges_laplacian()
        
        # Mostrar resultados de detección de bordes
        segmenter.show_images(
            [canny_edges, sobel_mag, laplacian],
            ["Canny", "Sobel", "Laplaciano"]
        )
        
        # 3. Detección de líneas y círculos
        _, lines_image = segmenter.hough_lines(canny_edges)
        _, circles_image = segmenter.hough_circles(canny_edges)
        
        segmenter.show_images(
            [lines_image, circles_image],
            ["Líneas Detectadas", "Círculos Detectados"]
        )
        
        # 4. Segmentación
        binary_seg = segmenter.threshold_segmentation(mode='otsu')
        _, watershed_seg = segmenter.watershed_segmentation()
        
        segmenter.show_images(
            [binary_seg, watershed_seg],
            ["Umbralización Otsu", "Watershed"],
            cmap=None
        )
        
        # 5. Contornos y componentes conectados
        _, contours_img = segmenter.find_contours(binary_seg)
        _, _, components_img = segmenter.connected_components(binary_seg)
        
        segmenter.show_images(
            [contours_img, components_img],
            ["Contornos", "Componentes Conectados"],
            cmap=None
        )
        
    except Exception as e:
        print(f"Error: {str(e)}")