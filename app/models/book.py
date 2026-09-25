from app.extensions import db
from app.models.author_model import Author



class Book(db.Model):

    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    available = db.Column(db.Boolean, default=True)

    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=True)
    author = db.relationship('Author', backref='books')

    def __repr__(self):
        return f"<Book {self.title}>"