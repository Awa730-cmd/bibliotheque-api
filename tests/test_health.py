def test_health_check_success(client):
    """Vérifie le fonctionnement du healthcheck et la connexion DB"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"

def test_404_not_found(client):
    """Vérifie la réponse du gestionnaire d'erreur 404 global"""
    response = client.get('/api/v1/route-inexistante')
    assert response.status_code == 404
    assert "error" in response.get_json()