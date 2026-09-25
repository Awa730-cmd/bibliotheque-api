def test_count_users_empty(client):
    """Vérifie le compteur d'utilisateurs au démarrage"""
    response = client.get('/api/v1/auth/users/count')
    assert response.status_code == 200
    # Vérifie la présence de la clé total_users dans la réponse
    assert "total_users" in response.get_json()

def test_register_user_success(client):
    """Test d'inscription réussie"""
    data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "Password123!"
    }
    response = client.post('/api/v1/auth/register', json=data)
    assert response.status_code == 201

def test_register_user_missing_data(client):
    """Test d'inscription avec requête vide"""
    response = client.post('/api/v1/auth/register', json={})
    assert response.status_code == 400

def test_login_success(client):
    """Test de connexion réussie et récupération du token JWT"""
    client.post('/api/v1/auth/register', json={
        "username": "logintest",
        "email": "logintest@example.com",
        "password": "Password123!"
    })
    
    response = client.post('/api/v1/auth/login', json={
        "username": "logintest",
        "password": "Password123!"
    })
    assert response.status_code == 200
    assert "access_token" in response.get_json()

def test_login_invalid_credentials(client):
    """Test de connexion avec identifiants invalides"""
    response = client.post('/api/v1/auth/login', json={
        "username": "nonexistent",
        "password": "wrongpassword"
    })
    assert response.status_code in [400, 401]

def test_get_current_user_success(client):
    """Test d'accès à la route /me avec un token valide"""
    client.post('/api/v1/auth/register', json={
        "username": "profileuser",
        "email": "profileuser@example.com",
        "password": "Password123!"
    })
    login_res = client.post('/api/v1/auth/login', json={
        "username": "profileuser",
        "password": "Password123!"
    })
    token = login_res.get_json().get("access_token")

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get('/api/v1/auth/me', headers=headers)
    assert response.status_code == 200

def test_get_current_user_unauthorized(client):
    """Test d'accès à la route /me sans token"""
    response = client.get('/api/v1/auth/me')
    assert response.status_code == 401