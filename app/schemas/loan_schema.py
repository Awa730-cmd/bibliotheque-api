from marshmallow import fields
from app.extensions import ma
from app.models.loan_model import Loan
from app.schemas.book_schema import BookSchema
from app.schemas.user_schema import UserSchema

class LoanSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Loan
        load_instance = True
        include_fk = True

        # Champ virtuel calculé
    overdue = fields.Boolean(attribute="is_overdue")

    # Intégration légère en lecture seule
    book = ma.Nested(BookSchema, only=("id", "title", "isbn"), dump_only=True)
    user = ma.Nested(UserSchema, only=("id", "username"), dump_only=True)

loan_schema = LoanSchema()
loans_schema = LoanSchema(many=True)