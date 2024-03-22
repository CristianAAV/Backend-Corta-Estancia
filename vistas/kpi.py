from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask_jwt_extended import current_user, jwt_required
from modelos import Movimiento, MovimientoSchema, Propiedad, db, TipoMovimiento
from vistas.utils import buscar_propiedad

movimiento_schema = MovimientoSchema()

class VistaKpi(Resource):

    @jwt_required()
    def get(self, id_propiedad):
        resultado_buscar_propiedad = buscar_propiedad(id_propiedad, current_user.id)
        if resultado_buscar_propiedad.error:
           return {"valor":0}
        movimientos = db.session.query(Movimiento).join(Propiedad).filter(Propiedad.id_usuario == current_user.id, Propiedad.id == id_propiedad).all()

        ingresos = 0
        egresos = 0

        for movimiento in movimientos:
            if movimiento.tipo_movimiento == TipoMovimiento.INGRESO:
                ingresos = ingresos + movimiento.valor
            if movimiento.tipo_movimiento == TipoMovimiento.EGRESO:
                egresos = egresos + movimiento.valor

        if egresos != 0:
            return {"valor":(ingresos - egresos)/ ingresos}
        else:
            return {"valor":0}
