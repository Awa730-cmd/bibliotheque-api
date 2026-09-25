from datetime import datetime
from app.extensions import db
from app.models.loan_model import Loan
from app.models.book import Book

# --- Exceptions personnalisées pour la gestion HTTP ---
class LoanConflictException(Exception):
    """Levée quand le livre est déjà emprunté (Erreur 409 Conflict)"""
    pass

class LoanLimitException(Exception):
    """Levée quand l'utilisateur dépasse la limite d'emprunts (Erreur 400 Bad Request)"""
    pass


class LoanService:

    @staticmethod
    def borrow_book(user_id, book_id):
        # 1. Vérification de l'existence du livre
        book = Book.query.get(book_id)
        if not book:
            raise ValueError("Livre introuvable.")

        # 2. Règle : Vérification de la disponibilité du livre (409 Conflict)
        if not book.available:
            raise LoanConflictException("Ce livre n'est pas disponible actuellement.")

        # 3. Règle : Limite maximale de 3 emprunts actifs par utilisateur (400 Bad Request)
        active_loans_count = Loan.query.filter_by(user_id=user_id, status='borrowed').count()
        if active_loans_count >= 3:
            raise LoanLimitException("Vous avez atteint la limite maximale de 3 emprunts actifs.")

        # 4. Création de l'emprunt
        book.available = False
        new_loan = Loan(
            user_id=user_id,
            book_id=book_id,
            borrow_date=datetime.utcnow(),
            status='borrowed'
        )

        db.session.add(new_loan)
        db.session.commit()
        return new_loan

    @staticmethod
    def return_book(loan_id, user_id, is_admin=False):
        loan = Loan.query.get(loan_id)
        if not loan:
            raise ValueError("Emprunt introuvable.")
        
        if not is_admin and loan.user_id != user_id:
            raise ValueError("Action non autorisée sur cet emprunt.")
            
        if loan.status == 'returned':
            raise ValueError("Ce livre a déjà été restitué.")

        loan.status = 'returned'
        loan.return_date = datetime.utcnow()

        book = Book.query.get(loan.book_id)
        if book:
            book.available = True

        db.session.commit()
        return loan

    @staticmethod
    def get_user_loans(user_id):
        return Loan.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_all_loans():
        return Loan.query.all()