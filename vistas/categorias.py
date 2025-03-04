from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from modelos import Categoria


class VistaCategorias(Resource):

    @jwt_required()
    def get(self):
        return jsonify([categoria.name for categoria in Categoria])
