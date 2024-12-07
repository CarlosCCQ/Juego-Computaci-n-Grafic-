# /// script
# requires-python = ">=3.11"
# dependencies = [
#  "pygame"
# ]
# ///

import asyncio
#import pygbag.aio as asyncio
#from cargar_animaciones import *
import sys
import pygame
# from fondo import *
# from suelo import *
# from plantas import *
# from pato import *
# from personaje import *
# from fuego import *
# from loro import *
import random
import os
import csv

pygame.init()
pygame.font.init()
pygame.mixer.init()

# Dimensiones
ANCHO_VENTANA = 620
ALTO_VENTANA = 434
TILE_SIZE = 31
FILAS = 14
COLUMNAS = 20

# Colores
COLOR_PERSONAJE = (255, 255, 0)
COLOR_BG = (135, 206, 235)
COLOR_BLANCO = (255, 255, 255)

# Configuración de animaciones y enemigos
FPS = 30
VELOCIDAD_PERSONAJE = 2
VELOCIDAD_ENEMIGO = 2
SCALA_PERSONAJE = 0.33
SCALA_ENEMIGOS = 0.33
NUM_MAX_PATOS = 5
RETRASO_ANIMACION_PATO = 10

SCALA_PATO = 0.2
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Guardabosques")

ruta_base = os.path.dirname(__file__)

def cargar_animaciones_personaje(prefijo, cantidad, escala):
    animaciones_personaje = []
    for i in range(1, cantidad + 1):
        nombre_archivo = f"/{prefijo}{i}.png"
        archivo = os.path.join(ruta_base + nombre_archivo)
        if os.path.exists(archivo):
            img = pygame.image.load(archivo)
            img = pygame.transform.scale(img, (
                int(img.get_width() * escala),
                int(img.get_height() * escala),
            ))
            animaciones_personaje.append(img)
    return animaciones_personaje

class Personaje:
    def __init__(self, x, y, escala):
        self.energia = 100
        self.flip = False
        self.estado = "reposo"
        self.animaciones = {
            "agua": cargar_animaciones_personaje("agua_",4, escala),
            "saltando": cargar_animaciones_personaje("Guardabosquesaltando",6, escala),
            "caminando": cargar_animaciones_personaje("Guardabosquecaminando",4, escala),
            "reposo": cargar_animaciones_personaje("Guardabodqueparado",4, escala)
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

jugador = Personaje(40, 40,SCALA_PERSONAJE)

def decoraciones_planta():
    decoraciones_sprites = {
        0: pygame.image.load(ruta_base +"/arbol (0).png"),
        1: pygame.image.load(ruta_base +"/arbol (1).png"),
        2: pygame.image.load(ruta_base +"/arbol (2).png"),
        3: pygame.image.load(ruta_base +"/arbol (3).png"),
        6: pygame.image.load(ruta_base +"/arbol (6).png"),
    }

    for key in decoraciones_sprites:
        decoraciones_sprites[key] = pygame.transform.scale(decoraciones_sprites[key], (
        TILE_SIZE, TILE_SIZE))

    return decoraciones_sprites

def cargar_decoraciones_planta():
    ruta_csv = os.path.join(ruta_base + "/plantas.csv")
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
                    x = col_idx * TILE_SIZE
                    y = fila_idx * TILE_SIZE
                    ventana.blit(sprite, (x, y))

def cargar_sprites_nivel():
    tile_sprites_nivel = {}
    for tile_id in [0, 1, 2, 3, 18, 19, 20, 21]:
        ruta = ruta_base + f"/tiled ({tile_id}).png"
        tile_sprites_nivel[tile_id] = pygame.image.load(ruta)
        tile_sprites_nivel[tile_id] = pygame.transform.scale(tile_sprites_nivel[tile_id], (
        TILE_SIZE, TILE_SIZE))

    tile_sprites_nivel[-1] = None
    return tile_sprites_nivel

def cargar_nivel():
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
                    ventana.blit(sprite, (col_idx * TILE_SIZE, fila_idx * TILE_SIZE))

class Pato:
    def __init__(self, x, y, animaciones):
        self.x = x
        self.y = y
        self.animaciones = animaciones
        self.frame_actual = 0
        self.contador_retraso = 0

    def update(self):
        self.contador_retraso += 1
        if self.contador_retraso >= RETRASO_ANIMACION_PATO:
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
        plataformas_disponibles, min(NUM_MAX_PATOS, len(plataformas_disponibles))
    )

    patos = []
    for col_idx, fila_idx in plataformas_seleccionadas:
        x_pato = col_idx * TILE_SIZE
        invertir = random.choice([True, False])

        animaciones = cargar_animaciones_pato(SCALA_PATO, invertir)

        altura_sprite = animaciones[0].get_height()

        y_pato = (fila_idx * TILE_SIZE) - altura_sprite

        patos.append(Pato(x_pato, y_pato, animaciones))

    return patos

