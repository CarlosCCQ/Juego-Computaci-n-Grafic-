import os
import pygame

def cargar_animaciones_personaje(directorio, escala):
    animaciones_personaje = []
    for archivo in os.listdir(directorio):
        if archivo.endswith(".png"):
            img = pygame.image.load(os.path.join(directorio, archivo))
            img = pygame.transform.scale(img, (
                int(img.get_width() * escala),
                int(img.get_height() * escala),
            ))
            animaciones_personaje.append(img)
    return animaciones_personaje

def cargar_animaciones_pato(escala, invertir_horizontalmente=False):
    ruta_base = os.path.dirname(__file__)
    ruta_absoluta = os.path.join(ruta_base + "/pato")
    animaciones_pato = []
    for archivo in sorted(os.listdir(ruta_absoluta)):
        if archivo.endswith(".png"):
            img = pygame.image.load(os.path.join(ruta_absoluta, archivo))
            img = pygame.transform.scale(img, (
                int(img.get_width() * escala),
                int(img.get_height() * escala),
            ))
            if invertir_horizontalmente:
                img = pygame.transform.flip(img, True, False)
            animaciones_pato.append(img)
    return animaciones_pato


def cargar_animaciones_loro( escala):
    ruta_base = os.path.dirname(__file__)
    ruta_absoluta = os.path.join(ruta_base + "/loro")
    animaciones_loro = []
    for archivo in os.listdir(ruta_absoluta):
        if archivo.endswith(".png"):
            img = pygame.image.load(os.path.join(ruta_absoluta, archivo))
            img = pygame.transform.scale(img, (
                int(img.get_width() * escala),
                int(img.get_height() * escala),
            ))
            animaciones_loro.append(img)
    return animaciones_loro


def cargar_animaciones_fuego(escala, invertir_horizontalmente=False):
    ruta_base = os.path.dirname(__file__)
    ruta_absoluta = os.path.join(ruta_base +"/fuego" )
    animaciones_fuego = []
    for archivo in sorted(os.listdir(ruta_absoluta)):
        if archivo.endswith(".png"):
            img = pygame.image.load(os.path.join(ruta_absoluta, archivo))
            img = pygame.transform.scale(img, (
                int(img.get_width() * escala),
                int(img.get_height() * escala),
            ))
            if invertir_horizontalmente:
                img = pygame.transform.flip(img, True, False)
            animaciones_fuego.append(img)
    return animaciones_fuego
