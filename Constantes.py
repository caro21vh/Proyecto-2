import pygame

#Dimensiones ventana
WIDTH = 1400
HEIGHT = 800

#Colores
BG = (242, 244, 248)
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
GRAY = (150, 150, 150)
LIGHT_GRAY = (230, 230, 230)
BLUE = (70, 120, 255)
GREEN = (0, 180, 120)
RED = (200, 70, 70)
ORANGE = (230, 140, 40)

#Fuentes (se inicializan después de pygame.init)
def init_fonts():
    global TITLE_FONT, TEXT_FONT, SMALL_FONT
    TITLE_FONT = pygame.font.SysFont("Montserrat", 34, bold=True)
    TEXT_FONT = pygame.font.SysFont("Montserrat", 20)
    SMALL_FONT = pygame.font.SysFont("Montserrat", 16)