from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from modelos import TipoDocumento


class VistaTipoDocumento(Resource):

    def get(self):
        return jsonify([tipo_documento.name for tipo_documento in TipoDocumento])
