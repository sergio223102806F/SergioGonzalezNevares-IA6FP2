# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 14:20:50 2025

@author: elvin
"""

import cv2
import numpy as np

# Cargar imagen
# Usa tu propia imagen aquí o toma un frame de un video
imagen = cv2.imread('lineas.jpg')  # Asegúrate de tener una imagen llamada 'lineas.jpg'

# Convertir a escala de grises
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# Aplicar Canny para detectar bordes
bordes = cv2.Canny(gris, 50, 150, apertureSize=3)

# Detectar líneas usando la Transformada de Hough
lineas = cv2.HoughLinesP(bordes, 1, np.pi / 180, threshold=100, minLineLength=50, maxLineGap=10)

# Dibujar las líneas detectadas y etiquetarlas
if lineas is not None:
    for idx, linea in enumerate(lineas):
        x1, y1, x2, y2 = linea[0]
        color = (0, 255, 0)  # Verde
        cv2.line(imagen, (x1, y1), (x2, y2), color, 2)
        # Etiqueta de la línea
        etiqueta = f"Línea {idx+1}"
        cv2.putText(imagen, etiqueta, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

# Mostrar la imagen con las líneas etiquetadas
cv2.imshow('Líneas Detectadas', imagen)
cv2.waitKey(0)
cv2.destroyAllWindows()
