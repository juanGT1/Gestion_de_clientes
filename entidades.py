"""Clase abstracta que representa las entidades generales del sistema."""

from abc import ABC, abstractmethod
from uuid import uuid4


class Entidad(ABC):
    """Clase base abstracta para los objetos principales de Software FJ."""

    def __init__(self):
        # Cada entidad recibe un identificador corto y único.
        self._id = uuid4().hex[:8].upper()

    @property
    def id(self):
        """Permite consultar el identificador sin modificarlo directamente."""
        return self._id

    @abstractmethod
    def validar(self):
        """Cada entidad debe implementar sus propias validaciones."""
        raise NotImplementedError

    @abstractmethod
    def descripcion(self):
        """Cada entidad debe indicar cómo se describe."""
        raise NotImplementedError
