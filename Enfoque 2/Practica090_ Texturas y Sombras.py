# -*- coding: utf-8 -*-                                                     # Define la codificación de caracteres del archivo como UTF-8
"""
Created on Sun Apr 27 13:43:58 2025                                         # Indica la fecha y hora de creación del archivo
                                                                           #
@author: elvin                                                              # Define el autor del archivo
"""

import pygame                                                              # Importa la biblioteca Pygame para el desarrollo de juegos
import sys                                                                 # Importa la biblioteca sys para funcionalidades específicas del sistema

# Inicializar Pygame                                                      # Comentario indicando la inicialización de Pygame
pygame.init()                                                              # Inicializa todos los módulos importados de Pygame

# Configurar ventana                                                       # Comentario indicando la configuración de la ventana
ancho, alto = 800, 600                                                     # Define el ancho y el alto de la ventana
pantalla = pygame.display.set_mode((ancho, alto))                          # Crea la ventana de visualización con las dimensiones especificadas
pygame.display.set_caption("Texturas y Sombras")                           # Establece el título de la ventana

# Colores                                                                  # Comentario indicando la definición de colores
BLANCO = (255, 255, 255)                                                   # Define el color blanco en formato RGB
GRIS = (100, 100, 100)                                                     # Define el color gris en formato RGB

# Cargar una textura (imagen)                                              # Comentario indicando la carga de la textura
# Asegúrate de tener una imagen "textura.jpg" en tu carpeta                  # Instrucción para asegurarse de que el archivo de imagen exista
textura = pygame.image.load("textura.jpg")                                 # Carga la imagen desde el archivo "textura.jpg"
textura = pygame.transform.scale(textura, (200, 200))                      # Escala la textura cargada a un tamaño de 200x200 píxeles

# Función para dibujar una sombra                                         # Comentario indicando la definición de la función para dibujar la sombra
def dibujar_sombra(x, y, ancho, alto):                                     # Define una función llamada dibujar_sombra que toma las coordenadas y dimensiones
    sombra = pygame.Surface((ancho, alto), pygame.SRCALPHA)               # Crea una superficie transparente para dibujar la sombra
    sombra.fill((0, 0, 0, 100))  # Negro con transparencia                 # Rellena la superficie de la sombra con color negro y un valor de transparencia de 100
    pantalla.blit(sombra, (x + 10, y + 10))  # Un poco desplazada para simular sombra # Dibuja la superficie de la sombra en la pantalla, desplazada para crear el efecto

# Bucle principal                                                          # Comentario indicando el bucle principal del juego
reloj = pygame.time.Clock()                                              # Crea un objeto de reloj para controlar la velocidad de fotogramas
while True:                                                               # Inicia un bucle infinito para el juego
    for evento in pygame.event.get():                                     # Itera sobre todos los eventos que han ocurrido desde el último ciclo
        if evento.type == pygame.QUIT:                                   # Verifica si el tipo de evento es la solicitud de cierre de la ventana
            pygame.quit()                                                # Desinicializa todos los módulos de Pygame
            sys.exit()                                                   # Sale del programa

    pantalla.fill(BLANCO)                                                # Rellena la pantalla con el color blanco en cada fotograma

    # Dibujar sombra primero                                              # Comentario indicando que la sombra se dibuja primero
    dibujar_sombra(300, 200, 200, 200)                                   # Llama a la función para dibujar la sombra debajo de la textura

    # Luego dibujar la textura encima                                     # Comentario indicando que la textura se dibuja encima
    pantalla.blit(textura, (300, 200))                                   # Dibuja la textura en la pantalla en las coordenadas especificadas

    pygame.display.update()                                               # Actualiza toda la pantalla para mostrar los cambios
    reloj.tick(60)                                                       # Controla la velocidad de fotogramas máxima a 60 FPS