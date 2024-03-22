from flask_jwt_extended import create_access_token
from modelos import Usuario, Propietario, db, PropiedadSchema, TipoUsuario


class TestObtenerPropiedades:

    def setup_method(self):
        self.usuario_1 = Usuario(usuario='usuario_1', contrasena='123456', tipo_usuario=TipoUsuario.ADMINISTRADOR.value)
        self.usuario_2 = Usuario(usuario='usuario_2', contrasena='123456', tipo_usuario=TipoUsuario.ADMINISTRADOR.value)
        self.usuario_3 = Usuario(usuario='usuario_3', contrasena='123456', tipo_usuario=TipoUsuario.ADMINISTRADOR.value)
        db.session.add(self.usuario_1)
        db.session.add(self.usuario_2)
        db.session.add(self.usuario_3)
        db.session.commit()

        self.propietario_1_usu_1 = Propietario(id_usuario=self.usuario_1.id, nombres='Nombre 1', apellidos='Apellido 1',
                              tipo_documento='CEDULA_CIUDADANIA', documento='22211133', correo='usuario_1@gmail.com', telefono="12345687")
        self.propietario_2_usu_2 = Propietario(id_usuario=self.usuario_2.id, nombres='Nombre 2', apellidos='Apellido 2',
                              tipo_documento='CEDULA_CIUDADANIA', documento='11144433', correo='usuario_2@gmail.com', telefono="12345687")
        self.propietario_3_usu_3 = Propietario(id_usuario=self.usuario_3.id, nombres='Nombre 3', apellidos='Apellido 3',
                              tipo_documento='CEDULA_CIUDADANIA', documento='66622288', correo='usuario_3@gmail.com', telefono="12345687")

        db.session.add(self.propietario_1_usu_1)
        db.session.add(self.propietario_2_usu_2)
        db.session.add(self.propietario_3_usu_3)
        db.session.commit()

    def actuar(self, client, token=None):
        headers = {'Content-Type': 'application/json'}
        if token:
            headers.update({'Authorization': f'Bearer {token}'})
        self.respuesta = client.get('/propietarios', headers=headers)
        print(str(self.respuesta))
        self.respuesta_json = self.respuesta.json

    def test_retorna_lista(self, client):
        token_usuario_1 = create_access_token(identity=self.usuario_1.id)
        self.actuar(client, token=token_usuario_1)
        assert isinstance(self.respuesta_json, list)

    def test_retorna_401_request_sin_token(self, client):
        self.actuar(client)
        assert self.respuesta.status_code == 401
