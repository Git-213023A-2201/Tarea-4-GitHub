from abc import ABC, abstractmethod
from datetime import datetime


# ==================================================
# LOGGER
# ==================================================

def registrar_log(mensaje):

    with open(
        "logs.txt",
        "a",
        encoding="utf-8"
    ) as archivo:

        archivo.write(
            f"{datetime.now()} "
            f"- ERROR: "
            f"{mensaje}\n"
        )


# ==================================================
# EXCEPCIONES PERSONALIZADAS
# ==================================================

class ClienteInvalidoError(Exception):
    pass


class ServicioNoDisponibleError(Exception):
    pass


class ReservaError(Exception):
    pass


# ==================================================
# CLASE ABSTRACTA ENTIDAD
# ==================================================

class Entidad(ABC):

    def __init__(self, nombre):

        self.nombre = nombre


# ==================================================
# CLASE CLIENTE
# ==================================================

class Cliente(Entidad):

    def __init__(
        self,
        nombre,
        correo,
        telefono
    ):

        super().__init__(nombre)

        if not nombre.strip():

            raise ClienteInvalidoError(
                "El nombre no puede estar vacío"
            )

        if "@" not in correo:

            raise ClienteInvalidoError(
                "Correo inválido"
            )

        if len(telefono) < 10:

            raise ClienteInvalidoError(
                "Teléfono inválido"
            )

        self.__correo = correo
        self.__telefono = telefono

    @property
    def correo(self):

        return self.__correo

    @property
    def telefono(self):

        return self.__telefono

    def __str__(self):

        return (
            f"Cliente: {self.nombre}"
        )


# ==================================================
# CLASE ABSTRACTA SERVICIO
# ==================================================

class Servicio(Entidad, ABC):

    def __init__(
        self,
        nombre,
        precio_base,
        disponibilidad
    ):

        super().__init__(nombre)

        self.precio_base = precio_base
        self.disponibilidad = disponibilidad

    @abstractmethod
    def calcular_costo(
        self,
        cantidad,
        impuesto=0,
        descuento=0
    ):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass


# ==================================================
# RESERVA SALA
# ==================================================

class ReservaSala(Servicio):

    def calcular_costo(
        self,
        cantidad,
        impuesto=0,
        descuento=0
    ):

        total = self.precio_base * cantidad

        total += total * impuesto

        total -= total * descuento

        return total

    def describir_servicio(self):

        return (
            f"Reserva de sala: "
            f"{self.nombre}"
        )


# ==================================================
# ALQUILER EQUIPO
# ==================================================

class AlquilerEquipo(Servicio):

    def calcular_costo(
        self,
        cantidad,
        impuesto=0,
        descuento=0
    ):

        total = self.precio_base * cantidad

        total += total * impuesto

        total -= total * descuento

        return total

    def describir_servicio(self):

        return (
            f"Alquiler de equipo: "
            f"{self.nombre}"
        )


# ==================================================
# ASESORÍA
# ==================================================

class AsesoriaEspecializada(Servicio):

    def __init__(
        self,
        nombre,
        precio_base,
        especialista
    ):

        super().__init__(
            nombre,
            precio_base,
            1
        )

        self.especialista = especialista

    def calcular_costo(
        self,
        cantidad,
        impuesto=0,
        descuento=0
    ):

        total = self.precio_base * cantidad

        total += total * impuesto

        total -= total * descuento

        return total

    def describir_servicio(self):

        return (
            f"Asesoría especializada "
            f"con experto "
            f"{self.especialista}"
        )


# ==================================================
# CLASE RESERVA
# ==================================================

class Reserva:

    def __init__(
        self,
        cliente,
        servicio,
        duracion
    ):

        if duracion <= 0:

            raise ReservaError(
                "La duración debe ser mayor a cero"
            )

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def confirmar(self):

        try:

            if self.servicio.disponibilidad <= 0:

                raise ServicioNoDisponibleError(
                    "Servicio no disponible"
                )

            self.servicio.disponibilidad -= 1

            self.estado = "Confirmada"

        except ServicioNoDisponibleError as e:

            raise ReservaError(
                "Error al confirmar reserva"
            ) from e

        else:

            print("Reserva confirmada")

        finally:

            print(
                "Proceso de reserva finalizado"
            )

    def cancelar(self):

        self.estado = "Cancelada"

        self.servicio.disponibilidad += 1

        print("Reserva cancelada")

    def __str__(self):

        return (
            f"{self.cliente.nombre}"
            f" | "
            f"{self.servicio.nombre}"
            f" | "
            f"{self.estado}"
        )


# ==================================================
# PROGRAMA PRINCIPAL
# ==================================================

def ejecutar_operaciones():

    reservas = []

    print(
        "\n========== SOFTWARE FJ ==========\n"
    )

    # CLIENTE VÁLIDO
    try:

        cliente1 = Cliente(
            "Juan Pérez",
            "juan@gmail.com",
            "3001234567"
        )

        print(cliente1)

    except Exception as e:

        registrar_log(str(e))

    # CLIENTE INVÁLIDO
    try:

        cliente2 = Cliente(
            "",
            "correo_malo",
            "123"
        )

    except Exception as e:

        registrar_log(str(e))

    # SERVICIOS
    try:

        sala = ReservaSala(
            "Sala Premium",
            100000,
            5
        )

        equipo = AlquilerEquipo(
            "Laptop Gamer",
            80000,
            3
        )

        asesoria = AsesoriaEspecializada(
            "Asesoría Python",
            120000,
            "Senior"
        )

        print(
            sala.describir_servicio()
        )

        print(
            equipo.describir_servicio()
        )

        print(
            asesoria.describir_servicio()
        )

    except Exception as e:

        registrar_log(str(e))

    # RESERVA EXITOSA
    try:

        reserva1 = Reserva(
            cliente1,
            sala,
            2
        )

        reserva1.confirmar()

        reservas.append(reserva1)

    except Exception as e:

        registrar_log(str(e))

    # RESERVA INVÁLIDA
    try:

        reserva2 = Reserva(
            cliente1,
            sala,
            -2
        )

        reserva2.confirmar()

    except Exception as e:

        registrar_log(str(e))

    # SERVICIO SIN DISPONIBILIDAD
    try:

        sala.disponibilidad = 0

        reserva3 = Reserva(
            cliente1,
            sala,
            1
        )

        reserva3.confirmar()

    except Exception as e:

        registrar_log(str(e))

    # CANCELAR
    try:

        reserva1.cancelar()

    except Exception as e:

        registrar_log(str(e))

    # COSTOS
    try:

        costo1 = sala.calcular_costo(
            2,
            impuesto=0.19
        )

        print(
            f"\nCosto con impuesto: "
            f"{costo1}"
        )

    except Exception as e:

        registrar_log(str(e))

    try:

        costo2 = equipo.calcular_costo(
            1,
            descuento=0.10
        )

        print(
            f"Costo con descuento: "
            f"{costo2}"
        )

    except Exception as e:

        registrar_log(str(e))

    print(
        "\n========== RESERVAS ==========\n"
    )

    for reserva in reservas:

        print(reserva)

    print(
        "\nSistema ejecutado correctamente.\n"
    )


# ==================================================
# EJECUCIÓN
# ==================================================

if __name__ == "__main__":

    ejecutar_operaciones()