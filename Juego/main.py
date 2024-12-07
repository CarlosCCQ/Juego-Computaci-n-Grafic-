# /// script
# requires-python = ">=3.11"
# dependencies = [
#  "pygame"
# ]
# ///

import asyncio
#import pygbag.aio as asyncio
import sys
from scripts.fondo import *
from scripts.suelo import *
from scripts.plantas import *
from scripts.pato import *
from scripts.personaje import *
from scripts.fuego import *
from scripts.loro import *
import os

pygame.init()
pygame.font.init()
pygame.mixer.init()

ventana = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
pygame.display.set_caption("Guardabosques")

ruta_base = os.path.dirname(__file__)

jugador = Personaje(40, 40, constantes.SCALA_PERSONAJE)
decoraciones_sprites = decoraciones_planta()
decoraciones_mapa = cargar_decoraciones_planta()
tile_sprites_nivel = cargar_sprites_nivel()
suelo = cargar_nivel()
patos = inicializar_patos(suelo)
fondo = cargar_fondo()

escala_enemigo = constantes.SCALA_ENEMIGOS * 0.8
animaciones_enemigo_temp = cargar_animaciones_fuego(escala_enemigo)
sprite_altura_enemigo = animaciones_enemigo_temp[0].get_height()
num_max_enemigos = 5
TIEMPO_TOTAL = 180
limite_enemigos = 0
velocidad_salto = -7
gravedad = 0.5
reloj = pygame.time.Clock()

pygame.mixer.music.load(os.path.join(ruta_base + "/sonidos/sonido_bosque.ogg"))
pygame.mixer.music.play(-1)
sonido_agua = pygame.mixer.Sound(os.path.join(ruta_base + "/sonidos/sonido_agua.ogg"))
sonido_loro = pygame.mixer.Sound(os.path.join(ruta_base + "/sonidos/sonido_loro.ogg"))

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
    jugador = Personaje(40, 40, constantes.SCALA_PERSONAJE)  # Reiniciar el personaje
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
        reloj.tick(constantes.FPS)
        tiempo_transcurrido += 1/constantes.FPS
        dibujar_fondo(fondo, ventana)
        dibujar_nivel(suelo, tile_sprites_nivel, ventana)
        dibujar_decoraciones_planta(decoraciones_mapa, decoraciones_sprites, ventana)

        if tiempo_transcurrido >= TIEMPO_TOTAL:
            corriendo = False

        tiempo_restante = TIEMPO_TOTAL - int(tiempo_transcurrido)
        fuente_tiempo = pygame.font.Font(None, 24)
        texto_tiempo = fuente_tiempo.render(f"Tiempo: {tiempo_restante}s", True, (255, 255, 255))
        ventana.blit(texto_tiempo, (constantes.ANCHO_VENTANA - 150, 10))

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

        if len(enemigos) == 0 or jugador.forma.top > constantes.ALTO_VENTANA:
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
            x_inicial = -constantes.TILE_SIZE if random.choice([True, False]) else constantes.ANCHO_VENTANA
            y_inicial = random.randint(50, constantes.ALTO_VENTANA - 100)
            nuevo_loro = Loro(x_inicial, y_inicial, constantes.SCALA_ENEMIGOS)
            loros.append(nuevo_loro)

        delta_x = 0
        if mover_derecha:
            delta_x += constantes.VELOCIDAD_PERSONAJE
        if mover_izquierda:
            delta_x -= constantes.VELOCIDAD_PERSONAJE

        if salto and esta_en_suelo:
            velocidad_y = velocidad_salto
            esta_en_suelo = False

        jugador.forma.x += delta_x
        jugador.forma.y += velocidad_y

        jugador.limitar_dentro_de_nivel(constantes.ANCHO_VENTANA)

        velocidad_y += gravedad
        jugador.forma.y += velocidad_y

        jugador_colisionado = False
        for fila_idx, fila in enumerate(suelo):
            for col_idx, celda in enumerate(fila):
                if celda in [0, 1, 2, 3, 18, 19, 20, 21]:
                    tile_rect = pygame.Rect(
                        col_idx * constantes.TILE_SIZE,
                        fila_idx * constantes.TILE_SIZE,
                        constantes.TILE_SIZE,
                        constantes.TILE_SIZE
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
            if loro.fuera_de_pantalla(constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA):
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