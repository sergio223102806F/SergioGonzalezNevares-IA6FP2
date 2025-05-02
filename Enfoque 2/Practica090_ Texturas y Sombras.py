# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 13:43:58 2025

@author: elvin
"""

import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configurar ventana
ancho, alto = 800, 600
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Texturas y Sombras")

# Colores
BLANCO = (255, 255, 255)
GRIS = (100, 100, 100)

# Cargar una textura (imagen)
# Asegúrate de tener una imagen "textura.jpg" en tu carpeta
textura = pygame.image.load("textura.jpg")
textura = pygame.transform.scale(textura, (200, 200))

# Función para dibujar una sombra
def dibujar_sombra(x, y, ancho, alto):
    sombra = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    sombra.fill((0, 0, 0, 100))  # Negro con transparencia
    pantalla.blit(sombra, (x + 10, y + 10))  # Un poco desplazada para simular sombra

# Bucle principal
reloj = pygame.time.Clock()
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pantalla.fill(BLANCO)

    # Dibujar sombra primero
    dibujar_sombra(300, 200, 200, 200)

    # Luego dibujar la textura encima
    pantalla.blit(textura, (300, 200))

    pygame.display.update()
    reloj.tick(60)
