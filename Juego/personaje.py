from cargar_animaciones import *

class Personaje:
    def __init__(self, x, y, escala):
        ruta_base = os.path.dirname(__file__)
        ruta_absoluta_agua = os.path.join(ruta_base + "/scripts/animaciones/personaje_agua")
        ruta_absoluta_saltando = os.path.join(ruta_base + "/scripts/animaciones/personaje_saltando")
        ruta_absoluta_caminando = os.path.join(ruta_base + "/scripts/animaciones/personaje_caminando")
        ruta_absoluta_reposo = os.path.join(ruta_base + "/scripts/animaciones/personaje_reposo")
        self.energia = 100
        self.flip = False
        self.estado = "reposo"
        self.animaciones = {
            "agua": cargar_animaciones_personaje(ruta_absoluta_agua, escala),
            "saltando": cargar_animaciones_personaje(ruta_absoluta_saltando, escala),
            "caminando": cargar_animaciones_personaje(ruta_absoluta_caminando, escala),
            "reposo": cargar_animaciones_personaje(ruta_absoluta_reposo, escala)
        }
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animaciones[self.estado][self.frame_index]
        self.forma = self.image.get_rect()
        self.forma.center = (x, y)

    def cambiar_estado(self, nuevo_estado):
        if self.estado == "agua" and nuevo_estado != "agua":
            if self.frame_index < len(self.animaciones["agua"]) - 1:
                return
        if nuevo_estado != self.estado:
            self.estado = nuevo_estado
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def movimiento(self, delta_x, delta_y):
        if delta_x < 0:
            self.flip = True
        elif delta_x > 0:
            self.flip = False

        self.forma.x += delta_x
        self.forma.y += delta_y

        if delta_x != 0 or delta_y != 0:
            self.cambiar_estado("caminando")
        else:
            self.cambiar_estado("reposo")

    def update(self):
        cooldown_animaciones = 200

        if pygame.time.get_ticks() - self.update_time >= cooldown_animaciones:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

            if self.frame_index >= len(self.animaciones[self.estado]):
                if self.estado == "agua":
                    self.frame_index = len(self.animaciones[self.estado]) - 1
                else:
                    self.frame_index = 0

            self.image = self.animaciones[self.estado][self.frame_index]

    def dibujar(self, interfaz):
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        interfaz.blit(imagen_flip, self.forma)

    def limitar_dentro_de_nivel(self, ancho_ventana):
        if self.forma.left < 0:
            self.forma.left = 0
        elif self.forma.right > ancho_ventana + 3:
            self.forma.right = ancho_ventana + 3

        if self.forma.top < 0:
            self.forma.top = 0