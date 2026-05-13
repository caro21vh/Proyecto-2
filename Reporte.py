class Reporte:
    def __init__(self):
        self.__tiempoPrimerProducto: int = 0
        self.__tiempoUltimoProducto: int = 0
        self.__tiempoTotalProcesamiento: int = 0
        self.__cuelloBotella = None  # Tipo: Proceso
        self.__promedioEsperaProducto: int = 0
        self.__procesoMayorEspera = None  # Tipo: Proceso
        self.__tareaMayorEspera = None  # Tipo: Tarea

    def generar(self) -> None:
        pass

    def imprimir(self) -> None:
        pass
