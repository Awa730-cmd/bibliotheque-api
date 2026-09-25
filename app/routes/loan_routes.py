from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.loan_service import (
    LoanService,
    LoanConflictException,
    LoanLimitException
)
from app.schemas.loan_schema import loan_schema, loans_schema
from app.models.user_model import User

loan_bp = Blueprint('loans', __name__, url_prefix='/api/v1/loans')


@loan_bp.route('', methods=['POST'])
@jwt_required()
def borrow_book():
    current_user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    book_id = data.get('book_id')

    if not book_id:
        return jsonify({"error": "L'identifiant du livre (book_id) est requis."}), 400

    try:
        loan = LoanService.borrow_book(user_id=current_user_id, book_id=book_id)
        return loan_schema.dump(loan), 201

    except LoanConflictException as e:
        # Retourne 409 Conflict si le livre est déjà emprunté
        return jsonify({"error": str(e)}), 409

    except LoanLimitException as e:
        # Retourne 400 Bad Request si la limite de 3 emprunts est atteinte
        return jsonify({"error": str(e)}), 400

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@loan_bp.route('/<int:loan_id>/return', methods=['PUT', 'POST'])
@jwt_required()
def return_book(loan_id):
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    is_admin_or_staff = (user.role in ['admin', 'staff']) if user else False

    try:
        loan = LoanService.return_book(
            loan_id=loan_id, 
            user_id=current_user_id, 
            is_admin=is_admin_or_staff
        )
        return loan_schema.dump(loan), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@loan_bp.route('', methods=['GET'])
@jwt_required()
def get_loans():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)

    # Un admin/staff voit tous les emprunts, un member voit uniquement les siens
    if user and user.role in ['admin', 'staff']:
        loans = LoanService.get_all_loans()
    else:
        loans = LoanService.get_user_loans(current_user_id)

    return loans_schema.dump(loans), 200