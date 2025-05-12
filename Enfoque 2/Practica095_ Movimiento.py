# -*- coding: utf-8 -*-                                                     # Define la codificación de caracteres del archivo como UTF-8
"""
Created on Sun Apr 27 14:22:45 2025                                         # Indica la fecha y hora de creación del archivo
                                                                           #
@author: elvin                                                              # Define el autor del archivo
"""

import cv2                                                                 # Importa la biblioteca OpenCV para procesamiento de imágenes

# Capturar video desde la webcam                                           # Comentario indicando la captura de video desde la webcam
camara = cv2.VideoCapture(0)                                               # Inicializa la captura de video desde la cámara predeterminada (índice 0)

# Leer el primer frame para comparar                                      # Comentario indicando la lectura del primer frame
ret, frame_anterior = camara.read()                                        # Lee el primer frame de la cámara
frame_anterior = cv2.cvtColor(frame_anterior, cv2.COLOR_BGR2GRAY)         # Convierte el primer frame a escala de grises
frame_anterior = cv2.GaussianBlur(frame_anterior, (21, 21), 0)            # Aplica un filtro gaussiano para suavizar el primer frame

while True:                                                               # Inicia un bucle infinito para el procesamiento continuo de video
    # Leer un nuevo frame                                                 # Comentario indicando la lectura de un nuevo frame
    ret, frame_actual = camara.read()                                     # Lee el siguiente frame de la cámara
    if not ret:                                                            # Verifica si la lectura del frame fue exitosa
        break                                                              # Sale del bucle si no se pudo leer un frame

    gris_actual = cv2.cvtColor(frame_actual, cv2.COLOR_BGR2GRAY)          # Convierte el frame actual a escala de grises
    gris_actual = cv2.GaussianBlur(gris_actual, (21, 21), 0)             # Aplica un filtro gaussiano para suavizar el frame actual

    # Comparar frames (diferencia absoluta)                                # Comentario indicando la comparación de frames
    diferencia = cv2.absdiff(frame_anterior, gris_actual)                 # Calcula la diferencia absoluta entre el frame anterior y el actual

    # Umbral para obtener regiones de movimiento                          # Comentario indicando la aplicación de un umbral
    _, umbral = cv2.threshold(diferencia, 25, 255, cv2.THRESH_BINARY)     # Aplica un umbral binario a la imagen de diferencia para resaltar el movimiento
    umbral = cv2.dilate(umbral, None, iterations=2)                      # Aplica una operación de dilatación para rellenar pequeños huecos en las regiones de movimiento

    # Buscar contornos en las áreas de movimiento                          # Comentario indicando la búsqueda de contornos
    contornos, _ = cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Encuentra los contornos externos en la imagen umbralizada

    for contorno in contornos:                                            # Itera sobre cada contorno encontrado
        if cv2.contourArea(contorno) < 500:                              # Ignora los contornos con un área menor a 500 píxeles (movimientos pequeños)
            continue                                                       # Continúa con el siguiente contorno si el área es demasiado pequeña
        # Dibujar rectángulo en el área que se mueve                      # Comentario indicando el dibujo de un rectángulo
        (x, y, w, h) = cv2.boundingRect(contorno)                         # Obtiene las coordenadas y dimensiones del rectángulo delimitador del contorno
        cv2.rectangle(frame_actual, (x, y), (x + w, y + h), (0, 255, 0), 2) # Dibuja un rectángulo verde alrededor del área de movimiento en el frame actual

    # Mostrar el video                                                    # Comentario indicando la visualización del video
    cv2.imshow('Detección de Movimiento', frame_actual)                   # Muestra el frame actual con los rectángulos de detección de movimiento

    # Actualizar el frame anterior                                        # Comentario indicando la actualización del frame anterior
    frame_anterior = gris_actual                                          # Actualiza el frame anterior con el frame actual en escala de grises

    # Salir con 'q'                                                      # Comentario indicando la condición de salida
    if cv2.waitKey(1) & 0xFF == ord('q'):                                 # Espera 1 milisegundo por una pulsación de tecla y verifica si es 'q'
        break                                                              # Sale del bucle si se presiona la tecla 'q'

# Liberar recursos                                                       # Comentario indicando la liberación de recursos
camara.release()                                                        # Libera el objeto de captura de video
cv2.destroyAllWindows()                                                   # Cierra todas las ventanas de OpenCV
