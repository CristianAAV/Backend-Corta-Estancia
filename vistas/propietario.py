from flask import request
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy import exc

from modelos import Propietario, db, PropietarioSchema

propietario_schema = PropietarioSchema()


class VistaPropietario(Resource):

    @jwt_required()
    def get(self):
        propietarios = Propietario.query.filter()
        return propietario_schema.dump(propietarios, many=True)