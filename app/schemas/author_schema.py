from app.extensions import ma
from app.models.author_model import Author
from app.schemas.book_schema import BookSchema # Pour afficher les livres de l'auteur

class AuthorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Author
        load_instance = True
    
    # Intégration de la liste des livres de l'auteur en lecture seule
    books = ma.Nested(BookSchema, many=True, dump_only=True)

author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)