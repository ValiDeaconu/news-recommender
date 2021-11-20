from sqlalchemy.orm import relationship
from model import db

class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    name = db.Column(db.String(50), nullable=False, unique=True)

    on_days = relationship('MovieOnDay')
    genre = relationship('Genre')

    def __init__(self, genre_id: int, name: str):
        self.genre_id = genre_id
        self.name = name
