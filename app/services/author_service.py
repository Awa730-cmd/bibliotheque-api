from app.extensions import db
from app.models.author_model import Author

class AuthorService:
    @staticmethod
    def get_all_authors():
        return Author.query.all()

    @staticmethod
    def get_author_by_id(author_id):
        return Author.query.get(author_id)

    @staticmethod
    def create_author(data):
        new_author = Author(
            name=data.get('name'),
            nationality=data.get('nationality'),
            bio=data.get('bio')
        )
        db.session.add(new_author)
        db.session.commit()
        return new_author

    @staticmethod
    def delete_author(author):
        db.session.delete(author)
        db.session.commit()