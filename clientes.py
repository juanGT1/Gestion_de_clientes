"""Definición de la clase Cliente y sus validaciones."""

import re

from entidades import Entidad
from excepciones import ValidacionError


class Cliente(Entidad):
    """Representa a una persona que solicita los servicios de Software FJ."""

    def __init__(self, nombre, documento, correo, telefono):
        super().__init__()
        # Los atributos privados evitan que se cambien sin pasar por validación.
        self.__nombre = nombre.strip() if isinstance(nombre, str) else nombre
        self.__documento = str(documento).strip() if documento is not None else ""
        self.__correo = correo.strip().lower() if isinstance(correo, str) else correo
        self.__telefono = str(telefono).strip() if telefono is not None else ""
        self.validar()

    @property
    def nombre(self):
        return self.__nombre

    @property
    def documento(self):
        return self.__documento

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def validar(self):
        """Comprueba que los datos personales tengan un formato válido."""
        if not isinstance(self.__nombre, str) or len(self.__nombre) < 3:
            raise ValidacionError("El nombre debe tener al menos 3 caracteres.")

        if not re.fullmatch(r"[A-Za-z0-9-]{5,15}", self.__documento):
            raise ValidacionError(
                "El documento debe tener entre 5 y 15 caracteres alfanuméricos."
            )

        patron_correo = r"^[\w.+-]+@[\w-]+\.[A-Za-z]{2,}$"
        if not isinstance(self.__correo, str) or not re.fullmatch(
            patron_correo, self.__correo
        ):
            raise ValidacionError("El correo electrónico no tiene un formato válido.")

        if not re.fullmatch(r"\+?[0-9]{7,15}", self.__telefono):
            raise ValidacionError("El teléfono debe contener entre 7 y 15 dígitos.")

    def descripcion(self):
        return (
            f"Cliente {self.__nombre} | Documento: {self.__documento} | "
            f"Correo: {self.__correo}"
        )

    def __str__(self):
        return f"{self.__nombre} ({self.__documento}) - ID: {self.id}"
