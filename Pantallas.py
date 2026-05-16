"""
Pantallas.py — Las 4 pantallas de la aplicación como métodos de una clase.
Cada draw_* dibuja la pantalla y devuelve lo que la Interfaz
necesita para procesar los eventos.
Toda la lógica (agregar procesos, construir simulador, etc.)
está en Interfaz; aquí solo se dibuja.
"""

import pygame
import Constantes as C
from ComponentesUI import (Button, InputField,
                            draw_rounded_rect,
                            render_text_centered, clip_text, draw_header)


class Pantallas:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen

    # Menú principal
    def draw_menu(self):
        """Retorna: start_btn"""
        s = self.screen
        s.fill(C.BG)

        pygame.draw.rect(s, C.BLUE, (0, 0, C.WIDTH, 300))

        t1 = C.TITLE_FONT.render("LinProd", True, C.WHITE)
        t2 = C.HEAD_FONT.render("Simulador de Línea de Producción", True, (200, 220, 255))
        s.blit(t1, t1.get_rect(center=(C.WIDTH // 2, 130)))
        s.blit(t2, t2.get_rect(center=(C.WIDTH // 2, 175)))

        btn = Button(C.WIDTH // 2 - 160, 350, 320, 60,
                     "Comenzar Configuración", C.GREEN, radius=14, font=C.HEAD_FONT)
        btn.draw(s)

        ver = C.SMALL_FONT.render(
            "CE5507 – Modelación HW/SW |  I Semestre 2026 | "
            "Marisa Méndez, Carolina Montero, Diana Obando, Carolina Vargas, Albert Vega",
            True, C.GRAY
        )
        s.blit(ver, ver.get_rect(center=(C.WIDTH // 2, C.HEIGHT - 20)))
        return btn

    # Configuración
    def draw_configuration(self):
        """
        Retorna:
          (add_proc_btn, start_sim_btn, back_btn, minus_btn, plus_btn,
           check_rects, proc_buttons, time_buttons)
        """
        s   = self.screen
        est = C.estado
        s.fill(C.BG)
        draw_header(s, "Configuración", "Define los procesos y tareas de la línea")

        SIDE = 270
        # Panel lateral
        pygame.draw.rect(s, C.WHITE, (0, 65, SIDE, C.HEIGHT - 65))
        pygame.draw.line(s, C.LIGHT, (SIDE, 65), (SIDE, C.HEIGHT), 2)

        s.blit(C.HEAD_FONT.render("Productos", True, C.BLACK),          (20, 85))
        s.blit(C.SMALL_FONT.render("Cantidad a simular:", True, C.GRAY), (20, 118))

        minus_btn = Button(20,  148, 40, 40, "−", C.RED,   radius=8, font=C.HEAD_FONT)
        plus_btn  = Button(110, 148, 40, 40, "+", C.GREEN, radius=8, font=C.HEAD_FONT)
        minus_btn.draw(s)
        plus_btn.draw(s)
        val = C.TITLE_FONT.render(str(est["cantidad_productos"]), True, C.BLUE)
        s.blit(val, val.get_rect(center=(85, 168)))

        pygame.draw.line(s, C.LIGHT, (20, 205), (SIDE - 20, 205), 1)

        s.blit(C.HEAD_FONT.render("Reglas", True, C.BLACK), (20, 220))
        ry = 250
        for rule in ["1 proceso inicial", "1 proceso final",
                     "Cada proceso ≥1 tarea", "Orden de ejecución"]:
            s.blit(C.SMALL_FONT.render(rule, True, C.GRAY), (20, ry))
            ry += 22

        pygame.draw.line(s, C.LIGHT, (20, ry + 10), (SIDE - 20, ry + 10), 1)

        add_proc_btn  = Button(15, ry + 20, 240, 44, "+ Agregar Proceso",   C.BLUE,  radius=10, font=C.TEXT_FONT)
        start_sim_btn = Button(15, ry + 74, 240, 44, "Iniciar Simulación",  C.GREEN, radius=10, font=C.TEXT_FONT)
        back_btn      = Button(15, C.HEIGHT - 65, 240, 44, "Volver al Menú", C.GRAY, radius=10, font=C.TEXT_FONT)
        add_proc_btn.draw(s)
        start_sim_btn.draw(s)
        back_btn.draw(s)

        # Mensaje de error
        if est["error_timer"] > 0:
            alpha = min(255, est["error_timer"] * 3)
            er = pygame.Surface((SIDE - 20, 36), pygame.SRCALPHA)
            er.fill((220, 70, 70, alpha))
            s.blit(er, (10, C.HEIGHT - 115))
            s.blit(C.SMALL_FONT.render(est["error_msg"][:34], True, C.WHITE), (16, C.HEIGHT - 108))
            est["error_timer"] -= 1

        # Área de procesos con scroll
        MAIN_X = SIDE + 10
        MAIN_W = C.WIDTH - MAIN_X - 10
        y_base = 80 + est["scroll_y"]

        s.set_clip(pygame.Rect(MAIN_X, 70, MAIN_W, C.HEIGHT - 70))

        check_rects  = []
        proc_buttons = []
        time_buttons = []

        for pi, proceso in enumerate(est["procesos_config"]):
            CARD_H    = 90 + max(1, len(proceso["tareas"])) * 80
            card_rect = pygame.Rect(MAIN_X, y_base, MAIN_W, CARD_H)
            accent    = C.PROCESS_COLORS[pi % len(C.PROCESS_COLORS)]

            if card_rect.bottom > 70 and card_rect.top < C.HEIGHT:
                draw_rounded_rect(s, C.WHITE, card_rect, 14)
                pygame.draw.rect(s, accent,
                                 pygame.Rect(MAIN_X, y_base, 6, CARD_H),
                                 border_radius=14)

                header_y = y_base + 14

                # Id. número
                bc = pygame.Rect(MAIN_X + 16, header_y, 34, 34)
                pygame.draw.circle(s, accent, bc.center, 17)
                num_s = C.HEAD_FONT.render(str(pi + 1), True, C.WHITE)
                s.blit(num_s, num_s.get_rect(center=bc.center))

                # Input nombre
                fi = est["nombre_inputs"][pi]
                fi.rect = pygame.Rect(MAIN_X + 60, header_y + 1, 220, 32)
                fi.draw(s)

                # Checkboxes
                init_r = self._draw_checkbox(s, "Inicial", proceso["es_inicial"], accent, MAIN_X + 300, header_y + 7)
                fin_r  = self._draw_checkbox(s, "Final",   proceso["es_final"],   accent, MAIN_X + 390, header_y + 7)
                check_rects.append((init_r, fin_r, pi))

                # Badges tipo
                tag_x = MAIN_X + 490
                if proceso["es_inicial"]:
                    br = pygame.Rect(tag_x, header_y + 5, 65, 24)
                    draw_rounded_rect(s, (255, 100, 130), br, 12)
                    render_text_centered(s, C.TINY_FONT, "INICIAL", C.WHITE, br)
                if proceso["es_final"]:
                    br = pygame.Rect(tag_x, header_y + 5, 55, 24)
                    draw_rounded_rect(s, C.GREEN, br, 12)
                    render_text_centered(s, C.TINY_FONT, "FINAL", C.WHITE, br)

                # Botones proceso
                add_t = Button(MAIN_W + MAIN_X - 190, header_y, 110, 32, "+ Tarea", C.TEAL, radius=8, font=C.SMALL_FONT)
                del_p = Button(MAIN_W + MAIN_X - 75,  header_y,  68, 32, "Borrar",  C.RED,  radius=8, font=C.SMALL_FONT)
                add_t.draw(s)
                del_p.draw(s)
                proc_buttons.append((add_t, del_p, pi))

                # Tareas
                task_y = y_base + 58
                for ti, tarea in enumerate(proceso["tareas"]):
                    task_y, entry = self._draw_task_row(s, task_y, pi, ti, tarea, accent, MAIN_X, MAIN_W)
                    time_buttons.append(entry)

            y_base += CARD_H + 30

        s.set_clip(None)
        return (add_proc_btn, start_sim_btn, back_btn, minus_btn, plus_btn,
                check_rects, proc_buttons, time_buttons)

    def _draw_checkbox(self, surface, label, value, accent, cx, cy):
        cr = pygame.Rect(cx, cy, 20, 20)
        pygame.draw.rect(surface, accent if value else C.LIGHT, cr, border_radius=5)
        pygame.draw.rect(surface, accent if value else C.GRAY,  cr, width=2, border_radius=5)
        if value:
            surface.blit(C.TINY_FONT.render("X", True, C.WHITE), (cx + 4, cy + 3))
        surface.blit(C.SMALL_FONT.render(label, True, C.BLACK), (cx + 26, cy + 2))
        return cr

    def _draw_task_row(self, surface, task_y, pi, ti, tarea, accent, MAIN_X, MAIN_W):
        """Dibuja una fila de tarea y retorna (next_y, time_button_entry)."""
        task_rect = pygame.Rect(MAIN_X + 16, task_y, MAIN_W - 32, 68)
        draw_rounded_rect(surface, C.PANEL_BG, task_rect, 10, 1, C.LIGHT)

        num_r = pygame.Rect(MAIN_X + 20, task_y + 20, 28, 28)
        pygame.draw.circle(surface, accent, num_r.center, 14)
        num_s = C.TINY_FONT.render(str(ti + 1), True, C.WHITE)
        surface.blit(num_s, num_s.get_rect(center=num_r.center))

        inp = C.estado["tarea_inputs"][pi][ti]
        inp.rect = pygame.Rect(MAIN_X + 56, task_y + 20, 180, 28)
        inp.draw(surface)

        tx = MAIN_X + 250
        surface.blit(C.SMALL_FONT.render("Ciclos:", True, C.GRAY), (tx, task_y + 24))
        tm = Button(tx + 52,  task_y + 20, 26, 28, "−", C.RED,   radius=6, font=C.HEAD_FONT)
        tp = Button(tx + 110, task_y + 20, 26, 28, "+", C.GREEN, radius=6, font=C.HEAD_FONT)
        tm.draw(surface)
        tp.draw(surface)
        val_s = C.HEAD_FONT.render(str(tarea["tiempo"]), True, C.BLUE)
        surface.blit(val_s, val_s.get_rect(center=(tx + 95, task_y + 34)))

        del_t = Button(MAIN_W + MAIN_X - 90, task_y + 20, 65, 28,
                       "Borrar", C.RED, radius=6, font=C.TINY_FONT)
        del_t.draw(surface)

        return task_y + 80, (tm, tp, pi, ti, del_t)

    # Simulación

    def draw_simulation(self):
        """Retorna: (pause_btn, report_btn, reconf_btn)"""
        s   = self.screen
        est = C.estado
        s.fill(C.BG)

        simulador = est["simulador"]
        linea     = simulador._Simulador__linea if simulador else None

        # Detectar fin
        if (linea and not linea.hay_trabajo_pendiente()
                and not est["simulation_done"]
                and not est["pasos_pendientes"]):
            est["simulation_done"] = True

        # Header
        status_color = C.ORANGE if est["simulacion_pausada"] else (C.GREEN if est["simulation_done"] else C.BLUE)
        status_text  = "PAUSADA" if est["simulacion_pausada"] else ("COMPLETADA" if est["simulation_done"] else "EN EJECUCIÓN")

        pygame.draw.rect(s, C.WHITE, (0, 0, C.WIDTH, 70))
        pygame.draw.line(s, C.LIGHT, (0, 70), (C.WIDTH, 70), 2)
        s.blit(C.TITLE_FONT.render("Simulacion de Produccion", True, C.BLACK), (30, 18))

        ciclo = (est["pasos_pendientes"][0]["ciclo"] if est["pasos_pendientes"]
                 else (linea.tiempo_actual if linea else 0))
        ciclo_s = C.HEAD_FONT.render(f"Ciclo {ciclo}", True, C.BLUE)
        s.blit(ciclo_s, (C.WIDTH - ciclo_s.get_width() - 20, 22))
        sb = pygame.Rect(C.WIDTH - ciclo_s.get_width() - 160, 15, 130, 38)
        draw_rounded_rect(s, status_color, sb, 10)
        render_text_centered(s, C.SMALL_FONT, status_text, C.WHITE, sb)

        if linea is None:
            s.blit(C.TEXT_FONT.render("Simulador no inicializado.", True, C.RED), (100, 200))
        elif est["pasos_pendientes"]:
            self._draw_simulation_snap(est["pasos_pendientes"][0])
        else:
            snap = self._capturar_snapshot(linea, simulador._Simulador__productos)
            self._draw_simulation_snap(snap)

        # Botones
        pause_label = "Pausar" if not est["simulacion_pausada"] else "Reanudar"
        pause_c     = C.ORANGE if not est["simulacion_pausada"] else C.GREEN
        pause_btn  = Button(C.WIDTH - 360, C.HEIGHT - 58, 160, 44, pause_label,    pause_c,  radius=10, font=C.TEXT_FONT)
        report_btn = Button(C.WIDTH - 190, C.HEIGHT - 58, 175, 44, "Ver Reporte",  C.PURPLE, radius=10, font=C.TEXT_FONT)
        reconf_btn = Button(C.WIDTH - 560, C.HEIGHT - 58, 185, 44, "Reconfigurar", C.GRAY,   radius=10, font=C.TEXT_FONT)
        pause_btn.draw(s)
        report_btn.draw(s)
        reconf_btn.draw(s)
        return pause_btn, report_btn, reconf_btn

    def _capturar_snapshot(self, linea, productos_todos):
        """Captura el estado visual actual."""
        snap = {"ciclo": linea.tiempo_actual, "procesos": []}
        for proceso in linea.procesos:
            proc_snap = {
                "nombre": proceso.nombre,
                "es_inicial": proceso.es_inicial,
                "es_final": proceso.es_final,
                "tareas": [],
            }
            for tarea in proceso.tareas:
                proc_snap["tareas"].append({
                    "nombre":   tarea.nombre,
                    "tiempo":   tarea.tiempo_procesamiento,
                    "restante": tarea.tiempo_restante,
                    "ocupada":  tarea.ocupada,
                    "prod_id":  tarea.producto_actual.id if tarea.producto_actual else None,
                    "cola_ids": [p.id for p in tarea.cola_productos],
                })
            snap["procesos"].append(proc_snap)
        snap["completados"] = [p.id for p in productos_todos if p.estado == "completado"]
        snap["total"]       = len(productos_todos)
        return snap

    def _draw_simulation_snap(self, snap):
        """Dibuja la pantalla de procesos/tareas con scroll V+H."""
        s   = self.screen
        est = C.estado

        procesos_snap = snap["procesos"]
        n_proc        = len(procesos_snap)
        max_tasks     = max((len(p["tareas"]) for p in procesos_snap), default=1)

        MARGIN   = 20
        ARROW_W  = 30
        TASK_H   = 120
        HEADER_H = 38
        COL_TOP  = 80
        SB_H     = 10

        available_w  = C.WIDTH - MARGIN * 2 - ARROW_W * max(n_proc - 1, 0)
        PROC_W       = max(180, available_w // max(n_proc, 1))

        visible_w = C.WIDTH
        visible_h = C.HEIGHT - COL_TOP - 65 - SB_H
        content_w = MARGIN * 2 + n_proc * PROC_W + max(n_proc - 1, 0) * ARROW_W
        content_h = HEADER_H + 8 + max_tasks * (TASK_H + 8)

        max_scroll_x = max(0, content_w - visible_w)
        max_scroll_y = max(0, content_h - visible_h)
        est["sim_scroll_x"] = max(-max_scroll_x, min(0, est["sim_scroll_x"]))
        est["sim_scroll_y"] = max(-max_scroll_y, min(0, est["sim_scroll_y"]))

        s.set_clip(pygame.Rect(0, COL_TOP, C.WIDTH, visible_h))

        for proc_idx, proc_snap in enumerate(procesos_snap):
            accent  = C.PROCESS_COLORS[proc_idx % len(C.PROCESS_COLORS)]
            px      = MARGIN + proc_idx * (PROC_W + ARROW_W)
            base_y  = COL_TOP  + est["sim_scroll_y"]
            real_px = px       + est["sim_scroll_x"]

            # Cabecera proceso
            header_rect = pygame.Rect(real_px, base_y, PROC_W, HEADER_H)
            draw_rounded_rect(s, accent, header_rect, 10)
            type_tag = " [I]" if proc_snap["es_inicial"] else (" [F]" if proc_snap["es_final"] else "")
            render_text_centered(s, C.SMALL_FONT,
                                 clip_text(C.SMALL_FONT, proc_snap["nombre"] + type_tag, PROC_W - 16),
                                 C.WHITE, header_rect)

            # Tarjetas de tarea
            for t_idx, tsnap in enumerate(proc_snap["tareas"]):
                ty   = base_y + HEADER_H + 8 + t_idx * (TASK_H + 8)
                card = pygame.Rect(real_px, ty, PROC_W, TASK_H)

                card_bg  = (255, 247, 247) if tsnap["ocupada"] else C.WHITE
                bord_col = accent if tsnap["ocupada"] else C.LIGHT
                draw_rounded_rect(s, card_bg, card, 10, 2, bord_col)

                s.blit(C.HEAD_FONT.render(clip_text(C.HEAD_FONT, tsnap["nombre"], PROC_W - 20), True, C.BLACK),
                       (real_px + 10, ty + 8))
                s.blit(C.TINY_FONT.render(f"Ciclos: {tsnap['tiempo']}", True, C.GRAY),
                       (real_px + 10, ty + 30))

                # Slot producto actual
                slot_size = 44
                slot_x    = real_px + PROC_W - slot_size - 10
                slot_y    = ty + 10
                slot_rect = pygame.Rect(slot_x, slot_y, slot_size, slot_size)
                slot_bg   = (220, 230, 255) if tsnap["ocupada"] else (230, 235, 245)
                draw_rounded_rect(s, slot_bg, slot_rect, 8, 2,
                                  accent if tsnap["ocupada"] else (190, 200, 215))
                if tsnap["prod_id"] is not None:
                    pcol = C.PRODUCT_COLORS.get((tsnap["prod_id"] - 1) % 199 + 1, C.BLUE)
                    pygame.draw.circle(s, pcol, slot_rect.center, 18)
                    pid_s = C.SMALL_FONT.render(str(tsnap["prod_id"]), True, C.WHITE)
                    s.blit(pid_s, pid_s.get_rect(center=slot_rect.center))
                else:
                    es = C.TINY_FONT.render("libre", True, (190, 200, 215))
                    s.blit(es, es.get_rect(center=slot_rect.center))

                # Barra de progreso
                bar_y  = slot_y + slot_size + 4
                bar_bg = pygame.Rect(slot_x, bar_y, slot_size, 6)
                draw_rounded_rect(s, (210, 215, 225), bar_bg, 3)
                if tsnap["ocupada"] and tsnap["tiempo"] > 0:
                    pct = 1.0 - tsnap["restante"] / tsnap["tiempo"]
                    fw  = max(4, int(slot_size * pct))
                    draw_rounded_rect(s, accent, pygame.Rect(slot_x, bar_y, fw, 6), 3)

                # Cola de espera
                cola_ids     = tsnap["cola_ids"]
                cola_label_y = ty + 48
                s.blit(C.TINY_FONT.render("Cola:", True, C.GRAY), (real_px + 10, cola_label_y))
                avail_w  = slot_x - real_px - 16
                r_c      = 11
                gap      = 4
                max_show = max(1, avail_w // (r_c * 2 + gap))
                for ci, cid in enumerate(cola_ids[:max_show]):
                    pcol = C.PRODUCT_COLORS.get((cid - 1) % 199 + 1, C.BLUE)
                    cx_c = real_px + 10 + ci * (r_c * 2 + gap) + r_c
                    cy_c = cola_label_y + 18
                    pygame.draw.circle(s, pcol, (cx_c, cy_c), r_c)
                    ns = C.TINY_FONT.render(str(cid), True, C.WHITE)
                    s.blit(ns, ns.get_rect(center=(cx_c, cy_c)))
                if len(cola_ids) > max_show:
                    ex_x = real_px + 10 + max_show * (r_c * 2 + gap)
                    s.blit(C.TINY_FONT.render(f"+{len(cola_ids) - max_show}", True, C.GRAY),
                           (ex_x, cola_label_y + 10))

                if tsnap["ocupada"]:
                    rs = C.TINY_FONT.render(f"Restante: {tsnap['restante']}", True, C.ORANGE)
                    s.blit(rs, (real_px + 10, ty + TASK_H - 18))

        s.set_clip(None)

        # Scrollbars
        if max_scroll_y > 0:
            vx  = C.WIDTH - 10
            vth = max(30, int(visible_h * visible_h / content_h))
            vpy = COL_TOP + int((-est["sim_scroll_y"]) / max_scroll_y * (visible_h - vth))
            pygame.draw.rect(s, C.LIGHT, pygame.Rect(vx, COL_TOP, 6, visible_h), border_radius=3)
            pygame.draw.rect(s, C.BLUE,  pygame.Rect(vx, vpy,     6, vth),       border_radius=3)

        if max_scroll_x > 0:
            hbar_y = COL_TOP + visible_h
            hth    = max(40, int(visible_w * visible_w / content_w))
            hpx    = int((-est["sim_scroll_x"]) / max_scroll_x * (visible_w - hth))
            pygame.draw.rect(s, C.LIGHT, pygame.Rect(0,   hbar_y, visible_w, SB_H), border_radius=3)
            pygame.draw.rect(s, C.BLUE,  pygame.Rect(hpx, hbar_y, hth,       SB_H), border_radius=3)
            if est["sim_scroll_x"] == 0:
                hint = C.TINY_FONT.render("Shift + rueda para ver más procesos →", True, C.GRAY)
                s.blit(hint, hint.get_rect(centerx=C.WIDTH // 2, y=hbar_y - 1))

        # Barra inferior de completados
        completados = snap["completados"]
        total       = snap["total"]
        done_s = C.SMALL_FONT.render(f"Completados: {len(completados)} / {total}",
                                     True, C.GREEN if completados else C.GRAY)
        s.blit(done_s, (MARGIN, C.HEIGHT - 54))
        for ci, cid in enumerate(completados[:20]):
            pcol = C.PRODUCT_COLORS.get((cid - 1) % 199 + 1, C.BLUE)
            bx   = MARGIN + done_s.get_width() + 14 + ci * 26
            if bx + 22 < C.WIDTH - 580:
                pygame.draw.circle(s, pcol, (bx + 10, C.HEIGHT - 40), 11)
                ns = C.TINY_FONT.render(str(cid), True, C.WHITE)
                s.blit(ns, ns.get_rect(center=(bx + 10, C.HEIGHT - 40)))

    # Reporte

    def draw_report(self):
        """Retorna: (back_btn, reconf_btn, reinit_btn)"""
        s   = self.screen
        est = C.estado
        s.fill(C.BG)
        draw_header(s, "Reporte Final", "Estadísticas de la simulación completada")

        if not est["simulador"]:
            s.blit(C.TEXT_FONT.render("Sin datos de simulación.", True, C.RED), (60, 90))
        else:
            linea    = est["simulador"]._Simulador__linea
            productos = est["simulador"]._Simulador__productos
            self._draw_report_content(linea, productos)

        back_btn   = Button(40,  C.HEIGHT - 60, 170, 44, "Menú",          C.GRAY,   radius=10, font=C.TEXT_FONT)
        reconf_btn = Button(220, C.HEIGHT - 60, 200, 44, "Reconfigurar",  C.BLUE,   radius=10, font=C.TEXT_FONT)
        reinit_btn = Button(430, C.HEIGHT - 60, 200, 44, "Reiniciar sim.", C.TEAL,  radius=10, font=C.TEXT_FONT)
        back_btn.draw(s)
        reconf_btn.draw(s)
        reinit_btn.draw(s)
        return back_btn, reconf_btn, reinit_btn

    def _draw_report_content(self, linea, productos):
        s = self.screen
        from Reporte import Reporte
        rep = Reporte()
        rep.generar(linea, productos)

        COL1_X = 60
        COL2_X = C.WIDTH // 2 + 30
        CARD_W  = C.WIDTH // 2 - 80
        y1 = y2 = 90

        def stat_card(x, y, label, value, color=C.BLUE):
            r = pygame.Rect(x, y, CARD_W, 56)
            draw_rounded_rect(s, C.WHITE, r, 10)
            pygame.draw.rect(s, color, pygame.Rect(x, y, 5, 56), border_radius=10)
            s.blit(C.SMALL_FONT.render(label,      True, C.GRAY),  (x + 18, y + 8))
            s.blit(C.HEAD_FONT.render(str(value),  True, C.BLACK), (x + 18, y + 28))
            return y + 64

        y1 = stat_card(COL1_X, y1, "Tiempo primer producto en salir",
                       f"{rep._Reporte__tiempoPrimerProducto} ciclos", C.BLUE)
        y1 = stat_card(COL1_X, y1, "Tiempo último producto en salir",
                       f"{rep._Reporte__tiempoUltimoProducto} ciclos", C.BLUE)
        y1 = stat_card(COL1_X, y1, "Tiempo total de la simulación",
                       f"{rep._Reporte__tiempoTotalProcesamiento} ciclos", C.TEAL)
        y1 = stat_card(COL1_X, y1, "Promedio de espera por producto",
                       f"{rep._Reporte__promedioEsperaProducto:.2f} ciclos", C.TEAL)
        comp = [p for p in productos if p.estado == "completado"]
        y1 = stat_card(COL1_X, y1, "Productos completados",
                       f"{len(comp)} / {len(productos)}", C.GREEN)

        if rep._Reporte__cuelloBotella:
            proc = rep._Reporte__cuelloBotella
            y2 = stat_card(COL2_X, y2, "Cuello de Botella (proceso)",
                           f"{proc.nombre}  (ID {proc.id})", C.RED)
        if rep._Reporte__procesoMayorEspera:
            proc = rep._Reporte__procesoMayorEspera
            y2 = stat_card(COL2_X, y2, "Proceso con mayor espera",
                           f"{proc.nombre}  (ID {proc.id})", C.ORANGE)
        if rep._Reporte__tareaMayorEspera:
            tarea = rep._Reporte__tareaMayorEspera
            y2 = stat_card(COL2_X, y2, "Tarea con mayor espera",
                           f"{tarea.nombre}  (ID {tarea.id})", C.ORANGE)

        # Tabla por producto
        table_y = max(y1, y2) + 20
        if table_y < C.HEIGHT - 120:
            s.blit(C.HEAD_FONT.render("Detalle por Producto", True, C.BLACK), (COL1_X, table_y))
            table_y += 30
            cols  = ["ID", "Ingreso", "Salida", "Total", "Estado"]
            col_x = [COL1_X, COL1_X + 80, COL1_X + 160, COL1_X + 240, COL1_X + 330]
            for i, col in enumerate(cols):
                s.blit(C.SMALL_FONT.render(col, True, C.GRAY), (col_x[i], table_y))
            table_y += 22
            pygame.draw.line(s, C.LIGHT, (COL1_X, table_y), (COL1_X + 500, table_y), 1)
            table_y += 4
            for p in productos[:10]:
                total = p.obtener_tiempo_total()
                row   = [str(p.id),
                         str(p.tiempo_ingreso) if p.tiempo_ingreso is not None else "-",
                         str(p.tiempo_salida)  if p.tiempo_salida  is not None else "-",
                         str(total)            if total             is not None else "-",
                         p.estado]
                rc = C.GREEN if p.estado == "completado" else C.ORANGE
                for i, val in enumerate(row):
                    s.blit(C.TINY_FONT.render(val, True, rc if i == 4 else C.BLACK),
                           (col_x[i], table_y))
                table_y += 18
            if len(productos) > 10:
                s.blit(C.TINY_FONT.render(f"… y {len(productos)-10} más", True, C.GRAY),
                       (COL1_X, table_y))