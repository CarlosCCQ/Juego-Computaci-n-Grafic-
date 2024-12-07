import random
from cargar_animaciones import *

class Loro:
    def __init__(self, x, y, escala):
        self.animaciones = cargar_animaciones_loro(escala)
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animaciones[self.frame_index]
        self.forma = self.image.get_rect()
        self.forma.topleft = (x, y)
        self.velocidad = random.choice([2, 3, 4])
        self.direccion = random.choice([-1, 1])
        self.flip = self.direccion == -1

    def update(self):
        cooldown_animaciones = 200
        if pygame.time.get_ticks() - self.update_time >= cooldown_animaciones:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

            if self.frame_index >= len(self.animaciones):
                self.frame_index = 0

            self.image = self.animaciones[self.frame_index]

        self.forma.x += self.velocidad * self.direccion

    def dibujar(self, ventana):
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        ventana.blit(imagen_flip, self.forma)

    def fuera_de_pantalla(self, ancho_ventana, alto_ventana):
        return (
            self.forma.right < 0 or self.forma.left > ancho_ventana or
            self.forma.bottom < 0 or self.forma.top > alto_ventana
        )