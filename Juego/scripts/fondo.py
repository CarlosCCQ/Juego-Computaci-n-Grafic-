import csv
import os
import pygame
from scripts import constantes

def cargar_fondo():
    ruta_base = os.path.dirname(__file__)
    ruta_csv_fondo = os.path.abspath(os.path.join(ruta_base + "/juego_csv/fondo.csv"))
    fondo = []
    with open(ruta_csv_fondo) as archivo_csv_fondo:
        lector = csv.reader(archivo_csv_fondo, delimiter=',')
        for fila in lector:
            fondo.append([int(celda) for celda in fila])
    return fondo


def dibujar_fondo(fondo, ventana):
    ruta_base = os.path.dirname(__file__)
    sprite_fondo = pygame.image.load(os.path.join(ruta_base + "/nivel/fondo/fondo.png"))
    for fila_idx, fila in enumerate(fondo):
        for col_idx, celda in enumerate(fila):
            if celda == 0:
                x = col_idx * constantes.TILE_SIZE
                y = fila_idx * constantes.TILE_SIZE
                ventana.blit(sprite_fondo, (x, y))