from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.book_service import BookService
from app.schemas.book_schema import book_schema, books_schema
from app.models.user_model import User

book_bp = Blueprint('books', __name__, url_prefix='/api/v1/books')


@book_bp.route('', methods=['GET'])
def get_books():
    """Récupérer la liste des livres avec filtrage, recherche et pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('q', type=str)
    available = request.args.get('available', type=str)

    pagination = BookService.get_paginated_books(
        page=page,
        per_page=per_page,
        search=search,
        available=available
    )

    return jsonify({
        "items": books_schema.dump(pagination.items),
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages,
        "per_page": pagination.per_page,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev
    }), 200


@book_bp.route('', methods=['POST'])
def create_book():
    """Créer un nouveau livre"""
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "Aucune donnée fournie"}), 400

    try:
        new_book = BookService.create_book(json_data)
        return book_schema.dump(new_book), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@book_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Récupérer un livre par son ID"""
    book = BookService.get_book_by_id(book_id)
    if not book:
        return jsonify({"error": "Livre non trouvé"}), 404
    return book_schema.dump(book), 200


@book_bp.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """Mettre à jour un livre"""
    book = BookService.get_book_by_id(book_id)
    if not book:
        return jsonify({"error": "Livre non trouvé"}), 404

    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "Aucune donnée fournie"}), 400

    try:
        updated_book = BookService.update_book(book, json_data)
        return book_schema.dump(updated_book), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@book_bp.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Supprimer un livre"""
    book = BookService.get_book_by_id(book_id)
    if not book:
        return jsonify({"error": "Livre non trouvé"}), 404

    BookService.delete_book(book)
    return jsonify({"message": "Livre supprimé avec succès"}), 200