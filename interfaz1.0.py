import pygame
import sys
from Simulador import Simulador
from Producto import Producto
from Proceso import Proceso
from Tarea import Tarea

pygame.init()

# CONFIGURACION GENERAL

WIDTH = 1400
HEIGHT = 820

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LinProd - Simulador de Producción")
clock = pygame.time.Clock()

# COLORES

BG         = (235, 238, 245)
WHITE      = (255, 255, 255)
BLACK      = (30,  30,  40)
GRAY       = (120, 120, 130)
LIGHT      = (210, 215, 225)
BLUE       = (58,  110, 240)
BLUE_DARK  = (40,  80,  190)
GREEN      = (48,  175, 110)
RED        = (220, 70,  70)
ORANGE     = (230, 140, 40)
PURPLE     = (140, 80,  220)
TEAL       = (40,  180, 175)
PANEL_BG   = (245, 247, 252)

PROCESS_COLORS = [
    (255, 100, 130),   # pink/red  - inicial
    (100, 140, 255),   # blue
    (80,  210, 170),   # teal
    (255, 185, 60),    # yellow
    (160, 100, 255),   # purple
    (255, 130, 60),    # orange
    (60,  200, 230),   # cyan
    (200, 230, 60),    # lime
]

PRODUCT_COLORS = {}
for i in range(1, 200):
    PRODUCT_COLORS[i] = (
        (i * 53 + 80)  % 180 + 60,
        (i * 89 + 120) % 180 + 60,
        (i * 127 + 50) % 180 + 60,
    )

# FUENTES

try:
    TITLE_FONT  = pygame.font.SysFont("Montserrat", 32, bold=True)
    HEAD_FONT   = pygame.font.SysFont("Montserrat", 22, bold=True)
    TEXT_FONT   = pygame.font.SysFont("Montserrat", 19)
    SMALL_FONT  = pygame.font.SysFont("Montserrat", 16)
    TINY_FONT   = pygame.font.SysFont("Montserrat", 13)
except:
    TITLE_FONT = HEAD_FONT = TEXT_FONT = SMALL_FONT = TINY_FONT = pygame.font.SysFont(None, 20)


# Efectos elementos visuales

def draw_shadow(surface, rect, radius=12, blur=20):
    """Dibuja una sombra suave debajo de un rect."""
    shadow_surf = pygame.Surface((rect.width + blur * 2, rect.height + blur * 2), pygame.SRCALPHA)
    for i in range(blur, 0, -1):
        alpha = int(60 * (1 - i / blur) ** 2)
        col = (0, 0, 0, alpha)
        r = pygame.Rect(blur - i, blur - i, rect.width + i * 2, rect.height + i * 2)
        pygame.draw.rect(shadow_surf, col, r, border_radius=radius + i)
    surface.blit(shadow_surf, (rect.x - blur, rect.y - blur))

def draw_rounded_rect(surface, color, rect, radius=12, border=0, border_color=None):
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    if border and border_color:
        pygame.draw.rect(surface, border_color, rect, width=border, border_radius=radius)

def render_text_centered(surface, font, text, color, rect):
    surf = font.render(text, True, color)
    r = surf.get_rect(center=rect.center)
    surface.blit(surf, r)

def clip_text(font, text, max_width):
    if font.size(text)[0] <= max_width:
        return text
    while len(text) > 1 and font.size(text + "…")[0] > max_width:
        text = text[:-1]
    return text + "…"


# CLASE BOTON

class Button:
    def __init__(self, x, y, width, height, text, color=None, text_color=WHITE,
                 radius=10, font=None, icon=None):
        self.rect   = pygame.Rect(x, y, width, height)
        self.text   = text
        self.color  = color if color else BLUE
        self.tcolor = text_color
        self.radius = radius
        self.font   = font if font else SMALL_FONT
        self.icon   = icon
        self.hovered = False

    def draw(self, surface):
        mp = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mp)
        c = self.color
        if self.hovered:
            c = tuple(min(v + 25, 255) for v in c)
        draw_rounded_rect(surface, c, self.rect, self.radius)
        txt_surf = self.font.render(self.text, True, self.tcolor)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        if self.icon:
            icon_surf = self.font.render(self.icon, True, self.tcolor)
            total_w = icon_surf.get_width() + 6 + txt_surf.get_width()
            ix = self.rect.centerx - total_w // 2
            iy = self.rect.centery - icon_surf.get_height() // 2
            surface.blit(icon_surf, (ix, iy))
            surface.blit(txt_surf, (ix + icon_surf.get_width() + 6, iy))
        else:
            surface.blit(txt_surf, txt_rect)

    def clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN and
                event.button == 1 and
                self.rect.collidepoint(event.pos))


# INPUTS

