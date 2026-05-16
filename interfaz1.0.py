"""
Interfaz1_0.py — Loop principal y manejo de eventos.
Solo inicializa pygame, instancia Pantallas, y orquesta
el render y los eventos de cada escena.
Toda la lógica de negocio vive en las funciones de este archivo
(agregar_proceso, construir_simulador, etc.) y opera sobre C.estado.
"""
 
import pygame
import sys
 
import Constantes as C
from Constantes   import init_fonts, TIME_EVENT
from ComponentesUI import InputField
from Pantallas    import Pantallas
 
from Simulador import Simulador
from Producto  import Producto
from Proceso   import Proceso
from Tarea     import Tarea
 
 
# Lógica de programa (opera con respecto a C.estado)
 
def agregar_proceso():
    est = C.estado
    idx = len(est["procesos_config"])
    nuevo = {"nombre": f"Proceso {idx + 1}", "tareas": [],
             "es_inicial": idx == 0, "es_final": False}
    est["procesos_config"].append(nuevo)
    est["nombre_inputs"].append(InputField(0, 0, 200, 32, nuevo["nombre"]))
    est["tarea_inputs"].append([])
 
 
def agregar_tarea(proc_idx):
    est   = C.estado
    t_idx = len(est["procesos_config"][proc_idx]["tareas"])
    nueva = {"nombre": f"Tarea {t_idx + 1}", "tiempo": 1}
    est["procesos_config"][proc_idx]["tareas"].append(nueva)
    est["tarea_inputs"][proc_idx].append(
        InputField(0, 0, 120, 28, nueva["nombre"], max_len=20, font=C.SMALL_FONT)
    )
 
 
def eliminar_proceso(proc_idx):
    est = C.estado
    if len(est["procesos_config"]) <= 1:
        set_error("Debe haber al menos un proceso.")
        return
    est["procesos_config"].pop(proc_idx)
    est["nombre_inputs"].pop(proc_idx)
    est["tarea_inputs"].pop(proc_idx)
    if not any(p["es_inicial"] for p in est["procesos_config"]):
        est["procesos_config"][0]["es_inicial"] = True
    if not any(p["es_final"] for p in est["procesos_config"]):
        est["procesos_config"][-1]["es_final"] = True
 
 
def eliminar_tarea(proc_idx, tarea_idx):
    est = C.estado
    est["procesos_config"][proc_idx]["tareas"].pop(tarea_idx)
    est["tarea_inputs"][proc_idx].pop(tarea_idx)
 
 
def set_error(msg):
    C.estado["error_msg"]   = msg
    C.estado["error_timer"] = 180
 
 
def sync_names():
    est = C.estado
    for i, proc in enumerate(est["procesos_config"]):
        if i < len(est["nombre_inputs"]) and est["nombre_inputs"][i].value.strip():
            proc["nombre"] = est["nombre_inputs"][i].value.strip()
        for j, tarea in enumerate(proc["tareas"]):
            if j < len(est["tarea_inputs"][i]) and est["tarea_inputs"][i][j].value.strip():
                tarea["nombre"] = est["tarea_inputs"][i][j].value.strip()
 
 
def validar_configuracion():
    sync_names()
    est   = C.estado
    procs = est["procesos_config"]
    if not procs:
        set_error("Debe haber al menos un proceso.")
        return False
    if sum(1 for p in procs if p["es_inicial"]) != 1:
        set_error("Debe marcarse exactamente UN proceso como inicial.")
        return False
    if sum(1 for p in procs if p["es_final"]) != 1:
        set_error("Debe marcarse exactamente UN proceso como final.")
        return False
    for proc in procs:
        if not proc["tareas"]:
            set_error(f"'{proc['nombre']}' no tiene tareas.")
            return False
    return True
 
 
def construir_simulador():
    sync_names()
    est    = C.estado
    id_p   = id_t = 1
    procs  = []
    for pc in est["procesos_config"]:
        p = Proceso(id_p, pc["nombre"], pc["es_inicial"], pc["es_final"])
        id_p += 1
        for tc in pc["tareas"]:
            p.agregar_tarea(Tarea(id_t, tc["nombre"], tc["tiempo"]))
            id_t += 1
        procs.append(p)
 
    prods = [Producto(i + 1) for i in range(est["cantidad_productos"])]
    sim   = Simulador()
    sim.configurar(procs, prods)
    sim._Simulador__linea.iniciar_simulacion(sim._Simulador__productos)
 
    est["simulador"]          = sim
    est["simulation_running"] = True
    est["simulacion_pausada"] = False
    est["simulation_done"]    = False
    est["sim_scroll_y"]       = 0
    est["sim_scroll_x"]       = 0
    est["pasos_pendientes"].clear()
 
    # Snapshot inicial
    from Pantallas import Pantallas as _P
    snap0 = _P(None)._capturar_snapshot(sim._Simulador__linea, sim._Simulador__productos)
    est["pasos_pendientes"].append(snap0)
 
 
# Loop principal
 
