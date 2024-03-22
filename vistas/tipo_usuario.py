from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from modelos import TipoUsuario


class VistaTiposUsuario(Resource):

    def get(self):
        return jsonify([tipo_usuario.name for tipo_usuario in TipoUsuario])
