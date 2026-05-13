import pygame
import sys

pygame.init()

# =========================================
# CONFIGURACION GENERAL
# =========================================
WIDTH = 1100
HEIGHT = 650

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LinProd")

clock = pygame.time.Clock()

# =========================================
# TIEMPO SIMULACION
# =========================================
simulation_time = 0

# =========================================
# COLORES
# =========================================
BG_COLOR = (242, 244, 248)

WHITE = (255, 255, 255)
BLACK = (30, 30, 30)

GRAY = (150, 150, 150)
LIGHT_GRAY = (230, 230, 230)

BLUE = (70, 120, 255)
GREEN = (0, 180, 120)
RED = (200, 70, 70)
ORANGE = (230, 140, 40)

# =========================================
# COLORES PRODUCTOS
# =========================================
PRODUCT_COLORS = {
    "P1": (70, 120, 255),
    "P2": (255, 80, 80),
    "P3": (80, 200, 120),
    "P4": (255, 170, 60),
    "P5": (180, 80, 255),
    "P6": (255, 120, 180),
    "P7": (80, 220, 220),
    "P8": (255, 220, 80),
    "P9": (120, 255, 120),
    "P10": (120, 120, 255),
    "P11": (255, 150, 80),
    "P12": (180, 180, 180)
}

# =========================================
# FUENTES
# =========================================
TITLE_FONT = pygame.font.SysFont("Montserrat", 34, bold=True)
TEXT_FONT = pygame.font.SysFont("Montserrat", 20)
SMALL_FONT = pygame.font.SysFont("Montserrat", 16)

