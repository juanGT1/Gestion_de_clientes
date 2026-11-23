"""Clase que administra clientes, servicios y reservas mediante listas."""

from clientes import Cliente
from excepciones import (
    ClienteNoEncontradoError,
    ServicioNoEncontradoError,
    ValidacionError,
)
from registro import registrar_evento, registrar_error
from reservas import Reserva


class SistemaFJ:
    """Administra los objetos en memoria, sin utilizar una base de datos."""

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise ValidacionError("El objeto que se desea registrar no es un Cliente.")
        if any(c.documento == cliente.documento for c in self.clientes):
            raise ValidacionError("Ya existe un cliente registrado con ese documento.")
        self.clientes.append(cliente)
        registrar_evento(f"Cliente registrado: {cliente.documento} - {cliente.nombre}")
        return cliente

    def registrar_servicio(self, servicio):
        # Se importa aquí para evitar dependencias innecesarias al cargar el módulo.
        from servicios import Servicio

        if not isinstance(servicio, Servicio):
            raise ValidacionError("El objeto que se desea registrar no es un Servicio.")
        servicio.validar()
        self.servicios.append(servicio)
        registrar_evento(f"Servicio registrado: {servicio.nombre} ({servicio.id})")
        return servicio

    def buscar_cliente(self, cliente_id):
        try:
            return next(c for c in self.clientes if c.id == cliente_id)
        except StopIteration as error:
            registrar_error(f"No se encontró el cliente con ID {cliente_id}.")
            raise ClienteNoEncontradoError(
                f"No existe un cliente con ID {cliente_id}."
            ) from error

    def buscar_servicio(self, servicio_id):
        try:
            return next(s for s in self.servicios if s.id == servicio_id)
        except StopIteration as error:
            registrar_error(f"No se encontró el servicio con ID {servicio_id}.")
            raise ServicioNoEncontradoError(
                f"No existe un servicio con ID {servicio_id}."
            ) from error

    def crear_reserva(self, cliente_id, servicio_id, duracion, **parametros):
        cliente = self.buscar_cliente(cliente_id)
        servicio = self.buscar_servicio(servicio_id)
        reserva = Reserva(cliente, servicio, duracion, **parametros)
        self.reservas.append(reserva)
        registrar_evento(f"Reserva creada: {reserva.id}")
        return reserva

    def listar_clientes(self):
        return [cliente.descripcion() for cliente in self.clientes]

    def listar_servicios(self):
        return [servicio.descripcion() for servicio in self.servicios]

    def listar_reservas(self):
        return [reserva.descripcion() for reserva in self.reservas]
