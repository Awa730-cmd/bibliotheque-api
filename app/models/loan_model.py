from app.extensions import db
from datetime import datetime, timezone

class Loan(db.Model):
    __tablename__ = 'loans'

    id = db.Column(db.Integer, primary_key=True)
    borrow_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='borrowed') # Valeurs possibles : 'borrowed', 'returned'
    
    # Clés étrangères
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)

    # Relations pour faciliter la récupération des données
    user = db.relationship('User', backref=db.backref('loans', lazy=True))
    book = db.relationship('Book', backref=db.backref('loans', lazy=True))

    @property
    def is_overdue(self):
        """Retourne True si le livre n'est pas encore rendu et que la date limite est dépassée."""
        if self.returned_at is None and self.due_date:
            # Comparaison avec la date/heure actuelle
            now = datetime.now(timezone.utc) if self.due_date.tzinfo else datetime.utcnow()
            return now > self.due_date
        return False

    def __repr__(self):
        return f"<Loan Book_ID:{self.book_id} User_ID:{self.user_id}>"