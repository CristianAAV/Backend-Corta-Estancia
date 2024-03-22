from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from modelos import TipoMantenimiento


class VistaTipoMantenimientos(Resource):

    @jwt_required()
    def get(self):
        return jsonify([tipo_mantenimiento.name for tipo_mantenimiento in TipoMantenimiento])
