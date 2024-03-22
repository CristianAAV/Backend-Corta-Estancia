from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from modelos import Estado


class VistaEstados(Resource):

    @jwt_required()
    def get(self):
        return jsonify([estado.name for estado in Estado])
