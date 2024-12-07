# from cargar_animaciones import *
# import random
# import constantes
#
#
# class Enemigo:
#     def __init__(self, x, y,animaciones, escala, velocidad_x, plataforma=None):
#         self.animaciones = animaciones
#         self.x = x
#         self.y = y
#         self.escala = escala
#         self.velocidad_x = velocidad_x
#         self.velocidad_original = velocidad_x
#         self.frame_actual = 0
#         self.retraso_animacion = 10
#         self.contador_retraso = 0
#         self.direccion = 1
#         self.plataforma = plataforma
#
#     def update(self):
#         self.contador_retraso += 1
#         if self.contador_retraso >= self.retraso_animacion:
#             self.contador_retraso = 0
#             self.frame_actual = (self.frame_actual + 1) % len(self.animaciones)
#
#         self.x += self.velocidad_x * self.direccion
#
#         if self.plataforma:
#             x_min, x_max = self.plataforma
#             if self.x <= x_min or self.x + self.animaciones[0].get_width() >= x_max:
#                 self.direccion *= -1
#                 self.x = max(x_min, min(self.x, x_max - self.animaciones[0].get_width()))
#
#     def dibujar(self, ventana):
#         imagen_actual = self.animaciones[self.frame_actual]
#         ventana.blit(imagen_actual, (self.x, self.y))
#
#     def detener(self):
#         self.velocidad_x = 0
#
#     def reanudar(self):
#         self.velocidad_x = self.velocidad_original
#
#
# def inicializar_enemigo(nivel_suelo, num_enemigos, escala_enemigo, altura_sprite):
#     plataformas_disponibles_enemigos = []
#     enemigos = []
#     for fila_idx, fila in enumerate(nivel_suelo):
#         plataforma_actual = []
#         for col_idx, celda in enumerate(fila):
#             if celda in [0, 1, 2, 3, 18, 19, 20, 21]:
#                 if not plataforma_actual:
#                     plataforma_actual = [col_idx * constantes.TILE_SIZE]
#             elif plataforma_actual:
#                 plataforma_actual.append(col_idx * constantes.TILE_SIZE)
#                 plataformas_disponibles_enemigos.append(
#                     (plataforma_actual[0], plataforma_actual[1], fila_idx * constantes.TILE_SIZE)
#                 )
#                 plataforma_actual = []
#
#         if plataforma_actual:
#             plataformas_disponibles_enemigos.append(
#                 (plataforma_actual[0], (len(fila) * constantes.TILE_SIZE), fila_idx * constantes.TILE_SIZE)
#             )
#
#     plataformas_seleccionadas_enemigos = random.sample(
#         plataformas_disponibles_enemigos, min(num_enemigos, len(plataformas_disponibles_enemigos))
#     )
#
#     for x_min, x_max, y_plataforma in plataformas_seleccionadas_enemigos:
#         x_enemigo = random.randint(x_min, x_max - constantes.TILE_SIZE)
#         y_enemigo = y_plataforma - altura_sprite
#
#         invertir = random.choice([True, False])
#         animaciones = cargar_animaciones_fuego(escala_enemigo, invertir)
#
#         enemigos.append(
#             Enemigo(x_enemigo, y_enemigo, animaciones, escala_enemigo, velocidad_x=1, plataforma=(x_min, x_max))
#         )
#
#     return enemigos