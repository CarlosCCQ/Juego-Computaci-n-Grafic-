import pygame
import csv
import os
from scripts import constantes

def decoraciones_planta():
    ruta_base = os.path.dirname(__file__)
    decoraciones_sprites = {
        0: pygame.image.load(ruta_base +"/nivel/plantas/arbol (0).png"),
        1: pygame.image.load(ruta_base +"/nivel/plantas/arbol (1).png"),
        2: pygame.image.load(ruta_base +"/nivel/plantas/arbol (2).png"),
        3: pygame.image.load(ruta_base +"/nivel/plantas/arbol (3).png"),
        6: pygame.image.load(ruta_base +"/nivel/plantas/arbol (6).png"),
    }

    for key in decoraciones_sprites:
        decoraciones_sprites[key] = pygame.transform.scale(decoraciones_sprites[key], (constantes.TILE_SIZE, constantes.TILE_SIZE))

    return decoraciones_sprites

def cargar_decoraciones_planta():
    ruta_base = os.path.dirname(__file__)
    ruta_csv = os.path.join(ruta_base + "/juego_csv/plantas.csv")
    decoraciones = []
    with open(ruta_csv) as archivo_csv:
        lector = csv.reader(archivo_csv, delimiter=',')
        for fila in lector:
            decoraciones.append([int(celda) for celda in fila])
    return decoraciones

def dibujar_decoraciones_planta(decoraciones, decoraciones_sprites, ventana):
    for fila_idx, fila in enumerate(decoraciones):
        for col_idx, celda in enumerate(fila):
            if celda != -1:
                sprite = decoraciones_sprites.get(celda)
                if sprite:
                    x = col_idx * constantes.TILE_SIZE
                    y = fila_idx * constantes.TILE_SIZE
                    ventana.blit(sprite, (x, y))