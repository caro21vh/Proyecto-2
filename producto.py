

class Producto:
    """
    Representa un producto que avanza por la línea de producción.
    """

    def __init__(self, id):
        self.id = id
        self.estado = "Pendiente"

        self.tiempo_ingreso = None
        self.tiempo_salida = None

        self.proceso_actual = None
        self.tarea_actual = None

    def registrar_ingreso(self, tiempo):
        self.tiempo_ingreso = tiempo
        self.estado = "Ingresado"

    def registrar_salida(self, tiempo):
        self.tiempo_salida = tiempo
        self.estado = "Finalizado"

    def cambiar_estado(self, estado):
        self.estado = estado

    def obtener_tiempo_total(self):
        if self.tiempo_ingreso is None or self.tiempo_salida is None:
            return None
        return self.tiempo_salida - self.tiempo_ingreso

    def __repr__(self):
        proceso = self.proceso_actual.nombre if self.proceso_actual else "Ninguno"
        tarea = self.tarea_actual.nombre if self.tarea_actual else "Ninguna"

        return (
            f"Producto(id={self.id}, estado='{self.estado}', "
            f"proceso_actual='{proceso}', tarea_actual='{tarea}')"
        )