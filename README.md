# Sistema Integral de Gestión 

Proyecto desarrollado en Python para gestionar clientes, servicios y reservas mediante programación orientada a objetos. No utiliza bases de datos: los objetos se conservan en listas mientras se ejecuta el programa. El archivo de logs se utiliza únicamente para registrar eventos y errores.

## Requisitos

- Python 3.9 o una versión posterior.
- No requiere instalar paquetes externos.

## Archivos del proyecto

- `main.py`: punto de entrada y demostración de 15 operaciones.
- `entidades.py`: clase abstracta `Entidad`.
- `clientes.py`: clase `Cliente` y validaciones de datos personales.
- `servicios.py`: clase abstracta `Servicio` y sus tres servicios especializados.
- `reservas.py`: clase `Reserva` y control de sus estados.
- `sistema.py`: administración de las listas de clientes, servicios y reservas.
- `excepciones.py`: excepciones personalizadas.
- `registro.py`: configuración del registro de eventos y errores.
- `logs/sistema.log`: se crea y actualiza al ejecutar el programa.



El programa muestra operaciones correctas y casos con errores controlados. Al terminar, los eventos y errores quedan registrados en `logs/sistema.log`.

## Conceptos de programación orientada a objetos

- **Abstracción:** `Entidad` y `Servicio` definen comportamientos comunes y métodos que deben implementar sus clases derivadas.
- **Herencia:** `Cliente`, `Servicio` y los tres servicios especializados reutilizan características de sus clases base.
- **Polimorfismo:** cada servicio implementa su propia versión de `calcular_costo`, `validar_parametros` y `descripcion`.
- **Encapsulación:** los datos personales de `Cliente` se guardan en atributos privados y se consultan mediante propiedades.
- **Excepciones:** se definen excepciones propias y se utilizan bloques `try/except`, `else` y `finally`. También se encadenan excepciones con `raise ... from error`.
- **Métodos con parámetros opcionales:** Python no permite sobrecargar métodos por firma como otros lenguajes. Por eso, el cálculo de costos ofrece distintas variantes mediante parámetros opcionales para duración, impuesto y descuento. En equipos también se admite indicar la cantidad.

## Cálculo de costos

El costo se calcula aplicando primero el descuento y después el impuesto. El impuesto general de las reservas está configurado en 19 % como valor de ejemplo académico. Se puede modificar en `reservas.py`.
