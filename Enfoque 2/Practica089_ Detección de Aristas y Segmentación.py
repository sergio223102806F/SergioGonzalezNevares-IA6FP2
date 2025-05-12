# -*- coding: utf-8 -*-  # Especifica la codificación del archivo como UTF-8
"""
Created on Sun Apr 27 13:43:57 2025  # Fecha de creación del archivo

@author: elvin  # Autor del código
"""
"""
Implementación de Detección de Aristas y Segmentación de Imágenes  # Descripción general

Este código incluye:  # Lista de funcionalidades
1. Detección de bordes (Canny, Sobel, Laplaciano)  # Métodos de detección
2. Transformada de Hough para detección de líneas/círculos  # Detección de formas
3. Segmentación por umbralización  # Métodos de segmentación
4. Segmentación por watershed  # Algoritmo avanzado
5. Contornos y regiones conectadas  # Análisis de componentes
"""

import cv2  # Biblioteca principal para visión por computadora
import numpy as np  # Para operaciones numéricas con arrays
import matplotlib.pyplot as plt  # Para visualización de imágenes
from skimage.feature import canny  # Implementación alternativa de Canny
from skimage.segmentation import watershed  # Algoritmo watershed
from skimage.filters import sobel  # Filtro Sobel de scikit-image
from scipy import ndimage as ndi  # Para operaciones morfológicas

