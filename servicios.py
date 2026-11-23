"""Clase abstracta Servicio y sus tres tipos de servicios especializados."""

from abc import abstractmethod
from math import isfinite

from entidades import Entidad
from excepciones import ValidacionError


class Servicio(Entidad):
    """Clase base para cualquier servicio ofrecido por Software FJ."""

    def __init__(self, nombre, precio_base, disponible=True):
        super().__init__()
        self.nombre = nombre.strip() if isinstance(nombre, str) else nombre
        self.precio_base = precio_base
        self.disponible = disponible
        # Se llama explícitamente a la validación base para no ejecutar
        # antes de tiempo las validaciones que dependen de las clases hijas.
        Servicio.validar(self)

    def validar(self):
        """Valida los datos que comparten todos los servicios."""
        if not isinstance(self.nombre, str) or not self.nombre:
            raise ValidacionError("El nombre del servicio es obligatorio.")
        if isinstance(self.precio_base, bool) or not isinstance(
            self.precio_base, (int, float)
        ):
            raise ValidacionError("El precio base debe ser un número.")
        if not isfinite(self.precio_base) or self.precio_base <= 0:
            raise ValidacionError("El precio base debe ser mayor que cero.")
        if not isinstance(self.disponible, bool):
            raise ValidacionError("La disponibilidad debe ser True o False.")

    @staticmethod
    def _validar_duracion(duracion):
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):
            raise ValidacionError("La duración debe ser un número.")
        if not isfinite(duracion) or duracion <= 0:
            raise ValidacionError("La duración debe ser mayor que cero.")

    @staticmethod
    def _calcular_total(subtotal, impuesto=0.0, descuento=0.0):
        """Aplica descuento e impuesto; ambos se reciben como porcentajes decimales."""
        try:
            if not 0 <= descuento <= 1:
                raise ValidacionError("El descuento debe estar entre 0 y 1.")
            if not 0 <= impuesto <= 1:
                raise ValidacionError("El impuesto debe estar entre 0 y 1.")
            total_con_descuento = subtotal * (1 - descuento)
            total = total_con_descuento * (1 + impuesto)
            if not isfinite(total) or total < 0:
                raise ValidacionError("El cálculo del costo produjo un valor inválido.")
            return round(total, 2)
        except TypeError as error:
            # Encadenamiento: conserva la causa original para facilitar el diagnóstico.
            raise ValidacionError("Impuesto y descuento deben ser valores numéricos.") from error

    def cambiar_disponibilidad(self, disponible):
        if not isinstance(disponible, bool):
            raise ValidacionError("La disponibilidad debe ser True o False.")
        self.disponible = disponible

    def __str__(self):
        return self.descripcion()

    @abstractmethod
    def validar_parametros(self, duracion, **kwargs):
        """Cada tipo de servicio valida sus parámetros particulares."""
        raise NotImplementedError

    @abstractmethod
    def calcular_costo(self, duracion=1, impuesto=0.0, descuento=0.0, **kwargs):
        """Cada servicio calcula su costo de forma diferente."""
        raise NotImplementedError

    @abstractmethod
    def descripcion(self):
        raise NotImplementedError


class ReservaSala(Servicio):
    """Servicio para reservar una sala por horas."""

    def __init__(self, nombre, precio_base, capacidad, disponible=True):
        super().__init__(nombre, precio_base, disponible)
        self.capacidad = capacidad
        self.validar()

    def validar(self):
        super().validar()
        if isinstance(getattr(self, "capacidad", None), bool) or not isinstance(
            getattr(self, "capacidad", None), int
        ) or self.capacidad <= 0:
            raise ValidacionError("La capacidad de la sala debe ser un entero positivo.")

    def validar_parametros(self, duracion, **kwargs):
        self._validar_duracion(duracion)
        personas = kwargs.get("personas", 1)
        if isinstance(personas, bool) or not isinstance(personas, int) or personas <= 0:
            raise ValidacionError("La cantidad de personas debe ser un entero positivo.")
        if personas > self.capacidad:
            raise ValidacionError(
                f"La sala admite máximo {self.capacidad} personas; se solicitaron {personas}."
            )

    def calcular_costo(self, duracion=1, impuesto=0.0, descuento=0.0, **kwargs):
        self.validar_parametros(duracion, **kwargs)
        return self._calcular_total(self.precio_base * duracion, impuesto, descuento)

    def descripcion(self):
        return f"Reserva de sala: {self.nombre} | Capacidad: {self.capacidad} personas"


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos por horas y unidades."""

    def __init__(self, nombre, precio_base, stock, disponible=True):
        super().__init__(nombre, precio_base, disponible)
        self.stock = stock
        self.validar()

    def validar(self):
        super().validar()
        if isinstance(getattr(self, "stock", None), bool) or not isinstance(
            getattr(self, "stock", None), int
        ) or self.stock <= 0:
            raise ValidacionError("El stock del equipo debe ser un entero positivo.")

    def validar_parametros(self, duracion, **kwargs):
        self._validar_duracion(duracion)
        cantidad = kwargs.get("cantidad", 1)
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            raise ValidacionError("La cantidad de equipos debe ser un entero positivo.")
        if cantidad > self.stock:
            raise ValidacionError(
                f"No hay suficientes unidades. Stock disponible: {self.stock}."
            )

    def calcular_costo(self, duracion=1, impuesto=0.0, descuento=0.0, **kwargs):
        self.validar_parametros(duracion, **kwargs)
        cantidad = kwargs.get("cantidad", 1)
        subtotal = self.precio_base * duracion * cantidad
        return self._calcular_total(subtotal, impuesto, descuento)

    def descripcion(self):
        return f"Alquiler de equipo: {self.nombre} | Unidades disponibles: {self.stock}"


class AsesoriaEspecializada(Servicio):
    """Servicio de asesoría especializada cobrado por hora."""

    def __init__(self, nombre, precio_base, especialidad, disponible=True):
        super().__init__(nombre, precio_base, disponible)
        self.especialidad = especialidad.strip() if isinstance(especialidad, str) else especialidad
        self.validar()

    def validar(self):
        super().validar()
        if not isinstance(getattr(self, "especialidad", None), str) or not self.especialidad:
            raise ValidacionError("La especialidad de la asesoría es obligatoria.")

    def validar_parametros(self, duracion, **kwargs):
        self._validar_duracion(duracion)
        if duracion > 8:
            raise ValidacionError("Una asesoría no puede superar 8 horas por reserva.")

    def calcular_costo(self, duracion=1, impuesto=0.0, descuento=0.0, **kwargs):
        self.validar_parametros(duracion, **kwargs)
        return self._calcular_total(self.precio_base * duracion, impuesto, descuento)

    def descripcion(self):
        return f"Asesoría: {self.nombre} | Especialidad: {self.especialidad}"
