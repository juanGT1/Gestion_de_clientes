"""Punto de entrada: ejecuta una demostración de más de 10 operaciones."""

from clientes import Cliente
from excepciones import SistemaFJError, ValidacionError
from registro import registrar_evento, registrar_error
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from sistema import SistemaFJ


def ejecutar_operacion(numero, titulo, funcion):
    """Ejecuta una operación y evita que un error detenga toda la demostración."""
    print(f"\nOPERACIÓN {numero}: {titulo}")
    try:
        resultado = funcion()
    except SistemaFJError as error:
        print(f"[ERROR CONTROLADO] {error}")
        registrar_error(f"Fallo en operación {numero}: {titulo}")
        return None
    except Exception as error:
        # Captura errores inesperados para que la aplicación continúe funcionando.
        print(f"[ERROR INESPERADO] {error}")
        registrar_error(f"Error inesperado en operación {numero}: {titulo}")
        return None
    else:
        print(f"[OK] {resultado if resultado is not None else 'Operación realizada.'}")
        return resultado
    finally:
        print("Fin de la operación.")


def main():
    sistema = SistemaFJ()
    print("=" * 62)
    print("       SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ")
    print("=" * 62)

    # Operación 1: registro de un cliente válido.
    cliente_1 = ejecutar_operacion(
        1,
        "Registrar un cliente válido",
        lambda: sistema.registrar_cliente(
            Cliente("Sofia Gómez", "10987654", "laura@gmail.com", "3001234567")
        ),
    )

    # Operación 2: se intenta registrar un cliente con correo inválido.
    ejecutar_operacion(
        2,
        "Intentar registrar un cliente con correo inválido",
        lambda: sistema.registrar_cliente(
            Cliente("Camilo Pérez", "12345678", "correo-invalido", "3109876543")
        ),
    )

    # Operación 3: registro de un segundo cliente válido.
    cliente_2 = ejecutar_operacion(
        3,
        "Registrar otro cliente válido",
        lambda: sistema.registrar_cliente(
            Cliente("Martin Ruiz", "87654321", "andres@gmail.com", "3155556677")
        ),
    )

    # Operación 4: creación y registro de una sala.
    sala = ejecutar_operacion(
        4,
        "Crear y registrar una sala",
        lambda: sistema.registrar_servicio(
            ReservaSala("Sala de reuniones", 50000, capacidad=12)
        ),
    )

    # Operación 5: precio inválido; el error se captura y queda registrado.
    ejecutar_operacion(
        5,
        "Intentar crear un servicio con precio negativo",
        lambda: sistema.registrar_servicio(
            AlquilerEquipo("Proyector", -20000, stock=3)
        ),
    )

    # Operación 6: creación y registro de equipos.
    equipo = ejecutar_operacion(
        6,
        "Crear y registrar un servicio de alquiler de equipos",
        lambda: sistema.registrar_servicio(
            AlquilerEquipo("Computador portátil", 12000, stock=5)
        ),
    )

    # Operación 7: creación y registro de una asesoría.
    asesoria = ejecutar_operacion(
        7,
        "Crear y registrar una asesoría especializada",
        lambda: sistema.registrar_servicio(
            AsesoriaEspecializada("Asesoría de software", 80000, "Desarrollo de software")
        ),
    )

    # Operación 8: crear y confirmar una reserva de sala.
    reserva_sala = None
    if cliente_1 and sala:
        reserva_sala = ejecutar_operacion(
            8,
            "Crear y confirmar una reserva de sala para 6 personas",
            lambda: _crear_y_confirmar(
                sistema, cliente_1.id, sala.id, 2, personas=6
            ),
        )

    # Operación 9: procesar la reserva confirmada.
    if reserva_sala:
        ejecutar_operacion(
            9,
            "Procesar la reserva de sala confirmada",
            lambda: _procesar_reserva(reserva_sala),
        )

    # Operación 10: crear una reserva válida de equipos y aplicar descuento.
    reserva_equipo = None
    if cliente_2 and equipo:
        reserva_equipo = ejecutar_operacion(
            10,
            "Reservar dos computadores con descuento del 10 %",
            lambda: _crear_y_confirmar(
                sistema, cliente_2.id, equipo.id, 3,
                descuento=0.10, cantidad=2
            ),
        )

    # Operación 11: se registra un servicio no disponible e intenta reservarse.
    servicio_no_disponible = ejecutar_operacion(
        11,
        "Crear un servicio no disponible e intentar reservarlo",
        lambda: sistema.registrar_servicio(
            AsesoriaEspecializada(
                "Consultoría temporal", 60000, "Infraestructura", disponible=False
            )
        ),
    )
    if cliente_1 and servicio_no_disponible:
        ejecutar_operacion(
            12,
            "Intentar confirmar una reserva de un servicio no disponible",
            lambda: _crear_y_confirmar(
                sistema, cliente_1.id, servicio_no_disponible.id, 1
            ),
        )

    # Operación 13: parámetro inválido: se excede la capacidad de la sala.
    if cliente_1 and sala:
        ejecutar_operacion(
            13,
            "Intentar reservar una sala para más personas de las permitidas",
            lambda: sistema.crear_reserva(
                cliente_1.id, sala.id, 1, personas=30
            ),
        )

    # Operación 14: cancelar una reserva que se encontraba confirmada.
    if reserva_equipo:
        ejecutar_operacion(
            14,
            "Cancelar la reserva confirmada de equipos",
            lambda: _cancelar_reserva(reserva_equipo),
        )

    # Operación 15: consulta de los datos que permanecen en las listas.
    ejecutar_operacion(
        15,
        "Consultar el resumen de clientes, servicios y reservas",
        lambda: _mostrar_resumen(sistema),
    )

    print("\n" + "=" * 62)
    print("Demostración finalizada. El sistema continúa funcionando.")
    print("Los eventos y errores se guardaron en: logs/sistema.log")
    print("=" * 62)
    registrar_evento("Finalizó la demostración de operaciones de Software FJ.")


def _crear_y_confirmar(sistema, cliente_id, servicio_id, duracion, descuento=0.0, **parametros):
    reserva = sistema.crear_reserva(
        cliente_id, servicio_id, duracion, **parametros
    )
    total = reserva.confirmar(descuento=descuento)
    # Se devuelve el objeto para poder procesarlo en la siguiente operación.
    return reserva


def _procesar_reserva(reserva):
    reserva.procesar()
    return reserva.descripcion()


def _cancelar_reserva(reserva):
    reserva.cancelar()
    return reserva.descripcion()


def _mostrar_resumen(sistema):
    print("\nCLIENTES REGISTRADOS:")
    for elemento in sistema.listar_clientes():
        print(" -", elemento)

    print("\nSERVICIOS REGISTRADOS:")
    for elemento in sistema.listar_servicios():
        print(" -", elemento)

    print("\nRESERVAS REGISTRADAS:")
    for elemento in sistema.listar_reservas():
        print(" -", elemento)

    return (
        f"Clientes: {len(sistema.clientes)} | Servicios: {len(sistema.servicios)} | "
        f"Reservas: {len(sistema.reservas)}"
    )


if __name__ == "__main__":
    main()
