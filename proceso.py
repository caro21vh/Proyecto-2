from Tarea import Tarea


class Proceso:
    """
    Agrupa una secuencia ordenada de tareas dentro de la línea de producción.
    Conoce su proceso anterior para armar la cadena.
    Puede marcarse como proceso inicial o final.
    """

    def __init__(self, id: int, nombre: str, es_inicial: bool = False, es_final: bool = False):
        self.__id = id
        self.__nombre = nombre
        self.__tareas: list[Tarea] = []
        self.__proceso_anterior: "Proceso | None" = None
        self.__es_inicial = es_inicial
        self.__es_final = es_final

    @property
    def nombre(self): return self.__nombre

    @property
    def es_inicial(self): return self.__es_inicial

    @property
    def tareas(self): return self.__tareas

    @property
    def id(self): return self.__id

    # ------------------------------------------------------------------
    # Métodos del diagrama UML
    # ------------------------------------------------------------------

    def agregar_tarea(self, tarea: Tarea) -> None:
        """Añade una tarea al final de la secuencia del proceso."""
        self.__tareas.append(tarea)

    def obtener_estado(self) -> str:
        """Descripción completa del proceso y todas sus tareas."""
        tipo = ""
        if self.__es_inicial:
            tipo = " [INICIAL]"
        elif self.__es_final:
            tipo = " [FINAL]"

        lineas = [f"Proceso [{self.__id}] {self.__nombre}{tipo}"]
        if not self.__tareas:
            lineas.append("  (sin tareas)")
        else:
            for tarea in self.__tareas:
                lineas.append(tarea.obtener_estado())
        return "\n".join(lineas)

    def vincular_anterior(self, proceso: "Proceso") -> None:
        """Vincula este proceso con el que le precede en la línea."""
        self.__proceso_anterior = proceso

    # ------------------------------------------------------------------
    # Lógica de simulación
    # ------------------------------------------------------------------

    def recibir_producto(self, producto) -> None:
        """Entrega el producto a la primera tarea del proceso."""
        if not self.__tareas:
            raise ValueError(f"El proceso '{self.__nombre}' no tiene tareas configuradas.")
        producto.proceso_actual = self
        self.__tareas[0].ejecutar(producto)

    def avanzar_ciclo(self) -> list:
        """
        Avanza un ciclo en todas las tareas del proceso.
        Retorna los productos que terminaron la última tarea (salen del proceso).
        """
        productos_terminados = []

        for i, tarea in enumerate(self.__tareas):
            producto_listo = tarea.avanzar_ciclo()

            if producto_listo is not None:
                es_ultima_tarea = (i == len(self.__tareas) - 1)
                if es_ultima_tarea:
                    producto_listo.tarea_actual = None
                    productos_terminados.append(producto_listo)
                else:
                    producto_listo.tarea_actual = self.__tareas[i + 1]
                    self.__tareas[i + 1].ejecutar(producto_listo)

        return productos_terminados

    def hay_trabajo_pendiente(self) -> bool:
        """True si alguna tarea está ocupada o tiene productos en cola."""
        return any(t.ocupada or len(t.cola_productos) > 0 for t in self.__tareas)

    def conteo_productos_en_espera(self) -> int:
        """Total de productos esperando en las colas de este proceso."""
        return sum(len(t.cola_productos) for t in self.__tareas)

    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"Proceso(id={self.__id}, nombre='{self.__nombre}', "
            f"tareas={len(self.__tareas)}, inicial={self.__es_inicial}, final={self.__es_final})"
        )
