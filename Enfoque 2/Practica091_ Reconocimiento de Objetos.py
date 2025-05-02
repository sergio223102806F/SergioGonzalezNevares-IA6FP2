# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 14:17:22 2025

@author: elvin
"""

import cv2

# Cargar el clasificador Haar Cascade para detección de caras
detector_cara = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Capturar video de la webcam
camara = cv2.VideoCapture(0)

while True:
    # Leer un frame
    ret, frame = camara.read()
    if not ret:
        break

    # Convertir a escala de grises (necesario para Haar Cascade)
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar caras
    caras = detector_cara.detectMultiScale(gris, scaleFactor=1.1, minNeighbors=5)

    # Dibujar un rectángulo alrededor de cada cara detectada
    for (x, y, w, h) in caras:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    # Mostrar el frame
    cv2.imshow('Detección de Caras', frame)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar ventanas
camara.release()
cv2.destroyAllWindows()
