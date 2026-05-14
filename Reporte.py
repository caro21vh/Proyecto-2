class Reporte:
    def __init__(self):
        self.__tiempoPrimerProducto: int = 0
        self.__tiempoUltimoProducto: int = 0
        self.__tiempoTotalProcesamiento: int = 0
        self.__cuelloBotella = None  # Tipo: Proceso
        self.__promedioEsperaProducto: float = 0.0
        self.__procesoMayorEspera = None  # Tipo: Proceso
        self.__tareaMayorEspera = None  # Tipo: Tarea

    def generar(self, linea, productos: list) -> None:
        if not productos or not linea.procesos:
            return

        productos_terminados = [p for p in productos if p.estado == "completado" or p.tiempo_salida is not None]
        
        if productos_terminados:
            self.__tiempoPrimerProducto = min(p.tiempo_salida for p in productos_terminados)
            self.__tiempoUltimoProducto = max(p.tiempo_salida for p in productos_terminados)
        else:
            self.__tiempoPrimerProducto = 0
            self.__tiempoUltimoProducto = 0

        self.__tiempoTotalProcesamiento = linea.tiempo_actual

        # Cálculo del cuello de botella (Proceso con mayor suma de tiempos de procesamiento de sus tareas)
        mayor_tiempo_proceso = -1
        for proceso in linea.procesos:
            tiempo_proc = sum(t.tiempo_procesamiento for t in proceso.tareas) 
            if tiempo_proc > mayor_tiempo_proceso:
                mayor_tiempo_proceso = tiempo_proc
                self.__cuelloBotella = proceso

        # Atributos de espera (cálculo básico en base al tiempo teórico vs real)
        tiempo_teorico_total = sum(t.tiempo_procesamiento for p in linea.procesos for t in p.tareas)
        espera_total = 0
        for p in productos_terminados:
            tiempo_real = p.tiempo_salida - p.tiempo_ingreso
            espera = tiempo_real - tiempo_teorico_total
            espera_total += espera if espera > 0 else 0
            
        self.__promedioEsperaProducto = espera_total / len(productos_terminados) if productos_terminados else 0.0
        
        # Como los productos no registran el tiempo de espera por cada proceso/tarea individualmente 
        # sin modificar drásticamente el modelo, asignaremos como mayor espera el cuello de botella
        self.__procesoMayorEspera = self.__cuelloBotella
        if self.__cuelloBotella and self.__cuelloBotella.tareas:
            self.__tareaMayorEspera = max(self.__cuelloBotella.tareas, key=lambda t: t.tiempo_procesamiento)

    def imprimir(self) -> None:
        print("\n" + "=" * 40)
        print("          REPORTE DE SIMULACIÓN ")
        print("=" * 40)
        print(f"Tiempo primer producto en salir: {self.__tiempoPrimerProducto} ciclos")
        print(f"Tiempo último producto en salir: {self.__tiempoUltimoProducto} ciclos")
        print(f"Tiempo total de simulación:      {self.__tiempoTotalProcesamiento} ciclos")
        print(f"Promedio de espera por producto: {self.__promedioEsperaProducto:.2f} ciclos")
        
        if self.__cuelloBotella:
            print(f"Proceso Cuello de Botella:       {self.__cuelloBotella.nombre} (ID: {self.__cuelloBotella.id})")
        if self.__procesoMayorEspera:
            print(f"Proceso con mayor espera:        {self.__procesoMayorEspera.nombre} (ID: {self.__procesoMayorEspera.id})")
        if self.__tareaMayorEspera:
            print(f"Tarea con mayor espera:          {self.__tareaMayorEspera.nombre} (ID: {self.__tareaMayorEspera.id})")
        print("=" * 40 + "\n")
