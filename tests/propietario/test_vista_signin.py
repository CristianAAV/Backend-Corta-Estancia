import json
from faker import Faker
from flask_jwt_extended import create_access_token
from modelos import Usuario, db, TipoUsuario
from modelos.modelos import Propietario, UsuarioSchema, TipoDocumento

usuario_schema = UsuarioSchema()

class TestCrearPropietario:

    def setup_method(self):
        self.data_factory = Faker()
        self.datos_nuevo_propietario = {
            'usuario': self.data_factory.name(),
            'contrasena': self.data_factory.word(),
            'tipoUsuario': TipoUsuario.PROPIETARIO.value,
            'nombres' : self.data_factory.name(), 
            'apellidos' : self.data_factory.name(),
            'tipoDocumento' : TipoDocumento.CEDULA_CIUDADANIA.value, 
            'documento' : self.data_factory.word(),
            'telefono' : self.data_factory.word(), 
            'correo' : self.data_factory.email(),
        }

    def teardown_method(self):
        db.session.rollback()
        Usuario.query.delete()
        Propietario.query.delete()

    def actuar(self, nuevo_usuario_info, client):
        self.respuesta = client.post('/signin', data=json.dumps(nuevo_usuario_info), headers={'Content-Type': 'application/json'})
        self.respuesta_json = self.respuesta.json
    
    def test_crear_usuario_responde_201(self, client):
        self.actuar(self.datos_nuevo_propietario, client)
        assert self.respuesta.status_code == 201

    def test_retorna_campos_esperados(self, client):
        self.actuar(self.datos_nuevo_propietario, client)
        assert 'token' in self.respuesta_json
        assert 'id' in self.respuesta_json
        assert 'mensaje' in self.respuesta_json

    def test_crea_propietario_en_db(self, client):
        self.actuar(self.datos_nuevo_propietario, client)
        usuario_db = Propietario.query.filter(Propietario.id_usuario == self.respuesta_json['id']).all()
        assert len(usuario_db) == 1