import datetime
from flask import request
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource
from modelos import Mantenimiento, MantenimientoSchema,Estado,TipoMantenimiento, db
from vistas.utils import buscar_mantenimiento

mantenimiento_schema = MantenimientoSchema()


class VistaMantenimiento(Resource):

    @jwt_required()
    def put(self, id_mantenimiento):
        resultado_buscar_mantenimiento = buscar_mantenimiento(id_mantenimiento, current_user.id)
        if resultado_buscar_mantenimiento.error:
            return resultado_buscar_mantenimiento.error
        mantenimiento = resultado_buscar_mantenimiento.mantenimiento
        if not self.es_posible_actualizar_mantenimiento(mantenimiento):
            return {'mensaje': 'No es posible actualizar este mantenimiento ya fue realizado.'}, 400
        mantenimiento_schema.load(request.json, session=db.session, instance=mantenimiento, partial=True)
        db.session.commit() 
        return mantenimiento_schema.dump(mantenimiento)
    
    @jwt_required()
    def delete(self, id_mantenimiento):
        resultado_buscar_mantenimiento = buscar_mantenimiento(id_mantenimiento, current_user.id)
        if resultado_buscar_mantenimiento.error:
            return resultado_buscar_mantenimiento.error
        mantenimiento = resultado_buscar_mantenimiento.mantenimiento
        if not self.es_posible_eliminar_mantenimiento(mantenimiento):
            return {'mensaje': 'No se puede eliminar este mantenimiento por que esta en una fecha pasada o ya fue realizado.'}, 400
        db.session.delete(mantenimiento)
        db.session.commit()
        return "", 204
    
    @jwt_required()
    def get(self, id_mantenimiento):
        resultado_buscar_mantenimiento = buscar_mantenimiento(id_mantenimiento, current_user.id)
        if resultado_buscar_mantenimiento.error:
            return resultado_buscar_mantenimiento.error
        return mantenimiento_schema.dump(resultado_buscar_mantenimiento.mantenimiento)
    
    def es_posible_actualizar_mantenimiento(self, mantenimiento):
        if mantenimiento.estado == Estado.REALIZADO:
            return False
        return True
            
    def es_posible_eliminar_mantenimiento(self, mantenimiento):
        if mantenimiento.estado == Estado.REALIZADO:
            return False
        if mantenimiento.fecha.month < datetime.datetime.now().month:
            return False
        return True
        
    
