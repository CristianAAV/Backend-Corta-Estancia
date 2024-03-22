from flask import request
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError
from modelos import Mantenimiento, MantenimientoSchema, Propiedad, TipoMantenimiento, TipoMovimiento, Estado, Movimiento, TipoMantenimiento, Mantenimiento, Categoria, db
from vistas.utils import buscar_propiedad
from sqlalchemy import exc

mantenimiento_schema = MantenimientoSchema()


class VistaMantenimientos(Resource):

    @jwt_required()
    def post(self, id_propiedad):
        resultado_buscar_propiedad = buscar_propiedad(id_propiedad, current_user.id)
        if resultado_buscar_propiedad.error:
           return resultado_buscar_propiedad.error
        try:
            mantenimiento = mantenimiento_schema.load(request.json, session=db.session)
            mantenimiento.id_propiedad = id_propiedad
            db.session.add(mantenimiento)
            db.session.commit()
        except ValidationError as validation_error:
            return validation_error.messages, 400
        except exc.IntegrityError:
            db.session.rollback()
            return {'mensaje': 'Hubo un error creando el mantenimiento. Revise los datos proporcionados'}, 400
        
        self.crear_movimiento(mantenimiento)
        return mantenimiento_schema.dump(mantenimiento), 201

    @jwt_required()
    def get(self, id_propiedad):
        resultado_buscar_propiedad = buscar_propiedad(id_propiedad, current_user.id)
        if resultado_buscar_propiedad.error:
           return resultado_buscar_propiedad.error
        mantenimientos = db.session.query(Mantenimiento).join(Propiedad).filter(Propiedad.id_usuario == current_user.id, Propiedad.id == id_propiedad).all()
        return mantenimiento_schema.dump(mantenimientos, many=True)
    
    def crear_movimiento(self, mantenimiento):
        movimiento_egreso = Movimiento(fecha=mantenimiento.fecha,
                                categoria=Categoria.EGRESOS_POR_ADMINISTRADOR,
                                descripcion="Costo por mantenimiento",
                                valor=mantenimiento.costo,
                                id_reserva=None,
                                tipo_movimiento=TipoMovimiento.EGRESO,
                                id_propiedad=mantenimiento.id_propiedad)
        db.session.add(movimiento_egreso)
        db.session.commit()

    