class InputField:
    def __init__(self, x, y, width, height, value="", max_len=25, font=None):
        self.rect    = pygame.Rect(x, y, width, height)
        self.value   = value
        self.active  = False
        self.max_len = max_len
        self.font    = font if font else TEXT_FONT

    def draw(self, surface):
        border_color = BLUE if self.active else LIGHT
        draw_rounded_rect(surface, WHITE, self.rect, 8, 2, border_color)
        txt = clip_text(self.font, self.value, self.rect.width - 12)
        surf = self.font.render(txt, True, BLACK)
        surface.blit(surf, (self.rect.x + 8, self.rect.y + (self.rect.height - surf.get_height()) // 2))
        if self.active:
            cursor_x = self.rect.x + 8 + self.font.size(txt)[0] + 2
            if (pygame.time.get_ticks() // 500) % 2 == 0:
                pygame.draw.line(surface, BLACK,
                                 (cursor_x, self.rect.y + 6),
                                 (cursor_x, self.rect.bottom - 6), 2)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.value = self.value[:-1]
            elif event.key not in (pygame.K_RETURN, pygame.K_TAB, pygame.K_ESCAPE):
                if len(self.value) < self.max_len:
                    self.value += event.unicode
        return self.active


# ESTADOS GLOBAL

cantidad_productos = 1
procesos_config    = []   # list of dicts
nombre_inputs      = []   # InputField per process
tarea_inputs       = []   # list[list[InputField]]

scroll_y           = 0
SCROLL_SPEED       = 35

simulador          = None
simulation_running = False
simulacion_pausada = False
simulation_done    = False
error_msg          = ""
error_timer        = 0

TIME_EVENT = pygame.USEREVENT + 1

# Mostrar estación por estación
pasos_pendientes = []   


# LÓGICA DE CONFIGURACIÓN

def agregar_proceso():
    idx = len(procesos_config)
    nuevo = {
        "nombre": f"Proceso {idx + 1}",
        "tareas": [],
        "es_inicial": idx == 0,
        "es_final":   False,
    }
    procesos_config.append(nuevo)
    nombre_inputs.append(InputField(0, 0, 200, 32, nuevo["nombre"]))
    tarea_inputs.append([])

def agregar_tarea(proc_idx):
    t_idx = len(procesos_config[proc_idx]["tareas"])
    nueva = {"nombre": f"Tarea {t_idx + 1}", "tiempo": 1}
    procesos_config[proc_idx]["tareas"].append(nueva)
    tarea_inputs[proc_idx].append(InputField(0, 0, 120, 28, nueva["nombre"], max_len=20, font=SMALL_FONT))

def eliminar_proceso(proc_idx):
    if len(procesos_config) <= 1:
        set_error("Debe haber al menos un proceso.")
        return
    procesos_config.pop(proc_idx)
    nombre_inputs.pop(proc_idx)
    tarea_inputs.pop(proc_idx)
    # Reasignar inicial si se eliminó el inicial
    if not any(p["es_inicial"] for p in procesos_config):
        procesos_config[0]["es_inicial"] = True
    # Reasignar final si se eliminó el final
    if not any(p["es_final"] for p in procesos_config):
        procesos_config[-1]["es_final"] = True

def eliminar_tarea(proc_idx, tarea_idx):
    procesos_config[proc_idx]["tareas"].pop(tarea_idx)
    tarea_inputs[proc_idx].pop(tarea_idx)

def set_error(msg):
    global error_msg, error_timer
    error_msg   = msg
    error_timer = 180  # frames ≈ 3 s

def sync_names():
    """Sync InputField values back to procesos_config."""
    for i, proc in enumerate(procesos_config):
        if i < len(nombre_inputs) and nombre_inputs[i].value.strip():
            proc["nombre"] = nombre_inputs[i].value.strip()
        for j, tarea in enumerate(proc["tareas"]):
            if j < len(tarea_inputs[i]) and tarea_inputs[i][j].value.strip():
                tarea["nombre"] = tarea_inputs[i][j].value.strip()

def validar_configuracion():
    sync_names()
    if not procesos_config:
        set_error("Debe haber al menos un proceso.")
        return False
    iniciales = [p for p in procesos_config if p["es_inicial"]]
    finales   = [p for p in procesos_config if p["es_final"]]
    if len(iniciales) != 1:
        set_error("Debe marcarse exactamente UN proceso como inicial.")
        return False
    if len(finales) != 1:
        set_error("Debe marcarse exactamente UN proceso como final.")
        return False
    for proc in procesos_config:
        if not proc["tareas"]:
            set_error(f"'{proc['nombre']}' no tiene tareas.")
            return False
    return True

def construir_simulador():
    global simulador, simulation_running, simulacion_pausada, simulation_done
    sync_names()
    procesos_obj = []
    id_p, id_t = 1, 1
    for pc in procesos_config:
        p = Proceso(id_p, pc["nombre"], pc["es_inicial"], pc["es_final"])
        id_p += 1
        for tc in pc["tareas"]:
            t = Tarea(id_t, tc["nombre"], tc["tiempo"])
            p.agregar_tarea(t)
            id_t += 1
        procesos_obj.append(p)
    productos_obj = [Producto(i + 1) for i in range(cantidad_productos)]
    simulador = Simulador()
    simulador.configurar(procesos_obj, productos_obj)
    # Iniciar la simulación en la línea
    simulador._Simulador__linea.iniciar_simulacion(simulador._Simulador__productos)
    simulation_running = True
    simulacion_pausada = False
    simulation_done    = False
    # Capturar snapshot inicial para mostrarlo de inmediato
    pasos_pendientes.clear()
    snap0 = capturar_snapshot(simulador._Simulador__linea, simulador._Simulador__productos)
    pasos_pendientes.append(snap0)


# HEADER 

def draw_header(title, subtitle=""):
    pygame.draw.rect(screen, BLUE_DARK, (0, 0, WIDTH, 65))
    surf = TITLE_FONT.render("LinProd", True, WHITE)
    screen.blit(surf, (30, 16))
    sep = HEAD_FONT.render("  |  " + title, True, (180, 200, 255))
    screen.blit(sep, (30 + surf.get_width(), 20))
    if subtitle:
        s = SMALL_FONT.render(subtitle, True, (160, 180, 230))
        screen.blit(s, (30 + surf.get_width() + sep.get_width() + 10, 26))


# PANTALLA: MENÚ PRINCIPAL

def draw_menu():
    screen.fill(BG)
    # Gradient-ish top band
    for i in range(200):
        alpha = int(40 * (1 - i / 200))
        pygame.draw.line(screen, (58, 110, 240), (0, 65 + i), (WIDTH, 65 + i))

    # Logo / título
    t1 = TITLE_FONT.render("LinProd", True, WHITE)
    t2 = HEAD_FONT.render("Simulador de Línea de Producción", True, (200, 220, 255))
    screen.blit(t1, t1.get_rect(center=(WIDTH // 2, 130)))
    screen.blit(t2, t2.get_rect(center=(WIDTH // 2, 175)))


    btn = Button(WIDTH // 2 - 160, 420, 320, 60, "Comenzar Configuración", GREEN, radius=14, font=HEAD_FONT)
    btn.draw(screen)

    ver = TINY_FONT.render("CE5507 – Modelación H/S OO  |  I Semestre 2026", True, GRAY)
    screen.blit(ver, ver.get_rect(center=(WIDTH // 2, HEIGHT - 20)))

    return btn

# PANTALLA: CONFIGURACIÓN

def draw_configuration():
    global scroll_y, cantidad_productos, error_timer, error_msg

    screen.fill(BG)
    draw_header("Configuración", "Define los procesos y tareas de la línea")

    # ---- Panel lateral izquierdo (productos + acciones globales) ----
    SIDE = 270
    pygame.draw.rect(screen, WHITE, (0, 65, SIDE, HEIGHT - 65))
    pygame.draw.line(screen, LIGHT, (SIDE, 65), (SIDE, HEIGHT), 2)

    # Cantidad de productos
    screen.blit(HEAD_FONT.render("Productos", True, BLACK), (20, 85))
    screen.blit(SMALL_FONT.render("Cantidad a simular:", True, GRAY), (20, 118))

    minus_btn = Button(20,  148, 40, 40, "−", RED,   radius=8, font=HEAD_FONT)
    plus_btn  = Button(110, 148, 40, 40, "+", GREEN, radius=8, font=HEAD_FONT)
    minus_btn.draw(screen)
    plus_btn.draw(screen)
    val = TITLE_FONT.render(str(cantidad_productos), True, BLUE)
    screen.blit(val, val.get_rect(center=(85, 168)))

    pygame.draw.line(screen, LIGHT, (20, 205), (SIDE - 20, 205), 1)

    # Info de validación
    screen.blit(HEAD_FONT.render("Reglas", True, BLACK), (20, 220))
    rules = [
        "1 proceso inicial",
        "1 proceso final",
        "Cada proceso ≥1 tarea",
        "Orden de ejecución",
    ]
    ry = 250
    for rule in rules:
        screen.blit(SMALL_FONT.render(rule, True, GRAY), (20, ry))
        ry += 22

    pygame.draw.line(screen, LIGHT, (20, ry + 10), (SIDE - 20, ry + 10), 1)

    # Botones de acción
    add_process_btn = Button(15, ry + 20,  240, 44, "+ Agregar Proceso", BLUE,  radius=10, font=TEXT_FONT)
    start_sim_btn   = Button(15, ry + 74,  240, 44, "Iniciar Simulación", GREEN, radius=10, font=TEXT_FONT)
    back_btn        = Button(15, HEIGHT - 65, 240, 44, "Volver al Menú", GRAY, radius=10, font=TEXT_FONT)
    add_process_btn.draw(screen)
    start_sim_btn.draw(screen)
    back_btn.draw(screen)

    # Error message
    if error_timer > 0:
        alpha = min(255, error_timer * 3)
        er = pygame.Surface((SIDE - 20, 36), pygame.SRCALPHA)
        er.fill((220, 70, 70, alpha))
        screen.blit(er, (10, HEIGHT - 115))
        screen.blit(SMALL_FONT.render(error_msg[:34], True, WHITE), (16, HEIGHT - 108))
        error_timer -= 1

    # ---- Área de procesos (scroll) ----
    MAIN_X    = SIDE + 10
    MAIN_W    = WIDTH - MAIN_X - 10
    CARD_H    = 0   # will be dynamic
    y_base    = 80 + scroll_y  # start y inside scrollable area

    # Clip rendering to main area
    clip_rect = pygame.Rect(MAIN_X, 70, MAIN_W, HEIGHT - 70)
    screen.set_clip(clip_rect)

    check_rects  = []
    proc_buttons = []
    time_buttons = []

    for proc_idx, proceso in enumerate(procesos_config):
        n_tareas = max(1, len(proceso["tareas"]))
        CARD_H = 90 + n_tareas * 80
        card_rect = pygame.Rect(MAIN_X, y_base, MAIN_W, CARD_H)

        color_idx = proc_idx % len(PROCESS_COLORS)
        accent = PROCESS_COLORS[color_idx]

        if card_rect.bottom > 70 and card_rect.top < HEIGHT:  # only draw visible cards
            draw_shadow(screen, card_rect, 14, 25)
            draw_rounded_rect(screen, WHITE, card_rect, 14)
            # Left accent bar
            accent_bar = pygame.Rect(MAIN_X, y_base, 6, CARD_H)
            pygame.draw.rect(screen, accent, accent_bar, border_radius=14)

            # ---- Header row ----
            header_y = y_base + 14

            # Process number badge
            badge_r = pygame.Rect(MAIN_X + 16, header_y, 34, 34)
            pygame.draw.circle(screen, accent, badge_r.center, 17)
            screen.blit(HEAD_FONT.render(str(proc_idx + 1), True, WHITE),
                        HEAD_FONT.render(str(proc_idx + 1), True, WHITE).get_rect(center=badge_r.center))

            # Name input field
            fi = nombre_inputs[proc_idx]
            fi.rect = pygame.Rect(MAIN_X + 60, header_y + 1, 220, 32)
            fi.draw(screen)

            # Checkboxes Inicial / Final
            def draw_check(label, value, cx, cy):
                cr = pygame.Rect(cx, cy, 20, 20)
                pygame.draw.rect(screen, (accent if value else LIGHT), cr, border_radius=5)
                pygame.draw.rect(screen, (accent if value else GRAY), cr, width=2, border_radius=5)
                if value:
                    screen.blit(TINY_FONT.render("✓", True, WHITE), (cx + 4, cy + 3))
                screen.blit(SMALL_FONT.render(label, True, BLACK), (cx + 26, cy + 2))
                return cr

            init_rect = draw_check("Inicial", proceso["es_inicial"], MAIN_X + 300, header_y + 7)
            fin_rect  = draw_check("Final",   proceso["es_final"],   MAIN_X + 390, header_y + 7)
            check_rects.append((init_rect, fin_rect, proc_idx))

            # Badges for type
            if proceso["es_inicial"]:
                br = pygame.Rect(MAIN_X + 490, header_y + 5, 65, 24)
                draw_rounded_rect(screen, (255, 100, 130), br, 12)
                screen.blit(TINY_FONT.render("INICIAL", True, WHITE), br.inflate(-8, -4).topleft)
            if proceso["es_final"]:
                br = pygame.Rect(MAIN_X + 490, header_y + 5, 55, 24)
                draw_rounded_rect(screen, GREEN, br, 12)
                screen.blit(TINY_FONT.render("FINAL", True, WHITE), br.inflate(-8, -4).topleft)

            # Botones de proceso
            add_t_btn  = Button(MAIN_W + MAIN_X - 190, header_y,     110, 32, "+ Tarea", TEAL,  radius=8, font=SMALL_FONT)
            del_p_btn  = Button(MAIN_W + MAIN_X - 75,  header_y,     68,  32, "Borrar",  RED,   radius=8, font=SMALL_FONT)
            add_t_btn.draw(screen)
            del_p_btn.draw(screen)
            proc_buttons.append((add_t_btn, del_p_btn, proc_idx))

            # ---- Tareas ----
            task_y = y_base + 58
            for tarea_idx, tarea in enumerate(proceso["tareas"]):
                task_rect = pygame.Rect(MAIN_X + 16, task_y, MAIN_W - 32, 68)
                draw_rounded_rect(screen, PANEL_BG, task_rect, 10, 1, LIGHT)

                # Task number
                num_r = pygame.Rect(MAIN_X + 20, task_y + 20, 28, 28)
                pygame.draw.circle(screen, accent, num_r.center, 14)
                screen.blit(TINY_FONT.render(str(tarea_idx + 1), True, WHITE),
                            TINY_FONT.render(str(tarea_idx + 1), True, WHITE).get_rect(center=num_r.center))

                # Tarea name input
                ti = tarea_inputs[proc_idx][tarea_idx]
                ti.rect = pygame.Rect(MAIN_X + 56, task_y + 20, 180, 28)
                ti.draw(screen)

                # Tiempo label + buttons
                tx = MAIN_X + 250
                screen.blit(SMALL_FONT.render("Ciclos:", True, GRAY), (tx, task_y + 24))
                tm_btn = Button(tx + 52,  task_y + 20, 26, 28, "−", RED,   radius=6, font=HEAD_FONT)
                tp_btn = Button(tx + 110, task_y + 20, 26, 28, "+", GREEN, radius=6, font=HEAD_FONT)
                tm_btn.draw(screen)
                tp_btn.draw(screen)
                val_s = HEAD_FONT.render(str(tarea["tiempo"]), True, BLUE)
                screen.blit(val_s, val_s.get_rect(center=(tx + 95, task_y + 34)))
                time_buttons.append((tm_btn, tp_btn, proc_idx, tarea_idx))

                # Delete task button
                del_t = Button(MAIN_W + MAIN_X - 75, task_y + 20, 65, 28, "✕ Borrar", RED, radius=6, font=TINY_FONT)
                del_t.draw(screen)
                # Store del_t in time_buttons as extra (we'll check separately)
                time_buttons[-1] = (tm_btn, tp_btn, proc_idx, tarea_idx, del_t)

                task_y += 80

            # Arrow to next process
            if proc_idx < len(procesos_config) - 1:
                ax = MAIN_X + MAIN_W // 2
                ay = y_base + CARD_H + 8
                pygame.draw.polygon(screen, LIGHT, [
                    (ax - 12, ay), (ax + 12, ay), (ax, ay + 14)
                ])

        y_base += CARD_H + 30

    screen.set_clip(None)

    return (add_process_btn, start_sim_btn, back_btn, minus_btn, plus_btn,
            check_rects, proc_buttons, time_buttons)


# =========================================
# SNAPSHOT: captura estado visual actual
# =========================================
def capturar_snapshot(linea, productos_todos):
    """
    Captura el estado actual de cada tarea: qué producto está en el slot
    y qué productos están en cola. Se guarda como estructura de datos pura
    (sin referencias a objetos que pueden mutar) para poder dibujarlo
    aunque el modelo ya avanzó.
    """
    snap = {
        "ciclo": linea.tiempo_actual,
        "procesos": []
    }
    for proceso in linea.procesos:
        proc_snap = {"nombre": proceso.nombre, "es_inicial": proceso.es_inicial,
                     "es_final": proceso.es_final, "tareas": []}
        for tarea in proceso.tareas:
            prod_id   = tarea.producto_actual.id if tarea.producto_actual else None
            cola_ids  = [p.id for p in tarea.cola_productos]
            proc_snap["tareas"].append({
                "nombre":     tarea.nombre,
                "tiempo":     tarea.tiempo_procesamiento,
                "restante":   tarea.tiempo_restante,
                "ocupada":    tarea.ocupada,
                "prod_id":    prod_id,
                "cola_ids":   cola_ids,
            })
        snap["procesos"].append(proc_snap)
    snap["completados"] = [p.id for p in productos_todos if p.estado == "completado"]
    snap["total"]       = len(productos_todos)
    return snap


# PANTALLA: SIMULACIÓN
# Columnas = Procesos  |  Dentro = Tareas apiladas
# Dibuja desde un snapshot (estado inmutable)

def draw_simulation_snap(snap):
    """Dibuja la pantalla de simulación a partir de un snapshot."""
    procesos_snap = snap["procesos"]
    n_proc        = len(procesos_snap)
    max_tasks     = max((len(p["tareas"]) for p in procesos_snap), default=1)

    MARGIN  = 20
    ARROW_W = 30
    PROC_W  = max(180, (WIDTH - MARGIN * 2 - ARROW_W * (n_proc - 1)) // max(n_proc, 1))
    TASK_H  = max(110, (HEIGHT - 165) // max(max_tasks, 1) - 10)
    COL_TOP = 80

    for proc_idx, proc_snap in enumerate(procesos_snap):
        accent = PROCESS_COLORS[proc_idx % len(PROCESS_COLORS)]
        px = MARGIN + proc_idx * (PROC_W + ARROW_W)

        # ── Cabecera proceso ─────────────────────────────────────────
        header_rect = pygame.Rect(px, COL_TOP, PROC_W, 38)
        draw_rounded_rect(screen, accent, header_rect, 10)
        type_tag = " [I]" if proc_snap["es_inicial"] else (" [F]" if proc_snap["es_final"] else "")
        h_text = clip_text(SMALL_FONT, proc_snap["nombre"] + type_tag, PROC_W - 16)
        render_text_centered(screen, SMALL_FONT, h_text, WHITE, header_rect)

        # ── Tarjetas de tarea ────────────────────────────────────────
        for t_idx, tsnap in enumerate(proc_snap["tareas"]):
            ty   = COL_TOP + 48 + t_idx * (TASK_H + 8)
            card = pygame.Rect(px, ty, PROC_W, TASK_H)

            ocupada  = tsnap["ocupada"]
            card_bg  = (255, 247, 247) if ocupada else WHITE
            bord_col = accent if ocupada else LIGHT
            draw_shadow(screen, card, 10, 14)
            draw_rounded_rect(screen, card_bg, card, 10, 2, bord_col)

            # Nombre + ciclos
            screen.blit(HEAD_FONT.render(clip_text(HEAD_FONT, tsnap["nombre"], PROC_W - 20),
                                         True, BLACK), (px + 10, ty + 8))
            screen.blit(TINY_FONT.render(f"Ciclos: {tsnap['tiempo']}", True, GRAY),
                        (px + 10, ty + 30))

            # ── Slot de PROCESANDO ────────────────────────────────────
            slot_size = 44
            slot_x    = px + PROC_W - slot_size - 10
            slot_y    = ty + 10
            slot_rect = pygame.Rect(slot_x, slot_y, slot_size, slot_size)
            slot_bg   = (220, 230, 255) if ocupada else (230, 235, 245)
            draw_rounded_rect(screen, slot_bg, slot_rect, 8, 2,
                              accent if ocupada else (190, 200, 215))

            if tsnap["prod_id"] is not None:
                pcol = PRODUCT_COLORS.get((tsnap["prod_id"] - 1) % 199 + 1, BLUE)
                pygame.draw.circle(screen, pcol, slot_rect.center, 18)
                pid_s = SMALL_FONT.render(str(tsnap["prod_id"]), True, WHITE)
                screen.blit(pid_s, pid_s.get_rect(center=slot_rect.center))
            else:
                es = TINY_FONT.render("libre", True, (190, 200, 215))
                screen.blit(es, es.get_rect(center=slot_rect.center))

            # ── Barra de progreso ─────────────────────────────────────
            bar_y  = slot_y + slot_size + 4
            bar_bg = pygame.Rect(slot_x, bar_y, slot_size, 6)
            draw_rounded_rect(screen, (210, 215, 225), bar_bg, 3)
            if ocupada and tsnap["tiempo"] > 0:
                pct = 1.0 - tsnap["restante"] / tsnap["tiempo"]
                fw  = max(4, int(slot_size * pct))
                draw_rounded_rect(screen, accent,
                                  pygame.Rect(slot_x, bar_y, fw, 6), 3)

            # ── Cola de espera ────────────────────────────────────────
            cola_ids     = tsnap["cola_ids"]
            cola_label_y = ty + 48
            screen.blit(TINY_FONT.render("Cola:", True, GRAY), (px + 10, cola_label_y))

            avail_w  = slot_x - px - 16
            r_c      = 11
            gap      = 4
            max_show = max(1, avail_w // (r_c * 2 + gap))
            for ci, cid in enumerate(cola_ids[:max_show]):
                pcol = PRODUCT_COLORS.get((cid - 1) % 199 + 1, BLUE)
                cx_c = px + 10 + ci * (r_c * 2 + gap) + r_c
                cy_c = cola_label_y + 18
                pygame.draw.circle(screen, pcol, (cx_c, cy_c), r_c)
                ns = TINY_FONT.render(str(cid), True, WHITE)
                screen.blit(ns, ns.get_rect(center=(cx_c, cy_c)))
            if len(cola_ids) > max_show:
                ex_x = px + 10 + max_show * (r_c * 2 + gap)
                screen.blit(TINY_FONT.render(f"+{len(cola_ids) - max_show}", True, GRAY),
                            (ex_x, cola_label_y + 10))

            # Ciclos restantes (si está ocupada)
            if ocupada:
                rs = TINY_FONT.render(f"Restante: {tsnap['restante']}", True, ORANGE)
                screen.blit(rs, (px + 10, ty + TASK_H - 18))

        # ── Flecha → siguiente proceso ────────────────────────────────
        if proc_idx < n_proc - 1:
            ax = px + PROC_W + 4
            ay = COL_TOP + 38 + max_tasks * (TASK_H + 8) // 2
            pygame.draw.line(screen, BLUE, (ax, ay), (ax + ARROW_W - 8, ay), 2)
            pygame.draw.polygon(screen, BLUE, [
                (ax + ARROW_W - 8, ay - 6),
                (ax + ARROW_W - 8, ay + 6),
                (ax + ARROW_W,     ay),
            ])

    # ── Barra inferior: completados ───────────────────────────────────
    completados = snap["completados"]
    total       = snap["total"]
    done_s = SMALL_FONT.render(f"Completados: {len(completados)} / {total}", True,
                                GREEN if completados else GRAY)
    screen.blit(done_s, (MARGIN, HEIGHT - 54))
    for ci, cid in enumerate(completados[:20]):
        pcol = PRODUCT_COLORS.get((cid - 1) % 199 + 1, BLUE)
        bx = MARGIN + done_s.get_width() + 14 + ci * 26
        if bx + 22 < WIDTH - 580:
            pygame.draw.circle(screen, pcol, (bx + 10, HEIGHT - 40), 11)
            ns = TINY_FONT.render(str(cid), True, WHITE)
            screen.blit(ns, ns.get_rect(center=(bx + 10, HEIGHT - 40)))


def draw_simulation():
    """Wrapper: dibuja header + controles + llama draw_simulation_snap."""
    global simulation_done

    screen.fill(BG)
    linea = simulador._Simulador__linea if simulador else None

    if linea and not linea.hay_trabajo_pendiente() and not simulation_done and not pasos_pendientes:
        simulation_done = True

    # ── Header ────────────────────────────────────────────────────────
    status_color = ORANGE if simulacion_pausada else (GREEN if simulation_done else BLUE)
    status_text  = "PAUSADA" if simulacion_pausada else ("COMPLETADA ✓" if simulation_done else "EN EJECUCIÓN")

    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, 70))
    pygame.draw.line(screen, LIGHT, (0, 70), (WIDTH, 70), 2)
    screen.blit(TITLE_FONT.render("Simulacion de Produccion", True, BLACK), (30, 18))

    ciclo = pasos_pendientes[0]["ciclo"] if pasos_pendientes else (linea.tiempo_actual if linea else 0)
    ciclo_s = HEAD_FONT.render(f"Ciclo {ciclo}", True, BLUE)
    screen.blit(ciclo_s, (WIDTH - ciclo_s.get_width() - 20, 22))
    sb = pygame.Rect(WIDTH - ciclo_s.get_width() - 160, 15, 130, 38)
    draw_rounded_rect(screen, status_color, sb, 10)
    render_text_centered(screen, SMALL_FONT, status_text, WHITE, sb)

    if linea is None:
        screen.blit(TEXT_FONT.render("Simulador no inicializado.", True, RED), (100, 200))
    elif pasos_pendientes:
        draw_simulation_snap(pasos_pendientes[0])
    else:
        # Sin pasos pendientes: capturar estado actual
        snap = capturar_snapshot(linea, simulador._Simulador__productos)
        draw_simulation_snap(snap)

    # ── Botones ───────────────────────────────────────────────────────
    pause_label = "⏸ Pausar" if not simulacion_pausada else "▶ Reanudar"
    pause_c     = ORANGE if not simulacion_pausada else GREEN
    pause_btn  = Button(WIDTH - 360, HEIGHT - 58, 160, 44, pause_label,    pause_c, radius=10, font=TEXT_FONT)
    report_btn = Button(WIDTH - 190, HEIGHT - 58, 175, 44, "Ver Reporte",  PURPLE,  radius=10, font=TEXT_FONT)
    reconf_btn = Button(WIDTH - 560, HEIGHT - 58, 185, 44, "Reconfigurar", GRAY,    radius=10, font=TEXT_FONT)
    pause_btn.draw(screen)
    report_btn.draw(screen)
    reconf_btn.draw(screen)

    return pause_btn, report_btn, reconf_btn

# PANTALLA: REPORTE

def draw_report():
    screen.fill(BG)
    draw_header("Reporte Final", "Estadísticas de la simulación completada")

    from Reporte import Reporte

    content_y = 80
    if not simulador:
        screen.blit(TEXT_FONT.render("Sin datos de simulación.", True, RED), (60, content_y))
    else:
        linea     = simulador._Simulador__linea
        productos = simulador._Simulador__productos

        rep = Reporte()
        rep.generar(linea, productos)

        # ---- Two-column layout ----
        COL1_X = 60
        COL2_X = WIDTH // 2 + 30
        y1 = content_y + 10
        y2 = content_y + 10

        def stat_card(x, y, label, value, color=BLUE, w=580):
            r = pygame.Rect(x, y, w, 56)
            draw_shadow(screen, r, 10, 20)
            draw_rounded_rect(screen, WHITE, r, 10)
            accent_b = pygame.Rect(x, y, 5, 56)
            pygame.draw.rect(screen, color, accent_b, border_radius=10)
            screen.blit(SMALL_FONT.render(label, True, GRAY),  (x + 18, y + 8))
            screen.blit(HEAD_FONT.render(str(value), True, BLACK), (x + 18, y + 28))
            return y + 64

        # Left column
        y1 = stat_card(COL1_X, y1, "Tiempo primer producto en salir",
                       f"{rep._Reporte__tiempoPrimerProducto} ciclos", BLUE)
        y1 = stat_card(COL1_X, y1, "Tiempo último producto en salir",
                       f"{rep._Reporte__tiempoUltimoProducto} ciclos", BLUE)
        y1 = stat_card(COL1_X, y1, "Tiempo total de la simulación",
                       f"{rep._Reporte__tiempoTotalProcesamiento} ciclos", TEAL)
        y1 = stat_card(COL1_X, y1, "Promedio de espera por producto",
                       f"{rep._Reporte__promedioEsperaProducto:.2f} ciclos", TEAL)

        # Productos completados
        completados = [p for p in productos if p.estado == "completado"]
        y1 = stat_card(COL1_X, y1, "Productos completados",
                       f"{len(completados)} / {len(productos)}", GREEN)

        # Right column
        if rep._Reporte__cuelloBotella:
            proc = rep._Reporte__cuelloBotella
            y2 = stat_card(COL2_X, y2, "Cuello de Botella (proceso)",
                           f"{proc.nombre}  (ID {proc.id})", RED)
        if rep._Reporte__procesoMayorEspera:
            proc = rep._Reporte__procesoMayorEspera
            y2 = stat_card(COL2_X, y2, "Proceso con mayor espera",
                           f"{proc.nombre}  (ID {proc.id})", ORANGE)
        if rep._Reporte__tareaMayorEspera:
            tarea = rep._Reporte__tareaMayorEspera
            y2 = stat_card(COL2_X, y2, "Tarea con mayor espera",
                           f"{tarea.nombre}  (ID {tarea.id})", ORANGE)

        # Per-product table
        table_y = max(y1, y2) + 20
        if table_y < HEIGHT - 120:
            screen.blit(HEAD_FONT.render("Detalle por Producto", True, BLACK), (COL1_X, table_y))
            table_y += 30
            cols = ["ID", "Ingreso", "Salida", "Total", "Estado"]
            col_x = [COL1_X, COL1_X + 80, COL1_X + 160, COL1_X + 240, COL1_X + 330]
            for i, col in enumerate(cols):
                screen.blit(SMALL_FONT.render(col, True, GRAY), (col_x[i], table_y))
            table_y += 22
            pygame.draw.line(screen, LIGHT, (COL1_X, table_y), (COL1_X + 500, table_y), 1)
            table_y += 4
            for p in productos[:10]:
                total = p.obtener_tiempo_total()
                row = [str(p.id),
                       str(p.tiempo_ingreso) if p.tiempo_ingreso is not None else "-",
                       str(p.tiempo_salida)  if p.tiempo_salida  is not None else "-",
                       str(total) if total is not None else "-",
                       p.estado]
                rc = GREEN if p.estado == "completado" else ORANGE
                for i, val in enumerate(row):
                    color = rc if i == 4 else BLACK
                    screen.blit(TINY_FONT.render(val, True, color), (col_x[i], table_y))
                table_y += 18
            if len(productos) > 10:
                screen.blit(TINY_FONT.render(f"… y {len(productos)-10} más", True, GRAY), (COL1_X, table_y))

    # Buttons
    back_btn   = Button(40, HEIGHT - 60, 170, 44, "← Menú", GRAY,   radius=10, font=TEXT_FONT)
    reconf_btn = Button(220, HEIGHT - 60, 200, 44, "⚙ Reconfigurar", BLUE,  radius=10, font=TEXT_FONT)
    reinit_btn = Button(430, HEIGHT - 60, 200, 44, "↺ Reiniciar sim.", TEAL, radius=10, font=TEXT_FONT)
    back_btn.draw(screen)
    reconf_btn.draw(screen)
    reinit_btn.draw(screen)

    return back_btn, reconf_btn, reinit_btn


# LOOP PRINCIPAL

def main():
    global scene, scroll_y, cantidad_productos
    global simulacion_pausada, simulador, simulation_done, pasos_pendientes

    scene = "menu"

    # Proceso por defecto al iniciar
    if not procesos_config:
        agregar_proceso()
        agregar_tarea(0)

    running = True
    pygame.time.set_timer(TIME_EVENT, 800)  # 800 ms por ciclo

    while running:
        start_btn   = None
        add_proc    = None
        start_sim   = None
        back_btn    = None
        minus_btn   = None
        plus_btn    = None
        check_rects  = []
        proc_buttons = []
        time_buttons = []
        pause_btn   = None
        report_btn  = None
        reconf_btn  = None
        report_back = None
        report_rec  = None
        report_rei  = None

        # ---- Render ----
        if scene == "menu":
            start_btn = draw_menu()

        elif scene == "config":
            (add_proc, start_sim, back_btn, minus_btn, plus_btn,
             check_rects, proc_buttons, time_buttons) = draw_configuration()

        elif scene == "simulation":
            pause_btn, report_btn, reconf_btn = draw_simulation()

        elif scene == "report":
            report_back, report_rec, report_rei = draw_report()

        # ---- Eventos ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Auto-avance de ciclo
            if event.type == TIME_EVENT:
                if (scene == "simulation" and not simulacion_pausada
                        and simulador and not simulation_done):
                    # Consumir el snapshot visible
                    if pasos_pendientes:
                        pasos_pendientes.pop(0)
                    # Si ya no quedan pasos pendientes, avanzar el modelo
                    if not pasos_pendientes:
                        linea = simulador._Simulador__linea
                        if linea.hay_trabajo_pendiente():
                            linea.avanzar_ciclo()
                            # Capturar nuevo snapshot post-ciclo
                            snap = capturar_snapshot(linea, simulador._Simulador__productos)
                            pasos_pendientes.append(snap)
                        else:
                            simulation_done = True

            # Scroll en config
            if scene == "config" and event.type == pygame.MOUSEWHEEL:
                scroll_y -= event.y * SCROLL_SPEED
                total_h = len(procesos_config) * 310
                scroll_y = max(-(total_h - 400), min(0, scroll_y))

            # Forward keyboard to inputs
            if scene == "config":
                for fi in nombre_inputs:
                    fi.handle_event(event)
                for ti_list in tarea_inputs:
                    for ti in ti_list:
                        ti.handle_event(event)

            # ===== MENÚ =====
            if scene == "menu":
                if start_btn and start_btn.clicked(event):
                    scene = "config"

            # ===== CONFIGURACIÓN =====
            elif scene == "config":
                if minus_btn and minus_btn.clicked(event) and cantidad_productos > 1:
                    cantidad_productos -= 1
                if plus_btn and plus_btn.clicked(event):
                    cantidad_productos += 1

                if add_proc and add_proc.clicked(event):
                    agregar_proceso()

                if back_btn and back_btn.clicked(event):
                    scene = "menu"

                if start_sim and start_sim.clicked(event):
                    sync_names()
                    if validar_configuracion():
                        construir_simulador()
                        scene = "simulation"

                # Checkboxes
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for init_r, fin_r, pi in check_rects:
                        if init_r.collidepoint(event.pos):
                            # Toggle inicial (exclusive)
                            if not procesos_config[pi]["es_inicial"]:
                                for p in procesos_config: p["es_inicial"] = False
                                procesos_config[pi]["es_inicial"] = True
                                procesos_config[pi]["es_final"]   = False
                        if fin_r.collidepoint(event.pos):
                            # Toggle final (exclusive)
                            if not procesos_config[pi]["es_final"]:
                                for p in procesos_config: p["es_final"] = False
                                procesos_config[pi]["es_final"]   = True
                                procesos_config[pi]["es_inicial"] = False

                # Process buttons
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for add_t, del_p, pi in proc_buttons:
                        if add_t.clicked(event):
                            agregar_tarea(pi)
                        if del_p.clicked(event):
                            eliminar_proceso(pi)

                # Time / delete task buttons
                for entry in time_buttons:
                    tm, tp, pi, ti = entry[0], entry[1], entry[2], entry[3]
                    del_t = entry[4] if len(entry) > 4 else None
                    if tm.clicked(event):
                        if procesos_config[pi]["tareas"][ti]["tiempo"] > 1:
                            procesos_config[pi]["tareas"][ti]["tiempo"] -= 1
                    if tp.clicked(event):
                        procesos_config[pi]["tareas"][ti]["tiempo"] += 1
                    if del_t and del_t.clicked(event):
                        if len(procesos_config[pi]["tareas"]) > 1:
                            eliminar_tarea(pi, ti)
                        else:
                            set_error("Un proceso necesita al menos 1 tarea.")

            # ===== SIMULACIÓN =====
            elif scene == "simulation":
                if pause_btn and pause_btn.clicked(event):
                    simulacion_pausada = not simulacion_pausada
                    if simulacion_pausada:
                        linea = simulador._Simulador__linea
                        print("\n" + "=" * 60)
                        print(f"PAUSA EN CICLO {linea.tiempo_actual}")
                        print(linea.mostrar_estado())
                        print("=" * 60 + "\n")

                if report_btn and report_btn.clicked(event):
                    scene = "report"

                if reconf_btn and reconf_btn.clicked(event):
                    simulacion_pausada = False
                    scene = "config"

            # ===== REPORTE =====
            elif scene == "report":
                if report_back and report_back.clicked(event):
                    scene = "menu"
                if report_rec and report_rec.clicked(event):
                    simulacion_pausada = False
                    scene = "config"
                if report_rei and report_rei.clicked(event):
                    # Reiniciar con misma configuración
                    construir_simulador()
                    scene = "simulation"

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()