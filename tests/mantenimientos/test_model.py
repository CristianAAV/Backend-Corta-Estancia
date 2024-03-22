from datetime import datetime
from unittest import TestCase
from modelos import Usuario, Propiedad, Mantenimiento, Banco, TipoMantenimiento, Estado, db
from modelos.modelos import TipoUsuario


class TestModeloMantenimiento(TestCase):

    def setUp(self):
        usuario = Usuario(usuario="usuario_test", contrasena='123456', tipo_usuario=TipoUsuario.ADMINISTRADOR.value)
        db.session.add(usuario)
        db.session.commit()

        self.propiedad = Propiedad(nombre_propiedad='propiedad cerca a la quebrada', ciudad='Boyaca', municipio='Paipa',
                              direccion='Vereda Toibita', id_propietario=1, numero_contacto='1234567', banco=Banco.BANCOLOMBIA,
                              numero_cuenta='000033322255599', id_usuario=usuario.id)
        db.session.add(self.propiedad)
        db.session.commit()

        self.mantenimiento = Mantenimiento(fecha=datetime.strptime('2023-01-06', '%Y-%m-%d'), 
                                     nombre='Mantenimiento de la propiedad por reserva',
                                     tipo_mantenimiento=TipoMantenimiento.MANTENIMIENTO_PROPIEDAD, 
                                     estado=Estado.REALIZADO, 
                                     descripcion='Mantenimiento de la propiedad por reserva', 
                                     costo=50000,
                                     id_propiedad=self.propiedad.id)
        
        db.session.add(self.mantenimiento)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()
        Usuario.query.delete()
        Propiedad.query.delete()
        Mantenimiento.query.delete()

    def test_solo_un_registro_es_creado(self):
        mantenimientos_en_db = Mantenimiento.query.all()
        self.assertEqual(len(mantenimientos_en_db), 1)

    def test_registro_contiene_info_correcta(self):
        mantenimiento_db = Mantenimiento.query.filter(Mantenimiento.id == self.mantenimiento.id).first()
        self.assertEqual(mantenimiento_db.costo, 50000.0)
        self.assertEqual(mantenimiento_db.tipo_mantenimiento, TipoMantenimiento.MANTENIMIENTO_PROPIEDAD)
        self.assertEqual(mantenimiento_db.estado, Estado.REALIZADO)
        self.assertIn('2023-01-06', str(mantenimiento_db.fecha))
        self.assertEqual(mantenimiento_db.id_propiedad, self.propiedad.id)