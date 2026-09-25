from app import db
from app.models.user_model import User


class UserService:
    @staticmethod
    def register_user(data):
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'member')

        if User.query.filter_by(username=username).first():
            raise Exception("Ce nom d'utilisateur est déjà pris.")
        if User.query.filter_by(email=email).first():
            raise Exception("Cet email est déjà utilisé.")

        user = User(username=username, email=email, role=role)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def count_users():
        return User.query.count()

    @staticmethod
    def authenticate_user(username, password):
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None
    
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)