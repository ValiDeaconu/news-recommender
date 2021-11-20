from sqlalchemy.orm import relationship
from model import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False, unique=False)
    mutation_rate = db.Column(db.Float, nullable=False, unique=False, server_default='0.0')

    categories = relationship('UserCategory')

    def __init__(self, username: str, password: str, mutation_rate: float):
        self.username = username
        self.password = password
        self.mutation_rate = mutation_rate

    @staticmethod
    def find_by_id(id: int):
        return User.query.get(id)
    
    @staticmethod
    def find_by_username_and_password(username: str, password: str):
        return User.query.filter(User.username == username).filter(User.password == password).first()

    @staticmethod
    def find_all():
        return User.query.all()