def cargar_fondo():
    ruta_csv_fondo = os.path.abspath(os.path.join(ruta_base + "/fondo.csv"))
    fondo = []
    with open(ruta_csv_fondo) as archivo_csv_fondo:
        lector = csv.reader(archivo_csv_fondo, delimiter=',')
        for fila in lector:
            fondo.append([int(celda) for celda in fila])
    return fondo


def dibujar_fondo(fondo, ventana):
    sprite_fondo = pygame.image.load(os.path.join(ruta_base + "/fondo.png"))
    for fila_idx, fila in enumerate(fondo):
        for col_idx, celda in enumerate(fila):
            if celda == 0:
                x = col_idx * TILE_SIZE
                y = fila_idx * TILE_SIZE
                ventana.blit(sprite_fondo, (x, y))

def cargar_animaciones_pato(escala, invertir_horizontalmente=False):
    animaciones_pato = []
    for i in range(1, 6):
        nombre_archivo = f"/PatoComiendo{i}.png"
        ruta_archivo = os.path.join(ruta_base + nombre_archivo)

        if os.path.isfile(ruta_archivo):
            img = pygame.image.load(ruta_archivo)
            img = pygame.transform.scale(img, (
                int(img.get_width() * escala),
                int(img.get_height() * escala),
            ))
            if invertir_horizontalmente:
                img = pygame.transform.flip(img, True, False)
            animaciones_pato.append(img)

    return animaciones_pato


def cargar_animaciones_loro( escala):
    animaciones_loro = []
    for i in range(1, 8):
        nombre_archivo = f"/LoroVolador{i}.png"
        ruta_archivo = os.path.join(ruta_base + nombre_archivo)

        if os.path.isfile(ruta_archivo):
            img = pygame.image.load(ruta_archivo)
            img = pygame.transform.scale(img, (
                int(img.get_width() * escala),
                int(img.get_height() * escala),
            ))
            animaciones_loro.append(img)

    return animaciones_loro


def cargar_animaciones_fuego(escala, invertir_horizontalmente=False):
    animaciones_fuego = []

    for i in range(0, 5):
        nombre_archivo = f"/fuego_{i}.png"
        ruta_archivo = os.path.join(ruta_base + nombre_archivo)

        if os.path.isfile(ruta_archivo):
            img = pygame.image.load(ruta_archivo)
            img = pygame.transform.scale(img, (
                int(img.get_width() * escala),
                int(img.get_height() * escala),
            ))
            if invertir_horizontalmente:
                img = pygame.transform.flip(img, True, False)
            animaciones_fuego.append(img)

    return animaciones_fuego

