# -*- coding: utf-8 -*-  # Especifica la codificación del archivo como UTF-8
"""
Created on Sun Apr 27 14:21:43 2025  # Fecha de creación del archivo

@author: elvin  # Autor del código
"""

"""
Sistema de Detección de Movimiento en Tiempo Real  # Descripción general

Este código implementa:  # Lista de funcionalidades
1. Captura de video en tiempo real  # Video processing
2. Resta de fondo para detección de movimiento  # Background subtraction
3. Filtrado y procesamiento de contornos  # Contour processing
4. Visualización de resultados  # Visualization
5. Registro de eventos de movimiento  # Event logging
"""

import cv2  # OpenCV para procesamiento de video
import numpy as np  # Para operaciones numéricas
import datetime  # Para manejo de fechas/horas
import time  # Para pausas y medición de tiempo

class MotionDetector:  # Clase principal del detector de movimiento
    def __init__(self, video_source=0, min_area=500, sensitivity=30):  # Constructor
        """
        Inicializa el detector de movimiento.
        
        Args:
            video_source: Fuente de video (0 para cámara predeterminada)  # Cámara o archivo
            min_area (int): Área mínima para considerar movimiento (en píxeles)  # Filtro
            sensitivity (int): Sensibilidad para la detección (1-100)  # Ajuste
        """
        self.video_source = video_source  # Guarda la fuente de video
        self.min_area = min_area  # Área mínima para detección
        self.sensitivity = sensitivity  # Nivel de sensibilidad
        
        # Inicializar captura de video  # Configuración de video
        self.cap = cv2.VideoCapture(self.video_source)  # Objeto de captura
        if not self.cap.isOpened():  # Verifica si se abrió correctamente
            raise ValueError("No se pudo abrir la fuente de video")  # Error
        
        # Configurar resolución (opcional)  # Ajustes de cámara
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Ancho
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Alto
        
        # Inicializar substractor de fondo  # Background subtractor
        self.fgbg = cv2.createBackgroundSubtractorMOG2(  # Algoritmo MOG2
            history=500,  # Número de frames para modelo de fondo
            varThreshold=16,  # Umbral de varianza
            detectShadows=True  # Detección de sombras
        )
        
        # Variables para estado y registro  # Tracking
        self.motion_detected = False  # Estado actual
        self.last_motion_time = None  # Última detección
        self.motion_log = []  # Registro de eventos
        
        # Kernel para operaciones morfológicas  # Procesamiento de imagen
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # Kernel elíptico
    
    def adjust_sensitivity(self, value):  # Ajuste de sensibilidad
        """Ajusta la sensibilidad de detección (1-100)."""
        self.sensitivity = max(1, min(100, value))  # Limita el rango
        # Ajustar umbral del substractor de fondo  # Configura algoritmo
        self.fgbg.setVarThreshold(100 - self.sensitivity)  # Umbral inverso
    
    def process_frame(self, frame):  # Procesamiento de frame
        """
        Procesa un frame para detectar movimiento.
        
        Args:
            frame: Frame de video a procesar  # Input
            
        Returns:
            tuple: (frame procesado, máscara de movimiento, lista de contornos)  # Outputs
        """
        # Aplicar substractor de fondo  # Paso 1: Resta de fondo
        fgmask = self.fgbg.apply(frame)  # Crea máscara de primer plano
        
        # Aplicar operaciones morfológicas para reducir ruido  # Paso 2: Filtrado
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, self.kernel)  # Opening
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, self.kernel)  # Closing
        
        # Encontrar contornos en la máscara  # Paso 3: Detección de contornos
        contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filtrar contornos pequeños  # Paso 4: Filtrado por área
        valid_contours = []  # Contornos válidos
        motion_detected = False  # Estado temporal
        for cnt in contours:  # Para cada contorno
            area = cv2.contourArea(cnt)  # Calcula área
            if area > self.min_area:  # Filtra por tamaño
                valid_contours.append(cnt)  # Añade a lista
                motion_detected = True  # Actualiza estado
        
        # Dibujar resultados en el frame original  # Paso 5: Visualización
        processed_frame = frame.copy()  # Copia del frame
        cv2.drawContours(processed_frame, valid_contours, -1, (0, 255, 0), 2)  # Dibuja contornos
        
        # Actualizar estado de movimiento  # Paso 6: Tracking
        self.update_motion_state(motion_detected)  # Llama a método
        
        return processed_frame, fgmask, valid_contours  # Retorna resultados
    
    def update_motion_state(self, current_detection):  # Actualización de estado
        """
        Actualiza el estado de detección de movimiento y registra eventos.
        
        Args:
            current_detection (bool): Si se detectó movimiento en el frame actual  # Input
        """
        now = datetime.datetime.now()  # Timestamp actual
        
        if current_detection:  # Si hay movimiento
            self.last_motion_time = now  # Actualiza último tiempo
            if not self.motion_detected:  # Si es nuevo evento
                # Nuevo evento de movimiento  # Logging
                self.motion_detected = True  # Actualiza estado
                event = {  # Crea diccionario de evento
                    'start_time': now,  # Inicio
                    'end_time': None,  # Fin (aún no)
                    'duration': None  # Duración (aún no)
                }
                self.motion_log.append(event)  # Añade al log
                print(f"Movimiento detectado a las {now.strftime('%H:%M:%S')}")  # Console output
        else:  # Si no hay movimiento
            if self.motion_detected:  # Pero había movimiento antes
                # Verificar si el movimiento ha terminado  # Transición
                if self.last_motion_time and (now - self.last_motion_time).seconds > 1:  # Timeout
                    self.motion_detected = False  # Actualiza estado
                    if self.motion_log:  # Si hay eventos registrados
                        self.motion_log[-1]['end_time'] = now  # Establece fin
                        self.motion_log[-1]['duration'] = (now - self.motion_log[-1]['start_time']).seconds  # Calcula duración
                        print(f"Movimiento terminado después de {self.motion_log[-1]['duration']} segundos")  # Console output
    
    def run(self):  # Método principal
        """
        Ejecuta el bucle principal de detección de movimiento.
        """
        print("Iniciando detección de movimiento...")  # Mensaje inicial
        print("Presione 'q' para salir")  # Instrucciones
        
        try:  # Manejo de errores
            while True:  # Bucle infinito
                # Leer frame del video  # Captura
                ret, frame = self.cap.read()  # Lee frame
                if not ret:  # Si falla
                    print("Error al leer el frame")  # Mensaje
                    break  # Sale del bucle
                
                # Redimensionar frame (opcional)  # Pre-procesamiento
                frame = cv2.resize(frame, (640, 480))  # Estándar
                
                # Procesar frame para detectar movimiento  # Procesamiento
                processed_frame, fgmask, contours = self.process_frame(frame)
                
                # Mostrar información en pantalla  # UI
                self.display_info(processed_frame, len(contours))
                
                # Mostrar ventanas  # Visualización
                cv2.imshow('Video Original', frame)  # Frame original
                cv2.imshow('Detección de Movimiento', processed_frame)  # Procesado
                cv2.imshow('Máscara de Movimiento', fgmask)  # Máscara
                
                # Salir con la tecla 'q'  # Control
                if cv2.waitKey(1) & 0xFF == ord('q'):  # Espera tecla
                    break  # Sale del bucle
                
                # Pequeña pausa para reducir uso de CPU  # Optimización
                time.sleep(0.01)  # 10ms
                
        except KeyboardInterrupt:  # Captura Ctrl+C
            print("Interrupción por usuario")  # Mensaje
        finally:  # Limpieza
            # Liberar recursos  # Good practices
            self.cap.release()  # Libera cámara
            cv2.destroyAllWindows()  # Cierra ventanas
            self.generate_report()  # Reporte final
    
    def display_info(self, frame, contour_count):  # UI overlay
        """
        Muestra información sobre el estado de detección en el frame.
        
        Args:
            frame: Frame donde dibujar la información  # Canvas
            contour_count: Número de contornos detectados  # Info
        """
        # Mostrar estado actual  # Texto 1
        status = "MOVIMIENTO DETECTADO" if self.motion_detected else "Sin movimiento"  # Estado
        color = (0, 0, 255) if self.motion_detected else (0, 255, 0)  # Color (rojo/verde)
        
        # Dibujar texto en el frame  # Overlays
        cv2.putText(frame, f"Estado: {status}", (10, 30),  # Posición
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)  # Texto estado
        cv2.putText(frame, f"Contornos: {contour_count}", (10, 60),  # Posición
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)  # Texto contornos
        cv2.putText(frame, f"Sensibilidad: {self.sensitivity}", (10, 90),  # Posición
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)  # Texto sensibilidad
        
        # Mostrar última vez que se detectó movimiento  # Texto adicional
        if self.last_motion_time:  # Si hay registro
            last_time = self.last_motion_time.strftime("%H:%M:%S")  # Formato
            cv2.putText(frame, f"Ultimo movimiento: {last_time}", (10, 120),  # Posición
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)  # Texto pequeño
    
    def generate_report(self):  # Reporte final
        """Genera un reporte de los eventos de movimiento detectados."""
        print("\nReporte de Detección de Movimiento:")  # Encabezado
        print("=" * 40)  # Separador
        
        if not self.motion_log:  # Si no hay eventos
            print("No se detectó movimiento durante la sesión")  # Mensaje
            return  # Termina
        
        total_duration = sum(  # Calcula tiempo total
            event['duration'] or 0  # Duración o 0
            for event in self.motion_log  # Para cada evento
            if event['duration'] is not None  # Si tiene duración
        )
        
        print(f"Total de eventos: {len(self.motion_log)}")  # Resumen
        print(f"Tiempo total de movimiento: {total_duration} segundos")  # Resumen
        print("\nDetalle de eventos:")  # Sub-encabezado
        
        for i, event in enumerate(self.motion_log, 1):  # Lista enumerada
            start = event['start_time'].strftime("%H:%M:%S")  # Formato inicio
            end = event['end_time'].strftime("%H:%M:%S") if event['end_time'] else "En curso"  # Formato fin
            duration = event['duration'] or "N/A"  # Duración o N/A
            print(f"{i}. Inicio: {start} - Fin: {end} - Duración: {duration}s")  # Línea por evento

# Ejemplo de uso  # Bloque principal
if __name__ == "__main__":  # Ejecución directa
    try:  # Manejo de errores
        # Crear detector de movimiento (0 para cámara predeterminada)  # Instancia
        detector = MotionDetector(video_source=0, min_area=1000, sensitivity=50)  # Configuración
        
        # Ajustar sensibilidad si es necesario  # Opcional
        # detector.adjust_sensitivity(70)  # Ejemplo
        
        # Ejecutar el detector  # Inicia
        detector.run()  # Método principal
        
    except Exception as e:  # Captura errores
        print(f"Error: {str(e)}")  # Mensaje de error