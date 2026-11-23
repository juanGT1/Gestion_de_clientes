"""Excepciones personalizadas utilizadas por el sistema Software FJ."""


class SistemaFJError(Exception):
    """Excepción base para los errores controlados del sistema."""


class ValidacionError(SistemaFJError):
    """Se produce cuando un dato no cumple las validaciones."""


class ClienteNoEncontradoError(SistemaFJError):
    """Se produce cuando no existe el cliente solicitado."""


class ServicioNoEncontradoError(SistemaFJError):
    """Se produce cuando no existe el servicio solicitado."""


class ServicioNoDisponibleError(SistemaFJError):
    """Se produce cuando se intenta reservar un servicio no disponible."""


class ReservaError(SistemaFJError):
    """Se produce cuando una operación de reserva no está permitida."""
