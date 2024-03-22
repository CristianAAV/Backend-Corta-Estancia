from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from vistas.bancos import VistaBancos
from vistas.mantenimiento import VistaMantenimiento
from vistas.mantenimientos import VistaMantenimientos
from vistas.movimiento import VistaMovimiento
from vistas.movimientos import VistaMovimientos
from vistas.propiedades import VistaPropiedades
from vistas.propiedad import VistaPropiedad
from vistas.propietario import VistaPropietario
from vistas.kpi import VistaKpi
from vistas.reserva import VistaReserva
from vistas.propietario import VistaPropietario
from vistas.reservas import VistaReservas
from vistas.reservas_estado import VistaReservasEstado
from vistas.sign_in import VistaSignIn
from vistas.login import VistaLogIn
from modelos import db, Usuario
from vistas.tipo_documento import VistaTipoDocumento
from vistas.categorias import VistaCategorias
from vistas.estados import VistaEstados
from vistas.tipo_mantenimientos import VistaTipoMantenimientos
from vistas.tipo_movimientos import VistaTipoMovimientos

def create_flask_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///admon_reservas.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "frase-secreta"
    app.config["PROPAGATE_EXCEPTIONS"] = True

    app_context = app.app_context()
    app_context.push()
    add_urls(app)
    CORS(app, origins = '*')

    jwt = JWTManager(app)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return Usuario.query.filter_by(id=identity).one_or_none()

    return app


def add_urls(app):
    api = Api(app)
    api.add_resource(VistaSignIn, '/signin', '/signin/<int:id_usuario>')
    api.add_resource(VistaLogIn, '/login')
    api.add_resource(VistaPropiedades, '/propiedades')
    api.add_resource(VistaPropiedad, '/propiedades/<int:id_propiedad>')
    api.add_resource(VistaKpi, '/propiedades/<int:id_propiedad>/kpi')
    api.add_resource(VistaReservas, '/propiedades/<int:id_propiedad>/reservas')
    api.add_resource(VistaReservasEstado, '/propiedades/<int:id_propiedad>/reservas/<estado>')
    api.add_resource(VistaPropietario, '/propietarios')
    api.add_resource(VistaReserva, '/reservas/<int:id_reserva>')
    api.add_resource(VistaMantenimientos, '/propiedades/<int:id_propiedad>/mantenimientos')
    api.add_resource(VistaMantenimiento, '/mantenimientos/<int:id_mantenimiento>')
    api.add_resource(VistaMovimientos, '/propiedades/<int:id_propiedad>/movimientos')
    api.add_resource(VistaMovimiento, '/movimientos/<int:id_movimiento>')
    api.add_resource(VistaBancos, '/bancos')
    api.add_resource(VistaEstados, '/estados')
    api.add_resource(VistaCategorias, '/categorias')
    api.add_resource(VistaTipoMantenimientos, '/tipo-mantenimientos')
    api.add_resource(VistaTipoMovimientos, '/tipo-movimientos')
    api.add_resource(VistaTipoDocumento, '/tipo-documento')

# Release
# Only for testing porpuses
app = create_flask_app()
db.init_app(app)
# db.drop_all()
db.create_all()


# if __name__ == '__main__':
#     app = create_flask_app()
#     db.init_app(app)
#     db.create_all()
#     app.run()
