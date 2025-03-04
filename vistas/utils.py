from dataclasses import dataclass
from typing import Tuple
from modelos import Propiedad, Reserva, Movimiento, Mantenimiento, db


@dataclass
class ResultadoBuscarPropiedad:
    propiedad: Propiedad = None
    error: Tuple = ()


def buscar_propiedad(id_propiedad: int, id_usuario: int) -> ResultadoBuscarPropiedad:
        buscar_propiedad = ResultadoBuscarPropiedad()
        propiedad = Propiedad.query.filter(Propiedad.id==id_propiedad, Propiedad.id_usuario == id_usuario).one_or_none()
        if not propiedad:
            buscar_propiedad.error = {'mensaje': 'propiedad no encontrada'}, 404
        buscar_propiedad.propiedad = propiedad
        return buscar_propiedad

@dataclass
class ResultadoBuscarMantenimiento:
    mantenimiento: Mantenimiento = None
    error: Tuple = ()


def buscar_mantenimiento(id_mantenimiento: int, id_usuario: int) -> ResultadoBuscarMantenimiento:
        buscar_mantenimiento = ResultadoBuscarMantenimiento()
        mantenimiento = db.session.query(Mantenimiento).join(Propiedad).filter(Mantenimiento.id == id_mantenimiento, Propiedad.id_usuario == id_usuario).one_or_none()
        if not mantenimiento:
            buscar_mantenimiento.error = {'mensaje': 'Mantenimiento no encontrado'}, 404
        buscar_mantenimiento.mantenimiento = mantenimiento
        return buscar_mantenimiento

@dataclass
class ResultadoBuscarReserva:
    reserva: Reserva = None
    error: Tuple = ()


def buscar_reserva(id_reserva: int, id_usuario: int) -> ResultadoBuscarReserva:
        buscar_reserva = ResultadoBuscarReserva()
        reserva = db.session.query(Reserva).join(Propiedad).filter(Reserva.id == id_reserva, Propiedad.id_usuario == id_usuario).one_or_none()
        if not reserva:
            buscar_reserva.error = {'mensaje': 'reserva no encontrada'}, 404
        buscar_reserva.reserva = reserva
        return buscar_reserva


@dataclass
class ResultadoBuscarMovimiento:
    movimiento: Movimiento = None
    error: Tuple = ()


def buscar_movimiento(id_movimiento: int, id_usuario: int) -> ResultadoBuscarMovimiento:
        buscar_movimiento = ResultadoBuscarMovimiento()
        movimiento = db.session.query(Movimiento).join(Propiedad).filter(Propiedad.id_usuario == id_usuario, Movimiento.id == id_movimiento).one_or_none()
        if not movimiento:
            buscar_movimiento.error = {'mensaje': 'movimiento no encontrado'}, 404
        buscar_movimiento.movimiento = movimiento
        return buscar_movimiento

