from sqlalchemy.orm import relationship
from model import db

from random import sample

class UserKeyword(db.Model):
    __tablename__ = 'user_keyword'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    keyword = db.Column(db.String(50), nullable=False, unique=False)
    liked = db.Column(db.Boolean, nullable=False, unique=False)

    user = relationship('User', back_populates='keywords')

    def __init__(self, user_id: int, keyword: str, liked: bool):
        self.user_id = user_id
        self.keyword = keyword
        self.liked = liked
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def find_all_liked_by_user_id(user_id: int):
        return UserKeyword.query.filter(UserKeyword.user_id == user_id).filter(UserKeyword.liked == True).all()
    
    @staticmethod
    def find_all_disliked_by_user_id(user_id: int):
        return UserKeyword.query.filter(UserKeyword.user_id == user_id).filter(UserKeyword.liked == False).all()

    @staticmethod
    def find_random_sample_for_user(user_id: int, sample_max_size: int = 10):
        keywords = UserKeyword.find_all_liked_by_user_id(user_id)
        size = min(sample_max_size, len(keywords))
        keywords = sample(keywords, size)

        return [k.keyword for k in keywords]
    