class EdgeSegmenter:  # Clase principal para detección y segmentación
    def __init__(self, image_path):  # Constructor de la clase
        """
        Inicializa el procesador de imágenes.
        
        Args:
            image_path (str): Ruta a la imagen a procesar  # Parámetro de entrada
        """
        self.image = cv2.imread(image_path)  # Carga la imagen en formato BGR
        if self.image is None:  # Verifica si la carga fue exitosa
            raise ValueError("No se pudo cargar la imagen")  # Lanza error si falla
        
        # Convertir a escala de grises para procesamiento  # Pre-procesamiento
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)  # Conversión a grises
        
        # Suavizar imagen para reducir ruido  # Pre-procesamiento
        self.blurred = cv2.GaussianBlur(self.gray, (5, 5), 0)  # Filtro Gaussiano
    
    def show_images(self, images, titles=None, cmap='gray'):  # Método para visualización
        """
        Muestra múltiples imágenes en una sola figura.
        
        Args:
            images (list): Lista de imágenes a mostrar  # Imágenes a visualizar
            titles (list): Lista de títulos para cada imagen  # Títulos opcionales
            cmap (str): Mapa de colores para matplotlib  # Paleta de colores
        """
        plt.figure(figsize=(15, 10))  # Crea figura de 15x10 pulgadas
        for i, img in enumerate(images):  # Itera sobre las imágenes
            plt.subplot(1, len(images), i+1)  # Crea subplot para cada imagen
            plt.imshow(img, cmap=cmap)  # Muestra la imagen
            if titles and i < len(titles):  # Si hay títulos disponibles
                plt.title(titles[i])  # Añade título al subplot
            plt.axis('off')  # Oculta los ejes
        plt.show()  # Muestra la figura completa
    
    def detect_edges_canny(self, low_threshold=50, high_threshold=150):  # Detección Canny
        """
        Detección de bordes con algoritmo Canny.
        
        Args:
            low_threshold (int): Umbral inferior para hysteresis  # Umbral bajo
            high_threshold (int): Umbral superior para hysteresis  # Umbral alto
            
        Returns:
            numpy.ndarray: Imagen binaria con bordes detectados  # Resultado
        """
        edges = cv2.Canny(self.blurred, low_threshold, high_threshold)  # Aplica Canny
        return edges  # Devuelve imagen de bordes
    
    def detect_edges_sobel(self, ksize=3):  # Detección Sobel
        """
        Detección de bordes usando operador Sobel.
        
        Args:
            ksize (int): Tamaño del kernel de Sobel  # Tamaño del filtro
            
        Returns:
            numpy.ndarray: Magnitud del gradiente  # Resultado principal
            numpy.ndarray: Dirección del gradiente  # Resultado secundario
        """
        # Calcular gradientes en X e Y  # Derivadas direccionales
        grad_x = cv2.Sobel(self.blurred, cv2.CV_64F, 1, 0, ksize=ksize)  # Derivada X
        grad_y = cv2.Sobel(self.blurred, cv2.CV_64F, 0, 1, ksize=ksize)  # Derivada Y
        
        # Calcular magnitud y dirección del gradiente  # Cálculos
        magnitude = np.sqrt(grad_x**2 + grad_y**2)  # Magnitud del gradiente
        direction = np.arctan2(grad_y, grad_x)  # Dirección del gradiente
        
        # Normalizar a rango 0-255  # Preparación para visualización
        magnitude = np.uint8(255 * magnitude / np.max(magnitude))  # Escalado
        
        return magnitude, direction  # Devuelve ambos resultados
    
    def detect_edges_laplacian(self):  # Detección Laplaciano
        """
        Detección de bordes usando Laplaciano.
        
        Returns:
            numpy.ndarray: Imagen con bordes resaltados  # Resultado
        """
        laplacian = cv2.Laplacian(self.blurred, cv2.CV_64F)  # Aplica Laplaciano
        laplacian = np.uint8(np.absolute(laplacian))  # Valor absoluto y conversión
        return laplacian  # Devuelve resultado
    
    def hough_lines(self, edges, rho=1, theta=np.pi/180, threshold=100):  # Transformada Hough para líneas
        """
        Detección de líneas rectas usando Transformada de Hough.
        
        Args:
            edges: Imagen binaria de bordes  # Entrada necesaria
            rho (float): Resolución de distancia en píxeles  # Parámetro
            theta (float): Resolución angular en radianes  # Parámetro
            threshold (int): Umbral mínimo de votos  # Sensibilidad
            
        Returns:
            list: Lista de líneas detectadas (rho, theta)  # Resultado crudo
            numpy.ndarray: Imagen con líneas dibujadas  # Visualización
        """
        lines = cv2.HoughLines(edges, rho, theta, threshold)  # Detecta líneas
        
        # Crear imagen de salida con líneas dibujadas  # Preparación visualización
        line_image = np.copy(self.image)  # Copia de la imagen original
        
        if lines is not None:  # Si se detectaron líneas
            for line in lines:  # Para cada línea detectada
                rho, theta = line[0]  # Obtiene parámetros
                a = np.cos(theta)  # Calcula componentes
                b = np.sin(theta)  # Calcula componentes
                x0 = a * rho  # Punto en la línea
                y0 = b * rho  # Punto en la línea
                # Calcula puntos extremos para dibujar
                x1 = int(x0 + 1000 * (-b))  # Punto final 1
                y1 = int(y0 + 1000 * (a))  # Punto final 1
                x2 = int(x0 - 1000 * (-b))  # Punto final 2
                y2 = int(y0 - 1000 * (a))  # Punto final 2
                # Dibuja línea en la imagen
                cv2.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        
        return lines, line_image  # Devuelve ambos resultados
    
    def hough_circles(self, edges, min_dist=20, param1=50, param2=30, min_radius=0, max_radius=0):  # Hough para círculos
        """
        Detección de círculos usando Transformada de Hough.
        
        Args:
            edges: Imagen binaria de bordes  # Entrada necesaria
            min_dist (int): Distancia mínima entre centros  # Parámetro
            param1 (int): Umbral superior para Canny interno  # Parámetro
            param2 (int): Umbral para detección de centros  # Sensibilidad
            min_radius (int): Radio mínimo a detectar  # Filtro
            max_radius (int): Radio máximo a detectar  # Filtro
            
        Returns:
            numpy.ndarray: Círculos detectados (x, y, radio)  # Resultado crudo
            numpy.ndarray: Imagen con círculos dibujados  # Visualización
        """
        circles = cv2.HoughCircles(  # Llama a la función de detección
            edges, 
            cv2.HOUGH_GRADIENT,  # Método a usar
            dp=1,  # Resolución
            minDist=min_dist,  # Distancia mínima
            param1=param1,  # Umbral alto
            param2=param2,  # Umbral de acumulador
            minRadius=min_radius,  # Radio mínimo
            maxRadius=max_radius  # Radio máximo
        )
        
        # Crear imagen de salida con círculos dibujados  # Preparación visualización
        circle_image = np.copy(self.image)  # Copia de la imagen original
        
        if circles is not None:  # Si se detectaron círculos
            circles = np.uint16(np.around(circles))  # Redondea y convierte
            for i in circles[0, :]:  # Para cada círculo
                # Dibuja el círculo exterior
                cv2.circle(circle_image, (i[0], i[1]), i[2], (0, 255, 0), 2)
                # Dibuja el centro del círculo
                cv2.circle(circle_image, (i[0], i[1]), 2, (0, 0, 255), 3)
        
        return circles, circle_image  # Devuelve ambos resultados
    
    def threshold_segmentation(self, thresh=127, maxval=255, mode='binary'):  # Segmentación por umbral
        """
        Segmentación por umbralización.
        
        Args:
            thresh (int): Valor de umbral  # Umbral fijo
            maxval (int): Valor máximo para píxeles sobre el umbral  # Valor de salida
            mode (str): Tipo de umbralización ('binary', 'otsu', 'adaptive')  # Método
            
        Returns:
            numpy.ndarray: Imagen binaria segmentada  # Resultado
        """
        if mode == 'binary':  # Umbralización simple
            _, segmented = cv2.threshold(self.blurred, thresh, maxval, cv2.THRESH_BINARY)
        elif mode == 'otsu':  # Umbralización automática
            _, segmented = cv2.threshold(self.blurred, 0, maxval, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        elif mode == 'adaptive':  # Umbralización adaptativa
            segmented = cv2.adaptiveThreshold(
                self.blurred, maxval, 
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,  # Método adaptativo
                cv2.THRESH_BINARY, 11, 2  # Parámetros adicionales
            )
        else:
            raise ValueError("Modo debe ser 'binary', 'otsu' o 'adaptive'")  # Error
        
        return segmented  # Devuelve imagen segmentada
    
    def watershed_segmentation(self):  # Segmentación por watershed
        """
        Segmentación usando algoritmo watershed.
        
        Returns:
            numpy.ndarray: Etiquetas de segmentación  # Resultado crudo
            numpy.ndarray: Imagen con regiones coloreadas  # Visualización
        """
        # Aplicar umbralización para obtener marcadores  # Paso 1
        ret, thresh = cv2.threshold(self.blurred, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        
        # Eliminar ruido con opening morfológico  # Paso 2
        kernel = np.ones((3, 3), np.uint8)  # Kernel 3x3
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
        
        # Encontrar área de fondo segura  # Paso 3
        sure_bg = cv2.dilate(opening, kernel, iterations=3)
        
        # Encontrar área de primer plano segura  # Paso 4
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)  # Transformada de distancia
        ret, sure_fg = cv2.threshold(dist_transform, 0.7*dist_transform.max(), 255, 0)
        sure_fg = np.uint8(sure_fg)
        
        # Encontrar región desconocida  # Paso 5
        unknown = cv2.subtract(sure_bg, sure_fg)
        
        # Etiquetar marcadores  # Paso 6
        ret, markers = cv2.connectedComponents(sure_fg)
        markers = markers + 1  # Ajuste de índices
        markers[unknown == 255] = 0  # Región desconocida
        
        # Aplicar watershed  # Paso principal
        markers = cv2.watershed(self.image, markers)
        
        # Colorear las regiones  # Preparación visualización
        colored = np.zeros_like(self.image, dtype=np.uint8)  # Imagen vacía
        colored[markers == -1] = [255, 0, 0]  # Bordes en azul
        for label in np.unique(markers):  # Para cada región
            if label > 1:  # Ignorar fondo y bordes
                colored[markers == label] = np.random.randint(0, 255, size=3)  # Color aleatorio
        
        return markers, colored  # Devuelve ambos resultados
    
    def find_contours(self, binary_image):  # Encontrar contornos
        """
        Encuentra contornos en una imagen binaria.
        
        Args:
            binary_image: Imagen binaria de entrada  # Segmentada
            
        Returns:
            list: Lista de contornos encontrados  # Resultado crudo
            numpy.ndarray: Imagen con contornos dibujados  # Visualización
        """
        contours, hierarchy = cv2.findContours(  # Función de OpenCV
            binary_image, 
            cv2.RETR_TREE,  # Método de recuperación
            cv2.CHAIN_APPROX_SIMPLE  # Método de aproximación
        )
        
        # Dibujar contornos en imagen original  # Preparación visualización
        contour_image = np.copy(self.image)  # Copia de la original
        cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)  # Dibuja todos
        
        return contours, contour_image  # Devuelve ambos resultados
    
    def connected_components(self, binary_image):  # Componentes conectados
        """
        Etiqueta componentes conectados en una imagen binaria.
        
        Args:
            binary_image: Imagen binaria de entrada  # Segmentada
            
        Returns:
            numpy.ndarray: Mapa de etiquetas  # Resultado crudo
            int: Número de componentes  # Conteo
            numpy.ndarray: Imagen coloreada por componente  # Visualización
        """
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_image)
        
        # Crear imagen coloreada aleatoriamente  # Preparación visualización
        colored = np.zeros((labels.shape[0], labels.shape[1], 3), dtype=np.uint8)  # Imagen RGB
        for label in range(1, num_labels):  # Para cada componente (ignorando fondo)
            colored[labels == label] = np.random.randint(0, 255, size=3)  # Color aleatorio
        
        return labels, num_labels, colored  # Devuelve múltiples resultados

