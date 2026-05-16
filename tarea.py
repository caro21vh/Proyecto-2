from Producto import Producto

class Tarea:
    """
    Representa una tarea o máquina dentro de un proceso.
    Cada tarea procesa un producto a la vez y mantiene una cola FIFO.
    """

    def __init__(self, id, nombre, tiempo_procesamiento):
        self.__id = id
        self.__nombre = nombre
        self.__tiempo_procesamiento = tiempo_procesamiento
        self.__ocupada = False
        self.__cola_productos = []

        self.__producto_actual = None
        self.__tiempo_restante = 0

    @property
    def id(self): return self.__id

    @property
    def nombre(self): return self.__nombre
    
    @property
    def tiempo_procesamiento(self): return self.__tiempo_procesamiento

    @property
    def ocupada(self): return self.__ocupada

    @property
    def cola_productos(self): return self.__cola_productos

    @property
    def tiempo_restante(self): return self.__tiempo_restante

    @property
    def producto_actual(self): return self.__producto_actual

    def ejecutar(self, producto):
        """
        Recibe un producto.
        Si la tarea está libre, inicia el procesamiento.
        Si está ocupada, el producto queda en cola FIFO.
        """
        if self.__ocupada:
            self.__cola_productos.append(producto)
            producto.cambiar_estado("En espera")
        else:
            self.__producto_actual = producto
            self.__tiempo_restante = self.__tiempo_procesamiento
            self.__ocupada = True

            producto.tarea_actual = self
            producto.cambiar_estado("En proceso")

    def avanzar_ciclo(self):
        """
        Avanza un ciclo de tiempo.
        Si termina el producto actual, lo retorna.
        Si hay productos en cola, toma el siguiente automáticamente.
        """
        if not self.__ocupada:
            return None

        self.__tiempo_restante -= 1

        if self.__tiempo_restante > 0:
            return None

        producto_terminado = self.__producto_actual
        producto_terminado.cambiar_estado("Tarea finalizada")

        if self.__cola_productos:
            siguiente_producto = self.__cola_productos.pop(0)
            self.__producto_actual = siguiente_producto
            self.__tiempo_restante = self.__tiempo_procesamiento
            self.__ocupada = True

            siguiente_producto.tarea_actual = self
            siguiente_producto.cambiar_estado("En proceso")
        else:
            self.__producto_actual = None
            self.__tiempo_restante = 0
            self.__ocupada = False

        return producto_terminado

    def obtener_estado(self):
        estado = f"  Tarea [{self.__id}] {self.__nombre}"

        if self.__ocupada:
            estado += (
                f" | Ocupada: Sí"
                f" | Producto actual: {self.__producto_actual.id}"
                f" | Tiempo restante: {self.__tiempo_restante}"
            )
        else:
            estado += " | Ocupada: No"

        estado += f" | En cola: {len(self.__cola_productos)}"

        return estado

    def esta_disponible(self):
        return not self.__ocupada

    def __repr__(self):
        return (
            f"Tarea(id={self.__id}, nombre='{self.__nombre}', "
            f"tiempo_procesamiento={self.__tiempo_procesamiento}, "
            f"ocupada={self.__ocupada}, cola={len(self.__cola_productos)})"
        )