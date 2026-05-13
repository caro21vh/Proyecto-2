from typing import List

class Simulador:
    def __init__(self):
        self.__linea = None  # Tipo: LineaProduccion
        self.__productos: List = []  # Lista de objetos Producto
        self.__contadorPEE: int = 0 # Contador de Productos en Espera
        self.__reporte = None # Tipo: Reporte

    def configurar(self, procesos: List, productos: List) -> None:
        pass

    def ejecutar(self) -> None:
        pass

    def reiniciar(self) -> None:
        pass

    def mostrarEstado(self) -> str:
        return ""
