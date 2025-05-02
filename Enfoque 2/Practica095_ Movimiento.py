# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 14:22:45 2025

@author: elvin
"""

import cv2

# Capturar video desde la webcam
camara = cv2.VideoCapture(0)

# Leer el primer frame para comparar
ret, frame_anterior = camara.read()
frame_anterior = cv2.cvtColor(frame_anterior, cv2.COLOR_BGR2GRAY)
frame_anterior = cv2.GaussianBlur(frame_anterior, (21, 21), 0)

while True:
    # Leer un nuevo frame
    ret, frame_actual = camara.read()
    if not ret:
        break

    gris_actual = cv2.cvtColor(frame_actual, cv2.COLOR_BGR2GRAY)
    gris_actual = cv2.GaussianBlur(gris_actual, (21, 21), 0)

    # Comparar frames (diferencia absoluta)
    diferencia = cv2.absdiff(frame_anterior, gris_actual)

    # Umbral para obtener regiones de movimiento
    _, umbral = cv2.threshold(diferencia, 25, 255, cv2.THRESH_BINARY)
    umbral = cv2.dilate(umbral, None, iterations=2)

    # Buscar contornos en las áreas de movimiento
    contornos, _ = cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contorno in contornos:
        if cv2.contourArea(contorno) < 500:  # Ignorar movimientos pequeños
            continue
        # Dibujar rectángulo en el área que se mueve
        (x, y, w, h) = cv2.boundingRect(contorno)
        cv2.rectangle(frame_actual, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Mostrar el video
    cv2.imshow('Detección de Movimiento', frame_actual)

    # Actualizar el frame anterior
    frame_anterior = gris_actual

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
camara.release()
cv2.destroyAllWindows()
