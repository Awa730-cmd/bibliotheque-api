from app.extensions import db
from app.models.book import Book

class BookService:

    @staticmethod
    def get_all_books():
        return Book.query.all()

    @staticmethod
    def get_paginated_books(page=1, per_page=10, search=None, available=None):
        query = Book.query

        # 1. Recherche partielle par titre 
        if search:
            search_term = f"%{search}%"
            query = query.filter(Book.title.ilike(search_term))

        # 2. Filtrage par disponibilité
        if available is not None:
            if isinstance(available, str):
                is_available = available.lower() == 'true'
            else:
                is_available = bool(available)
            query = query.filter(Book.available == is_available)

        # 3. Pagination Flask-SQLAlchemy
        return query.paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def get_book_by_id(book_id):
        return Book.query.get(book_id)

    @staticmethod
    def update_book(book, data):
        book.title = data.get('title', book.title)
        book.isbn = data.get('isbn', book.isbn)
        book.year = data.get('year', book.year)
        book.genre = data.get('genre', book.genre)
        book.available = data.get('available', book.available)
        db.session.commit()
        return book

    @staticmethod
    def delete_book(book):
        db.session.delete(book)
        db.session.commit()

    @staticmethod
    def create_book(data):
        new_book = Book(
            title=data.get('title'),
            isbn=data.get('isbn'),
            year=data.get('year'),
            genre=data.get('genre'),
            available=data.get('available', True)
        )
        db.session.add(new_book)
        db.session.commit()
        return new_book