# =========================================
# CONFIG SCENE DINAMICA
# =========================================

import pygame

pygame.init()

WIDTH = 1400
HEIGHT = 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# =========================================
# COLORES
# =========================================

BG = (242, 244, 248)
WHITE = (255, 255, 255)
BLACK = (35, 35, 35)
GRAY = (120, 120, 120)
LIGHT = (225, 225, 225)

BLUE = (70, 120, 255)
GREEN = (60, 180, 120)
RED = (220, 80, 80)

# =========================================
# FUENTES
# =========================================

TITLE_FONT = pygame.font.SysFont("Montserrat", 32, bold=True)
TEXT_FONT = pygame.font.SysFont("Montserrat", 22)
SMALL_FONT = pygame.font.SysFont("Montserrat", 18)

# =========================================
# DATOS MOCK DINAMICOS
# =========================================

cantidad_productos = 12

procesos = [
    {
        "nombre": "Proceso 1",
        "tareas": [
            {"nombre": "Tarea 1", "tiempo": 2},
            {"nombre": "Tarea 2", "tiempo": 1},
        ]
    },

    {
        "nombre": "Proceso 2",
        "tareas": [
            {"nombre": "Tarea 1", "tiempo": 3},
        ]
    }
]

# =========================================
# SCROLL
# =========================================

scroll_y = 0
SCROLL_SPEED = 30

# =========================================
# BOTON
# =========================================

