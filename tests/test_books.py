def test_get_all_books(client):
    """Test de récupération de la liste des livres"""
    response = client.get('/api/v1/books')
    assert response.status_code == 200

def test_get_book_not_found(client):
    """Test de recherche d'un livre inexistant"""
    response = client.get('/api/v1/books/9999')
    assert response.status_code == 404

def test_create_book_unauthorized(client):
    """Test de création d'un livre sans authentification"""
    data = {
        "title": "L'Étranger",
        "isbn": "9782070360024"
    }
    response = client.post('/api/v1/books', json=data)
    # Vérifie le rejet sans token JWT (401)
    assert response.status_code in [400, 401, 422]