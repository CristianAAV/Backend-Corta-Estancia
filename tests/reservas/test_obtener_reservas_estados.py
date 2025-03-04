from datetime import datetime

from flask_jwt_extended import create_access_token
from modelos import Usuario, Propiedad, Reserva, Banco, ReservaSchema, db, TipoUsuario


class TestObtenerReservasEstados:

    def setup_method(self):
        self.usuario_1 = Usuario(usuario='usuario_1', contrasena='123456', tipo_usuario=TipoUsuario.ADMINISTRADOR.value)
        self.usuario_2 = Usuario(usuario='usuario_2', contrasena='123456', tipo_usuario=TipoUsuario.ADMINISTRADOR.value)
        db.session.add(self.usuario_1)
        db.session.add(self.usuario_2)
        db.session.commit()

        self.propiedad_1_usu_1 = Propiedad(nombre_propiedad='propiedad cerca a la quebrada', ciudad='Boyaca', municipio='Paipa',
                              direccion='Vereda Toibita', id_propietario=1, numero_contacto='1234567', banco=Banco.BANCOLOMBIA,
                              numero_cuenta='000033322255599', id_usuario=self.usuario_1.id)
        self.propiedad_2_usu_1 = Propiedad(nombre_propiedad='Apto edificio Alto', ciudad='Bogota',
                              direccion='cra 100#7-21 apto 1302', id_propietario=1, numero_contacto='666777999', banco=Banco.NEQUI,
                              numero_cuenta='3122589635', id_usuario=self.usuario_1.id)
        db.session.add(self.propiedad_1_usu_1)
        db.session.add(self.propiedad_2_usu_1)
        db.session.commit()

        self.reserva_1 = Reserva(nombre='Julio Hernandez', fecha_ingreso=datetime.strptime('2023-01-03', '%Y-%m-%d'),
                          fecha_salida=datetime.strptime('2023-01-06', '%Y-%m-%d'), plataforma_reserva='Booking', total_reserva=568000,
                          comision='74800', id_propiedad=self.propiedad_1_usu_1.id)
        db.session.add(self.reserva_1)
        db.session.commit()
        
        self.reserva_2 = Reserva(nombre='Julio Hernandez', fecha_ingreso=datetime.strptime('2024-05-23', '%Y-%m-%d'),
                          fecha_salida=datetime.strptime('2024-05-28', '%Y-%m-%d'), plataforma_reserva='Booking', total_reserva=568000,
                          comision='74800', id_propiedad=self.propiedad_1_usu_1.id)
        db.session.add(self.reserva_2)
        db.session.commit()

    def teardown_method(self):
        db.session.rollback()
        Propiedad.query.delete()
        Reserva.query.delete()
        Usuario.query.delete()

    def actuar(self, client, id_propiedad, estado=None, token=None):
        headers = {'Content-Type': 'application/json'}
        if token:
            headers.update({'Authorization': f'Bearer {token}'})
        if estado:
             self.respuesta = client.get(f'/propiedades/{id_propiedad}/reservas/{estado}', headers=headers)
        else:
            self.respuesta = client.get(f'/propiedades/{id_propiedad}/reservas', headers=headers)
        self.respuesta_json = self.respuesta.json
    
    def test_retorna_lista_reservas_activas_propiedad(self, client):
        reserva_schema = ReservaSchema()
        token_usuario_1 = create_access_token(identity=self.usuario_1.id)
        self.actuar(client, self.propiedad_1_usu_1.id, estado='activas', token=token_usuario_1)
        assert isinstance(self.respuesta_json, list)
        assert [reserva_schema.dump(self.reserva_2)] == self.respuesta_json
    
    def test_retorna_lista_reservas_pasadas_propiedad(self, client):
        reserva_schema = ReservaSchema()
        token_usuario_1 = create_access_token(identity=self.usuario_1.id)
        self.actuar(client, self.propiedad_1_usu_1.id, estado='pasadas', token=token_usuario_1)
        assert isinstance(self.respuesta_json, list)
        assert [reserva_schema.dump(self.reserva_1)] == self.respuesta_json

    def test_retorna_lista_vacia_si_propiedad_no_tiene_reservas(self, client):
        token_usuario_1 = create_access_token(identity=self.usuario_1.id)
        self.actuar(client, self.propiedad_2_usu_1.id, estado='activas', token=token_usuario_1)
        assert self.respuesta_json == []
    
    def test_retorna_401_lista_reservas_estados(self, client):
        self.actuar(client, 123, estado='pasadas')
        assert self.respuesta.status_code == 401
    
    def test_retorna_404_si_propiedad_no_es_del_usuario(self, client):
        token_usuario_1 = create_access_token(identity=self.usuario_1.id)
        self.actuar(client, 123,  estado='activas', token=token_usuario_1)
        assert self.respuesta.status_code == 404
        assert self.respuesta_json == {"mensaje": "propiedad no encontrada"}