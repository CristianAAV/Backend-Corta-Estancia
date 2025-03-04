import enum
from sqlalchemy import UniqueConstraint
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()
CASCADE_OPTIONS = 'all, delete, delete-orphan'

class TipoMovimiento(enum.Enum):
    INGRESO = 'INGRESO'
    EGRESO = 'EGRESO'


class Banco(enum.Enum):
    BANCO_BBVA                      = 'BANCO_BBVA'
    BANCAMIA                        = 'BANCAMIA'
    BANCO_AGRARIO                   = 'BANCO_AGRARIO'
    BANCO_AV_VILLAS                 = 'BANCO_AV_VILLAS'
    BANCO_CAJA_SOCIAL               = 'BANCO_CAJA_SOCIAL'
    BANCO_CITIBANK                  = 'BANCO_CITIBANK'
    BANCO_COOPERATIVO_COOPCENTRAL   = 'BANCO_COOPERATIVO_COOPCENTRAL'
    BANCO_CREDIFINANCIERA           = 'BANCO_CREDIFINANCIERA'
    DAVIPLATA                       = 'DAVIPLATA'
    BANCO_DE_BOGOTA                 = 'BANCO_DE_BOGOTA'
    BANCO_DE_OCCIDENTE              = 'BANCO_DE_OCCIDENTE'
    BANCO_FALABELLA                 = 'BANCO_FALABELLA'
    BANCO_FINANDINA                 = 'BANCO_FINANDINA'
    BANCO_GNB_SUDAMERIS             = 'BANCO_GNB_SUDAMERIS'
    BANCO_ITAU                      = 'BANCO_ITAU'
    BANCO_MUNDO_MUJER               = 'BANCO_MUNDO_MUJER'
    BANCO_PICHINCHA                 = 'BANCO_PICHINCHA'
    BANCO_POPULAR                   = 'BANCO_POPULAR'
    BANCO_PROCREDIT                 = 'BANCO_PROCREDIT'
    BANCO_SANTANDER                 = 'BANCO_SANTANDER'
    BANCO_SERFINANZA                = 'BANCO_SERFINANZA'
    BANCO_TEQUENDAMA                = 'BANCO_TEQUENDAMA'
    BANCO_WWB                       = 'BANCO_WWB'
    BANCOLDEX                       = 'BANCOLDEX'
    BANCOLOMBIA                     = 'BANCOLOMBIA'
    BANCOMPARTIR                    = 'BANCOMPARTIR'
    BANCOOMEVA                      = 'BANCOOMEVA'
    COLTEFINANCIERA                 = 'COLTEFINANCIERA'
    CONFIAR_COOPERATIVA_FINANCIERA  = 'CONFIAR_COOPERATIVA_FINANCIERA'
    COOFIANTIOQUIA                  = 'COOFIANTIOQUIA'
    COOFINEP_COOPERATIVA_FINANCIERA = 'COOFINEP_COOPERATIVA_FINANCIERA'
    COTRAFA_COOPERATIVA_FINANCIERA  = 'COTRAFA_COOPERATIVA_FINANCIERA'
    FINANCIERA_JURISCOOP            = 'FINANCIERA_JURISCOOP'
    GIROS_Y_FINANZAS_CF             = 'GIROS_Y_FINANZAS_CF'
    IRIS                            = 'IRIS'
    LULO_BANK                       = 'LULO_BANK'
    MOVii                           = 'MOVii'
    SCOTIABANK_COLPATRIA            = 'SCOTIABANK_COLPATRIA'
    SERVIFINANSA                    = 'SERVIFINANSA'
    RAPPIPAY                        = 'RAPPIPAY'
    NEQUI                           = 'NEQUI'
    
class TipoUsuario(enum.Enum):
    ADMINISTRADOR = 'ADMINISTRADOR'
    PROPIETARIO = 'PROPIETARIO'

class TipoDocumento(enum.Enum):
    CEDULA_CIUDADANIA = 'CEDULA_CIUDADANIA'
    CEDULA_EXTRANJERIA = 'CEDULA_EXTRANJERIA'
    NIT = 'NIT'
    PASAPORTE = 'PASAPORTE'
    TARJETA_IDENTIDAD = 'TARJETA_IDENTIDAD'

class Categoria(enum.Enum):
    INGRESOS_POR_RESERVAS = 'INGRESOS_POR_RESERVAS'
    INGRESOS_ADICIONALES_NO_CONTEMPLADOS = 'INGRESOS_ADICIONALES_NO_CONTEMPLADOS'
    EGRESOS_POR_ADMINISTRADOR = 'EGRESOS_POR_ADMINISTRADOR'
    EGRESOS_POR_PLATAFORMA = 'EGRESOS_POR_PLATAFORMA'

class TipoDocumento(enum.Enum):
    CEDULA_CIUDADANIA = 'CEDULA_CIUDADANIA'
    CEDULA_EXTRANJERIA = 'CEDULA_EXTRANJERIA'
    NIT = 'NIT'
    PASAPORTE = 'PASAPORTE'

class Categoria(enum.Enum):
    INGRESOS_POR_RESERVAS = 'INGRESOS_POR_RESERVAS'
    INGRESOS_ADICIONALES_NO_CONTEMPLADOS = 'INGRESOS_ADICIONALES_NO_CONTEMPLADOS'
    EGRESOS_POR_ADMINISTRADOR = 'EGRESOS_POR_ADMINISTRADOR'
    EGRESOS_POR_PLATAFORMA = 'EGRESOS_POR_PLATAFORMA'