class Button:

    def __init__(self, x, y, width, height, text, color=BLUE):

        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color

    def draw(self, surface):

        mouse_pos = pygame.mouse.get_pos()

        current_color = self.color

        if self.rect.collidepoint(mouse_pos):
            current_color = (
                min(self.color[0] + 20, 255),
                min(self.color[1] + 20, 255),
                min(self.color[2] + 20, 255)
            )

        pygame.draw.rect(
            surface,
            current_color,
            self.rect,
            border_radius=12
        )

        text_surface = SMALL_FONT.render(
            self.text,
            True,
            WHITE
        )

        text_rect = text_surface.get_rect(
            center=self.rect.center
        )

        surface.blit(text_surface, text_rect)

    def clicked(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# =========================================
# FUNCIONES
# =========================================

def agregar_proceso():

    nuevo = {
        "nombre": f"Proceso {len(procesos) + 1}",
        "tareas": []
    }

    procesos.append(nuevo)

def agregar_tarea(proceso):

    nueva_tarea = {
        "nombre": f"Tarea {len(proceso['tareas']) + 1}",
        "tiempo": 1
    }

    proceso["tareas"].append(nueva_tarea)

# =========================================
# BOTONES GLOBALES
# =========================================

add_process_button = Button(
    1050,
    90,
    250,
    45,
    "+ Agregar proceso",
    GREEN
)

start_button = Button(
    1050,
    730,
    250,
    45,
    "Iniciar simulacion"
)

# =========================================
# LOOP
# =========================================

running = True

while running:

    screen.fill(BG)

    # =====================================
    # HEADER
    # =====================================

    pygame.draw.rect(
        screen,
        WHITE,
        (0, 0, WIDTH, 70)
    )

    pygame.draw.line(
        screen,
        LIGHT,
        (0, 70),
        (WIDTH, 70),
        2
    )

    title = TITLE_FONT.render(
        "Configuracion de linea de produccion",
        True,
        BLACK
    )

    screen.blit(title, (40, 18))

    # =====================================
    # PANEL PRODUCTOS
    # =====================================

    products_panel = pygame.Rect(
        40,
        100,
        300,
        100
    )

    pygame.draw.rect(
        screen,
        WHITE,
        products_panel,
        border_radius=18
    )

    pygame.draw.rect(
        screen,
        LIGHT,
        products_panel,
        width=2,
        border_radius=18
    )

    text = TEXT_FONT.render(
        "Cantidad de productos",
        True,
        BLACK
    )

    value = TITLE_FONT.render(
        str(cantidad_productos),
        True,
        BLUE
    )

    screen.blit(text, (60, 120))
    screen.blit(value, (160, 150))

    # =====================================
    # BOTONES PRODUCTOS
    # =====================================

    minus_button = Button(
        60,
        150,
        40,
        40,
        "-"
    )

    plus_button = Button(
        260,
        150,
        40,
        40,
        "+"
    )

    minus_button.draw(screen)
    plus_button.draw(screen)

    # =====================================
    # BOTONES GENERALES
    # =====================================

    add_process_button.draw(screen)
    start_button.draw(screen)

    # =====================================
    # SCROLL AREA
    # =====================================

    y_offset = 240 + scroll_y

    # =====================================
    # RENDER DINAMICO PROCESOS
    # =====================================
    
    # Guardar referencias a los botones de tiempo para procesarlos después
    time_buttons = []
    add_task_buttons = []

    for proceso_index, proceso in enumerate(procesos):

        process_card = pygame.Rect(
            40,
            y_offset,
            1260,
            170
        )

        pygame.draw.rect(
            screen,
            WHITE,
            process_card,
            border_radius=18
        )

        pygame.draw.rect(
            screen,
            LIGHT,
            process_card,
            width=2,
            border_radius=18
        )

        # =================================
        # TITULO PROCESO
        # =================================

        process_title = TEXT_FONT.render(
            proceso["nombre"],
            True,
            BLACK
        )

        screen.blit(
            process_title,
            (60, y_offset + 20)
        )

        # =================================
        # BOTON AGREGAR TAREA
        # =================================

        add_task_button = Button(
            1020,
            y_offset + 15,
            220,
            40,
            "+ Agregar tarea",
            GREEN
        )

        add_task_button.draw(screen)
        add_task_buttons.append((add_task_button, proceso))

        # =================================
        # RENDER TAREAS
        # =================================

        for tarea_index, tarea in enumerate(proceso["tareas"]):

            task_x = 60 + (tarea_index * 240)
            task_y = y_offset + 80

            task_rect = pygame.Rect(
                task_x,
                task_y,
                210,
                65
            )

            pygame.draw.rect(
                screen,
                BG,
                task_rect,
                border_radius=12
            )

            pygame.draw.rect(
                screen,
                LIGHT,
                task_rect,
                width=2,
                border_radius=12
            )

            # =============================
            # INFO TAREA
            # =============================

            task_name = SMALL_FONT.render(
                tarea["nombre"],
                True,
                BLACK
            )

            task_time = SMALL_FONT.render(
                f"Tiempo: {tarea['tiempo']}",
                True,
                GRAY
            )

            screen.blit(
                task_name,
                (task_x + 15, task_y + 10)
            )

            screen.blit(
                task_time,
                (task_x + 15, task_y + 35)
            )

            # =============================
            # BOTONES TIEMPO
            # =============================

            time_minus = Button(
                task_x + 140,
                task_y + 10,
                25,
                25,
                "-"
            )

            time_plus = Button(
                task_x + 170,
                task_y + 10,
                25,
                25,
                "+"
            )

            time_minus.draw(screen)
            time_plus.draw(screen)
            
            # Guardar los botones con su tarea para procesar eventos después
            time_buttons.append((time_minus, time_plus, tarea))

        y_offset += 200

    # =====================================
    # EVENTOS (SOLO UN BUCLE)
    # =====================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # =================================
        # SCROLL
        # =================================

        if event.type == pygame.MOUSEWHEEL:
            scroll_y += event.y * SCROLL_SPEED

        # =================================
        # PRODUCTOS
        # =================================

        if minus_button.clicked(event):
            if cantidad_productos > 1:
                cantidad_productos -= 1

        if plus_button.clicked(event):
            cantidad_productos += 1

        # =================================
        # AGREGAR PROCESO
        # =================================

        if add_process_button.clicked(event):
            agregar_proceso()

        # =================================
        # AGREGAR TAREA
        # =================================
        
        for btn, proceso in add_task_buttons:
            if btn.clicked(event):
                agregar_tarea(proceso)

        # =================================
        # AJUSTAR TIEMPO DE TAREAS
        # =================================
        
        for time_minus, time_plus, tarea in time_buttons:
            if time_minus.clicked(event):
                if tarea["tiempo"] > 1:
                    tarea["tiempo"] -= 1
                    
            if time_plus.clicked(event):
                tarea["tiempo"] += 1

    pygame.display.update()
    clock.tick(60)

pygame.quit()