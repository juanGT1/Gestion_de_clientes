"""Clase Reserva: relaciona un cliente con un servicio y controla su estado."""

from enum import Enum

from entidades import Entidad
from excepciones import ReservaError, ServicioNoDisponibleError, ValidacionError
from registro import registrar_evento


class EstadoReserva(Enum):
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
    COMPLETADA = "Completada"


class Reserva(Entidad):
    """Representa una reserva y permite confirmarla, cancelarla o procesarla."""

    IMPUESTO_GENERAL = 0.19

    def __init__(self, cliente, servicio, duracion, **parametros):
        super().__init__()
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.parametros = parametros
        self.estado = EstadoReserva.PENDIENTE
        self.costo_final = None
        self.validar()

    def validar(self):
        if self.cliente is None or self.servicio is None:
            raise ValidacionError("La reserva debe tener un cliente y un servicio.")
        if not hasattr(self.cliente, "id") or not hasattr(self.servicio, "id"):
            raise ValidacionError("El cliente o el servicio no son objetos válidos.")
        self.servicio.validar_parametros(self.duracion, **self.parametros)

    def confirmar(self, descuento=0.0):
        """Confirma la reserva y calcula su costo con el impuesto general."""
        if self.estado is not EstadoReserva.PENDIENTE:
            raise ReservaError("Solo se pueden confirmar reservas pendientes.")
        if not self.servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self.servicio.nombre}' no está disponible."
            )
        self.validar()
        self.costo_final = self.servicio.calcular_costo(
            self.duracion,
            impuesto=self.IMPUESTO_GENERAL,
            descuento=descuento,
            **self.parametros,
        )
        self.estado = EstadoReserva.CONFIRMADA
        registrar_evento(f"Reserva {self.id} confirmada. Total: {self.costo_final}")
        return self.costo_final

    def cancelar(self):
        """Cancela una reserva pendiente o confirmada."""
        if self.estado not in (EstadoReserva.PENDIENTE, EstadoReserva.CONFIRMADA):
            raise ReservaError("La reserva no se puede cancelar en su estado actual.")
        self.estado = EstadoReserva.CANCELADA
        registrar_evento(f"Reserva {self.id} cancelada.")

    def procesar(self):
        """Marca como completada una reserva que ya fue confirmada."""
        if self.estado is not EstadoReserva.CONFIRMADA:
            raise ReservaError("Solo se pueden procesar reservas confirmadas.")
        self.estado = EstadoReserva.COMPLETADA
        registrar_evento(f"Reserva {self.id} procesada correctamente.")

    def descripcion(self):
        total = f"${self.costo_final:,.2f}" if self.costo_final is not None else "Pendiente de cálculo"
        return (
            f"Reserva {self.id} | Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | Estado: {self.estado.value} | Total: {total}"
        )

    def __str__(self):
        return self.descripcion()
