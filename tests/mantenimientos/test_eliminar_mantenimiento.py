import json
from flask_jwt_extended import create_access_token
from modelos import Usuario, Propiedad,  Mantenimiento, MantenimientoSchema, Estado, TipoMantenimiento, Banco, db
from datetime import datetime, timedelta

from modelos.modelos import TipoUsuario


class TestEliminarMantenimiento:

    def setup_method(self):
        self.usuario_1 = Usuario(usuario='usuario_1', contrasena='123456', tipo_usuario=TipoUsuario.ADMINISTRADOR.value)
        self.usuario_2 = Usuario(usuario='usuario_2', contrasena='123456', tipo_usuario=TipoUsuario.ADMINISTRADOR.value)
        db.session.add(self.usuario_1)
        db.session.add(self.usuario_2)
        db.session.commit()

        self.propiedad_1_usu_1 = Propiedad(nombre_propiedad='propiedad cerca a la quebrada', ciudad='Boyaca', municipio='Paipa',
                              direccion='Vereda Toibita', id_propietario=1, numero_contacto='1234567', banco=Banco.BANCOLOMBIA,
                              numero_cuenta='000033322255599', id_usuario=self.usuario_1.id)
        db.session.add(self.propiedad_1_usu_1)
        db.session.commit()

        self.mantenimiento_reserva = Mantenimiento(fecha=datetime.strptime('2023-01-06', '%Y-%m-%d'), 
                                     nombre='Mantenimiento de la propiedad por reserva',
                                     tipo_mantenimiento=TipoMantenimiento.MANTENIMIENTO_PROPIEDAD, 
                                     estado=Estado.PROGRAMADO, 
                                     descripcion='Mantenimiento de la propiedad por reserva', 
                                     costo=50000,
                                     id_propiedad=self.propiedad_1_usu_1.id)
        self.mantenimiento_piscina = Mantenimiento(fecha=datetime.strptime('2023-01-06', '%Y-%m-%d'), 
                                     nombre='Mantenimiento de la piscina periodica',
                                     tipo_mantenimiento=TipoMantenimiento.MANTENIMIENTO_PISCINA, 
                                     estado=Estado.NO_REALIZADO, 
                                     descripcion='Mantenimiento de la piscina periodica', 
                                     costo=4000,
                                     id_propiedad=self.propiedad_1_usu_1.id)
        self.mantenimiento_aires = Mantenimiento(
                                     nombre='Mantenimiento de los aires',
                                     fecha=datetime.strptime('2023-01-06', '%Y-%m-%d'), 
                                     tipo_mantenimiento=TipoMantenimiento.MANTENIMIENTO_AIRES, 
                                     descripcion='Mantenimiento de los aires de la propiedad periodicamente', 
                                     estado=Estado.PROGRAMADO, 
                                     costo=7000.0,
                                     id_propiedad=self.propiedad_1_usu_1.id)
        
        db.session.add(self.mantenimiento_reserva)
        db.session.add(self.mantenimiento_piscina)
        db.session.add(self.mantenimiento_aires)
        db.session.commit()

    def teardown_method(self):
        db.session.rollback()
        Propiedad.query.delete()
        Usuario.query.delete()
        Mantenimiento.query.delete()

    def actuar(self, client, id_mantenimiento, token=None):
        headers = {'Content-Type': 'application/json'}
        if token:
            headers.update({'Authorization': f'Bearer {token}'})
        self.respuesta = client.delete(f'/mantenimientos/{id_mantenimiento}', headers=headers)

    def test_retorna_204_mantenimiento_pertenece_a_propiedad_usuario_token(self, client, mock_datetime_now):
        mock_datetime_now(self.mantenimiento_piscina.fecha)
        token_usuario_1 = create_access_token(identity=self.usuario_1.id)
        self.actuar(client, self.mantenimiento_piscina.id, token=token_usuario_1)
        assert self.respuesta.status_code == 204

    def test_retorna_404_si_mantenimiento_no_es_de_propiedad_del_usuario(self, client):
        token_usuario_2 = create_access_token(identity=self.usuario_2.id)
        self.actuar(client, self.mantenimiento_piscina.id, token=token_usuario_2)
        assert self.respuesta.status_code == 404
        assert self.respuesta.json == {'mensaje': 'Mantenimiento no encontrado'}

    def test_retorna_401_token_no_enviado(self, client):
        self.actuar(client, 123)
        assert self.respuesta.status_code == 401

    def test_retorna_204_eliminar_mantenimiento_categoria_reseva(self, client, mock_datetime_now):
        mock_datetime_now(self.mantenimiento_reserva.fecha)
        token_usuario_1 = create_access_token(identity=self.usuario_1.id)
        self.actuar(client, self.mantenimiento_reserva.id, token=token_usuario_1)
        assert self.respuesta.status_code == 204

    def test_retorna_204_eliminar_mantenimiento_piscina(self, client, mock_datetime_now):
        mock_datetime_now(self.mantenimiento_piscina.fecha)
        token_usuario_1 = create_access_token(identity=self.usuario_1.id)
        self.actuar(client, self.mantenimiento_piscina.id, token=token_usuario_1)
        assert self.respuesta.status_code == 204

    def test_retorna_400_eliminar_mantenimiento_mes_anterior(self, client, mock_datetime_now):
        mock_datetime_now(self.mantenimiento_piscina.fecha + timedelta(days=31))
        token_usuario_1 = create_access_token(identity=self.usuario_1.id)
        self.actuar(client, self.mantenimiento_piscina.id, token=token_usuario_1)
        assert self.respuesta.status_code == 400
