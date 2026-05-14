from Simulador import Simulador
from Producto import Producto
from Proceso import Proceso
from Tarea import Tarea

def menu_configurar(simulador: Simulador):
    print("\n--- CONFIGURACIÓN DE LA LÍNEA DE PRODUCCIÓN ---")
    
    # 1. Pedir Productos
    while True:
        try:
            cant_productos = int(input("Ingrese la cantidad de productos a simular: "))
            if cant_productos > 0:
                break
            print("La cantidad debe ser mayor a cero.")
        except ValueError:
            print("Por favor, ingrese un número válido.")
            
    productos = [Producto(i + 1) for i in range(cant_productos)]
    
    # 2. Pedir Procesos y Tareas
    procesos = []
    id_proceso_global = 1
    id_tarea_global = 1
    
    agregando_procesos = True
    while agregando_procesos:
        print(f"\n> Configurando Proceso {id_proceso_global}:")
        nombre_proceso = input("  Nombre del proceso: ")
        
        es_inicial = False
        es_final = False
        tipo = input("  ¿Es inicial (I), final (F), o ninguno (N)?: ").strip().upper()
        if tipo == 'I':
            es_inicial = True
        elif tipo == 'F':
            es_final = True
            
        nuevo_proceso = Proceso(id_proceso_global, nombre_proceso, es_inicial, es_final)
        
        agregando_tareas = True
        while agregando_tareas:
            print(f"\n  >> Configurando Tarea {id_tarea_global} para el proceso '{nombre_proceso}':")
            nombre_tarea = input("     Nombre de la tarea: ")
            
            while True:
                try:
                    tiempo_proc = int(input("     Tiempo de procesamiento (ciclos): "))
                    if tiempo_proc > 0:
                        break
                    print("     El tiempo debe ser mayor a cero.")
                except ValueError:
                    print("     Por favor, ingrese un número válido.")
            
            nueva_tarea = Tarea(id_tarea_global, nombre_tarea, tiempo_proc)
            nuevo_proceso.agregar_tarea(nueva_tarea)
            id_tarea_global += 1
            
            resp_tarea = input("\n     ¿Quiere agregar otra tarea a este proceso? (S/N): ").strip().upper()
            agregando_tareas = (resp_tarea == 'S')
            
        procesos.append(nuevo_proceso)
        id_proceso_global += 1
        
        resp_proceso = input("\n¿Quiere agregar otro proceso a la línea? (S/N): ").strip().upper()
        agregando_procesos = (resp_proceso == 'S')
    
    # 3. Guardar en el Simulador
    simulador.configurar(procesos, productos)
    print("\n✔ ¡Simulador configurado exitosamente!")


def main():
    simulador = Simulador()
    
    while True:
        print("\n===============================")
        print("      S I M U L A D O R        ")
        print("===============================")
        print("1. Configurar")
        print("2. Ejecutar")
        print("3. Reiniciar")
        print("4. Salir")
        print("===============================")
        
        opcion = input("Elige una opción: ").strip()
        
        if opcion == "1":
            menu_configurar(simulador)
        elif opcion == "2":
            simulador.ejecutar()
        elif opcion == "3":
            simulador.reiniciar()
        elif opcion == "4":
            print("Saliendo del simulador...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
