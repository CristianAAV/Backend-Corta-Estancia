from datetime import datetime
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource
from modelos.modelos import ReservaSchema
from vistas.utils import buscar_propiedad

reserva_schema = ReservaSchema()

class VistaReservasEstado(Resource):

    @jwt_required()
    def get(self, id_propiedad, estado):
        resultado_buscar_propiedad = buscar_propiedad(id_propiedad, current_user.id)
        if resultado_buscar_propiedad.error:
            return resultado_buscar_propiedad.error
        reservas = resultado_buscar_propiedad.propiedad.reservas
        reserva_estado = []
        for reserva in reservas:
            if estado == 'activas':
                if reserva.fecha_salida  > datetime.now():
                    reserva_estado.append(reserva)
            else : #estado es 'pasadas'
                if reserva.fecha_salida  < datetime.now():
                    reserva_estado.append(reserva)
        return reserva_schema.dump(reserva_estado, many=True)