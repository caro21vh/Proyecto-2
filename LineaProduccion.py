from Proceso import Proceso, Tarea


class LineaProduccion:
    """
    Orquesta la cadena completa de procesos.
    Compone uno o más objetos Proceso en secuencia.
    Delega el avance de ciclos a cada proceso.
    """

    def __init__(self):
        self.__procesos: list[Proceso] = []
        self.__tiempo_actual: int = 0

    @property
    def procesos(self):
        return self.__procesos

    @property
    def tiempo_actual(self):
        return self.__tiempo_actual

    # ------------------------------------------------------------------
    # Construcción de la línea
    # ------------------------------------------------------------------

    def agregar_proceso(self, proceso: Proceso) -> None:
        """
        Añade un proceso al final de la línea y vincula automáticamente
        el proceso anterior.
        """
        if self.__procesos:
            proceso.vincular_anterior(self.__procesos[-1])
        self.__procesos.append(proceso)
        

    def _proceso_inicial(self) -> "Proceso | None":
        for p in self.__procesos:
            if p.es_inicial:
                return p
        return self.__procesos[0] if self.__procesos else None

    def _proceso_final(self) -> "Proceso | None":
        for p in self.__procesos:
            if p.es_final:
                return p
        return self.__procesos[-1] if self.__procesos else None

    # ------------------------------------------------------------------
    # Métodos del diagrama UML
    # ------------------------------------------------------------------

    def iniciar_simulacion(self, productos: list) -> None:
        """Inyecta los productos en el proceso inicial y arranca el reloj."""
        inicio = self._proceso_inicial()
        if inicio is None:
            raise ValueError("La línea no tiene procesos configurados.")

        self.__tiempo_actual = 0

        for producto in productos:
            producto.registrar_ingreso(self.__tiempo_actual)
            inicio.recibir_producto(producto)

        print(f"▶  Simulación iniciada con {len(productos)} producto(s).")

    def pausar(self) -> None:
        """Imprime el estado completo de la línea en el ciclo actual."""
        print(self.mostrar_estado())

    def avanzar_ciclo(self) -> list:
        """
        Avanza UN ciclo en toda la línea.
        Para evitar que un producto cruce varios procesos en un mismo
        ciclo, primero se recolectan todos los productos que terminan
        cada proceso y LUEGO se transfieren al siguiente proceso.
        Retorna los productos que completaron la línea entera.
        """
        self.__tiempo_actual += 1
        productos_completados = []

        # 1. Avanzar todos los procesos de atrás hacia adelante para
        #    evitar que una transferencia inmediata haga avanzar un
        #    producto dos veces en el mismo ciclo.
        transferencias = []   # (producto, índice_proceso_destino)

        for i in range(len(self.__procesos) - 1, -1, -1):
            proceso = self.__procesos[i]
            terminados_en_proceso = proceso.avanzar_ciclo()

            for producto in terminados_en_proceso:
                es_ultimo_proceso = (i == len(self.__procesos) - 1)
                if es_ultimo_proceso:
                    producto.registrar_salida(self.__tiempo_actual)
                    producto.cambiar_estado("completado")
                    productos_completados.append(producto)
                else:
                    transferencias.append((producto, i + 1))

        # 2. Ahora sí: entregar los productos al siguiente proceso
        #    (ya no se van a procesar en este ciclo porque el bucle terminó)
        for producto, idx_destino in transferencias:
            siguiente_proceso = self.__procesos[idx_destino]
            producto.proceso_actual = siguiente_proceso
            siguiente_proceso.recibir_producto(producto)

        return productos_completados

    def generar_reporte(self):
        """Retorna un objeto Reporte con las estadísticas de la simulación."""
        from Reporte import Reporte
        return Reporte(self)

    # ------------------------------------------------------------------
    # Estado / diagnóstico
    # ------------------------------------------------------------------

    def mostrar_estado(self) -> str:
        separador = "=" * 60
        lineas = [
            separador,
            f"  LÍNEA DE PRODUCCIÓN  |  Ciclo: {self.__tiempo_actual}",
            separador,
        ]
        for proceso in self.__procesos:
            lineas.append(proceso.obtener_estado())
            lineas.append("-" * 40)
        return "\n".join(lineas)

    def hay_trabajo_pendiente(self) -> bool:
        return any(p.hay_trabajo_pendiente() for p in self.__procesos)

    def __repr__(self) -> str:
        return (
            f"LineaProduccion(procesos={len(self.__procesos)}, "
            f"ciclo={self.__tiempo_actual})"
        )