def draw_header(surface, text, y=0, height=150):
    # barra más compacta
    pygame.draw.rect(
        surface,
        WHITE,
        (0, y, WIDTH, height)
    )

    pygame.draw.line(
        surface,
        LIGHT_GRAY,
        (0, y + height),
        (WIDTH, y + height),
        2
    )

    # texto centrado más “pegado” a la barra
    title = TITLE_FONT.render(text, True, BLACK)
    title_rect = title.get_rect(center=(WIDTH // 2, y + height // 2 + 1))

    surface.blit(title, title_rect)

# =========================================
# BOTON
# =========================================
class Button:

    def __init__(self, x, y, width, height, text):

        self.rect = pygame.Rect(x, y, width, height)

        self.text = text

    def draw(self, surface):

        pygame.draw.rect(
            surface,
            BLUE,
            self.rect,
            border_radius=12
        )

        text_surface = TEXT_FONT.render(
            self.text,
            True,
            WHITE
        )

        text_rect = text_surface.get_rect(
            center=self.rect.center
        )

        surface.blit(text_surface, text_rect)

    def is_clicked(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.rect.collidepoint(event.pos):
                return True

        return False

# =========================================
# CELDA SIMULACION
# =========================================
class SimulationCell:

    def __init__(self, x, y, tarea, tiempo, cola, procesando):

        self.x = x
        self.y = y

        self.tarea = tarea
        self.tiempo = tiempo

        self.cola = cola
        self.procesando = procesando

        self.width = 230
        self.height = 150

    def draw(self, surface):

        rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

        # SOMBRA
        shadow = pygame.Rect(
            self.x + 4,
            self.y + 4,
            self.width,
            self.height
        )

        pygame.draw.rect(
            surface,
            (210, 210, 210),
            shadow,
            border_radius=14
        )

        # PANEL
        pygame.draw.rect(
            surface,
            WHITE,
            rect,
            border_radius=14
        )

        pygame.draw.rect(
            surface,
            LIGHT_GRAY,
            rect,
            width=2,
            border_radius=14
        )

        # =========================
        # TITULO
        # =========================
        title = TEXT_FONT.render(
            self.tarea,
            True,
            BLACK
        )

        surface.blit(
            title,
            (self.x + 15, self.y + 12)
        )

        # =========================
        # TIEMPO
        # =========================
        tp_text = SMALL_FONT.render(
            f"Tiempo: {self.tiempo}",
            True,
            GRAY
        )

        surface.blit(
            tp_text,
            (self.x + 15, self.y + 38)
        )

        # =========================
        # COLA
        # =========================
        cola_title = SMALL_FONT.render(
            "Cola",
            True,
            BLACK
        )

        surface.blit(
            cola_title,
            (self.x + 20, self.y + 70)
        )

        for i, producto in enumerate(self.cola):

            color = PRODUCT_COLORS.get(
                producto,
                BLUE
            )

            pygame.draw.circle(
                surface,
                color,
                (
                    self.x + 35 + (i * 28),
                    self.y + 105
                ),
                10
            )

        # =========================
        # PROCESANDO
        # =========================
        process_title = SMALL_FONT.render(
            "Procesando",
            True,
            BLACK
        )

        surface.blit(
            process_title,
            (self.x + 120, self.y + 70)
        )

        process_rect = pygame.Rect(
            self.x + 120,
            self.y + 90,
            70,
            35
        )

        pygame.draw.rect(
            surface,
            LIGHT_GRAY,
            process_rect,
            border_radius=10
        )

        pygame.draw.rect(
            surface,
            GRAY,
            process_rect,
            width=2,
            border_radius=10
        )

        if self.procesando:

            process_color = PRODUCT_COLORS.get(
                self.procesando,
                BLUE
            )
            
            pygame.draw.circle(
                surface,
                process_color,
                process_rect.center,
                12
            )

# =========================================
# ESCENAS
# =========================================
scene = "menu"

# =========================================
# BOTONES
# =========================================
start_button = Button(
    450,
    420,
    200,
    55,
    "Empezar"
)

simulation_button = Button(
    400,
    500,
    300,
    55,
    "Iniciar Simulacion"
)

report_button = Button(
    860,
    570,
    180,
    45,
    "Reporte"
)

back_button = Button(
    40,
    570,
    160,
    45,
    "Volver"
)

# =========================================
# DATOS MOCK
# =========================================
cells = [

    # FILA 1
    SimulationCell(
        180,
        160,
        "Tarea 1",
        2,
        ["P1", "P2", "P3"],
        "P4"
    ),

    SimulationCell(
        430,
        160,
        "Tarea 2",
        1,
        ["P5"],
        "P6"
    ),

    SimulationCell(
        680,
        160,
        "Tarea 3",
        3,
        [],
        "P7"
    ),

    # FILA 2
    SimulationCell(
        180,
        380,
        "Tarea 1",
        2,
        ["P8"],
        "P9"
    ),

    SimulationCell(
        430,
        380,
        "Tarea 2",
        1,
        ["P10", "P11"],
        None
    ),

    SimulationCell(
        680,
        380,
        "Tarea 3",
        4,
        [],
        "P12"
    )
]

# =========================================
# EVENTO TIEMPO
# =========================================
TIME_EVENT = pygame.USEREVENT + 1

pygame.time.set_timer(
    TIME_EVENT,
    1000
)

# =========================================
# LOOP PRINCIPAL
# =========================================
running = True

while running:

    # =====================================
    # EVENTOS
    # =====================================
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # CONTADOR CICLOS
        if event.type == TIME_EVENT:

            if scene == "simulation":
                simulation_time += 1

        # MENU
        if scene == "menu":

            if start_button.is_clicked(event):
                scene = "config"

        # CONFIG
        elif scene == "config":

            if simulation_button.is_clicked(event):
                scene = "simulation"

        # SIMULATION
        elif scene == "simulation":

            if report_button.is_clicked(event):
                scene = "report"

        # REPORT
        elif scene == "report":

            if back_button.is_clicked(event):
                scene = "menu"

    # =====================================
    # FONDO
    # =====================================
    screen.fill(BG_COLOR)

    # =====================================
    # MENU
    # =====================================
    if scene == "menu":

        title = TITLE_FONT.render(
            "Proyecto 2: LinProd",
            True,
            BLACK
        )

        subtitle = TEXT_FONT.render(
            "Simulador de Produccion",
            True,
            GRAY
        )

        title_rect = title.get_rect(center=(WIDTH // 2, 200))
        subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, 250))

        screen.blit(title, title_rect)
        screen.blit(subtitle, subtitle_rect)

        start_button.draw(screen)

    # =====================================
    # CONFIG
    # =====================================
    elif scene == "config":
        #title = TITLE_FONT.render("Configuracion", True, BLACK)
        #title_rect = title.get_rect(center=(WIDTH // 2, 90))
        #screen.blit(title, title_rect)
        draw_header(screen, "Configuracion")

        info1 = TEXT_FONT.render(
            "Cantidad de productos: 12",
            True,
            BLACK
        )

        info2 = TEXT_FONT.render(
            "Procesos: 2",
            True,
            BLACK
        )

        info3 = TEXT_FONT.render(
            "Tareas por proceso: 3",
            True,
            BLACK
        )

        screen.blit(info1, (350, 220))
        screen.blit(info2, (350, 270))
        screen.blit(info3, (350, 320))

        simulation_button.draw(screen)

    # =====================================
    # SIMULACION
    # =====================================
    elif scene == "simulation":

        pygame.draw.rect(
            screen,
            WHITE,
            (0, 0, WIDTH, 70)
        )

        pygame.draw.line(
            screen,
            LIGHT_GRAY,
            (0, 70),
            (WIDTH, 70),
            2
        )
        title = TITLE_FONT.render(
            "Simulacion de Produccion",
            True,
            BLACK
        )

        title_rect = title.get_rect(midleft=(30, 35))

        screen.blit(title, title_rect)

        # CONTADOR CICLOS
        cycle_text = TEXT_FONT.render(
            f"Ciclo {simulation_time}",
            True,
            BLUE
        )

        cycle_rect = cycle_text.get_rect(midright=(WIDTH - 40, 35))
        screen.blit(cycle_text, cycle_rect)

        # CABECERAS COLUMNAS
        headers = [
            "Tarea 1",
            "Tarea 2",
            "Tarea 3"
        ]

        for i, header in enumerate(headers):

            text = TEXT_FONT.render(
                header,
                True,
                BLACK
            )

            screen.blit(
                text,
                (235 + (i * 250), 115)
            )

        # FILAS
        process1 = TEXT_FONT.render(
            "Proceso 1",
            True,
            BLACK
        )

        process2 = TEXT_FONT.render(
            "Proceso 2",
            True,
            BLACK
        )

        screen.blit(process1, (40, 210))
        screen.blit(process2, (40, 400))

        # CELDAS
        for cell in cells:
            cell.draw(screen)

        report_button.draw(screen)

    # =====================================
    # REPORTE
    # =====================================
    elif scene == "report":

        title = TITLE_FONT.render("Reporte Final", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH // 2, 90))
        screen.blit(title, title_rect)

        #draw_header(screen, "Reporte Final")

        stat1 = TEXT_FONT.render(
            "Productos procesados: 12",
            True,
            BLACK
        )

        stat2 = TEXT_FONT.render(
            f"Tiempo total: {simulation_time} ciclos",
            True,
            BLACK
        )

        stat3 = TEXT_FONT.render(
            "Cuello de botella: Tarea 3",
            True,
            BLACK
        )

        screen.blit(stat1, (320, 220))
        screen.blit(stat2, (320, 280))
        screen.blit(stat3, (320, 340))

        back_button.draw(screen)

    # =====================================
    # ACTUALIZAR
    # =====================================
    pygame.display.update()

    clock.tick(60)

pygame.quit()
sys.exit()