class Enemigo:
    def __init__(self, x, y,animaciones, escala, velocidad_x, plataforma=None):
        self.animaciones = animaciones
        self.x = x
        self.y = y
        self.escala = escala
        self.velocidad_x = velocidad_x
        self.velocidad_original = velocidad_x
        self.frame_actual = 0
        self.retraso_animacion = 10
        self.contador_retraso = 0
        self.direccion = 1
        self.plataforma = plataforma

    def update(self):
        self.contador_retraso += 1
        if self.contador_retraso >= self.retraso_animacion:
            self.contador_retraso = 0
            self.frame_actual = (self.frame_actual + 1) % len(self.animaciones)

        self.x += self.velocidad_x * self.direccion

        if self.plataforma:
            x_min, x_max = self.plataforma
            if self.x <= x_min or self.x + self.animaciones[0].get_width() >= x_max:
                self.direccion *= -1
                self.x = max(x_min, min(self.x, x_max - self.animaciones[0].get_width()))

    def dibujar(self, ventana):
        imagen_actual = self.animaciones[self.frame_actual]
        ventana.blit(imagen_actual, (self.x, self.y))

    def detener(self):
        self.velocidad_x = 0

    def reanudar(self):
        self.velocidad_x = self.velocidad_original


def inicializar_enemigo(nivel_suelo, num_enemigos, escala_enemigo, altura_sprite):
    plataformas_disponibles_enemigos = []
    enemigos = []
    for fila_idx, fila in enumerate(nivel_suelo):
        plataforma_actual = []
        for col_idx, celda in enumerate(fila):
            if celda in [0, 1, 2, 3, 18, 19, 20, 21]:
                if not plataforma_actual:
                    plataforma_actual = [col_idx * TILE_SIZE]
            elif plataforma_actual:
                plataforma_actual.append(col_idx * TILE_SIZE)
                plataformas_disponibles_enemigos.append(
                    (plataforma_actual[0], plataforma_actual[1], fila_idx * TILE_SIZE)
                )
                plataforma_actual = []

        if plataforma_actual:
            plataformas_disponibles_enemigos.append(
                (plataforma_actual[0], (len(fila) * TILE_SIZE), fila_idx * TILE_SIZE)
            )

    plataformas_seleccionadas_enemigos = random.sample(
        plataformas_disponibles_enemigos, min(num_enemigos, len(plataformas_disponibles_enemigos))
    )

    for x_min, x_max, y_plataforma in plataformas_seleccionadas_enemigos:
        x_enemigo = random.randint(x_min, x_max - TILE_SIZE)
        y_enemigo = y_plataforma - altura_sprite

        invertir = random.choice([True, False])
        animaciones = cargar_animaciones_fuego(escala_enemigo, invertir)

        enemigos.append(
            Enemigo(x_enemigo, y_enemigo, animaciones, escala_enemigo, velocidad_x=1, plataforma=(x_min, x_max))
        )

    return enemigos

decoraciones_sprites = decoraciones_planta()
decoraciones_mapa = cargar_decoraciones_planta()
tile_sprites_nivel = cargar_sprites_nivel()
suelo = cargar_nivel()
patos = inicializar_patos(suelo)
fondo = cargar_fondo()

escala_enemigo = SCALA_ENEMIGOS * 0.8
animaciones_enemigo_temp = cargar_animaciones_fuego(escala_enemigo)
sprite_altura_enemigo = animaciones_enemigo_temp[0].get_height()
num_max_enemigos = 5
TIEMPO_TOTAL = 180
limite_enemigos = 0
velocidad_salto = -7
gravedad = 0.5
reloj = pygame.time.Clock()

pygame.mixer.music.load(os.path.join(ruta_base + "/sonido_bosque.ogg"))
pygame.mixer.music.play(-1)
sonido_agua = pygame.mixer.Sound(os.path.join(ruta_base + "/sonido_agua.ogg"))
sonido_loro = pygame.mixer.Sound(os.path.join(ruta_base + "/sonido_loro.ogg"))

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

def mostrar_texto(ventana, texto, tamano, x, y, color=(255, 255, 255)):
    fuente = pygame.font.Font(None, tamano)
    superficie = fuente.render(texto, True, color)
    ventana.blit(superficie, (x, y))

async def menu_principal():
    pygame.event.clear()
    pygame.time.delay(200)

    menu = True
    while menu:
        ventana.fill((0, 0, 0))
        mostrar_texto(ventana, "Guardabosques vs fuego", 50, 100, 50)
        mostrar_texto(ventana, "1. Iniciar Juego", 36, 100, 150)
        mostrar_texto(ventana, "2. Instrucciones", 36, 100, 200)
        mostrar_texto(ventana, "3. Salir", 36, 100, 250)
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    menu = False
                elif evento.key == pygame.K_2:
                    await mostrar_instrucciones()
                elif evento.key == pygame.K_3:
                    pygame.quit()
                    exit()

