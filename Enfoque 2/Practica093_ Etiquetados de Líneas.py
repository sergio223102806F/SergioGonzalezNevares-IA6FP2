# -*- coding: utf-8 -*-                                                     # Define la codificación de caracteres del archivo como UTF-8
"""
Created on Sun Apr 27 14:20:50 2025                                         # Indica la fecha y hora de creación del archivo
                                                                           #
@author: elvin                                                              # Define el autor del archivo
"""

import cv2                                                                 # Importa la biblioteca OpenCV para procesamiento de imágenes
import numpy as np                                                          # Importa la biblioteca NumPy para operaciones numéricas

# Cargar imagen                                                            # Comentario indicando la carga de la imagen
# Usa tu propia imagen aquí o toma un frame de un video                    # Instrucción para usar una imagen propia
imagen = cv2.imread('lineas.jpg')  # Asegúrate de tener una imagen llamada 'lineas.jpg' # Lee la imagen desde el archivo 'lineas.jpg'

# Convertir a escala de grises                                              # Comentario indicando la conversión a escala de grises
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)                            # Convierte la imagen de espacio de color BGR a escala de grises

# Aplicar Canny para detectar bordes                                        # Comentario indicando la aplicación del detector de bordes Canny
bordes = cv2.Canny(gris, 50, 150, apertureSize=3)                         # Aplica el detector de bordes Canny a la imagen en escala de grises

# Detectar líneas usando la Transformada de Hough                           # Comentario indicando la detección de líneas usando la Transformada de Hough
lineas = cv2.HoughLinesP(bordes, 1, np.pi / 180, threshold=100, minLineLength=50, maxLineGap=10) # Detecta líneas en la imagen de bordes usando la Transformada de Hough probabilística

# Dibujar las líneas detectadas y etiquetarlas                             # Comentario indicando el dibujo y etiquetado de las líneas
if lineas is not None:                                                    # Verifica si se detectaron líneas
    for idx, linea in enumerate(lineas):                                  # Itera sobre cada línea detectada con su índice
        x1, y1, x2, y2 = linea[0]                                        # Extrae las coordenadas de los puntos finales de la línea
        color = (0, 255, 0)  # Verde                                      # Define el color verde para dibujar las líneas
        cv2.line(imagen, (x1, y1), (x2, y2), color, 2)                   # Dibuja una línea verde en la imagen original entre los puntos detectados
        # Etiqueta de la línea                                              # Comentario indicando la etiqueta de la línea
        etiqueta = f"Línea {idx+1}"                                      # Crea una etiqueta para la línea con su número
        cv2.putText(imagen, etiqueta, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1) # Coloca la etiqueta de texto cerca del punto inicial de la línea

# Mostrar la imagen con las líneas etiquetadas                           # Comentario indicando la visualización de la imagen con las líneas
cv2.imshow('Líneas Detectadas', imagen)                                  # Muestra la imagen con las líneas detectadas en una ventana
cv2.waitKey(0)                                                           # Espera hasta que se presione una tecla
cv2.destroyAllWindows()                                                  # Cierra todas las ventanas de OpenCV
