from unittest import TestCase

from faker import Faker
from modelos import Propietario, db
from sqlalchemy import exc

from modelos.modelos import TipoDocumento, TipoUsuario, Usuario, UsuarioSchema

usuario_schema = UsuarioSchema()

class TestCreatePropietairo(TestCase):

    def setUp(self):
        self.data_factory = Faker()
        self.usuario = Usuario(
            usuario=self.data_factory.name(),
            contrasena=self.data_factory.word(),
            tipo_usuario=TipoUsuario.PROPIETARIO.value
        )
        db.session.add(self.usuario)
        db.session.commit()
    
    def tearDown(self):
        db.session.rollback()
        Propietario.query.delete()
        Usuario.query.delete()

    def test_solo_un_propietario_es_creado_en_db(self):
        nuevo_propietario = Propietario(nombres = self.data_factory.name(), apellidos = self.data_factory.name(),
                                        tipo_documento = 'CEDULA_CIUDADANIA', documento = self.data_factory.word(),
                                        telefono = self.data_factory.word(), correo = self.data_factory.email(),
                                        id_usuario = self.usuario.id)
        db.session.add(nuevo_propietario)
        db.session.commit()
        propietario_db = Propietario.query.all()
        self.assertEqual(len(propietario_db), 1)
        
    def test_id_usuario_repetido(self):
        nuevo_propietario = Propietario(nombres = self.data_factory.name(), apellidos = self.data_factory.name(),
                                        tipo_documento = 'CEDULA_CIUDADANIA', documento = self.data_factory.word(),
                                        telefono = self.data_factory.word(), correo = self.data_factory.email(),
                                        id_usuario = self.usuario.id)
        db.session.add(nuevo_propietario)
        db.session.commit()
        with self.assertRaises(exc.IntegrityError):
            nuevo_propietario = Propietario(nombres = self.data_factory.name(), apellidos = self.data_factory.name(),
                                        tipo_documento = 'CEDULA_CIUDADANIA', documento = self.data_factory.word(),
                                        telefono = self.data_factory.word(), correo = self.data_factory.email(),
                                        id_usuario = self.usuario.id)
            db.session.add(nuevo_propietario)
            db.session.commit()
    
    def test_campos_no_pueden_ser_nullos(self):
        user = Propietario()
        with self.assertRaises(exc.IntegrityError):
            db.session.add(user)
            db.session.commit()


