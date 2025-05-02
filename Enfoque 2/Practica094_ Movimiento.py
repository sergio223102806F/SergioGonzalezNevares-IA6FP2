# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 14:21:43 2025

@author: elvin
"""

"""
Sistema de Detección de Movimiento en Tiempo Real

Este código implementa:
1. Captura de video en tiempo real
2. Resta de fondo para detección de movimiento
3. Filtrado y procesamiento de contornos
4. Visualización de resultados
5. Registro de eventos de movimiento
"""

import cv2
import numpy as np
import datetime
import time

class MotionDetector:
    def __init__(self, video_source=0, min_area=500, sensitivity=30):
        """
        Inicializa el detector de movimiento.
        
        Args:
            video_source: Fuente de video (0 para cámara predeterminada)
            min_area (int): Área mínima para considerar movimiento (en píxeles)
            sensitivity (int): Sensibilidad para la detección (1-100)
        """
        self.video_source = video_source
        self.min_area = min_area
        self.sensitivity = sensitivity
        
        # Inicializar captura de video
        self.cap = cv2.VideoCapture(self.video_source)
        if not self.cap.isOpened():
            raise ValueError("No se pudo abrir la fuente de video")
        
        # Configurar resolución (opcional)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Inicializar substractor de fondo
        self.fgbg = cv2.createBackgroundSubtractorMOG2(
            history=500, 
            varThreshold=16, 
            detectShadows=True
        )
        
        # Variables para estado y registro
        self.motion_detected = False
        self.last_motion_time = None
        self.motion_log = []
        
        # Kernel para operaciones morfológicas
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    
    def adjust_sensitivity(self, value):
        """Ajusta la sensibilidad de detección (1-100)."""
        self.sensitivity = max(1, min(100, value))
        # Ajustar umbral del substractor de fondo
        self.fgbg.setVarThreshold(100 - self.sensitivity)
    
    def process_frame(self, frame):
        """
        Procesa un frame para detectar movimiento.
        
        Args:
            frame: Frame de video a procesar
            
        Returns:
            tuple: (frame procesado, máscara de movimiento, lista de contornos)
        """
        # Aplicar substractor de fondo
        fgmask = self.fgbg.apply(frame)
        
        # Aplicar operaciones morfológicas para reducir ruido
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, self.kernel)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, self.kernel)
        
        # Encontrar contornos en la máscara
        contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filtrar contornos pequeños
        valid_contours = []
        motion_detected = False
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > self.min_area:
                valid_contours.append(cnt)
                motion_detected = True
        
        # Dibujar resultados en el frame original
        processed_frame = frame.copy()
        cv2.drawContours(processed_frame, valid_contours, -1, (0, 255, 0), 2)
        
        # Actualizar estado de movimiento
        self.update_motion_state(motion_detected)
        
        return processed_frame, fgmask, valid_contours
    
    def update_motion_state(self, current_detection):
        """
        Actualiza el estado de detección de movimiento y registra eventos.
        
        Args:
            current_detection (bool): Si se detectó movimiento en el frame actual
        """
        now = datetime.datetime.now()
        
        if current_detection:
            self.last_motion_time = now
            if not self.motion_detected:
                # Nuevo evento de movimiento
                self.motion_detected = True
                event = {
                    'start_time': now,
                    'end_time': None,
                    'duration': None
                }
                self.motion_log.append(event)
                print(f"Movimiento detectado a las {now.strftime('%H:%M:%S')}")
        else:
            if self.motion_detected:
                # Verificar si el movimiento ha terminado
                if self.last_motion_time and (now - self.last_motion_time).seconds > 1:
                    self.motion_detected = False
                    if self.motion_log:
                        self.motion_log[-1]['end_time'] = now
                        self.motion_log[-1]['duration'] = (now - self.motion_log[-1]['start_time']).seconds
                        print(f"Movimiento terminado después de {self.motion_log[-1]['duration']} segundos")
    
    def run(self):
        """
        Ejecuta el bucle principal de detección de movimiento.
        """
        print("Iniciando detección de movimiento...")
        print("Presione 'q' para salir")
        
        try:
            while True:
                # Leer frame del video
                ret, frame = self.cap.read()
                if not ret:
                    print("Error al leer el frame")
                    break
                
                # Redimensionar frame (opcional)
                frame = cv2.resize(frame, (640, 480))
                
                # Procesar frame para detectar movimiento
                processed_frame, fgmask, contours = self.process_frame(frame)
                
                # Mostrar información en pantalla
                self.display_info(processed_frame, len(contours))
                
                # Mostrar ventanas
                cv2.imshow('Video Original', frame)
                cv2.imshow('Detección de Movimiento', processed_frame)
                cv2.imshow('Máscara de Movimiento', fgmask)
                
                # Salir con la tecla 'q'
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
                # Pequeña pausa para reducir uso de CPU
                time.sleep(0.01)
                
        except KeyboardInterrupt:
            print("Interrupción por usuario")
        finally:
            # Liberar recursos
            self.cap.release()
            cv2.destroyAllWindows()
            self.generate_report()
    
    def display_info(self, frame, contour_count):
        """
        Muestra información sobre el estado de detección en el frame.
        
        Args:
            frame: Frame donde dibujar la información
            contour_count: Número de contornos detectados
        """
        # Mostrar estado actual
        status = "MOVIMIENTO DETECTADO" if self.motion_detected else "Sin movimiento"
        color = (0, 0, 255) if self.motion_detected else (0, 255, 0)
        
        # Dibujar texto en el frame
        cv2.putText(frame, f"Estado: {status}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        cv2.putText(frame, f"Contornos: {contour_count}", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Sensibilidad: {self.sensitivity}", (10, 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Mostrar última vez que se detectó movimiento
        if self.last_motion_time:
            last_time = self.last_motion_time.strftime("%H:%M:%S")
            cv2.putText(frame, f"Ultimo movimiento: {last_time}", (10, 120), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    def generate_report(self):
        """Genera un reporte de los eventos de movimiento detectados."""
        print("\nReporte de Detección de Movimiento:")
        print("=" * 40)
        
        if not self.motion_log:
            print("No se detectó movimiento durante la sesión")
            return
        
        total_duration = sum(
            event['duration'] or 0 
            for event in self.motion_log 
            if event['duration'] is not None
        )
        
        print(f"Total de eventos: {len(self.motion_log)}")
        print(f"Tiempo total de movimiento: {total_duration} segundos")
        print("\nDetalle de eventos:")
        
        for i, event in enumerate(self.motion_log, 1):
            start = event['start_time'].strftime("%H:%M:%S")
            end = event['end_time'].strftime("%H:%M:%S") if event['end_time'] else "En curso"
            duration = event['duration'] or "N/A"
            print(f"{i}. Inicio: {start} - Fin: {end} - Duración: {duration}s")

# Ejemplo de uso
if __name__ == "__main__":
    try:
        # Crear detector de movimiento (0 para cámara predeterminada)
        detector = MotionDetector(video_source=0, min_area=1000, sensitivity=50)
        
        # Ajustar sensibilidad si es necesario
        # detector.adjust_sensitivity(70)
        
        # Ejecutar el detector
        detector.run()
        
    except Exception as e:
        print(f"Error: {str(e)}")