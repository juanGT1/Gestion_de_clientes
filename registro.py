"""Configuración del registro de eventos y errores en un archivo log."""

import logging
from pathlib import Path


RUTA_LOGS = Path(__file__).resolve().parent / "logs"
RUTA_LOGS.mkdir(exist_ok=True)
RUTA_ARCHIVO = RUTA_LOGS / "sistema.log"

logger = logging.getLogger("SoftwareFJ")
logger.setLevel(logging.INFO)

# Evita agregar manejadores repetidos si el módulo se importa más de una vez.
if not logger.handlers:
    formato = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    manejador = logging.FileHandler(RUTA_ARCHIVO, encoding="utf-8")
    manejador.setFormatter(formato)
    logger.addHandler(manejador)


def registrar_evento(mensaje):
    """Guarda un evento importante en el archivo de registro."""
    logger.info(mensaje)


def registrar_error(mensaje):
    """Guarda un error y su información de excepción en el archivo."""
    logger.exception(mensaje)
