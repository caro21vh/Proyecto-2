from Producto import Producto
from LineaProduccion import LineaProduccion
import copy

class Simulador:
    def __init__(self):
        self.__linea: 'LineaProduccion | None' = None
        self.__productos: list[Producto] = []
        self.__contadorPEE: int = 0
        self.__reporte = None
        
        # Para la opción reiniciar, guardamos la configuración original
        self.__procesos_originales = []
        self.__productos_originales = []

    @property
    def linea(self):
        return self.__linea

    @property
    def productos(self):
        return self.__productos

    def configurar(self, procesos: list, productos: list) -> None:
        self.__procesos_originales = copy.deepcopy(procesos)
        self.__productos_originales = copy.deepcopy(productos)
        
        self.__linea = LineaProduccion()
        for p in procesos:
            self.__linea.agregar_proceso(p)
        self.__productos = productos

    def ejecutar(self) -> None:
        if self.__linea is None:
            print("❌ Debes configurar el simulador primero.")
            return
        
        self.__linea.iniciar_simulacion(self.__productos)
        print("Empezando ejecución...\n")
        print(self.__linea.mostrar_estado())
        
        while self.__linea.hay_trabajo_pendiente():
            input("\n[Presiona ENTER para avanzar al siguiente ciclo]")
            self.__linea.avanzar_ciclo()
            print(self.__linea.mostrar_estado())
            
        print("\n✔ Simulación completada.")

    def reiniciar(self) -> None:
        if not self.__procesos_originales:
            print("❌ No hay una configuración previa para reiniciar.")
            return
            
        print("↻ Reiniciando la última configuración de la simulación...")
        # Vuelve a crear la línea con copias limpias de los procesos y productos originales
        # esto borra la instancia usada (y su estado modificado)
        self.configurar(copy.deepcopy(self.__procesos_originales), copy.deepcopy(self.__productos_originales))
        print("✔ Simulación reiniciada correctamente y lista para ser ejecutada nuevamente.")

    def mostrarEstado(self) -> str:
        if self.__linea is None:
            return "El simulador no está configurado."
        return self.__linea.mostrar_estado()

