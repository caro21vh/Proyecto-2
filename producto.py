

class Producto:
    """
    Representa un producto que avanza por la línea de producción.
    """

    def __init__(self, id):
        self.__id = id
        self.__estado = "Pendiente"

        self.__tiempo_ingreso = None
        self.__tiempo_salida = None

        self.__proceso_actual = None
        self.__tarea_actual = None

    @property
    def id(self):
        return self.__id

    @property
    def estado(self):
        return self.__estado

    @property
    def proceso_actual(self):
        return self.__proceso_actual

    @proceso_actual.setter
    def proceso_actual(self, proceso):
        self.__proceso_actual = proceso

    @property
    def tarea_actual(self):
        return self.__tarea_actual

    @tarea_actual.setter
    def tarea_actual(self, tarea):
        self.__tarea_actual = tarea

    def registrar_ingreso(self, tiempo):
        self.__tiempo_ingreso = tiempo
        self.__estado = "Ingresado"

    def registrar_salida(self, tiempo):
        self.__tiempo_salida = tiempo
        self.__estado = "Finalizado"

    def cambiar_estado(self, estado):
        self.__estado = estado

    def obtener_tiempo_total(self):
        if self.__tiempo_ingreso is None or self.__tiempo_salida is None:
            return None
        return self.__tiempo_salida - self.__tiempo_ingreso

    def __repr__(self):
        proceso = self.__proceso_actual.nombre if self.__proceso_actual else "Ninguno"
        tarea = self.__tarea_actual.nombre if self.__tarea_actual else "Ninguna"

        return (
            f"Producto(id={self.__id}, estado='{self.__estado}', "
            f"proceso_actual='{proceso}', tarea_actual='{tarea}')"
        )