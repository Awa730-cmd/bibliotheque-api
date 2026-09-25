from flask import Blueprint, request, jsonify
from app.models.user_model import User
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from app.services.user_service import UserService
from app.schemas.user_schema import user_schema

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Inscription d'un nouvel utilisateur
    ---
    tags:
      - Authentification
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
            email:
              type: string
            password:
              type: string
    responses:
      201:
        description: Utilisateur créé avec succès
      400:
        description: Erreur de validation
    """
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "Aucune donnée fournie"}), 400
    
    try:
        user = UserService.register_user(json_data)
        return user_schema.dump(user), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@auth_bp.route('/users/count', methods=['GET'])
def count_users():
    """
    Récupérer le nombre total d'utilisateurs inscrits
    ---
    tags:
      - Utilisateurs
    responses:
      200:
        description: Nombre total d'utilisateurs
    """
    total = User.query.count()
    return jsonify({"total_users": total}), 200

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authentification d'un utilisateur
    ---
    tags:
      - Authentification
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Connexion réussie, retourne le token JWT
      400:
        description: Aucune donnée fournie
      401:
        description: Identifiants invalides
    """
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "Aucune donnée fournie"}), 400

    username = json_data.get('username')
    password = json_data.get('password')

    user = UserService.authenticate_user(username, password)
    if not user:
        return jsonify({"error": "Identifiants invalides"}), 401
    
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user_schema.dump(user)
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Récupérer les informations de l'utilisateur connecté
    ---
    tags:
      - Utilisateurs
    security:
      - Bearer: []
    responses:
      200:
        description: Informations de l'utilisateur
      404:
        description: Utilisateur introuvable
    """
    current_user_id = get_jwt_identity()
    user = UserService.get_user_by_id(current_user_id)
    if not user:
        return jsonify({"error": "Utilisateur introuvable"}), 404
    return user_schema.dump(user), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Rafraîchir le token d'accès
    ---
    tags:
      - Authentification
    security:
      - Bearer: []
    responses:
      200:
        description: Nouveau token d'accès généré
    """
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=str(current_user_id))
    return jsonify({"access_token": new_access_token}), 200