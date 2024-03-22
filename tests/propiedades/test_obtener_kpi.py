from flask_jwt_extended import create_access_token
from modelos import Usuario, Propiedad, Reserva, Movimiento, MovimientoSchema, Categoria, TipoMovimiento, Banco, db
from datetime import datetime

from modelos.modelos import TipoUsuario


class TestObtenerMovimientos:

    def setup_method(self):
        self.usuario_1 = Usuario(usuario='usuario_1', contrasena='123456', tipo_usuario=TipoUsuario.ADMINISTRADOR)
        db.session.add(self.usuario_1)
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

        self.movimiento_reserva = Movimiento(fecha=datetime.strptime('2023-01-06', '%Y-%m-%d'), valor=40.0,
                                      categoria=Categoria.INGRESOS_POR_RESERVAS, descripcion='Ingreso por reserva', tipo_movimiento=TipoMovimiento.INGRESO,
                                     id_propiedad=self.propiedad_1_usu_1.id, id_reserva=self.reserva_1.id)
        self.movimiento_comision = Movimiento(fecha=datetime.strptime('2023-01-06', '%Y-%m-%d'), valor=20.0,
                                     categoria=Categoria.EGRESOS_POR_PLATAFORMA, descripcion='egreso por comision', tipo_movimiento=TipoMovimiento.EGRESO,
                                     id_propiedad=self.propiedad_1_usu_1.id, id_reserva=self.reserva_1.id)
        db.session.add(self.movimiento_reserva)
        db.session.add(self.movimiento_comision)
        db.session.commit()

    def teardown_method(self):
        db.session.rollback()
        Propiedad.query.delete()
        Reserva.query.delete()
        Usuario.query.delete()
        Movimiento.query.delete()

    def actuar(self, client, id_propiedad, token=None):
        headers = {'Content-Type': 'application/json'}
        if token:
            headers.update({'Authorization': f'Bearer {token}'})
        self.respuesta = client.get(f'/propiedades/{id_propiedad}/kpi', headers=headers)
        self.respuesta_json = self.respuesta.json

    def test_retorna_cero_si_no_existen_movimientos(self, client):
        token_usuario_1 = create_access_token(identity=self.usuario_1.id)
        self.actuar(client, self.propiedad_2_usu_1.id, token_usuario_1)
        assert self.respuesta_json['valor'] == 0

    def test_retorna_valor_si_existen_movimientos(self, client):
        token_usuario_1 = create_access_token(identity=self.usuario_1.id)
        self.actuar(client, self.propiedad_1_usu_1.id, token_usuario_1)
        assert self.respuesta_json['valor'] == 0.5

    def test_retorna_401_token_no_enviado(self, client):
        self.actuar(client, 123)
        assert self.respuesta.status_code == 401
