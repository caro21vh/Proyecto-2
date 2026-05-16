import pygame

# Dimensiones
WIDTH  = 1200
HEIGHT = 700

# Colores
BG        = (235, 238, 245)
WHITE     = (255, 255, 255)
BLACK     = (30,  30,  40)
GRAY      = (120, 120, 130)
LIGHT     = (210, 215, 225)
BLUE      = (58,  110, 240)
BLUE_DARK = (40,  80,  190)
GREEN     = (48,  175, 110)
RED       = (220, 70,  70)
ORANGE    = (230, 140, 40)
PURPLE    = (140, 80,  220)
TEAL      = (40,  180, 175)
PANEL_BG  = (245, 247, 252)

PROCESS_COLORS = [
    (255, 100, 130),
    (100, 140, 255),
    (80,  210, 170),
    (255, 185, 60),
    (160, 100, 255),
    (255, 130, 60),
    (60,  200, 230),
    (200, 230, 60),
]

PRODUCT_COLORS = {
    i: (
        (i * 53 + 80)  % 180 + 60,
        (i * 89 + 120) % 180 + 60,
        (i * 127 + 50) % 180 + 60,
    )
    for i in range(1, 200)
}

# Fuentes  (inicializar con init_fonts())=
TITLE_FONT = None
HEAD_FONT  = None
TEXT_FONT  = None
SMALL_FONT = None
TINY_FONT  = None

def init_fonts():
    """Debe llamarse después de pygame.init()."""
    global TITLE_FONT, HEAD_FONT, TEXT_FONT, SMALL_FONT, TINY_FONT
    try:
        TITLE_FONT = pygame.font.SysFont("Montserrat", 32, bold=True)
        HEAD_FONT  = pygame.font.SysFont("Montserrat", 22, bold=True)
        TEXT_FONT  = pygame.font.SysFont("Montserrat", 19)
        SMALL_FONT = pygame.font.SysFont("Montserrat", 16)
        TINY_FONT  = pygame.font.SysFont("Montserrat", 13)
    except Exception:
        fb = pygame.font.SysFont(None, 20)
        TITLE_FONT = HEAD_FONT = TEXT_FONT = SMALL_FONT = TINY_FONT = fb

# Estado global del simulador
# Pantallas e Interfaz necesitan esto
estado = {
    # Navegación
    "scene": "menu",

    # Configuración
    "cantidad_productos": 1,
    "procesos_config":    [],   # list[dict]
    "nombre_inputs":      [],   # list[InputField]  (paralelo a procesos_config)
    "tarea_inputs":       [],   # list[list[InputField]]

    # Scroll de pantalla config
    "scroll_y":     0,
    "SCROLL_SPEED": 35,

    # Scroll de pantalla simulación
    "sim_scroll_y": 0,
    "sim_scroll_x": 0,

    # Simulación
    "simulador":          None,
    "simulation_running": False,
    "simulacion_pausada": False,
    "simulation_done":    False,
    "pasos_pendientes":   [],   

    # Mensajes de error en config
    "error_msg":   "",
    "error_timer": 0,
}

TIME_EVENT = pygame.USEREVENT + 1