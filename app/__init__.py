from flask import Flask, jsonify
from sqlalchemy import text
from app.config import Config
from app.extensions import db, migrate, jwt, ma, cors
from flasgger import Swagger
from app.routes.auth_routes import auth_bp
from app.routes.loan_routes import loan_bp
from app.routes.book_routes import book_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialisation des extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)
    cors.init_app(app)

    # Configuration de base pour Swagger sur /docs/
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda rule: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs/"
    }

    # Initialisation dans l'app
    Swagger(app, config=swagger_config)

    # Route /health durcie avec vérification réelle de la base de données
    @app.route('/health', methods=['GET'])
    def health_check():
        try:
            db.session.execute(text('SELECT 1'))
            return jsonify({
                "status": "healthy",
                "database": "connected"
            }), 200
        except Exception as e:
            return jsonify({
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e)
            }), 500

    # Gestionnaires d'erreurs globaux en JSON propre
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": "Bad Request", "message": str(e.description)}), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not Found", "message": "La ressource demandée n'existe pas."}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": "Method Not Allowed", "message": "La méthode HTTP n'est pas autorisée pour cette route."}), 405

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({"error": "Internal Server Error", "message": "Une erreur interne est survenue sur le serveur."}), 500

    # Enregistrement des blueprints
    app.register_blueprint(book_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(loan_bp)

    return app