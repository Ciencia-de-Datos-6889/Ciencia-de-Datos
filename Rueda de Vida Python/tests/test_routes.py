def test_index_route(client):
    """Prueba que la ruta principal funcione"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Rueda De La Vida" in response.data

def test_agregar_usuario(client):
    """Prueba el envío del formulario"""
    response = client.post('/agregar', data={
        'nombre': 'Test',
        'apellido': 'User',
        'edad': 25,
        'salud': 8,
        'crecimiento_personal': 7,
        'familia_amigos': 9,
        'amor': 6,
        'ocio': 5,
        'trabajo': 8,
        'dinero': 7
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Test" in response.data

def test_descargar_pdf(client):
    """Prueba la descarga de PDF"""
    response = client.get('/descargar_pdf')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/pdf'

def test_eliminar_usuario(client):
    """Prueba que se pueda eliminar un usuario"""
    # Primero crea un usuario de prueba
    client.post('/agregar', data={
        'nombre': 'UsuarioParaEliminar',
        'apellido': 'ApellidoTest',
        'edad': 30,
        'salud': 5,
        'crecimiento_personal': 6,
        'familia_amigos': 7,
        'amor': 8,
        'ocio': 5,
        'trabajo': 6,
        'dinero': 7
    }, follow_redirects=True)
    
    # Luego elimínalo (asumiendo que creará el ID 1)
    response = client.get('/eliminar/1', follow_redirects=True)
    
    # Verificaciones
    assert response.status_code == 200
    assert b"UsuarioParaEliminar" not in response.data  # El nombre no debe aparecer
    assert b"ApellidoTest" not in response.data  # El apellido no debe aparecer