def main():
    pygame.init()
    screen = pygame.display.set_mode((C.WIDTH, C.HEIGHT))
    pygame.display.set_caption("LinProd - Simulador de Producción")
    clock = pygame.time.Clock()
    init_fonts()
 
    pantallas = Pantallas(screen)
 
    # Proceso por defecto
    if not C.estado["procesos_config"]:
        agregar_proceso()
        agregar_tarea(0)
 
    pygame.time.set_timer(TIME_EVENT, 800)
    running = True
 
    while running:
        est   = C.estado
        scene = est["scene"]
 
        # Render
        start_btn    = add_proc = start_sim = None
        back_btn     = minus_btn = plus_btn = None
        check_rects  = proc_buttons = time_buttons = []
        pause_btn    = report_btn = reconf_btn = None
        report_back  = report_rec = report_rei = None
 
        if scene == "menu":
            start_btn = pantallas.draw_menu()
        elif scene == "config":
            (add_proc, start_sim, back_btn, minus_btn, plus_btn,
             check_rects, proc_buttons, time_buttons) = pantallas.draw_configuration()
        elif scene == "simulation":
            pause_btn, report_btn, reconf_btn = pantallas.draw_simulation()
        elif scene == "report":
            report_back, report_rec, report_rei = pantallas.draw_report()
 
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
 
            # Auto-avance de ciclo
            if event.type == TIME_EVENT and scene == "simulation":
                if not est["simulacion_pausada"] and est["simulador"] and not est["simulation_done"]:
                    if est["pasos_pendientes"]:
                        est["pasos_pendientes"].pop(0)
                    if not est["pasos_pendientes"]:
                        linea = est["simulador"]._Simulador__linea
                        if linea.hay_trabajo_pendiente():
                            linea.avanzar_ciclo()
                            snap = pantallas._capturar_snapshot(linea, est["simulador"]._Simulador__productos)
                            est["pasos_pendientes"].append(snap)
                        else:
                            est["simulation_done"] = True
 
            # Scroll config
            if scene == "config" and event.type == pygame.MOUSEWHEEL:
                est["scroll_y"] += event.y * est["SCROLL_SPEED"]
                total_h = len(est["procesos_config"]) * 310
                est["scroll_y"] = max(-(total_h - 400), min(0, est["scroll_y"]))
 
            # Scroll simulación (V normal, H con Shift)
            if scene == "simulation" and event.type == pygame.MOUSEWHEEL:
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    est["sim_scroll_x"] += event.y * est["SCROLL_SPEED"]
                else:
                    est["sim_scroll_y"] += event.y * est["SCROLL_SPEED"]
 
            # Inputs de texto (solo en config)
            if scene == "config":
                for fi in est["nombre_inputs"]:
                    fi.handle_event(event)
                for ti_list in est["tarea_inputs"]:
                    for ti in ti_list:
                        ti.handle_event(event)
 
            # Menú
            if scene == "menu":
                if start_btn and start_btn.clicked(event):
                    est["scene"] = "config"
 
            # Config
            elif scene == "config":
                if minus_btn and minus_btn.clicked(event) and est["cantidad_productos"] > 1:
                    est["cantidad_productos"] -= 1
                if plus_btn and plus_btn.clicked(event):
                    est["cantidad_productos"] += 1
                if add_proc and add_proc.clicked(event):
                    agregar_proceso()
                if back_btn and back_btn.clicked(event):
                    est["scene"] = "menu"
                if start_sim and start_sim.clicked(event):
                    if validar_configuracion():
                        construir_simulador()
                        est["scene"] = "simulation"
 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Checkboxes Inicial / Final
                    for init_r, fin_r, pi in check_rects:
                        procs = est["procesos_config"]
                        if init_r.collidepoint(event.pos) and not procs[pi]["es_inicial"]:
                            for p in procs: p["es_inicial"] = False
                            procs[pi]["es_inicial"] = True
                            procs[pi]["es_final"]   = False
                        if fin_r.collidepoint(event.pos) and not procs[pi]["es_final"]:
                            for p in procs: p["es_final"] = False
                            procs[pi]["es_final"]   = True
                            procs[pi]["es_inicial"] = False
 
                    # Botones agregar/eliminar proceso
                    for add_t, del_p, pi in proc_buttons:
                        if add_t.clicked(event):
                            agregar_tarea(pi)
                        if del_p.clicked(event):
                            eliminar_proceso(pi)
 
                # Botones tiempo y eliminar tarea
                for entry in time_buttons:
                    tm, tp, pi, ti, del_t = entry
                    tareas = est["procesos_config"][pi]["tareas"]
                    if tm.clicked(event) and tareas[ti]["tiempo"] > 1:
                        tareas[ti]["tiempo"] -= 1
                    if tp.clicked(event):
                        tareas[ti]["tiempo"] += 1
                    if del_t and del_t.clicked(event):
                        if len(tareas) > 1:
                            eliminar_tarea(pi, ti)
                        else:
                            set_error("Un proceso necesita al menos 1 tarea.")
 
            # Simulación
            elif scene == "simulation":
                if pause_btn and pause_btn.clicked(event):
                    est["simulacion_pausada"] = not est["simulacion_pausada"]
                    if est["simulacion_pausada"]:
                        linea = est["simulador"]._Simulador__linea
                        print("\n" + "=" * 60)
                        print(f"PAUSA EN CICLO {linea.tiempo_actual}")
                        print(linea.mostrar_estado())
                        print("=" * 60 + "\n")
                if report_btn and report_btn.clicked(event):
                    est["scene"] = "report"
                if reconf_btn and reconf_btn.clicked(event):
                    est["simulacion_pausada"] = False
                    est["scene"] = "config"
 
            # Reporte
            elif scene == "report":
                if report_back and report_back.clicked(event):
                    est["scene"] = "menu"
                if report_rec and report_rec.clicked(event):
                    est["simulacion_pausada"] = False
                    est["scene"] = "config"
                if report_rei and report_rei.clicked(event):
                    construir_simulador()
                    est["scene"] = "simulation"
 
        pygame.display.update()
        clock.tick(60)
 
    pygame.quit()
    sys.exit()
 
 
if __name__ == "__main__":
    main()