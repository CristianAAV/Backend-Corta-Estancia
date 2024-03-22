from flask_jwt_extended import create_access_token
from modelos import Usuario, db
from modelos.modelos import TipoUsuario

content_type = 'application/json'

def test_bancos(client):
    usuario_1 = Usuario(usuario='usuario_1', contrasena='123456', tipo_usuario=TipoUsuario.ADMINISTRADOR.value)
    db.session.add(usuario_1)
    db.session.commit()

    token_usuario_1 = create_access_token(identity=usuario_1.id)
    headers = {'Content-Type': content_type, 'Authorization': f'Bearer {token_usuario_1}'}
    response = client.get('/bancos', headers=headers)
    response_json = response.json
    assert isinstance(response_json, list)
    assert len(response_json) == 41

def test_categorias(client):
    usuario_1 = Usuario(usuario='usuario_1', contrasena='123456', tipo_usuario=TipoUsuario.ADMINISTRADOR.value)
    db.session.add(usuario_1)
    db.session.commit()

    token_usuario_1 = create_access_token(identity=usuario_1.id)
    headers = {'Content-Type': content_type, 'Authorization': f'Bearer {token_usuario_1}'}
    response = client.get('/categorias', headers=headers)
    response_json = response.json
    assert isinstance(response_json, list)
    assert len(response_json) == 4

def test_estados(client):
    usuario_1 = Usuario(usuario='usuario_1', contrasena='123456', tipo_usuario=TipoUsuario.ADMINISTRADOR.value)
    db.session.add(usuario_1)
    db.session.commit()

    token_usuario_1 = create_access_token(identity=usuario_1.id)
    headers = {'Content-Type': content_type, 'Authorization': f'Bearer {token_usuario_1}'}
    response = client.get('/estados', headers=headers)
    response_json = response.json
    assert isinstance(response_json, list)
    assert len(response_json) == 4


def test_tipo_movimientos(client):
    usuario_1 = Usuario(usuario='usuario_1', contrasena='123456', tipo_usuario=TipoUsuario.ADMINISTRADOR.value)
    db.session.add(usuario_1)
    db.session.commit()

    token_usuario_1 = create_access_token(identity=usuario_1.id)
    headers = {'Content-Type': content_type, 'Authorization': f'Bearer {token_usuario_1}'}
    response = client.get('/tipo-movimientos', headers=headers)
    response_json = response.json
    assert isinstance(response_json, list)
    assert len(response_json) == 2
    assert 'INGRESO' in response_json
    assert 'EGRESO' in response_json

def test_tipo_mantenimientos(client):
    usuario_1 = Usuario(usuario='usuario_1', contrasena='123456', tipo_usuario=TipoUsuario.ADMINISTRADOR.value)
    db.session.add(usuario_1)
    db.session.commit()

    token_usuario_1 = create_access_token(identity=usuario_1.id)
    headers = {'Content-Type': content_type, 'Authorization': f'Bearer {token_usuario_1}'}
    response = client.get('/tipo-mantenimientos', headers=headers)
    response_json = response.json
    assert isinstance(response_json, list)
    assert len(response_json) == 4
    assert 'MANTENIMIENTO_PISCINA' in response_json
    assert 'MANTENIMIENTO_PROPIEDAD' in response_json
