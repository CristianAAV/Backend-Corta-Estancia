from unittest import TestCase
from modelos import Usuario, db, TipoUsuario
from sqlalchemy import exc

from modelos.modelos import UsuarioSchema

usuario_schema = UsuarioSchema()

class TestCreateUser(TestCase):

    def tearDown(self):
        db.session.rollback()
        Usuario.query.delete()

    def test_solo_un_usuario_es_creado_en_db(self):
        new_user = Usuario(usuario='test_user', contrasena='123456', tipo_usuario=TipoUsuario.ADMINISTRADOR.value)
        db.session.add(new_user)
        db.session.commit()

        users_in_db = Usuario.query.all()
        self.assertEqual(len(users_in_db), 1)

    def test_usuario_administrador_esperado_es_creado(self):
        new_user = Usuario(usuario='test_user', contrasena='123456', tipo_usuario=TipoUsuario.ADMINISTRADOR.value)
        db.session.add(new_user)
        db.session.commit()

        user_from_db = Usuario.query.filter(Usuario.usuario=='test_user').first()
        self.assertEqual(user_from_db.contrasena, '123456')
        self.assertEqual(user_from_db.tipo_usuario.value, TipoUsuario.ADMINISTRADOR.value)
    
    def test_usuario_propietario_esperado_es_creado(self):
        new_user = Usuario(usuario='test_user', contrasena='123456', tipo_usuario=TipoUsuario.PROPIETARIO.value)
        db.session.add(new_user)
        db.session.commit()

        user_from_db = Usuario.query.filter(Usuario.usuario=='test_user').first()
        self.assertEqual(user_from_db.contrasena, '123456')
        self.assertEqual(user_from_db.tipo_usuario.value, TipoUsuario.PROPIETARIO.value)    

    def test_usuario_normal_esperado_es_creado(self):
        new_user = Usuario(usuario='test_user', contrasena='123456', tipo_usuario=TipoUsuario.ADMINISTRADOR.value)
        db.session.add(new_user)
        db.session.commit()

        user_from_db = Usuario.query.filter(Usuario.usuario=='test_user').first()
        self.assertEqual(user_from_db.contrasena, '123456')
        self.assertEqual(user_from_db.tipo_usuario.value, TipoUsuario.ADMINISTRADOR.value)

    def test_dispara_un_error_de_integridad(self):
        first_user = Usuario(usuario='test_user', contrasena='123456', tipo_usuario=TipoUsuario.ADMINISTRADOR.value)
        db.session.add(first_user)
        db.session.commit()
        with self.assertRaises(exc.IntegrityError):
            user_same_username = Usuario(usuario='test_user', contrasena='abcdef', tipo_usuario=TipoUsuario.ADMINISTRADOR.value)
            db.session.add(user_same_username)
            db.session.commit()

    def test_campos_no_pueden_ser_nullos(self):
        user = Usuario()
        with self.assertRaises(exc.IntegrityError):
            db.session.add(user)
            db.session.commit()
