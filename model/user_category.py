from sqlalchemy.orm import relationship
from model import db

class UserCategory(db.Model):
    __tablename__ = 'user_category'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category = db.Column(db.String(50), nullable=False, unique=False)

    user = relationship('User', back_populates='categories')

    def __init__(self, user_id: int, category: str):
        self.user_id = user_id
        self.category = category

    @staticmethod
    def find_all_by_user_id(user_id: int):
        return UserCategory.query.filter(UserCategory.user_id == user_id).all()