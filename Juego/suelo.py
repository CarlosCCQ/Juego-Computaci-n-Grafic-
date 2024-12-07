import pygame
import csv
import os
import constantes


def cargar_sprites_nivel():
    ruta_base = os.path.dirname(__file__)
    tile_sprites_nivel = {}
    for tile_id in [0, 1, 2, 3, 18, 19, 20, 21]:
        ruta = ruta_base + f"/tiled ({tile_id}).png"
        tile_sprites_nivel[tile_id] = pygame.image.load(ruta)
        tile_sprites_nivel[tile_id] = pygame.transform.scale(tile_sprites_nivel[tile_id], (
        constantes.TILE_SIZE, constantes.TILE_SIZE))

    tile_sprites_nivel[-1] = None
    return tile_sprites_nivel

def cargar_nivel():
    ruta_base = os.path.dirname(__file__)
    ruta_csv = os.path.join(ruta_base + "/suelo.csv")
    nivel = []
    with open(ruta_csv) as archivo_csv:
        lector = csv.reader(archivo_csv, delimiter=',')
        for fila in lector:
            nivel.append([int(celda) for celda in fila])
    return nivel

def dibujar_nivel(nivel, tile_sprites_nivel, ventana):
    for fila_idx, fila in enumerate(nivel):
        for col_idx, celda in enumerate(fila):
            if celda != -1:
                sprite = tile_sprites_nivel.get(celda)
                if sprite:
                    ventana.blit(sprite, (col_idx * constantes.TILE_SIZE, fila_idx * constantes.TILE_SIZE))