# Ejemplo de uso  # Bloque principal
if __name__ == "__main__":  # Ejecución directa
    try:  # Manejo de errores
        # 1. Crear segmentador con imagen de ejemplo  # Paso 1
        segmenter = EdgeSegmenter("imagen.jpg")  # Instancia el objeto
        
        # 2. Detección de bordes  # Paso 2
        canny_edges = segmenter.detect_edges_canny()  # Canny
        sobel_mag, _ = segmenter.detect_edges_sobel()  # Sobel
        laplacian = segmenter.detect_edges_laplacian()  # Laplaciano
        
        # Mostrar resultados de detección de bordes  # Visualización
        segmenter.show_images(
            [canny_edges, sobel_mag, laplacian],  # Imágenes
            ["Canny", "Sobel", "Laplaciano"]  # Títulos
        )
        
        # 3. Detección de líneas y círculos  # Paso 3
        _, lines_image = segmenter.hough_lines(canny_edges)  # Líneas
        _, circles_image = segmenter.hough_circles(canny_edges)  # Círculos
        
        segmenter.show_images(  # Visualización
            [lines_image, circles_image],  # Imágenes
            ["Líneas Detectadas", "Círculos Detectados"]  # Títulos
        )
        
        # 4. Segmentación  # Paso 4
        binary_seg = segmenter.threshold_segmentation(mode='otsu')  # Otsu
        _, watershed_seg = segmenter.watershed_segmentation()  # Watershed
        
        segmenter.show_images(  # Visualización
            [binary_seg, watershed_seg],  # Imágenes
            ["Umbralización Otsu", "Watershed"],  # Títulos
            cmap=None  # Usar colores para watershed
        )
        
        # 5. Contornos y componentes conectados  # Paso 5
        _, contours_img = segmenter.find_contours(binary_seg)  # Contornos
        _, _, components_img = segmenter.connected_components(binary_seg)  # Componentes
        
        segmenter.show_images(  # Visualización final
            [contours_img, components_img],  # Imágenes
            ["Contornos", "Componentes Conectados"],  # Títulos
            cmap=None  # Usar colores
        )
        
    except Exception as e:  # Captura errores
        print(f"Error: {str(e)}")  # Muestra mensaje de error