class Estado(enum.Enum):
    PROGRAMADO = 'PROGRAMADO'
    VENCIDO = 'VENCIDO'
    REALIZADO = 'REALIZADO'
    NO_REALIZADO = 'NO_REALIZADO'

class TipoMantenimiento(enum.Enum):
    MANTENIMIENTO_AIRES = 'MANTENIMIENTO_AIRES'
    MANTENIMIENTO_ELECTRODOMESTICOS = 'MANTENIMIENTO_ELECTRODOMESTICOS'
    MANTENIMIENTO_PISCINA = 'MANTENIMIENTO_PISCINA'
    MANTENIMIENTO_PROPIEDAD = 'MANTENIMIENTO_PROPIEDAD'

class Propiedad(db.Model):
    __table_args__ = (UniqueConstraint('direccion', 'ciudad', 'municipio', name='unique_address'),)

    id = db.Column(db.Integer, primary_key=True)
    nombre_propiedad = db.Column(db.String(128), nullable=False)
    ciudad = db.Column(db.String(128), nullable=False)
    municipio = db.Column(db.String(128), nullable=True)
    direccion = db.Column(db.String(128), nullable=False)
    id_propietario = db.Column(db.Integer, db.ForeignKey('propietario.id'), nullable=False)
    numero_contacto = db.Column(db.String(15), nullable=False)
    banco = db.Column(db.Enum(Banco), nullable=True)
    numero_cuenta = db.Column(db.String(32), nullable=True)
    movimientos = db.relationship('Movimiento', cascade=CASCADE_OPTIONS)
    mantenimiento = db.relationship('Mantenimiento', cascade=CASCADE_OPTIONS)
    reservas = db.relationship('Reserva', cascade=CASCADE_OPTIONS)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128), nullable=False)
    fecha_ingreso = db.Column(db.DateTime, nullable=False)
    fecha_salida = db.Column(db.DateTime, nullable=False)
    plataforma_reserva = db.Column(db.String(50), nullable=False)
    total_reserva = db.Column(db.Float, nullable=False)
    comision = db.Column(db.Float, nullable=False)
    numero_personas = db.Column(db.Integer, nullable=False, default=0)
    observaciones = db.Column(db.String(128))
    id_propiedad = db.Column(db.Integer, db.ForeignKey('propiedad.id'))
    movimientos = db.relationship('Movimiento', cascade=CASCADE_OPTIONS)


class Movimiento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False)
    categoria = db.Column(db.Enum(Categoria), nullable=False)
    descripcion = db.Column(db.String(128), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    id_reserva = db.Column(db.Integer, db.ForeignKey('reserva.id'), nullable=True)
    tipo_movimiento = db.Column(db.Enum(TipoMovimiento), nullable=False)
    id_propiedad = db.Column(db.Integer, db.ForeignKey('propiedad.id'))
    
class Mantenimiento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    tipo_mantenimiento  = db.Column(db.Enum(TipoMantenimiento), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    descripcion = db.Column(db.String(128), nullable=False)
    estado = db.Column(db.Enum(Estado), nullable=False)
    costo = db.Column(db.Float, nullable=False)
    id_propiedad = db.Column(db.Integer, db.ForeignKey('propiedad.id'))

class Usuario(db.Model):
    __table_args__ = (UniqueConstraint('usuario', name='unique_username'),)
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), nullable=False)
    contrasena = db.Column(db.String(50), nullable=False)
    #se comenta temporalmente para poder hacer login
    tipo_usuario = db.Column(db.Enum(TipoUsuario), nullable=False)
    propiedades = db.relationship('Propiedad', cascade=CASCADE_OPTIONS)

class Propietario(db.Model):
    __table_args__ = (UniqueConstraint('id_usuario', name='unique_usuario'),)
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    nombres = db.Column(db.String(65), nullable=False)
    apellidos = db.Column(db.String(65), nullable=False)
    tipo_documento = db.Column(db.Enum(TipoDocumento), nullable=False)
    documento = db.Column(db.String(200), nullable=False)
    correo = db.Column(db.String(10), nullable=False)
    telefono = db.Column(db.String(10), nullable=False)

class ReservaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Reserva
        include_relationships = True
        include_fk = True
        load_instance = True


class PropiedadSchema(SQLAlchemyAutoSchema):
    banco = fields.Enum(Banco, by_value=True, allow_none=True)
    id_propietario = fields.Integer()
    class Meta:
        model = Propiedad
        include_relationships = True
        load_instance = True

class MovimientoSchema(SQLAlchemyAutoSchema):
    tipo_movimiento = fields.Enum(TipoMovimiento, by_value=True)
    categoria = fields.Enum(Categoria, by_value=True)
    id_reserva = fields.Integer(allow_none=True)
    id_propiedad = fields.Integer()
    class Meta:
        model = Movimiento
        include_relationships = True
        load_instance = True

class MantenimientoSchema(SQLAlchemyAutoSchema):
    tipo_mantenimiento = fields.Enum(TipoMantenimiento, by_value=True)
    estado = fields.Enum(Estado, by_value=True)
    id_propiedad = fields.Integer()
    class Meta:
        model = Mantenimiento
        include_relationships = True
        load_instance = True

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True
        exclude = ('contrasena',)

class PropietarioSchema(SQLAlchemyAutoSchema):
    tipo_documento = fields.Enum(TipoDocumento, by_value=True, allow_none=True)
    class Meta:
        model = Propietario
        include_relationships = True
        load_instance = True