async def mostrar_instrucciones():
    mostrando = True
    while mostrando:
        ventana.fill((0, 0, 0))
        mostrar_texto(ventana, "Instrucciones", 50, 100, 50)
        mostrar_texto(ventana, "Usa las teclas de 'a' y 'd' para moverte", 36, 100, 150)
        mostrar_texto(ventana, "Presiona la tecla'ESPACIO' para saltar", 36, 100, 200)
        mostrar_texto(ventana, "Presiona 'P' para lanzar agua", 36, 100, 250)
        mostrar_texto(ventana, "Evita que el bosque se incendie", 36, 100, 300)
        mostrar_texto(ventana, "Presiona cualquier tecla para volver", 36, 100, 350)
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                mostrando = False

#menu_principal()

async def bucle_juego():
    tiempo_transcurrido = 0
    puntaje = 0
    jugador = Personaje(40, 40, SCALA_PERSONAJE)  # Reiniciar el personaje
    enemigos = inicializar_enemigo(suelo, num_max_enemigos, escala_enemigo, sprite_altura_enemigo)
    loros = []
    mover_derecha = False
    mover_izquierda = False
    salto = False
    esta_en_suelo = True
    velocidad_y = 0
    echando_agua = False
    corriendo = True

    while corriendo:
        reloj.tick(FPS)
        tiempo_transcurrido += 1 / FPS
        dibujar_fondo(fondo, ventana)
        dibujar_nivel(suelo, tile_sprites_nivel, ventana)
        dibujar_decoraciones_planta(decoraciones_mapa, decoraciones_sprites, ventana)

        if tiempo_transcurrido >= TIEMPO_TOTAL:
            corriendo = False

        tiempo_restante = TIEMPO_TOTAL - int(tiempo_transcurrido)
        fuente_tiempo = pygame.font.Font(None, 24)
        texto_tiempo = fuente_tiempo.render(f"Tiempo: {tiempo_restante}s", True, (255, 255, 255))
        ventana.blit(texto_tiempo, (ANCHO_VENTANA - 150, 10))

        if tiempo_transcurrido >= TIEMPO_TOTAL:
            ventana.fill((0, 0, 0))
            mostrar_texto(ventana, "¡Game Over!", 36, 100, 200, (255, 0, 0))
            mostrar_texto(ventana, "Presiona cualquier tecla para volver al menú.", 20, 100, 250, (255, 255, 255))
            pygame.display.update()

            esperando = True
            while esperando:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if evento.type == pygame.KEYDOWN:
                        esperando = False

            pygame.time.delay(200)
            pygame.event.clear()
            await menu_principal()
            break

        if len(enemigos) == 0 or jugador.forma.top > ALTO_VENTANA:
            ventana.fill((0, 0, 0))

            jugador_gano = len(enemigos) == 0
            mensaje = "¡Felicidades! Bosque salvado." if jugador_gano else "¡Game Over!"
            color = (0, 255, 0) if jugador_gano else (255, 0, 0)

            mostrar_texto(ventana, mensaje, 36, 100, 200, color)
            mostrar_texto(ventana, "Presiona cualquier tecla para volver al menú.", 20, 100, 250, (255, 255, 255))
            pygame.display.update()

            esperando = True
            while esperando:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if evento.type == pygame.KEYDOWN:
                        esperando = False

            pygame.time.delay(200)
            pygame.event.clear()
            await menu_principal()
            break

        if random.randint(1, 300) == 1:
            x_inicial = -TILE_SIZE if random.choice([True, False]) else ANCHO_VENTANA
            y_inicial = random.randint(50, ALTO_VENTANA - 100)
            nuevo_loro = Loro(x_inicial, y_inicial, SCALA_ENEMIGOS)
            loros.append(nuevo_loro)

        delta_x = 0
        if mover_derecha:
            delta_x += VELOCIDAD_PERSONAJE
        if mover_izquierda:
            delta_x -= VELOCIDAD_PERSONAJE

        if salto and esta_en_suelo:
            velocidad_y = velocidad_salto
            esta_en_suelo = False

        jugador.forma.x += delta_x
        jugador.forma.y += velocidad_y

        jugador.limitar_dentro_de_nivel(ANCHO_VENTANA)

        velocidad_y += gravedad
        jugador.forma.y += velocidad_y

        jugador_colisionado = False
        for fila_idx, fila in enumerate(suelo):
            for col_idx, celda in enumerate(fila):
                if celda in [0, 1, 2, 3, 18, 19, 20, 21]:
                    tile_rect = pygame.Rect(
                        col_idx * TILE_SIZE,
                        fila_idx * TILE_SIZE,
                        TILE_SIZE,
                        TILE_SIZE
                    )
                    if jugador.forma.colliderect(tile_rect):
                        jugador_colisionado = True
                        if jugador.forma.bottom > tile_rect.top and jugador.forma.top < tile_rect.top and velocidad_y > 0:
                            jugador.forma.bottom = tile_rect.top
                            esta_en_suelo = True
                            velocidad_y = 0
                        elif jugador.forma.right > tile_rect.left and jugador.forma.left < tile_rect.left and delta_x > 0:
                            jugador.forma.right = tile_rect.left
                            delta_x = 0
                        elif jugador.forma.left < tile_rect.right and jugador.forma.right > tile_rect.right and delta_x < 0:
                            jugador.forma.left = tile_rect.right
                            delta_x = 0

        if not jugador_colisionado:
            esta_en_suelo = False

        if echando_agua:
            jugador.cambiar_estado("agua")
        else:
            if not esta_en_suelo:
                jugador.cambiar_estado("saltando")
            elif delta_x != 0:
                jugador.cambiar_estado("caminando")
            else:
                jugador.cambiar_estado("reposo")


        for pato in patos:
            pato.update()
            pato.dibujar(ventana)

        for enemigo in enemigos[:]:
            enemigo.update()
            enemigo.dibujar(ventana)

            enemigo_rect = pygame.Rect(enemigo.x, enemigo.y, enemigo.animaciones[0].get_width(),
                                       enemigo.animaciones[0].get_height())
            if jugador.forma.colliderect(enemigo_rect):
                if jugador.estado == "agua":
                    enemigos.remove(enemigo)
                    puntaje += 10
                    nuevos_enemigos = inicializar_enemigo(
                        suelo,
                        random.randint(0, 1),
                        escala_enemigo,
                        sprite_altura_enemigo
                    )
                    enemigos.extend(nuevos_enemigos)
                else:
                    enemigo.detener()
            else:
                enemigo.reanudar()

        for loro in loros[:]:
            loro.update()
            loro.dibujar(ventana)
            sonido_loro.set_volume(0.2)
            sonido_loro.play()
            if loro.fuera_de_pantalla(ANCHO_VENTANA, ALTO_VENTANA):
                loros.remove(loro)
                sonido_loro.stop()

        jugador.movimiento(delta_x, 0)
        jugador.update()
        jugador.dibujar(ventana)

        mostrar_texto(ventana, f"Puntaje: {puntaje}", 36, 10, 10)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_d:
                    mover_derecha = True
                elif evento.key == pygame.K_a:
                    mover_izquierda = True
                elif evento.key == pygame.K_SPACE:
                    salto = True
                elif evento.key == pygame.K_p:
                    echando_agua = True
                    sonido_agua.play()
            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_d:
                    mover_derecha = False
                elif evento.key == pygame.K_a:
                    mover_izquierda = False
                elif evento.key == pygame.K_SPACE:
                    salto = False
                elif evento.key == pygame.K_p:
                    echando_agua = False

        pygame.display.update()
        await asyncio.sleep(0)

async def main():
    await menu_principal()
    while True:
        await bucle_juego()

if __name__ == '__main__':
    asyncio.run(main())