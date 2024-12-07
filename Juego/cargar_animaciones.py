#

# def cargar_animaciones_personaje(prefijo, cantidad, escala):
#     ruta_base = os.path.dirname(__file__)
#     animaciones_personaje = []
#     for i in range(1, cantidad + 1):
#         nombre_archivo = f"/{prefijo}{i}.png"
#         archivo = os.path.join(ruta_base + nombre_archivo)
#         if os.path.exists(archivo):
#             img = pygame.image.load(archivo)
#             img = pygame.transform.scale(img, (
#                 int(img.get_width() * escala),
#                 int(img.get_height() * escala),
#             ))
#             animaciones_personaje.append(img)
#     return animaciones_personaje
#
# def cargar_animaciones_pato(escala, invertir_horizontalmente=False):
#     ruta_base = os.path.dirname(__file__)
#     animaciones_pato = []
#     for i in range(1, 6):
#         nombre_archivo = f"/PatoComiendo{i}.png"
#         ruta_archivo = os.path.join(ruta_base + nombre_archivo)
#
#         if os.path.isfile(ruta_archivo):
#             img = pygame.image.load(ruta_archivo)
#             img = pygame.transform.scale(img, (
#                 int(img.get_width() * escala),
#                 int(img.get_height() * escala),
#             ))
#             if invertir_horizontalmente:
#                 img = pygame.transform.flip(img, True, False)
#             animaciones_pato.append(img)
#
#     return animaciones_pato
#
#
# def cargar_animaciones_loro( escala):
#     ruta_base = os.path.dirname(__file__)
#     animaciones_loro = []
#     for i in range(1, 8):
#         nombre_archivo = f"/LoroVolador{i}.png"
#         ruta_archivo = os.path.join(ruta_base + nombre_archivo)
#
#         if os.path.isfile(ruta_archivo):
#             img = pygame.image.load(ruta_archivo)
#             img = pygame.transform.scale(img, (
#                 int(img.get_width() * escala),
#                 int(img.get_height() * escala),
#             ))
#             animaciones_loro.append(img)
#
#     return animaciones_loro
#
#
# def cargar_animaciones_fuego(escala, invertir_horizontalmente=False):
#     ruta_base = os.path.dirname(__file__)
#     animaciones_fuego = []
#
#     for i in range(0, 5):
#         nombre_archivo = f"/fuego_{i}.png"
#         ruta_archivo = os.path.join(ruta_base + nombre_archivo)
#
#         if os.path.isfile(ruta_archivo):
#             img = pygame.image.load(ruta_archivo)
#             img = pygame.transform.scale(img, (
#                 int(img.get_width() * escala),
#                 int(img.get_height() * escala),
#             ))
#             if invertir_horizontalmente:
#                 img = pygame.transform.flip(img, True, False)
#             animaciones_fuego.append(img)
#
#     return animaciones_fuego
