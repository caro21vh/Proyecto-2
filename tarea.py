from producto import Producto

class Tarea:
    """
    Representa una tarea o máquina dentro de un proceso.
    Cada tarea procesa un producto a la vez y mantiene una cola FIFO.
    """

    def __init__(self, id, nombre, tiempo_procesamiento):
        self.id = id
        self.nombre = nombre
        self.tiempo_procesamiento = tiempo_procesamiento
        self.ocupada = False
        self.cola_productos = []

        self.producto_actual = None
        self.tiempo_restante = 0

    def ejecutar(self, producto):
        """
        Recibe un producto.
        Si la tarea está libre, inicia el procesamiento.
        Si está ocupada, el producto queda en cola FIFO.
        """
        if self.ocupada:
            self.cola_productos.append(producto)
            producto.cambiar_estado("En espera")
        else:
            self.producto_actual = producto
            self.tiempo_restante = self.tiempo_procesamiento
            self.ocupada = True

            producto.tarea_actual = self
            producto.cambiar_estado("En proceso")

    def avanzar_ciclo(self):
        """
        Avanza un ciclo de tiempo.
        Si termina el producto actual, lo retorna.
        Si hay productos en cola, toma el siguiente automáticamente.
        """
        if not self.ocupada:
            return None

        self.tiempo_restante -= 1

        if self.tiempo_restante > 0:
            return None

        producto_terminado = self.producto_actual
        producto_terminado.cambiar_estado("Tarea finalizada")

        if self.cola_productos:
            siguiente_producto = self.cola_productos.pop(0)
            self.producto_actual = siguiente_producto
            self.tiempo_restante = self.tiempo_procesamiento
            self.ocupada = True

            siguiente_producto.tarea_actual = self
            siguiente_producto.cambiar_estado("En proceso")
        else:
            self.producto_actual = None
            self.tiempo_restante = 0
            self.ocupada = False

        return producto_terminado

    def obtener_estado(self):
        estado = f"  Tarea [{self.id}] {self.nombre}"

        if self.ocupada:
            estado += (
                f" | Ocupada: Sí"
                f" | Producto actual: {self.producto_actual.id}"
                f" | Tiempo restante: {self.tiempo_restante}"
            )
        else:
            estado += " | Ocupada: No"

        estado += f" | En cola: {len(self.cola_productos)}"

        return estado

    def esta_disponible(self):
        return not self.ocupada

    def __repr__(self):
        return (
            f"Tarea(id={self.id}, nombre='{self.nombre}', "
            f"tiempo_procesamiento={self.tiempo_procesamiento}, "
            f"ocupada={self.ocupada}, cola={len(self.cola_productos)})"
        )