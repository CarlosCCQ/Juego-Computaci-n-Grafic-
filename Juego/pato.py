import random
import constantes
from cargar_animaciones import *

class Pato:
    def __init__(self, x, y, animaciones):
        self.x = x
        self.y = y
        self.animaciones = animaciones
        self.frame_actual = 0
        self.contador_retraso = 0

    def update(self):
        self.contador_retraso += 1
        if self.contador_retraso >= constantes.RETRASO_ANIMACION_PATO:
            self.contador_retraso = 0
            self.frame_actual = (self.frame_actual + 1) % len(self.animaciones)

    def dibujar(self, ventana):
        imagen_actual = self.animaciones[self.frame_actual]
        ventana.blit(imagen_actual, (self.x, self.y))


def inicializar_patos(nivel_suelo):
    plataformas_disponibles = []

    for fila_idx, fila in enumerate(nivel_suelo):
        for col_idx, celda in enumerate(fila):
            if celda in [0, 1, 2, 3, 18, 19, 20, 21]:
                plataformas_disponibles.append((col_idx, fila_idx))

    plataformas_seleccionadas = random.sample(
        plataformas_disponibles, min(constantes.NUM_MAX_PATOS, len(plataformas_disponibles))
    )

    patos = []
    for col_idx, fila_idx in plataformas_seleccionadas:
        x_pato = col_idx * constantes.TILE_SIZE
        invertir = random.choice([True, False])

        animaciones = cargar_animaciones_pato(constantes.SCALA_PATO, invertir)

        altura_sprite = animaciones[0].get_height()

        y_pato = (fila_idx * constantes.TILE_SIZE) - altura_sprite

        patos.append(Pato(x_pato, y_pato, animaciones))

    return patos